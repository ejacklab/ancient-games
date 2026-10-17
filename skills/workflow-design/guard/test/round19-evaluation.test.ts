// Acceptance expectations come from SPEC.md, Round 19 (V1–V5): the evaluator's verdict reaches the guard. Written by
// the main agent (Claude); the implementation is opencode's.
import { afterEach, beforeEach, expect, test } from "bun:test";
import { execFileSync, spawnSync } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { readJournal } from "../src/journal.ts";
import type { FailureRecord } from "../src/types.ts";

const CLI = path.resolve(import.meta.dirname, "../src/cli.ts");
let root: string;
const run = "runs/20261018-eval";

beforeEach(() => {
  root = fs.mkdtempSync(path.join(os.tmpdir(), "hg-eval-"));
  execFileSync("git", ["init", "--quiet"], { cwd: root });
  fs.mkdirSync(path.join(root, run), { recursive: true });
});
afterEach(() => { fs.rmSync(root, { recursive: true, force: true }); });

const verdict = {
  meets: false,
  counts: { PASS: 1, FAIL: 1, UNKNOWN: 1, out_of_scope: 0 },
  cases: [
    { case: "G1-c1", kind: "executable", verdict: "FAIL", reason: "probe red", repro: "EVAL_PRODUCT=p python3 -m pytest probes/g1.py -k t1" },
    { case: "G2-c1", kind: "judged", verdict: "UNKNOWN", reason: "judging void: plant missed", repro: "" },
    { case: "G3-c1", kind: "static", verdict: "PASS", reason: "", repro: "" },
  ],
  requirements: [
    { id: "R1.1", group: "G1", verdict: "FAIL", reason: "the index omits a file" },
    { id: "R1.2", group: "G2", verdict: "UNKNOWN", reason: "judging void: plant missed" },
    { id: "R1.3", group: "G3", verdict: "PASS", reason: "" },
  ],
  out_of_scope: [], manifest: ["R1.1", "R1.2", "R1.3"],
};

function write(name: string, body: unknown): string {
  const file = path.join(root, run, name);
  fs.writeFileSync(file, typeof body === "string" ? body : JSON.stringify(body));
  return file;
}
function ingest(file: string) {
  return spawnSync(process.execPath, [CLI, "evaluation", "ingest", file, "--run", run, "--session", "s1"], {
    cwd: root, encoding: "utf8", env: { ...process.env, BUN_RUNTIME_TRANSPILER_CACHE_PATH: "0" },
  });
}
const failures = () => readJournal(root).records.filter((r): r is FailureRecord => r.kind === "failure");
const notes = () => { const f = path.join(root, run, "evaluator-notes.md"); return fs.existsSync(f) ? fs.readFileSync(f, "utf8") : ""; };

test("V1: a FAIL requirement becomes one failure found by the evaluator, with the group's repro as evidence", () => {
  const r = ingest(write("verdict.json", verdict));
  expect(r.status).toBe(0);
  const found = failures();
  expect(found).toHaveLength(1);
  expect(found[0]).toMatchObject({ found_by: "evaluator", check: "evaluator:G1", input: "R1.1", expected: "PASS", actual: "FAIL", session: "s1" }); // V6: one per group
  const evidence = fs.readFileSync(path.resolve(root, found[0]!.evidence), "utf8");
  expect(evidence).toContain("R1.1");
  expect(evidence).toContain("probes/g1.py -k t1");
});

test("V2: an UNKNOWN is a note, a PASS writes nothing", () => {
  ingest(write("verdict.json", verdict));
  expect(notes()).toContain("- R1.2 · UNKNOWN · judging void: plant missed");
  expect(notes()).not.toContain("R1.3");
  expect(failures().map((f) => f.input)).toEqual(["R1.1"]);
});

test("V3: ingesting the same verdict again records nothing new", () => {
  const file = write("verdict.json", verdict);
  ingest(file); ingest(file);
  expect(failures()).toHaveLength(1);
  expect(notes().split("R1.2").length - 1).toBe(1);
});

test.each([["missing", null], ["not json", "{oops"], ["no requirements", { meets: false }]])(
  "V4: a %s verdict is a could-not-run note, exit 1, no failure", (_name, body) => {
    const file = body === null ? path.join(root, run, "absent.json") : write("verdict.json", body);
    const r = ingest(file);
    expect(r.status).toBe(1);
    expect(failures()).toEqual([]);
    expect(notes()).toContain("- evaluation · could not run ·");
  },
);

test("V5: one summary line", () => {
  const r = ingest(write("verdict.json", verdict));
  expect(r.stdout.trim()).toBe("evaluation ingest: 1 FAIL recorded, 1 UNKNOWN noted, 1 PASS");
});

// ---- V6, V7: run 20261017-evaluator-wiring round 3, measured on the evaluator's K2 calibration verdicts: one fault
// fails every id of its group, and a group failing before any fault was planted failed in every run.
const grouped = {
  ...verdict,
  requirements: [
    { id: "B1.1", group: "B1", verdict: "FAIL", reason: "r" }, { id: "B1.2", group: "B1", verdict: "FAIL", reason: "r" },
    { id: "B3.1", group: "B3", verdict: "FAIL", reason: "r" }, { id: "B3.2", group: "B3", verdict: "FAIL", reason: "r" },
    { id: "R1.3", group: "G3", verdict: "PASS", reason: "" },
  ],
};
const baseline = { ...verdict, requirements: [{ id: "B1.1", group: "B1", verdict: "FAIL", reason: "r" }, { id: "B1.2", group: "B1", verdict: "FAIL", reason: "r" }] };
function ingestWith(file: string, extra: string[]) {
  return spawnSync(process.execPath, [CLI, "evaluation", "ingest", file, "--run", run, "--session", "s1", ...extra], {
    cwd: root, encoding: "utf8", env: { ...process.env, BUN_RUNTIME_TRANSPILER_CACHE_PATH: "0" },
  });
}

test("V6: one failure per failing group, naming every id of the group", () => {
  ingest(write("verdict.json", grouped));
  const found = failures();
  expect(found.map((f) => f.check).sort()).toEqual(["evaluator:B1", "evaluator:B3"]);
  expect(found.find((f) => f.check === "evaluator:B3")!.input).toBe("B3.1, B3.2");
});

// V7 measured: on K2 run k2-4 the planted fault was a new FAIL case (B1-F1) inside group B1, which already failed in
// the baseline; comparing groups hid it. A group with a FAIL case the baseline did not fail is a new failure.
test("V7: a new FAIL case in a group that already failed in the baseline is still a failure", () => {
  const withCases = (cases: string[]) => ({ ...grouped, cases: cases.map((c) => ({ case: c, kind: "executable", verdict: "FAIL", reason: "r", repro: `repro ${c}` })) });
  const base = write("baseline.json", { ...baseline, cases: [{ case: "B1-F2", kind: "executable", verdict: "FAIL", reason: "r", repro: "x" }] });
  ingestWith(write("verdict.json", withCases(["B1-F1", "B1-F2", "B3-F1"])), ["--baseline", base]);
  expect(failures().map((f) => f.check).sort()).toEqual(["evaluator:B1", "evaluator:B3"]);
});

test("V7: with --baseline, a group that also fails in the baseline is a note, not a failure", () => {
  const base = write("baseline.json", baseline);
  const r = ingestWith(write("verdict.json", grouped), ["--baseline", base]);
  expect(r.status).toBe(0);
  expect(failures().map((f) => f.check)).toEqual(["evaluator:B3"]);
  expect(notes()).toContain("- B1 · FAIL in the baseline too ·");
});
