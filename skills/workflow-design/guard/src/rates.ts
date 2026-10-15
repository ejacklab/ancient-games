// Round 5, S2: success and failure counts per (check, engine), read from the journal. Only check ids, engine names
// and counts: a record's other fields never reach a row.

import { readJournal } from "./journal.ts";
import type { FailureRecord } from "./types.ts";

export interface RateRow {
  check: string;
  engine: string;
  ok: number;
  fail: number;
}

// A failure counts against the success line it would have been: an engine-call check (R12.1-…, trap:…) made by an
// engine, a failed test run, or else its own check id.
function failureCheck(record: FailureRecord): string {
  if ((record.check.startsWith("R12.1-") || record.check.startsWith("trap:")) && record.engine !== "none") return "engine-call";
  if (record.check === "R12.2-test-failed") return "test-run";
  return record.check;
}

export function rates(root: string, session: string | null): RateRow[] {
  const rows = new Map<string, RateRow>();
  const row = (check: string, engine: string): RateRow => {
    const key = JSON.stringify([check, engine]);
    let found = rows.get(key);
    if (found === undefined) {
      found = { check, engine, ok: 0, fail: 0 };
      rows.set(key, found);
    }
    return found;
  };
  for (const record of readJournal(root).records) {
    if (session !== null && record.session !== session) continue;
    if (record.kind === "success") row(String(record.check), String(record.engine)).ok += 1;
    else if (record.kind === "failure") row(failureCheck(record), String(record.engine)).fail += 1;
  }
  return [...rows.values()].sort((a, b) => a.check.localeCompare(b.check) || a.engine.localeCompare(b.engine));
}

// A table cell holds a check id or an engine name; a pipe or a line break would break the table.
function cell(value: string): string {
  return value.replace(/[|\r\n]/g, " ");
}

export function ratesMarkdown(rows: RateRow[]): string {
  const lines = ["| check | engine | ok | fail |", "|---|---|---|---|"];
  for (const r of rows) lines.push(`| ${cell(r.check)} | ${cell(r.engine)} | ${r.ok} | ${r.fail} |`);
  return lines.join("\n");
}
