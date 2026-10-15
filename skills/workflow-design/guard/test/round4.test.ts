// Acceptance expectations come from SPEC.md, Round 4 (D1–D5 and every Fails-if).
import { afterEach, beforeEach, describe, expect, test } from "bun:test";
import { execFileSync } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { handleHook } from "../src/hooks.ts";
import { readJournal } from "../src/journal.ts";
import type { FailureRecord, HookEnv, HookResult } from "../src/types.ts";

const secret = "SECRET-PLANT-7f3a9c";
const time = "2026-10-15T14:00:00.000Z";
const session = "round4-session";
const ownFailureContext = "your own failures count — answer them in the insight; one section may answer several ids with one cause";
const events = ["PostToolUse", "PostToolUseFailure"] as const;
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

function bashFailure(command: string, output = `diagnostic ${secret}`, exit = 1): Record<string, unknown> {
  return {
    hook_event_name: "PostToolUseFailure", session_id: session, cwd: folder,
    tool_name: "Bash", tool_input: { command },
    error: `Exit code ${exit}\n${output}`, is_interrupt: false,
  };
}

function bashSuccess(command: string, stdout = secret, stderr = ""): Record<string, unknown> {
  return {
    hook_event_name: "PostToolUse", session_id: session, cwd: folder,
    tool_name: "Bash", tool_input: { command },
    tool_response: { stdout, stderr, interrupted: false },
  };
}

// Check confidentiality before any behavioural assertion can fail, including on the red baseline.
function invokeHook(payload: Record<string, unknown>): HookResult {
  const result = handleHook(payload, env);
  expect(JSON.stringify(result)).not.toContain(secret);
  expect(JSON.stringify(readJournal(folder))).not.toContain(secret);
  const state = path.join(folder, ".harness-guard");
  if (fs.existsSync(state)) {
    for (const name of fs.readdirSync(state, { recursive: true, encoding: "utf8" })) {
      expect(name).not.toContain(secret);
      const file = path.join(state, name);
      if (fs.statSync(file).isFile()) expect(fs.readFileSync(file, "utf8")).not.toContain(secret);
    }
  }
  return result;
}

function failures(): FailureRecord[] {
  const journal = readJournal(folder);
  expect(journal.badLines).toBe(0);
  // D6 (COO): the journal may also hold "raised" records after a final message names the insight.
  // Round 5 S1 (COO): passing calls also write "success" lines.
  expect(journal.records.every((record) => record.kind === "failure" || record.kind === "raised" || record.kind === "success")).toBe(true);
  return journal.records.filter((record): record is FailureRecord => record.kind === "failure");
}

function expectFailure(check: string, fields: Partial<FailureRecord> = {}): FailureRecord {
  const records = failures();
  expect(records).toHaveLength(1);
  const record = records[0]!;
  expect(record).toMatchObject({ kind: "failure", check, session, found_by: "guard", harness: "claude-code", ...fields });
  expect(record.id).toMatch(/^F-[0-9a-f]{8}$/);
  expect(record.time).toBe(time);
  expect(record.reason.trim().length).toBeGreaterThan(0);
  expect(record.evidence.trim().length).toBeGreaterThan(0);
  expect(fs.statSync(path.resolve(folder, record.evidence)).isFile()).toBe(true);
  expect(() => JSON.parse(fs.readFileSync(path.resolve(folder, record.evidence), "utf8"))).not.toThrow();
  return record;
}

// The spec fixes the evidence facts, but does not prescribe JSON property names or nesting.
function evidenceValues(record: FailureRecord): unknown[] {
  function leaves(value: unknown): unknown[] {
    if (Array.isArray(value)) return value.flatMap(leaves);
    if (value !== null && typeof value === "object") return Object.values(value).flatMap(leaves);
    return [value];
  }
  return leaves(JSON.parse(fs.readFileSync(path.resolve(folder, record.evidence), "utf8")));
}

function contextLine(result: HookResult, ids: string[], ownFailure: boolean): string {
  expect(result.exitCode).toBe(0);
  expect(result.stderr).toBe("");
  const context = JSON.parse(result.stdout).hookSpecificOutput.additionalContext as string;
  expect(context.trim().split("\n")).toHaveLength(1);
  expect(context.match(/harness-guard logged/g)).toHaveLength(1);
  for (const id of ids) {
    expect(context.split(id)).toHaveLength(2);
  }
  expect(context).toContain("already in the journal; do not log them again.");
  expect(context).toContain("An insight answering them is required before you stop.");
  if (ownFailure) expect(context).toContain(ownFailureContext);
  else expect(context).not.toContain("your own failures count");
  return context;
}

function expectQuiet(result: HookResult): void {
  expect(result).toEqual({ exitCode: 0, stdout: "", stderr: "" });
  expect(failures()).toEqual([]);
}

describe("D1 test runs that fail", () => {
  const runners = [
    { command: "pytest -q", identity: /pytest/ },
    { command: "python -m pytest -q", identity: /python|pytest/ },
    { command: "python3 -m pytest -q", identity: /python3?|pytest/ },
    { command: "bun test", identity: /bun/ },
    { command: "npm test", identity: /npm/ },
    { command: "npm run test", identity: /npm/ },
    { command: "yarn test", identity: /yarn/ },
    { command: "pnpm test", identity: /pnpm/ },
    { command: "npx jest", identity: /npx|jest/ },
    { command: "npx vitest", identity: /npx|vitest/ },
    { command: "go test ./...", identity: /go/ },
    { command: "cargo test", identity: /cargo/ },
  ];

  test.each(runners.map((runner) => [runner] as const))("D1: failure event recognises %j", (runner) => {
    const result = invokeHook(bashFailure(runner.command));
    const record = expectFailure("R12.2-test-failed", { expected: "all tests pass", actual: "exit 1" });
    // <runner> has no canonical spelling specified for aliases such as python3 -m pytest.
    expect(record.input).toMatch(runner.identity);
    expect(record.input).toMatch(/ run$/);
    expect(record.input).not.toContain("-q");
    contextLine(result, [record.id], true);
  });

  const wrappers = [
    "CI=1 pytest -q", "timeout 60 pytest -q", "timeout --signal=TERM 60 pytest -q",
    "env -u NO_COLOR pytest -q", "env -i CI=1 pytest -q", "nohup pytest -q", "time pytest -q",
    "exec pytest -q", "command pytest -q", "python3 scripts/runlog.py --out run.log -- pytest -q",
    "scripts/runlog.py --out run.log -- pytest -q",
    "CI=1 timeout 60 env -u NO_COLOR command pytest -q",
  ];
  test.each(wrappers.map((command) => [command]))("D1: M1 wrappers are stripped in %s", (command: string) => {
    const result = invokeHook(bashFailure(command));
    const record = expectFailure("R12.2-test-failed", { input: "pytest run", expected: "all tests pass", actual: "exit 1" });
    contextLine(result, [record.id], true);
  });

  test.each([["cd work && pytest -q"], ["printf heading; pytest -q"], ["true && pytest -q"]])(
    "D1: a test runner in a later segment of %s is recognised", (command: string) => {
      fs.mkdirSync(path.join(folder, "work"));
      const result = invokeHook(bashFailure(command));
      const record = expectFailure("R12.2-test-failed", { input: "pytest run", actual: "exit 1" });
      contextLine(result, [record.id], true);
    },
  );

  test("D1/Fails-if: pytest exit 1 records the summary count without its output text", () => {
    const result = invokeHook(bashFailure("pytest -q", `FAILED test_private.py::case\n${secret}\n3 failed, 4 passed`));
    const record = expectFailure("R12.2-test-failed", { input: "pytest run", expected: "all tests pass", actual: "3 failed" });
    const facts = evidenceValues(record);
    expect(facts).toContain("pytest");
    expect(facts).toContain(3);
    expect(facts).toContain(1);
    expect(JSON.stringify(readJournal(folder))).not.toContain("test_private.py::case");
    expect(fs.readFileSync(path.resolve(folder, record.evidence), "utf8")).not.toContain("test_private.py::case");
    expect(result.stdout + result.stderr).not.toContain("test_private.py::case");
    contextLine(result, [record.id], true);
  });

  test.each([[7], [124]])("D1: no summary falls back to the exit %i from error", (exit: number) => {
    const result = invokeHook(bashFailure("pytest -q", `runner could not start ${secret}`, exit));
    const record = expectFailure("R12.2-test-failed", { input: "pytest run", actual: `exit ${exit}` });
    expect(evidenceValues(record)).toContain(exit);
    contextLine(result, [record.id], true);
  });

  test.each([["2 failed"], ["12 failed"], ["1 error"], ["4 errors"]])(
    "D1/Fails-if: a pipeline hides the exit but stdout gives %s", (summary: string) => {
      const result = invokeHook(bashSuccess("pytest -q | tail -3", `${secret}\n${summary}, 5 passed`));
      const record = expectFailure("R12.2-test-failed", { input: "pytest run", expected: "all tests pass", actual: summary });
      expect(evidenceValues(record)).toContain(Number(summary.split(" ")[0]));
      contextLine(result, [record.id], true);
    },
  );

  test.each(runners.map((runner) => [runner] as const))("D1 control: passing %j stays quiet", (runner) => {
    expectQuiet(invokeHook(bashSuccess(runner.command, `15 passed, 0 failed, 0 errors\n${secret}`)));
  });

  test.each([["0 failed"], ["0 errors"], ["2 failures"], ["failed 2"], ["x2 failed"], ["2 failedness"]])(
    "D1 control: stdout %s does not match the specified failure summary", (summary: string) => {
      expectQuiet(invokeHook(bashSuccess("pytest -q", `${summary}\n${secret}`)));
    },
  );

  test("D1 control: PostToolUse stderr alone does not trigger the stdout rule", () => {
    expectQuiet(invokeHook(bashSuccess("pytest -q", "15 passed", `2 failed\n${secret}`)));
  });

  test.each([
    ['echo "pytest -q"'], ['printf "%s" "bun test"'], ['grep "pytest" notes.txt'],
    ["npm run build"], ["python3 -m compileall ."], ["cat <<'EOF'\npytest -q\nEOF"],
  ])("D1 control: %s is not a test runner command word", (command: string) => {
    expectQuiet(invokeHook(bashSuccess(command, `2 failed\n${secret}`)));
  });
});

describe("D2 other Bash calls that error", () => {
  test.each([
    [{ command: "false", input: "false call", exit: 1 }],
    [{ command: "git status", input: "git call", exit: 128 }],
    [{ command: "missing-command --flag", input: "missing-command call", exit: 127 }],
    [{ command: "timeout 60 env -u X false", input: "false call", exit: 7 }],
    [{ command: "pytest-helper --flag", input: "pytest-helper call", exit: 1 }],
    [{ command: "npm run build", input: "npm call", exit: 1 }],
    [{ command: "npx jestify", input: "npx call", exit: 1 }],
  ])("D2/Fails-if: ordinary failure %j is recorded", ({ command, input, exit }) => {
    const result = invokeHook(bashFailure(command, `ordinary diagnostic ${secret}`, exit));
    const record = expectFailure("R12.2-command-error", { input, expected: "exit 0", actual: `exit ${exit}` });
    contextLine(result, [record.id], true);
  });

  test.each([["false"], ["grep needle absent.txt"], ["pytest -q"], ["bun test"]])(
    "D2/Fails-if: a person interrupted %s, so it is not recorded", (command: string) => {
      expectQuiet(invokeHook({ ...bashFailure(command), is_interrupt: true }));
    },
  );

  test("D2/Fails-if: grep with no match is PostToolUse and stays quiet", () => {
    expectQuiet(invokeHook(bashSuccess("grep needle absent.txt", "", secret)));
  });

  test("D2 control: ordinary stdout saying 2 failed does not make it a test run", () => {
    expectQuiet(invokeHook(bashSuccess('printf "2 failed"', `2 failed\n${secret}`)));
  });

  test("D2 control: an engine failure belongs to M5, without a duplicate command-error record", () => {
    fs.writeFileSync(path.join(folder, "answer.md"), "complete answer");
    const result = invokeHook(bashFailure("codex exec x -o answer.md </dev/null", secret, 7));
    const record = expectFailure("R12.1-exit");
    contextLine(result, [record.id], false);
  });
});

describe("D3 unknown paths are not checked", () => {
  const outputPaths = ["$OUT/r.md", "${OUT}/r.md", "`printf out`/r.md", "out/*.md", "out/?.md", "out/[ab].md"];
  const cdTargets = ["$R", "${R}", "`printf work`", "work/*", "work/?", "work/[ab]"];

  for (const event of events) {
    function payload(command: string): Record<string, unknown> {
      return event === "PostToolUseFailure" ? bashFailure(command) : bashSuccess(command);
    }

    test.each(outputPaths.map((output) => [output]))(`D3/Fails-if: ${event} skips unknown -o %s`, (output: string) => {
      expectQuiet(invokeHook(payload(`codex exec x -o ${output} </dev/null`)));
    });

    test.each(outputPaths.map((output) => [output]))(`D3: ${event} skips unknown redirect %s`, (output: string) => {
      expectQuiet(invokeHook(payload(`codex exec x > ${output} </dev/null`)));
    });

    test.each(cdTargets.map((target) => [target]))(`D3: ${event} skips unknown cd %s`, (target: string) => {
      expectQuiet(invokeHook(payload(`cd ${target} && codex exec x -o answer.md </dev/null`)));
    });
  }

  test("D3 control: a known missing output is still checked", () => {
    const result = invokeHook(bashSuccess("codex exec x -o missing.md </dev/null"));
    const record = expectFailure("R12.1-missing-output");
    contextLine(result, [record.id], false);
  });

  test("D3 control: a known cd target still checks a missing output", () => {
    fs.mkdirSync(path.join(folder, "work"));
    const result = invokeHook(bashSuccess("cd work && codex exec x -o missing.md </dev/null"));
    const record = expectFailure("R12.1-missing-output");
    contextLine(result, [record.id], false);
  });

  test("D3 control: metacharacters in prompt text do not make a literal output path unknown", () => {
    const result = invokeHook(bashSuccess('codex exec "explain $VALUE and glob * ? [a]" -o missing.md </dev/null'));
    const record = expectFailure("R12.1-missing-output");
    contextLine(result, [record.id], false);
  });
});

describe("D4 context and insight for the agent's own failures", () => {
  test("D4: one failed run with several summary counts produces one record and one context line", () => {
    const result = invokeHook(bashSuccess("pytest -q | tail -3", `2 failed, 3 passed\n${secret}`));
    const record = expectFailure("R12.2-test-failed");
    contextLine(result, [record.id], true);
  });

  test("D4: an engine context names every new id once and retains the C23 wording", () => {
    const payload = bashSuccess("codex exec x -o missing.md </dev/null");
    payload.tool_response = { stdout: secret, stderr: "", interrupted: true };
    const result = invokeHook(payload);
    const records = failures();
    expect(records).toHaveLength(2);
    expect(records.map((record) => record.check).sort()).toEqual(["R12.1-interrupted", "R12.1-missing-output"]);
    for (const record of records) expect(fs.existsSync(path.resolve(folder, record.evidence))).toBe(true);
    contextLine(result, records.map((record) => record.id), false);
  });

  test("D4: repeated failures report each new id once without re-announcing old ids", () => {
    const firstResult = invokeHook(bashFailure("false"));
    const first = expectFailure("R12.2-command-error");
    contextLine(firstResult, [first.id], true);
    const secondResult = invokeHook(bashFailure("false"));
    const records = failures();
    expect(records).toHaveLength(2);
    const second = records[1]!;
    expect(second.id).not.toBe(first.id);
    expect(contextLine(secondResult, [second.id], true)).not.toContain(first.id);
  });

  test("D4: both own failure kinds block Stop and one insight section can answer both ids", () => {
    const testResult = invokeHook(bashFailure("pytest -q"));
    const testFailure = expectFailure("R12.2-test-failed");
    contextLine(testResult, [testFailure.id], true);
    const commandResult = invokeHook(bashFailure("false"));
    const records = failures();
    expect(records).toHaveLength(2);
    const commandFailure = records[1]!;
    expect(commandFailure.check).toBe("R12.2-command-error");
    contextLine(commandResult, [commandFailure.id], true);
    const stop = { hook_event_name: "Stop", session_id: session, cwd: folder, stop_hook_active: false };
    const blocked = invokeHook(stop);
    expect(blocked.exitCode).toBe(0);
    expect(blocked.stderr).toBe("");
    const decision = JSON.parse(blocked.stdout);
    expect(decision.decision).toBe("block");
    for (const record of records) expect(decision.reason).toContain(record.id);

    const insight = ".harness-guard/insights/own-failures.md";
    fs.mkdirSync(path.dirname(path.join(folder, insight)), { recursive: true });
    fs.writeFileSync(path.join(folder, insight), [
      `## ${records.map((record) => record.id).join(", ")}`, "Whys:",
      "1. The commands used an invalid fixture.", "2. The fixture had not been checked.",
      "3. The check omitted fixture validation.", "Source: check",
      "Root cause: fixture validation was absent.", "Options:",
      "1. [check] validate the fixture; evidence: test/round4.test.ts",
      "2. [rule] require a valid fixture; evidence: SPEC.md", "",
    ].join("\n"));
    expect(invokeHook({ ...stop, last_assistant_message: `Insight: ${insight}` })).toEqual({ exitCode: 0, stdout: "", stderr: "" });
    expect(failures()).toHaveLength(2);
  });
});

describe("D5 non-Bash errors are not observable in this round", () => {
  // Synthetic payloads pin the handler boundary; they cannot prove which events a live harness emits.
  for (const event of events) {
    test.each([["Edit"], ["Write"], ["Read"]])(`D5: ${event} for %s does not manufacture a Bash failure`, (tool: string) => {
      const payload = event === "PostToolUseFailure" ? bashFailure("false") : bashSuccess("false");
      expectQuiet(invokeHook({
        ...payload, tool_name: tool,
        tool_input: { file_path: "notes.md", old_string: "old", new_string: "new" },
      }));
    });
  }
});
