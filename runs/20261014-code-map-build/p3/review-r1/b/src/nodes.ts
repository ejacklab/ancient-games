import ts from "typescript";
import type { Loc, Node, NodeKind } from "./answer.ts";
import type { Project } from "./project.ts";

export interface Definition {
  node: Node;
  declaration: ts.Declaration;
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

function holderVariableName(node: ts.Node): string | undefined {
  const parent: ts.Node | undefined = node.parent;
  if (parent && ts.isVariableDeclaration(parent) && ts.isIdentifier(parent.name)) return parent.name.text;
  if (parent && ts.isBinaryExpression(parent) && parent.operatorToken.kind === ts.SyntaxKind.EqualsToken) {
    return parent.left.getText();
  }
  return undefined;
}

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

function effectFnHolderName(fn: ts.ArrowFunction | ts.FunctionExpression): { name: string; kind: NodeKind } | undefined {
  const parent: ts.Node | undefined = fn.parent;
  if (!parent || !ts.isCallExpression(parent) || !parent.arguments.some(argument => argument === fn)) return undefined;
  const callee = parent.expression.getText();
  if (!callee.endsWith(".fn")) return undefined;
  const held = holderVariableName(parent);
  return held ? { name: held, kind: "effect-fn" } : undefined;
}

function anonymousName(fn: ts.ArrowFunction | ts.FunctionExpression): { name: string; kind: NodeKind } {
  const kind: NodeKind = ts.isArrowFunction(fn) ? "arrow" : "effect-fn";
  const parent: ts.Node | undefined = fn.parent;
  if (parent && ts.isCallExpression(parent)) {
    const title = callTitleText(parent);
    if (title) return { name: title, kind: ts.isArrowFunction(fn) ? "arrow" : "effect-fn" };
    const effect = effectFnHolderName(fn);
    if (effect) return effect;
  }
  const held = holderVariableName(fn);
  if (held) return { name: held, kind };
  if (parent && ts.isCallExpression(parent)) return { name: `${parent.expression.getText()} callback`, kind };
  const propertyParent: ts.Node | undefined = fn.parent;
  if (propertyParent && ts.isPropertyAssignment(propertyParent)) {
    const name = propertyNameText(propertyParent.name);
    if (name) return { name, kind };
  }
  return { name: "<anonymous>", kind };
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
    const holder = owner ? nameText(owner.name) : undefined;
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
    const { name, kind } = anonymousName(node);
    return { ...loc, name, kind };
  }
  if (ts.isVariableDeclaration(node) || ts.isPropertyDeclaration(node) || ts.isPropertyAssignment(node)) {
    const name = nameText(node.name as ts.BindingName | undefined) ?? propertyNameText(node.name as ts.PropertyName);
    return { ...loc, name: name ?? "<anonymous>", kind: "variable" };
  }
  const owner = declaringInterface(node);
  const interfaceName = owner?.name.text;
  const interfaceMember = interfaceName ? nameText((node as { name?: ts.DeclarationName }).name) : undefined;
  if (interfaceName && interfaceMember) {
    return { ...loc, name: `${interfaceName}.${interfaceMember}`, kind: "interface-member" };
  }
  return { ...loc, name: "<declaration>", kind: "other" };
}

export function definitionKind(node: ts.Node): NodeKind | undefined {
  if (ts.isFunctionDeclaration(node)) return "function";
  if (ts.isClassDeclaration(node)) return "class";
  if (ts.isMethodDeclaration(node)) return "method";
  if (ts.isMethodSignature(node)) return "interface-member";
  if (ts.isVariableDeclaration(node)) {
    const init = node.initializer;
    if (!init) return undefined;
    if (ts.isArrowFunction(init) || ts.isFunctionExpression(init)) {
      const effect = effectFnHolderName(init);
      if (effect) return "effect-fn";
      return "arrow";
    }
    if (ts.isCallExpression(init) && init.expression.getText().endsWith(".fn")) return "effect-fn";
    return undefined;
  }
  if (ts.isPropertyDeclaration(node) || ts.isPropertyAssignment(node)) {
    const init = node.initializer;
    if (init && (ts.isArrowFunction(init) || ts.isFunctionExpression(init))) return "arrow";
    if (init && ts.isCallExpression(init) && init.expression.getText().endsWith(".fn")) return "effect-fn";
    return undefined;
  }
  return undefined;
}

function declarationOrder(left: ts.Node, right: ts.Node): number {
  return left.getStart() - right.getStart();
}

export function definitionsIn(project: Project, file: ts.SourceFile): Definition[] {
  const found: Definition[] = [];
  const visit = (node: ts.Node): void => {
    const kind = definitionKind(node);
    if (kind && kind !== "interface-member") {
      found.push({ node: { ...located(project, node), name: nodeOf(project, node).name, kind }, declaration: node as ts.Declaration });
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
      const kind = definitionKind(node);
      if (kind || ts.isMethodSignature(node)) found.push({ node: nodeOf(project, node), declaration: node as ts.Declaration });
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
