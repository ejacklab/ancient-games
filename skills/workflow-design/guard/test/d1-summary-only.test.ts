// Written by the COO after long-session round 2 (B2): a compound command's other output must not read as a test failure.
import { expect, test } from "bun:test";
import { execSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { handleHook } from "../src/hooks.ts";
import { readJournal } from "../src/journal.ts";

function run(command: string, stdout: string) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "hg-"));
  execSync("git init -q", { cwd: root });
  handleHook({ hook_event_name: "PostToolUse", session_id: "s", cwd: root, tool_name: "Bash", tool_input: { command },
    tool_response: { stdout, stderr: "", interrupted: false } }, { cwd: root, running: [], now: () => new Date() });
  return readJournal(root).records.filter((r) => r.kind === "failure");
}

test("D1: a passing run followed by log counts that mention errors is not a test failure", () => {
  const out = "12 passed in 0.01s\n--- error lines:\n57\n--- by message:\n      9 errors from billing\n      3 failed logins\n";
  expect(run('python3 -m pytest -q 2>&1 | tail -1 && cd data && echo "--- error lines:" && grep -c ERROR log.txt', out)).toHaveLength(0);
});

test("D1: a pytest summary with failures still counts", () => {
  expect(run("python3 -m pytest -q | tail -1", "2 failed, 10 passed in 0.03s\n")).toHaveLength(1);
});

test("D1: a pytest collection error summary still counts", () => {
  expect(run("pytest -q | tail -1", "1 error in 0.05s\n")).toHaveLength(1);
});
