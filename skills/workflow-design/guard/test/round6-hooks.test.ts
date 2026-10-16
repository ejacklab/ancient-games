// Acceptance expectations come from SPEC.md K2/K3, S1/S5 and D6.
import { afterEach, beforeEach, describe, expect, test } from "bun:test";
import { execFileSync } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { handleHook } from "../src/hooks.ts";
import { readJournal } from "../src/journal.ts";
import { skeleton } from "../src/paths.ts";
import type { CriteriaFile, Criterion, FailureRecord, HookEnv, HookResult, JournalRecord, SuccessPath, WarningRecord } from "../src/types.ts";

const secret = "SECRET-PLANT-7f3a9c";
const session = "round6-session";
const file = "runs/task/criteria.yaml";
let root: string;
let env: HookEnv;
let tick: number;

beforeEach(() => {
  root = fs.mkdtempSync(path.join(os.tmpdir(), "hg-round6-"));
  execFileSync("git", ["init", "--quiet"], { cwd: root });
  tick = Date.parse("2026-10-15T15:00:00.000Z");
  env = { cwd: root, running: [], now: () => new Date(tick) };
});
afterEach(() => fs.rmSync(root, { recursive: true, force: true }));

function write(relative: string, text: string): void {
  const target = path.join(root, relative);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, text);
}

function privateOutput(text: string): void {
  expect(text).not.toContain(secret);
  const state = path.join(root, ".harness-guard");
  if (!fs.existsSync(state)) return;
  for (const relative of fs.readdirSync(state, { recursive: true, encoding: "utf8" })) {
    expect(relative).not.toContain(secret);
    const target = path.join(state, relative);
    if (fs.statSync(target).isFile()) expect(fs.readFileSync(target, "utf8")).not.toContain(secret);
  }
}

function invoke(payload: Record<string, unknown>, selectedSession = session): HookResult {
  tick += 1000;
  const result = handleHook({ session_id: selectedSession, cwd: root, ...payload }, env);
  privateOutput(JSON.stringify(result));
  expect(result.exitCode).toBe(0);
  expect(result.stderr).toBe("");
  return result;
}

function records(): JournalRecord[] {
  const result = readJournal(root);
  expect(result.badLines).toBe(0);
  return result.records;
}

function failures(check?: string): FailureRecord[] {
  return records().filter((r): r is FailureRecord => r.kind === "failure" && (!check || r.check === check));
}

// Round 9 (COO): late criteria are a timing guess, so they are warnings, not failures.
function lateWarnings(): WarningRecord[] {
  return records().filter((r): r is WarningRecord => r.kind === "warning" && r.check === "R12.7-criteria-late");
}

function criteria(items: Criterion[] = [{ id: "C1", text: `criterion ${secret}`, met: true, evidence: "checked" }], relative = file, selectedSession = session): void {
  const value: CriteriaFile = { criteria: 1, session: selectedSession, request: `request ${secret}`, items };
  write(relative, JSON.stringify(value));
}

function touch(relative = file, tool = "Write", selectedSession = session): HookResult {
  return invoke({ hook_event_name: "PostToolUse", tool_name: tool,
    tool_input: { file_path: path.join(root, relative), content: secret }, tool_response: { output: secret } }, selectedSession);
}

function prompt(selectedSession = session): HookResult {
  return invoke({ hook_event_name: "UserPromptSubmit", prompt: `request ${secret}` }, selectedSession);
}

function stop(message = "done", selectedSession = session): HookResult {
  return invoke({ hook_event_name: "Stop", last_assistant_message: message, stop_hook_active: false }, selectedSession);
}

function blocked(result: HookResult): string {
  const value = JSON.parse(result.stdout);
  expect(value.decision).toBe("block");
  return value.reason;
}

function bash(passing = true, selectedSession = session): HookResult {
  return invoke({ hook_event_name: passing ? "PostToolUse" : "PostToolUseFailure", tool_name: "Bash",
    tool_input: { command: `pytest -q '${secret}'` },
    tool_response: { stdout: `1 passed ${secret}`, stderr: secret },
    ...(passing ? {} : { exit_code: 1, error: `exit 1 ${secret}` }) }, selectedSession);
}

function answer(ids: string[]): string {
  const insight = "runs/task/insight.md";
  write(insight, `## ${ids.join(", ")}\nWhys:\n1. input was unchecked\n2. check was absent\n3. instruction omitted the check\nSource: instruction\nRoot cause: missing check\nOptions:\n1. [check] add validation evidence: fixture\n2. [tool] validate input evidence: fixture\n`);
  return insight;
}

function pathSkeleton(selectedSession = session): SuccessPath {
  const text = skeleton(root, selectedSession);
  privateOutput(text);
  return Bun.YAML.parse(text) as SuccessPath;
}

describe("K2 criteria reminder and touch", () => {
  test("Fails-if: reminder repeats; first prompt gives the specified context and one marker", () => {
    const result = prompt();
    const context = JSON.parse(result.stdout).hookSpecificOutput;
    expect(context.hookEventName).toBe("UserPromptSubmit");
    expect(context.additionalContext).toContain("before you start, write the criteria this request will be scored on");
    expect(context.additionalContext).toContain("criteria new --out runs/<run>/criteria.yaml");
    expect(context.additionalContext).toContain(".harness-guard/criteria/<name>.yaml");
    expect(context.additionalContext).toContain("one item per thing the result must get right");
    expect(context.additionalContext).toContain("mark each met or not met with evidence at the end");
    // Round 10 (T6): the first prompt may also ask for the time; this test is about the criteria reminder.
    expect(prompt().stdout).not.toContain("criteria this request");
    // Round 8: every prompt also writes a time-only prompt record; the reminder's marker is still written once.
    expect(records().filter((r) => r.kind !== "prompt" && !(r.kind === "raised" && r.ids.includes("deadline-ask"))).map((r) => ({ ...r, time: "" })))
      .toEqual([{ kind: "raised", session, time: "", ids: ["criteria"] }]);
    expect(records().filter((r) => r.kind === "prompt")).toHaveLength(2);
  });

  test.each([["Write"], ["Edit"], ["MultiEdit"]])("Fails-if: touched criteria still gets reminder (%s)", (tool: string) => {
    criteria();
    expect(touch(file, tool).stdout).toBe("");
    expect(records()).toEqual([{ kind: "touched", session, time: new Date(tick).toISOString(), path: file }]);
    expect(prompt().stdout).not.toContain("criteria this request");
    expect(records().filter((r) => r.kind === "raised" && r.ids.includes("criteria"))).toEqual([]);
  });

  test("another session's reminder and touches do not consume this session's reminder", () => {
    prompt("other");
    criteria(undefined, file, "other");
    touch(file, "Write", "other");
    expect(prompt().stdout).not.toBe("");
    expect(prompt().stdout).toBe("");
  });

  test("a non-criteria touch does not suppress the reminder", () => {
    touch("notes.md");
    expect(prompt().stdout).not.toBe("");
  });
});

describe("K2 Stop criteria validation", () => {
  const invalid: [string, string | Criterion[], string][] = [
    ["unreadable YAML", "criteria: [", ""],
    ["wrong discriminator", JSON.stringify({ criteria: 2, request: secret, items: [] }), ""],
    ["no items", [], "R12.7-criteria-empty"],
    ["blank text", [{ id: "C1", text: "", met: true, evidence: "checked" }], "R12.7-criterion-text"],
    ["blank id", [{ id: "", text: secret }], "R12.7-criterion-text"],
    ["duplicate ids", [{ id: "C1", text: secret }, { id: "C1", text: secret }], "R12.7-criterion-text"],
    ["missing true evidence", [{ id: "C1", text: secret, met: true }], "R12.7-criterion-evidence"],
    ["missing false evidence", [{ id: "C1", text: secret, met: false }], "R12.7-criterion-evidence"],
    ["absent mark", [{ id: "C1", text: secret }], "C1"],
    ["null mark", [{ id: "C1", text: secret, met: null }], "C1"],
  ];
  for (const [label, input, rule] of invalid) test(`invalid ${label} blocks once without item text`, () => {
    if (typeof input === "string") write(file, input);
    else criteria(input);
    touch();
    const reason = blocked(stop());
    expect(reason).toContain("mark each criterion met: true|false with evidence");
    if (rule) expect(reason).toContain(rule);
    const second = stop();
    if (label === "missing false evidence" && second.stdout) {
      const failure = failures("criterion:C1")[0];
      expect(failure).toBeDefined();
      expect(blocked(second)).toContain(failure!.id);
      expect(second.stdout).not.toContain("mark each criterion met: true|false with evidence");
    } else expect(second.stdout).toBe("");
  });

  test("a changed invalid file state gets a new single block", () => {
    criteria([{ id: "C1", text: secret }]);
    touch();
    blocked(stop());
    expect(stop().stdout).toBe("");
    criteria([{ id: "C2", text: secret }]);
    touch();
    expect(blocked(stop())).toContain("C2");
    expect(stop().stdout).toBe("");
  });

  test("deleted touched files are skipped", () => {
    criteria(); touch(); fs.unlinkSync(path.join(root, file));
    expect(stop().stdout).toBe("");
    expect(failures()).toEqual([]);
  });

  test("another session's touched invalid file does not block", () => {
    criteria([]); touch(file, "Write", "other");
    expect(stop().stdout).toBe("");
  });

  test("valid fully met criteria stop without failures", () => {
    criteria(); touch();
    expect(stop().stdout).toBe("");
    expect(failures()).toEqual([]);
  });

  test("Fails-if: met:false has no failure; repeated Stops block until answered and D6 raises once", () => {
    criteria([{ id: "C1", text: secret, met: false, evidence: "observed mismatch" }]);
    touch();
    const first = stop();
    const [failure] = failures("criterion:C1");
    expect(failure).toBeDefined();
    expect(failure!).toMatchObject({ kind: "failure", session, found_by: "guard", check: "criterion:C1",
      input: path.basename(file), expected: "met", actual: "not met", reason: "a criterion of the task was not met", evidence: file });
    expect(failure!.id).toMatch(/^F-[0-9a-f]{8}$/);
    expect(blocked(first)).toContain(failure!.id);
    expect(blocked(stop())).toContain(failure!.id);
    expect(failures("criterion:C1")).toHaveLength(1);
    const insight = answer([failure!.id]);
    expect(blocked(stop())).toContain("raise the insight");
    expect(stop(`see ${insight}`).stdout).toBe("");
    expect(stop().stdout).toBe("");
    expect(records().some((r) => r.kind === "raised" && r.ids.includes(failure!.id))).toBe(true);
    expect(failures("criterion:C1")).toHaveLength(1);
  });

  test("each unmet id gets one failure even with repeated touch records", () => {
    criteria(["C1", "C2"].map((id) => ({ id, text: secret, met: false, evidence: "checked" })));
    touch(); touch(); stop(); stop();
    expect(failures().map((r) => r.check).sort()).toEqual(["criterion:C1", "criterion:C2"]);
  });

  test("another session's criterion failure does not suppress this session's failure", () => {
    criteria([{ id: "C1", text: secret, met: false, evidence: "checked" }]);
    touch(file, "Write", "other"); stop("done", "other");
    touch(); stop();
    expect(failures("criterion:C1").map((r) => r.session).sort()).toEqual(["other", session].sort());
  });

  test("criteria validation precedes the S5 path ask", () => {
    criteria([{ id: "C1", text: secret }]); touch(); bash();
    expect(blocked(stop())).toContain("C1");
    expect(records().some((r) => r.kind === "raised" && r.ids.includes("path"))).toBe(false);
    criteria(); touch();
    expect(blocked(stop())).toContain("record the path of this task");
    expect(stop().stdout).toBe("");
  });

  test("open failures and the raise check precede criteria validation", () => {
    criteria([{ id: "C1", text: secret }]); touch(); bash(false);
    const failure = failures()[0]!;
    expect(blocked(stop())).toContain(failure.id);
    const insight = answer([failure.id]);
    expect(blocked(stop())).toContain("raise the insight");
    expect(blocked(stop(`see ${insight}`))).toContain("C1");
  });
});

describe("K2 late criteria", () => {
  test.each([[true], [false]])("Fails-if: criteria after a checked result leave no late record (success %s)", (passing: boolean) => {
    bash(passing);
    if (!passing) {
      const insight = answer(failures().map((r) => r.id));
      stop(`see ${insight}`);
    }
    criteria(); touch(); stop();
    expect(lateWarnings()).toHaveLength(1);
    stop(); touch(); stop();
    expect(lateWarnings()).toHaveLength(1);
  });

  test.each([[true], [false]])("criteria touched first never get a late failure (success %s)", (passing: boolean) => {
    criteria(); touch(); bash(passing);
    const ids = failures().map((r) => r.id);
    const message = ids.length ? `see ${answer(ids)}` : "done";
    stop(message);
    expect(lateWarnings()).toEqual([]);
  });

  test("each late file gets a record once", () => {
    bash(); criteria(); touch();
    criteria(undefined, "runs/task/criteria-second.yaml"); touch("runs/task/criteria-second.yaml");
    stop(); stop();
    expect(lateWarnings()).toHaveLength(2);
  });

  test("a later edit uses the first touch time when detecting late criteria", () => {
    criteria(); touch(); bash();
    criteria([{ id: "C1", text: secret, met: true, evidence: "rechecked" }]); touch(file, "Edit");
    stop();
    expect(lateWarnings()).toEqual([]);
  });

  test("another session's checked result does not make criteria late", () => {
    bash(true, "other"); criteria(); touch(); stop();
    expect(lateWarnings()).toEqual([]);
  });

  test("a criterion failure does not make a subsequently touched file late", () => {
    criteria([{ id: "C1", text: secret, met: false, evidence: "checked" }]); touch(); stop();
    const insight = answer(failures().map((r) => r.id));
    criteria(undefined, "runs/task/criteria-second.yaml"); touch("runs/task/criteria-second.yaml");
    stop(`see ${insight}`);
    expect(lateWarnings()).toEqual([]);
  });
});

describe("K3 path skeleton score", () => {
  test("Fails-if: a scored file has no path score; 2 of 3 is 66.7", () => {
    criteria([true, true, false].map((met, i) => ({ id: `C${i}`, text: secret, met, evidence: "checked" })));
    touch();
    expect(pathSkeleton().measures.score).toBe(66.7);
  });

  test("several files contribute their mean percentage, not a pooled item ratio", () => {
    criteria([{ id: "C1", text: secret, met: true, evidence: "checked" }]); touch(); touch();
    const second = "runs/task/criteria-second.yaml";
    criteria([false, false, false].map((met, i) => ({ id: `D${i}`, text: secret, met, evidence: "checked" })), second);
    touch(second);
    expect(pathSkeleton().measures.score).toBe(50);
  });

  test("another session's scored files do not contribute", () => {
    criteria(undefined, file, "other"); touch(file, "Write", "other");
    expect(pathSkeleton().measures).not.toHaveProperty("score");
    expect(pathSkeleton("other").measures.score).toBe(100);
  });

  test("no criteria means no score; zero percent remains a score", () => {
    expect(pathSkeleton().measures).not.toHaveProperty("score");
    criteria([{ id: "C1", text: secret, met: false, evidence: "checked" }]); touch();
    expect(pathSkeleton().measures.score).toBe(0);
  });

  test("scored files are discovered by session even without a touch record", () => {
    criteria();
    expect(pathSkeleton().measures.score).toBe(100);
  });

  test("the written path skeleton includes the same score", () => {
    criteria(); touch();
    const out = "runs/task/success-path.yaml";
    const text = skeleton(root, session, out);
    privateOutput(text);
    const written = fs.readFileSync(path.join(root, out), "utf8");
    privateOutput(written);
    expect((Bun.YAML.parse(written) as SuccessPath).measures.score).toBe(100);
  });

  test("zero items have no scored percentage", () => {
    criteria([]); touch();
    expect(pathSkeleton().measures).not.toHaveProperty("score");
  });
});
