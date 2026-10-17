import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import { isObject, selectPath, type Expectation } from "./matcher.ts";
import { requirementLines, type Requirement } from "./requirements.ts";

export type EvalCase = { id: string; requirement: Requirement; line: string; args: string[]; tests?: string[]; format?: "json" | "text"; expect: Expectation };
export type CaseFile = { project: string[]; root: string; tests: string[]; cases: EvalCase[] };
export type LoadedCaseFile = CaseFile & { source: string };

function stringArray(value: unknown): value is string[] {
  return Array.isArray(value) && value.every(item => typeof item === "string");
}

export function validateCaseFile(value: unknown): CaseFile {
  if (!isObject(value) || !stringArray(value.project) || !value.project.length ||
      typeof value.root !== "string" || !stringArray(value.tests) || !Array.isArray(value.cases)) {
    throw new Error("Case file needs project: string[], root: string, tests: string[], cases: array");
  }
  const ids = new Set<string>();
  for (const candidate of value.cases) {
    if (!isObject(candidate) || typeof candidate.id !== "string" || !candidate.id || ids.has(candidate.id) ||
        typeof candidate.requirement !== "string" || !(candidate.requirement in requirementLines) ||
        typeof candidate.line !== "string" || !stringArray(candidate.args) || !candidate.args.length || !isObject(candidate.expect)) {
      throw new Error("Invalid or duplicate case: " + JSON.stringify(candidate));
    }
    if (candidate.tests !== undefined && !stringArray(candidate.tests)) throw new Error(`Invalid test patterns in ${candidate.id}`);
    if (candidate.format !== undefined && !["json", "text"].includes(candidate.format as string)) throw new Error(`Invalid format in ${candidate.id}`);
    if (candidate.expect.textIncludes !== undefined && !stringArray(candidate.expect.textIncludes)) throw new Error(`Invalid text expectations in ${candidate.id}`);
    if (candidate.expect.shapes !== undefined && !Array.isArray(candidate.expect.shapes)) throw new Error(`Invalid shapes in ${candidate.id}`);
    if (candidate.expect.exactLimitReasons !== undefined && !stringArray(candidate.expect.exactLimitReasons)) throw new Error(`Invalid exact limit reasons in ${candidate.id}`);
    ids.add(candidate.id);
    const lines: readonly string[] = requirementLines[candidate.requirement as Requirement];
    if (!lines.includes(candidate.line.replace(/\.$/, ""))) throw new Error(`Unknown Fails-if line in ${candidate.id}: ${candidate.line}`);
    candidate.line = candidate.line.replace(/\.$/, "");
    const expect = candidate.expect;
    if (!Array.isArray(expect.includes) || !Array.isArray(expect.excludes) || !Array.isArray(expect.equals) ||
        ![true, false, null].includes(expect.ambiguous as boolean | null) || !stringArray(expect.limitReasons)) {
      throw new Error(`Invalid expectation in ${candidate.id}`);
    }
    for (const location of [...expect.includes, ...expect.excludes]) {
      if (!isObject(location) || typeof location.path !== "string" || typeof location.file !== "string" ||
          !Number.isInteger(location.line) || (location.line as number) < 1) throw new Error(`Invalid location in ${candidate.id}`);
      selectPath({}, location.path);
    }
    for (const equality of [...expect.equals, ...(expect.shapes as unknown[] ?? [])]) {
      if (!isObject(equality) || typeof equality.path !== "string" || !Object.hasOwn(equality, "value")) {
        throw new Error(`Invalid equality in ${candidate.id}`);
      }
      selectPath({}, equality.path);
    }
  }
  return value as CaseFile;
}

export async function loadCaseFile(path: string): Promise<LoadedCaseFile> {
  const source = resolve(path);
  const value = validateCaseFile(JSON.parse(await readFile(source, "utf8")));
  // Bundled examples remain runnable from either the repository or the package directory.
  const base = source === resolve(import.meta.dir, "cases/fixtures.json") ? resolve(import.meta.dir, "..") : process.cwd();
  return { ...value, source, root: resolve(base, value.root), project: value.project.map(project => resolve(base, project)) };
}
