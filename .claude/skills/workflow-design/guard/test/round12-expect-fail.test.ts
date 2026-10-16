// Acceptance expectations come from SPEC.md Round 12, E1–E4 (a planned red run).
import { afterEach, beforeEach, expect, test } from "bun:test";
import { execFileSync, spawnSync } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { handleHook } from "../src/hooks.ts";
import { appendRecord, readJournal } from "../src/journal.ts";
import { openFailures } from "../src/insight.ts";
import type { FailureRecord, HookEnv, HookResult, JournalRecord } from "../src/types.ts";

const secret = "SECRET-PLANT-e12";
const session = "round12-session";
const cli = path.resolve(import.meta.dirname, "..", "src", "cli.ts");
let root: string;
let env: HookEnv;
let tick: number;
let serial: number;

beforeEach(() => {
  root = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), "hg-round12-")));
  execFileSync("git", ["init", "--quiet"], { cwd: root });
  for (const name of ["tests/test_a.py", "tests/test_b.py"]) {
    fs.mkdirSync(path.join(root, path.dirname(name)), { recursive: true });
    fs.writeFileSync(path.join(root, name), "def test_x():\n    assert False\n");
  }
  tick = Date.parse("2026-10-17T04:00:00.000Z");
  serial = 0;
  env = { cwd: root, running: [], now: () => new Date(tick) };
});
afterEach(() => fs.rmSync(root, { recursive: true, force: true }));

// A declaration as E1 writes it, appended directly so these tests read the hook's side alone.
function declare(file: string, owner = session): string {
  serial += 1;
  const id = `E-0000000${serial}`;
  tick += 1000;
  appendRecord(root, { kind: "expect-fail", id, time: new Date(tick).toISOString(), session: owner, file } as never);
  return id;
}

function red(command: string, output = `2 failed, 1 passed ${secret}`, owner = session): HookResult {
  return invoke({
    hook_event_name: "PostToolUseFailure", session_id: owner, cwd: root, tool_name: "Bash",
    tool_input: { command }, error: `Exit code 1\n${output}`, is_interrupt: false,
  });
}

function green(command: string, stdout = `3 passed ${secret}`): HookResult {
  return invoke({
    hook_event_name: "PostToolUse", session_id: session, cwd: root, tool_name: "Bash",
    tool_input: { command }, tool_response: { stdout, stderr: "", interrupted: false },
  });
}

function invoke(payload: Record<string, unknown>): HookResult {
  tick += 1000;
  const result = handleHook(payload, env);
  expect(JSON.stringify(result)).not.toContain(secret);
  expect(fs.readFileSync(path.join(root, ".harness-guard", "journal.jsonl"), "utf8")).not.toContain(secret);
  return result;
}

function records(kind: string): JournalRecord[] {
  const journal = readJournal(root);
  expect(journal.badLines).toBe(0);
  return journal.records.filter((record) => record.kind === kind);
}

function failures(): FailureRecord[] {
  return records("failure") as FailureRecord[];
}

// ---- E3: red as declared

test("a failing run naming a declared file is a red record, not a failure", () => {
  const id = declare("tests/test_a.py");
  const result = red("python3 -m pytest -q tests/test_a.py");
  expect(failures()).toEqual([]);
  const reds = records("red");
  expect(reds).toHaveLength(1);
  expect(reds[0]).toMatchObject({ kind: "red", session, runner: "pytest", declared: [id], failed: 2 });
  expect(JSON.stringify(result)).toContain(id);
});

test("the run after the red step is judged as usual: a failure, then a success line", () => {
  declare("tests/test_a.py");
  red("pytest tests/test_a.py");
  red("pytest tests/test_a.py");
  expect(failures().map((record) => record.check)).toEqual(["R12.2-test-failed"]);
  green("pytest tests/test_a.py | tail -1");
  expect(records("success")).toHaveLength(1);
});

test("one declaration covers one run", () => {
  declare("tests/test_a.py");
  red("pytest tests/test_a.py");
  red("pytest tests/test_a.py");
  expect(records("red")).toHaveLength(1);
  expect(failures()).toHaveLength(1);
});

test("a run in the folder a cd moved to, with a pytest node id, is covered", () => {
  const id = declare("tests/test_a.py");
  red("cd tests && pytest -q test_a.py::test_x 2>&1 | tail -3");
  expect(failures()).toEqual([]);
  expect(records("red")[0]).toMatchObject({ declared: [id] });
});

test("a red record holds counts, never output text", () => {
  declare("tests/test_a.py");
  red("pytest tests/test_a.py", `1 failed ${secret}\nAssertionError: ${secret}`);
  const line = JSON.stringify(records("red")[0]);
  expect(line).not.toContain(secret);
  expect(line).not.toContain("AssertionError");
});

// ---- E4: green where red was declared

test("a covered run that passes is an R12.2-red-passed failure and writes no success line", () => {
  const id = declare("tests/test_a.py");
  const result = green("python3 -m pytest -q tests/test_a.py | tail -1");
  const found = failures();
  expect(found).toHaveLength(1);
  expect(found[0]).toMatchObject({ check: "R12.2-red-passed", input: "pytest run", expected: "the declared red run fails",
    actual: "no test failed", declared: [id], found_by: "guard" });
  expect(fs.existsSync(path.resolve(root, found[0]!.evidence))).toBe(true);
  expect(records("success")).toEqual([]);
  expect(openFailures(root, session).map((record) => record.id)).toEqual([found[0]!.id]);
  expect(JSON.stringify(result)).toContain(found[0]!.id);
});

// ---- R12 still holds (D1): what a declaration does not excuse

test("a failing run with no declaration is a failure, as before", () => {
  red("pytest tests/test_a.py");
  expect(failures().map((record) => record.check)).toEqual(["R12.2-test-failed"]);
  expect(records("red")).toEqual([]);
});

test("another session's declaration does not cover the run", () => {
  declare("tests/test_a.py", "another-session");
  red("pytest tests/test_a.py");
  expect(failures()).toHaveLength(1);
  expect(records("red")).toEqual([]);
});

test("another file's declaration does not cover the run, and stays open", () => {
  declare("tests/test_b.py");
  red("pytest tests/test_a.py");
  expect(failures()).toHaveLength(1);
  red("pytest tests/test_b.py");
  expect(records("red")).toHaveLength(1);
});

test("a declaration made after a failing run does not remove its failure", () => {
  red("pytest tests/test_a.py");
  const [failure] = failures();
  declare("tests/test_a.py");
  expect(openFailures(root, session).map((record) => record.id)).toEqual([failure!.id]);
});

test("an interrupted run consumes nothing", () => {
  const id = declare("tests/test_a.py");
  invoke({ hook_event_name: "PostToolUseFailure", session_id: session, cwd: root, tool_name: "Bash",
    tool_input: { command: "pytest tests/test_a.py" }, error: "Exit code 130\n", is_interrupt: true });
  red("pytest tests/test_a.py");
  expect(records("red")[0]).toMatchObject({ declared: [id] });
});

// ---- E1: the command

function runCli(args: string[], extraEnv: Record<string, string | undefined> = {}) {
  const childEnv: Record<string, string | undefined> = { ...process.env, CLAUDE_CODE_SESSION_ID: undefined, ...extraEnv };
  for (const key of Object.keys(childEnv)) if (childEnv[key] === undefined) delete childEnv[key];
  return spawnSync(process.execPath, [cli, ...args], { cwd: root, encoding: "utf8", timeout: 10000,
    env: childEnv as NodeJS.ProcessEnv });
}

test("expect-fail records a declaration with the harness session, root-relative", () => {
  const result = runCli(["expect-fail", "--tests", "tests/test_a.py"], { CLAUDE_CODE_SESSION_ID: "env-session" });
  expect(result.status).toBe(0);
  const [record] = records("expect-fail");
  expect(record).toMatchObject({ kind: "expect-fail", session: "env-session", file: "tests/test_a.py" });
  expect((record as { id: string }).id).toMatch(/^E-[0-9a-f]{8}$/);
  expect(result.stdout).toContain((record as { id: string }).id);
});

test("expect-fail takes --session over the harness session, and none without either", () => {
  runCli(["expect-fail", "--tests", "tests/test_a.py", "--session", "flag-session"], { CLAUDE_CODE_SESSION_ID: "env-session" });
  runCli(["expect-fail", "--tests", "tests/test_b.py"]);
  expect(records("expect-fail").map((record) => record.session)).toEqual(["flag-session", "none"]);
});

test("expect-fail refuses a missing file and a file outside the root", () => {
  const outside = fs.mkdtempSync(path.join(os.tmpdir(), "hg-round12-out-"));
  fs.writeFileSync(path.join(outside, "test_c.py"), "");
  try {
    const cases: [string, string][] = [["tests/test_missing.py", "no such file"], [path.join(outside, "test_c.py"), "outside the root"]];
    for (const [target, why] of cases) {
      const result = runCli(["expect-fail", "--tests", target]);
      expect(result.status).toBe(2);
      expect(result.stderr).toContain(`expect-fail: ${why}`);
    }
    expect(records("expect-fail")).toEqual([]);
  } finally {
    fs.rmSync(outside, { recursive: true, force: true });
  }
});

test("a declaration from the command covers the hook's next run of that file", () => {
  runCli(["expect-fail", "--tests", "tests/test_a.py"], { CLAUDE_CODE_SESSION_ID: session });
  red("pytest tests/test_a.py");
  expect(failures()).toEqual([]);
  expect(records("red")).toHaveLength(1);
});
