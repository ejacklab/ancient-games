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

// T4: the runner is last: its exit is the call's.
test.each([["cd work && pytest -q"], ["pytest -q a.py && pytest -q b.py"]])(
  "T4: %s exiting 1 is a failed test run", (command: string) => {
    bashFailure(command, "runner could not start", 1);
    expect(failures()).toHaveLength(1);
    expect(failures()[0]).toMatchObject({ check: "R12.2-test-failed", input: "pytest run", actual: "exit 1" });
    expect(warnings()).toEqual([]);
  },
);

// T5 (crossed review, finding 1): a guard query after the runner does not excuse the exit — after `&&` the query may
// never have run, so the exit may be the runner's.
test("T5: a runner followed by a guard query that exit 1 is a warning, not nothing", () => {
  bashFailure("pytest -q && bun /guard/src/cli.ts insight", "collection error", 1);
  expect(failures()).toEqual([]);
  expect(warnings()).toHaveLength(1);
  expect(warnings()[0]).toMatchObject({ check: "R12.2-command-error", input: "bun call", actual: "exit 1" });
});

// T6 (finding 2): a pipeline's exit is its last command's — `grep` finding nothing is not a failed test run.
test.each([["pytest -q | grep missing", "grep"], ["pytest -q 2>&1 | tail -3", "tail"]])(
  "T6: %s exiting 1 with no summary is a warning naming the last command", (command: string, word: string) => {
    bashFailure(command, "", 1);
    expect(failures()).toEqual([]);
    expect(warnings()).toHaveLength(1);
    expect(warnings()[0]).toMatchObject({ check: "R12.2-command-error", input: `${word} call`, actual: "exit 1" });
  },
);

// T7 (finding 4): a group at the end of a pipe is still piped, so the runner's summary in stdout counts.
test("T7: pytest -q | (cat) with a failure summary in stdout is a failed test run", () => {
  handleHook({
    hook_event_name: "PostToolUse", session_id: session, cwd: folder, tool_name: "Bash",
    tool_input: { command: "pytest -q | (cat)" }, tool_response: { stdout: "3 failed, 2 passed", stderr: "", interrupted: false },
  }, env);
  expect(failures()).toHaveLength(1);
  expect(failures()[0]).toMatchObject({ check: "R12.2-test-failed", input: "pytest run", actual: "3 failed" });
});

// T8 (finding 5): the record names the runner that made the exit, the last one.
test("T8: bun test a; pytest b exiting 2 with no summary names the pytest run", () => {
  bashFailure("bun test a.test.ts; pytest b.py", "no tests ran", 2);
  expect(failures()).toHaveLength(1);
  expect(failures()[0]).toMatchObject({ check: "R12.2-test-failed", input: "pytest run", actual: "exit 2" });
});
