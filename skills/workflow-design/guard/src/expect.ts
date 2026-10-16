// Round 12 (SPEC.md, E1–E4): a planned red run. The agent declares, before a test run, that the next run naming a test
// file must fail — the red step of writing a test before the change. A run it covers that fails is recorded as red, not
// as a failure; one that passes is the failure. Without a declaration every failing run is a failure (D1).

import { randomBytes } from "node:crypto";
import * as fs from "node:fs";
import * as path from "node:path";
import { appendRecord, readJournal } from "./journal.ts";
import type { ExpectFailRecord } from "./types.ts";

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
