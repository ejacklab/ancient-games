import ts from "typescript";
import type { Loc, Node, NodeKind } from "./answer.ts";
import type { Project } from "./project.ts";

export interface Definition {
  node: Node;
  declaration: ts.Declaration;
  /** The function the declaration implements: its initializer, or the body a wrapper call was given. */
  implementation?: ts.Node;
}

export function lineOf(file: ts.SourceFile, position: number): number {
  return file.getLineAndCharacterOfPosition(position).line + 1;
}

export function locOf(node: ts.Node): Loc {
  const file = node.getSourceFile();
  const start = node.getStart(file);
  const end = Math.max(start, node.getEnd() - 1);
  return {
    file: file.fileName,
    line: lineOf(file, start),
    endLine: lineOf(file, end),
  };
}

export function located(project: Project, node: ts.Node): Loc {
  const { file, line, endLine } = locOf(node);
  return { file: project.pathOf(node) ?? file, line, endLine };
}

function nameText(name: ts.DeclarationName | undefined): string | undefined {
  if (!name) return undefined;
  if (ts.isIdentifier(name) || ts.isPrivateIdentifier(name)) return name.text;
  if (ts.isStringLiteralLike(name) || ts.isNumericLiteral(name)) return name.text;
  return undefined;
}

function propertyNameText(name: ts.PropertyName | undefined): string | undefined {
  if (!name) return undefined;
  if (ts.isIdentifier(name) || ts.isPrivateIdentifier(name) || ts.isStringLiteralLike(name) || ts.isNumericLiteral(name)) {
    return name.text;
  }
  return undefined;
}

function declaringClass(node: ts.Node): ts.ClassLikeDeclaration | undefined {
  let parent: ts.Node | undefined = node.parent;
  while (parent) {
    if (ts.isClassLike(parent)) return parent;
    if (ts.isFunctionLike(parent)) return undefined;
    parent = parent.parent;
  }
  return undefined;
}

function declaringInterface(node: ts.Node): ts.InterfaceDeclaration | undefined {
  let parent: ts.Node | undefined = node.parent;
  while (parent) {
    if (ts.isInterfaceDeclaration(parent)) return parent;
    if (ts.isFunctionLike(parent)) return undefined;
    parent = parent.parent;
  }
  return undefined;
}

function memberName(node: ts.Node): string | undefined {
  if (ts.isPropertyAssignment(node) || ts.isPropertyDeclaration(node) || ts.isMethodDeclaration(node)) {
    return propertyNameText(node.name);
  }
  return undefined;
}

/**
 * The written names that lead to a declaration, outermost first: `{ get: … }` inside `const svc = {…}`
 * gives `["svc", "get"]`, a name at the top of a module gives `["svc"]`, and a name inside a function
 * body gives nothing above its own.
 */
function holderChain(node: ts.Node): string[] {
  const names: string[] = [];
  let current: ts.Node | undefined = node;
  while (current && !isFunctionLikeDeclaration(current) && !ts.isClassLike(current)) {
    const name = ts.isVariableDeclaration(current) ? nameText(current.name) : memberName(current);
    if (name) names.unshift(name);
    else if (ts.isVariableDeclaration(current)) break;
    current = current.parent;
  }
  return names;
}

const chainName = (node: ts.Node): string | undefined => {
  const names = holderChain(node);
  return names.length ? names.join(".") : undefined;
};

function isTestCall(expression: ts.Expression): boolean {
  const text = expression.getText();
  const name = ts.isPropertyAccessExpression(expression) ? expression.name.text : text;
  return name === "test" || name === "it";
}

function callTitleText(call: ts.CallExpression): string | undefined {
  if (!isTestCall(call.expression)) return undefined;
  const title = call.arguments[0];
  return title && ts.isStringLiteralLike(title) ? title.text : undefined;
}

/** `Effect.fn("Name")(body)` and its relatives: a wrapper call given a function, whose result is that shape. */
function wrapperBody(project: Project, call: ts.CallExpression): ts.Node | undefined {
  const body = call.arguments.find(argument => ts.isArrowFunction(argument) || ts.isFunctionExpression(argument));
  if (!body || !project.checker.getTypeAtLocation(call).getCallSignatures().length) return undefined;
  return body;
}

function anonymousName(project: Project, fn: ts.ArrowFunction | ts.FunctionExpression): { name: string; kind: NodeKind } {
  const kind: NodeKind = ts.isArrowFunction(fn) ? "arrow" : "function";
  const parent: ts.Node | undefined = fn.parent;
  const held = parent ? chainName(parent) : undefined;
  if (held) {
    const wrapped = ts.isCallExpression(parent!) && wrapperBody(project, parent!) === fn;
    return { name: held, kind: wrapped ? "effect-fn" : kind };
  }
  if (parent && ts.isCallExpression(parent)) {
    const title = callTitleText(parent);
    return { name: title ?? `${parent.expression.getText()} callback`, kind };
  }
  const named = ts.isFunctionExpression(fn) ? fn.name?.getText() : undefined;
  return { name: named ?? "<anonymous>", kind };
}

export function nodeOf(project: Project, node: ts.Node): Node {
  const loc = located(project, node);
  if (ts.isFunctionDeclaration(node)) {
    return { ...loc, name: nameText(node.name) ?? "<anonymous>", kind: "function" };
  }
  if (ts.isClassDeclaration(node) || ts.isClassExpression(node)) {
    return { ...loc, name: nameText(node.name) ?? "<anonymous>", kind: "class" };
  }
  if (ts.isMethodDeclaration(node) || ts.isMethodSignature(node)) {
    const owner = declaringClass(node);
    const name = nameText(node.name) ?? "<anonymous>";
    const holder = owner ? nameText(owner.name) : chainName(node.parent ?? node);
    return { ...loc, name: holder ? `${holder}.${name}` : name, kind: "method" };
  }
  if (ts.isConstructorDeclaration(node)) {
    const owner = declaringClass(node);
    return { ...loc, name: `${owner ? nameText(owner.name) ?? "<anonymous>" : "<anonymous>"}.constructor`, kind: "method" };
  }
  if (ts.isGetAccessorDeclaration(node) || ts.isSetAccessorDeclaration(node)) {
    const owner = declaringClass(node);
    const name = nameText(node.name) ?? "<anonymous>";
    return { ...loc, name: owner ? `${nameText(owner.name)}.${name}` : name, kind: "property" };
  }
  if (ts.isArrowFunction(node) || ts.isFunctionExpression(node)) {
    const { name, kind } = anonymousName(project, node);
    return { ...loc, name, kind };
  }
  if (ts.isVariableDeclaration(node) || ts.isPropertyDeclaration(node) || ts.isPropertyAssignment(node)) {
    const name = nameText(node.name as ts.BindingName | undefined) ?? propertyNameText(node.name as ts.PropertyName);
    return { ...loc, name: chainName(node) ?? name ?? "<anonymous>", kind: "variable" };
  }
  const owner = declaringInterface(node);
  const interfaceName = owner?.name.text;
  const interfaceMember = interfaceName ? nameText((node as { name?: ts.DeclarationName }).name) : undefined;
  if (interfaceName && interfaceMember) {
    return { ...loc, name: `${interfaceName}.${interfaceMember}`, kind: "interface-member" };
  }
  return { ...loc, name: "<declaration>", kind: "other" };
}

export function definitionKind(project: Project, node: ts.Node): NodeKind | undefined {
  if (ts.isFunctionDeclaration(node)) return "function";
  if (ts.isClassDeclaration(node)) return "class";
  if (ts.isMethodDeclaration(node)) return "method";
  if (ts.isMethodSignature(node)) return "interface-member";
  if (ts.isVariableDeclaration(node) || ts.isPropertyDeclaration(node) || ts.isPropertyAssignment(node)) {
    const init = node.initializer;
    if (!init) return undefined;
    if (ts.isArrowFunction(init)) return "arrow";
    if (ts.isFunctionExpression(init)) return "function";
    if (implementationBody(project, node)) return "effect-fn";
    return undefined;
  }
  return undefined;
}

/**
 * The function a declaration implements: the declaration itself, its initializer, or the body a wrapper
 * call such as `Effect.fn("Name")(body)` was given.
 */
export function implementationBody(project: Project, node: ts.Node): ts.Node | undefined {
  if (isFunctionLikeDeclaration(node)) return node;
  if (!ts.isVariableDeclaration(node) && !ts.isPropertyDeclaration(node) && !ts.isPropertyAssignment(node)) return undefined;
  const init = node.initializer;
  if (!init) return undefined;
  if (ts.isArrowFunction(init) || ts.isFunctionExpression(init)) return init;
  return ts.isCallExpression(init) ? wrapperBody(project, init) : undefined;
}

function declarationOrder(left: ts.Node, right: ts.Node): number {
  return left.getStart() - right.getStart();
}

export function definitionsIn(project: Project, file: ts.SourceFile): Definition[] {
  const found: Definition[] = [];
  const visit = (node: ts.Node): void => {
    const kind = definitionKind(project, node);
    if (kind && kind !== "interface-member") {
      found.push({
        node: { ...located(project, node), name: nodeOf(project, node).name, kind },
        declaration: node as ts.Declaration,
        implementation: implementationBody(project, node),
      });
    }
    ts.forEachChild(node, visit);
  };
  visit(file);
  return found.sort((left, right) => declarationOrder(left.declaration, right.declaration));
}

export function searchableDefinitions(project: Project): Definition[] {
  const found: Definition[] = [];
  for (const file of project.files) {
    const visit = (node: ts.Node): void => {
      const kind = definitionKind(project, node);
      if (!kind && !ts.isMethodSignature(node)) {
        ts.forEachChild(node, visit);
        return;
      }
      const written = nodeOf(project, node);
      found.push({
        node: kind ? { ...written, kind } : written,
        declaration: node as ts.Declaration,
        implementation: implementationBody(project, node),
      });
      ts.forEachChild(node, visit);
    };
    visit(file);
  }
  return found.sort((left, right) => {
    const leftPath = left.node.file;
    const rightPath = right.node.file;
    if (leftPath !== rightPath) return leftPath < rightPath ? -1 : 1;
    return left.node.line - right.node.line || declarationOrder(left.declaration, right.declaration);
  });
}

export function placeableKind(kind: NodeKind): boolean {
  return kind === "function" || kind === "method" || kind === "arrow" || kind === "effect-fn";
}

export function isFunctionLikeDeclaration(node: ts.Node): boolean {
  return ts.isFunctionDeclaration(node) || ts.isMethodDeclaration(node) || ts.isConstructorDeclaration(node) ||
    ts.isGetAccessorDeclaration(node) || ts.isSetAccessorDeclaration(node) || ts.isArrowFunction(node) ||
    ts.isFunctionExpression(node) || ts.isMethodSignature(node);
}

export function nearestFunction(node: ts.Node): ts.Node | undefined {
  let parent: ts.Node | undefined = node;
  while (parent) {
    if (isFunctionLikeDeclaration(parent)) return parent;
    parent = parent.parent;
  }
  return undefined;
}

export function enclosingNode(project: Project, node: ts.Node): Node {
  const functionLike = nearestFunction(node);
  if (functionLike) return nodeOf(project, functionLike);
  const loc = located(project, node);
  return { ...loc, name: "<module>", kind: "other" };
}

export function nameOfDeclaration(node: ts.Node): string | undefined {
  if (ts.isFunctionDeclaration(node) || ts.isMethodDeclaration(node) || ts.isMethodSignature(node) ||
      ts.isPropertySignature(node) || ts.isPropertyDeclaration(node) || ts.isGetAccessorDeclaration(node) ||
      ts.isSetAccessorDeclaration(node)) {
    return nameText((node as { name?: ts.DeclarationName }).name);
  }
  if (ts.isVariableDeclaration(node)) return nameText(node.name);
  return undefined;
}
