import { afterEach, beforeEach, describe, expect, spyOn, test } from "bun:test";
import { execFileSync } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { handleHook } from "../src/hooks.ts";
import { appendFailure, readJournal, validateFailure, writeEvidence } from "../src/journal.ts";
import { freezeHash, units } from "../src/register.ts";
import { lintCommand } from "../src/traps.ts";
import type { FailureRecord, GuardErrorRecord, HookEnv, HookResult, Register, TouchedRecord } from "../src/types.ts";

const secret = "SECRET-PLANT-7f3a9c";
const time = "2026-10-15T08:00:00.000Z";
const first = "F-1a2b3c4d";
const second = "F-2b3c4d5e";
let folder: string;
let env: HookEnv;

beforeEach(() => {
  folder = fs.mkdtempSync(path.join(os.tmpdir(), "hg-"));
  env = { cwd: folder, running: [], now: () => new Date(time) };
});

afterEach(() => {
  fs.rmSync(folder, { recursive: true, force: true });
});

function writeFile(name: string, text: string): string {
  const file = path.join(folder, name);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, text);
  return file;
}

function bash(event: string, command: string, response: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    hook_event_name: event,
    session_id: "session-a",
    tool_name: "Bash",
    tool_input: { command },
    tool_response: { stdout: "", stderr: "", interrupted: false, ...response },
    // The failure event does not specify where its exit and error fields live.
    ...(event === "PostToolUseFailure" ? response : {}),
  };
}

function stop(event = "Stop", changes: Record<string, unknown> = {}): Record<string, unknown> {
  return { hook_event_name: event, session_id: "session-a", stop_hook_active: false, ...changes };
}

function seedFailure(id = first, session = "session-a"): FailureRecord {
  const rec: FailureRecord = {
    kind: "failure", id, time, session, found_by: "guard", check: "R12.1-empty-output",
    input: "codex answer.md", expected: "non-empty output", actual: "empty output",
    engine: "codex", harness: "claude-code", reason: "the output file is empty",
    evidence: writeEvidence(folder, id, { stdoutLength: 0, rules: ["R12.1-empty-output"] }),
  };
  return appendFailure(folder, rec);
}

function writeInsight(ids: string[] = [first], name = "runs/test/insight.md"): string {
  writeFile(name, [
    "# Insight", `## ${ids.join(", ")}`, "Whys:",
    "1. The call produced no answer.", "2. Its result was not checked.", "3. The instruction omitted the result check.",
    "Source: instruction", "Root cause: the instruction omitted the result check", "Options:",
    "1. [rule] require a result check; evidence: runs/test/result.md",
    "2. [check] reject an empty answer; evidence: runs/test/check.md", "",
  ].join("\n"));
  return name;
}

function register(): Register {
  const r: Register = {
    register: 1,
    use_cases: [{ id: "UC1", origin: "user", purpose: "preserve work", fails_if: ["work is lost"], min_acceptance: ["work reopens"] }],
    coverage: [
      { unit: "UC1/f1", covered_by: ["test/save.test.ts"] },
      { unit: "UC1/m1", covered_by: ["test/open.test.ts"] },
    ],
  };
  r.frozen = freezeHash(units(r));
  return r;
}

function touch(name: string, tool = "Write", session = "session-a"): HookResult {
  return handleHook({ hook_event_name: "PostToolUse", session_id: session, tool_name: tool, tool_input: { file_path: name } }, env);
}

function expectQuiet(result: HookResult): void {
  expect(result).toEqual({ exitCode: 0, stdout: "", stderr: "" });
}

function blockReason(result: HookResult): string {
  expect(result.exitCode).toBe(0);
  expect(result.stderr).toBe("");
  const output = JSON.parse(result.stdout);
  expect(output.decision).toBe("block");
  expect(typeof output.reason).toBe("string");
  expect(output.reason.trim().length).toBeGreaterThan(0);
  return output.reason;
}

function failures(): FailureRecord[] {
  return readJournal(folder).records.filter((r): r is FailureRecord => r.kind === "failure");
}

function expectEvidence(rec: FailureRecord): Record<string, unknown> {
  expect(validateFailure(rec, folder)).toEqual([]);
  const file = path.resolve(folder, rec.evidence);
  expect(fs.existsSync(file)).toBe(true);
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function expectNoSecret(action: () => unknown): unknown {
  const printed: string[] = [];
  const spies = [
    spyOn(console, "log").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
    spyOn(console, "warn").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
    spyOn(console, "error").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
    spyOn(process.stdout, "write").mockImplementation((chunk) => { printed.push(String(chunk)); return true; }),
    spyOn(process.stderr, "write").mockImplementation((chunk) => { printed.push(String(chunk)); return true; }),
  ];
  let output: unknown;
  try { output = action(); } finally { for (const spy of spies) spy.mockRestore(); }
  expect(JSON.stringify(output)).not.toContain(secret);
  expect(printed.join("\n")).not.toContain(secret);
  const state = path.join(folder, ".harness-guard");
  if (fs.existsSync(state)) {
    for (const name of fs.readdirSync(state, { recursive: true, encoding: "utf8" })) {
      const file = path.join(state, name);
      expect(name).not.toContain(secret);
      if (fs.statSync(file).isFile()) expect(fs.readFileSync(file, "utf8")).not.toContain(secret);
    }
  }
  return output;
}

describe("PreToolUse", () => {
  test.each([
    ["codex exec 'answer the task'", "trap:codex-stdin"],
    ["opencode run 'answer the task' &", "trap:opencode-parallel"],
    ["opencode run /outside-hg-repo/input.md", "trap:opencode-outside-repo"],
  ])("pre: %s is denied with its catalogued finding and fix", (command: string, rule: string) => {
    const result: HookResult = handleHook(bash("PreToolUse", command), env);
    expect(result.exitCode).toBe(0);
    expect(result.stderr).toBe("");
    const output = JSON.parse(result.stdout).hookSpecificOutput;
    expect(output.hookEventName).toBe("PreToolUse");
    expect(output.permissionDecision).toBe("deny");
    const finding = lintCommand(command, { repoRoot: folder, running: [] }).find((f) => f.rule === rule)!;
    expect(finding).toBeDefined();
    expect(output.permissionDecisionReason).toContain(`${rule}: ${finding.message} Fix: ${finding.fix}`);
    // Round 5 S1 (COO): a passing call now writes a success line — only failures must be absent.
    expect(readJournal(folder).records.filter((r) => r.kind !== "success")).toEqual([]);
  });

  test("pre: every hit is included when one command triggers multiple traps", () => {
    const result = handleHook(bash("PreToolUse", "codex exec task; opencode run /outside-hg-repo/input.md &"), env);
    const reason = JSON.parse(result.stdout).hookSpecificOutput.permissionDecisionReason;
    for (const rule of ["trap:codex-stdin", "trap:opencode-parallel", "trap:opencode-outside-repo"]) expect(reason).toContain(rule);
  });

  test("pre: the supplied running processes deny a concurrent opencode call", () => {
    env.running = ["opencode run another-task"];
    const output = JSON.parse(handleHook(bash("PreToolUse", "opencode run task"), env).stdout).hookSpecificOutput;
    expect(output.permissionDecision).toBe("deny");
    expect(output.permissionDecisionReason).toContain("trap:opencode-parallel");
  });

  test.each(["echo clean", "codex exec task </dev/null", "codex exec --help", "echo 'codex exec task'", "opencode run task", "agy -p task --mode plan"])(
    "pre: clean or proposed-only command %s is allowed without output",
    (command: string) => { expectQuiet(handleHook(bash("PreToolUse", command), env)); },
  );

  test("pre: a non-Bash tool does not lint a command-shaped field", () => {
    expectQuiet(handleHook({ ...bash("PreToolUse", "codex exec task"), tool_name: "Read" }, env));
  });

  test("pre: prompt text never appears in a deny response or guard state", () => {
    expectNoSecret(() => handleHook(bash("PreToolUse", `codex exec '${secret}'`), env));
  });
});

describe("PostToolUse", () => {
  test.each(["", " \t\n"])("post: an empty output file %j logs a valid failure with evidence and context", (text: string) => {
    writeFile("answer.md", text);
    const result = handleHook(bash("PostToolUse", "codex exec task -o answer.md </dev/null"), env);
    expect(result.exitCode).toBe(0);
    expect(result.stderr).toBe("");
    const records = failures();
    expect(records).toHaveLength(1);
    const rec = records[0]!;
    expect(rec).toMatchObject({
      kind: "failure", time, session: "session-a", found_by: "guard", harness: "claude-code",
      engine: "codex", check: "R12.1-empty-output",
    });
    expect(rec.id).toMatch(/^F-[0-9a-f]{8}$/);
    expect(rec.input).toContain("codex");
    expect(rec.input).toContain("answer.md");
    expectEvidence(rec);
    const output = JSON.parse(result.stdout).hookSpecificOutput;
    expect(output.hookEventName).toBe("PostToolUse");
    // Round 3 C23: the line says the failure is already logged, so the agent does not log it again.
    expect(output.additionalContext).toContain(`harness-guard logged ${rec.id} — already in the journal; do not log them again.`);
    expect(output.additionalContext).toContain("insight");
  });

  test("post: a missing output file is a recorded failure", () => {
    handleHook(bash("PostToolUse", "codex exec task -o missing.md </dev/null"), env);
    expect(failures()).toHaveLength(1);
    expect(failures()[0]!.check).toBe("R12.1-missing-output");
    expectEvidence(failures()[0]!);
  });

  test("post: every fail finding becomes its own record and evidence file", () => {
    const result = handleHook(bash("PostToolUse", "dsh headless task", { interrupted: true }), env);
    const records = failures();
    expect(records).toHaveLength(2);
    expect(records.map((r) => r.check).sort()).toEqual(["R12.1-empty-output", "R12.1-interrupted"]);
    expect(new Set(records.map((r) => r.id)).size).toBe(2);
    expect(new Set(records.map((r) => r.evidence)).size).toBe(2);
    const context = JSON.parse(result.stdout).hookSpecificOutput.additionalContext;
    // Round 3 C23: ids only, and the line says they are already in the journal.
    expect(context).toContain("already in the journal; do not log them again.");
    for (const rec of records) {
      expectEvidence(rec);
      expect(context).toContain(rec.id);
    }
  });

  test.each(["dsh headless task", "opencode run task"])("post: %s with whitespace stdout records an empty answer", (command: string) => {
    handleHook(bash("PostToolUse", command, { stdout: " \n\t" }), env);
    expect(failures().map((r) => r.check)).toEqual(["R12.1-empty-output"]);
  });

  test("post: an agy soft denial is recorded even with non-empty stdout", () => {
    handleHook(bash("PostToolUse", "agy -p task", { stdout: "partial answer", stderr: "soft-denied" }), env);
    expect(failures().map((r) => r.check)).toEqual(["trap:agy-soft-deny"]);
  });

  test("post: a successful file answer writes no record and returns no output", () => {
    writeFile("answer.md", "the answer\n");
    expectQuiet(handleHook(bash("PostToolUse", "codex exec task -o answer.md </dev/null"), env));
    // Round 5 S1 (COO): a passing call now writes a success line — only failures must be absent.
    expect(readJournal(folder).records.filter((r) => r.kind !== "success")).toEqual([]);
  });

  test("post: a successful stdout answer writes no record", () => {
    expectQuiet(handleHook(bash("PostToolUse", "dsh headless task", { stdout: "the answer" }), env));
    // Round 5 S1 (COO): a passing call now writes a success line — only failures must be absent.
    expect(readJournal(folder).records.filter((r) => r.kind !== "success")).toEqual([]);
  });

  test("post: a successful event does not use an exit field as a tool failure", () => {
    expectQuiet(handleHook(bash("PostToolUse", "dsh headless task", { stdout: "answer", exit_code: 7 }), env));
    expect(failures()).toEqual([]);
  });

  test("post: a non-engine Bash command writes no failure", () => {
    expectQuiet(handleHook(bash("PostToolUse", "echo 'codex exec task'"), env));
    // Round 5 S1 (COO): a passing call now writes a success line — only failures must be absent.
    expect(readJournal(folder).records.filter((r) => r.kind !== "success")).toEqual([]);
  });

  test("post: nested cwd uses the git root for state and resolves engine outputs against cwd", () => {
    execFileSync("git", ["init", "--quiet", folder], { cwd: folder });
    const nested = path.join(folder, "nested");
    fs.mkdirSync(nested);
    env.cwd = nested;
    writeFile("nested/answer.md", "answer");
    expectQuiet(handleHook(bash("PostToolUse", "codex exec task -o answer.md </dev/null"), env));
    writeFile("nested/answer.md", "");
    handleHook(bash("PostToolUse", "codex exec task -o answer.md </dev/null"), env);
    expect(failures()).toHaveLength(1);
    expectEvidence(failures()[0]!);
    expect(fs.existsSync(path.join(nested, ".harness-guard"))).toBe(false);
  });

  test("post: raw prompts, stdout, stderr and config never reach guard output, journal or evidence", () => {
    const payload = bash("PostToolUse", `codex exec '${secret}' -o missing.md </dev/null`, {
      stdout: secret, stderr: secret, config: { token: secret },
    });
    expectNoSecret(() => handleHook(payload, env));
    expect(failures()).toHaveLength(1);
    const facts = expectEvidence(failures()[0]!);
    const text = JSON.stringify(facts);
    expect(text).toContain("R12.1-missing-output");
    const values: unknown[] = [];
    JSON.stringify(facts, (_key, value: unknown) => {
      if (value === null || typeof value === "number") values.push(value);
      return value;
    });
    expect(values).toContain(secret.length);
    expect(values).toContain(null);
  });
});

describe("PostToolUseFailure", () => {
  test.each(["exit_code", "exitCode"])("failure: numeric %s becomes the result exit code", (key: string) => {
    handleHook(bash("PostToolUseFailure", "dsh headless task", { stdout: "answer", [key]: 7 }), env);
    expect(failures().map((r) => r.check)).toEqual(["R12.1-exit"]);
    expectEvidence(failures()[0]!);
  });

  test.each([undefined, "0", null])("failure: nonnumeric or absent exit %j defaults to one", (exit) => {
    handleHook(bash("PostToolUseFailure", "dsh headless task", { stdout: "answer", exit_code: exit }), env);
    expect(failures().map((r) => r.check)).toEqual(["R12.1-exit"]);
  });

  test("failure: numeric zero is used rather than replaced by the default", () => {
    expectQuiet(handleHook(bash("PostToolUseFailure", "dsh headless task", { stdout: "answer", exit_code: 0 }), env));
    expect(failures()).toEqual([]);
  });

  test("failure: exit 124 records a timeout rather than a generic exit failure", () => {
    handleHook(bash("PostToolUseFailure", "dsh headless task", { stdout: "answer", exit_code: 124 }), env);
    expect(failures().map((r) => r.check)).toEqual(["R12.1-timeout"]);
  });

  test("failure: a string error is used as stderr for result traps", () => {
    handleHook(bash("PostToolUseFailure", "agy -p task", { stdout: "partial", exitCode: 0, error: "soft-denied" }), env);
    expect(failures().map((r) => r.check)).toEqual(["trap:agy-soft-deny"]);
  });

  test("failure: a tool error containing a secret is reduced to safe facts", () => {
    expectNoSecret(() => handleHook(bash("PostToolUseFailure", `agy -p '${secret}'`, {
      stdout: secret, error: `soft-denied ${secret}`,
    }), env));
    expect(failures().length).toBeGreaterThan(0);
    for (const rec of failures()) expectEvidence(rec);
  });
});

describe("register touches and Stop", () => {
  test.each(["Write", "Edit", "MultiEdit"])("touch: %s appends a session-scoped root-relative touched record", (tool: string) => {
    const name = "docs/cases.register.yaml";
    writeFile(name, JSON.stringify(register()));
    expectQuiet(touch(path.join(folder, name), tool));
    const records: TouchedRecord[] = readJournal(folder).records.filter((r): r is TouchedRecord => r.kind === "touched");
    expect(records).toEqual([{ kind: "touched", time, session: "session-a", path: name }]);
  });

  test("touch: register.yaml is a register file", () => {
    writeFile("register.yaml", JSON.stringify(register()));
    expectQuiet(touch(path.join(folder, "register.yaml")));
    expect(readJournal(folder).records).toContainEqual(expect.objectContaining({ kind: "touched", path: "register.yaml" }));
  });

  test.each([["Write", "notes.md"], ["Read", "cases.register.yaml"], ["Bash", "cases.register.yaml"]])(
    "touch: %s on %s does not append a touched record",
    (tool: string, file: string) => { expectQuiet(touch(file, tool)); // Round 5 S1 (COO): a passing call now writes a success line — only failures must be absent.
    expect(readJournal(folder).records.filter((r) => r.kind !== "success")).toEqual([]); },
  );

  test.each(["Stop", "SubagentStop"])("stop: %s permits a session with no failures", (event: string) => {
    expectQuiet(handleHook(stop(event), env));
  });

  test.each(["Stop", "SubagentStop"])("stop: %s blocks every unanswered id and describes the insight format", (event: string) => {
    seedFailure(first);
    seedFailure(second);
    const reason = blockReason(handleHook(stop(event), env));
    for (const text of [first, second, "Whys", "Source", "Root cause", "Options", "evidence"]) expect(reason).toContain(text);
    expect(reason).toMatch(/heading|##/i);
    expect(reason).toMatch(/3\s*[-–—]\s*6/);
    expect(reason).toMatch(/2\s*[-–—]\s*3/);
    expect(reason).toMatch(/kind|\[rule\]/i);
  });

  test.each([true, false])("stop: stop_hook_active=%j never bypasses an open failure", (active: boolean) => {
    seedFailure();
    for (let attempt = 0; attempt < 3; attempt++) {
      expect(blockReason(handleHook(stop("Stop", { stop_hook_active: active }), env))).toContain(first);
    }
  });

  test("stop: failures from another session do not block this one", () => {
    seedFailure(first, "session-b");
    expectQuiet(handleHook(stop(), env));
  });

  test("stop: a valid insight must be named in the final message", () => {
    seedFailure();
    const name = writeInsight();
    const reason = blockReason(handleHook(stop("Stop", { last_assistant_message: "work finished" }), env));
    expect(reason).toContain(`raise the insight: name ${name} in your final message`);
    expectQuiet(handleHook(stop("Stop", { last_assistant_message: `See ${name} for the insight.` }), env));
  });

  test("stop: naming an invalid insight does not answer a failure", () => {
    seedFailure();
    const name = "runs/test/insight-invalid.md";
    writeFile(name, `## ${first}\nWhys:\n1. only one why\n`);
    expect(blockReason(handleHook(stop("Stop", { last_assistant_message: name }), env))).toContain(first);
  });

  test("stop: one valid section can answer two failures and its named path permits Stop", () => {
    seedFailure(first);
    seedFailure(second);
    const name = writeInsight([first, second]);
    expectQuiet(handleHook(stop("Stop", { last_assistant_message: name }), env));
  });

  test("stop: a touched register with a validation failure blocks", () => {
    const r = register();
    r.use_cases![0]!.origin = "ai";
    writeFile("cases.register.yaml", JSON.stringify(r));
    touch("cases.register.yaml");
    expect(blockReason(handleHook(stop(), env))).toContain("R13.1-no-decision");
  });

  test("stop: a touched register with a coverage failure blocks", () => {
    const r = register();
    r.coverage = [];
    writeFile("cases.register.yaml", JSON.stringify(r));
    touch("cases.register.yaml");
    expect(blockReason(handleHook(stop(), env))).toContain("R11.1-basic-uncovered");
  });

  test("stop: every register touched by this session is checked", () => {
    writeFile("good.register.yaml", JSON.stringify(register()));
    const invalid = register();
    delete invalid.frozen;
    writeFile("bad.register.yaml", JSON.stringify(invalid));
    touch("good.register.yaml");
    touch("bad.register.yaml");
    expect(blockReason(handleHook(stop(), env))).toContain("R11.1-not-frozen");
  });

  test("stop: valid registers and warnings alone do not block", () => {
    const r = register();
    r.coverage![1] = { unit: "UC1/m1", skippable: { reason: "owner deferred it" } };
    writeFile("cases.register.yaml", JSON.stringify(r));
    touch("cases.register.yaml");
    expectQuiet(handleHook(stop(), env));
  });

  test("stop: an invalid register touched only by another session does not block", () => {
    writeFile("cases.register.yaml", JSON.stringify({ register: 1 }));
    touch("cases.register.yaml", "Edit", "session-b");
    expectQuiet(handleHook(stop(), env));
  });

  test("stop: invalid untouched registers do not block", () => {
    writeFile("cases.register.yaml", JSON.stringify({ register: 1 }));
    expectQuiet(handleHook(stop(), env));
  });

  test("stop: raw register fields never appear in a blocking reason", () => {
    const r = register();
    r.use_cases![0]!.purpose = secret;
    r.use_cases![0]!.fails_if = [secret];
    r.coverage = [];
    writeFile("cases.register.yaml", JSON.stringify(r));
    expectNoSecret(() => {
      touch("cases.register.yaml");
      const result = handleHook(stop(), env);
      blockReason(result);
      return result;
    });
  });
});

describe("SessionStart and handler errors", () => {
  test("start: other sessions' open failures are raised as additional context", () => {
    seedFailure(first, "session-b");
    seedFailure(second, "session-a");
    const result = handleHook({ hook_event_name: "SessionStart", session_id: "session-a" }, env);
    expect(result.exitCode).toBe(0);
    expect(result.stderr).toBe("");
    const context = JSON.parse(result.stdout).hookSpecificOutput.additionalContext;
    expect(context).toContain(first);
    expect(context).not.toContain(second);
  });

  test("start: answered failures in other sessions produce no context", () => {
    seedFailure(first, "session-b");
    writeInsight();
    expectQuiet(handleHook({ hook_event_name: "SessionStart", session_id: "session-a" }, env));
  });

  test("start: this session's open failures alone produce no context", () => {
    seedFailure();
    expectQuiet(handleHook({ hook_event_name: "SessionStart", session_id: "session-a" }, env));
  });

  test.each([[null], [false], [0], ["payload"], [[]], [{}], [{ hook_event_name: "Unknown" }]])(
    "dispatch: unsupported payload %j is a quiet success",
    (payload: unknown) => { expectQuiet(handleHook(payload, env)); },
  );

  test("error: an internal exception returns exit one, one stderr line and a guard_error record", () => {
    const payload = { hook_event_name: "PreToolUse", session_id: "session-a", tool_name: "Bash",
      get tool_input(): never { throw new Error(`broken input ${secret}\nsecond line`); } };
    const result = expectNoSecret(() => handleHook(payload, env)) as HookResult;
    expect(result.exitCode).toBe(1);
    expect(result.stderr.trim().length).toBeGreaterThan(0);
    expect(result.stderr.trim().split(/\r?\n/)).toHaveLength(1);
    const records: GuardErrorRecord[] = readJournal(folder).records.filter((r): r is GuardErrorRecord => r.kind === "guard_error");
    expect(records).toHaveLength(1);
    expect(records[0]).toMatchObject({ kind: "guard_error", time, session: "session-a" });
    expect(records[0]!.message.trim().length).toBeGreaterThan(0);
  });

  test("error: an unwritable journal cannot escape the handler's best-effort error reporting", () => {
    writeFile(".harness-guard", "blocks directory creation");
    const result = handleHook(bash("PostToolUse", "dsh headless task"), env);
    expect(result.exitCode).toBe(1);
    expect(result.stderr.trim().length).toBeGreaterThan(0);
    expect(result.stderr.trim().split(/\r?\n/)).toHaveLength(1);
  });
});
