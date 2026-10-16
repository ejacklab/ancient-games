// Written by the COO for Round 9: the guard fails only where a meaning is written down; where it can only guess it
// warns, and the agent settles each warning — logged as a failure, or dismissed with a recorded one-line reason.
import { expect, test } from "bun:test";
import { execSync, spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { handleHook } from "../src/hooks.ts";
import { readJournal } from "../src/journal.ts";
import { dismiss, openWarnings, settleAsFailure, warnings } from "../src/warnings.ts";

const CLI = path.resolve(import.meta.dirname, "../src/cli.ts");

function box() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "hg-"));
  execSync("git init -q", { cwd: root });
  let clock = 1_000_000;
  const env = { cwd: root, running: [], now: () => new Date((clock += 1000)) };
  const post = (payload: Record<string, unknown>) => handleHook({ session_id: "s", cwd: root, ...payload }, env);
  const kinds = (kind: string) => readJournal(root).records.filter((r) => r.kind === kind);
  const stop = (message = "done") => post({ hook_event_name: "Stop", stop_hook_active: false, last_assistant_message: message });
  const cli = (...args: string[]) => spawnSync(process.execPath, [CLI, ...args], {
    cwd: root, encoding: "utf8", env: { ...process.env, BUN_RUNTIME_TRANSPILER_CACHE_PATH: "0" } });
  return { root, post, kinds, stop, cli };
}

function failedCall(post: (p: Record<string, unknown>) => unknown, command: string, exitCode: number) {
  post({ hook_event_name: "PostToolUseFailure", tool_name: "Bash", tool_input: { command }, exit_code: exitCode, error: "x" });
}

const warningId = (b: ReturnType<typeof box>) => {
  const [w] = b.kinds("warning");
  if (w === undefined || w.kind !== "warning") throw new Error("no warning");
  return w.id;
};

test.each([["grep needle absent.txt", 1], ["git diff --quiet", 1], ["make", 2]])(
  "a command whose exit codes the guard does not know is a warning, not a failure: %s exit %d",
  (command: string, exitCode: number) => {
    const b = box();
    failedCall(b.post, command, exitCode);
    expect(b.kinds("failure")).toHaveLength(0);
    expect(b.kinds("warning")).toHaveLength(1);
  },
);

test("a written meaning is still a failure: a test run that failed", () => {
  const b = box();
  failedCall(b.post, "pytest -q", 1);
  expect(b.kinds("failure")).toHaveLength(1);
  expect(b.kinds("warning")).toHaveLength(0);
});

test("a written meaning is still a failure: an engine call with no output file (R12.1)", () => {
  const b = box();
  b.post({ hook_event_name: "PostToolUse", tool_name: "Bash", tool_input: { command: "codex exec x -o missing.md </dev/null" },
    tool_response: { stdout: "", stderr: "", interrupted: false } });
  expect(b.kinds("failure").length).toBeGreaterThan(0);
  expect(b.kinds("warning")).toHaveLength(0);
});

test("an open warning blocks every stop until it is settled; a dismissal ends it and keeps the reason", () => {
  const b = box();
  failedCall(b.post, "grep x y", 1);
  const id = warningId(b);
  for (let i = 0; i < 2; i++) {
    const out = JSON.parse(b.stop().stdout);
    expect(out.decision).toBe("block");
    expect(out.reason).toContain(id);
  }
  dismiss(b.root, id, "grep found no match, which was the expected answer", new Date());
  expect(b.stop().stdout).toBe("");
  expect(warnings(b.root, "s")).toEqual([expect.objectContaining({ settled: { state: "dismissed", reason: "grep found no match, which was the expected answer" } })]);
});

test("a warning logged as a failure becomes an open failure that needs an insight, and cites the warning", () => {
  const b = box();
  failedCall(b.post, "make", 2);
  const id = warningId(b);
  const failure = settleAsFailure(b.root, id, "the build broke on my edit", new Date(), () => "F-0000abcd");
  expect(failure).toMatchObject({ kind: "failure", from: id, found_by: "agent", reason: "the build broke on my edit", check: "R12.2-command-error" });
  expect(openWarnings(b.root, "s")).toEqual([]);
  const out = JSON.parse(b.stop().stdout);
  expect(out.decision).toBe("block");
  expect(out.reason).toContain("F-0000abcd");
});

test.each([[""], ["   "], ["two\nlines"]])("a settlement needs a one-line reason: %j", (reason: string) => {
  const b = box();
  failedCall(b.post, "make", 2);
  const id = warningId(b);
  expect(() => dismiss(b.root, id, reason, new Date())).toThrow();
  expect(() => settleAsFailure(b.root, id, reason, new Date(), () => "F-0000abcd")).toThrow();
  expect(openWarnings(b.root, "s")).toHaveLength(1);
});

test("a warning is settled once; an unknown id is refused", () => {
  const b = box();
  failedCall(b.post, "make", 2);
  const id = warningId(b);
  dismiss(b.root, id, "expected", new Date());
  expect(() => dismiss(b.root, id, "again", new Date())).toThrow();
  expect(() => settleAsFailure(b.root, id, "late", new Date(), () => "F-0000abcd")).toThrow();
  expect(() => dismiss(b.root, "W-00000000", "none", new Date())).toThrow();
});

test("CLI: warning dismiss and warning fail settle; warnings lists each with its state; exit 1 while one is open", () => {
  const b = box();
  failedCall(b.post, "make", 2);
  failedCall(b.post, "grep x y", 1);
  const ids = b.kinds("warning").map((w) => (w.kind === "warning" ? w.id : ""));
  expect(b.cli("warnings").status).toBe(1);
  expect(b.cli("warning", ids[1]!, "dismiss", "--reason", "no match was the answer").status).toBe(0);
  const logged = b.cli("warning", ids[0]!, "fail", "--reason", "the build broke");
  expect(logged.status).toBe(0);
  expect(logged.stdout).toMatch(/logged as F-[0-9a-f]{8}/);
  const list = b.cli("warnings");
  expect(list.status).toBe(0);
  expect(list.stdout).toContain("dismissed: no match was the answer");
  expect(list.stdout).toMatch(new RegExp(`${ids[0]} .*failure F-[0-9a-f]{8}`));
  expect(b.cli("warning", ids[1]!, "dismiss", "--reason", "again").status).toBe(1);
});

test.each([[["warning"]], [["warning", "W-1"]], [["warning", "W-0000abcd", "maybe", "--reason", "x"]], [["warning", "W-0000abcd", "dismiss"]]])(
  "CLI: a malformed warning command is a usage error: %j",
  (args: string[]) => {
    expect(box().cli(...args).status).toBe(2);
  },
);

test("late criteria are a warning, not a failure", () => {
  const b = box();
  b.post({ hook_event_name: "UserPromptSubmit", prompt: "r" });
  b.post({ hook_event_name: "PostToolUse", tool_name: "Bash", tool_input: { command: "pytest -q" },
    tool_response: { stdout: "3 passed in 0.01s\n", stderr: "", interrupted: false } });
  const file = path.join(b.root, ".harness-guard", "criteria", "c.yaml");
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, "criteria: 1\nsession: s\nrequest: r\nitems:\n  - id: C1\n    text: t\n    met: true\n    evidence: e\n");
  b.post({ hook_event_name: "PostToolUse", tool_name: "Write", tool_input: { file_path: file }, tool_response: {} });
  const out = JSON.parse(b.stop().stdout);
  expect(out.decision).toBe("block");
  expect(b.kinds("failure")).toHaveLength(0);
  expect(b.kinds("warning")).toHaveLength(1);
});
