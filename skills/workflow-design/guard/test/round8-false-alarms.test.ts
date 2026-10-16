// Written by the COO for Round 8: two false alarms the guard logged in run 20261016-integrate-r11-r13 are filtered by
// the checks themselves (F-3e11ce16: the guard's own "findings" exit; F-8392b4ce: criteria read against the session's
// first work, not the request's). The real failures beside them still count.
import { expect, test } from "bun:test";
import { execSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { handleHook } from "../src/hooks.ts";
import { readJournal } from "../src/journal.ts";

function box() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "hg-"));
  execSync("git init -q", { cwd: root });
  let clock = 1_000_000;
  const env = { cwd: root, running: [], now: () => new Date((clock += 1000)) };
  const post = (payload: Record<string, unknown>) => handleHook({ session_id: "s", cwd: root, ...payload }, env);
  const failures = (check?: string) =>
    readJournal(root).records.filter((r) => r.kind === "failure" && (check === undefined || r.check === check));
  return { root, post, failures };
}

function failedCall(post: (p: Record<string, unknown>) => unknown, command: string, exitCode: number) {
  post({ hook_event_name: "PostToolUseFailure", tool_name: "Bash", tool_input: { command }, exit_code: exitCode, error: "x" });
}

const CLI = "bun /x/.claude/skills/workflow-design/guard/src/cli.ts";

test.each([["insight"], ["criteria score runs/r/criteria.yaml"], ["register r.yaml"], ["path check p.yaml"]])(
  "a guard query that exits 1 (findings) is not a command error: %s",
  (args: string) => {
    const { post, failures } = box();
    failedCall(post, `git commit -q -m x && ${CLI} ${args}`, 1);
    expect(failures("R12.2-command-error")).toHaveLength(0);
  },
);

test.each([
  [`${CLI} insight`, 2],                 // a usage error is still an error
  [`${CLI} doctor`, 1],                  // not a query whose exit 1 means findings
  [`${CLI} insight && git push`, 1],     // the exit is the last command's, not the guard's
  ["bun run build", 1],
])("still a command error: %s exit %d", (command: string, exitCode: number) => {
  const { post, failures } = box();
  failedCall(post, command, exitCode);
  expect(failures("R12.2-command-error")).toHaveLength(1);
});

function criteria(root: string) {
  const file = path.join(root, ".harness-guard", "criteria", "c.yaml");
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, "criteria: 1\nsession: s\nrequest: r\nitems:\n  - id: C1\n    text: t\n    met: true\n    evidence: e\n");
  return file;
}

const green = { hook_event_name: "PostToolUse", tool_name: "Bash", tool_input: { command: "pytest -q" },
  tool_response: { stdout: "3 passed in 0.01s\n", stderr: "", interrupted: false } };

test("criteria written first for a new request are not late, though an earlier request's work came before", () => {
  const { root, post, failures } = box();
  post({ hook_event_name: "UserPromptSubmit", prompt: "first request" });
  post(green);                                            // the first request's work
  post({ hook_event_name: "UserPromptSubmit", prompt: "second request" });
  post({ hook_event_name: "PostToolUse", tool_name: "Write", tool_input: { file_path: criteria(root) }, tool_response: {} });
  post(green);                                            // the second request's work, after its criteria
  post({ hook_event_name: "Stop", stop_hook_active: false, last_assistant_message: "done" });
  expect(failures("R12.7-criteria-late")).toHaveLength(0);
});

test("criteria written after the request's own work began are still late", () => {
  const { root, post, failures } = box();
  post({ hook_event_name: "UserPromptSubmit", prompt: "first request" });
  post(green);
  post({ hook_event_name: "UserPromptSubmit", prompt: "second request" });
  post(green);                                            // the second request's work, before its criteria
  post({ hook_event_name: "PostToolUse", tool_name: "Write", tool_input: { file_path: criteria(root) }, tool_response: {} });
  post({ hook_event_name: "Stop", stop_hook_active: false, last_assistant_message: "done" });
  expect(failures("R12.7-criteria-late")).toHaveLength(1);
});

test("a prompt record holds its time and session only, never the prompt's text", () => {
  const { root, post } = box();
  post({ hook_event_name: "UserPromptSubmit", prompt: "SECRET-PLANT-7f3a9c" });
  const text = fs.readFileSync(path.join(root, ".harness-guard", "journal.jsonl"), "utf8");
  expect(text).not.toContain("SECRET-PLANT-7f3a9c");
  const prompts = readJournal(root).records.filter((r) => r.kind === "prompt");
  expect(prompts).toHaveLength(1);
  expect(Object.keys(prompts[0]!).sort()).toEqual(["kind", "session", "time"]);
});
