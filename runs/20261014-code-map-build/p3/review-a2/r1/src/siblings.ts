import ts from "typescript";
import type { Siblings } from "./answer.ts";
import { located } from "./nodes.ts";
import type { Project } from "./project.ts";

interface SiblingFile {
  path: string;
  functions: Map<string, ts.FunctionDeclaration>;
}

function exportedFunctions(file: ts.SourceFile): Map<string, ts.FunctionDeclaration> {
  const found = new Map<string, ts.FunctionDeclaration>();
  for (const statement of file.statements) {
    if (!ts.isFunctionDeclaration(statement) || !statement.name || !statement.body) continue;
    const exported = statement.modifiers?.some(modifier => modifier.kind === ts.SyntaxKind.ExportKeyword) ?? false;
    if (exported) found.set(statement.name.text, statement);
  }
  return found;
}

function concernKind(statement: ts.Statement): string {
  if (ts.isIfStatement(statement)) return "condition";
  if (ts.isForStatement(statement) || ts.isForOfStatement(statement) || ts.isForInStatement(statement) ||
      ts.isWhileStatement(statement) || ts.isDoStatement(statement)) return "repetition";
  if (ts.isTryStatement(statement)) return "failure handling";
  if (statement.kind === ts.SyntaxKind.CatchClause) return "failure recovery";
  if (ts.isReturnStatement(statement)) return "result";
  return "call";
}

/** Compares sibling files statement by statement, positionally, for the names every sibling exports. */
export function siblingTable(project: Project, members: string[]): Siblings | undefined {
  const files: SiblingFile[] = members.map(path => ({
    path,
    functions: project.sourceOf({ file: path }) ? exportedFunctions(project.sourceOf({ file: path })!) : new Map(),
  }));
  const sharedNames = [...(files[0]?.functions.keys() ?? [])].filter(name => files.every(file => file.functions.has(name)));
  const rows: Siblings["rows"] = [];
  for (const name of sharedNames) {
    const bodies = files.map(file => file.functions.get(name)!.body!.statements);
    const depth = bodies.reduce((most, body) => Math.max(most, body.length), 0);
    for (let index = 0; index < depth; index++) {
      const statements = bodies.map(body => body[index]);
      const complete = statements.every(statement => statement !== undefined);
      const identical = complete && statements.every(statement => statement!.getText() === statements[0]!.getText());
      rows.push({
        concern: `${concernKind(statements.find(Boolean) as ts.Statement)} (step ${index + 1})`,
        status: !complete ? "unclear" : identical ? "shared" : "varies",
        cells: files.flatMap((file, member) => {
          const statement = statements[member];
          if (!statement) return [];
          return [{ member: file.path, text: statement.getText(), at: located(project, statement) }];
        }),
      });
    }
  }
  return { members, rows };
}