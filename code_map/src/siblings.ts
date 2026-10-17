import ts from "typescript";
import type { Siblings } from "./answer.ts";
import { implementationBody, located, propertyNameText } from "./nodes.ts";
import type { Project } from "./project.ts";

interface SiblingFile {
  path: string;
  source?: ts.SourceFile;
  functions: Map<string, ts.Node[]>;
}

const isExported = (statement: ts.Statement): boolean =>
  (statement as { modifiers?: ts.NodeArray<ts.ModifierLike> }).modifiers
    ?.some(modifier => modifier.kind === ts.SyntaxKind.ExportKeyword) === true;

/** The steps a function is written in, one written expression counted as a single step. */
function stepsOfBody(fn: ts.Node | undefined): ts.Node[] | undefined {
  if (!fn || !isFunctionLike(fn)) return undefined;
  const body = fn.body;
  if (!body) return undefined;
  return ts.isBlock(body) ? [...body.statements] : [body];
}

const isFunctionLike = (fn: ts.Node): fn is ts.FunctionLikeDeclaration =>
  ts.isFunctionDeclaration(fn) || ts.isFunctionExpression(fn) || ts.isArrowFunction(fn);

/** The names a built value usually gives the function that does its work. */
const behaviorNames = new Set(["execute", "handler", "handle", "run"]);

/**
 * The function written inside a value that is not itself a function: the `execute` member of a tool built by
 * `Tool.make({ …, execute: Effect.fn(…)(…) })`, or the first function the value holds when no member is named.
 */
function embeddedBehavior(project: Project, value: ts.Node): ts.FunctionLikeDeclaration | undefined {
  let named: ts.FunctionLikeDeclaration | undefined;
  let first: ts.FunctionLikeDeclaration | undefined;
  const visit = (node: ts.Node): void => {
    if (isFunctionLike(node) && node.body) {
      if (!first) first = node;
      return;
    }
    if (ts.isPropertyAssignment(node) && behaviorNames.has(propertyNameText(node.name) ?? "")) {
      named = embeddedBehavior(project, node.initializer);
      if (named) return;
    }
    ts.forEachChild(node, visit);
  };
  visit(value);
  return named ?? first;
}

/**
 * The functions a file exports, and the steps each one is written in: `export function work()` and
 * `export const execute = Effect.fn("…")(body)` both keep their function, so both can be compared. A value
 * built by a call keeps the function it holds — a `Tool.make` tool's `execute` body — so built tools compare too.
 */
function exportedFunctions(project: Project, file: ts.SourceFile): Map<string, ts.Node[]> {
  const found = new Map<string, ts.Node[]>();
  const keep = (name: string, declaration: ts.Declaration | undefined): void => {
    const steps = stepsOfBody(declaration ? implementationBody(project, declaration) : undefined) ??
      (declaration && ts.isVariableDeclaration(declaration) && declaration.initializer
        ? stepsOfBody(embeddedBehavior(project, declaration.initializer))
        : undefined);
    if (name && steps) found.set(name, steps);
  };
  for (const statement of file.statements) {
    if (!isExported(statement)) continue;
    if (ts.isFunctionDeclaration(statement) && statement.name) keep(statement.name.text, statement);
    else if (ts.isVariableStatement(statement)) {
      for (const declaration of statement.declarationList.declarations) {
        if (!ts.isIdentifier(declaration.name)) continue;
        keep(declaration.name.text, declaration);
      }
    }
  }
  return found;
}

function concernKind(statement: ts.Node): string {
  if (ts.isIfStatement(statement)) return "condition";
  if (ts.isForStatement(statement) || ts.isForOfStatement(statement) || ts.isForInStatement(statement) ||
      ts.isWhileStatement(statement) || ts.isDoStatement(statement)) return "repetition";
  if (ts.isTryStatement(statement)) return "failure handling";
  if (statement.kind === ts.SyntaxKind.CatchClause) return "failure recovery";
  if (ts.isReturnStatement(statement)) return "result";
  return "call";
}

/** The exported declarations of a member, as the source its own cells may cite. */
function exportedStatements(file: ts.SourceFile | undefined): ts.Statement[] {
  return file?.statements.filter(statement =>
    isExported(statement) && !ts.isExportDeclaration(statement)) ?? [];
}

/**
 * The groups a comparison can be made in: one group per exported callable two or more members hold. A member
 * joins a group by the name it shares, so a member of another shape cannot empty the group it would have
 * emptied had the names been intersected across every member.
 */
function comparableGroups(files: SiblingFile[]): { name: string; files: SiblingFile[] }[] {
  const names = [...new Set(files.flatMap(file => [...file.functions.keys()]))].sort();
  return names.flatMap(name => {
    const group = files.filter(file => file.functions.has(name));
    return group.length > 1 ? [{ name, files: group }] : [];
  });
}

/**
 * Compares the sibling files step by step, positionally, for every callable two or more of them export. The
 * members that join no group are reported as `unclear` rows over their own exports, and named separately so
 * that the caller can say they were left out rather than compared.
 */
export function siblingTable(project: Project, members: string[]): { siblings: Siblings; uncompared: string[] } {
  const files: SiblingFile[] = members.map(path => {
    const source = project.sourceOf({ file: path });
    return { path, source, functions: source ? exportedFunctions(project, source) : new Map() };
  });
  const rows: Siblings["rows"] = [];
  const groups = comparableGroups(files);
  for (const { name, files: group } of groups) {
    const bodies = group.map(file => file.functions.get(name)!);
    const depth = bodies.reduce((most, body) => Math.max(most, body.length), 0);
    for (let index = 0; index < depth; index++) {
      const steps = bodies.map(body => body[index]);
      const complete = steps.every(step => step !== undefined);
      const identical = complete && steps.every(step => step!.getText() === steps[0]!.getText());
      rows.push({
        concern: `${concernKind(steps.find(Boolean) as ts.Node)} (${name}, step ${index + 1})`,
        status: !complete ? "unclear" : identical ? "shared" : "varies",
        cells: group.flatMap((file, member) => {
          const step = steps[member];
          if (!step) return [];
          return [{ member: file.path, text: step.getText(), at: located(project, step) }];
        }),
      });
    }
  }
  const compared = new Set(groups.flatMap(group => group.files.map(file => file.path)));
  const uncompared = files.filter(file => !compared.has(file.path));
  for (const file of uncompared) {
    const cells = exportedStatements(file.source).map(statement => ({
      member: file.path, text: statement.getText(), at: located(project, statement),
    }));
    if (cells.length) rows.push({
      concern: `no exported callable in common with the other siblings (${file.path})`,
      status: "unclear",
      cells,
    });
  }
  return { siblings: { members, rows }, uncompared: uncompared.map(file => file.path) };
}