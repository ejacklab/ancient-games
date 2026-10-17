// Acceptance checks for the guard's clock as SPEC.md Round 10, T5 "Clock" and the notes after it describe it, written
// from that text: with a deadline recorded for the session, every PostToolUse or PostToolUseFailure call the hooks see
// adds exactly one line `harness-guard clock: <used>/<minutes> min (<percent>%), <left> left`; there is no fuller block
// and no reminder at 50%, 80% or 100%, and no `raised` record for a mark; after the deadline every call adds the
// time-up line instead. The clock is injected (`env.now`), never slept for.
import { afterEach, expect, test } from "bun:test";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { handleHook } from "../src/hooks.ts";
import { startDeadline, claimDeadlines } from "../src/deadline.ts";
import { readJournal } from "../src/journal.ts";
import type { HookResult } from "../src/types.ts";

const EPOCH = Date.parse("2026-10-16T02:00:00.000Z");
const MINUTES = 10;
const CLOCK = /^harness-guard clock: (\d+)\/(\d+) min \((\d+)%\), (\d+) left$/;
const TIME_UP = /^harness-guard time is up \((\d+) min over\): stop trying, finish the report, and put what is open to the owner\.$/;
const EVENTS = ["PostToolUse", "PostToolUseFailure"] as const;

// A reminder at a mark would have to say it in words; the clock's own percent is not one of them.
const MARK_WORDS = /mark|reminder|halfway|budget|threshold/i;
const roots: string[] = [];
afterEach(() => {
  for (const root of roots.splice(0)) fs.rmSync(root, { recursive: true, force: true });
});

function box() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "hg-clock-"));
  roots.push(root);
  execFileSync("git", ["init", "-q"], { cwd: root });
  let tick = EPOCH;
  const env = { cwd: root, running: [], now: () => new Date(tick) };
  const at = (minutes: number) => { tick = EPOCH + minutes * 60_000; };
  const post = (event: string = "PostToolUse", session = "s", payload: Record<string, unknown> = {}) => handleHook({
    session_id: session, cwd: root, hook_event_name: event, tool_name: "Bash",
    tool_input: { command: "true" }, tool_response: { stdout: "", stderr: "", interrupted: false },
    ...(event === "PostToolUseFailure" ? { tool_input: { command: "exit 1" }, exit_code: 1, error: "exit 1" } : {}),
    ...payload,
  }, env);
  // A deadline recorded for this session: started at the injected time, then claimed for `session`.
  const deadline = (session = "s", minutes = MINUTES) => {
    const started = startDeadline(root, { minutes }, env.now());
    if (session !== null) claimDeadlines(root, session);
    return started;
  };
  const raised = () => readJournal(root).records.filter((record) => record.kind === "raised")
    .flatMap((record) => record.ids);
  return { root, env, at, post, deadline, raised };
}

type Box = ReturnType<typeof box>;
function context(result: HookResult): string {
  expect(result.exitCode).toBe(0);
  return result.stdout === "" ? "" : JSON.parse(result.stdout).hookSpecificOutput?.additionalContext ?? "";
}
function lines(b: Box, event: string, session = "s"): string[] {
  const text = context(b.post(event, session));
  return text === "" ? [] : text.split("\n");
}
function clockLines(all: string[]): string[] {
  return all.filter((line) => line.startsWith("harness-guard clock:"));
}
// The points the SPEC names: 50%, 80% and 100% carry no reminder, so they are checked like every other point.
const POINTS: [number, number][] = [[1, 10], [4.9, 49], [5, 50], [5.1, 51], [8, 80], [9.9, 99]];
// A call of this event that is not this guard's business (a non-zero exit warns) may carry other context; the clock is
// then one line among them, and adds to them rather than replacing them (T5).
const timeLines = (all: string[]) => all.filter((line) => TIME_UP.test(line));

for (const event of EVENTS) {
  test.each(POINTS.map((point) => [event, ...point]))(
    "T5: %s at %p min, percent %p of the deadline, adds one clock line and no mark",
    (event: string, minutes: number, percent: number) => {
      const b = box();
      b.deadline();
      b.at(minutes);
      const all = lines(b, event);
      const clocks = clockLines(all);
      expect(clocks).toHaveLength(1);
      if (event === "PostToolUse") {
        // A call whose only business is the clock gets one line, and nothing else.
        expect(all).toHaveLength(1);
      } else {
        expect(all.length).toBeGreaterThanOrEqual(1);
      }
      const match = CLOCK.exec(clocks[0]!);
      expect(match).not.toBeNull();
      expect(match![1]).toMatch(/^\d+$/);
      expect(match![2]).toBe(String(MINUTES));
      expect(match![3]).toBe(String(percent));
      expect(Number(match![4])).toBeGreaterThanOrEqual(0);
      // Whatever else the call produced, no mark reminder is among it and none follows.
      for (const line of all) expect(line).not.toMatch(MARK_WORDS);
      for (const line of lines(b, event)) expect(line).not.toMatch(MARK_WORDS);
    },
  );

  test(`T5: ${event} after the deadline adds the time-up line on two calls in a row`, () => {
    const b = box();
    b.deadline();
    b.at(MINUTES + 1);
    const first = timeLines(lines(b, event));
    const second = timeLines(lines(b, event));
    expect(first).toHaveLength(1);
    expect(clockLines(lines(b, event))).toEqual([]);
    expect(second).toEqual(first);
    expect(first[0]).toContain("stop trying, finish the report, and put what is open to the owner.");
  });
}

test("T5: no raised record for a mark is ever written, at any point of the deadline", () => {
  const b = box();
  const deadline = b.deadline();
  for (const [minutes] of POINTS) {
    b.at(minutes);
    for (const event of EVENTS) lines(b, event);
  }
  b.at(MINUTES + 1);
  lines(b, "PostToolUse");
  const ids = b.raised();
  expect(ids.filter((id) => id === `deadline:${deadline.id}:50` || id === `deadline:${deadline.id}:80`
    || id === `deadline:${deadline.id}:100`)).toEqual([]);
  // No mark record at all: the only deadline id the journal may hold is the once-per-session ask, not a mark.
  expect(ids.filter((id) => id.startsWith("deadline:") && id !== "deadline-ask")).toEqual([]);
});

test("T5: 100% of the deadline carries no reminder for the mark", () => {
  const b = box();
  b.deadline();
  b.at(MINUTES);
  const all = lines(b, "PostToolUse");
  expect(clockLines(all).length + all.filter((line) => TIME_UP.test(line)).length).toBe(1);
  for (const line of all) {
    expect(line).not.toMatch(MARK_WORDS);
    expect(line).not.toContain("100%");
  }
});

test("T5: another session's deadline adds nothing to this session's calls", () => {
  const b = box();
  b.deadline("other");
  b.at(MINUTES + 1);
  expect(context(b.post("PostToolUse", "s"))).toBe("");
  expect(clockLines(lines(b, "PostToolUseFailure", "s"))).toEqual([]);
  expect(timeLines(lines(b, "PostToolUseFailure", "s"))).toEqual([]);
  // The other session's own clock is the one it sees.
  expect(timeLines(lines(b, "PostToolUse", "other"))).toHaveLength(1);
  expect(clockLines(lines(b, "PostToolUse", "s"))).toEqual([]);
  expect(context(b.post("PostToolUse", "s"))).toBe("");
});