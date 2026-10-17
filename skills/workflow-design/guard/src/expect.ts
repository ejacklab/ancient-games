// Round 12 (SPEC.md, E1–E4): a planned red run. The agent declares, before a test run, that the next run naming a test
// file must fail — the red step of writing a test before the change. A run it covers that fails is recorded as red, not
// as a failure; one that passes is the failure. Without a declaration every failing run is a failure (D1).

import { spawnSync } from "node:child_process";
import { randomBytes } from "node:crypto";
import * as fs from "node:fs";
import * as path from "node:path";
import { appendFailure, appendRecord, newFailureId, readJournal } from "./journal.ts";
import { FAILED_SUMMARY, recognizeTestRun, segments, testRunFiles } from "./traps.ts";
import type { ExpectFailRecord, FailureRecord, RedRecord } from "./types.ts";

export class ExpectError extends Error {}

export function newExpectId(): string {
  return `E-${randomBytes(4).toString("hex")}`;
}

// E1: `file` is absolute or relative to the caller's folder; it is stored relative to the root.
export function declareRed(root: string, file: string, session: string, now: Date): ExpectFailRecord {
  const target = path.resolve(file);
  const relative = path.relative(root, target);
  if (relative === "" || relative.startsWith("..") || path.isAbsolute(relative)) {
    throw new ExpectError(`expect-fail: outside the root: ${file}`);
  }
  if (!fs.existsSync(target) || !fs.statSync(target).isFile()) throw new ExpectError(`expect-fail: no such file: ${file}`);
  const record: ExpectFailRecord = { kind: "expect-fail", id: newExpectId(), time: now.toISOString(), session, file: relative };
  appendRecord(root, record);
  return record;
}

// The session's declarations no run has consumed yet: a red record or a red-passed failure names the ones it consumed.
export function openDeclarations(root: string, session: string): ExpectFailRecord[] {
  const records = readJournal(root).records;
  const consumed = new Set<string>();
  for (const record of records) {
    if ((record.kind === "red" || record.kind === "failure") && Array.isArray(record.declared)) {
      for (const id of record.declared) consumed.add(id);
    }
  }
  return records.filter((record): record is ExpectFailRecord =>
    record.kind === "expect-fail" && record.session === session && !consumed.has(record.id));
}

// E2: the open declarations a test run covers — those whose file is one of the absolute paths the run names.
export function coveringDeclarations(root: string, session: string, named: string[]): string[] {
  const files = new Set(named);
  return openDeclarations(root, session)
    .filter((record) => files.has(path.resolve(root, record.file)))
    .map((record) => record.id);
}

// ---- the guard runs the red run (round 16, X1–X4) ----------------------------------------------------------------

export interface RedRun {
  runner: string;
  exit: number | null;
  out: string; // the output file, relative to the root
  record: RedRecord | FailureRecord;
}

function inside(root: string, target: string): boolean {
  const relative = path.relative(root, target);
  return relative !== "" && !relative.startsWith("..") && !path.isAbsolute(relative);
}

// X1–X3: declare each test file the command names, run the command with its stdout and stderr in `outFile`, and record
// the result from the runner's own exit — so no pipe, redirect or later command in the agent's call can hide it
// (F-d3132a7f). Nothing is declared or run when the command is refused.
export function runRed(root: string, command: string, cwd: string, outFile: string, session: string, harness: string,
  now: () => Date): RedRun {
  if (segments(command).length !== 1) {
    throw new ExpectError("expect-fail --run: give the test command alone — no pipe, `;` or `&&` — so the exit is the runner's");
  }
  const runner = recognizeTestRun(command);
  if (runner === null) throw new ExpectError("expect-fail --run: the command is not a test run the guard recognises");
  const files = [...new Set(testRunFiles(command, cwd))].filter((file) => fs.existsSync(file) && fs.statSync(file).isFile());
  if (files.length === 0) throw new ExpectError("expect-fail --run: the command names no test file");
  const outside = files.find((file) => !inside(root, file));
  if (outside !== undefined) throw new ExpectError(`expect-fail --run: outside the root: ${outside}`);
  const target = path.resolve(cwd, outFile);
  if (!inside(root, target)) throw new ExpectError(`expect-fail --run: --out must be inside the root: ${outFile}`);

  const declared = files.map((file) => declareRed(root, file, session, now()).id);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  const fd = fs.openSync(target, "w");
  let exit: number | null;
  try {
    exit = spawnSync("bash", ["-c", command], { cwd, stdio: ["ignore", fd, fd] }).status;
  } finally {
    fs.closeSync(fd);
  }
  const out = path.relative(root, target);
  if (exit !== 0) {
    // X2: a run that did not exit 0 — a failed test, or a run that ended on a signal — is the red step.
    const summary = FAILED_SUMMARY.exec(fs.readFileSync(target, "utf8"));
    const record: RedRecord = { kind: "red", time: now().toISOString(), session, runner, declared,
      failed: summary === null ? null : Number(summary[1]), exit };
    appendRecord(root, record);
    return { runner, exit, out, record };
  }
  // X3: a declared red run that passed is the failure E4 names, with the run's output as its evidence.
  const record: FailureRecord = {
    kind: "failure", id: newFailureId(), time: now().toISOString(), session, found_by: "guard",
    check: "R12.2-red-passed", input: `${runner} run`, expected: "the declared red run fails", actual: "no test failed",
    engine: "none", harness, reason: `the ${runner} run was declared red (${declared.join(", ")}) and no test failed`,
    evidence: out, declared,
  };
  appendFailure(root, record);
  return { runner, exit, out, record };
}
