// Round 19 (SPEC.md, V1–V7): the requirements evaluator's verdict reaches the guard. A failing requirement group is a
// failure under R12.2 — the stop that ends the run asks for its insight — an UNKNOWN is the owner's to read, and a PASS
// writes nothing. The same verdict is ingested once: the same finding twice is one finding, so the bytes' hash is the
// key. V6 (round 3, measured on the six K2 calibration verdicts): one fault fails every id of its group, so the group
// is the unit — one record per group, never one per id. V7: a group that failed before the change was judged is a note,
// but by case (round 3b): a FAIL case the baseline did not fail is a new fault inside an old group, and it is a failure.

import { createHash } from "node:crypto";
import * as fs from "node:fs";
import * as path from "node:path";
import { appendFailure, newFailureId, writeEvidence } from "./journal.ts";
import type { FailureRecord } from "./types.ts";

const GUARD_DIR = ".harness-guard";
const NOTES_FILE = "evaluator-notes.md";
const INGESTED_FILE = "evaluations.jsonl";
const DOT = "\u00b7"; // the separator of a note line: `- <id> · UNKNOWN · <reason>`

export class EvaluationError extends Error {}

// The rows of verdict.json, read defensively: the file is written by another program, so a field may be missing or of
// another type. Nothing here trusts the shape; every value is checked where it is used.
interface VerdictCase {
  case?: unknown;
  verdict?: unknown;
  repro?: unknown;
}

interface VerdictRequirement {
  id?: unknown;
  group?: unknown;
  verdict?: unknown;
  reason?: unknown;
}

export interface IngestResult {
  fails: number; // requirements recorded as failures this run
  unknowns: number; // requirements noted this run
  passes: number; // requirements that are neither a FAIL nor an UNKNOWN
  problem: string | null; // V4: why the verdict could not be read — a note, never a failure
  already: boolean; // V3: these exact bytes were ingested before
}

function text(value: unknown): string {
  return typeof value === "string" ? value.trim() : "";
}

function isEntry(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

// A case belongs to a requirement's group when its id is the group's name or carries it as its prefix: the evaluator
// writes `G1-F1` and its own verdict.md joins the rows the same way (tools/evaluator/verdict.py).
function casesOfGroup(cases: VerdictCase[], group: string): VerdictCase[] {
  if (group === "") return [];
  return cases.filter((entry) => {
    const id = text(entry.case);
    return id === group || id.startsWith(`${group}-`);
  });
}

interface FailingGroup {
  group: string;
  ids: string[];
  reason: string;
}

// V6: one failure per failing group. A group is the row's `group` field, or the id itself when the row names no group
// (a requirement with no group is a group of one). Ids keep the order the verdict lists them, so the joined input is
// the evaluator's own order.
function failingGroups(rows: VerdictRequirement[]): FailingGroup[] {
  const byGroup = new Map<string, FailingGroup>();
  for (const row of rows) {
    if (text(row.verdict).toUpperCase() !== "FAIL") continue;
    const id = text(row.id);
    const group = text(row.group) || id;
    const found = byGroup.get(group);
    if (found === undefined) byGroup.set(group, { group, ids: [id], reason: text(row.reason) });
    else {
      found.ids.push(id);
      if (found.reason === "") found.reason = text(row.reason);
    }
  }
  return [...byGroup.values()];
}

// The groups a verdict holds as failing: the same reading, so a baseline and the verdict judged against it are compared
// like with like.
function failingGroupNames(rows: VerdictRequirement[]): Set<string> {
  return new Set(failingGroups(rows).map((entry) => entry.group));
}

// The ids of a group's FAIL cases. A case belongs to the group its id starts with, as casesOfGroup reads it.
function failingCaseIds(cases: VerdictCase[], group: string): Set<string> {
  return new Set(
    casesOfGroup(cases, group)
      .filter((entry) => text(entry.verdict).toUpperCase() === "FAIL")
      .map((entry) => text(entry.case)),
  );
}

// V7, by case (measured on K2 run k2-4, where the planted fault was a new FAIL case inside a group the baseline already
// failed — comparing groups alone hid it): a group held back as failing before the change is a note only when every one of
// its FAIL cases was FAIL in the baseline too. A FAIL case the baseline did not fail makes the group a failure. The
// requirement rows and the case rows are both asked: the group must have failed before, and none of its faults may be new.
// A case the baseline says nothing about was not failed by the baseline, so it counts as new.
function heldBackGroups(verdict: ReadVerdict, baseline: ReadVerdict): Set<string> {
  const failedBefore = failingGroupNames(baseline.requirements);
  const heldBack = new Set<string>();
  for (const group of failingGroups(verdict.requirements)) {
    if (!failedBefore.has(group.group)) continue;
    const before = failingCaseIds(baseline.cases, group.group);
    if ([...failingCaseIds(verdict.cases, group.group)].every((id) => before.has(id))) heldBack.add(group.group);
  }
  return heldBack;
}

// ---- the owner's notes ------------------------------------------------------------------------------------------

function notesFile(root: string, run: string): string {
  return path.join(root, run, NOTES_FILE);
}

function existingNotes(root: string, run: string): string[] {
  try {
    return fs.readFileSync(notesFile(root, run), "utf8").split("\n").filter((line) => line.trim() !== "");
  } catch {
    return [];
  }
}

// A line already in the file is not written again: the same UNKNOWN is one line however often the run is ingested.
function addNote(root: string, run: string, line: string, written: Set<string>): void {
  if (written.has(line)) return;
  const file = notesFile(root, run);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.appendFileSync(file, `${line}\n`);
  written.add(line);
}

function unknownLine(id: string, reason: string): string {
  // An UNKNOWN with no reason says so by having none; no text is invented for it.
  return reason === "" ? `- ${id} ${DOT} UNKNOWN` : `- ${id} ${DOT} UNKNOWN ${DOT} ${reason}`;
}

function blockedLine(reason: string): string {
  return `- evaluation ${DOT} could not run ${DOT} ${reason}`;
}

// V7: a group that failed before the change being judged. It is named with the group's ids, as the UNKNOWN lines are.
function baselineLine(group: string, ids: string): string {
  return `- ${group} ${DOT} FAIL in the baseline too ${DOT} ${ids}`;
}

// ---- which verdicts were ingested (V3) --------------------------------------------------------------------------

function ingestedFile(root: string): string {
  return path.join(root, GUARD_DIR, INGESTED_FILE);
}

// The hashes of the verdicts already ingested here. A bad line is skipped and never thrown, as in M2's journal.
function ingestedHashes(root: string): Set<string> {
  const hashes = new Set<string>();
  let file: string;
  try {
    file = fs.readFileSync(ingestedFile(root), "utf8");
  } catch {
    return hashes;
  }
  for (const line of file.split("\n")) {
    if (line.trim() === "") continue;
    try {
      const value: unknown = JSON.parse(line);
      if (isEntry(value) && typeof value.verdict === "string") hashes.add(value.verdict);
    } catch {
      continue;
    }
  }
  return hashes;
}

function markIngested(root: string, entry: Record<string, unknown>): void {
  const file = ingestedFile(root);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.appendFileSync(file, `${JSON.stringify(entry)}\n`);
}

// ---- counting ---------------------------------------------------------------------------------------------------

// The summary counts what the ingest did: `fails` is the failure records written, so one per failing group (V6), and a
// group held back by the baseline (V7) is in none of the three — it is a note in the owner's file, not a count.
function count(rows: VerdictRequirement[], heldBack: Set<string>): { fails: number; unknowns: number; passes: number } {
  let fails = 0;
  let unknowns = 0;
  let passes = 0;
  const counted = new Set<string>();
  for (const row of rows) {
    const verdict = text(row.verdict).toUpperCase();
    const group = text(row.group) || text(row.id);
    if (verdict === "FAIL") {
      if (heldBack.has(group) || counted.has(group)) continue;
      counted.add(group);
      fails += 1;
    } else if (verdict === "UNKNOWN") {
      unknowns += 1;
    } else {
      passes += 1;
    }
  }
  return { fails, unknowns, passes };
}

// ---- the ingest -------------------------------------------------------------------------------------------------

// V4: a missing file, JSON that does not parse or a verdict with no requirements is a note and nothing else.
function blocked(root: string, run: string, reason: string): IngestResult {
  addNote(root, run, blockedLine(reason), new Set(existingNotes(root, run)));
  return { fails: 0, unknowns: 0, passes: 0, problem: reason, already: false };
}

interface ReadVerdict {
  bytes: Uint8Array;
  requirements: VerdictRequirement[];
  cases: VerdictCase[];
}

// V4: a missing file, JSON that does not parse or a verdict with no requirements is a note and nothing else. The
// baseline is read by the same rules (V7), so a verdict and the baseline it is judged against are read alike.
function readVerdict(target: string, named: string): { ok: true; verdict: ReadVerdict } | { ok: false; problem: string } {
  let bytes: Uint8Array;
  try {
    bytes = fs.readFileSync(target);
  } catch {
    return { ok: false, problem: `no such verdict file: ${named}` };
  }

  let parsed: unknown;
  try {
    parsed = JSON.parse(new TextDecoder().decode(bytes));
  } catch {
    return { ok: false, problem: `${named} is not JSON` };
  }
  if (!isEntry(parsed) || !Array.isArray(parsed.requirements)) {
    return { ok: false, problem: `${named} has no requirements` };
  }
  const requirements = parsed.requirements as VerdictRequirement[];
  // An unnamed requirement cannot be a failure's input (M2 rejects an empty one), so the verdict is not usable.
  const unnamed = requirements.findIndex((row) => !isEntry(row) || text(row.id) === "");
  if (unnamed >= 0) return { ok: false, problem: `${named}: requirement ${unnamed + 1} has no id` };
  return {
    ok: true,
    verdict: { bytes, requirements, cases: Array.isArray(parsed.cases) ? (parsed.cases as VerdictCase[]) : [] },
  };
}

export function ingestVerdict(root: string, file: string, run: string, session: string, now: Date, baseline: string | null = null): IngestResult {
  // The notes are the owner's, in the run's own folder: nothing is written outside the root.
  const folder = path.resolve(root, run);
  const relative = path.relative(root, folder);
  if (relative === "" || relative.startsWith("..") || path.isAbsolute(relative)) {
    throw new EvaluationError(`evaluation ingest: --run must be inside the root: ${run}`);
  }
  const target = path.resolve(root, file);
  const named = path.relative(root, target) || target;

  const read = readVerdict(target, named);
  if (!read.ok) return blocked(root, relative, read.problem);
  const { bytes, requirements, cases } = read.verdict;

  // V7: with a baseline, the groups it already held as failing, case by case. A baseline that cannot be read is the same
  // note as a blocked verdict: without it, a group that failed before the change would be recorded as a new failure.
  let heldBack = new Set<string>();
  if (baseline !== null) {
    const baseTarget = path.resolve(root, baseline);
    const baseNamed = path.relative(root, baseTarget) || baseTarget;
    const baseRead = readVerdict(baseTarget, baseNamed);
    if (!baseRead.ok) return blocked(root, relative, baseRead.problem);
    heldBack = heldBackGroups({ bytes, requirements, cases }, baseRead.verdict);
  }

  const totals = count(requirements, heldBack);

  // V3: the same bytes are one verdict, so the second ingest records nothing.
  const hash = createHash("sha256").update(bytes).digest("hex");
  if (ingestedHashes(root).has(hash)) return { ...totals, fails: 0, unknowns: 0, problem: null, already: true };

  const written = new Set(existingNotes(root, relative));
  for (const row of requirements) {
    if (text(row.verdict).toUpperCase() === "UNKNOWN") addNote(root, relative, unknownLine(text(row.id), text(row.reason)), written);
  }
  // V6: one failure per failing group — a fault fails every id of its group, so one record names them all.
  for (const group of failingGroups(requirements)) {
    const ids = group.ids.join(", ");
    // V7: the group, and every one of its FAIL cases, failed before the change being judged: the owner's note, not new.
    if (heldBack.has(group.group)) {
      addNote(root, relative, baselineLine(group.group, ids), written);
      continue;
    }
    const reason = group.reason === "" ? "the evaluator judged it FAIL" : group.reason;
    const failureId = newFailureId();
    // The evidence is every FAIL case of the group with its repro — the command that shows the failure.
    const evidence = writeEvidence(root, failureId, {
      group: group.group,
      requirements: group.ids,
      reason,
      cases: casesOfGroup(cases, group.group)
        .filter((entry) => text(entry.verdict).toUpperCase() === "FAIL")
        .map((entry) => ({ case: text(entry.case), repro: text(entry.repro) })),
    });
    const record: FailureRecord = {
      kind: "failure", id: failureId, time: now.toISOString(), session, found_by: "evaluator",
      check: `evaluator:${group.group}`, input: ids, expected: "PASS", actual: "FAIL",
      engine: "none", harness: "none",
      reason,
      evidence,
    };
    appendFailure(root, record);
  }
  markIngested(root, { time: now.toISOString(), session, verdict: hash, file: named, run: relative, ...totals });
  return { ...totals, problem: null, already: false };
}