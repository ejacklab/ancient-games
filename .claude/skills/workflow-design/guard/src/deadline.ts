// Round 10 (SPEC.md): the agent cannot feel time pass, so the guard keeps the owner's time limit and tells it — a
// status it can run (way 1), a wait a harness can run in the background as a timer (way 2), and reminders the hooks
// add after tool calls (way 3). Workers' progress files are read for one line each: piece, state, age — never notes.

import { randomBytes } from "node:crypto";
import * as fs from "node:fs";
import * as path from "node:path";
const GUARD_DIR = ".harness-guard";
import type { Deadline, ProgressSummary } from "./types.ts";

export class DeadlineError extends Error {}

export const DEFAULT_MARKS = [50, 80, 100];

function folder(root: string): string {
  return path.join(root, GUARD_DIR, "deadlines");
}

function fileOf(root: string, id: string): string {
  return path.join(folder(root), `${id}.json`);
}

export function parseMarks(text: string | null): number[] {
  if (text === null) return [...DEFAULT_MARKS];
  const marks = text.split(",").map((part) => Number(part.trim()));
  if (marks.length === 0 || marks.some((mark) => !Number.isInteger(mark) || mark < 1 || mark > 100)) {
    throw new DeadlineError("--marks: integers from 1 to 100, comma-separated");
  }
  return [...new Set([...marks, 100])].sort((a, b) => a - b);
}

export function startDeadline(root: string, opts: { minutes: number; run?: string | null; marks?: number[] }, now: Date): Deadline {
  if (!Number.isFinite(opts.minutes) || opts.minutes <= 0) throw new DeadlineError("--minutes: a positive number");
  // A duration whose end is not a representable time would never expire (review finding 6).
  if (!Number.isFinite(new Date(now.getTime() + opts.minutes * 60_000).getTime())) throw new DeadlineError("--minutes: too large to be a time");
  const marks = opts.marks === undefined ? [...DEFAULT_MARKS] : [...new Set([...opts.marks, 100])].sort((a, b) => a - b);
  if (marks.some((mark) => !Number.isInteger(mark) || mark < 1 || mark > 100)) throw new DeadlineError("marks: integers from 1 to 100");
  const run = opts.run === undefined || opts.run === null || opts.run === "" ? null : path.relative(root, path.resolve(root, opts.run));
  const deadline: Deadline = { id: `D-${randomBytes(4).toString("hex")}`, start: now.toISOString(), minutes: opts.minutes, run, marks, session: null };
  fs.mkdirSync(folder(root), { recursive: true });
  fs.writeFileSync(fileOf(root, deadline.id), `${JSON.stringify(deadline, null, 2)}\n`);
  return deadline;
}

const ID = /^D-[0-9a-f]{8}$/;

function isDeadline(value: unknown): value is Deadline {
  if (typeof value !== "object" || value === null) return false;
  const d = value as Record<string, unknown>;
  return typeof d.id === "string" && ID.test(d.id) && typeof d.start === "string" && Number.isFinite(Date.parse(d.start))
    && typeof d.minutes === "number" && d.minutes > 0
    && Number.isFinite(new Date(Date.parse(d.start) + d.minutes * 60_000).getTime())
    && Array.isArray(d.marks) && d.marks.every((m) => Number.isInteger(m) && (m as number) >= 1 && (m as number) <= 100)
    && (d.session === null || typeof d.session === "string") && (d.run === null || typeof d.run === "string");
}

export function readDeadlines(root: string): Deadline[] {
  let names: string[];
  try {
    names = fs.readdirSync(folder(root)).filter((name) => name.endsWith(".json"));
  } catch {
    return [];
  }
  const found: Deadline[] = [];
  for (const name of names) {
    try {
      const parsed: unknown = JSON.parse(fs.readFileSync(path.join(folder(root), name), "utf8"));
      // The id names the file it came from, so a claim can only write that file (review finding 5).
      if (isDeadline(parsed) && name === `${parsed.id}.json`) found.push(parsed);
    } catch {
      // an unreadable deadline file is no deadline
    }
  }
  return found;
}

// The call that ran `deadline start` claims every unclaimed deadline for its session (T1).
export function claimDeadlines(root: string, session: string): number {
  let claimed = 0;
  for (const deadline of readDeadlines(root)) {
    if (deadline.session !== null) continue;
    fs.writeFileSync(fileOf(root, deadline.id), `${JSON.stringify({ ...deadline, session }, null, 2)}\n`);
    claimed++;
  }
  return claimed;
}

const endOf = (d: Deadline): number => Date.parse(d.start) + d.minutes * 60_000;

// The session's deadline: the newest one still running, else the latest one.
export function sessionDeadline(root: string, session: string | null, now: Date): Deadline | null {
  const own = readDeadlines(root).filter((d) => session === null || d.session === session);
  if (own.length === 0) return null;
  const byStart = own.sort((a, b) => Date.parse(b.start) - Date.parse(a.start));
  return byStart.find((d) => endOf(d) > now.getTime()) ?? byStart[0]!;
}

const LINE = /^- (\S+) · (\S+) · (planned|start|done|fail) · ?(.*)$/;

export function progressSummary(file: string, now: Date): ProgressSummary {
  const node = path.basename(file).replace(/\.progress\.md$/, "");
  let text = "";
  try {
    text = fs.readFileSync(file, "utf8");
  } catch {
    return { node, done: 0, total: 0, last: null, ageMinutes: null, badLines: 0 };
  }
  const pieces = new Map<string, string>();
  let last: ProgressSummary["last"] = null;
  let badLines = 0;
  for (const raw of text.split("\n")) {
    const line = raw.trim();
    if (line === "") continue;
    const match = LINE.exec(line);
    if (match === null || !Number.isFinite(Date.parse(match[1]!))) {
      badLines++;
      continue;
    }
    pieces.set(match[2]!, match[3]!);
    last = { time: match[1]!, piece: match[2]!, state: match[3]! };
  }
  const done = [...pieces.values()].filter((state) => state === "done").length;
  const ageMinutes = last === null ? null : Math.max(0, Math.round((now.getTime() - Date.parse(last.time)) / 60_000));
  return { node, done, total: pieces.size, last, ageMinutes, badLines };
}

export function progressFiles(root: string, run: string | null): string[] {
  if (run === null) return [];
  const dir = path.join(root, run, "nodes");
  try {
    return fs.readdirSync(dir).filter((name) => name.endsWith(".progress.md")).sort().map((name) => path.join(dir, name));
  } catch {
    return [];
  }
}

export function workerLine(s: ProgressSummary): string {
  const last = s.last === null ? "no line yet" : `last ${s.last.piece} ${s.last.state} ${s.ageMinutes} min ago`;
  return `${s.node}: ${s.done}/${s.total} pieces, ${last}`;
}

const clock = (ms: number): string => {
  const d = new Date(ms);
  return `${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`;
};

export interface DeadlineStatus {
  deadline: Deadline;
  usedMinutes: number;
  leftMinutes: number;
  percent: number;
  up: boolean;
  line: string;
  workers: string[];
}

export function deadlineStatus(root: string, session: string | null, now: Date, withWorkers = true): DeadlineStatus | null {
  const deadline = sessionDeadline(root, session, now);
  if (deadline === null) return null;
  const usedMs = now.getTime() - Date.parse(deadline.start);
  const usedMinutes = Math.max(0, Math.round(usedMs / 60_000));
  const percent = Math.max(0, Math.floor((usedMs / (deadline.minutes * 60_000)) * 100));
  const up = now.getTime() >= endOf(deadline);
  const leftMinutes = Math.max(0, Math.ceil((endOf(deadline) - now.getTime()) / 60_000));
  const line = up
    ? `time is up, ${Math.round((now.getTime() - endOf(deadline)) / 60_000)} min over (deadline ${clock(endOf(deadline))})`
    : `used ${usedMinutes} of ${deadline.minutes} min (${percent}%), ${leftMinutes} left, deadline ${clock(endOf(deadline))}`;
  // The workers' files are read only where they are shown — a mark block or status, not the every-call clock.
  const workers = withWorkers ? progressFiles(root, deadline.run).map((file) => workerLine(progressSummary(file, now))) : [];
  return { deadline, usedMinutes, leftMinutes, percent, up, line, workers };
}

// The highest mark passed and not yet announced (T5); null when none is due.
export function dueMark(status: DeadlineStatus, announced: Set<string>): number | null {
  const passed = status.deadline.marks.filter((mark) => status.percent >= mark || (mark === 100 && status.up));
  const fresh = passed.filter((mark) => !announced.has(markId(status.deadline, mark)));
  return fresh.length === 0 ? null : fresh[fresh.length - 1]!;
}

export function markId(deadline: Deadline, mark: number): string {
  return `deadline:${deadline.id}:${mark}`;
}

export function deadlineEnd(deadline: Deadline): number {
  return endOf(deadline);
}
