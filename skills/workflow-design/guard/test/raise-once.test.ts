// Written by the COO (round 4, D6) after the guard asked this session to name its insight at every stop.
import { expect, test } from "bun:test";
import { execSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { handleHook } from "../src/hooks.ts";
import { appendFailure, newFailureId, writeEvidence } from "../src/journal.ts";

function setup() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "hg-"));
  execSync("git init -q", { cwd: root });
  const env = { cwd: root, running: [], now: () => new Date() };
  const log = () => {
    const id = newFailureId();
    const evidence = writeEvidence(root, id, { exit: 1 });
    appendFailure(root, { kind: "failure", id, time: new Date().toISOString(), session: "s1", found_by: "evaluator", check: "c", input: "i", expected: "e", actual: "a", engine: "none", harness: "claude-code", reason: "r", evidence });
    return id;
  };
  const answer = (ids: string[]) => {
    fs.mkdirSync(path.join(root, ".harness-guard", "insights"), { recursive: true });
    fs.writeFileSync(path.join(root, ".harness-guard", "insights", "i.md"), ids.map((id) => `## ${id}\nWhys:\n1. a\n2. b\n3. c\nSource: check\nRoot cause: x\nOptions:\n1. [rule] y evidence: z\n2. [tool] w evidence: v\n`).join("\n"));
  };
  const stop = (message: string) => handleHook({ hook_event_name: "Stop", session_id: "s1", stop_hook_active: false, last_assistant_message: message }, env).stdout;
  return { log, answer, stop };
}

test("raise once: after a final message names the insight, a later stop need not name it again", () => {
  const { log, answer, stop } = setup();
  const a = log(); answer([a]);
  expect(stop("done")).toContain("raise the insight");
  expect(stop("see .harness-guard/insights/i.md")).toBe("");
  expect(stop("another unrelated reply")).toBe("");
});

test("raise once: a new failure after the raise must be raised again", () => {
  const { log, answer, stop } = setup();
  const a = log(); answer([a]);
  expect(stop("see .harness-guard/insights/i.md")).toBe("");
  const b = log(); answer([a, b]);
  expect(stop("later reply")).toContain("raise the insight");
  expect(stop("updated .harness-guard/insights/i.md")).toBe("");
});
