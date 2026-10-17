import { readFileSync } from "node:fs";
import { resolve, relative } from "node:path";
import ts from "typescript";
import { isObject } from "./matcher.ts";

export const normalizeText = (text: string) => text.replace(/[\t ]+$/gm, "").replace(/\s+$/, "");
export const samePlace = (left: unknown, right: unknown) => isObject(left) && isObject(right) && left.file === right.file && left.line === right.line;

/** Source observations use syntax only, independently of the tool's type/call analysis. */
export function sourceEvidence(root: string) {
  const cache = new Map<string, ts.SourceFile>();
  function source(file: string): ts.SourceFile | undefined {
    const path = resolve(root, file);
    if (relative(root, path).startsWith("..")) return undefined;
    if (!cache.has(file)) {
      try { cache.set(file, ts.createSourceFile(file, readFileSync(path, "utf8"), ts.ScriptTarget.Latest, true)); }
      catch { return undefined; }
    }
    return cache.get(file);
  }
  function nodes(at: unknown, predicate: (node: ts.Node, file: ts.SourceFile) => boolean): ts.Node[] {
    if (!isObject(at) || typeof at.file !== "string" || typeof at.line !== "number") return [];
    const file = source(at.file); if (!file) return [];
    const found: ts.Node[] = [];
    const line = at.line;
    function visit(node: ts.Node) {
      if (file!.getLineAndCharacterOfPosition(node.getStart(file)).line + 1 === line && predicate(node, file!)) found.push(node);
      ts.forEachChild(node, visit);
    }
    visit(file); return found;
  }
  function hasText(at: unknown, text: unknown) {
    return typeof text === "string" && nodes(at, (node, file) => normalizeText(node.getText(file)) === normalizeText(text) &&
      (!isObject(at) || at.endLine === undefined || file.getLineAndCharacterOfPosition(node.getEnd() - 1).line + 1 === at.endLine)).length > 0;
  }
  function isCallSite(edge: unknown) {
    if (!isObject(edge) || !isObject(edge.from)) return false;
    const from = edge.from;
    return nodes(edge.site, node => {
      if (edge.kind === "new" ? !ts.isNewExpression(node) : !ts.isCallExpression(node)) return false;
      let parent: ts.Node | undefined = node.parent;
      while (parent && !ts.isFunctionLike(parent)) parent = parent.parent;
      if (!parent) return from.kind === "other";
      const file = parent.getSourceFile();
      return samePlace(from, { file: file.fileName, line: file.getLineAndCharacterOfPosition(parent.getStart(file)).line + 1 });
    }).length > 0;
  }
  function isTestStart(test: Record<string, unknown>, first: unknown) {
    if (!isObject(first) || !samePlace(test, first.from)) return false;
    return nodes(test, node => {
      if (!ts.isCallExpression(node) || !node.arguments[0] || !ts.isStringLiteralLike(node.arguments[0]) || node.arguments[0].text !== test.name) return false;
      // An ambient framework API can be renamed in a held-out fixture; the body and title identify this call.
      const body = node.arguments[1];
      if (!body || (!ts.isArrowFunction(body) && !ts.isFunctionExpression(body))) return false;
      const file = node.getSourceFile();
      return isObject(first.site) && first.site.file === file.fileName && nodes(first.site, call =>
        ts.isCallExpression(call) && call.getStart(file) >= body.getStart(file) && call.getEnd() <= body.getEnd()).length > 0;
    }).length > 0;
  }
  return { hasText, isCallSite, isTestStart };
}
