import ts from "typescript";
import type { Siblings } from "./answer.ts";
import { implementationBody, located } from "./nodes.ts";
import type { Project } from "./project.ts";

interface SiblingFile {
  path: string;
  functions: Map<string, ts.Node[]>;
}

/** The steps a function is written in, one written expression counted as a single step. */
function stepsOfBody(fn: ts.Node | undefined): ts.Node[] | undefined {
  if (!fn || !isFunctionLike(fn)) return undefined;
  const body = fn.body;
  if (!body) return undefined;
  return ts.isBlock(body) ? [...body.statements] : [body];
}

const isFunctionLike = (fn: ts.Node): fn is ts.FunctionLikeDeclaration =>
  ts.isFunctionDeclaration(fn) || ts.isFunctionExpression(fn) || ts.isArrowFunction(fn);

/**
 * The functions a file exports, and the steps each one is written in: `export function work()` and
 * `export const execute = Effect.fn("…")(body)` both keep their function, so both can be compared.
 */
function exportedFunctions(project: Project, file: ts.SourceFile): Map<string, ts.Node[]> {
  const found = new Map<string, ts.Node[]>();
  const keep = (name: string, fn: ts.Node | undefined): void => {
    const steps = stepsOfBody(fn);
    if (name && steps) found.set(name, steps);
  };
  for (const statement of file.statements) {
    const { modifiers } = statement as { modifiers?: ts.NodeArray<ts.ModifierLike> };
    if (!modifiers?.some(modifier => modifier.kind === ts.SyntaxKind.ExportKeyword)) continue;
    if (ts.isFunctionDeclaration(statement) && statement.name) keep(statement.name.text, statement);
    else if (ts.isVariableStatement(statement)) {
      for (const declaration of statement.declarationList.declarations) {
        if (!ts.isIdentifier(declaration.name)) continue;
        keep(declaration.name.text, implementationBody(project, declaration));
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

/** Compares sibling files step by step, positionally, for the names every sibling exports. */
export function siblingTable(project: Project, members: string[]): Siblings | undefined {
  const files: SiblingFile[] = members.map(path => ({
    path,
    functions: project.sourceOf({ file: path }) ? exportedFunctions(project, project.sourceOf({ file: path })!) : new Map(),
  }));
  const sharedNames = [...(files[0]?.functions.keys() ?? [])].filter(name => files.every(file => file.functions.has(name)));
  const rows: Siblings["rows"] = [];
  for (const name of sharedNames) {
    const bodies = files.map(file => file.functions.get(name)!);
    const depth = bodies.reduce((most, body) => Math.max(most, body.length), 0);
    for (let index = 0; index < depth; index++) {
      const steps = bodies.map(body => body[index]);
      const complete = steps.every(step => step !== undefined);
      const identical = complete && steps.every(step => step!.getText() === steps[0]!.getText());
      rows.push({
        concern: `${concernKind(steps.find(Boolean) as ts.Node)} (${name}, step ${index + 1})`,
        status: !complete ? "unclear" : identical ? "shared" : "varies",
        cells: files.flatMap((file, member) => {
          const step = steps[member];
          if (!step) return [];
          return [{ member: file.path, text: step.getText(), at: located(project, step) }];
        }),
      });
    }
  }
  return { members, rows };
}