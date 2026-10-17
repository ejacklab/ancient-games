// Acceptance expectations come from SPEC.md Round 17 — V1 ("the runner's exit"), V2 ("otherwise a guess") and every
// Fails-if of that round — read together with Round 4 (what R12.2-test-failed and R12.2-command-error hold) and
// Round 9 (a guess is a warning record, not a failure).
import { afterEach, beforeEach, describe, expect, test } from "bun:test";
import { execFileSync } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { handleHook } from "../src/hooks.ts";
import { readJournal } from "../src/journal.ts";
import type { FailureRecord, HookEnv, HookResult, WarningRecord } from "../src/types.ts";

const time = "2026-10-17T10:00:00.000Z";
const session = "round17-crossed-session";
// Planted text that appears in the output of the failed calls; no record, evidence file or context line may hold it.
const planted = "PRIVATE-OUTPUT-4b91ce";
let folder: string;
let env: HookEnv;

beforeEach(() => {
  folder = fs.mkdtempSync(path.join(os.tmpdir(), "hg17-"));
  execFileSync("git", ["init", "--quiet"], { cwd: folder });
  fs.mkdirSync(path.join(folder, "work"));
  env = { cwd: folder, running: [], now: () => new Date(time) };
});

afterEach(() => {
  fs.rmSync(folder, { recursive: true, force: true });
});

// Round 4, D1/D2 facts: a failed Bash call arrives as PostToolUseFailure with `error` = "Exit code N\n<output>".
function failedCall(command: string, output = `diagnostic ${planted}`, exit = 1): Record<string, unknown> {
  return {
    hook_event_name: "PostToolUseFailure", session_id: session, cwd: folder,
    tool_name: "Bash", tool_input: { command },
    error: `Exit code ${exit}\n${output}`, is_interrupt: false,
  };
}

// A call the harness classes as no error: its output is in the response's stdout and stderr.
function succeededCall(command: string, stdout = "", stderr = ""): Record<string, unknown> {
  return {
    hook_event_name: "PostToolUse", session_id: session, cwd: folder,
    tool_name: "Bash", tool_input: { command },
    tool_response: { stdout, stderr, interrupted: false },
  };
}

// Confidentiality before any behavioural assertion can fail.
function invokeHook(payload: Record<string, unknown>): HookResult {
  const result = handleHook(payload, env);
  const state = path.join(folder, ".harness-guard");
  const written = fs.existsSync(state)
    ? fs.readdirSync(state, { recursive: true, encoding: "utf8" })
        .filter((name) => fs.statSync(path.join(state, name)).isFile())
        .map((name) => fs.readFileSync(path.join(state, name), "utf8"))
        .join("")
    : "";
  expect(JSON.stringify(result) + written).not.toContain(planted);
  return result;
}

type Judged = FailureRecord | WarningRecord;

// One verdict and one only: neither a second failure nor a warning, nor any other record kind that would show the
// handler answered the same call twice.
function onlyVerdict(kind: "failure" | "warning"): Judged {
  const journal = readJournal(folder);
  expect(journal.badLines).toBe(0);
  const judged = journal.records.filter((record) => record.kind === "failure" || record.kind === "warning");
  expect(judged).toHaveLength(1);
  expect(journal.records).toHaveLength(1);
  const record = judged[0] as Judged;
  expect(record.kind).toBe(kind);
  expect(record.session).toBe(session);
  expect(record.harness).toBe("claude-code");
  expect(record.reason.trim().length).toBeGreaterThan(0);
  expect(fs.statSync(path.resolve(folder, record.evidence)).isFile()).toBe(true);
  return record;
}

// V1: the runner made the exit, so D1's failure record stands.
function expectTestFailed(result: HookResult, fields: { input: string | string[]; actual: string }): FailureRecord {
  const record = onlyVerdict("failure") as FailureRecord;
  expect(record.id).toMatch(/^F-[0-9a-f]{8}$/);
  expect(record.check).toBe("R12.2-test-failed");
  expect(record.found_by).toBe("guard");
  expect(fields.input.includes(record.input)).toBe(true);
  expect(record.expected).toBe("all tests pass");
  expect(record.actual).toBe(fields.actual);
  // D4: one context line naming the new id once, and no record text in it.
  expect(result.exitCode).toBe(0);
  expect(result.stderr).toBe("");
  const context = JSON.parse(result.stdout).hookSpecificOutput.additionalContext as string;
  expect(context.match(/harness-guard logged/g)).toHaveLength(1);
  expect(context.split(record.id)).toHaveLength(2);
  expect(context).toContain("already in the journal as evidence; do not log them again.");
  return record;
}

// V2 with Round 9: the guard cannot tell whose exit it was, so the record is a warning the agent settles.
function expectCommandErrorWarning(result: HookResult, fields: { input: string; exit: number }): WarningRecord {
  const record = onlyVerdict("warning") as WarningRecord;
  expect(record.id).toMatch(/^W-[0-9a-f]{8}$/);
  expect(record.check).toBe("R12.2-command-error");
  expect(record.input).toBe(fields.input);
  expect(record.expected).toBe("exit 0");
  expect(record.actual).toBe(`exit ${fields.exit}`);
  // R12.2 (2026-10-17): the context line names the warning and says it is evidence; nothing has to be settled.
  expect(result.exitCode).toBe(0);
  expect(result.stderr).toBe("");
  const context = JSON.parse(result.stdout).hookSpecificOutput.additionalContext as string;
  expect(context).toContain(`harness-guard warning ${record.id}`);
  expect(context).toContain("kept as evidence");
  return record;
}

describe("Round 17 V2: a failed call that holds a test run but whose exit the runner did not make is a guess", () => {
  test("V2/Fails-if: F-bdea5631's shape — a run, a `;`, then a command that exits 2 with no summary — is not a failure", () => {
    // The base-commit run was planned; the worktree was gone, so `ls` exited 2. D1 read the ls's exit as a failed run.
    const result = invokeHook(failedCall(
      "bun test test/round17.test.ts; ls /tmp/gone-worktree",
      `ls: cannot access '/tmp/gone-worktree': No such file or directory\n${planted}`,
      2,
    ));
    expectCommandErrorWarning(result, { input: "ls call", exit: 2 });
  });

  test("V2: after `&&` the exit may still be the runner's, so it is a warning the agent settles", () => {
    // V2's own example: `pytest && echo done`, the runner failing.
    const result = invokeHook(failedCall("pytest -q && echo done", `1 passed, rest skipped\n${planted}`));
    expectCommandErrorWarning(result, { input: "echo call", exit: 1 });
  });

  test("V2: a runner followed by `||` is a warning naming the last command word", () => {
    const result = invokeHook(failedCall("pytest -q || echo fallback ran", `no tests ran\n${planted}`));
    expectCommandErrorWarning(result, { input: "echo call", exit: 1 });
  });

  test("V2: M1's wrappers do not make a not-last runner's exit the runner's (`timeout 60 …`)", () => {
    const result = invokeHook(failedCall(
      "timeout 60 bun test test/round17.test.ts; ls /tmp/gone-worktree",
      `ls: cannot access '/tmp/gone-worktree': No such file or directory\n${planted}`,
      2,
    ));
    expectCommandErrorWarning(result, { input: "ls call", exit: 2 });
  });

  test("V2: M1's wrappers do not make a not-last runner's exit the runner's (`env -u NO_COLOR …`)", () => {
    const result = invokeHook(failedCall(
      "env -u NO_COLOR pytest -q && git status",
      `fatal: not a git repository\n${planted}`,
      128,
    ));
    expectCommandErrorWarning(result, { input: "git call", exit: 128 });
  });

  test("V2 control: the warning's evidence holds the exit and the command word, never the output text", () => {
    const result = invokeHook(failedCall("pytest -q ; ls /tmp/gone-worktree", `2 could not read\n${planted}`, 2));
    const record = expectCommandErrorWarning(result, { input: "ls call", exit: 2 });
    const facts = JSON.parse(fs.readFileSync(path.resolve(folder, record.evidence), "utf8"));
    expect(Object.values(facts)).toContain(2);
    expect(Object.values(facts)).toContain("ls");
  });
});

describe("Round 17 V1: the runner made the exit, or its own summary says so", () => {
  // Changed after the crossed review (finding 2, EJ 2026-10-17): a pipeline's exit is its last command's, so a failed
  // pipeline with no summary is a guess. Written by opencode as R12.2-test-failed; the expectation changed, not the input.
  test("V1/Fails-if: a runner piped to `tail` with no summary is a warning naming tail", () => {
    const result = invokeHook(failedCall("pytest -q 2>&1 | tail -3", `collecting ...\n${planted}`, 1));
    expectCommandErrorWarning(result, { input: "tail call", exit: 1 });
  });

  test("V1: a runner piped to `grep` with no summary is a warning naming grep", () => {
    const result = invokeHook(failedCall(
      "bun test test/round17.test.ts | grep -n failed",
      `no lines matched\n${planted}`,
      1,
    ));
    expectCommandErrorWarning(result, { input: "grep call", exit: 1 });
  });

  test("V1: a runner last after `cd … &&` made the exit", () => {
    const result = invokeHook(failedCall("cd work && pytest -q", `collection error\n${planted}`, 1));
    expectTestFailed(result, { input: "pytest run", actual: "exit 1" });
  });

  test("V1: with two runners the last one is last, so its run is the failure", () => {
    const result = invokeHook(failedCall("pytest -q ; cargo test", `no summary at all\n${planted}`, 1));
    // The specification names the record's input "<runner> run" but no canonical label for which of two runners it is.
    expectTestFailed(result, { input: ["pytest run", "cargo test run"], actual: "exit 1" });
  });

  test("V1/Fails-if: a runner that is not last, whose output holds a failure summary, is R12.2-test-failed", () => {
    // The `ls`'s exit is not the run's, but the summary is the runner's own words (V1's first clause).
    const result = invokeHook(failedCall(
      "pytest -q ; ls /tmp/gone-worktree",
      `3 failed, 2 passed in 0.4s\nls: cannot access '/tmp/gone-worktree'\n${planted}`,
      2,
    ));
    expectTestFailed(result, { input: "pytest run", actual: "3 failed" });
  });

  test("V1: a not-last runner behind M1's wrappers is still recognised when its summary speaks", () => {
    const result = invokeHook(failedCall(
      "timeout 60 env -u NO_COLOR pytest -q && ls /tmp/gone-worktree",
      `2 failed, 9 passed\nls: cannot access '/tmp/gone-worktree'\n${planted}`,
      2,
    ));
    expectTestFailed(result, { input: "pytest run", actual: "2 failed" });
  });

  test("V1: a not-last runner whose PostToolUse stdout holds the summary — D1 speaks only for a run that owns stdout", () => {
    // Every segment after the runner is its own pipeline, so its stdout speaks for the run (D1).
    const result = invokeHook(succeededCall(
      "pytest -q 2>&1 | tail -3",
      `4 failed, 1 passed\n${planted}`,
      "",
    ));
    expectTestFailed(result, { input: "pytest run", actual: "4 failed" });
  });

  test("V1 control: a summary in a not-last runner's stdout is another command's stdout, so nothing is recorded", () => {
    // D1: after `;`, `&&` or `||` other commands write to the same stdout, so the run's exit cannot be read from it.
    const result = invokeHook(succeededCall("pytest -q ; ls /tmp/gone-worktree", `3 failed\n${planted}`, ""));
    expect(result).toEqual({ exitCode: 0, stdout: "", stderr: "" });
    expect(readJournal(folder).records).toEqual([]);
  });

  test("V1 control: a runner made the exit but a person stopped it, so it is not recorded (D1/D2)", () => {
    const payload = failedCall("cd work && pytest -q", `1 failed\n${planted}`, 1);
    expect(invokeHook({ ...payload, is_interrupt: true })).toEqual({ exitCode: 0, stdout: "", stderr: "" });
    expect(readJournal(folder).records).toEqual([]);
  });
});