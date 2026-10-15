// M2: failure journal (SPEC.md M2). Journal: <root>/.harness-guard/journal.jsonl, one JSON object per line.
// The journal holds lengths, counts, ids, rule ids and paths. Raw stdout, stderr, prompts and config values
// never reach a line or an evidence file: they are dropped on write.

import { execFileSync } from "node:child_process";
import { randomBytes } from "node:crypto";
import * as fs from "node:fs";
import * as path from "node:path";
import type { FailureRecord, GuardErrorRecord, JournalRecord, TouchedRecord } from "./types.ts";

const GUARD_DIR = ".harness-guard";
const ID_RE = /^F-[0-9a-f]{8}$/;
const ISO_RE = /^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:?\d{2})?$/;

// Facts and record fields that would carry raw content out of a command.
const RAW_KEYS = new Set([
  "argv", "args", "body", "command", "config", "content", "env", "input", "output", "prompt", "raw", "response", "secret", "stderr", "stdout", "token", "text",
]);

const REASON_FIELDS = ["check", "input", "expected", "actual", "engine", "harness", "found_by", "session", "reason"];

// ---- errors -----------------------------------------------------------------------------------------------------

export class JournalError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "JournalError";
  }
}

// ---- paths ------------------------------------------------------------------------------------------------------

export function guardRoot(cwd: string): string {
  try {
    const out = execFileSync("git", ["rev-parse", "--show-toplevel"], {
      cwd,
      timeout: 5000,
      encoding: "utf8",
      stdio: ["ignore", "pipe", "ignore"],
    }).trim();
    return out === "" ? cwd : out;
  } catch {
    return cwd;
  }
}

function journalFile(root: string): string {
  return path.join(root, GUARD_DIR, "journal.jsonl");
}

function isEntry(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

// ---- raw-content filter ------------------------------------------------------------------------------------------

const MAX_FACT_STRING = 200; // evidence holds lengths, counts, ids and paths: a longer string is raw content

function redactRawText(text: string): string {
  // A line that starts with a raw-content label carries the content itself: keep the label, drop the tail.
  return text
    .split("\n")
    .map((line) => (/^\s*(stdout|stderr|output|prompt|config|response|body|secret|token|raw)\s*:/i.test(line) ? line.replace(/(\s*:).*$/, "$1 [redacted]") : line))
    .join("\n");
}

function scrub(value: unknown, depth = 0, seen: Set<unknown> = new Set()): unknown {
  if (typeof value === "string") return value.length > MAX_FACT_STRING ? `[${value.length} chars]` : redactRawText(value);
  if (value === null || typeof value !== "object") return value;
  if (depth > 8 || seen.has(value)) return undefined;
  seen.add(value);
  if (Array.isArray(value)) return value.map((item) => scrub(item, depth + 1, seen)).filter((item) => item !== undefined);
  const out: Record<string, unknown> = {};
  for (const [key, item] of Object.entries(value as Record<string, unknown>)) {
    if (RAW_KEYS.has(key.toLowerCase())) continue;
    const scrubbed = scrub(item, depth + 1, seen);
    if (scrubbed !== undefined) out[key] = scrubbed;
  }
  return out;
}

// A record's own fields are kept as written; only fields that name raw content are replaced by their length.
function scrubRecord(rec: Record<string, unknown>): Record<string, unknown> {
  const out: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(rec)) {
    const lower = key.toLowerCase();
    if (RAW_KEYS.has(lower) && !REASON_FIELDS.includes(lower)) {
      out[key] = typeof value === "string" ? `[${value.length} chars]` : "[redacted]";
      continue;
    }
    out[key] = typeof value === "string" ? redactRawText(value) : scrub(value);
  }
  return out;
}

// ---- validation -------------------------------------------------------------------------------------------------

function evidenceExists(evidence: string, root: string): boolean {
  try {
    const file = path.isAbsolute(evidence) ? evidence : path.resolve(root, evidence);
    return fs.statSync(file).isFile();
  } catch {
    return false;
  }
}

function nonEmpty(value: unknown): boolean {
  return typeof value === "string" && value.trim() !== "";
}

export function validateFailure(rec: unknown, root: string): string[] {
  if (!isEntry(rec)) return ["record: not a JSON object"];
  const problems: string[] = [];
  if (rec.kind !== "failure") problems.push("kind: not \"failure\"");
  for (const field of ["session", "found_by", "check", "input", "expected", "actual", "engine", "harness", "reason", "evidence"] as const) {
    const value = rec[field];
    if (!(field in rec)) problems.push(`${field}: missing`);
    else if (typeof value !== "string") problems.push(`${field}: not a string`);
    else if (value.trim() === "") problems.push(`${field}: empty`);
  }
  if (!("id" in rec)) problems.push("id: missing");
  else if (typeof rec.id !== "string") problems.push("id: not a string");
  else if (!ID_RE.test(rec.id)) problems.push("id: not F- plus eight lowercase hex digits");
  if (!("time" in rec)) problems.push("time: missing");
  else if (typeof rec.time !== "string") problems.push("time: not a string");
  else if (!ISO_RE.test(rec.time) || Number.isNaN(Date.parse(rec.time))) problems.push("time: not ISO 8601");
  if (typeof rec.evidence === "string" && rec.evidence.trim() !== "" && !evidenceExists(rec.evidence, root)) {
    problems.push("evidence: path does not exist");
  }
  return problems;
}

// ---- writing ----------------------------------------------------------------------------------------------------

export function newFailureId(): string {
  return `F-${randomBytes(4).toString("hex")}`;
}

function appendLine(root: string, value: unknown): void {
  const file = journalFile(root);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.appendFileSync(file, `${JSON.stringify(value)}\n`);
}

export function appendFailure(root: string, rec: FailureRecord): FailureRecord {
  const problems = validateFailure(rec, root);
  if (problems.length > 0) throw new JournalError(`failure record rejected: ${problems.join("; ")}`);
  const line = scrubRecord(rec as unknown as Record<string, unknown>);
  appendLine(root, line);
  return rec;
}

export function appendRecord(root: string, rec: TouchedRecord | GuardErrorRecord): void {
  appendLine(root, scrubRecord(rec as unknown as Record<string, unknown>));
}

export function writeEvidence(root: string, id: string, facts: Record<string, unknown>): string {
  const relative = path.join(GUARD_DIR, "evidence", `${id}.json`);
  const file = path.join(root, relative);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(scrub(facts), null, 2)}\n`);
  return relative;
}

export function readJournal(root: string): { records: JournalRecord[]; badLines: number } {
  const records: JournalRecord[] = [];
  let badLines = 0;
  let text: string;
  try {
    text = fs.readFileSync(journalFile(root), "utf8");
  } catch {
    return { records, badLines };
  }
  for (const line of text.split("\n")) {
    if (line.trim() === "") continue;
    let value: unknown;
    try {
      value = JSON.parse(line);
    } catch {
      badLines += 1;
      continue;
    }
    if (!isEntry(value) || typeof value.kind !== "string") continue;
    records.push(value as unknown as JournalRecord);
  }
  return { records, badLines };
}

export function failuresFor(root: string, session: string | null): FailureRecord[] {
  return readJournal(root).records.filter(
    (record): record is FailureRecord => record.kind === "failure" && (session === null || record.session === session),
  );
}

// ---- CLI helper -------------------------------------------------------------------------------------------------

const FLAGS = ["--check", "--input", "--expected", "--actual", "--reason", "--evidence", "--found-by", "--engine", "--harness", "--session"];

// Missing --reason or --evidence is an error, never a default.
export function recordFailureFromArgs(root: string, args: string[]): FailureRecord {
  const given = new Map<string, string>();
  for (let i = 0; i < args.length; i++) {
    const flag = args[i]!;
    if (!FLAGS.includes(flag)) throw new JournalError(`fail: unknown argument (use ${FLAGS.join(" ")})`);
    const value = args[i + 1];
    if (value === undefined) throw new JournalError(`fail: ${flag} needs a value`);
    given.set(flag, value);
    i += 1;
  }
  for (const flag of ["--reason", "--evidence"] as const) {
    const value = given.get(flag);
    if (value === undefined || value.trim() === "") throw new JournalError(`fail: ${flag} is required and cannot be empty`);
  }
  const rec: FailureRecord = {
    kind: "failure",
    id: newFailureId(),
    time: new Date().toISOString(),
    session: given.get("--session") ?? "none",
    found_by: given.get("--found-by") ?? "cli",
    check: given.get("--check") ?? "R12.2-manual",
    input: given.get("--input") ?? "none",
    expected: given.get("--expected") ?? "none",
    actual: given.get("--actual") ?? "none",
    engine: given.get("--engine") ?? "none",
    harness: given.get("--harness") ?? "none",
    reason: given.get("--reason")!,
    evidence: given.get("--evidence")!,
  };
  return appendFailure(root, rec);
}