// Round 5, S3 (SPEC.md "S3 Path files"): the path a successful task took, as a YAML file under the root. The guard
// reads ids, counts, numbers and paths out of it — never the author's own text — so a path file can be compared with
// its parent (what it changed, whether it was better) and reported as a warning when it misses an aim.

import * as fs from "node:fs";
import * as path from "node:path";
import { readJournal } from "./journal.ts";
import type { FailureRecord, Finding, PathReport, SuccessPath, SuccessRecord } from "./types.ts";

const GUARD_DIR = ".harness-guard";
const PATHS_DIR = path.join(GUARD_DIR, "paths");
const RUNS_DIR = "runs";
const AIM_PERCENT = 2;

export class PathError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "PathError";
  }
}

// ---- loading ---------------------------------------------------------------------------------------------------

function isEntry(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

// A value that counts as written: a string with something in it. Blank and non-strings do not.
function text(value: unknown): string {
  return typeof value === "string" ? value.trim() : "";
}

function numeric(value: unknown): value is number {
  return typeof value === "number" && Number.isFinite(value);
}

function measureValue(value: unknown): number | null {
  return numeric(value) ? value : null;
}

// The numeric entries of a measures mapping; anything else in it is not a measure.
function numbers(value: unknown): Record<string, number> {
  const found: Record<string, number> = {};
  if (!isEntry(value)) return found;
  for (const [key, each] of Object.entries(value)) {
    const number = measureValue(each);
    if (number !== null) found[key] = number;
  }
  return found;
}

function idList(value: unknown): string[] {
  if (!Array.isArray(value)) return [];
  return value.map(text).filter((each) => each !== "");
}

export function loadPath(file: string): SuccessPath {
  const name = path.basename(file);
  let parsed: unknown;
  try {
    parsed = Bun.YAML.parse(fs.readFileSync(file, "utf8"));
  } catch {
    // The parser's own message would carry the source line, so the diagnostic stays generic.
    throw new PathError(`path ${name}: cannot be read or parsed`);
  }
  if (!isEntry(parsed) || parsed.path !== 1) {
    throw new PathError(`path ${name}: has no numeric "path: 1" marker`);
  }
  return parsed as unknown as SuccessPath;
}

// ---- discovery --------------------------------------------------------------------------------------------------

function readDirSafe(dir: string): fs.Dirent[] {
  try {
    return fs.readdirSync(dir, { withFileTypes: true });
  } catch {
    return [];
  }
}

// Under .harness-guard/paths/ every *.yaml counts, whatever its name; under runs/** only success-path*.yaml.
function isPathName(name: string): boolean {
  return name.startsWith("success-path") && name.endsWith(".yaml");
}

function isGuardPathName(name: string): boolean {
  return name.endsWith(".yaml");
}

export function findPathFiles(root: string): string[] {
  const found: string[] = [];

  for (const entry of readDirSafe(path.join(root, PATHS_DIR))) {
    if (entry.isFile() && isGuardPathName(entry.name)) found.push(path.join(PATHS_DIR, entry.name));
  }

  const walk = (dir: string, relative: string): void => {
    for (const entry of readDirSafe(dir)) {
      const childRelative = path.join(relative, entry.name);
      if (entry.isDirectory()) {
        if (entry.name === ".git" || entry.name === "node_modules" || childRelative === GUARD_DIR) continue;
        walk(path.join(dir, entry.name), childRelative);
        continue;
      }
      if (!entry.isFile()) continue;
      const parts = childRelative.split(path.sep);
      const name = parts[parts.length - 1]!;
      if (parts[0] === RUNS_DIR && isPathName(name)) found.push(childRelative);
    }
  };
  walk(path.join(root, RUNS_DIR), RUNS_DIR);

  return found.sort();
}

// ---- checks -----------------------------------------------------------------------------------------------------

function fail(rule: string, message: string, fix: string): Finding {
  return { rule, severity: "fail", message, fix, ref: "SPEC.md S3" };
}

function exists(target: string): boolean {
  try {
    fs.statSync(target);
    return true;
  } catch {
    return false;
  }
}

// One decimal, and the sign a reader expects: positive is improved on the aim's measure.
function round1(value: number): number {
  return Number(value.toFixed(1));
}

export function checkPath(root: string, file: string): PathReport {
  const findings: Finding[] = [];

  let doc: SuccessPath;
  try {
    doc = loadPath(path.join(root, file));
  } catch {
    return {
      file,
      findings: [
        fail(
          "R12.7-path-missing",
          `${file}: not a readable path file (no numeric "path: 1" marker)`,
          "start from the skeleton: cli.ts path new --session <id> --out <file>",
        ),
      ],
      better: null,
      gainPercent: null,
      repeatedFailures: [],
    };
  }

  if (text(doc.session) === "") {
    findings.push(fail("R12.7-path-missing", "session is missing or empty", "session: the id this task ran in."));
  }
  if (text(doc.category) === "") {
    findings.push(fail("R12.7-path-missing", "category is missing or empty", "category: <the kind of task, for the parents of a later run>."));
  }
  if (text(doc.objective) === "") {
    findings.push(fail("R12.7-path-missing", "objective is missing or empty", "objective: <what the task had to achieve>, in one line."));
  }

  const steps = Array.isArray(doc.steps) ? doc.steps : [];
  const done = steps.filter((step) => isEntry(step) && text(step.did) !== "").length;
  if (done === 0) {
    findings.push(fail("R12.7-path-missing", `steps: none of ${steps.length} steps has a non-empty did`, "steps: - did: <what happened>, one item per step."));
  } else if (done !== steps.length) {
    findings.push(fail("R12.7-path-missing", `steps: ${steps.length - done} of ${steps.length} steps have no did`, "give every step a did: <what happened>."));
  }

  const childMeasures = numbers(doc.measures);
  if (Object.keys(childMeasures).length === 0) {
    findings.push(fail("R12.7-path-missing", "measures: no numeric entry", "measures: { <name>: <number> } — at least one, e.g. seconds or failures."));
  }

  let parent: SuccessPath | null = null;
  const parentRef = text(doc.parent);
  if (parentRef !== "") {
    try {
      parent = loadPath(path.join(root, parentRef));
    } catch {
      parent = null;
    }
    if (parent === null) {
      findings.push(
        fail("R12.7-parent-missing", `parent ${parentRef} is missing or is not a path file`, "parent: the relative path of an earlier path file, or drop the field."),
      );
    }
  }

  let aimMeasure = "";
  let parentValue: number | null = null;
  let gainPercent: number | null = null;

  if (parent !== null) {
    if (text(doc.change) === "") {
      findings.push(
        fail("R12.7-copied", "change is empty: a child that names a parent must say what it changed", "change: <what this run did differently from the parent>."),
      );
    }

    const parentMeasures = numbers(parent.measures);
    const aim = isEntry(doc.aim) ? doc.aim : null;
    // SPEC S3: with a parent, the aim is required — a child must say what it tries to improve (COO, round 5).
    if (aim === null) {
      findings.push(
        fail("R12.7-aim-missing", "a child that names a parent has no aim", "aim: measure: <a name present in both measures>, parent_value: <the parent's value>, lower_is_better: true|false"),
      );
    }
    if (aim !== null) {
      aimMeasure = text(aim.measure);
      const inChild = aimMeasure !== "" && measureValue(childMeasures[aimMeasure]) !== null;
      const inParent = aimMeasure !== "" && measureValue(parentMeasures[aimMeasure]) !== null;
      if (!inChild || !inParent) {
        findings.push(
          fail(
            "R12.7-aim-missing",
            `aim.measure ${aimMeasure === "" ? "(none)" : aimMeasure} is not a measure in both this file and the parent`,
            "aim: measure: <a name present in both measures>, lower_is_better: true|false",
          ),
        );
      } else if (measureValue(aim.parent_value) === null || aim.parent_value !== parentMeasures[aimMeasure]) {
        findings.push(
          fail(
            "R12.7-aim-mismatch",
            `aim.parent_value is not the parent's ${aimMeasure}`,
            "aim.parent_value must be the value the parent's file holds on that measure.",
          ),
        );
      } else if (parentMeasures[aimMeasure] !== 0) {
        // Positive means improved: the direction the aim declares decides which side the child is on.
        const parentNumber = parentMeasures[aimMeasure]!;
        const childNumber = childMeasures[aimMeasure]!;
        const lowerIsBetter = aim.lower_is_better === true;
        const raw = lowerIsBetter ? (parentNumber - childNumber) / parentNumber : (childNumber - parentNumber) / parentNumber;
        gainPercent = round1(raw * 100);
        parentValue = parentNumber;
      }
    }
  }

  const childFailures = idList(doc.failures);
  const parentFailures = idList(parent === null ? undefined : parent.failures);
  const repeatedFailures = childFailures.filter((each) => parentFailures.includes(each));
  const better = gainPercent === null ? null : gainPercent > 0 && repeatedFailures.length === 0;

  if (gainPercent !== null) {
    // The aim is reported, never a finding: a child 1% better than its aim passed.
    findings.push({
      rule: "R12.7-aim-report",
      severity: "warn",
      message: `gain ${gainPercent.toFixed(1)}% against a ${AIM_PERCENT}% aim`,
      fix: `aim.measure ${aimMeasure}${parentValue === null ? "" : ` (parent ${parentValue})`}: reach the ${AIM_PERCENT}% aim or say why not.`,
      ref: "SPEC.md S3",
    });
  }

  if (doc.great !== undefined && doc.great !== null) {
    const great = isEntry(doc.great) ? doc.great : null;
    const comparison = great === null ? "" : text(great.comparison);
    const evidence = great === null ? "" : text(great.evidence);
    if (comparison === "") {
      findings.push(fail("R12.7-great-evidence", "great.comparison is missing or empty", "great: comparison: <what this beat>, in one line."));
    }
    if (evidence === "") {
      findings.push(fail("R12.7-great-evidence", "great.evidence is missing or empty", "great: evidence: <the path of a file that exists>."));
    } else if (!exists(path.resolve(root, evidence))) {
      findings.push(fail("R12.7-great-evidence", "great.evidence names a path that does not exist", "great: evidence: <the path of a file or folder that exists under the root>."));
    }
  }

  return { file, findings, better, gainPercent, repeatedFailures };
}

// ---- skeleton ---------------------------------------------------------------------------------------------------

function plain(value: string): boolean {
  return /^[A-Za-z0-9_][A-Za-z0-9 _./-]*$/.test(value);
}

// A YAML scalar: plain when it can be, quoted otherwise, so a session id with a colon in it still parses.
function scalar(value: string): string {
  return plain(value) ? value : JSON.stringify(value);
}

// The path skeleton for a session: the journal's own counts and check ids are filled in, everything the agent has to
// write is an empty placeholder. Command text and output never reach it — ids, counts and numbers only.
export function skeleton(root: string, session: string, out?: string): string {
  const { records } = readJournal(root);
  const failures = records.filter((record): record is FailureRecord => record.kind === "failure" && record.session === session);
  const successes = records.filter((record): record is SuccessRecord => record.kind === "success" && record.session === session);

  const checks: string[] = [];
  for (const record of failures) if (!checks.includes(record.check)) checks.push(record.check);

  const checkLines = checks.map((each) => `  - ${scalar(each)}`);
  const yaml = [
    "# The path of this task: what was done, in order, and what it measured.",
    "# The placeholders are empty on purpose — fill them; nothing here is read but ids, counts and numbers.",
    "path: 1",
    `session: ${scalar(session)}`,
    'category: ""',
    'objective: ""',
    "steps:",
    '  - did: ""',
    '    engine: ""',
    '    model: ""',
    '    check: ""',
    "decisions: []",
    "measures:",
    `  failures: ${failures.length}`,
    `  successes: ${successes.length}`,
    checkLines.length > 0 ? "failures:" : "failures: []",
    ...(checkLines.length > 0 ? checkLines : []),
    "# parent: runs/<run>/success-path.yaml   # an earlier path in this category",
    '# change: ""                            # what this run did differently',
    "# aim:                                  # the bar this run aimed at",
    "#   measure: seconds",
    "#   parent_value: 0",
    "#   lower_is_better: true",
    "# great:                                # only when the result beat a known best",
    '#   comparison: ""',
    '#   evidence: ""',
    "",
  ].join("\n");

  if (out !== undefined && out !== "") {
    const base = path.resolve(root);
    const target = path.resolve(base, out);
    if (target !== base && !target.startsWith(base + path.sep)) {
      throw new PathError("out: a path file is only written inside the root");
    }
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, yaml, "utf8");
  }

  return yaml;
}

// ---- parents ----------------------------------------------------------------------------------------------------

// The path files of one category, most recent file name last, with the measures a child aims against and whether the
// file was itself better than its own parent.
export function parents(
  root: string,
  category: string,
): { file: string; measures: Record<string, number>; better: boolean | null }[] {
  const found: { file: string; measures: Record<string, number>; better: boolean | null }[] = [];
  for (const file of findPathFiles(root)) {
    let doc: SuccessPath;
    try {
      doc = loadPath(path.join(root, file));
    } catch {
      continue;
    }
    if (text(doc.category) !== category.trim()) continue;
    found.push({ file, measures: numbers(doc.measures), better: checkPath(root, file).better });
  }
  return found;
}