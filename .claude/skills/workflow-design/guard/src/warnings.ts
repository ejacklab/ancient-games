// Round 9 (SPEC.md): the guard fails only where a meaning is written down; where it can only guess, it warns. A warning
// is settled by the agent — logged as a failure with its reason, or dismissed with a one-line reason — and every
// dismissal stays in the journal for the project owner to read and overrule.

import { randomBytes } from "node:crypto";
import { appendFailure, appendRecord, readJournal } from "./journal.ts";
import type { DismissedRecord, FailureRecord, WarningRecord } from "./types.ts";

export class WarningError extends Error {}

export function newWarningId(): string {
  return `W-${randomBytes(4).toString("hex")}`;
}

export function appendWarning(root: string, rec: WarningRecord): WarningRecord {
  appendRecord(root, rec);
  return rec;
}

export type WarningState =
  | { state: "open" }
  | { state: "failure"; failure: string }
  | { state: "dismissed"; reason: string };

export interface WarningRow {
  warning: WarningRecord;
  settled: WarningState;
}

// Every warning in the root (of one session, or all), with how it was settled. The first settlement counts.
export function warnings(root: string, session: string | null): WarningRow[] {
  const records = readJournal(root).records;
  const settled = new Map<string, WarningState>();
  for (const record of records) {
    if (record.kind === "failure" && typeof record.from === "string" && !settled.has(record.from)) {
      settled.set(record.from, { state: "failure", failure: record.id });
    }
    if (record.kind === "dismissed" && !settled.has(record.id)) {
      settled.set(record.id, { state: "dismissed", reason: record.reason });
    }
  }
  return records
    .filter((record): record is WarningRecord => record.kind === "warning" && (session === null || record.session === session))
    .map((warning) => ({ warning, settled: settled.get(warning.id) ?? { state: "open" } }));
}

export function openWarnings(root: string, session: string | null): WarningRecord[] {
  return warnings(root, session).filter((row) => row.settled.state === "open").map((row) => row.warning);
}

function find(root: string, id: string): WarningRow {
  const row = warnings(root, null).find((candidate) => candidate.warning.id === id);
  if (row === undefined) throw new WarningError(`no warning ${id} in this root`);
  if (row.settled.state !== "open") throw new WarningError(`warning ${id} is already settled (${row.settled.state})`);
  return row;
}

function oneLine(reason: string): string {
  const line = reason.trim();
  if (line === "") throw new WarningError("--reason is required: one line saying why");
  if (/[\r\n]/.test(line)) throw new WarningError("--reason is one line");
  return line;
}

// The agent judged it a failure: one failure record with the warning's facts, the agent's reason, and `from`.
export function settleAsFailure(root: string, id: string, reason: string, now: Date, newId: () => string): FailureRecord {
  const { warning } = find(root, id);
  return appendFailure(root, {
    kind: "failure",
    id: newId(),
    time: now.toISOString(),
    session: warning.session,
    found_by: "agent",
    check: warning.check,
    input: warning.input,
    expected: warning.expected,
    actual: warning.actual,
    engine: warning.engine,
    harness: warning.harness,
    reason: oneLine(reason),
    evidence: warning.evidence,
    from: warning.id,
  });
}

// The agent judged it not a failure: the reason is kept, so the project owner can read it and overrule it.
export function dismiss(root: string, id: string, reason: string, now: Date): DismissedRecord {
  const { warning } = find(root, id);
  const record: DismissedRecord = { kind: "dismissed", time: now.toISOString(), session: warning.session, id, reason: oneLine(reason) };
  appendRecord(root, record);
  return record;
}
