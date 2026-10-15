import { afterEach, beforeEach, describe, expect, spyOn, test } from "bun:test";
import * as fs from "node:fs";
import * as path from "node:path";
import { checkPath, findPathFiles, loadPath, parents, skeleton } from "../src/paths.ts";
import type { FailureRecord, JournalRecord, PathReport, SuccessPath, SuccessRecord } from "../src/types.ts";

const secret = "SECRET-PLANT-7f3a9c";
let folder: string;
let root: string;

beforeEach(() => {
  folder = fs.mkdtempSync(path.join(import.meta.dir, ".round5-paths-"));
  root = path.join(folder, "root");
  fs.mkdirSync(root);
});

afterEach(() => {
  fs.rmSync(folder, { recursive: true, force: true });
});

function writeFile(name: string, text: string): string {
  const file = path.join(root, name);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, text);
  return file;
}

function successPath(changes: Partial<SuccessPath> = {}): SuccessPath {
  return {
    path: 1,
    session: "session-a",
    category: "implementation",
    objective: "Deliver a checked change",
    steps: [{ did: "Run acceptance tests", engine: "bun", check: "all tests pass" }],
    decisions: ["Use the existing interface"],
    measures: { seconds: 100, failures: 0, successes: 2 },
    failures: [],
    ...changes,
  };
}

function writePath(name: string, value: Record<string, unknown> | SuccessPath): string {
  // JSON values on YAML mapping lines keep planted strings and nested fixtures unambiguous.
  return writeFile(name, Object.entries(value).filter(([, item]) => item !== undefined)
    .map(([key, item]) => `${key}: ${JSON.stringify(item)}`).join("\n") + "\n");
}

function reportFor(file: string): PathReport {
  return checkPath(root, path.relative(root, file));
}

function expectFail(report: PathReport, rule: string): void {
  expect(report.findings).toContainEqual(expect.objectContaining({ rule, severity: "fail" }));
}

function expectNoFail(report: PathReport): void {
  expect(report.findings.filter((finding) => finding.severity === "fail")).toEqual([]);
}

function writeChild(changes: Partial<SuccessPath> = {}, parentChanges: Partial<SuccessPath> = {}): string {
  writePath("runs/20261014/success-path.yaml", successPath(parentChanges));
  return writePath("runs/20261015/success-path.yaml", successPath({
    parent: "runs/20261014/success-path.yaml",
    change: "Remove a redundant check",
    aim: { measure: "seconds", parent_value: 100, lower_is_better: true },
    measures: { seconds: 99, failures: 0, successes: 2 },
    ...changes,
  }));
}

function success(changes: Partial<SuccessRecord> = {}): SuccessRecord {
  return { kind: "success", time: "2026-10-15T08:00:00Z", session: "session-a", check: "test-run", engine: "bun", ...changes };
}

function failure(changes: Partial<FailureRecord> = {}): FailureRecord {
  return {
    kind: "failure", id: "F-1a2b3c4d", time: "2026-10-15T08:00:00Z", session: "session-a",
    found_by: "guard", check: "R12.2-test-failed", input: "bun run", expected: "all tests pass",
    actual: "1 failed", engine: "bun", harness: "claude-code", reason: "tests failed", evidence: "proof.json",
    ...changes,
  };
}

function writeJournal(records: JournalRecord[]): string {
  return writeFile(".harness-guard/journal.jsonl", records.map((record) => JSON.stringify(record)).join("\n") + "\n");
}

describe("S3 findPathFiles and loadPath", () => {
  test("a root with no path files returns an empty list", () => {
    expect(findPathFiles(root)).toEqual([]);
  });

  test("discovers only specified YAML locations, including zero and many run folders, sorted and relative", () => {
    const included = [
      "runs/z/deep/success-path-2.yaml", "runs/success-path.yaml", "runs/a/success-path-one.yaml",
      ".harness-guard/paths/z.yaml", ".harness-guard/paths/a.yaml",
    ];
    for (const name of included) writePath(name, successPath());
    for (const name of [
      "success-path.yaml", "other/success-path.yaml", "runs/a/path.yaml", "runs/a/success-path.yml",
      "runs/a/success-path.yaml.bak", ".harness-guard/paths/nested/hidden.yaml", ".harness-guard/paths/a.yml",
    ]) writePath(name, successPath());
    expect(findPathFiles(root)).toEqual([...included].sort());
    expect(findPathFiles(root).every((file) => !path.isAbsolute(file))).toBe(true);
  });

  test("loads a complete YAML path without losing optional fields", () => {
    const value = successPath({ parent: "runs/old/success-path.yaml", change: "Reuse a fixture",
      aim: { measure: "seconds", parent_value: 100, lower_is_better: true },
      great: { comparison: "Quicker than the parent", evidence: "proof.json" } });
    const loaded: SuccessPath = loadPath(writePath("runs/run/success-path.yaml", value));
    expect(loaded).toEqual(value);
  });

  test.each([["path: [unterminated\n"], ["session: session-a\n"], ["path: 2\n"], ["path: '1'\n"], [""], ["null\n"], ["[]\n"]])(
    "malformed YAML or a missing numeric path version throws PathError: %j", (text: string) => {
      const file = writeFile("runs/run/success-path.yaml", text);
      let thrown: unknown;
      try { loadPath(file); } catch (error) { thrown = error; }
      expect(thrown).toBeInstanceOf(Error);
      expect((thrown as Error).name).toBe("PathError");
    },
  );
});

describe("S3 checkPath required fields", () => {
  test("a complete standalone path passes and has no comparison", () => {
    const file = writePath("runs/run/success-path.yaml", successPath());
    const report: PathReport = reportFor(file);
    expect(report.findings).toEqual([]);
    expect(report.better).toBeNull();
    expect(report.gainPercent).toBeNull();
    expect(report.repeatedFailures).toEqual([]);
  });

  test.each([["session"], ["category"], ["objective"], ["steps"], ["measures"]])(
    "missing %s fails", (field: string) => {
      const value: Record<string, unknown> = { ...successPath() };
      delete value[field];
      expectFail(reportFor(writePath("runs/run/success-path.yaml", value)), "R12.7-path-missing");
    },
  );

  test.each([
    [{ session: "" }], [{ session: " \t" }], [{ category: "" }], [{ category: " \t" }],
    [{ objective: "" }], [{ objective: " \t" }], [{ steps: [] }], [{ steps: [{}] }],
    [{ steps: [{ did: "" }] }], [{ steps: [{ did: " \t" }] }],
    [{ steps: [{ did: "valid" }, { did: "" }] }], [{ measures: {} }], [{ measures: { seconds: "100" } }],
  ])("empty required field or absence of numeric measures fails: %j", (changes: Record<string, unknown>) => {
    expectFail(reportFor(writePath("runs/run/success-path.yaml", { ...successPath(), ...changes })), "R12.7-path-missing");
  });

  test("zero is a valid numeric measure", () => {
    expectNoFail(reportFor(writePath("runs/run/success-path.yaml", successPath({ measures: { failures: 0 } }))));
  });
});

describe("S3 child paths", () => {
  test.each([[undefined], [""], [" \t"]])("a copied child with change %j fails", (change: string | undefined) => {
    expectFail(reportFor(writeChild({ change })), "R12.7-copied");
  });

  test("a nonexistent parent fails", () => {
    expectFail(reportFor(writeChild({ parent: "runs/missing/success-path.yaml" })), "R12.7-parent-missing");
  });

  test.each([["path: [broken\n"], ["path: 2\n"]])("a parent that cannot load fails: %j", (text: string) => {
    const file = writeChild();
    writeFile("runs/20261014/success-path.yaml", text);
    expectFail(reportFor(file), "R12.7-parent-missing");
  });

  test("a child without an aim fails and has null gain and better", () => {
    const report = reportFor(writeChild({ aim: undefined }));
    expectFail(report, "R12.7-aim-missing");
    expect(report.gainPercent).toBeNull();
    expect(report.better).toBeNull();
  });

  test.each([[""], ["absent"]])("an aim naming no shared measure fails: %j", (measure: string) => {
    expectFail(reportFor(writeChild({ aim: { measure, parent_value: 100, lower_is_better: true } })), "R12.7-aim-missing");
  });

  test("an aim measure absent only from the child fails", () => {
    expectFail(reportFor(writeChild({ measures: { successes: 3 } })), "R12.7-aim-missing");
  });

  test("an aim measure absent only from the parent fails", () => {
    expectFail(reportFor(writeChild({}, { measures: { successes: 2 } })), "R12.7-aim-missing");
  });

  test("an aim parent value different from the parent's recorded value fails", () => {
    expectFail(reportFor(writeChild({ aim: { measure: "seconds", parent_value: 101, lower_is_better: true } })), "R12.7-aim-mismatch");
  });

  test("a 1% gain is better with an aim warning and no fail findings", () => {
    const report = reportFor(writeChild());
    expectNoFail(report);
    expect(report.gainPercent).toBe(1);
    expect(report.better).toBe(true);
    expect(report.findings).toContainEqual(expect.objectContaining({ rule: "R12.7-aim-report", severity: "warn" }));
    expect(report.findings.find((finding) => finding.rule === "R12.7-aim-report")!.message).toMatch(/gain 1(?:\.0)?% against a 2% aim/);
  });

  test.each([[96.86, 3.1, true], [104, -4, false], [100, 0, false]])(
    "lower-is-better child value %s reports gain %s and better %s", (seconds: number, gain: number, better: boolean) => {
      const report = reportFor(writeChild({ measures: { seconds } }));
      expectNoFail(report);
      expect(report.gainPercent).toBe(gain);
      expect(report.better).toBe(better);
      expect(report.findings).toContainEqual(expect.objectContaining({ rule: "R12.7-aim-report", severity: "warn" }));
      const message = report.findings.find((finding) => finding.rule === "R12.7-aim-report")!.message.replaceAll("−", "-");
      expect(message).toMatch(new RegExp(`gain ${gain}(?:\\.0)?% against a 2% aim`));
    },
  );

  test("higher-is-better reverses the gain calculation and rounds to one decimal", () => {
    const report = reportFor(writeChild({ measures: { seconds: 103.14 },
      aim: { measure: "seconds", parent_value: 100, lower_is_better: false } }));
    expectNoFail(report);
    expect(report.gainPercent).toBe(3.1);
    expect(report.better).toBe(true);
  });

  test("a zero parent measure gives null gain and better", () => {
    const report = reportFor(writeChild({ measures: { seconds: 1 },
      aim: { measure: "seconds", parent_value: 0, lower_is_better: false } }, { measures: { seconds: 0 } }));
    expectNoFail(report);
    expect(report.gainPercent).toBeNull();
    expect(report.better).toBeNull();
  });

  test("an improved child repeating a parent check failure is not better", () => {
    const report = reportFor(writeChild({ failures: ["R12.2-test-failed", "R12.1-exit"] },
      { failures: ["R12.2-test-failed", "trap:codex-stdin"] }));
    expect(report.gainPercent).toBe(1);
    expect(report.repeatedFailures).toEqual(["R12.2-test-failed"]);
    expect(report.better).toBe(false);
  });

  test("different child failures do not count as repeated failures", () => {
    const report = reportFor(writeChild({ failures: ["R12.1-exit"] }, { failures: ["R12.2-test-failed"] }));
    expect(report.repeatedFailures).toEqual([]);
    expect(report.better).toBe(true);
  });
});

describe("S3 great success evidence", () => {
  test.each([
    [{ comparison: "", evidence: "proof.json" }], [{ comparison: " \t", evidence: "proof.json" }],
    [{ comparison: "Faster", evidence: "" }], [{ comparison: "Faster", evidence: " \t" }],
    [{ comparison: "Faster", evidence: "missing.json" }], [{}],
  ])("a great success with absent comparison or existing evidence fails: %j", (great: Record<string, string>) => {
    writeFile("proof.json", "{}");
    const file = writePath("runs/run/success-path.yaml", { ...successPath(), great });
    expectFail(reportFor(file), "R12.7-great-evidence");
  });

  test("a great success with comparison and existing root-relative evidence passes", () => {
    writeFile("proof/result.json", "{}");
    const file = writePath("runs/run/success-path.yaml", successPath({ great: { comparison: "Less time for the same objective", evidence: "proof/result.json" } }));
    expectNoFail(reportFor(file));
  });
});

describe("S3 skeleton", () => {
  test("a missing journal produces zero session counts and empty placeholders", () => {
    const text: string = skeleton(root, "session-a");
    const value = Bun.YAML.parse(text) as SuccessPath;
    expect(value.path).toBe(1);
    expect(value.session).toBe("session-a");
    expect(value.measures).toMatchObject({ failures: 0, successes: 0 });
    expect(value.failures).toEqual([]);
    expect(value.category).toBe("");
    expect(value.objective).toBe("");
    expect(value.steps.every((step) => step.did.trim() === "")).toBe(true);
    expect(value.decisions === undefined || value.decisions.every((decision) => decision.trim() === "")).toBe(true);
  });

  test("counts only this session's successes and failures, and uses check ids rather than failure ids", () => {
    writeJournal([
      success(), success({ check: "engine-call", engine: "codex" }), success({ session: "other" }),
      failure(), failure({ id: "F-5e6f7a8b", check: "R12.1-exit" }), failure({ session: "other" }),
      { kind: "raised", time: "2026-10-15T08:00:00Z", session: "session-a", ids: ["path"] },
      { kind: "touched", time: "2026-10-15T08:00:00Z", session: "session-a", path: "register.yaml" },
      { kind: "guard_error", time: "2026-10-15T08:00:00Z", session: "session-a", message: "unreadable file" },
    ]);
    const value = Bun.YAML.parse(skeleton(root, "session-a")) as SuccessPath;
    expect(value.measures).toMatchObject({ failures: 2, successes: 2 });
    expect(value.failures).toEqual(["R12.2-test-failed", "R12.1-exit"]);
  });

  test("a malformed journal line does not lose valid session counts", () => {
    const journal = writeJournal([success(), failure()]);
    fs.appendFileSync(journal, "{broken\n");
    const value = Bun.YAML.parse(skeleton(root, "session-a")) as SuccessPath;
    expect(value.measures).toMatchObject({ failures: 1, successes: 1 });
  });

  test("out writes the returned skeleton inside the root and creates folders", () => {
    writeJournal([success()]);
    const out = "runs/new/success-path.yaml";
    const text = skeleton(root, "session-a", out);
    expect(fs.readFileSync(path.join(root, out), "utf8")).toBe(text);
    expect(loadPath(path.join(root, out)).session).toBe("session-a");
  });

  test.each([["relative"], ["absolute"]])("out never creates or overwrites an outside-root %s path", (kind: string) => {
    const outside = path.join(folder, "outside.yaml");
    fs.writeFileSync(outside, "keep this content\n");
    const out = kind === "relative" ? "../outside.yaml" : outside;
    try { skeleton(root, "session-a", out); } catch { /* Rejection style is not specified. */ }
    expect(fs.readFileSync(outside, "utf8")).toBe("keep this content\n");
    fs.rmSync(outside);
    try { skeleton(root, "session-a", out); } catch { /* Only the write boundary is contractual. */ }
    expect(fs.existsSync(outside)).toBe(false);
  });

  test("journal command, prompt and output content never enters the skeleton, printed output or generated file", () => {
    const journal = writeJournal([{
      ...failure({ input: secret, actual: secret, reason: secret }),
      command: secret, prompt: secret, stdout: secret, stderr: secret,
    } as FailureRecord, success()]);
    const journalBefore = fs.readFileSync(journal, "utf8");
    const printed: string[] = [];
    const spies = [
      spyOn(console, "log").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
      spyOn(console, "warn").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
      spyOn(console, "error").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
      spyOn(process.stdout, "write").mockImplementation((chunk) => { printed.push(String(chunk)); return true; }),
      spyOn(process.stderr, "write").mockImplementation((chunk) => { printed.push(String(chunk)); return true; }),
    ];
    let text = "";
    try { text = skeleton(root, "session-a", "runs/new/success-path.yaml"); }
    finally { for (const spy of spies) spy.mockRestore(); }
    expect(text).not.toContain(secret);
    expect(printed.join("\n")).not.toContain(secret);
    expect(fs.readFileSync(path.join(root, "runs/new/success-path.yaml"), "utf8")).not.toContain(secret);
    expect(fs.readFileSync(journal, "utf8")).toBe(journalBefore);
  });
});

describe("S3 parents", () => {
  test("an absent category has no parents", () => {
    expect(parents(root, "implementation")).toEqual([]);
  });

  test("filters category, returns measures and better, and orders recent filenames last", () => {
    const parent = "runs/20261014/success-path.yaml";
    const child = "runs/20261015/success-path.yaml";
    writeChild();
    writePath("runs/20261016/success-path.yaml", successPath({ category: "research" }));
    // Deliberately invert modification time: the contract orders by filename.
    fs.utimesSync(path.join(root, parent), new Date("2026-10-16"), new Date("2026-10-16"));
    fs.utimesSync(path.join(root, child), new Date("2026-10-14"), new Date("2026-10-14"));
    expect(parents(root, "implementation")).toEqual([
      { file: parent, measures: { seconds: 100, failures: 0, successes: 2 }, better: null },
      { file: child, measures: { seconds: 99, failures: 0, successes: 2 }, better: true },
    ]);
  });

  test("includes guard-directory path files and preserves a repeated-failure better verdict", () => {
    writeChild({ failures: ["R12.2-test-failed"] }, { failures: ["R12.2-test-failed"] });
    writePath(".harness-guard/paths/local.yaml", successPath({ measures: { successes: 5 } }));
    const rows = parents(root, "implementation");
    expect(rows.map((row) => row.file)).toEqual([
      ".harness-guard/paths/local.yaml", "runs/20261014/success-path.yaml", "runs/20261015/success-path.yaml",
    ]);
    expect(rows[0]).toEqual({ file: ".harness-guard/paths/local.yaml", measures: { successes: 5 }, better: null });
    expect(rows[2]!.better).toBe(false);
  });
});
