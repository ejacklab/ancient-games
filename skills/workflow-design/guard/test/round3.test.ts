// Round 3 (SPEC.md "Round 3 — changes from the review and the measurements"): one describe block per item C1–C23.
// Inputs reuse the failing inputs of runs/20261015-ts-hybrid/nodes/review-1.result.md (R# = its row) and the E1/E2/E4
// measurements. Expectations come from SPEC.md only.
import { afterEach, beforeEach, describe, expect, spyOn, test } from "bun:test";
import { type ChildProcess, execFileSync, spawn, spawnSync } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { doctor } from "../src/doctor.ts";
import { handleHook } from "../src/hooks.ts";
import { answered, checkSection, findInsightFiles, openFailures, parseInsight } from "../src/insight.ts";
import { installSnippet } from "../src/install.ts";
import { appendFailure, appendRecord, readJournal, recordFailureFromArgs, validateFailure, writeEvidence } from "../src/journal.ts";
import { coverage, loadRegister, validateRegister } from "../src/register.ts";
import { checkResult, lintCommand, recognizeEngineCall, segments } from "../src/traps.ts";
import type { DoctorReport, EngineCall, FailureRecord, Finding, GuardErrorRecord, HookEnv, HookResult, Register } from "../src/types.ts";

const secret = "SECRET-PLANT-7f3a9c";
const time = "2026-10-15T08:00:00.000Z";
const cli = path.resolve(import.meta.dir, "../src/cli.ts");
const packageDir = path.resolve(import.meta.dir, "..");
const contextLine = "already in the journal; do not log them again. An insight answering them is required before you stop.";
let folder: string;
let env: HookEnv;

beforeEach(() => {
  folder = fs.mkdtempSync(path.join(os.tmpdir(), "hg-"));
  env = { cwd: folder, running: [], now: () => new Date(time) };
});

afterEach(() => {
  fs.rmSync(folder, { recursive: true, force: true });
});

// ---- helpers ----------------------------------------------------------------------------------------------------

function writeFile(name: string, text: string): string {
  const file = path.join(folder, name);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, text);
  return file;
}

function gitInit(): void {
  execFileSync("git", ["init", "--quiet", folder], { cwd: folder });
}

interface PostOptions {
  input?: Record<string, unknown>;
  response?: Record<string, unknown>;
  payload?: Record<string, unknown>;
  session?: string;
}

function post(event: "PostToolUse" | "PostToolUseFailure", command: string, options: PostOptions = {}): Record<string, unknown> {
  return {
    hook_event_name: event,
    session_id: options.session ?? "session-a",
    tool_name: "Bash",
    tool_input: { command, ...options.input },
    tool_response: { stdout: "", stderr: "", interrupted: false, ...options.response },
    ...options.payload,
  };
}

function pre(command: string): Record<string, unknown> {
  return { hook_event_name: "PreToolUse", session_id: "session-a", tool_name: "Bash", tool_input: { command } };
}

function stop(changes: Record<string, unknown> = {}): Record<string, unknown> {
  return { hook_event_name: "Stop", session_id: "session-a", stop_hook_active: false, ...changes };
}

function failures(root = folder): FailureRecord[] {
  return readJournal(root).records.filter((r): r is FailureRecord => r.kind === "failure");
}

function guardErrors(root = folder): GuardErrorRecord[] {
  return readJournal(root).records.filter((r): r is GuardErrorRecord => r.kind === "guard_error");
}

function expectQuiet(result: HookResult): void {
  expect(result).toEqual({ exitCode: 0, stdout: "", stderr: "" });
}

function blockReason(result: HookResult): string {
  expect(result.exitCode).toBe(0);
  expect(result.stderr).toBe("");
  const output = JSON.parse(result.stdout);
  expect(output.decision).toBe("block");
  return String(output.reason);
}

function expectFailure(findings: Finding[], rule: string): void {
  expect(findings).toContainEqual(expect.objectContaining({ rule, severity: "fail" }));
}

function rules(findings: Finding[]): string[] {
  return findings.map((finding) => finding.rule);
}

function call(changes: Partial<EngineCall> = {}): EngineCall {
  return { engine: "codex", outputFile: null, stdoutIsAnswer: false, statusFile: null, background: false, ...changes };
}

// Every printed byte, the returned value, and every file under .harness-guard/ must be free of the planted secret.
function expectNoSecret<T>(action: () => T, root = folder): T {
  const printed: string[] = [];
  const spies = [
    spyOn(console, "log").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
    spyOn(console, "warn").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
    spyOn(console, "error").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
    spyOn(process.stdout, "write").mockImplementation((chunk) => { printed.push(String(chunk)); return true; }),
    spyOn(process.stderr, "write").mockImplementation((chunk) => { printed.push(String(chunk)); return true; }),
  ];
  let output: T;
  try { output = action(); } finally { for (const spy of spies) spy.mockRestore(); }
  expect(JSON.stringify(output)).not.toContain(secret);
  expect(printed.join("\n")).not.toContain(secret);
  const state = path.join(root, ".harness-guard");
  if (fs.existsSync(state)) {
    for (const name of fs.readdirSync(state, { recursive: true, encoding: "utf8" })) {
      const file = path.join(state, name);
      expect(name).not.toContain(secret);
      if (fs.statSync(file).isFile()) expect(fs.readFileSync(file, "utf8")).not.toContain(secret);
    }
  }
  return output;
}

// The `input` of a guard-found record holds "<engine> call" and at most the output file's basename.
function expectInput(rec: FailureRecord, engine: string, basename: string | null): void {
  expect(rec.input.startsWith(`${engine} call`)).toBe(true);
  let rest = rec.input.slice(`${engine} call`.length);
  if (basename !== null) {
    expect(rest).toContain(basename);
    rest = rest.replace(basename, "");
  }
  expect(rest.replace(/[\s:,;()"'—–-]/g, "")).toBe("");
}

function seedFailure(id: string, session = "session-a", root = folder): FailureRecord {
  return appendFailure(root, {
    kind: "failure", id, time, session, found_by: "guard", check: "R12.1-empty-output",
    input: "codex call answer.md", expected: "non-empty output", actual: "empty output",
    engine: "codex", harness: "claude-code", reason: "the output file is empty",
    evidence: writeEvidence(root, id, { stdoutLength: 0, rules: ["R12.1-empty-output"] }),
  });
}

interface SectionParts {
  whys?: string;
  source?: string;
  options?: string;
}

const threeWhys = "1. The call produced no answer.\n2. Its result was not checked.\n3. The instruction omitted the result check.";
const twoOptions = "1. [rule] require a result check; evidence: runs/test/result.md\n2. [check] reject an empty answer; evidence: runs/test/check.md";

function insightText(ids: string[], parts: SectionParts = {}): string {
  return [
    "# Insight", "", `## ${ids.join(", ")}`, "",
    "Whys:", parts.whys ?? threeWhys, "",
    `Source: ${parts.source ?? "instruction"}`, "",
    "Root cause: the instruction omitted the result check", "",
    "Options:", parts.options ?? twoOptions, "",
  ].join("\n");
}

function runCli(args: string[], input = "", cwd = folder) {
  const result = spawnSync(process.execPath, [cli, ...args], { cwd, input, encoding: "utf8", timeout: 15000 });
  expect(result.error).toBeUndefined();
  return { exitCode: result.status, stdout: result.stdout, stderr: result.stderr };
}

// ---- C1 ---------------------------------------------------------------------------------------------------------

describe("C1 (R1) background calls are not checked on return", () => {
  test("C1: a codex call backgrounded with & writes no record and no output (R1 input)", () => {
    expectQuiet(handleHook(post("PostToolUse", 'codex exec "x" -o bg.md </dev/null &'), env));
    // Round 5 S1 (COO): a passing call now writes a success line — only failures must be absent.
    expect(readJournal(folder).records.filter((r) => r.kind !== "success")).toEqual([]);
  });

  test("C1: a call inside a backgrounded group writes no record", () => {
    expectQuiet(handleHook(post("PostToolUse", '(codex exec "x" -o bg.md </dev/null) &'), env));
    // Round 5 S1 (COO): a passing call now writes a success line — only failures must be absent.
    expect(readJournal(folder).records.filter((r) => r.kind !== "success")).toEqual([]);
  });

  test("C1: run_in_background with a backgroundTaskId response writes no record (R1 input)", () => {
    const payload = post("PostToolUse", 'opencode run "review the diff"', {
      input: { run_in_background: true }, response: { stdout: "", backgroundTaskId: "b1" },
    });
    expectQuiet(handleHook(payload, env));
    // Round 5 S1 (COO): a passing call now writes a success line — only failures must be absent.
    expect(readJournal(folder).records.filter((r) => r.kind !== "success")).toEqual([]);
  });

  test("C1: tool_input.run_in_background alone skips the check", () => {
    expectQuiet(handleHook(post("PostToolUse", 'opencode run "review the diff"', { input: { run_in_background: true } }), env));
    // Round 5 S1 (COO): a passing call now writes a success line — only failures must be absent.
    expect(readJournal(folder).records.filter((r) => r.kind !== "success")).toEqual([]);
  });

  test("C1: tool_response.backgroundTaskId alone skips the check", () => {
    expectQuiet(handleHook(post("PostToolUse", 'opencode run "review the diff"', { response: { backgroundTaskId: "b1" } }), env));
    // Round 5 S1 (COO): a passing call now writes a success line — only failures must be absent.
    expect(readJournal(folder).records.filter((r) => r.kind !== "success")).toEqual([]);
  });

  test("C1: PostToolUseFailure of a backgrounded call writes no record", () => {
    const payload = post("PostToolUseFailure", 'codex exec "x" -o bg.md </dev/null &', { payload: { exit_code: 1 }, response: { exit_code: 1 } });
    expectQuiet(handleHook(payload, env));
    // Round 5 S1 (COO): a passing call now writes a success line — only failures must be absent.
    expect(readJournal(folder).records.filter((r) => r.kind !== "success")).toEqual([]);
  });

  test("C1 control: the same call in the foreground is still checked", () => {
    handleHook(post("PostToolUse", 'codex exec "x" -o bg.md </dev/null'), env);
    expect(failures().map((r) => r.check)).toEqual(["R12.1-missing-output"]);
    handleHook(post("PostToolUse", 'opencode run "review the diff"', { input: { run_in_background: false } }), env);
    expect(failures().map((r) => r.check)).toContain("R12.1-empty-output");
  });
});

// ---- C2 ---------------------------------------------------------------------------------------------------------

describe("C2 (R2) output flags and > are read outside quotes only", () => {
  test.each([
    ['opencode run "use key > sk-live-ABC123"'],
    ["opencode run 'use key > sk-live-ABC123'"],
    ['opencode run "use key >> sk-live-ABC123"'],
  ])("C2: a > inside the quoted prompt of %s is prompt text, not an output file", (command: string) => {
    expect(recognizeEngineCall(command)).toEqual(call({ engine: "opencode", stdoutIsAnswer: true }));
  });

  test.each([
    ['codex exec "explain why -o mytoken matters" </dev/null'],
    ["codex exec 'explain why -o mytoken matters' </dev/null"],
    ['codex exec "explain --output-last-message=mytoken" </dev/null'],
  ])("C2: an output flag inside the quoted prompt of %s is prompt text", (command: string) => {
    expect(recognizeEngineCall(command)?.outputFile).toBeNull();
  });

  test("C2: an unquoted -o after a quoted prompt holding -o is the output file", () => {
    expect(recognizeEngineCall('codex exec "explain why -o mytoken matters" -o answer.md </dev/null')?.outputFile).toBe("answer.md");
  });

  test("C2: an unquoted > after a quoted prompt holding > is the output file", () => {
    expect(recognizeEngineCall('opencode run "use key > sk-live" > answer.md')).toEqual(
      call({ engine: "opencode", outputFile: "answer.md", stdoutIsAnswer: false }),
    );
  });

  test("C2: a > inside the quoted prompt with a good stdout answer writes no record (R2 input)", () => {
    expectQuiet(handleHook(post("PostToolUse", `opencode run "use key > ${secret}"`, { response: { stdout: "a full answer" } }), env));
    // Round 5 S1 (COO): a passing call now writes a success line — only failures must be absent.
    expect(readJournal(folder).records.filter((r) => r.kind !== "success")).toEqual([]);
  });

  test("C2: the planted secret after > inside quotes never reaches the journal, evidence or hook output", () => {
    const result = expectNoSecret(() => handleHook(post("PostToolUse", `opencode run "use key > ${secret}"`), env));
    const records = failures();
    expect(records.map((r) => r.check)).toEqual(["R12.1-empty-output"]);
    expectInput(records[0]!, "opencode", null);
    expect(records[0]!.input).toBe("opencode call");
    expect(JSON.parse(result.stdout).hookSpecificOutput.additionalContext).toContain(records[0]!.id);
  });

  test("C2: the planted secret after -o inside quotes never reaches the journal, evidence or hook output", () => {
    expectNoSecret(() => handleHook(post("PostToolUse", `codex exec "explain why -o ${secret} matters" -o missing.md </dev/null`), env));
    const records = failures();
    expect(records.map((r) => r.check)).toEqual(["R12.1-missing-output"]);
    expectInput(records[0]!, "codex", "missing.md");
  });

  test("C2: the planted secret after -o inside quotes with no real output flag writes nothing", () => {
    expectNoSecret(() => handleHook(post("PostToolUse", `codex exec "explain why -o ${secret} matters" </dev/null`), env));
    expect(failures()).toEqual([]);
  });

  test("C2: PostToolUseFailure with the secret after > inside quotes keeps it out of every guard file", () => {
    expectNoSecret(() => handleHook(post("PostToolUseFailure", `opencode run "use key > ${secret}"`, {
      payload: { exit_code: 3 }, response: { stdout: "partial" },
    }), env));
    const records = failures();
    expect(records.length).toBeGreaterThan(0);
    for (const rec of records) expectInput(rec, "opencode", null);
  });

  test("C2: input holds only the output file's basename, never its folders", () => {
    handleHook(post("PostToolUse", "codex exec task -o nested/deeper/answer.md </dev/null"), env);
    const rec = failures()[0]!;
    expectInput(rec, "codex", "answer.md");
    expect(rec.input).not.toContain("nested");
    expect(rec.input).not.toContain("deeper");
    expect(rec.input).not.toContain("task");
  });
});

// ---- C3 ---------------------------------------------------------------------------------------------------------

describe("C3 (R5) the working folder of a call", () => {
  test("C3: cd sub && codex … -o out.md resolves out.md in sub (R5 input)", () => {
    gitInit();
    writeFile("sub/out.md", "real answer");
    expectQuiet(handleHook(post("PostToolUse", 'cd sub && codex exec "x" -o out.md </dev/null'), env));
    expect(failures()).toEqual([]);
  });

  test("C3: the cd'd folder is used, not env.cwd, when only env.cwd holds the file", () => {
    gitInit();
    writeFile("out.md", "an answer in the wrong folder");
    fs.mkdirSync(path.join(folder, "sub"));
    handleHook(post("PostToolUse", 'cd sub && codex exec "x" -o out.md </dev/null'), env);
    expect(failures().map((r) => r.check)).toEqual(["R12.1-missing-output"]);
  });

  test("C3: cd with ; and an absolute folder is followed", () => {
    gitInit();
    writeFile("abs/out.md", "real answer");
    expectQuiet(handleHook(post("PostToolUse", `cd ${path.join(folder, "abs")}; codex exec "x" -o out.md </dev/null`), env));
    expect(failures()).toEqual([]);
  });

  test("C3: payload.cwd is used when it is a string", () => {
    gitInit();
    writeFile("sub/out.md", "real answer");
    const payload = post("PostToolUse", 'codex exec "x" -o out.md </dev/null', { payload: { cwd: path.join(folder, "sub") } });
    expectQuiet(handleHook(payload, env));
    expect(failures()).toEqual([]);
  });

  test("C3: payload.cwd rather than env.cwd decides where a missing file is looked for", () => {
    gitInit();
    writeFile("out.md", "an answer in env.cwd");
    fs.mkdirSync(path.join(folder, "sub"));
    handleHook(post("PostToolUse", 'codex exec "x" -o out.md </dev/null', { payload: { cwd: path.join(folder, "sub") } }), env);
    expect(failures().map((r) => r.check)).toEqual(["R12.1-missing-output"]);
  });

  test("C3: a relative cd is resolved against payload.cwd", () => {
    gitInit();
    writeFile("sub/deeper/out.md", "real answer");
    const payload = post("PostToolUse", 'cd deeper && codex exec "x" -o out.md </dev/null', { payload: { cwd: path.join(folder, "sub") } });
    expectQuiet(handleHook(payload, env));
    expect(failures()).toEqual([]);
  });

  test("C3: a payload.cwd that is not a string falls back to env.cwd", () => {
    gitInit();
    writeFile("out.md", "real answer");
    expectQuiet(handleHook(post("PostToolUse", 'codex exec "x" -o out.md </dev/null', { payload: { cwd: 42 } }), env));
    expect(failures()).toEqual([]);
  });

  test("C3: PostToolUseFailure resolves the output against the cd'd folder too", () => {
    gitInit();
    writeFile("sub/out.md", "real answer");
    handleHook(post("PostToolUseFailure", 'cd sub && codex exec "x" -o out.md </dev/null', { payload: { exit_code: 1 }, response: { exit_code: 1 } }), env);
    expect(failures().map((r) => r.check)).not.toContain("R12.1-missing-output");
  });
});

// ---- C4 ---------------------------------------------------------------------------------------------------------

describe("C4 (R20) a failure exit belongs to the engine only when it ends its pipeline", () => {
  function failure(command: string): HookResult {
    return handleHook(post("PostToolUseFailure", command, { payload: { exit_code: 1 }, response: { exit_code: 1 } }), env);
  }

  test.each([
    ['codex exec "x" -o a.md </dev/null | grep -q DONE'],
    ['codex exec "x" -o a.md </dev/null && false'],
    ['codex exec "x" -o a.md </dev/null || false'],
    ['codex exec "x" -o a.md </dev/null; false'],
  ])("C4: %s with a good output file writes no exit failure (R20 input)", (command: string) => {
    writeFile("a.md", "real answer");
    expectQuiet(failure(command));
    expect(failures()).toEqual([]);
  });

  test("C4: the output checks still run when the exit is not the engine's", () => {
    failure('codex exec "x" -o missing.md </dev/null | grep -q DONE');
    const checks = failures().map((r) => r.check);
    expect(checks).toContain("R12.1-missing-output");
    expect(checks).not.toContain("R12.1-exit");
  });

  test("C4: a stdout answer engine followed by a failing segment still has its stdout checked", () => {
    handleHook(post("PostToolUseFailure", 'dsh headless "task"; false', { payload: { exit_code: 1 }, response: { exit_code: 1, stdout: "" } }), env);
    const checks = failures().map((r) => r.check);
    expect(checks).toContain("R12.1-empty-output");
    expect(checks).not.toContain("R12.1-exit");
  });

  test.each([
    ['echo start && codex exec "x" -o a.md </dev/null'],
    ['printf task | codex exec - -o a.md'],
    ['codex exec "x" -o a.md </dev/null'],
  ])("C4 control: %s ends with the engine, so the exit is the engine's", (command: string) => {
    writeFile("a.md", "real answer");
    failure(command);
    expect(failures().map((r) => r.check)).toEqual(["R12.1-exit"]);
  });
});

// ---- C5 ---------------------------------------------------------------------------------------------------------

describe("C5 (R3) insight file locations", () => {
  test("C5: every *.md under .harness-guard/insights/ counts, whatever its name", () => {
    writeFile(".harness-guard/insights/F-218c4def.md", insightText(["F-218c4def"]));
    writeFile(".harness-guard/insights/notes.md", insightText(["F-218c4def"]));
    writeFile(".harness-guard/insights/insight-a.md", insightText(["F-218c4def"]));
    const found = findInsightFiles(folder);
    for (const name of ["F-218c4def.md", "notes.md", "insight-a.md"]) {
      expect(found).toContain(path.join(".harness-guard", "insights", name));
    }
  });

  test("C5: under runs/** only files named insight*.md count", () => {
    writeFile("runs/r1/insight.md", insightText(["F-218c4def"]));
    writeFile("runs/insight-top.md", insightText(["F-218c4def"]));
    writeFile("runs/r1/notes.md", insightText(["F-218c4def"]));
    writeFile("runs/r1/F-218c4def.md", insightText(["F-218c4def"]));
    expect(findInsightFiles(folder)).toEqual([path.join("runs", "insight-top.md"), path.join("runs", "r1", "insight.md")].sort());
  });

  test("C5: a valid section in .harness-guard/insights/F-218c4def.md answers the failure and lets Stop through (R3 input)", () => {
    seedFailure("F-218c4def", "s2");
    const name = path.join(".harness-guard", "insights", "F-218c4def.md");
    writeFile(name, insightText(["F-218c4def"]));
    expect(answered(folder).get("F-218c4def")).toBe(name);
    expect(openFailures(folder, "s2")).toEqual([]);
    expectQuiet(handleHook(stop({ session_id: "s2", last_assistant_message: `The insight is in ${name}.` }), env));
  });
});

// ---- C6 ---------------------------------------------------------------------------------------------------------

describe("C6 (R4) numbered lists in insight sections", () => {
  test("C6: blank lines after Whys: and Options: are skipped until the first item (R4 input)", () => {
    const text = [
      "## F-3c4d5e6f", "", "Whys:", "", "1. The call produced no answer.", "2. Its result was not checked.",
      "3. The instruction omitted the result check.", "", "Source: instruction", "",
      "Root cause: the instruction omitted the result check", "", "Options:", "", "",
      "1. [rule] require a result check; evidence: runs/test/result.md",
      "2. [check] reject an empty answer; evidence: runs/test/check.md", "",
    ].join("\n");
    const sections = parseInsight(text);
    expect(sections).toHaveLength(1);
    expect(sections[0]!.whys).toHaveLength(3);
    expect(sections[0]!.options).toHaveLength(2);
    expect(checkSection(sections[0]!).filter((f) => f.severity === "fail")).toEqual([]);
  });

  test("C6: a section with a blank line after Whys: answers its failure (R4: insight --session s3)", () => {
    seedFailure("F-3c4d5e6f", "s3");
    writeFile("runs/r3/insight.md", insightText(["F-3c4d5e6f"], { whys: `\n${threeWhys}`, options: `\n${twoOptions}` }));
    expect(openFailures(folder, "s3")).toEqual([]);
  });

  test("C6: an indented continuation line is joined to its item (R4 input)", () => {
    const whys = [
      "1. The call produced no answer because the engine",
      "   read stdin and waited until the timeout.",
      "2. Its result was not checked.",
      "3. The instruction omitted the result check.",
    ].join("\n");
    const sections = parseInsight(insightText(["F-3c4d5e6f"], { whys }));
    expect(sections[0]!.whys).toHaveLength(3);
    expect(sections[0]!.whys[0]).toContain("read stdin and waited until the timeout");
    expect(checkSection(sections[0]!).filter((f) => f.severity === "fail")).toEqual([]);
  });

  test("C6: an indented continuation of an option is joined, and its evidence on that line is read", () => {
    const options = [
      "1. [rule] require a result check",
      "   before the step ends; evidence: runs/test/result.md",
      "2. [check] reject an empty answer; evidence: runs/test/check.md",
    ].join("\n");
    const sections = parseInsight(insightText(["F-3c4d5e6f"], { options }));
    expect(sections[0]!.options).toHaveLength(2);
    expect(sections[0]!.options[0]!.kind).toBe("rule");
    expect(sections[0]!.options[0]!.evidence).toContain("runs/test/result.md");
    expect(checkSection(sections[0]!).filter((f) => f.severity === "fail")).toEqual([]);
  });

  test("C6: the list ends at the next unindented line that is not an item", () => {
    const whys = `${threeWhys}\nThese three are enough.\n4. an item after the list ended`;
    const sections = parseInsight(insightText(["F-3c4d5e6f"], { whys }));
    expect(sections[0]!.whys).toHaveLength(3);
  });

  test("C6: the list ends at the next label and at the next heading", () => {
    const text = [
      "## F-3c4d5e6f", "Whys:", threeWhys, "Source: instruction", "Root cause: the instruction omitted the check",
      "Options:", twoOptions, "## F-4d5e6f7a", "Whys:", threeWhys, "Source: tool", "Root cause: the tool hid it",
      "Options:", twoOptions, "",
    ].join("\n");
    const sections = parseInsight(text);
    expect(sections).toHaveLength(2);
    for (const section of sections) {
      expect(section.whys).toHaveLength(3);
      expect(section.options).toHaveLength(2);
      expect(checkSection(section).filter((f) => f.severity === "fail")).toEqual([]);
    }
    expect(sections[0]!.source).toBe("instruction");
  });
});

// ---- C7 ---------------------------------------------------------------------------------------------------------

describe("C7 (E4) Source: first word decides", () => {
  test.each([
    ["tool (the shim exits 0 with no output), with the instruction gap noted"],
    ["instruction — the brief never named the result check"],
    ["config: the hook was not installed"],
    ["check, because nothing read the output file"],
  ])("C7: Source: %s passes on its first word (E4 A2 shape)", (source: string) => {
    const sections = parseInsight(insightText(["F-5e6f7a8b"], { source }));
    expect(sections).toHaveLength(1);
    expect(rules(checkSection(sections[0]!))).not.toContain("R12.3-source");
  });

  test("C7: a failure answered by Source: tool (detail) is not open", () => {
    seedFailure("F-5e6f7a8b");
    writeFile("runs/r4/insight.md", insightText(["F-5e6f7a8b"], { source: "tool (the shim), with the instruction gap noted" }));
    expect(openFailures(folder, "session-a")).toEqual([]);
  });

  test.each([["toolbox"], ["config-advice"], ["policy tool"], ["the tool"]])(
    "C7: Source: %s fails because its first word is not one of the four",
    (source: string) => {
      const sections = parseInsight(insightText(["F-5e6f7a8b"], { source }));
      expectFailure(checkSection(sections[0]!), "R12.3-source");
    },
  );
});

// ---- C8 ---------------------------------------------------------------------------------------------------------

describe("C8 (R8) malformed register entries", () => {
  const r8 = "register: 1\nuse_cases:\n  -\n  - id: UC2\n    origin: ai\n";

  test("C8: an empty list item is R13-malformed naming its list and position, and the rest is still checked (R8 input)", () => {
    const r = loadRegister(writeFile("cases.register.yaml", r8));
    let findings: Finding[] = [];
    expect(() => { findings = validateRegister(r); }).not.toThrow();
    const malformed = findings.filter((f) => f.rule === "R13-malformed");
    expect(malformed).toHaveLength(1);
    expect(malformed[0]!.severity).toBe("fail");
    expect(malformed[0]!.message).toContain("use_cases");
    expect(malformed[0]!.message).toMatch(/\b[01]\b/);
    expectFailure(findings, "R13.1-no-decision");
    expect(() => coverage(r)).not.toThrow();
  });

  test.each([
    ["use_cases: [null, 3, text, [1, 2]]", "use_cases"],
    ["requirements: [null, 7]", "requirements"],
    ["conflicts: [null, x]", "conflicts"],
    ["coverage: [null, 5]", "coverage"],
  ])("C8: non-mapping list items in %s are R13-malformed fails", (yaml: string, list: string) => {
    const r = loadRegister(writeFile("cases.register.yaml", `register: 1\n${yaml}\n`));
    let findings: Finding[] = [];
    expect(() => { findings = validateRegister(r); }).not.toThrow();
    const malformed = findings.filter((f) => f.rule === "R13-malformed");
    expect(malformed.length).toBeGreaterThan(0);
    for (const finding of malformed) {
      expect(finding.severity).toBe("fail");
      expect(finding.message).toContain(list);
    }
    expect(() => coverage(r)).not.toThrow();
  });

  test.each([
    ["use_cases: 5"],
    ["use_cases: text"],
    ["use_cases: {a: 1}"],
    ["requirements: true"],
    ["coverage: {unit: UC1/f1}"],
    ["use_cases:\n  - id: 7\n    origin: user\n    fails_if: not a list\n    min_acceptance: {a: 1}\n    decision: declined"],
    ["use_cases:\n  - id: UC1\n    origin: ai\n    decision: [1]\nrequirements:\n  - id: RQ1\n    origin: user\n    serves: UC1\n    fails_if: [null, [1]]"],
    ["coverage:\n  - unit: [1]\n    covered_by: text\n    skippable: yes"],
    ["conflicts:\n  - use_case: [1]\n    requirement: {a: 1}\n    shown_to_owner: maybe"],
    ["frozen: [1, 2]\nuse_cases: []"],
  ])("C8: validation and coverage never throw on %j", (yaml: string) => {
    const r = loadRegister(writeFile("cases.register.yaml", `register: 1\n${yaml}\n`));
    expect(() => validateRegister(r)).not.toThrow();
    expect(() => coverage(r)).not.toThrow();
    expect(Array.isArray(validateRegister(r))).toBe(true);
    expect(typeof coverage(r).total).toBe("number");
  });

  test("C8: a touched register with an empty item and an undecided AI case blocks Stop rather than failing open (R8 input)", () => {
    writeFile("cases.register.yaml", r8);
    handleHook({ hook_event_name: "PostToolUse", session_id: "session-a", tool_name: "Write", tool_input: { file_path: "cases.register.yaml" } }, env);
    const reason = blockReason(handleHook(stop(), env));
    expect(reason).toContain("R13.1-no-decision");
    expect(reason).toContain("R13-malformed");
    expect(guardErrors()).toEqual([]);
  });

  test("C8: cli register on the R8 register exits 1 with R13-malformed, not an internal error", () => {
    writeFile("cases.register.yaml", r8);
    const result = runCli(["register", "cases.register.yaml"]);
    expect(result.exitCode).toBe(1);
    expect(result.stdout).toContain("R13-malformed");
    expect(result.stdout).toContain("R13.1-no-decision");
    expect(result.stderr).not.toContain("internal error");
  });
});

// ---- C9 ---------------------------------------------------------------------------------------------------------

describe("C9 (R19) a touched register that no longer exists", () => {
  test("C9: a touched then deleted register is skipped at Stop (R19 input)", () => {
    writeFile("tmp.register.yaml", "register: 1\n");
    handleHook({ hook_event_name: "PostToolUse", session_id: "session-a", tool_name: "Write", tool_input: { file_path: "tmp.register.yaml" } }, env);
    expect(readJournal(folder).records).toContainEqual(expect.objectContaining({ kind: "touched", path: "tmp.register.yaml" }));
    fs.rmSync(path.join(folder, "tmp.register.yaml"));
    expectQuiet(handleHook(stop(), env));
  });

  test("C9 control: a touched register that still exists and fails still blocks", () => {
    writeFile("tmp.register.yaml", "register: 1\n");
    handleHook({ hook_event_name: "PostToolUse", session_id: "session-a", tool_name: "Write", tool_input: { file_path: "tmp.register.yaml" } }, env);
    expect(blockReason(handleHook(stop(), env))).toContain("R11.1-not-frozen");
  });
});

// ---- C10 --------------------------------------------------------------------------------------------------------

describe("C10 (R21) the raise check needs last_assistant_message", () => {
  test.each([[{}], [{ last_assistant_message: null }], [{ last_assistant_message: 7 }], [{ last_assistant_message: ["runs/test/insight.md"] }]])(
    "C10: a Stop payload %j with no message string skips the raise check (R21 input)",
    (changes: Record<string, unknown>) => {
      seedFailure("F-218c4def", "s2");
      writeFile("runs/test/insight-a.md", insightText(["F-218c4def"]));
      expectQuiet(handleHook(stop({ session_id: "s2", ...changes }), env));
    },
  );

  test("C10: with no message string an open failure still blocks", () => {
    seedFailure("F-218c4def", "s2");
    expect(blockReason(handleHook(stop({ session_id: "s2" }), env))).toContain("F-218c4def");
  });

  test("C10 control: a message string that does not name the insight still blocks with the raise reason", () => {
    seedFailure("F-218c4def", "s2");
    writeFile("runs/test/insight-a.md", insightText(["F-218c4def"]));
    expect(blockReason(handleHook(stop({ session_id: "s2", last_assistant_message: "work finished" }), env))).toContain(
      path.join("runs", "test", "insight-a.md"),
    );
  });
});

// ---- C11 --------------------------------------------------------------------------------------------------------

describe("C11 (R11) a hook payload that is not JSON", () => {
  test.each([["not json"], [""], ["{\"hook_event_name\":"]])("C11: cli hook claude with stdin %j exits 0 quietly with one stderr line (R11 input)", (input: string) => {
    const result = runCli(["hook", "claude"], input);
    expect(result.exitCode).toBe(0);
    expect(result.stdout).toBe("");
    expect(result.stderr.trim().length).toBeGreaterThan(0);
    expect(result.stderr.trim().split(/\r?\n/)).toHaveLength(1);
  });
});

// ---- C12 --------------------------------------------------------------------------------------------------------

describe("C12 (R10) agent records are stored as given", () => {
  function record(changes: Partial<FailureRecord> = {}): FailureRecord {
    writeFile("runs/r1/insight.md", "evidence");
    return {
      kind: "failure", id: "F-6f7a8b9c", time, session: "session-a", found_by: "worker", check: "R12.1-empty-output",
      input: "stdout: the codex call", expected: "prompt: a full answer", actual: "output: an empty file",
      engine: "codex", harness: "claude-code", reason: "Output: the engine wrote nothing",
      evidence: "runs/r1/insight.md", ...changes,
    };
  }

  test("C12: appendFailure stores every field exactly as given (R10 input)", () => {
    const rec = record();
    appendFailure(folder, rec);
    expect(readJournal(folder).records).toEqual([rec]);
  });

  test("C12: recordFailureFromArgs stores --actual and --reason exactly as given (R10 input)", () => {
    writeFile("runs/r1/insight.md", "evidence");
    const stored = recordFailureFromArgs(folder, [
      "--check", "R12.1-empty-output", "--input", "codex call", "--expected", "a full answer",
      "--actual", "output: an empty file", "--reason", "Output: the engine wrote nothing",
      "--evidence", "runs/r1/insight.md", "--found-by", "worker", "--engine", "codex", "--harness", "claude-code", "--session", "s1",
    ]);
    const records = failures();
    expect(records).toHaveLength(1);
    expect(records[0]).toMatchObject({ actual: "output: an empty file", reason: "Output: the engine wrote nothing" });
    expect(stored.reason).toBe("Output: the engine wrote nothing");
  });

  test("C12 control: writeEvidence and appendRecord still drop raw-content keys", () => {
    const evidence = writeEvidence(folder, "F-6f7a8b9c", { stdoutLength: 3, stdout: secret, prompt: secret, command: secret });
    const facts = JSON.parse(fs.readFileSync(path.resolve(folder, evidence), "utf8"));
    expect(facts.stdoutLength).toBe(3);
    expect(JSON.stringify(facts)).not.toContain(secret);
    appendRecord(folder, { kind: "guard_error", time, session: "session-a", message: "a fixed phrase", stderr: secret } as GuardErrorRecord);
    expect(JSON.stringify(readJournal(folder).records)).not.toContain(secret);
    expect(guardErrors()).toHaveLength(1);
  });
});

// ---- C13 --------------------------------------------------------------------------------------------------------

describe("C13 (R17) evidence may be a file or a folder", () => {
  function record(evidence: string): FailureRecord {
    return {
      kind: "failure", id: "F-7a8b9c0d", time, session: "session-a", found_by: "worker", check: "R12.1-exit",
      input: "codex call", expected: "exit 0", actual: "exit 1", engine: "codex", harness: "claude-code",
      reason: "the engine exited 1", evidence,
    };
  }

  test("C13: an existing relative folder is valid evidence (R17 input)", () => {
    fs.mkdirSync(path.join(folder, "runs", "r1"), { recursive: true });
    expect(validateFailure(record("runs/r1"), folder)).toEqual([]);
    expect(() => appendFailure(folder, record("runs/r1"))).not.toThrow();
  });

  test("C13: an existing absolute folder is valid evidence", () => {
    fs.mkdirSync(path.join(folder, "runs", "r1"), { recursive: true });
    expect(validateFailure(record(path.join(folder, "runs", "r1")), folder)).toEqual([]);
  });

  test("C13: cli fail --evidence with an existing folder appends one record (R17 input)", () => {
    fs.mkdirSync(path.join(folder, "runs", "r1"), { recursive: true });
    const result = runCli(["fail", "--check", "R12.1-exit", "--input", "codex call", "--expected", "exit 0", "--actual", "exit 1",
      "--reason", "the engine exited 1", "--evidence", "runs/r1", "--found-by", "worker", "--engine", "codex",
      "--harness", "claude-code", "--session", "s1"]);
    expect(result.exitCode).toBe(0);
    expect(failures()).toHaveLength(1);
  });

  test("C13 control: a folder that does not exist is still rejected", () => {
    expect(validateFailure(record("runs/missing"), folder).length).toBeGreaterThan(0);
  });
});

// ---- C14 --------------------------------------------------------------------------------------------------------

describe("C14 (R18) doctor health with unexpected JSON", () => {
  test.each([["null"], ["[]"], ["42"], ['"text"'], ["true"], ["{}"], ['{"findings":3}'], ['{"findings":{"a":1}}']])(
    "C14: health JSON %s with exit 0 is ok false, unexpected JSON (R18 input)",
    (stdout: string) => {
      const home = path.join(folder, "home");
      const projectRoot = path.join(folder, "project");
      fs.mkdirSync(home);
      fs.mkdirSync(projectRoot);
      let report: DoctorReport | undefined;
      expect(() => { report = doctor({ home, projectRoot, healthScript: "x.py", run: () => ({ code: 0, stdout }) }); }).not.toThrow();
      expect(report!.health).toEqual({ ok: false, summary: "unexpected JSON" });
    },
  );

  test("C14 control: an object with a findings array is still ok", () => {
    const home = path.join(folder, "home");
    const projectRoot = path.join(folder, "project");
    fs.mkdirSync(home);
    fs.mkdirSync(projectRoot);
    const report = doctor({ home, projectRoot, healthScript: "x.py", run: () => ({ code: 0, stdout: '{"findings":[1,2]}' }) });
    expect(report.health).toEqual({ ok: true, summary: "2 findings" });
  });
});

// ---- C15 --------------------------------------------------------------------------------------------------------

describe("C15 (R6) opencode install prints a one-line plugin file", () => {
  function pluginLine(snippet: string): string {
    const line = snippet.split("\n").map((each) => each.trim()).find((each) => each.startsWith("export { default } from"));
    expect(line).toBeDefined();
    return line!;
  }

  test("C15: the snippet holds the exact one-line plugin file and names a plugins folder", () => {
    const guardDir = "/opt/tools/harness-guard";
    const snippet = installSnippet("opencode", guardDir);
    expect(pluginLine(snippet)).toBe(`export { default } from "${guardDir}/src/plugins/opencode.ts";`);
    expect(snippet).toMatch(/plugins?\//);
  });

  test("C15: the printed line, saved in a plugins folder outside the package, loads and blocks a trap (R6 input)", async () => {
    const line = pluginLine(installSnippet("opencode", packageDir));
    const file = writeFile("home/.config/opencode/plugins/harness-guard.ts", `${line}\n`);
    const loaded = await import(file);
    expect(typeof loaded.default).toBe("function");
    const plugin = await loaded.default({ directory: folder });
    await expect(plugin["tool.execute.before"]({ tool: "bash" }, { args: { command: "codex exec task" } })).rejects.toThrow("trap:codex-stdin");
  });
});

// ---- C16 --------------------------------------------------------------------------------------------------------

describe("C16 (R7) doctor opencode reads a plugin file's text", () => {
  test.each([
    ["home/.config/opencode/plugins/harness-guard.ts"],
    ["home/.config/opencode/plugin/guard.ts"],
    ["project/.opencode/plugins/guard.ts"],
    ["project/.opencode/plugin/guard.ts"],
  ])("C16: the installed one-line plugin file in %s counts as installed (R7 input)", (name: string) => {
    fs.mkdirSync(path.join(folder, "home"), { recursive: true });
    fs.mkdirSync(path.join(folder, "project"), { recursive: true });
    writeFile(name, 'export { default } from "/opt/tools/harness-guard/src/plugins/opencode.ts";\n');
    const report = doctor({ home: path.join(folder, "home"), projectRoot: path.join(folder, "project") });
    expect(report.harnesses.find((row) => row.harness === "opencode")?.guard).toBe("installed");
  });

  test("C16: harness-guard anywhere in the text, such as a comment, counts", () => {
    fs.mkdirSync(path.join(folder, "project"), { recursive: true });
    writeFile("home/.config/opencode/plugins/guard.ts", "// the harness-guard adapter\nexport { default } from \"/opt/g/src/plugins/opencode.ts\";\n");
    const report = doctor({ home: path.join(folder, "home"), projectRoot: path.join(folder, "project") });
    expect(report.harnesses.find((row) => row.harness === "opencode")?.guard).toBe("installed");
  });

  test("C16 control: a plugin file without harness-guard is absent", () => {
    fs.mkdirSync(path.join(folder, "project"), { recursive: true });
    writeFile("home/.config/opencode/plugins/other.ts", "export default async () => ({});\n");
    const report = doctor({ home: path.join(folder, "home"), projectRoot: path.join(folder, "project") });
    expect(report.harnesses.find((row) => row.harness === "opencode")?.guard).toBe("absent");
  });
});

// ---- C17 --------------------------------------------------------------------------------------------------------

// These tests read the real process table through the CLI (the CLI has no injection point for `running`). They start
// their own process and fail loudly if another `opencode run` is already running, since the result would then not
// tell the two behaviours apart.
describe("C17 (R9) the CLI drops only its own process and its parent from running", () => {
  const other = /opencode\s+run/;

  function processLines(): string[] {
    return execFileSync("ps", ["-eo", "args="], { encoding: "utf8" }).split("\n");
  }

  function requireNoOtherOpencode(): void {
    const busy = processLines().filter((line) => other.test(line));
    if (busy.length > 0) throw new Error(`C17 needs a machine with no other opencode run process (found ${busy.length})`);
  }

  // bash -c 'sleep 30; :' opencode run review <marker>: ps shows "bash -c sleep 30; : opencode run review <marker>".
  // Detached, so stopSleeper can kill the whole group (bash and its sleep).
  function startSleeper(marker: string): ChildProcess {
    const child = spawn("bash", ["-c", "sleep 30; :", "opencode", "run", "review", marker], { stdio: "ignore", detached: true });
    const deadline = Date.now() + 3000;
    while (!processLines().some((line) => line.includes(marker))) {
      if (Date.now() > deadline) { stopSleeper(child); throw new Error("the sleeper process did not appear"); }
      Bun.sleepSync(25);
    }
    return child;
  }

  function stopSleeper(child: ChildProcess): void {
    try { process.kill(-child.pid!, "SIGKILL"); } catch { child.kill("SIGKILL"); }
  }

  test("C17: another process whose line contains harness-guard still counts for lint (R9 input)", () => {
    requireNoOtherOpencode();
    const sleeper = startSleeper(`tools/harness-guard/SPEC.md-${path.basename(folder)}`);
    try {
      const result = runCli(["lint", 'opencode run "second task"']);
      expect(result.exitCode).toBe(1);
      expect(result.stdout).toContain("trap:opencode-parallel");
    } finally {
      stopSleeper(sleeper);
    }
  });

  test("C17: another process whose line contains harness-guard still counts for the hook", () => {
    requireNoOtherOpencode();
    const sleeper = startSleeper(`tools/harness-guard/SPEC.md-${path.basename(folder)}`);
    try {
      const result = runCli(["hook", "claude"], JSON.stringify(pre('opencode run "second task"')));
      expect(result.exitCode).toBe(0);
      expect(JSON.parse(result.stdout).hookSpecificOutput.permissionDecisionReason).toContain("trap:opencode-parallel");
    } finally {
      stopSleeper(sleeper);
    }
  });

  test("C17: the CLI's own process and its parent are dropped even when their lines name an engine", () => {
    requireNoOtherOpencode();
    const quote = (text: string) => `'${text.replace(/'/g, "'\\''")}'`;
    const script = `${quote(process.execPath)} ${quote(cli)} lint ${quote('opencode run "second task"')}; exit $?`;
    const result = spawnSync("bash", ["-c", script], { cwd: folder, encoding: "utf8", timeout: 15000 });
    expect(result.status).toBe(0);
    expect(result.stdout).not.toContain("trap:opencode-parallel");
  });
});

// ---- C18 --------------------------------------------------------------------------------------------------------

describe("C18 (R12) heredocs open with or without a space before <<", () => {
  test.each([
    ["cat >notes.md<<EOF\ncodex exec x\nEOF"],
    ["cat<<EOF\ncodex exec x\nEOF"],
    ["x>f<<EOF\ncodex exec x\nEOF"],
    ["cat<<'EOF'\nopencode run task &\nEOF"],
    ["cat<<-EOF\n\tcodex exec x\n\tEOF"],
  ])("C18: the heredoc body of %j is dropped (R12 input)", (command: string) => {
    for (const segment of segments(command)) {
      expect(segment.text).not.toContain("codex exec");
      expect(segment.text).not.toContain("opencode run");
    }
    expect(lintCommand(command, { repoRoot: folder, running: [] })).toEqual([]);
    expect(recognizeEngineCall(command)).toBeNull();
  });

  test("C18: a command after the heredoc's end is still read", () => {
    expectFailure(lintCommand("cat>notes.md<<EOF\ntext\nEOF\ncodex exec x", { repoRoot: folder, running: [] }), "trap:codex-stdin");
  });
});

// ---- C19 --------------------------------------------------------------------------------------------------------

describe("C19 (R13, E2) more segment starts", () => {
  test.each([["out=`codex exec x`"], ["out=$(codex exec x)"], ["echo $(codex exec x) done"], ["printf '%s' `codex exec x`"]])(
    "C19: a codex call inside a command substitution %s is recognised and linted (R13 input)",
    (command: string) => {
      expect(recognizeEngineCall(command)?.engine).toBe("codex");
      expectFailure(lintCommand(command, { repoRoot: folder, running: [] }), "trap:codex-stdin");
    },
  );

  test("C19: a substituted codex call with its stdin redirected is clean", () => {
    expect(lintCommand("out=$(codex exec x </dev/null)", { repoRoot: folder, running: [] })).toEqual([]);
    expect(lintCommand("out=`codex exec x </dev/null`", { repoRoot: folder, running: [] })).toEqual([]);
  });

  test.each([
    ["for f in a b; do timeout 600 opencode run \"review $f\"; done", "opencode"],
    ["for f in a b; do codex exec x; done", "codex"],
    ["if true; then codex exec x; fi", "codex"],
    ["if false; then :; else codex exec x; fi", "codex"],
    ["if false; then :; elif true; then codex exec x; fi", "codex"],
    ["! codex exec x", "codex"],
    ["{ codex exec x; }", "codex"],
  ])("C19: a shell word before the engine in %j is stripped (E2 input)", (command: string, engine: string) => {
    expect(recognizeEngineCall(command)?.engine).toBe(engine);
    if (engine === "codex") expectFailure(lintCommand(command, { repoRoot: folder, running: [] }), "trap:codex-stdin");
  });

  test("C19: a for loop that starts opencode in the background is caught by the parallel trap", () => {
    const command = 'for f in a b; do timeout 600 opencode run "review $f" & done';
    expectFailure(lintCommand(command, { repoRoot: folder, running: [] }), "trap:opencode-parallel");
  });
});

// ---- C20 --------------------------------------------------------------------------------------------------------

describe("C20 (R14) any input redirect satisfies codex-stdin", () => {
  test.each([
    ["codex exec - < brief.md"],
    ["codex exec \"do x\" 0<brief.md"],
    ["codex exec \"do x\" <brief.md"],
    ["codex exec \"do x\" <<< \"the task\""],
    ["codex exec - 0< runs/r1/briefs/brief.md"],
  ])("C20: %s passes the lint (R14 input)", (command: string) => {
    expect(lintCommand(command, { repoRoot: folder, running: [] })).toEqual([]);
  });

  test("C20 control: codex exec with no input redirect still fails", () => {
    expectFailure(lintCommand('codex exec "do x" > out.md', { repoRoot: folder, running: [] }), "trap:codex-stdin");
  });
});

// ---- C21 --------------------------------------------------------------------------------------------------------

describe("C21 (R15, E1) opencode paths: redirect targets never count, quoted paths do", () => {
  const repo = () => path.join(folder, "repo");
  const outside = () => path.join(folder, "outside");

  test.each([["2> %s/err.log"], ["> %s/out.md"], [">> %s/out.md"], ["&> %s/all.log"], ["2>%s/err.log"], [">%s/out.md"], ["2>> %s/err.log"]])(
    "C21: a redirect target %s outside the repo is not a path opencode reads (R15 input)",
    (redirect: string) => {
      const command = `opencode run "x" ${redirect.replace("%s", outside())}`;
      expect(lintCommand(command, { repoRoot: repo(), running: [] })).toEqual([]);
    },
  );

  test("C21: a /tmp redirect target is not counted (R15 input)", () => {
    expect(lintCommand('opencode run "x" 2> /tmp/err.log', { repoRoot: repo(), running: [] })).toEqual([]);
    expect(lintCommand('opencode run "x" > /tmp/out.md', { repoRoot: repo(), running: [] })).toEqual([]);
  });

  test.each([
    ['opencode run -m m "Read /home/someone/elsewhere/brief.md and do what it says"'],
    ["opencode run -m m 'Read /home/someone/elsewhere/brief.md and do what it says'"],
    ['opencode run "/home/someone/elsewhere/brief.md"'],
  ])("C21: an absolute path inside a quoted prompt counts: %s (E1 trap 3)", (command: string) => {
    expectFailure(lintCommand(command, { repoRoot: repo(), running: [] }), "trap:opencode-outside-repo");
  });

  test("C21: the E1 trap 3 input is denied through the PreToolUse hook", () => {
    const output = JSON.parse(handleHook(pre('opencode run -m m "Read /home/someone/elsewhere/brief.md and do what it says"'), env).stdout).hookSpecificOutput;
    expect(output.permissionDecision).toBe("deny");
    expect(output.permissionDecisionReason).toContain("trap:opencode-outside-repo");
  });

  test("C21 control: a quoted absolute path inside the repo does not count", () => {
    const command = `opencode run "Read ${path.join(repo(), "briefs", "brief.md")} and do what it says"`;
    expect(lintCommand(command, { repoRoot: repo(), running: [] })).toEqual([]);
  });

  test("C21: an outside path inside quotes counts even when a redirect target is also outside", () => {
    const command = `opencode run "Read ${path.join(outside(), "brief.md")}" > ${path.join(outside(), "out.md")}`;
    expectFailure(lintCommand(command, { repoRoot: repo(), running: [] }), "trap:opencode-outside-repo");
  });
});

// ---- C22 --------------------------------------------------------------------------------------------------------

describe("C22 (R16) agy 502 needs a 502 context", () => {
  function agy(stderr: string): Finding[] {
    return checkResult({ call: call({ engine: "agy", stdoutIsAnswer: true }), cwd: folder, exitCode: 0, stdout: "full answer", stderr, interrupted: false });
  }

  test.each([["warning: src/app.ts:502: unused variable"], ["502"], ["processed 502 files"], ["line 502 of the log"]])(
    "C22: stderr %j is not a 502 failure (R16 input)",
    (stderr: string) => {
      expect(rules(agy(stderr))).not.toContain("trap:agy-502");
    },
  );

  test.each([["Error: 502 Bad Gateway"], ["Bad Gateway"], ["HTTP 502"], ["status 502"], ["error 502"]])(
    "C22: stderr %j is a 502 failure",
    (stderr: string) => {
      expectFailure(agy(stderr), "trap:agy-502");
    },
  );
});

// ---- C23 --------------------------------------------------------------------------------------------------------

describe("C23 (E4) the PostToolUse context says the failure is already logged", () => {
  test("C23: one failure: the context line names the id and says not to log it again", () => {
    writeFile("answer.md", "");
    const result = handleHook(post("PostToolUse", "codex exec task -o answer.md </dev/null"), env);
    const records = failures();
    expect(records).toHaveLength(1);
    const context = JSON.parse(result.stdout).hookSpecificOutput.additionalContext as string;
    expect(context).toContain(`harness-guard logged ${records[0]!.id} — ${contextLine}`);
    expect(context).not.toContain("Log it in your report");
  });

  test("C23: several failures: every id is named and the line says they are already in the journal", () => {
    const result = handleHook(post("PostToolUse", "dsh headless task", { response: { interrupted: true } }), env);
    const records = failures();
    expect(records).toHaveLength(2);
    const context = JSON.parse(result.stdout).hookSpecificOutput.additionalContext as string;
    expect(context.startsWith("harness-guard logged ")).toBe(true);
    for (const rec of records) expect(context).toContain(rec.id);
    expect(context).toContain(contextLine);
    expect(context).not.toContain("Log it in your report");
  });

  test("C23: PostToolUseFailure uses the same context line", () => {
    const result = handleHook(post("PostToolUseFailure", "dsh headless task", { payload: { exit_code: 7 }, response: { stdout: "answer", exit_code: 7 } }), env);
    const records = failures();
    expect(records).toHaveLength(1);
    expect(JSON.parse(result.stdout).hookSpecificOutput.additionalContext).toContain(`harness-guard logged ${records[0]!.id} — ${contextLine}`);
  });
});
