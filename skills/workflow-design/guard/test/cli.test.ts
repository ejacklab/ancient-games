import { afterEach, beforeEach, describe, expect, spyOn, test } from "bun:test";
import { execFileSync, spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { installSnippet } from "../src/install.ts";
import { appendFailure, readJournal, writeEvidence } from "../src/journal.ts";
import type { FailureRecord, Register } from "../src/types.ts";

const secret = "SECRET-PLANT-7f3a9c";
const cli = path.resolve(import.meta.dir, "../src/cli.ts");
const first = "F-1a2b3c4d";
let folder: string;

beforeEach(() => {
  folder = fs.mkdtempSync(path.join(os.tmpdir(), "hg-"));
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

function runCli(args: string[], input = "", cwd = folder) {
  const result = spawnSync(process.execPath, [cli, ...args], { cwd, input, encoding: "utf8", timeout: 10000 });
  expect(result.error).toBeUndefined();
  expect(result.signal).toBeNull();
  return { exitCode: result.status, stdout: result.stdout, stderr: result.stderr };
}

function printed(result: ReturnType<typeof runCli>): string {
  return `${result.stdout}\n${result.stderr}`;
}

function snapshot(): Record<string, string> {
  const files: Record<string, string> = {};
  for (const name of fs.readdirSync(folder, { recursive: true, encoding: "utf8" })) {
    const file = path.join(folder, name);
    files[name] = fs.statSync(file).isDirectory() ? "directory" : fs.readFileSync(file).toString("base64");
  }
  return files;
}

function expectNoSecret(result: ReturnType<typeof runCli>): void {
  expect(printed(result)).not.toContain(secret);
  const state = path.join(folder, ".harness-guard");
  if (fs.existsSync(state)) {
    for (const name of fs.readdirSync(state, { recursive: true, encoding: "utf8" })) {
      const file = path.join(state, name);
      expect(name).not.toContain(secret);
      if (fs.statSync(file).isFile()) expect(fs.readFileSync(file, "utf8")).not.toContain(secret);
    }
  }
}

function seedFailure(id = first, session = "session-a"): FailureRecord {
  return appendFailure(folder, {
    kind: "failure", id, time: "2026-10-15T08:00:00.000Z", session, found_by: "guard",
    check: "R12.1-empty-output", input: "codex answer.md", expected: "non-empty output", actual: "empty output",
    engine: "codex", harness: "claude-code", reason: "output is empty",
    evidence: writeEvidence(folder, id, { stdoutLength: 0, rules: ["R12.1-empty-output"] }),
  });
}

function writeInsight(id = first, invalid = false): string {
  const name = "runs/test/insight.md";
  writeFile(name, [
    `## ${id}`, "Whys:", "1. Output was empty.", "2. It was not checked.",
    ...(invalid ? [] : ["3. The instruction omitted a check."]),
    "Source: instruction", "Root cause: the instruction omitted the check", "Options:",
    "1. [rule] add the check; evidence: runs/test/rule.md",
    "2. [check] validate the answer; evidence: runs/test/result.md", "",
  ].join("\n"));
  return name;
}

function register(): Register {
  return {
    register: 1,
    frozen: createHash("sha256").update(JSON.stringify([["UC1/f1", "work is lost"], ["UC1/m1", "work reopens"]])).digest("hex"),
    use_cases: [{ id: "UC1", origin: "user", purpose: "preserve work", fails_if: ["work is lost"], min_acceptance: ["work reopens"] }],
    coverage: [{ unit: "UC1/f1", covered_by: ["test/save.test.ts"] }, { unit: "UC1/m1", covered_by: ["test/open.test.ts"] }],
  };
}

function failureArgs(): string[] {
  return ["--check", "R12.1-empty-output", "--input", "codex answer.md", "--expected", "non-empty output",
    "--actual", "empty output", "--reason", "output is empty", "--evidence", "proof.json", "--found-by", "worker",
    "--engine", "codex", "--harness", "claude-code", "--session", "session-cli"];
}

describe("installSnippet", () => {
  test.each(["claude-code", "codex", "qwen"] as const)("install: %s has every required event and matcher", (harness) => {
    const guardDir = path.join(folder, "harness-guard");
    const snippet: string = installSnippet(harness, guardDir);
    const firstLine = snippet.split("\n")[0]!;
    expect(firstLine).toContain(".harness-guard/");
    expect(firstLine).toContain(".gitignore");
    expect(firstLine).toMatch(/[\w./-]+\.(?:json|jsonc|toml)\b/);
    const start = snippet.indexOf("{");
    expect(start).toBeGreaterThanOrEqual(0);
    const settings = JSON.parse(snippet.slice(start, snippet.lastIndexOf("}") + 1));
    const events = ["PreToolUse", "PostToolUse", "PostToolUseFailure", "Stop", "SubagentStop", "SessionStart"];
    for (const event of events) {
      const entries = settings.hooks[event];
      expect(Array.isArray(entries)).toBe(true);
      expect(entries.length).toBeGreaterThan(0);
      const hooks = entries.flatMap((entry: { hooks: unknown[] }) => entry.hooks);
      expect(hooks).toContainEqual({ type: "command", command: `bun ${guardDir}/src/cli.ts hook claude` });
      for (const hook of hooks) expect(hook).toEqual({ type: "command", command: `bun ${guardDir}/src/cli.ts hook claude` });
    }
    expect(settings.hooks.PreToolUse).toContainEqual(expect.objectContaining({ matcher: "Bash" }));
    // After a call the guard watches Bash and file writes only (EJ, 2026-10-17).
    expect(settings.hooks.PostToolUse).toEqual([expect.objectContaining({ matcher: "Bash|Write|Edit|MultiEdit" })]);
    expect(settings.hooks.PostToolUseFailure).toEqual([expect.objectContaining({ matcher: "Bash" })]);
    if (harness === "codex" || harness === "qwen") {
      expect(snippet).toMatch(/reported/i);
      expect(snippet).toMatch(/not verified|unverified/i);
    }
  });

  test("install: opencode advice places its adapter in a plugins folder", () => {
    const snippet = installSnippet("opencode", path.join(folder, "harness-guard"));
    expect(snippet).toContain("src/plugins/opencode.ts");
    expect(snippet).toMatch(/plugins\//);
  });

  test.each(["claude-code", "codex", "qwen", "opencode"] as const)("install: %s snippet generation never changes a file", (harness) => {
    writeFile(".claude/settings.json", '{"token":"keep this value"}');
    const before = snapshot();
    const previousCwd = process.cwd();
    try {
      process.chdir(folder);
      installSnippet(harness, path.join(folder, "harness-guard"));
    } finally { process.chdir(previousCwd); }
    expect(snapshot()).toEqual(before);
  });

  test("install: existing config secrets are never read into the advice", () => {
    writeFile(".claude/settings.json", JSON.stringify({ env: { token: secret } }));
    const printed: string[] = [];
    const spies = [
      spyOn(console, "log").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
      spyOn(console, "warn").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
      spyOn(console, "error").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
      spyOn(process.stdout, "write").mockImplementation((chunk) => { printed.push(String(chunk)); return true; }),
      spyOn(process.stderr, "write").mockImplementation((chunk) => { printed.push(String(chunk)); return true; }),
    ];
    const previousCwd = process.cwd();
    try {
      process.chdir(folder);
      for (const harness of ["claude-code", "codex", "qwen", "opencode"] as const) {
        expect(installSnippet(harness, path.join(folder, "harness-guard"))).not.toContain(secret);
      }
    } finally {
      process.chdir(previousCwd);
      for (const spy of spies) spy.mockRestore();
    }
    expect(printed.join("\n")).not.toContain(secret);
    expect(readJournal(folder).records).toEqual([]);
  });
});

describe("CLI usage and lint", () => {
  test.each([[], ["unknown-command"], ["hook"], ["hook", "unknown"], ["lint"], ["register"], ["result"], ["install"], ["install", "--print", "unknown"]].map((args) => ({ args })))(
    "usage: incomplete or unknown command %j exits two",
    ({ args }: { args: string[] }) => {
      const result = runCli(args);
      expect(result.exitCode).toBe(2);
      expect(printed(result).trim().length).toBeGreaterThan(0);
    },
  );

  test("lint: a catalogued command trap exits one with its rule", () => {
    const result = runCli(["lint", "codex", "exec", "task"]);
    expect(result.exitCode).toBe(1);
    expect(printed(result)).toContain("trap:codex-stdin");
  });

  test("lint: a clean command exits zero", () => {
    expect(runCli(["lint", "codex exec task </dev/null"]).exitCode).toBe(0);
  });

  test("lint: command text never leaks through printed findings or state", () => {
    const result = runCli(["lint", `codex exec '${secret}'`]);
    expect(result.exitCode).toBe(1);
    expect(printed(result)).toContain("trap:codex-stdin");
    expectNoSecret(result);
  });
});

describe("CLI hook", () => {
  test("hook: stdin trap payload produces protocol denial JSON with exit zero", () => {
    const result = runCli(["hook", "claude"], JSON.stringify({ hook_event_name: "PreToolUse", session_id: "session-cli",
      tool_name: "Bash", tool_input: { command: "codex exec task" } }));
    expect(result.exitCode).toBe(0);
    expect(result.stderr).toBe("");
    expect(JSON.parse(result.stdout).hookSpecificOutput).toMatchObject({
      hookEventName: "PreToolUse", permissionDecision: "deny",
      permissionDecisionReason: expect.stringContaining("trap:codex-stdin"),
    });
  });

  test("hook: a clean input produces no output", () => {
    const result = runCli(["hook", "claude"], JSON.stringify({ hook_event_name: "PreToolUse", session_id: "session-cli",
      tool_name: "Bash", tool_input: { command: "echo clean" } }));
    expect(result).toEqual({ exitCode: 0, stdout: "", stderr: "" });
  });

  test("hook: an empty engine result writes a failure and evidence under the git root", () => {
    execFileSync("git", ["init", "--quiet", folder], { cwd: folder });
    const nested = path.join(folder, "nested");
    fs.mkdirSync(nested);
    writeFile("nested/answer.md", "");
    const result = runCli(["hook", "claude"], JSON.stringify({ hook_event_name: "PostToolUse", session_id: "session-cli",
      tool_name: "Bash", tool_input: { command: "codex exec task -o answer.md </dev/null" },
      tool_response: { stdout: "", stderr: "", interrupted: false } }), nested);
    expect(result.exitCode).toBe(0);
    const records = readJournal(folder).records.filter((r): r is FailureRecord => r.kind === "failure");
    expect(records).toHaveLength(1);
    expect(records[0]).toMatchObject({ session: "session-cli", check: "R12.1-empty-output", found_by: "guard" });
    expect(fs.existsSync(path.resolve(folder, records[0]!.evidence))).toBe(true);
    expect(JSON.parse(result.stdout).hookSpecificOutput.additionalContext).toContain(records[0]!.id);
    expect(fs.existsSync(path.join(nested, ".harness-guard"))).toBe(false);
  });

  test("hook: a secret in the prompt or tool error stays out of all guard output", () => {
    const result = runCli(["hook", "claude"], JSON.stringify({ hook_event_name: "PostToolUseFailure", session_id: "session-cli",
      tool_name: "Bash", tool_input: { command: `dsh headless '${secret}'` },
      error: secret, exit_code: 7, tool_response: { stdout: secret, error: secret, exit_code: 7 } }));
    expect(result.exitCode).toBe(0);
    expectNoSecret(result);
    expect(readJournal(folder).records.filter((r) => r.kind === "failure")).toHaveLength(1);
  });

  test("hook: a handler error propagates stderr and exit one without freezing", () => {
    writeFile(".harness-guard", "blocks directory creation");
    const result = runCli(["hook", "claude"], JSON.stringify({ hook_event_name: "PostToolUse", session_id: "session-cli",
      tool_name: "Bash", tool_input: { command: "dsh headless task" }, tool_response: { stdout: "", stderr: "" } }));
    expect(result.exitCode).toBe(1);
    expect(result.stderr.trim().length).toBeGreaterThan(0);
    expect(result.stderr.trim().split(/\r?\n/)).toHaveLength(1);
  });
});

describe("CLI result", () => {
  test("result: an empty output exits one and names its finding", () => {
    writeFile("answer.md", " \n");
    const result = runCli(["result", "--engine", "codex", "--out", "answer.md"]);
    expect(result.exitCode).toBe(1);
    expect(printed(result)).toContain("R12.1-empty-output");
  });

  test("result: a missing output exits one", () => {
    const result = runCli(["result", "--engine", "codex", "--out", "missing.md"]);
    expect(result.exitCode).toBe(1);
    expect(printed(result)).toContain("R12.1-missing-output");
  });

  test("result: a good output and zero exit produce no failure", () => {
    writeFile("answer.md", "answer");
    expect(runCli(["result", "--engine", "codex", "--out", "answer.md", "--exit", "0"]).exitCode).toBe(0);
    expect(readJournal(folder).records.filter((r) => r.kind === "failure")).toEqual([]);
  });

  test.each([["7", "R12.1-exit"], ["124", "R12.1-timeout"]])("result: exit %s is reported as %s", (exit: string, rule: string) => {
    writeFile("answer.md", "answer");
    const result = runCli(["result", "--engine", "codex", "--out", "answer.md", "--exit", exit]);
    expect(result.exitCode).toBe(1);
    expect(printed(result)).toContain(rule);
  });

  test("result: stderr-file feeds result traps without leaking the file's content", () => {
    writeFile("answer.md", secret);
    writeFile("stderr.txt", `soft-denied ${secret}`);
    const result = runCli(["result", "--engine", "agy", "--out", "answer.md", "--exit", "0", "--stderr-file", "stderr.txt"]);
    expect(result.exitCode).toBe(1);
    expect(printed(result)).toContain("trap:agy-soft-deny");
    expectNoSecret(result);
  });
});

describe("CLI fail", () => {
  test("fail: complete flags append a validated agent record", () => {
    writeFile("proof.json", "{}");
    const result = runCli(["fail", ...failureArgs()]);
    expect(result.exitCode).toBe(0);
    const records = readJournal(folder).records.filter((r): r is FailureRecord => r.kind === "failure");
    expect(records).toHaveLength(1);
    expect(records[0]).toMatchObject({
      check: "R12.1-empty-output", input: "codex answer.md", expected: "non-empty output", actual: "empty output",
      reason: "output is empty", evidence: "proof.json", found_by: "worker", engine: "codex", harness: "claude-code", session: "session-cli",
    });
    expect(records[0]!.id).toMatch(/^F-[0-9a-f]{8}$/);
  });

  test.each(["--reason", "--evidence"])("fail: missing %s is usage error rather than a default", (flag: string) => {
    writeFile("proof.json", "{}");
    const args = failureArgs();
    args.splice(args.indexOf(flag), 2);
    const result = runCli(["fail", ...args]);
    expect(result.exitCode).toBe(2);
    expect(printed(result)).toContain(flag.slice(2));
    expect(readJournal(folder).records).toEqual([]);
  });

  test("fail: existing evidence content is not echoed into output or the journal", () => {
    writeFile("proof.json", JSON.stringify({ prompt: secret }));
    const result = runCli(["fail", ...failureArgs()]);
    expect(result.exitCode).toBe(0);
    expectNoSecret(result);
  });
});

describe("CLI insight", () => {
  test("insight: an open failure exits one and lists its id", () => {
    seedFailure();
    const result = runCli(["insight"]);
    expect(result.exitCode).toBe(1);
    expect(printed(result)).toContain(first);
  });

  test("insight: an invalid section is listed and does not close its failure", () => {
    seedFailure();
    writeInsight(first, true);
    const result = runCli(["insight"]);
    expect(result.exitCode).toBe(1);
    expect(printed(result)).toContain(first);
    expect(printed(result)).toContain("R12.3-whys-count");
  });

  test("insight: a valid section closes the failure", () => {
    seedFailure();
    writeInsight();
    expect(runCli(["insight"]).exitCode).toBe(0);
  });

  test("insight: session filtering excludes other sessions' open failures", () => {
    seedFailure(first, "session-b");
    const result = runCli(["insight", "--session", "session-a"]);
    expect(result.exitCode).toBe(0);
    expect(printed(result)).not.toContain(first);
    expect(runCli(["insight", "--session", "session-b"]).exitCode).toBe(1);
  });

  test("insight: no failures is success", () => {
    expect(runCli(["insight"]).exitCode).toBe(0);
  });

  test("insight: raw text in an invalid section is not printed", () => {
    seedFailure();
    writeFile("runs/test/insight.md", `## ${first}\nWhys:\n1. ${secret}\nSource: instruction\nRoot cause: ${secret}\n`);
    const result = runCli(["insight"]);
    expect(result.exitCode).toBe(1);
    expectNoSecret(result);
  });
});

describe("CLI register", () => {
  test("register: validation failure exits one with the rule id", () => {
    const r = register();
    r.use_cases![0]!.origin = "ai";
    writeFile("cases.register.yaml", JSON.stringify(r));
    const result = runCli(["register", "cases.register.yaml"]);
    expect(result.exitCode).toBe(1);
    expect(printed(result)).toContain("R13.1-no-decision");
  });

  test("register: a coverage failure exits one", () => {
    const r = register();
    delete r.frozen;
    writeFile("cases.register.yaml", JSON.stringify(r));
    const result = runCli(["register", "cases.register.yaml"]);
    expect(result.exitCode).toBe(1);
    expect(printed(result)).toContain("R11.1-not-frozen");
  });

  test("register: a valid fully covered register exits zero", () => {
    writeFile("cases.register.yaml", JSON.stringify(register()));
    expect(runCli(["register", "cases.register.yaml"]).exitCode).toBe(0);
  });

  test("register: warnings alone exit zero", () => {
    const r = register();
    r.coverage![1] = { unit: "UC1/m1", skippable: { reason: "owner deferred it" } };
    writeFile("cases.register.yaml", JSON.stringify(r));
    const result = runCli(["register", "cases.register.yaml"]);
    expect(result.exitCode).toBe(0);
    expect(printed(result)).toContain("R11.1-below-target");
  });

  test("register: raw fields are not echoed in validation output", () => {
    const r = register();
    r.use_cases![0]!.purpose = secret;
    r.use_cases![0]!.fails_if = [secret];
    r.coverage = [];
    writeFile("cases.register.yaml", JSON.stringify(r));
    const result = runCli(["register", "cases.register.yaml"]);
    expect(result.exitCode).toBe(1);
    expectNoSecret(result);
  });
});

describe("CLI install", () => {
  test.each(["claude-code", "codex", "qwen", "opencode"] as const)("install: --print %s only prints and never writes a file", (harness) => {
    writeFile(".claude/settings.json", JSON.stringify({ token: secret }));
    const before = snapshot();
    const result = runCli(["install", "--print", harness]);
    expect(result.exitCode).toBe(0);
    expect(result.stdout.trim().length).toBeGreaterThan(0);
    expect(result.stdout).toContain(harness === "opencode" ? "src/plugins/opencode.ts" : "src/cli.ts hook claude");
    expectNoSecret(result);
    expect(snapshot()).toEqual(before);
  });
});
