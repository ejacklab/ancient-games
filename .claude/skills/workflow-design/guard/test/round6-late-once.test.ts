// Written by the COO after a surviving mutant (round 6): the late-criteria record is written once per file, not at every stop.
import { expect, test } from "bun:test";
import { execSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { handleHook } from "../src/hooks.ts";
import { readJournal } from "../src/journal.ts";

test("K2: late criteria leave exactly one R12.7-criteria-late record across several stops", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "hg-"));
  execSync("git init -q", { cwd: root });
  let clock = 1_000_000;
  const env = { cwd: root, running: [], now: () => new Date((clock += 1000)) };
  const post = (payload: Record<string, unknown>) => handleHook({ session_id: "s", cwd: root, ...payload }, env);
  // the work comes first: a green test run
  post({ hook_event_name: "PostToolUse", tool_name: "Bash", tool_input: { command: "pytest -q" }, tool_response: { stdout: "3 passed in 0.01s\n", stderr: "", interrupted: false } });
  // then the criteria file, all met
  const file = path.join(root, ".harness-guard", "criteria", "c.yaml");
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, "criteria: 1\nsession: s\nrequest: r\nitems:\n  - id: C1\n    text: t\n    met: true\n    evidence: e\n");
  post({ hook_event_name: "PostToolUse", tool_name: "Write", tool_input: { file_path: file }, tool_response: {} });
  post({ hook_event_name: "Stop", stop_hook_active: false, last_assistant_message: "done" });
  // answer the late failure, then stop again: the criteria step runs again and must not write a second late record
  const first = readJournal(root).records.filter((r) => r.kind === "failure" && r.check === "R12.7-criteria-late");
  expect(first).toHaveLength(1);
  const insight = path.join(root, ".harness-guard", "insights", "i.md");
  fs.mkdirSync(path.dirname(insight), { recursive: true });
  fs.writeFileSync(insight, `## ${first[0]!.kind === "failure" ? first[0]!.id : ""}\nWhys:\n1. a\n2. b\n3. c\nSource: instruction\nRoot cause: x\nOptions:\n1. [rule] y evidence: z\n2. [tool] w evidence: v\n`);
  for (let i = 0; i < 3; i++) post({ hook_event_name: "Stop", stop_hook_active: false, last_assistant_message: "see .harness-guard/insights/i.md" });
  const late = readJournal(root).records.filter((r) => r.kind === "failure" && r.check === "R12.7-criteria-late");
  expect(late).toHaveLength(1);
});
