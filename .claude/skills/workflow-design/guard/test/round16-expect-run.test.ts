// Acceptance expectations come from SPEC.md Round 16, X1–X4 (the guard runs the declared red run itself).
import { afterEach, beforeEach, expect, test } from "bun:test";
import { execFileSync, spawnSync } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { handleHook } from "../src/hooks.ts";
import { readJournal } from "../src/journal.ts";
import type { FailureRecord, HookEnv, JournalRecord, RedRecord } from "../src/types.ts";

const cli = path.resolve(import.meta.dirname, "..", "src", "cli.ts");
const session = "round16-session";
let root: string;

beforeEach(() => {
  root = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), "hg-round16-")));
  execFileSync("git", ["init", "--quiet"], { cwd: root });
  fs.mkdirSync(path.join(root, "t"));
  fs.writeFileSync(path.join(root, "t/fail.test.ts"),
    'import { test } from "bun:test";\ntest("new behaviour", () => { console.log("STDOUT-LINE"); throw new Error("not built yet"); });\n');
  fs.writeFileSync(path.join(root, "t/pass.test.ts"), 'import { expect, test } from "bun:test";\ntest("pin", () => { expect(1).toBe(1); });\n');
});
afterEach(() => fs.rmSync(root, { recursive: true, force: true }));

function run(args: string[]) {
  const result = spawnSync(process.execPath, [cli, "expect-fail", ...args, "--session", session],
    { cwd: root, encoding: "utf8", timeout: 60000, env: { ...process.env, BUN_RUNTIME_TRANSPILER_CACHE_PATH: "0" } });
  return { exitCode: result.status, out: `${result.stdout}${result.stderr}` };
}

function records(kind: string): JournalRecord[] {
  return readJournal(root).records.filter((record) => record.kind === kind);
}

test("a declared run that fails is a red record with the runner's own exit, and its whole output is in the file", () => {
  const result = run(["--run", "bun test ./t/fail.test.ts", "--out", "runs/r/red.txt"]);
  expect(result.exitCode).toBe(0);
  const declared = records("expect-fail");
  expect(declared.map((record) => (record as { file: string }).file)).toEqual(["t/fail.test.ts"]);
  const reds = records("red") as RedRecord[];
  expect(reds).toHaveLength(1);
  expect(reds[0]!.declared).toEqual(declared.map((record) => (record as { id: string }).id));
  expect(reds[0]!.runner).toBe("bun test");
  expect(reds[0]!.exit).toBe(1);
  expect(records("failure")).toEqual([]);
  const output = fs.readFileSync(path.join(root, "runs/r/red.txt"), "utf8");
  expect(output).toContain("not built yet"); // bun's report, on stderr
  expect(output).toContain("STDOUT-LINE"); // the test's own stdout
});

test("a declared run that passes is one R12.2-red-passed failure, with the output file as its evidence", () => {
  const result = run(["--run", "bun test ./t/pass.test.ts", "--out", "runs/r/passed.txt"]);
  expect(result.exitCode).toBe(1);
  expect(result.out).toContain("R12.2-red-passed");
  const failures = records("failure") as FailureRecord[];
  expect(failures).toHaveLength(1);
  expect(failures[0]!.check).toBe("R12.2-red-passed");
  expect(failures[0]!.evidence).toBe("runs/r/passed.txt");
  expect(failures[0]!.declared).toEqual(records("expect-fail").map((record) => (record as { id: string }).id));
  expect(records("red")).toEqual([]);
});

test("that call's exit 1 is not logged again by the hook", () => {
  const env: HookEnv = { cwd: root, running: [], now: () => new Date("2026-10-17T07:00:00.000Z") };
  handleHook({
    hook_event_name: "PostToolUseFailure", session_id: session, cwd: root, tool_name: "Bash",
    tool_input: { command: `bun ${cli} expect-fail --run "bun test ./t/pass.test.ts" --out runs/r/passed.txt` },
    error: "Exit code 1\nexpect-fail --run: bun test exited 0", is_interrupt: false,
  }, env);
  expect(records("failure")).toEqual([]);
  expect(records("warning")).toEqual([]); // an unknown command's non-zero exit is a warning (Round 9); this one is answered
});

test("a command that is not one test run naming its files, or that writes outside the root, is refused and runs nothing", () => {
  for (const [args, message] of [
    [["--run", "echo hi > t/ran.txt", "--out", "runs/r/x.txt"], "not a test run"],
    [["--run", "bun test ./t/pass.test.ts; touch t/ran.txt", "--out", "runs/r/x.txt"], "the test command alone"],
    [["--run", "bun test ./t/fail.test.ts | tail -3", "--out", "runs/r/x.txt"], "the test command alone"],
    [["--run", "bun test", "--out", "runs/r/x.txt"], "names no test file"],
    [["--run", "bun test ./t/fail.test.ts", "--out", `../${path.basename(root)}-outside.txt`], "--out must be inside the root"],
    [["--run", "bun test ./t/fail.test.ts"], "needs --out FILE"],
  ] as [string[], string][]) {
    const result = run(args);
    expect(result.exitCode).toBe(2);
    expect(result.out).toContain(message);
  }
  expect(fs.existsSync(path.join(root, "t/ran.txt"))).toBe(false);
  expect(fs.existsSync(path.join(root, "runs"))).toBe(false);
  // A name of this test's own, so an earlier run's file (a mutant's, F-59498b2a) cannot stand in for one.
  expect(fs.existsSync(`${root}-outside.txt`)).toBe(false);
  expect(readJournal(root).records).toEqual([]);
});

test("--tests without --run declares as before and runs nothing", () => {
  const result = run(["--tests", "t/fail.test.ts"]);
  expect(result.exitCode).toBe(0);
  expect(records("expect-fail")).toHaveLength(1);
  expect(records("red")).toEqual([]);
});
