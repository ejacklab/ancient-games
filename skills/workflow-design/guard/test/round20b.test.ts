// Acceptance checks written from SPEC.md "Round 20, after its review" (CR1a, DL5), independently of the implementation.
// CR1a: a deferred criteria step is no result at all; the stop goes on to the path ask exactly as with no criteria file.
// DL5: `deadline wait --mark` is a usage error (exit 2) with --id or --run too, before anything waits.
import { afterEach, expect, test } from "bun:test";
import { execFileSync, spawnSync } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { handleHook } from "../src/hooks.ts";
import { appendRecord, readJournal } from "../src/journal.ts";
import type { CriteriaFile, Criterion, Deadline, FailureRecord, HookEnv, HookResult, SuccessRecord } from "../src/types.ts";

const CLI = path.resolve(import.meta.dirname, "../src/cli.ts");
const session = "round20b-session";
const file = "runs/task/criteria.yaml";
const EPOCH = Date.parse("2026-10-18T02:00:00.000Z");
const roots: string[] = [];
afterEach(() => {
  for (const root of roots.splice(0)) fs.rmSync(root, { recursive: true, force: true });
});

// ---- CR1a ----------------------------------------------------------------------------------------------------------

const MET: Criterion[] = [{ id: "C1", text: "the first thing", met: true, evidence: "checked" }];
const UNMARKED: Criterion[] = [{ id: "C1", text: "the first thing" }];

// One repository: optionally a 10-min deadline of the session started at EPOCH, a criteria file the session wrote
// (or none), and a success journal record with check test-run; then a Stop 2 minutes in.
function scenario(opts: { deadline: boolean; items: Criterion[] | null }) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "hg-round20b-"));
  roots.push(root);
  execFileSync("git", ["init", "--quiet"], { cwd: root });
  let tick = EPOCH;
  const env: HookEnv = { cwd: root, running: [], now: () => new Date(tick) };
  const write = (relative: string, text: string) => {
    const target = path.join(root, relative);
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, text);
  };
  const invoke = (payload: Record<string, unknown>): HookResult => {
    const result = handleHook({ session_id: session, cwd: root, ...payload }, env);
    expect(result.exitCode).toBe(0);
    expect(result.stderr).toBe("");
    return result;
  };
  if (opts.deadline) {
    const deadline: Deadline = { id: "D-0000c1a0", start: new Date(EPOCH).toISOString(), minutes: 10, run: "runs/task", session };
    write(`.harness-guard/deadlines/${deadline.id}.json`, JSON.stringify(deadline));
  }
  if (opts.items !== null) {
    const value: CriteriaFile = { criteria: 1, session, request: "the request", items: opts.items };
    write(file, JSON.stringify(value));
    invoke({ hook_event_name: "PostToolUse", tool_name: "Write",
      tool_input: { file_path: path.join(root, file), content: "x" }, tool_response: {} });
  }
  tick = EPOCH + 60_000;
  const success: SuccessRecord = { kind: "success", time: new Date(tick).toISOString(), session, check: "test-run", engine: "bun" };
  appendRecord(root, success);
  tick = EPOCH + 2 * 60_000;
  const stop = invoke({ hook_event_name: "Stop", last_assistant_message: "done", stop_hook_active: false });
  const criterionFailures = readJournal(root).records
    .filter((r): r is FailureRecord => r.kind === "failure" && r.check.startsWith("criterion:"));
  return { stop, criterionFailures };
}

function pathAskReason(result: HookResult): string {
  expect(result.stdout.trim()).not.toBe("");
  const output = JSON.parse(result.stdout);
  expect(output.decision).toBe("block");
  expect(output.reason).toContain("harness-guard: record the path of this task");
  expect(output.reason).toContain("path new --session " + session);
  return output.reason;
}

test("CR1a: inside an open, not-up deadline, met criteria and a success record get the path ask at Stop, as with no deadline", () => {
  const withDeadline = scenario({ deadline: true, items: MET });
  const without = scenario({ deadline: false, items: MET });
  const reason = pathAskReason(withDeadline.stop);
  expect(reason).toBe(pathAskReason(without.stop));
});

test("CR1a: the deferred stop asks for the path exactly as a session that touched no criteria file", () => {
  const deferred = scenario({ deadline: true, items: MET });
  const noCriteria = scenario({ deadline: true, items: null });
  expect(pathAskReason(deferred.stop)).toBe(pathAskReason(noCriteria.stop));
});

test("CR1a: only the criteria step waits: unmarked criteria inside the deadline still get the path ask, no criteria block, no criterion failure", () => {
  const { stop, criterionFailures } = scenario({ deadline: true, items: UNMARKED });
  const reason = pathAskReason(stop);
  expect(reason).not.toContain("mark each criterion met: true|false with evidence");
  expect(criterionFailures).toEqual([]);
});

// ---- DL5 -----------------------------------------------------------------------------------------------------------

// A budget of centuries: a wait that started would be killed by the 10 s spawn timeout.
const LONG = 100_000_000;

function box() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "hg-r20b-deadline-"));
  roots.push(root);
  execFileSync("git", ["init", "-q"], { cwd: root });
  const deadline: Deadline = { id: "D-0000d150", start: "2000-01-01T00:00:00.000Z", minutes: LONG, run: "runs/a", session: "s" };
  const target = path.join(root, `.harness-guard/deadlines/${deadline.id}.json`);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, JSON.stringify(deadline));
  const cli = (...args: string[]) => spawnSync(process.execPath, [CLI, ...args], {
    cwd: root, encoding: "utf8", timeout: 10_000,
    env: { ...process.env, BUN_RUNTIME_TRANSPILER_CACHE_PATH: "0", TZ: Intl.DateTimeFormat().resolvedOptions().timeZone },
  });
  return { cli, id: deadline.id };
}

test.each([["--id"], ["--run"], ["none"]])("DL5: deadline wait %s … --mark 50 exits 2 with the --mark message and does not wait", (flag: string) => {
  const b = box();
  const named = flag === "--id" ? ["--id", b.id] : flag === "--run" ? ["--run", "runs/a"] : [];
  const started = Date.now();
  const result = b.cli("deadline", "wait", ...named, "--mark", "50");
  expect(result.error).toBeUndefined(); // a wait on the centuries-long deadline would be killed by the 10 s timeout
  expect(Date.now() - started).toBeLessThan(9_000);
  expect(result.status).toBe(2);
  expect(result.stderr).toContain("--mark was removed");
}, 15_000);
