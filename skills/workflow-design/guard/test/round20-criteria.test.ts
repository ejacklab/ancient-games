// Acceptance checks written from SPEC.md Round 20 (CR1), independently of the implementation: at a Stop inside an
// open, not-up deadline of the session, the criteria step waits; once the deadline is ended or up, or with no deadline,
// it runs as before (round 6, K2).
import { afterEach, beforeEach, expect, test } from "bun:test";
import { execFileSync } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { endDeadline } from "../src/deadline.ts";
import { handleHook } from "../src/hooks.ts";
import { readJournal } from "../src/journal.ts";
import type { CriteriaFile, Criterion, Deadline, FailureRecord, HookEnv, HookResult } from "../src/types.ts";

const session = "round20-session";
const file = "runs/task/criteria.yaml";
const EPOCH = Date.parse("2026-10-18T02:00:00.000Z");
let root: string;
let env: HookEnv;
let tick: number;

beforeEach(() => {
  root = fs.mkdtempSync(path.join(os.tmpdir(), "hg-round20-"));
  execFileSync("git", ["init", "--quiet"], { cwd: root });
  tick = EPOCH;
  env = { cwd: root, running: [], now: () => new Date(tick) };
});
afterEach(() => fs.rmSync(root, { recursive: true, force: true }));

const at = (minutes: number) => { tick = EPOCH + minutes * 60_000; };

function write(relative: string, text: string): void {
  const target = path.join(root, relative);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, text);
}

function invoke(payload: Record<string, unknown>, selectedSession = session): HookResult {
  const result = handleHook({ session_id: selectedSession, cwd: root, ...payload }, env);
  expect(result.exitCode).toBe(0);
  expect(result.stderr).toBe("");
  return result;
}

function plant(overrides: Partial<Deadline> = {}): Deadline {
  const deadline: Deadline = { id: "D-0000c0de", start: new Date(EPOCH).toISOString(), minutes: 10, run: "runs/task", session, ...overrides };
  write(`.harness-guard/deadlines/${deadline.id}.json`, JSON.stringify(deadline));
  return deadline;
}

// C1 unmarked (blocks today), C2 marked not met (a criterion failure today).
const ITEMS: Criterion[] = [{ id: "C1", text: "the first thing" }, { id: "C2", text: "the second thing", met: false, evidence: "observed a mismatch" }];

function criteria(items: Criterion[] = ITEMS): void {
  const value: CriteriaFile = { criteria: 1, session, request: "the request", items };
  write(file, JSON.stringify(value));
  invoke({ hook_event_name: "PostToolUse", tool_name: "Write",
    tool_input: { file_path: path.join(root, file), content: "x" }, tool_response: {} });
}

function stop(selectedSession = session): HookResult {
  return invoke({ hook_event_name: "Stop", last_assistant_message: "done", stop_hook_active: false }, selectedSession);
}

function criterionFailures(): FailureRecord[] {
  return readJournal(root).records.filter((r): r is FailureRecord => r.kind === "failure" && r.check.startsWith("criterion:"));
}

function decision(result: HookResult): string | undefined {
  return result.stdout.trim() === "" ? undefined : JSON.parse(result.stdout).decision;
}

// Today's stop on this file: blocked once for the unmarked C1, and a failure for C2.
function expectBlockedAsToday(result: HookResult): void {
  expect(decision(result)).toBe("block");
  expect(JSON.parse(result.stdout).reason).toContain("mark each criterion met: true|false with evidence");
  expect(JSON.parse(result.stdout).reason).toContain("C1");
  expect(criterionFailures().map((r) => r.check)).toEqual(["criterion:C2"]);
}

const deferred = (id: string, left: number) => `harness-guard: criteria are scored when deadline ${id} ends or is up (${left} min left)`;

// CR1 as amended (run 20261018-finish-everything, 03:12): a context line at Stop makes Claude Code continue the turn,
// so every stop of a waiting agent woke it again; the deferred stop is quiet.
test("CR1: a Stop inside an open, not-up deadline is not blocked by unmarked criteria, writes no criteria failure, and prints nothing", () => {
  const deadline = plant();
  criteria();
  at(2);
  const result = stop();
  expect(decision(result)).not.toBe("block");
  expect(result.stdout, deferred(deadline.id, 8)).toBe("");
  expect(criterionFailures()).toEqual([]);
  // Every stop while the deadline runs: still not blocked, still no failure.
  at(7);
  const again = stop();
  expect(decision(again)).not.toBe("block");
  expect(again.stdout, deferred(deadline.id, 3)).toBe("");
  expect(criterionFailures()).toEqual([]);
});

test("CR1: after the deadline is ended, the same stop is blocked as today", () => {
  const deadline = plant();
  criteria();
  at(2);
  expect(decision(stop())).not.toBe("block");
  endDeadline(root, session, new Date(tick));
  at(3);
  const result = stop();
  expectBlockedAsToday(result);
  expect(result.stdout).not.toContain(`deadline ${deadline.id} ends or is up`);
});

test("CR1: when the deadline is up, the same stop is blocked as today", () => {
  plant();
  criteria();
  at(2);
  expect(decision(stop())).not.toBe("block");
  at(11);
  expectBlockedAsToday(stop());
});

test("CR1: a session with no deadline is blocked as today", () => {
  criteria();
  at(2);
  expectBlockedAsToday(stop());
});

test("CR1: another session's open deadline does not hold this session's criteria step", () => {
  plant({ id: "D-0000beef", session: "other" });
  criteria();
  at(2);
  const result = stop();
  expectBlockedAsToday(result);
  expect(result.stdout).not.toContain("D-0000beef");
});
