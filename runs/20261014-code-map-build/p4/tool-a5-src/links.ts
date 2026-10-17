import ts from "typescript";
import type { Candidate, Limit, Link, Loc, Node } from "./answer.ts";
import {
  definitionKind, enclosingNode, isFunctionLikeDeclaration, lineOf, located, nameOfDeclaration, nearestFunction,
  nodeOf, placeableKind, propertyNameText,
} from "./nodes.ts";
import type { Project, WrittenObject } from "./project.ts";

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

/** A written function type: a shape with no body of its own, which a wrapper hands back unchanged. */
function isFunctionType(declaration: ts.Node): boolean {
  return ts.isFunctionTypeNode(declaration) || ts.isConstructorTypeNode(declaration);
}

/**
 * A signature with no body of its own: what a wrapper call returns, not an implementation.
 * `const compute = Effect.fn("Compute")(body)` is `compute`, not the arrow the wrapper happens to
 * return — and neither is the `(…args) => A` type the wrapper is written with.
 */
function isWrapperResult(declaration: ts.Node): boolean {
  if (isFunctionType(declaration)) return true;
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
  if (ts.isInterfaceDeclaration(parent) || ts.isClassDeclaration(parent)) return symbolOf(project, parent.name);
  if (ts.isTypeAliasDeclaration(parent)) return symbolOf(project, parent.name);
  // A shape written inline has no name of its own; its type is what another written place can share.
  if (ts.isTypeLiteralNode(parent)) return project.checker.getTypeFromTypeNode(parent).symbol;
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

/** The type that owns a member: an interface, a class, or the shape written inline. */
function ownsMembers(node: ts.Node | undefined): boolean {
  if (!node) return false;
  return ts.isInterfaceDeclaration(node) || ts.isClassLike(node) || ts.isTypeLiteralNode(node);
}

/** A member written as a type, with no body of its own. */
function isTypeMember(node: ts.Node): boolean {
  return ts.isFunctionTypeNode(node) || ts.isConstructorTypeNode(node) || ts.isMethodSignature(node) ||
    ts.isPropertySignature(node) || ts.isCallSignatureDeclaration(node) || ts.isIndexSignatureDeclaration(node);
}

/**
 * The written member a callee names, when the checker points at the shape rather than at a body:
 * `permission.assert(…)` on `readonly assert: (…) => T` is that interface member, not the type node.
 */
export function memberDeclaration(declaration: ts.Declaration): ts.Declaration {
  let current: ts.Node = declaration;
  for (let parent = current.parent; parent; current = parent, parent = current.parent) {
    if (ownsMembers(parent)) return current as ts.Declaration;
    if (!isTypeMember(current)) break;
  }
  return declaration;
}

/** A member written into a type, which is dispatched rather than carried: the call goes through it. */
function dispatchedThroughType(declaration: ts.Declaration): boolean {
  const parent = declaration.parent;
  return Boolean(parent && (ts.isInterfaceDeclaration(parent) || ts.isTypeLiteralNode(parent)));
}

/** The symbols a written type stands for: itself, its parts, and everything it is built on. */
function symbolsOfType(type: ts.Type | undefined): ts.Symbol[] {
  const symbols: ts.Symbol[] = [];
  const seen = new Set<ts.Type>();
  const visit = (current: ts.Type | undefined): void => {
    if (!current || seen.has(current)) return;
    seen.add(current);
    if (current.isUnionOrIntersection()) {
      for (const part of current.types) visit(part);
      return;
    }
    if (current.symbol) symbols.push(current.symbol);
    if (current.flags & ts.TypeFlags.Object) {
      for (const base of (current as ts.ObjectType).getBaseTypes() ?? []) visit(base);
    }
  };
  visit(type);
  return symbols;
}

function isCallableType(project: Project, node: ts.Node): boolean {
  return project.checker.getTypeAtLocation(node).getCallSignatures().length > 0;
}

/**
 * What a written `{ assert, ask }` names: the property that carries the member, or — for the shorthand
 * `Service.of({ get })` — the variable the shorthand refers to, which is the written implementation.
 */
function writtenPropertyDeclaration(project: Project, property: ts.ObjectLiteralElementLike): ts.Declaration | undefined {
  if (ts.isShorthandPropertyAssignment(property)) {
    const symbol = project.checker.getShorthandAssignmentValueSymbol(property);
    const value = symbol?.valueDeclaration ?? symbol?.declarations?.[0];
    return value && isCallableType(project, value) ? value : undefined;
  }
  if (ts.isPropertyAssignment(property) || ts.isMethodDeclaration(property)) {
    return isCallableType(project, property) ? property : undefined;
  }
  return undefined;
}

/** Every object literal in the program written where a service type is expected. */
function writtenObjectsOf(project: Project): WrittenObject[] {
  const checker = project.checker;
  const written: WrittenObject[] = [];
  const consider = (literal: ts.ObjectLiteralExpression, type: ts.Type | undefined): void => {
    const owners = symbolsOfType(type);
    if (owners.length) written.push({ literal, owners });
  };
  for (const file of project.files) {
    const visit = (node: ts.Node): void => {
      if (ts.isCallExpression(node) || ts.isNewExpression(node)) {
        for (const argument of node.arguments ?? []) {
          if (ts.isObjectLiteralExpression(argument)) consider(argument, checker.getContextualType(argument));
        }
      }
      else if (ts.isVariableDeclaration(node) || ts.isPropertyDeclaration(node)) {
        const initializer = node.initializer;
        if (initializer && ts.isObjectLiteralExpression(initializer) && node.type) {
          consider(initializer, checker.getTypeFromTypeNode(node.type));
        }
      }
      ts.forEachChild(node, visit);
    };
    visit(file);
  }
  return written;
}

/** Every implementation a written member has: the class members that carry it, and the written objects that do. */
export function implementationsOfMember(project: Project, owner: ts.Symbol, memberName: string): ts.Declaration[] {
  const byName = project.cache.implementationsByMember.get(owner);
  const cached = byName?.get(memberName);
  if (cached) return cached;
  const found: ts.Declaration[] = [];
  for (const file of project.files) {
    for (const statement of file.statements) {
      if (ts.isClassDeclaration(statement) && statement.name) {
        const member = memberOfClass(project, statement, owner, memberName, new Set([statement]));
        if (member && !found.some(existing => existing === member)) found.push(member);
      }
    }
  }
  const written = project.cache.writtenObjects ?? (project.cache.writtenObjects = writtenObjectsOf(project));
  for (const object of written) {
    if (!object.owners.includes(owner)) continue;
    for (const property of object.literal.properties) {
      if (propertyNameText(property.name) !== memberName) continue;
      const declaration = writtenPropertyDeclaration(project, property);
      if (declaration && !found.includes(declaration)) found.push(declaration);
    }
  }
  if (byName) byName.set(memberName, found);
  else project.cache.implementationsByMember.set(owner, new Map([[memberName, found]]));
  return found;
}

export interface ImplementationLookup {
  implementations: ts.Declaration[];
  via: "definition" | "implementation-lookup";
}

export function lookupImplementation(project: Project, declaration: ts.Declaration | undefined): ImplementationLookup {
  const lookup = (implementations: ts.Declaration[], via: "definition" | "implementation-lookup"): ImplementationLookup =>
    ({ implementations, via });
  if (!declaration) return lookup([], "definition");
  const member = memberDeclaration(declaration);
  if (member !== declaration) {
    const owner = ownerTypeSymbol(project, member);
    const memberName = nameOfDeclaration(member);
    if (owner && memberName) return lookup(implementationsOfMember(project, owner, memberName), "implementation-lookup");
  }
  if (isFunctionType(declaration)) {
    const holder = functionHolderOf(declaration);
    return lookup(holder ? [holder] : [], "definition");
  }
  if (isConcreteImplementation(declaration)) return lookup([declaration], "definition");
  const owner = ownerTypeSymbol(project, declaration);
  const memberName = nameOfDeclaration(declaration);
  if (!owner || !memberName) return lookup([], "definition");
  const parent = declaration.parent!;
  if (ts.isClassDeclaration(parent)) {
    const inherited = memberOfClass(project, parent, owner, memberName, new Set([parent]));
    return lookup(inherited ? [inherited] : [], "implementation-lookup");
  }
  if (!dispatchedThroughType(declaration)) return lookup([], "definition");
  return lookup(implementationsOfMember(project, owner, memberName), "implementation-lookup");
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
  const resolved = resolvedDeclaration(project, site);
  // What the checker names is the written member when the call is dispatched through a type.
  const declaration = resolved ? memberDeclaration(resolved) : undefined;
  const declaredHere = project.isSource(declaration);
  const dispatchedThroughTypeAtCall = Boolean(declaredHere && declaration && dispatchedThroughType(declaration));
  const { implementations, via } = lookupImplementation(project, resolved);
  const candidates = implementations
    .map(implementation => candidateNode(project, implementation, context.testPatterns))
    .filter((candidate): candidate is Candidate => candidate !== undefined);
  const realImplementations = candidates.filter(candidate => !candidate.testFake);
  const link: Link = {
    from: site.from,
    site: site.site,
    kind: ts.isNewExpression(site.node) ? "new" : dispatchedThroughTypeAtCall ? "service-call" : "call",
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

/** True when a call site reaches the given declaration: by its own name, or through the member it carries. */
function reachesDeclaration(project: Project, calleeDeclaration: ts.Declaration, target: ts.Declaration): boolean {
  if (calleeDeclaration === target) return true;
  return lookupImplementation(project, calleeDeclaration).implementations.includes(target);
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
  for (const file of project.files) {
    for (const site of callSitesIn(project, file)) {
      const calleeDeclaration = resolvedDeclaration(project, site);
      if (!calleeDeclaration) continue;
      const calleeSymbol = declarationSymbol(project, calleeDeclaration);
      const named = Boolean(calleeSymbol && symbols.has(calleeSymbol));
      if (!named && !reachesDeclaration(project, calleeDeclaration, declaration)) continue;
      found.push({ link: analyzeCall(project, site, context), enclosing: nearestFunction(site.node) });
    }
  }
  return found.sort((left, right) => left.link.site.file.localeCompare(right.link.site.file) ||
    left.link.site.line - right.link.site.line);
}