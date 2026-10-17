import ts from "typescript";
import type { Loc, Step, StepKind } from "./answer.ts";
import { implementationBody, located } from "./nodes.ts";
import type { Project } from "./project.ts";

function at(project: Project, node: ts.Node): Loc {
  return located(project, node);
}

function isCatchClause(node: ts.Node): node is ts.CatchClause {
  return node.kind === ts.SyntaxKind.CatchClause;
}

function loopBodyOf(statement: ts.Statement): ts.Statement | undefined {
  if (ts.isForStatement(statement) || ts.isForOfStatement(statement) || ts.isForInStatement(statement) ||
      ts.isWhileStatement(statement) || ts.isDoStatement(statement)) {
    return (statement as ts.ForStatement).statement;
  }
  return undefined;
}

function stepKindOf(statement: ts.Statement): StepKind | undefined {
  if (ts.isIfStatement(statement)) return "if";
  if (ts.isForStatement(statement) || ts.isForOfStatement(statement) || ts.isForInStatement(statement) ||
      ts.isWhileStatement(statement) || ts.isDoStatement(statement)) return "loop";
  if (ts.isTryStatement(statement)) return "try";
  if (isCatchClause(statement)) return "catch";
  if (ts.isReturnStatement(statement)) return "return";
  if (ts.isExpressionStatement(statement)) {
    const expression = statement.expression;
    if (ts.isYieldExpression(expression)) return "yield*";
    return "call";
  }
  if (ts.isVariableStatement(statement)) return "call";
  if (ts.isBlock(statement)) return "call";
  return undefined;
}

function expressionSteps(project: Project, node: ts.Node): Step[] {
  const steps: Step[] = [];
  const visit = (child: ts.Node): void => {
    if (child !== node && (ts.isFunctionDeclaration(child) || ts.isFunctionExpression(child) || ts.isArrowFunction(child) ||
        ts.isMethodDeclaration(child) || ts.isClassDeclaration(child) || ts.isGetAccessorDeclaration(child) ||
        ts.isSetAccessorDeclaration(child))) {
      return;
    }
    if (ts.isCallExpression(child) || ts.isNewExpression(child)) {
      steps.push({ kind: "call", at: at(project, child), text: child.getText(child.getSourceFile()) });
    } else if (ts.isYieldExpression(child)) {
      steps.push({ kind: "yield*", at: at(project, child), text: child.getText(child.getSourceFile()) });
    }
    ts.forEachChild(child, visit);
  };
  ts.forEachChild(node, visit);
  return steps;
}

function statementStep(project: Project, statement: ts.Statement): Step[] {
  const kind = stepKindOf(statement);
  if (!kind) return [];
  const text = statement.getText(statement.getSourceFile());
  const location = at(project, statement);
  if (ts.isBlock(statement)) {
    return statement.statements.flatMap(child => statementStep(project, child));
  }
  if (ts.isIfStatement(statement)) {
    const children: Step[] = ts.isBlock(statement.thenStatement)
      ? statement.thenStatement.statements.flatMap(child => statementStep(project, child))
      : statementStep(project, statement.thenStatement);
    const branch = statement.elseStatement;
    if (branch) {
      const inner = ts.isBlock(branch)
        ? branch.statements.flatMap(child => statementStep(project, child))
        : statementStep(project, branch);
      children.push({ kind: "else", at: at(project, branch), text: branch.getText(branch.getSourceFile()), children: inner });
    }
    return [{ kind: "if", at: location, text, children }];
  }
  if (ts.isTryStatement(statement)) {
    const children = statement.tryBlock.statements.flatMap(child => statementStep(project, child));
    const clause = statement.catchClause;
    if (clause) {
      children.push({ kind: "catch", at: at(project, clause), text: clause.getText(clause.getSourceFile()),
        children: clause.block.statements.flatMap(child => statementStep(project, child)) });
    }
    if (statement.finallyBlock) {
      children.push(...statement.finallyBlock.statements.flatMap(child => statementStep(project, child)));
    }
    return [{ kind: "try", at: location, text, children }];
  }
  if (isCatchClause(statement)) {
    return [{ kind: "catch", at: location, text, children: statement.block.statements.flatMap(child => statementStep(project, child)) }];
  }
  const loopBody = loopBodyOf(statement);
  if (loopBody) {
    const children = ts.isBlock(loopBody) ? loopBody.statements.flatMap(child => statementStep(project, child)) : statementStep(project, loopBody);
    return [{ kind: "loop", at: location, text, children }];
  }
  const children = expressionSteps(project, statement);
  return [{ kind, at: location, text, ...(children.length ? { children } : {}) }];
}

export function stepsOf(project: Project, node: ts.Node): Step[] {
  const implementation = implementationBody(project, node);
  const body = implementation && ts.isFunctionLike(implementation) ? (implementation as { body?: ts.Node }).body : undefined;
  if (!body || !ts.isBlock(body)) return [];
  return body.statements.flatMap(statement => statementStep(project, statement));
}
