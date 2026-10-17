import ts from "typescript";
import {
  finish, LimitLog, type Answer, type ChainStep, type Link, type ModuleMap, type Node,
  type TestCase, type TestsAnswer,
} from "./answer.ts";
import { stepsOf } from "./flow.ts";
import {
  analyzeCall, callSitesIn, computedCallsIn, findCallers, isTestFile, lookupImplementation, resolvedDeclaration,
  type AnalysisContext,
} from "./links.ts";
import {
  belongsTo, definitionKind, definitionsIn, isFunctionLikeDeclaration, lineOf, located, nearestFunction, nodeOf,
  placeableKind, propertyNameText, searchableDefinitions, type Definition,
} from "./nodes.ts";
import { createProject, type Project } from "./project.ts";
import { siblingTable } from "./siblings.ts";

export interface Options {
  command: string;
  query: string[];
  project: string[];
  root: string;
  tests: string[];
  siblings: string[];
  up?: number;
  down?: number;
  fakeRule?: "count" | "exclude";
  file?: string;
  perFunction: boolean;
  json?: boolean;
}

interface Session {
  project: Project;
  limits: LimitLog;
  context: AnalysisContext;
  definitions: Definition[];
  index: Map<string, Definition>;
}

const normalize = (text: string) => text.replace(/[\t ]+$/gm, "").replace(/\s+$/, "");
const codeText = (text: string) => normalize(text).replace(/;$/, "");
const keyOf = (node: { file: string; line: number }) => `${node.file}:${node.line}`;
const isNameQuery = (query: string) => /^[A-Za-z_$][\w$]*(\.[A-Za-z_$][\w$]*)?$/.test(query);

/** The places a definition answers to: its own line, and the line of the function that implements it. */
function keysOf(project: Project, definition: Definition): string[] {
  const keys = [keyOf(definition.node)];
  if (definition.implementation) keys.push(keyOf(located(project, definition.implementation)));
  return keys;
}

function buildIndex(project: Project, definitions: Definition[]): Map<string, Definition> {
  const index = new Map<string, Definition>();
  for (const definition of definitions) {
    for (const key of keysOf(project, definition)) {
      const existing = index.get(key);
      if (!existing || (!placeableKind(existing.node.kind) && placeableKind(definition.node.kind))) index.set(key, definition);
    }
  }
  return index;
}

function definitionsByName(session: Session, query: string): Definition[] {
  return session.definitions.filter(definition =>
    definition.node.name === query || definition.node.name.endsWith(`.${query}`));
}

/**
 * The modules a namespace qualifier stands for: `export * as Permission from "./permission"` and
 * `import * as Permission from "./permission"` both put the module's symbol where the qualifier is read.
 */
function namespaceModules(session: Session, qualifier: string): ts.SourceFile[] {
  const checker = session.project.checker;
  const modules = new Map<string, ts.SourceFile>();
  for (const file of session.project.files) {
    const visit = (node: ts.Node): void => {
      if (ts.isIdentifier(node) && node.text === qualifier) {
        const symbol = checker.getSymbolAtLocation(node);
        const target = symbol && symbol.flags & ts.SymbolFlags.Alias ? checker.getAliasedSymbol(symbol) : symbol;
        for (const declaration of target?.declarations ?? []) {
          if (ts.isSourceFile(declaration) && session.project.isSource(declaration)) {
            modules.set(declaration.fileName, declaration);
          }
        }
      }
      ts.forEachChild(node, visit);
    };
    visit(file);
  }
  return [...modules.values()];
}

/** A declaration whose written name is `name`: a member, a variable, a function or a property. */
function declaresName(node: ts.Node, name: string): boolean {
  const written = (node as { name?: ts.Node }).name;
  if (!written || propertyNameText(written as ts.PropertyName) !== name) return false;
  return ts.isFunctionDeclaration(node) || ts.isClassDeclaration(node) || ts.isMethodDeclaration(node) ||
    ts.isMethodSignature(node) || ts.isPropertyDeclaration(node) || ts.isPropertySignature(node) ||
    ts.isGetAccessorDeclaration(node) || ts.isSetAccessorDeclaration(node) ||
    ts.isVariableDeclaration(node) || ts.isPropertyAssignment(node);
}

function nodeFor(project: Project, declaration: ts.Declaration): Node {
  const written = nodeOf(project, declaration);
  const kind = definitionKind(project, declaration);
  return kind ? { ...written, kind } : written;
}

/**
 * `Permission.assert` names a member of the module the qualifier re-exports. The module's own members with
 * that name are the definition, and each member's implementation lookup adds the consts written for it, so
 * `where Permission.assert` finds the layer's `assert` rather than an unrelated `….permission.assert`.
 */
function qualifiedMatches(session: Session, query: string): Node[] | undefined {
  const parts = query.split(".");
  if (parts.length < 2) return undefined;
  const qualifier = parts[0]!;
  const member = parts[parts.length - 1]!;
  const modules = namespaceModules(session, qualifier);
  if (!modules.length) return undefined;
  const found = new Map<string, Node>();
  const add = (declaration: ts.Declaration | undefined): void => {
    if (!declaration || !session.project.isSource(declaration)) return;
    const node = nodeFor(session.project, declaration);
    found.set(keyOf(node), node);
  };
  for (const source of modules) {
    const visit = (node: ts.Node): void => {
      if (declaresName(node, member)) {
        const declaration = node as ts.Declaration;
        add(declaration);
        for (const implementation of lookupImplementation(session.project, declaration).implementations) {
          add(implementation);
        }
      }
      ts.forEachChild(node, visit);
    };
    visit(source);
  }
  return [...found.values()];
}

function firstLine(text: string): string {
  const line = text.split("\n")[0]!.trim();
  return line.length > 60 ? `${line.slice(0, 57)}...` : line;
}

function matchesByText(session: Session, query: string): Node[] {
  const wanted = codeText(query);
  const found = new Map<string, Node>();
  for (const file of session.project.files) {
    const visit = (node: ts.Node): void => {
      if (!ts.isToken(node) && codeText(node.getText(file)) === wanted) {
        const enclosing = nearestFunction(node);
        const match = enclosing
          ? nodeOf(session.project, enclosing)
          : { ...located(session.project, node), name: firstLine(node.getText(file)), kind: "other" as const };
        found.set(keyOf(match), match);
      }
      ts.forEachChild(node, visit);
    };
    visit(file);
  }
  return [...found.values()];
}

/** The nodes whose written comments belong to a definition: the declaration, and the statement it sits in. */
function documentedNodes(declaration: ts.Node): ts.Node[] {
  const nodes = [declaration];
  for (let parent = declaration.parent; parent && !ts.isSourceFile(parent); parent = parent.parent) {
    if (ts.isStatement(parent) || ts.isClassElement(parent) || ts.isInterfaceDeclaration(parent)) {
      nodes.push(parent);
      break;
    }
  }
  return nodes;
}

/** What a definition says in writing: its name, plus the comments and string literals around and inside it. */
function writtenText(definition: Definition): string {
  const source = definition.declaration.getSourceFile();
  const written: string[] = [];
  const commentTexts = (ranges: ts.CommentRange[] | undefined): string[] =>
    (ranges ?? []).map(range => source.text.slice(range.pos, range.end).toLowerCase());
  for (const node of documentedNodes(definition.declaration)) written.push(...commentTexts(ts.getLeadingCommentRanges(source.text, node.getFullStart())));
  written.push(...commentTexts(ts.getTrailingCommentRanges(source.text, definition.declaration.getEnd())));
  const scanner = ts.createScanner(
    ts.ScriptTarget.Latest, false, source.languageVariant ?? ts.LanguageVariant.Standard,
    source.text.slice(definition.declaration.getStart(source), definition.declaration.getEnd()),
  );
  for (let token = scanner.scan(); token !== ts.SyntaxKind.EndOfFileToken; token = scanner.scan()) {
    if (token === ts.SyntaxKind.SingleLineCommentTrivia || token === ts.SyntaxKind.MultiLineCommentTrivia ||
        token === ts.SyntaxKind.StringLiteral || token === ts.SyntaxKind.NoSubstitutionTemplateLiteral) {
      written.push(scanner.getTokenText().toLowerCase());
    }
  }
  return [definition.node.name.toLowerCase(), ...written].join("\n");
}

function matchesByDescription(session: Session, query: string): Node[] {
  const wanted = query.toLowerCase().trim();
  const words = wanted.split(/\s+/).filter(Boolean);
  const scored: { node: Node; score: number }[] = [];
  for (const definition of session.definitions) {
    const name = definition.node.name.toLowerCase();
    const written = writtenText(definition);
    const score = name.includes(wanted) ? 3
      : words.every(word => name.includes(word)) ? 2
      : words.every(word => written.includes(word)) ? 1
      : 0;
    if (score) scored.push({ node: definition.node, score });
  }
  const best = scored.reduce((most, entry) => Math.max(most, entry.score), 0);
  if (!best) return [];
  // Only the best rank is shown, so the ranks below it are named rather than dropped in silence.
  const weaker = scored.filter(entry => entry.score !== best);
  if (weaker.length) {
    const named = weaker.slice(0, 5).map(entry => `${entry.node.name} (${entry.node.file}:${entry.node.line})`);
    session.limits.addReason("other", weaker[0]!.node,
      `${weaker.length} weaker match(es) below the best rank ${best} were left out: ${named.join(", ")}`);
  }
  return scored.filter(entry => entry.score === best).map(entry => entry.node);
}

interface TestRecord {
  node: Node;
  body: ts.Node;
}

function testRecords(session: Session): TestRecord[] {
  const records: TestRecord[] = [];
  for (const file of session.project.files) {
    if (!isTestFile(session.context.testPatterns, session.project.pathOf(file)!)) continue;
    const visit = (node: ts.Node): void => {
      if (ts.isCallExpression(node)) {
        const callee = node.expression.getText().split(".").pop();
        const title = node.arguments[0];
        const body = node.arguments[1];
        if ((callee === "test" || callee === "it") && title && ts.isStringLiteralLike(title) && body &&
            (ts.isArrowFunction(body) || ts.isFunctionExpression(body))) {
          records.push({
            body,
            node: { ...located(session.project, node), name: title.text, kind: "arrow" },
          });
        }
      }
      ts.forEachChild(node, visit);
    };
    visit(file);
  }
  return records.sort((left, right) => keyOf(left.node).localeCompare(keyOf(right.node)));
}

function throughFakeOf(path: Link[]): boolean {
  return path.some(link => link.kind === "service-call" && link.candidates.some(candidate => candidate.testFake));
}

interface Reach {
  node: Node;
  path: Link[];
}

/** How many functions one walk may expand before it stops and says so. */
const walkVisitBudget = 2000;

function reachableFrom(session: Session, start: ts.Node, from: Node): Map<string, Reach> {
  const reached = new Map<string, Reach>();
  const queue: { declaration: ts.Node; from: Node; path: Link[] }[] = [{ declaration: start, from, path: [] }];
  let visited = 0;
  let lastVisited: ts.Node | undefined;
  while (queue.length && visited < walkVisitBudget) {
    const current = queue.shift()!;
    visited++;
    lastVisited = current.declaration;
    for (const site of callSitesIn(session.project, current.declaration.getSourceFile())) {
      if (!belongsTo(session.project, site.node, current.declaration)) continue;
      const link = analyzeCall(session.project, site, session.context);
      if (current.path.length === 0) link.from = current.from;
      if (!link.to) continue;
      const key = keyOf(link.to);
      if (reached.has(key)) continue;
      const path = [...current.path, link];
      reached.set(key, { node: link.to, path });
      const definition = session.index.get(key);
      if (definition && placeableKind(definition.node.kind)) {
        queue.push({ declaration: walkTarget(definition), from: link.to, path });
      }
    }
  }
  // A walk that stopped on its visit budget leaves functions unvisited, and the tests behind them unfound.
  if (queue.length && lastVisited) {
    session.limits.addReason("other", located(session.project, lastVisited),
      `the walk stopped after its budget of ${walkVisitBudget} visited functions; ` +
      `${queue.length} function(s) reached but not expanded, and no test was searched through them`);
  }
  return reached;
}

/** The function that carries a definition's body: its initializer, or the body a wrapper call was given. */
function walkTarget(definition: Definition): ts.Node {
  return definition.implementation ?? definition.declaration;
}

/**
 * The place a line names when no definition begins there: the function written around it — a body inside a
 * named function belongs to that function — or the module's top level when the line is a call no function and
 * no declaration carries. Every node a link names as its `from` answers to one of these, so `callees` on it
 * can be asked.
 */
function placeAround(session: Session, file: string, line: number): Definition | undefined {
  const project = session.project;
  const source = project.sourceOf({ file });
  if (!source) return undefined;
  let inner: ts.Node | undefined;
  let topLevel: ts.Node | undefined;
  const visit = (node: ts.Node): void => {
    if (isFunctionLikeDeclaration(node)) {
      const span = located(project, node);
      if (span.line <= line && line <= (span.endLine ?? span.line)) inner = node;
    }
    else if (!topLevel && (ts.isCallExpression(node) || ts.isNewExpression(node)) &&
             lineOf(source, node.getStart(source)) === line && belongsTo(project, node, source)) {
      topLevel = node;
    }
    ts.forEachChild(node, visit);
  };
  visit(source);
  if (inner) {
    const written = nodeOf(project, inner);
    return {
      node: { ...written, kind: definitionKind(project, inner) ?? written.kind },
      declaration: inner as ts.Declaration,
    };
  }
  if (topLevel) return { node: { ...located(project, topLevel), name: "<module>", kind: "other" }, declaration: source };
  return undefined;
}

function placeFor(session: Session, argument: string): { place?: Definition; candidates: Definition[] } {
  const position = /^(.*):(\d+)$/.exec(argument);
  if (position) {
    const file = position[1]!;
    const line = Number(position[2]);
    const definitions = session.definitions.filter(definition => keysOf(session.project, definition).includes(`${file}:${line}`));
    const place = definitions.find(definition => placeableKind(definition.node.kind)) ?? definitions[0];
    return { place: place ?? placeAround(session, file, line), candidates: [] };
  }
  const candidates = definitionsByName(session, argument);
  return candidates.length === 1 ? { place: candidates[0], candidates } : { place: undefined, candidates };
}

function isExported(session: Session, declaration: ts.Declaration): boolean {
  const checker = session.project.checker;
  const modifiers = (declaration as { modifiers?: ts.NodeArray<ts.ModifierLike> }).modifiers;
  if (modifiers?.some(modifier => modifier.kind === ts.SyntaxKind.ExportKeyword)) return true;
  const file = declaration.getSourceFile();
  const moduleSymbol = checker.getSymbolAtLocation(file);
  const name = (declaration as { name?: ts.Node }).name;
  const symbol = name ? checker.getSymbolAtLocation(name) : undefined;
  if (!moduleSymbol || !symbol) return false;
  const resolved = symbol.flags & ts.SymbolFlags.Alias ? checker.getAliasedSymbol(symbol) : symbol;
  return checker.getExportsOfModule(moduleSymbol).some(exported => exported === symbol || exported === resolved);
}

function moduleFiles(session: Session, paths: string[]): ts.SourceFile[] {
  const wanted = new Set<string>();
  for (const path of paths) {
    const trimmed = path.replace(/^\.\/+/, "").replace(/\/+$/, "");
    if (trimmed === "" || trimmed === ".") {
      for (const file of session.project.files) wanted.add(session.project.pathOf(file)!);
      continue;
    }
    const source = session.project.sourceOf({ file: trimmed });
    if (source) {
      wanted.add(trimmed);
      continue;
    }
    const prefix = `${trimmed}/`;
    let found = false;
    for (const file of session.project.files) {
      const path2 = session.project.pathOf(file)!;
      if (path2 === trimmed || path2.startsWith(prefix)) {
        wanted.add(path2);
        found = true;
      }
    }
    if (!found) {
      session.limits.addReason("not-found", undefined, `${path} is not a file or folder of this program`);
    }
  }
  return session.project.files.filter(file => wanted.has(session.project.pathOf(file)!));
}

/** A member chosen at run time has no static target, so the place where the walk could not go is named. */
function dynamicLimitsIn(session: Session, file: ts.SourceFile, inside: (node: ts.Node) => boolean): void {
  for (const node of computedCallsIn(file)) {
    if (!inside(node)) continue;
    session.limits.addReason("dynamic", located(session.project, node), `${node.getText()} names its callee at run time`);
  }
}

/** Calls made inside one place, including the bodies written straight into calls inside it. */
function calleesOf(session: Session, implementation: ts.Node): Link[] {
  const file = implementation.getSourceFile();
  dynamicLimitsIn(session, file, node => belongsTo(session.project, node, implementation));
  return callSitesIn(session.project, file)
    .filter(site => belongsTo(session.project, site.node, implementation))
    .map(site => analyzeCall(session.project, site, session.context));
}

/**
 * The place a link names but no name stands for: a body written straight into a call belongs to the
 * `const x = Effect.fn(…)(body)` that holds it, and walking on from it adds no call link of its own.
 */
function definitionAround(session: Session, node: ts.Node | undefined): Definition | undefined {
  for (let current = node; current; current = current.parent) {
    const definition = session.index.get(keyOf(located(session.project, current)));
    if (definition && placeableKind(definition.node.kind)) return definition;
  }
  return undefined;
}

/**
 * The chain one level at a time, so the route a function is first shown on is its shortest route, and a
 * function reached again on a longer one keeps the links it has from the shorter route. Each step hangs
 * what the next level found on it; `shown` is where each function was first expanded.
 */
interface Frontier {
  /** The body to walk: a place's implementation, or the definition a step leads to. */
  body: ts.Node;
  /** The step whose children this level's steps are. */
  step?: ChainStep;
}

function chainDown(session: Session, declaration: ts.Node, level: number, maxDepth: number, expanded: Map<string, Node>): ChainStep[] {
  const steps: ChainStep[] = [];
  let frontier: Frontier[] = [{ body: declaration }];
  for (let depth = level; frontier.length && depth <= maxDepth; depth++) {
    const next: Frontier[] = [];
    for (const item of frontier) {
      for (const link of calleesOf(session, item.body)) {
        const step: ChainStep = { level: depth, link, children: [] };
        const target = link.to;
        if (target) {
          const firstSeen = expanded.get(keyOf(target));
          if (firstSeen) {
            step.stop = { reason: "seen", ref: { file: firstSeen.file, line: firstSeen.line } };
          } else {
            expanded.set(keyOf(target), target);
            const reached = depth < maxDepth ? session.index.get(keyOf(target)) : undefined;
            if (reached && placeableKind(reached.node.kind)) {
              next.push({ body: walkTarget(reached), step });
            }
          }
        }
        if (depth === maxDepth && !step.stop) step.stop = { reason: "depth" };
        // Only the steps of the first level are the answer; the rest hang on the step that reached them.
        if (item.step) item.step.children.push(step);
        else steps.push(step);
      }
    }
    frontier = next;
  }
  return steps;
}

function chainUp(session: Session, place: Definition, level: number, maxDepth: number, expanded: Map<string, Node>): ChainStep[] {
  const steps: ChainStep[] = [];
  let frontier: { definition: Definition; step?: ChainStep }[] = [{ definition: place }];
  for (let depth = level; frontier.length && depth <= maxDepth; depth++) {
    const next: { definition: Definition; step: ChainStep }[] = [];
    for (const item of frontier) {
      const current = item.definition;
      for (const entry of findCallers(session.project, current.declaration, session.context)) {
        const link = entry.link;
        const joined = link.to && keyOf(link.to) === keyOf(current.node);
        if (!joined) {
          session.limits.addReason("other", link.site, `a call to ${current.node.name} did not resolve to this one implementation and was not expanded`);
          continue;
        }
        const step: ChainStep = { level: depth, link, children: [] };
        const target = link.from;
        const firstSeen = expanded.get(keyOf(target));
        if (firstSeen) {
          step.stop = { reason: "seen", ref: { file: firstSeen.file, line: firstSeen.line } };
        } else {
          expanded.set(keyOf(target), target);
          const reached = session.index.get(keyOf(target)) ??
            (entry.enclosing ? definitionAround(session, entry.enclosing) : undefined);
          if (depth < maxDepth && entry.enclosing && reached && placeableKind(reached.node.kind)) {
            next.push({ definition: reached, step });
          }
        }
        if (depth === maxDepth && !step.stop) step.stop = { reason: "depth" };
        // Only the steps of the first level are the answer; the rest hang on the step that reached them.
        if (item.step) item.step.children.push(step);
        else steps.push(step);
      }
    }
    frontier = next;
  }
  return steps;
}

function siblingMembers(session: Session, globs: string[]): string[] {
  return session.project.files
    .map(file => session.project.pathOf(file)!)
    .filter(path => globs.some(glob => new Bun.Glob(glob).match(path)))
    .sort();
}

function buildMap(session: Session, options: Options): ModuleMap {
  const files = moduleFiles(session, options.query);
  const definitions: Node[] = [];
  const links: Link[] = [];
  for (const file of files) {
    for (const definition of definitionsIn(session.project, file)) definitions.push(definition.node);
    links.push(...calleesOfFile(session, file));
  }
  const inside = new Set(files.map(file => session.project.pathOf(file)!));
  const insideDefinitions = new Map<string, Definition>();
  for (const definition of session.definitions) {
    if (!inside.has(definition.node.file)) continue;
    for (const key of keysOf(session.project, definition)) insideDefinitions.set(key, definition);
  }
  const called = new Set<string>();
  const callerFolders = new Set<string>();
  for (const file of session.project.files) {
    const callerPath = session.project.pathOf(file)!;
    if (inside.has(callerPath)) continue;
    for (const site of callSitesIn(session.project, file)) {
      const declaration = resolvedDeclaration(session.project, site);
      if (!declaration) continue;
      const path = session.project.pathOf(declaration);
      if (!path || !inside.has(path)) continue;
      const key = keyOf(located(session.project, declaration));
      if (!insideDefinitions.has(key)) continue;
      called.add(key);
      // The folder the caller is written in, which is one of the paths the user did not name.
      const folder = callerPath.split("/").slice(0, -1).join("/");
      if (folder) callerFolders.add(folder);
    }
  }
  const entries = [...called]
    .map(key => insideDefinitions.get(key)!)
    .filter(definition => placeableKind(definition.node.kind) && isExported(session, definition.declaration))
    .sort((left, right) => keyOf(left.node).localeCompare(keyOf(right.node)))
    .map(definition => ({ fn: definition.node, steps: stepsOf(session.project, definition.declaration) }));
  const map: ModuleMap = { definitions, links, entries };
  if (options.query.length && callerFolders.size) {
    const notSearched = [...callerFolders].sort().join(", ");
    session.limits.addReason("other", undefined,
      `links are the calls made inside ${options.query.join(", ")}; callers written in these folders were not searched: ${notSearched}`);
  }
  if (options.siblings.length) {
    const members = siblingMembers(session, options.siblings);
    if (members.length) {
      const { siblings, uncompared } = siblingTable(session.project, members);
      map.siblings = siblings;
      if (uncompared.length) session.limits.addReason("other", undefined,
        `not compared with the other siblings, because no other member exports the same callables: ${uncompared.join(", ")}`);
    } else session.limits.addReason("other", undefined, "the sibling rule matched no files of this program");
  } else {
    session.limits.addReason("other", undefined, "no sibling rule given (A1)");
  }
  return map;
}

function calleesOfFile(session: Session, file: ts.SourceFile): Link[] {
  dynamicLimitsIn(session, file, () => true);
  return callSitesIn(session.project, file).map(site => analyzeCall(session.project, site, session.context));
}

function buildTests(session: Session, options: Options, keys: Set<string>): TestsAnswer {
  const cases: TestCase[] = [];
  for (const record of testRecords(session)) {
    const reached = reachableFrom(session, record.body, record.node);
    for (const key of keys) {
      const reach = reached.get(key);
      if (!reach || !reach.path.length) continue;
      cases.push({ file: record.node.file, line: record.node.line, name: record.node.name, path: reach.path, throughFake: throughFakeOf(reach.path) });
    }
  }
  const decided = cases.filter(testCase => !testCase.throughFake);
  const faked = cases.filter(testCase => testCase.throughFake);
  const tests = options.fakeRule === "count" ? decided.concat(faked) : decided;
  const undecided = options.fakeRule ? [] : faked;
  if (undecided.length) session.limits.addReason("other", undefined, "fake rule not set (A3)");
  return { label: "static-call-path", count: tests.length, tests, undecided };
}

function testsFor(session: Session, options: Options, argument: string | undefined): TestsAnswer {
  const keys = new Set<string>();
  if (options.file !== undefined) {
    for (const definition of session.definitions) {
      if (definition.node.file !== options.file || !placeableKind(definition.node.kind)) continue;
      for (const key of keysOf(session.project, definition)) keys.add(key);
    }
  } else if (argument !== undefined) {
    const place = placeFor(session, argument).place;
    if (place) keys.add(keyOf(place.node));
  }
  return buildTests(session, options, keys);
}

/** One place, every candidate when the name is ambiguous, or the not-found limit. */
function answerThePlace(answer: Answer, session: Session, argument: string): Definition | undefined {
  const { place, candidates } = placeFor(session, argument);
  if (candidates.length > 1) {
    answer.matches = candidates.map(candidate => candidate.node);
    answer.ambiguous = true;
    return undefined;
  }
  if (!place) {
    answer.matches = [];
    answer.ambiguous = false;
    session.limits.addReason("not-found", undefined, `no definition was found at ${argument}`);
    return undefined;
  }
  return place;
}

export function answerFor(options: Options): Answer {
  const project = createProject(options.project, options.root);
  const limits = new LimitLog();
  const session: Session = {
    project,
    limits,
    context: { testPatterns: options.tests, limits },
    definitions: searchableDefinitions(project),
    index: new Map(),
  };
  session.index = buildIndex(project, session.definitions);
  if (!options.tests.length) limits.addReason("other", undefined, "no test-file pattern given");
  const answer: Answer = { command: options.command, query: options.query, limits: [] };
  const argument = options.query[0] ?? "";

  switch (options.command) {
    case "where":
    case "find": {
      let matches: Node[];
      if (isNameQuery(argument)) {
        const qualified = argument.includes(".") ? qualifiedMatches(session, argument) : undefined;
        matches = qualified?.length ? qualified : definitionsByName(session, argument).map(definition => definition.node);
        // A word that names nothing may still be what a definition says about itself.
        if (!matches.length) matches = matchesByDescription(session, argument);
      }
      else {
        matches = matchesByText(session, argument);
        if (!matches.length) matches = matchesByDescription(session, argument);
      }
      answer.matches = matches;
      answer.ambiguous = matches.length > 1;
      if (!matches.length) {
        session.limits.addReason("not-found", undefined, `nothing named or written like ${argument} was found`);
      }
      break;
    }
    case "map": {
      answer.map = buildMap(session, options);
      break;
    }
    case "tests": {
      if (options.file !== undefined) {
        if (!options.perFunction) {
          session.limits.addReason("other", undefined, "per-function report requires --per-function (A3)");
          answer.empty = "none found by static analysis";
          break;
        }
        answer.tests = testsFor(session, options, undefined);
        break;
      }
      const place = answerThePlace(answer, session, argument);
      if (place) answer.tests = testsFor(session, options, argument);
      break;
    }
    case "callers":
    case "callees":
    case "chain": {
      const place = answerThePlace(answer, session, argument);
      if (!place) break;
      if (!placeableKind(place.node.kind) && !ts.isSourceFile(place.declaration)) {
        answer.matches = [place.node];
        answer.ambiguous = false;
        session.limits.addReason("other", undefined, `${place.node.name} is a declaration, not an implementation to walk`);
        break;
      }
      if (options.command === "callees") answer.links = calleesOf(session, walkTarget(place));
      else if (options.command === "callers") {
        answer.links = findCallers(project, place.declaration, session.context).map(entry => entry.link);
      } else {
        const up = options.up ?? 6;
        const down = options.down ?? 6;
        if (up === 0 || down === 0) {
          session.limits.addReason("depth", { file: place.node.file, line: place.node.line },
            `chain depth ${up} up and ${down} down`);
        }
        answer.chain = {
          up: up > 0 ? chainUp(session, place, 1, up, new Map([[keyOf(place.node), place.node]])) : [],
          down: down > 0 ? chainDown(session, walkTarget(place), 1, down, new Map([[keyOf(place.node), place.node]])) : [],
        };
      }
      break;
    }
    default:
      session.limits.addReason("other", undefined, `unknown command ${options.command}`);
      break;
  }
  answer.limits = session.limits.all;
  return finish(answer);
}