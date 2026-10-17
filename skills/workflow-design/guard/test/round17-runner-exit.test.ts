// Acceptance expectations come from SPEC.md, Round 17 (a test failure only when the runner made the exit).
import { afterEach, beforeEach, expect, test } from "bun:test";
import { execFileSync } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { handleHook } from "../src/hooks.ts";
import { readJournal } from "../src/journal.ts";
import type { FailureRecord, HookEnv, WarningRecord } from "../src/types.ts";

const time = "2026-10-17T10:30:00.000Z";
const session = "round17-session";
let folder: string;
let env: HookEnv;

beforeEach(() => {
  folder = fs.mkdtempSync(path.join(os.tmpdir(), "hg-"));
  execFileSync("git", ["init", "--quiet"], { cwd: folder });
  env = { cwd: folder, running: [], now: () => new Date(time) };
});

afterEach(() => {
  fs.rmSync(folder, { recursive: true, force: true });
});

function bashFailure(command: string, output: string, exit: number): void {
  handleHook({
    hook_event_name: "PostToolUseFailure", session_id: session, cwd: folder,
    tool_name: "Bash", tool_input: { command },
    error: `Exit code ${exit}\n${output}`, is_interrupt: false,
  }, env);
}

function failures(): FailureRecord[] {
  return readJournal(folder).records.filter((record): record is FailureRecord => record.kind === "failure");
}

function warnings(): WarningRecord[] {
  return readJournal(folder).records.filter((record): record is WarningRecord => record.kind === "warning");
}

// T1: F-bdea5631's shape — the base tests, then an `ls` that exits 2 because the worktree is gone, as planned.
test("T1: a trailing ls's exit is a command-error warning naming ls, not a failed test run", () => {
  bashFailure("cd /tmp/base && bun test test/a.test.ts; ls /tmp/base",
    " 7 pass\n 10 fail\nls: cannot access '/tmp/base': No such file or directory", 2);
  expect(failures()).toEqual([]);
  expect(warnings()).toHaveLength(1);
  expect(warnings()[0]).toMatchObject({ check: "R12.2-command-error", input: "ls call", actual: "exit 2" });
});

// T2: after `&&` the exit may be the runner's or the later command's; the guard cannot tell, so it is a guess.
test("T2: a runner followed by && with no summary is a warning, not a failure", () => {
  bashFailure("pytest -q && echo done", "collection error", 1);
  expect(failures()).toEqual([]);
  expect(warnings()).toHaveLength(1);
  expect(warnings()[0]).toMatchObject({ check: "R12.2-command-error", input: "echo call", actual: "exit 1" });
});

// T3: the runner's own summary shows failures, so the run failed wherever it stands in the chain.
test("T3: a runner that is not last but whose summary shows failures is a failed test run", () => {
  bashFailure("pytest -q; ls /gone", "3 failed, 4 passed\nls: cannot access '/gone'", 2);
  expect(failures()).toHaveLength(1);
  expect(failures()[0]).toMatchObject({ check: "R12.2-test-failed", input: "pytest run", actual: "3 failed" });
  expect(warnings()).toEqual([]);
});

// T4: the runner is last, or last but for its own pipeline: its exit is the call's.
test.each([["cd work && pytest -q"], ["pytest -q 2>&1 | tail -3"], ["pytest -q a.py && pytest -q b.py"]])(
  "T4: %s exiting 1 is a failed test run", (command: string) => {
    bashFailure(command, "runner could not start", 1);
    expect(failures()).toHaveLength(1);
    expect(failures()[0]).toMatchObject({ check: "R12.2-test-failed", input: "pytest run", actual: "exit 1" });
    expect(warnings()).toEqual([]);
  },
);
