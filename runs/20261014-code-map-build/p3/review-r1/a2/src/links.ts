import ts from "typescript";
import type { Candidate, Limit, Link, Loc, Node } from "./answer.ts";
import {
  definitionKind, enclosingNode, isFunctionLikeDeclaration, lineOf, located, nameOfDeclaration, nearestFunction, nodeOf,
  placeableKind,
} from "./nodes.ts";
import type { Project } from "./project.ts";

export interface CallSite {
  node: ts.CallExpression | ts.NewExpression;
  file: ts.SourceFile;
  callee: ts.Expression;
  from: Node;
  site: Loc;
  name: string;
}

export function isComputedCallee(callee: ts.Expression): boolean {
  if (!ts.isElementAccessExpression(callee)) return false;
  const key = callee.argumentExpression;
  return !(ts.isStringLiteralLike(key) || ts.isNumericLiteral(key));
}

function calleeName(callee: ts.Expression): string | undefined {
  if (ts.isIdentifier(callee)) return callee.text;
  if (ts.isPropertyAccessExpression(callee)) return callee.getText();
  if (ts.isElementAccessExpression(callee) && ts.isStringLiteralLike(callee.argumentExpression)) {
    const key = callee.argumentExpression.text;
    return ts.isPropertyAccessExpression(callee.expression) ? `${callee.expression.getText()}.${key}` : key;
  }
  return undefined;
}

export function callSitesIn(project: Project, file: ts.SourceFile): CallSite[] {
  const found: CallSite[] = [];
  const visit = (node: ts.Node): void => {
    if (ts.isCallExpression(node) || ts.isNewExpression(node)) {
        const callee = node.expression;
        if (!isComputedCallee(callee)) {
          const name = calleeName(callee);
          if (name) {
            const start = node.getStart(file);
            const end = Math.max(start, node.getEnd() - 1);
            found.push({
              node, file, callee, name,
              from: enclosingNode(project, node),
              site: { file: project.pathOf(file)!, line: lineOf(file, start), endLine: lineOf(file, end) },
            });
          }
        }
      }
      ts.forEachChild(node, visit);
    };
    visit(file);
  return found.sort((left, right) => left.node.getStart() - right.node.getStart());
}

export function computedCallsIn(file: ts.SourceFile): (ts.CallExpression | ts.NewExpression)[] {
  const found: (ts.CallExpression | ts.NewExpression)[] = [];
  const visit = (node: ts.Node): void => {
    if ((ts.isCallExpression(node) || ts.isNewExpression(node)) && isComputedCallee(node.expression)) found.push(node);
    ts.forEachChild(node, visit);
  };
  visit(file);
  return found;
}

function symbolOf(project: Project, node: ts.Node | undefined): ts.Symbol | undefined {
  if (!node) return undefined;
  const checker = project.checker;
  const symbol = checker.getSymbolAtLocation(node);
  if (!symbol) return undefined;
  return symbol.flags & ts.SymbolFlags.Alias ? checker.getAliasedSymbol(symbol) : symbol;
}

function declarationSymbol(project: Project, declaration: ts.Declaration | undefined): ts.Symbol | undefined {
  if (!declaration) return undefined;
  const named = (declaration as { name?: ts.Node }).name;
  if (named) {
    const symbol = symbolOf(project, named);
    if (symbol) return symbol;
  }
  // A function expression has no name of its own; the symbol that names it is the one holding it.
  const holder = isFunctionLikeDeclaration(declaration) ? functionHolderOf(declaration) : undefined;
  if (holder) {
    const held = (holder as { name?: ts.Node }).name;
    const symbol = symbolOf(project, held ?? holder);
    if (symbol) return symbol;
  }
  return symbolOf(project, declaration);
}

function isHeldFunction(declaration: ts.Node): boolean {
  const holder = declaration.parent;
  if (!holder) return false;
  if (ts.isVariableDeclaration(holder) || ts.isPropertyDeclaration(holder) || ts.isPropertyAssignment(holder)) {
    return holder.initializer === declaration;
  }
  return false;
}

/** A function expression that no written name stands for: what a wrapper call returns, not an implementation. */
function isWrapperResult(declaration: ts.Node): boolean {
  if (!ts.isArrowFunction(declaration) && !ts.isFunctionExpression(declaration)) return false;
  if ((declaration as ts.FunctionExpression).name) return false;
  return !isHeldFunction(declaration);
}

function symbolDeclaration(project: Project, node: ts.Node | undefined): ts.Symbol | undefined {
  if (!node) return undefined;
  const checker = project.checker;
  const symbol = checker.getSymbolAtLocation(node);
  if (!symbol) return undefined;
  return symbol.flags & ts.SymbolFlags.Alias ? checker.getAliasedSymbol(symbol) : symbol;
}

/**
 * What the name at a call site stands for, when the type checker points only at a wrapper's return value:
 * `const compute = Effect.fn("Compute")(body)` is `compute`, not the arrow the wrapper happens to return.
 */
function namedImplementation(project: Project, declaration: ts.Declaration | undefined, callee: ts.Expression): ts.Declaration | undefined {
  if (!declaration || !isWrapperResult(declaration)) return undefined;
  const symbol = symbolOf(project, callee);
  const value = symbol?.valueDeclaration ?? symbol?.declarations?.[0];
  return value && definitionKind(project, value) ? value : undefined;
}

export function resolvedDeclaration(project: Project, site: CallSite): ts.Declaration | undefined {
  const signature = project.checker.getResolvedSignature(site.node)?.declaration;
  if (signature) return namedImplementation(project, signature, site.callee) ?? signature;
  const checker = project.checker;
  const symbol = checker.getSymbolAtLocation(site.callee);
  if (!symbol) return undefined;
  const resolved = symbol.flags & ts.SymbolFlags.Alias ? checker.getAliasedSymbol(symbol) : symbol;
  return resolved.valueDeclaration ?? resolved.declarations?.[0];
}

function isConcreteImplementation(declaration: ts.Declaration): boolean {
  if (isFunctionLikeDeclaration(declaration)) return Boolean((declaration as { body?: ts.Node }).body);
  if (ts.isClassDeclaration(declaration)) return true;
  if (ts.isVariableDeclaration(declaration)) return Boolean(declaration.initializer);
  return false;
}

function ownerTypeSymbol(project: Project, declaration: ts.Declaration): ts.Symbol | undefined {
  const parent = declaration.parent;
  if (!parent) return undefined;
  if (ts.isInterfaceDeclaration(parent)) return symbolOf(project, parent.name);
  if (ts.isTypeAliasDeclaration(parent)) return symbolOf(project, parent.name);
  if (ts.isClassDeclaration(parent)) return symbolOf(project, parent.name);
  return undefined;
}

function memberOfClass(project: Project, classDeclaration: ts.ClassDeclaration, owner: ts.Symbol,
  memberName: string, seen: Set<ts.ClassDeclaration>): ts.Declaration | undefined {
  const checker = project.checker;
  const classType = checker.getTypeAtLocation(classDeclaration);
  for (const clause of classDeclaration.heritageClauses ?? []) {
    for (const type of clause.types) {
      const base = checker.getTypeAtLocation(type) as ts.ObjectType;
      if (base.symbol === owner) return checker.getPropertyOfType(classType, memberName)?.valueDeclaration;
      if (clause.token !== ts.SyntaxKind.ExtendsKeyword) continue;
      const baseDeclaration = base.symbol?.declarations?.find(ts.isClassDeclaration);
      if (!baseDeclaration || seen.has(baseDeclaration)) continue;
      seen.add(baseDeclaration);
      const inherited = memberOfClass(project, baseDeclaration, owner, memberName, seen);
      if (inherited) return inherited;
    }
  }
  return undefined;
}

const implementationCache = new WeakMap<ts.Node, Map<ts.Symbol, ts.Declaration[]>>();

function heldFunction(value: ts.Node): ts.Declaration | undefined {
  const holder = value.parent;
  if (!holder) return undefined;
  if (ts.isVariableDeclaration(holder) || ts.isPropertyDeclaration(holder) || ts.isPropertyAssignment(holder)) {
    return holder.initializer === value ? holder : undefined;
  }
  return undefined;
}

/** The function a written function type belongs to: a variable, a property or the enclosing arrow. */
function functionHolderOf(declaration: ts.Declaration): ts.Declaration | undefined {
  const direct = heldFunction(declaration);
  if (direct) return direct;
  let current: ts.Node | undefined = declaration;
  while (current && !isFunctionLikeDeclaration(current)) current = current.parent;
  return current ? heldFunction(current) : undefined;
}

export interface ImplementationLookup {
  implementations: ts.Declaration[];
  via: "definition" | "implementation-lookup";
}

export function lookupImplementation(project: Project, declaration: ts.Declaration | undefined): ImplementationLookup {
  const lookup = (implementations: ts.Declaration[], via: "definition" | "implementation-lookup"): ImplementationLookup =>
    ({ implementations, via });
  if (!declaration) return lookup([], "definition");
  if (ts.isFunctionTypeNode(declaration) || ts.isConstructorTypeNode(declaration)) {
    const holder = functionHolderOf(declaration);
    return lookup(holder ? [holder] : [], "definition");
  }
  if (isConcreteImplementation(declaration)) return lookup([declaration], "definition");
  const owner = ownerTypeSymbol(project, declaration);
  const memberName = nameOfDeclaration(declaration);
  if (!owner || !memberName) return lookup([], "definition");
  const parent = declaration.parent!;
  if (ts.isClassDeclaration(parent)) {
    const member = memberOfClass(project, parent, owner, memberName, new Set([parent]));
    return lookup(member ? [member] : [], "implementation-lookup");
  }
  if (!ts.isInterfaceDeclaration(parent) && !ts.isTypeAliasDeclaration(parent)) return lookup([], "definition");
  let byOwner = implementationCache.get(declaration.getSourceFile());
  if (!byOwner) {
    byOwner = new Map();
    implementationCache.set(declaration.getSourceFile(), byOwner);
  }
  const cached = byOwner.get(owner);
  if (cached) return lookup(cached, "implementation-lookup");
  const found: ts.Declaration[] = [];
  for (const file of project.files) {
    for (const statement of file.statements) {
      if (ts.isClassDeclaration(statement) && statement.name) {
        const member = memberOfClass(project, statement, owner, memberName, new Set([statement]));
        if (member && !found.some(existing => existing === member)) found.push(member);
      }
    }
  }
  byOwner.set(owner, found);
  return lookup(found, "implementation-lookup");
}

export function interfaceMembersOf(project: Project, declaration: ts.Declaration): ts.Declaration[] {
  const checker = project.checker;
  const parent = declaration.parent;
  if (!parent || !ts.isClassDeclaration(parent)) return [];
  const memberName = nameOfDeclaration(declaration);
  if (!memberName) return [];
  const found: ts.Declaration[] = [];
  const visit = (classDeclaration: ts.ClassDeclaration, seen: Set<ts.ClassDeclaration>): void => {
    if (seen.has(classDeclaration)) return;
    seen.add(classDeclaration);
    for (const clause of classDeclaration.heritageClauses ?? []) {
      for (const type of clause.types) {
        const base = checker.getTypeAtLocation(type);
        if (!(base.flags & ts.TypeFlags.Object)) continue;
        const member = checker.getPropertyOfType(base as ts.ObjectType, memberName);
        const memberDeclaration = member?.valueDeclaration;
        if (memberDeclaration && ts.isMethodSignature(memberDeclaration) && !found.includes(memberDeclaration)) {
          found.push(memberDeclaration);
        }
        const baseDeclaration = (base as ts.ObjectType).symbol?.declarations?.find(ts.isClassDeclaration);
        if (clause.token === ts.SyntaxKind.ExtendsKeyword && baseDeclaration) visit(baseDeclaration, seen);
      }
    }
  };
  visit(parent, new Set());
  return found;
}

export function isTestFile(patterns: string[], file: string): boolean {
  return patterns.some(pattern => new Bun.Glob(pattern).match(file));
}

function candidateNode(project: Project, declaration: ts.Declaration, testPatterns: string[]): Candidate | undefined {
  const path = project.pathOf(declaration);
  if (!path || !project.isSource(declaration)) return undefined;
  const written = nodeOf(project, declaration);
  const kind = definitionKind(project, declaration);
  return { ...written, ...(kind && placeableKind(kind) ? { kind } : {}), testFake: isTestFile(testPatterns, path) };
}

export interface AnalysisContext {
  testPatterns: string[];
  limits: { addReason(reason: Limit["reason"], at?: Loc, text?: string): void };
}

function dynamicReason(project: Project, site: CallSite, declaration: ts.Declaration | undefined): string | undefined {
  if (ts.isElementAccessExpression(site.callee)) return "the member called is chosen at run time";
  if (!ts.isIdentifier(site.callee)) return undefined;
  const symbol = project.checker.getSymbolAtLocation(site.callee);
  const value = symbol?.valueDeclaration;
  if (value && ts.isParameter(value)) return `${site.name} is a parameter, so the function it names is only known at run time`;
  if (value && ts.isVariableDeclaration(value) && !value.initializer) {
    return `${site.name} is assigned at run time, so the function it names is only known then`;
  }
  if (!declaration && !value) return `${site.name} has no declaration in this program`;
  return undefined;
}

export function analyzeCall(project: Project, site: CallSite, context: AnalysisContext): Link {
  const declaration = resolvedDeclaration(project, site);
  const declaredHere = project.isSource(declaration);
  const dispatchedThroughInterface = Boolean(
    declaredHere && declaration?.parent && ts.isInterfaceDeclaration(declaration.parent));
  const { implementations, via } = lookupImplementation(project, declaration);
  const candidates = implementations
    .map(implementation => candidateNode(project, implementation, context.testPatterns))
    .filter((candidate): candidate is Candidate => candidate !== undefined);
  const realImplementations = candidates.filter(candidate => !candidate.testFake);
  const link: Link = {
    from: site.from,
    site: site.site,
    kind: ts.isNewExpression(site.node) ? "new" : dispatchedThroughInterface ? "service-call" : "call",
    resolution: realImplementations.length === 0 ? "unresolved"
      : realImplementations.length === 1 ? "implementation" : "ambiguous",
    candidates,
    via,
  };
  if (declaration && declaredHere) link.declaration = located(project, declaration);
  if (link.resolution === "implementation") link.to = realImplementations[0];
  if (link.resolution === "unresolved") {
    if (declaration && !declaredHere) {
      link.reason = `${site.name} is implemented outside the repository`;
      context.limits.addReason("outside-repo", site.site);
    } else if (candidates.length > 0) {
      link.reason = `the only implementations of ${site.name} are in test files`;
      context.limits.addReason("not-found", site.site);
    } else {
      const dynamic = dynamicReason(project, site, declaration);
      if (dynamic) {
        link.reason = dynamic;
        context.limits.addReason("dynamic", site.site);
      } else {
        link.reason = `no implementation of ${site.name} was found by static analysis`;
        context.limits.addReason("not-found", site.site);
      }
    }
  }
  return link;
}

export interface CallerLink {
  link: Link;
  enclosing?: ts.Node;
}

export function findCallers(project: Project, declaration: ts.Declaration, context: AnalysisContext): CallerLink[] {
  const symbols = new Set<ts.Symbol>();
  const own = declarationSymbol(project, declaration);
  if (own) symbols.add(own);
  for (const member of interfaceMembersOf(project, declaration)) {
    const symbol = declarationSymbol(project, member);
    if (symbol) symbols.add(symbol);
  }
  const found: CallerLink[] = [];
  if (!symbols.size) return found;
  for (const file of project.files) {
    for (const site of callSitesIn(project, file)) {
      const calleeDeclaration = resolvedDeclaration(project, site);
      if (!calleeDeclaration) continue;
      const calleeSymbol = declarationSymbol(project, calleeDeclaration);
      if (!calleeSymbol || !symbols.has(calleeSymbol)) continue;
      found.push({ link: analyzeCall(project, site, context), enclosing: nearestFunction(site.node) });
    }
  }
  return found.sort((left, right) => left.link.site.file.localeCompare(right.link.site.file) ||
    left.link.site.line - right.link.site.line);
}