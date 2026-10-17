import { afterEach, beforeEach, describe, expect, test } from "bun:test";
import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import type { FailureRecord, JournalRecord } from "../src/types.ts";

const cli = path.resolve(import.meta.dir, "../src/cli.ts");
const openId = "F-1a2b3c4d";
const answeredId = "F-5e6f7a8b";
const otherId = "F-abcdef01";
const time = "2026-10-16T08:00:00.000Z";
let root: string;
let home: string;

beforeEach(() => {
  root = fs.mkdtempSync(path.join(os.tmpdir(), "guard-round7-"));
  home = path.join(root, "home");
  fs.mkdirSync(home);
  writeFile("keep.txt", "existing project content\n");
});
afterEach(() => fs.rmSync(root, { recursive: true, force: true }));

function writeFile(name: string, content: string): void {
  const file = path.join(root, name);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, content);
}

function hashTree(): string {
  const hash = createHash("sha256");
  for (const name of fs.readdirSync(root, { recursive: true, encoding: "utf8" }).sort()) {
    const file = path.join(root, name);
    const stat = fs.lstatSync(file);
    hash.update(JSON.stringify([name, stat.mode, stat.size, stat.mtimeMs]));
    if (stat.isFile()) {
      try { hash.update(fs.readFileSync(file)); }
      catch (error) {
        if ((error as NodeJS.ErrnoException).code !== "EACCES") throw error;
        hash.update("unreadable:EACCES");
      }
    }
  }
  return hash.digest("hex");
}

function runCli(args: string[]) {
  const before = hashTree();
  // File descriptors capture stdout synchronously even when the CLI exits immediately.
  const capture = fs.mkdtempSync(path.join(os.tmpdir(), "guard-round7-output-"));
  const stdout = fs.openSync(path.join(capture, "stdout"), "w+");
  const stderr = fs.openSync(path.join(capture, "stderr"), "w+");
  try {
    const result = spawnSync(process.execPath, [cli, ...args], {
      cwd: root, encoding: "utf8", timeout: 10000, stdio: ["ignore", stdout, stderr],
      // Exclude Bun's transpiler cache writes from the planted project home.
      env: { ...process.env, HOME: home, XDG_CONFIG_HOME: path.join(home, ".config"), BUN_RUNTIME_TRANSPILER_CACHE_PATH: "0" },
    });
    expect(result.error).toBeUndefined();
    expect(result.signal).toBeNull();
    expect(hashTree()).toBe(before);
    return { exitCode: result.status, stdout: fs.readFileSync(path.join(capture, "stdout"), "utf8"), stderr: fs.readFileSync(path.join(capture, "stderr"), "utf8") };
  } finally {
    fs.closeSync(stdout);
    fs.closeSync(stderr);
    fs.rmSync(capture, { recursive: true, force: true });
  }
}

function failure(id = openId, session = "session-a", check = "R12.1-empty-output", engine = "codex"): FailureRecord {
  writeFile(`.harness-guard/evidence/${id}.json`, '{"stdoutLength":0}\n');
  return {
    kind: "failure", id, time, session, found_by: "evaluator", check, engine, harness: "claude-code",
    input: `${engine} call`, expected: "non-empty output", actual: "empty output", reason: "output is empty",
    evidence: `.harness-guard/evidence/${id}.json`,
  };
}
function writeJournal(records: JournalRecord[]): void {
  writeFile(".harness-guard/journal.jsonl", records.map((record) => JSON.stringify(record)).join("\n") + "\n");
}
function writeInsight(id: string, valid = true, name = "runs/task/insight.md"): void {
  writeFile(name, [
    `## ${id}`, "Whys:", "1. Output was empty.", "2. It was not checked.",
    ...(valid ? ["3. The instruction omitted a check."] : []),
    "Source: instruction", "Root cause: the instruction omitted the check", "Options:",
    "1. [rule] add the check; evidence: runs/task/rule.md",
    "2. [check] validate the answer; evidence: runs/task/result.md", "",
  ].join("\n"));
}
function jsonOutput(args: string[], exitCode = 0) {
  const result = runCli(args);
  expect(result.exitCode).toBe(exitCode);
  expect(result.stderr).toBe("");
  // Parse all stdout to reject text preambles, trailing text and multiple documents.
  return JSON.parse(result.stdout);
}

describe("Round 7 J1 doctor JSON", () => {
  test("prints every DoctorReport field and harness with a read-only answering probe", () => {
    writeJournal([failure()]);
    writeInsight(openId, false);
    writeFile(".claude/settings.json", JSON.stringify({ hooks: { PreToolUse: [{ matcher: "Bash", hooks: [
      { type: "command", command: "bun harness-guard/src/cli.ts hook claude" },
    ] }] } }));
    const report = jsonOutput(["doctor", "--json"]);
    expect(report.health).toBeNull();
    expect(Array.isArray(report.harnesses)).toBe(true);
    expect(report.harnesses.map((row: { harness: string }) => row.harness).sort()).toEqual([
      "claude-code", "codex", "opencode", "qwen",
    ]);
    for (const row of report.harnesses) {
      expect(row).toMatchObject({
        harness: expect.any(String), guard: row.harness === "claude-code" ? "installed" : "absent",
        answers: true, note: expect.any(String),
      });
    }
  });
  test("health reports include ok and summary when a health script is supplied", () => {
    writeJournal([failure()]);
    writeInsight(openId);
    writeFile("health.py", `print('{"findings":[{},{}]}')\n`);
    const report = jsonOutput(["doctor", "--json", "--health", path.join(root, "health.py")]);
    expect(report.health).toEqual({ ok: true, summary: "2 findings" });
  });
});

describe("Round 7 J2 rates JSON", () => {
  beforeEach(() => {
    writeJournal([
      { kind: "success", time, session: "session-a", check: "engine-call", engine: "codex" },
      { kind: "success", time, session: "session-a", check: "engine-call", engine: "codex" },
      failure(), failure(answeredId, "session-a", "trap:codex-stdin"),
      { kind: "success", time, session: "session-a", check: "test-run", engine: "bun" },
      failure(otherId, "session-b", "R12.2-test-failed", "bun"),
    ]);
    writeInsight(answeredId);
  });
  test.each([[false], [true]])("prints row fields and counts; session filter %s", (filtered: boolean) => {
    const report = jsonOutput(["rates", "--json", ...(filtered ? ["--session", "session-a"] : [])]);
    expect(Array.isArray(report.rows)).toBe(true);
    expect(report.rows).toHaveLength(2);
    expect(report.rows).toEqual(expect.arrayContaining([
      { check: "engine-call", engine: "codex", ok: 2, fail: 2 },
      { check: "test-run", engine: "bun", ok: 1, fail: filtered ? 0 : 1 },
    ]));
  });
  test("an absent session returns the rows field as an empty array", () => {
    expect(jsonOutput(["rates", "--session", "missing", "--json"])).toEqual({ rows: [] });
  });
});

describe("Round 7 J3 insight JSON", () => {
  test("open failures exit one; invalid sections expose id, file and fail rules", () => {
    writeJournal([failure(), failure(answeredId), failure(otherId, "session-b")]);
    writeInsight(openId, false, "runs/task/insight-invalid.md");
    writeInsight(answeredId);
    expect(jsonOutput(["insight", "--json", "--session", "session-a"], 1)).toEqual({
      open: [{ id: openId, check: "R12.1-empty-output" }],
      invalid: [{ id: openId, file: "runs/task/insight-invalid.md", rules: ["R12.3-whys-count"] }],
      unreadable: [],
    });
    expect(jsonOutput(["insight", "--json"], 1).open).toEqual(expect.arrayContaining([
      { id: openId, check: "R12.1-empty-output" }, { id: otherId, check: "R12.1-empty-output" },
    ]));
  });
  test("valid answers close failures and exit zero with every field present", () => {
    writeJournal([failure()]);
    writeInsight(openId);
    expect(jsonOutput(["insight", "--json"])).toEqual({ open: [], invalid: [], unreadable: [] });
  });
  test("session filtering excludes another session's open failures", () => {
    writeJournal([failure(openId, "session-b")]);
    expect(jsonOutput(["insight", "--session", "session-a", "--json"])).toEqual({
      open: [], invalid: [], unreadable: [],
    });
    expect(jsonOutput(["insight", "--json", "--session", "session-b"], 1).open).toEqual([
      { id: openId, check: "R12.1-empty-output" },
    ]);
  });
  test("unreadable files are reported by relative path without closing the failure", () => {
    writeJournal([failure()]);
    const name = "runs/task/insight-unreadable.md";
    writeInsight(openId, true, name);
    fs.chmodSync(path.join(root, name), 0);
    try {
      expect(jsonOutput(["insight", "--json"], 1)).toEqual({
        open: [{ id: openId, check: "R12.1-empty-output" }], invalid: [], unreadable: [name],
      });
    } finally { fs.chmodSync(path.join(root, name), 0o600); }
  });
});

describe("Round 7 preserves text output and exit codes without --json", () => {
  test.each([["doctor"], ["rates"], ["insight"]])("%s preserves text across JSON calls without writing", (command: string) => {
    writeJournal([
      failure(), { kind: "success", time, session: "session-a", check: "engine-call", engine: "codex" },
    ]);
    writeInsight(openId, false);
    const before = runCli([command]);
    expect(before.exitCode).toBe(command === "insight" ? 1 : 0);
    expect(before.stdout.trim().length).toBeGreaterThan(0);
    expect(() => JSON.parse(before.stdout)).toThrow();
    if (command === "doctor") {
      for (const harness of ["claude-code", "codex", "qwen", "opencode"]) expect(before.stdout).toContain(harness);
      expect(before.stdout).toContain("|");
    } else if (command === "rates") {
      expect(before.stdout).toContain("|");
      for (const field of ["check", "engine", "ok", "fail", "engine-call", "codex"]) expect(before.stdout).toContain(field);
    } else {
      expect(before.stdout + before.stderr).toContain(openId);
      expect(before.stdout + before.stderr).toContain("R12.3-whys-count");
    }
    jsonOutput([command, "--json"], command === "insight" ? 1 : 0);
    expect(runCli([command])).toEqual(before);
  });
  test("answered insight text still exits zero", () => {
    writeJournal([failure()]);
    writeInsight(openId);
    const before = runCli(["insight"]);
    expect(before.exitCode).toBe(0);
    jsonOutput(["insight", "--json"]);
    expect(runCli(["insight"])).toEqual(before);
  });
});

// runCli hashes every entry before/after; empty guard state also detects first-use writes.
describe("Round 7 read-only commands on roots without guard state", () => {
  test.each([["doctor"], ["rates"], ["insight"]])("%s creates no files on first use", (command: string) => {
    const report = jsonOutput([command, "--json"]);
    if (command === "rates") expect(report).toEqual({ rows: [] });
    if (command === "insight") expect(report).toEqual({ open: [], invalid: [], unreadable: [] });
    runCli([command]);
    expect(fs.existsSync(path.join(root, ".harness-guard"))).toBe(false);
  });
});

// Health-check consumers capture stdout through a pipe rather than a regular file.
describe("Round 7 JSON through consumer stdout pipes", () => {
  test.each([["doctor"], ["rates"], ["insight"]])("%s JSON parses when stdout is piped", (command: string) => {
    writeJournal([failure()]);
    writeInsight(openId);
    const before = hashTree();
    const result = spawnSync(process.execPath, [cli, command, "--json"], {
      cwd: root, encoding: "utf8", timeout: 10000,
      env: { ...process.env, HOME: home, BUN_RUNTIME_TRANSPILER_CACHE_PATH: "0" },
    });
    expect(result.error).toBeUndefined();
    expect(result.signal).toBeNull();
    expect(hashTree()).toBe(before);
    expect(result.status).toBe(0);
    expect(result.stderr).toBe("");
    expect(() => JSON.parse(result.stdout)).not.toThrow();
  });
});
