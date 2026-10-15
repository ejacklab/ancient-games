// Acceptance expectations: SPEC.md Round 5 S1/S2/S5, with M1/M2/M3/M5, C1, D1/D3/D6.
import { afterEach, beforeEach, describe, expect, test } from "bun:test";
import { execFileSync, spawnSync } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { handleHook } from "../src/hooks.ts";
import { readJournal } from "../src/journal.ts";
import { rates } from "../src/rates.ts";
import type { FailureRecord, HookEnv, HookResult, JournalRecord, SuccessPath, SuccessRecord } from "../src/types.ts";

const secret = "SECRET-PLANT-7f3a9c";
const time = "2026-10-15T15:00:00.000Z";
const session = "round5-session";
const cli = path.resolve(import.meta.dir, "../src/cli.ts");
let root: string;
let env: HookEnv;

beforeEach(() => {
  root = fs.mkdtempSync(path.join(os.tmpdir(), "hg-"));
  execFileSync("git", ["init", "--quiet"], { cwd: root });
  env = { cwd: root, running: [], now: () => new Date(time) };
});

afterEach(() => fs.rmSync(root, { recursive: true, force: true }));

function write(relative: string, content: string): void {
  const file = path.join(root, relative);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, content);
}

function bash(command: string, stdout = `answer ${secret}`, stderr = ""): Record<string, unknown> {
  return {
    hook_event_name: "PostToolUse", session_id: session, cwd: root, tool_name: "Bash",
    tool_input: { command }, tool_response: { stdout, stderr, interrupted: false },
  };
}

function failure(command: string): Record<string, unknown> {
  return {
    ...bash(command), hook_event_name: "PostToolUseFailure", exit_code: 1,
    error: `Exit code 1\n${secret}`,
  };
}

function invoke(payload: Record<string, unknown>): HookResult {
  const result = handleHook(payload, env);
  // Check all guard-owned output before behavioural assertions, even on a red baseline.
  expect(JSON.stringify(result)).not.toContain(secret);
  const state = path.join(root, ".harness-guard");
  if (fs.existsSync(state)) {
    for (const relative of fs.readdirSync(state, { recursive: true, encoding: "utf8" })) {
      expect(relative).not.toContain(secret);
      const file = path.join(state, relative);
      if (fs.statSync(file).isFile()) expect(fs.readFileSync(file, "utf8")).not.toContain(secret);
    }
  }
  expect(result.exitCode).toBe(0);
  expect(result.stderr).toBe("");
  return result;
}

function records(): JournalRecord[] {
  const journal = readJournal(root);
  expect(journal.badLines).toBe(0);
  return journal.records;
}

function successes(): SuccessRecord[] {
  return records().filter((record): record is SuccessRecord => record.kind === "success");
}

function success(check = "engine-call", engine = "codex", selectedSession = session): SuccessRecord {
  return { kind: "success", time, session: selectedSession, check, engine };
}

function failed(check: string, engine: string, selectedSession = session, id = "F-1234abcd"): FailureRecord {
  return {
    kind: "failure", id, time, session: selectedSession, found_by: "guard", check, engine,
    harness: "claude-code", input: `${engine} call`, expected: "exit 0", actual: "exit 1",
    reason: "planted failure", evidence: ".harness-guard/evidence/fixture.json",
  };
}

// Write journal fixtures directly so S2/S5 tests do not depend on S1 being implemented.
function seed(entries: JournalRecord[]): void {
  write(".harness-guard/journal.jsonl", entries.map((entry) => JSON.stringify(entry)).join("\n") + "\n");
  write(".harness-guard/evidence/fixture.json", '{"exit":1}\n');
}

function stop(message = "done", selectedSession = session, event = "Stop"): HookResult {
  return invoke({
    hook_event_name: event, session_id: selectedSession, cwd: root,
    stop_hook_active: false, last_assistant_message: message,
  });
}

function expectPathAsk(result: HookResult): void {
  const output = JSON.parse(result.stdout);
  expect(output.decision).toBe("block");
  expect(output.reason).toContain("harness-guard: record the path of this task");
  expect(output.reason).toContain("path new --session " + session);
  expect(output.reason).toContain("--out runs/<run>/success-path.yaml");
  expect(output.reason).toContain(".harness-guard/paths/<name>.yaml");
  expect(output.reason).toContain("fill steps, decisions and measures");
  expect(output.reason).toContain("name a parent and what you changed");
}

function pathFile(file: string, selectedSession = session, great = false): void {
  if (great) write("comparison.txt", "comparison evidence");
  const value: SuccessPath = {
    path: 1, session: selectedSession, category: "test", objective: "check a result",
    steps: [{ did: "ran the check" }], decisions: ["used the existing check"], measures: { successes: 1 },
    ...(great ? { great: { comparison: "fewer retries", evidence: "comparison.txt" } } : {}),
  };
  // JSON is valid YAML, and avoids introducing a serialization dependency.
  write(file, JSON.stringify(value));
}

describe("S1 success lines", () => {
  test("Fails-if: a passing engine writes exactly one success, with no context or raw content", () => {
    write("answer.md", `file answer ${secret}`);
    expect(invoke(bash(`codex exec '${secret}' -o answer.md </dev/null`, `stdout ${secret}`, `stderr ${secret}`)).stdout).toBe("");
    expect(records()).toEqual([success()]);
  });

  test("a stdout-answer engine also writes a success", () => {
    expect(invoke(bash(`opencode run '${secret}'`)).stdout).toBe("");
    expect(records()).toEqual([success("engine-call", "opencode")]);
  });

  const runners = [
    ["pytest -q", /pytest/], ["python -m pytest -q", /python|pytest/],
    ["python3 -m pytest -q", /python|pytest/], ["bun test", /bun/],
    ["npm test", /npm/], ["npm run test", /npm/], ["yarn test", /yarn/],
    ["pnpm test", /pnpm/], ["npx jest", /npx|jest/], ["npx vitest", /npx|vitest/],
    ["go test ./...", /go/], ["cargo test", /cargo/],
  ] as const;
  test.each(runners.map((runner) => [runner] as const))("Fails-if: green test run %j writes a quiet success", ([command, label]) => {
    expect(invoke(bash(`${command} '${secret}'`, `12 passed, 0 failed, 0 errors\n${secret}`)).stdout).toBe("");
    expect(records()).toHaveLength(1);
    expect(successes()[0]).toMatchObject({ kind: "success", session, time, check: "test-run" });
    // D1 does not fix a single spelling for labels such as python3 -m pytest.
    expect(successes()[0]!.engine).toMatch(label);
  });

  test.each([
    ["codex exec x -o missing.md </dev/null", "missing"],
    ["codex exec x -o empty.md </dev/null", "empty"],
    ["opencode run x", "empty-stdout"],
    ["agy -p x", "silent-failure"],
    ["codex exec x -o answer.md </dev/null", "exit"],
    ["pytest -q", "exit"],
    ["pytest -q | tail -3", "summary"],
  ])("Fails-if: failing %s (%s) never writes success", (command: string, mode: string) => {
    write("empty.md", " \n");
    write("answer.md", "answer");
    const payload = mode === "exit" ? failure(command) : bash(command,
      mode === "empty-stdout" ? "" : mode === "summary" ? `2 failed\n${secret}` : secret,
      mode === "silent-failure" ? `auto-denied ${secret}` : "");
    invoke(payload);
    expect(successes()).toEqual([]);
    expect(records().some((record) => record.kind === "failure")).toBe(true);
  });

  test.each([["segment"], ["input"], ["response"]])("C1: background via %s writes nothing", (source: string) => {
    write("answer.md", "answer");
    const payload = bash("codex exec x -o answer.md </dev/null" + (source === "segment" ? " &" : ""));
    if (source === "input") payload.tool_input = { command: "codex exec x -o answer.md </dev/null", run_in_background: true };
    if (source === "response") payload.tool_response = { stdout: secret, backgroundTaskId: "bg-1" };
    expect(invoke(payload).stdout).toBe("");
    expect(records()).toEqual([]);
  });

  test.each([
    ["codex exec x -o $OUT/r.md </dev/null"],
    ["codex exec x -o out/*.md </dev/null"],
    ["cd $ROOT && codex exec x -o answer.md </dev/null"],
  ])("D3: unknown paths in %s write nothing", (command: string) => {
    expect(invoke(bash(command)).stdout).toBe("");
    expect(records()).toEqual([]);
  });

  test("an ordinary command is not a checked success", () => {
    expect(invoke(bash(`echo '${secret}'`)).stdout).toBe("");
    expect(records()).toEqual([]);
  });
});

describe("S2 rates", () => {
  test("Fails-if: mixed counts, mapping, session filters and non-result records", () => {
    seed([
      success(), success(), success("test-run", "pytest"), success("engine-call", "opencode", "other"),
      failed("R12.1-exit", "codex"), failed("trap:codex-fixture", "codex"),
      failed("R12.2-test-failed", "pytest"), failed("R12.2-command-error", "none"),
      failed("R12.1-exit", "none"), failed("trap:fixture", "none"),
      failed("custom-check", "codex"), failed("R12.1-timeout", "opencode", "other"),
      { kind: "raised", session, time, ids: ["path"] },
      { kind: "touched", session, time, path: "register.yaml" },
      { kind: "guard_error", session, time, message: "fixture error" },
    ]);
    const expected = [
      { check: "engine-call", engine: "codex", ok: 2, fail: 2 },
      { check: "test-run", engine: "pytest", ok: 1, fail: 1 },
      { check: "R12.2-command-error", engine: "none", ok: 0, fail: 1 },
      { check: "R12.1-exit", engine: "none", ok: 0, fail: 1 },
      { check: "trap:fixture", engine: "none", ok: 0, fail: 1 },
      { check: "custom-check", engine: "codex", ok: 0, fail: 1 },
    ];
    const sorted = (rows: ReturnType<typeof rates>) => [...rows].sort((a, b) => `${a.check}/${a.engine}`.localeCompare(`${b.check}/${b.engine}`));
    expect(sorted(rates(root, session))).toEqual(sorted(expected));
    expect(sorted(rates(root, null))).toEqual(sorted([
      ...expected, { check: "engine-call", engine: "opencode", ok: 1, fail: 1 },
    ]));
    expect(rates(root, "absent")).toEqual([]);
  });

  test("an empty journal has no rates", () => expect(rates(root, null)).toEqual([]));

  test("Fails-if: rates rows contain raw command, prompt or output text", () => {
    const record = failed("R12.1-exit", "codex");
    record.input = `codex exec '${secret}'`;
    record.actual = `output ${secret}`;
    record.reason = `prompt ${secret}`;
    seed([record, success()]);
    const rows = rates(root, null);
    expect(JSON.stringify(rows)).not.toContain(secret);
    expect(rows).toEqual([{ check: "engine-call", engine: "codex", ok: 1, fail: 1 }]);
  });

  test.each([[false], [true]])("CLI rates prints a Markdown table, exit 0; session filter %s", (filtered: boolean) => {
    const record = failed("R12.1-exit", "codex");
    record.input = `codex exec '${secret}'`;
    record.actual = `output ${secret}`;
    seed([success(), record, success("test-run", "pytest", "other")]);
    const result = spawnSync(process.execPath, [cli, "rates", ...(filtered ? ["--session", session] : [])], {
      cwd: root, input: "", encoding: "utf8", timeout: 10000,
    });
    expect(result.error).toBeUndefined();
    expect(result.signal).toBeNull();
    const stdout = result.stdout;
    expect(stdout + result.stderr).not.toContain(secret);
    expect(result.status).toBe(0);
    expect(result.stderr).toBe("");
    const lines = stdout.trim().split("\n");
    expect(lines[0]).toMatch(/\|\s*check\s*\|\s*engine\s*\|\s*ok\s*\|\s*fail\s*\|/i);
    expect(lines[1]).toMatch(/^\s*\|?[\s:|-]+\|\s*$/);
    expect(stdout).toMatch(/\|\s*engine-call\s*\|\s*codex\s*\|\s*1\s*\|\s*1\s*\|/);
    if (filtered) expect(stdout).not.toContain("pytest");
    else expect(stdout).toMatch(/\|\s*test-run\s*\|\s*pytest\s*\|\s*1\s*\|\s*0\s*\|/);
  });
});

describe("S5 Stop asks for the path once", () => {
  test.each([["Stop"], ["SubagentStop"]])("Fails-if: %s asks once and records the session marker", (event: string) => {
    seed([success()]);
    expectPathAsk(stop("done", session, event));
    expect(records().filter((record) => record.kind === "raised")).toEqual([
      { kind: "raised", time, session, ids: ["path"] },
    ]);
    expect(stop("another reply", session, event).stdout).toBe("");
    expect(records().filter((record) => record.kind === "raised")).toHaveLength(1);
  });

  test("a success produced through the hook leads to the path ask", () => {
    invoke(bash("pytest -q", `12 passed\n${secret}`));
    expectPathAsk(stop());
  });

  test.each([["empty"], ["other session"], ["non-success records"]])("Fails-if: no successes in this session (%s) means no ask", (fixture: string) => {
    if (fixture === "other session") seed([success("engine-call", "codex", "other")]);
    if (fixture === "non-success records") seed([{ kind: "guard_error", time, session, message: "fixture" }]);
    expect(stop().stdout).toBe("");
    expect(records().filter((record) => record.kind === "raised")).toEqual([]);
  });

  test("another session's path marker does not consume this session's ask", () => {
    seed([success(), { kind: "raised", time, session: "other", ids: ["path"] }]);
    expectPathAsk(stop());
  });

  test("further successes do not reset an existing path reminder", () => {
    seed([success(), { kind: "raised", time, session, ids: ["path"] }]);
    invoke(bash("pytest -q", `12 passed\n${secret}`));
    expect(stop().stdout).toBe("");
    expect(records().filter((entry) => entry.kind === "raised")).toHaveLength(1);
  });

  test.each([["runs/success-path.yaml"], ["runs/task/nested/success-path-1.yaml"], [".harness-guard/paths/task.yaml"]])(
    "a path naming this session at %s satisfies Stop", (file: string) => {
      seed([success()]);
      pathFile(file);
      expect(stop().stdout).toBe("");
      expect(records().filter((record) => record.kind === "raised")).toEqual([]);
    },
  );

  test("another session's path does not satisfy this session", () => {
    seed([success()]);
    pathFile("runs/success-path.yaml", "other");
    expectPathAsk(stop());
  });

  test("open failures and their raise check precede the path ask; D6 then stays raised", () => {
    const record = failed("R12.2-test-failed", "pytest");
    seed([success(), record]);
    expect(stop().stdout).toContain(record.id);
    expect(records().filter((entry) => entry.kind === "raised")).toEqual([]);
    const insight = ".harness-guard/insights/answer.md";
    write(insight, `## ${record.id}\nWhys:\n1. fixture was invalid\n2. validation was absent\n3. check omitted validation\nSource: check\nRoot cause: missing validation\nOptions:\n1. [check] validate evidence: fixture\n2. [tool] validate evidence: fixture\n`);
    expect(stop().stdout).toContain("raise the insight");
    expect(records().filter((entry) => entry.kind === "raised")).toEqual([]);
    expectPathAsk(stop(`see ${insight}`));
    const raisedIds = records().flatMap((entry) => entry.kind === "raised" ? entry.ids : []);
    expect(raisedIds).toContain(record.id);
    expect(raisedIds).toContain("path");
    expect(stop("unrelated later reply").stdout).toBe("");
  });

  test.each([[false], [true]])("a great path with no valid great section asks once (invalid section: %s)", (invalid: boolean) => {
    seed([success()]);
    const file = "runs/success-path.yaml";
    pathFile(file, session, true);
    if (invalid) write("runs/insight.md", `## great: ${file}\nComparison: fewer retries\nOptions:\n1. [check] validate evidence: comparison.txt\n`);
    // S5 requires the same once-only block, without prescribing great-section reason text.
    expect(JSON.parse(stop().stdout).decision).toBe("block");
    expect(stop().stdout).toBe("");
    expect(records().filter((entry) => entry.kind === "raised")).toEqual([
      { kind: "raised", time, session, ids: ["path"] },
    ]);
  });

  test("a great path with a valid great insight needs no ask", () => {
    seed([success()]);
    const file = "runs/success-path.yaml";
    pathFile(file, session, true);
    write("runs/insight.md", `## great: ${file}\nComparison: fewer retries\nCause: fixture validation\nOptions:\n1. [check] validate evidence: comparison.txt\n`);
    expect(stop().stdout).toBe("");
    expect(records().filter((entry) => entry.kind === "raised")).toEqual([]);
  });
});
