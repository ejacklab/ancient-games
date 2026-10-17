// Acceptance expectations come from SPEC.md Round 14, Q1–Q3 (the tests item a code-changing request's criteria carry).
import { afterEach, beforeEach, expect, test } from "bun:test";
import { execFileSync, spawnSync } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { checkCriteria, loadCriteria, skeleton } from "../src/criteria.ts";
import { handleHook } from "../src/hooks.ts";
import type { HookEnv } from "../src/types.ts";

// The wording SPEC Q1 fixes, typed here once more so a change to the source shows as a failing test.
const WORDING = "the tests of new behaviour fail on the old code and pass on the new; the tests that pin unchanged behaviour pass on both, and mutants show they bite";
const cli = path.resolve(import.meta.dir, "../src/cli.ts");
let root: string;

beforeEach(() => {
  root = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), "hg-round14-")));
  execFileSync("git", ["init", "--quiet"], { cwd: root });
});
afterEach(() => fs.rmSync(root, { recursive: true, force: true }));

function criteriaNew(args: string[]): { exitCode: number | null; out: string; file: string } {
  const file = path.join(root, "runs/run/criteria.yaml");
  const result = spawnSync(process.execPath, [cli, "criteria", "new", ...args, "--out", "runs/run/criteria.yaml"],
    { cwd: root, encoding: "utf8", timeout: 10000 });
  return { exitCode: result.status, out: `${result.stdout}${result.stderr}`, file };
}

test("criteria new --code writes the tests item with the standard wording, unmarked", () => {
  const result = criteriaNew(["--code", "--session", "s14", "--request", "change the code"]);
  expect(result.exitCode).toBe(0);
  const loaded = loadCriteria(result.file);
  const tests = loaded.items.find((item) => item.id === "tests");
  expect(tests?.text).toBe(WORDING);
  expect(typeof tests?.met).not.toBe("boolean");
  expect(loaded.items.map((item) => item.id)).toEqual(["C1", "C2", "tests"]);
  // The placeholders are empty until the agent fills them; the tests item is complete as written.
  expect(checkCriteria(loaded).filter((finding) => finding.message.includes("tests"))).toEqual([]);
});

test("criteria new without --code writes the two placeholders only, as before", () => {
  const result = criteriaNew(["--session", "s14", "--request", "write a document"]);
  expect(result.exitCode).toBe(0);
  const loaded = loadCriteria(result.file);
  expect(loaded.items.map((item) => item.id)).toEqual(["C1", "C2"]);
  expect(fs.readFileSync(result.file, "utf8")).not.toContain("fail on the old code");
});

test("criteria new --from-register --code adds the tests item after the register's units", () => {
  fs.writeFileSync(path.join(root, "register.yaml"), [
    "register: 1",
    "use_cases:",
    "  - id: UC1",
    "    origin: user",
    "    purpose: keep the saved file",
    '    fails_if: ["the file is lost"]',
    '    min_acceptance: ["reopens"]',
    "",
  ].join("\n"));
  const result = criteriaNew(["--from-register", "register.yaml", "--code", "--session", "s14"]);
  expect(result.exitCode).toBe(0);
  const items = loadCriteria(result.file).items;
  expect(items.at(-1)?.id).toBe("tests");
  expect(items.at(-1)?.text).toBe(WORDING);
  expect(typeof items.at(-1)?.met).not.toBe("boolean");
  expect(items.length).toBeGreaterThan(1);
});

test("the skeleton's header says each item must be markable before the task ends (F-336edcb0)", () => {
  const text = skeleton("s14", "any request");
  expect(text).toContain("one you can mark before the task ends");
  expect(text).toContain("a use expected later goes in the success path or the next task's criteria");
});

test("the reminder at the start of a request names --code", () => {
  const env: HookEnv = { cwd: root, running: [], now: () => new Date("2026-10-17T06:00:00.000Z") };
  const result = handleHook({ hook_event_name: "UserPromptSubmit", session_id: "s14", cwd: root, prompt: "go" }, env);
  const context = String(JSON.parse(result.stdout).hookSpecificOutput.additionalContext);
  expect(context).toContain("before you start, write the criteria this request will be scored on");
  expect(context).toContain("`--code` when the request changes code");
});
