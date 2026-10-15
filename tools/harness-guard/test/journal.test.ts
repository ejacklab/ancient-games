import { afterEach, beforeEach, describe, expect, spyOn, test } from "bun:test";
import { execFileSync } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import {
  appendFailure,
  appendRecord,
  failuresFor,
  guardRoot,
  newFailureId,
  readJournal,
  recordFailureFromArgs,
  validateFailure,
  writeEvidence,
} from "../src/journal.ts";
import type { FailureRecord, GuardErrorRecord, JournalRecord, TouchedRecord } from "../src/types.ts";

const secret = "SECRET-PLANT-7f3a9c";
let folder: string;

beforeEach(() => {
  folder = fs.mkdtempSync(path.join(os.tmpdir(), "hg-"));
});

afterEach(() => {
  fs.rmSync(folder, { recursive: true, force: true });
});

function writeFile(name: string, text: string): string {
  const file = path.join(folder, name);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, text);
  return file;
}

function failure(changes: Partial<FailureRecord> = {}): FailureRecord {
  writeFile("proof.json", JSON.stringify({ stdoutLength: 0, exitCode: 1 }));
  return {
    kind: "failure",
    id: "F-1a2b3c4d",
    time: "2026-10-15T08:00:00.000Z",
    session: "session-a",
    found_by: "guard",
    check: "R12.1-empty-output",
    input: "codex answer.txt",
    expected: "non-empty output",
    actual: "empty output",
    engine: "codex",
    harness: "claude-code",
    reason: "the output file has no non-whitespace content",
    evidence: "proof.json",
    ...changes,
  };
}

function journalText(): string {
  const file = path.join(folder, ".harness-guard", "journal.jsonl");
  return fs.existsSync(file) ? fs.readFileSync(file, "utf8") : "";
}

function expectRejected(record: unknown): void {
  const problems: string[] = validateFailure(record, folder);
  expect(problems.length).toBeGreaterThan(0);
  const before = journalText();
  let thrown: unknown;
  try {
    appendFailure(folder, record as FailureRecord);
  } catch (error) {
    thrown = error;
  }
  expect(thrown).toBeInstanceOf(Error);
  if (!(thrown instanceof Error)) return;
  expect(thrown.name).toBe("JournalError");
  for (const problem of problems) expect(thrown.message).toContain(problem);
  expect(journalText()).toBe(before);
}

function cliArgs(): string[] {
  return [
    "--check", "R12.1-empty-output",
    "--input", "codex answer.txt",
    "--expected", "non-empty output",
    "--actual", "empty output",
    "--reason", "the output file has no non-whitespace content",
    "--evidence", "proof.json",
    "--found-by", "worker",
    "--engine", "codex",
    "--harness", "claude-code",
    "--session", "session-cli",
  ];
}

function expectNoSecret(action: () => unknown): void {
  const printed: string[] = [];
  const spies = [
    spyOn(console, "log").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
    spyOn(console, "warn").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
    spyOn(console, "error").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
    spyOn(process.stdout, "write").mockImplementation((chunk) => { printed.push(String(chunk)); return true; }),
    spyOn(process.stderr, "write").mockImplementation((chunk) => { printed.push(String(chunk)); return true; }),
  ];
  let output: unknown;
  let thrown: unknown;
  try {
    output = action();
  } catch (error) {
    thrown = error;
  } finally {
    for (const spy of spies) spy.mockRestore();
  }
  expect(String(JSON.stringify(output))).not.toContain(secret);
  expect(String(thrown)).not.toContain(secret);
  expect(printed.join("\n")).not.toContain(secret);
  const state = path.join(folder, ".harness-guard");
  if (fs.existsSync(state)) {
    for (const name of fs.readdirSync(state, { recursive: true, encoding: "utf8" })) {
      const file = path.join(state, name);
      expect(name).not.toContain(secret);
      if (fs.statSync(file).isFile()) expect(fs.readFileSync(file, "utf8")).not.toContain(secret);
    }
  }
}

describe("guardRoot", () => {
  test("root: a nested cwd uses its own git top-level", () => {
    const repo = path.join(folder, "repo");
    const nested = path.join(repo, "one", "two");
    fs.mkdirSync(nested, { recursive: true });
    execFileSync("git", ["init", "--quiet", repo], { cwd: folder });
    expect(fs.realpathSync(guardRoot(nested))).toBe(fs.realpathSync(repo));
  });

  test("root: a failed git lookup falls back to the supplied cwd", () => {
    writeFile(".git", "gitdir: missing-git-directory\n");
    expect(guardRoot(folder)).toBe(folder);
  });

  test("root: a nonexistent cwd is returned when git cannot run there", () => {
    const missing = path.join(folder, "missing");
    expect(guardRoot(missing)).toBe(missing);
  });
});

describe("newFailureId", () => {
  test("id: each generated id has F- and eight lowercase hex digits", () => {
    const ids = Array.from({ length: 64 }, () => newFailureId());
    for (const id of ids) expect(id).toMatch(/^F-[0-9a-f]{8}$/);
    expect(new Set(ids).size).toBe(ids.length);
  });
});

describe("validateFailure and appendFailure", () => {
  test("validation: a complete failure with root-relative evidence is valid", () => {
    expect(validateFailure(failure(), folder)).toEqual([]);
  });

  test("validation: existing absolute evidence and none session and engine are valid", () => {
    const record = failure({ session: "none", engine: "none", evidence: writeFile("absolute.json", "{}") });
    expect(validateFailure(record, folder)).toEqual([]);
    expect(appendFailure(folder, record)).toEqual(record);
  });

  test("validation: an ISO time with a timezone offset is valid", () => {
    expect(validateFailure(failure({ time: "2026-10-15T16:00:00+08:00" }), folder)).toEqual([]);
  });

  test("validation: unknown extra fields do not invalidate a failure", () => {
    const record = { ...failure(), attempt: 1, extra: { ruleIds: ["R12.1-empty-output"] } };
    expect(validateFailure(record, folder)).toEqual([]);
    expect(() => appendFailure(folder, record)).not.toThrow();
    expect(readJournal(folder).records).toHaveLength(1);
  });

  test.each(["kind", "id", "time", "session", "found_by", "check", "input", "expected", "actual", "engine", "harness", "reason", "evidence"])(
    "validation: a missing %s is rejected without an append",
    (field: string) => {
      const record: Record<string, unknown> = { ...failure() };
      delete record[field];
      expectRejected(record);
    },
  );

  test.each(["session", "found_by", "check", "input", "expected", "actual", "engine", "harness", "reason", "evidence"])(
    "validation: an empty %s is rejected without an append",
    (field: string) => { expectRejected({ ...failure(), [field]: "" }); },
  );

  test.each(["kind", "id", "time", "session", "found_by", "check", "input", "expected", "actual", "engine", "harness", "reason", "evidence"])(
    "validation: a non-string %s is rejected without an append",
    (field: string) => { expectRejected({ ...failure(), [field]: 7 }); },
  );

  test.each([" ", "\t\n\r "])("validation: a whitespace-only reason %j is rejected", (reason: string) => {
    expectRejected(failure({ reason }));
  });

  test.each(["F-1234567", "F-123456789", "F-ABCDEF12", "F-1234567g", "f-12345678", "prefix-F-12345678", "F-12345678-suffix"])(
    "validation: malformed id %s is rejected",
    (id: string) => { expectRejected(failure({ id })); },
  );

  test.each(["", "not-a-time", "10/15/2026 08:00:00", "2026-99-99T88:00:00Z"])(
    "validation: non-ISO time %j is rejected",
    (time: string) => { expectRejected(failure({ time })); },
  );

  test("validation: another record kind is not a failure", () => {
    expectRejected({ ...failure(), kind: "touched" });
  });

  test.each([null, undefined, 7, "failure", [], {}])("validation: non-record input %j reports problems without crashing", (record: unknown) => {
    expectRejected(record);
  });

  test("validation: a nonexistent relative evidence path is rejected", () => {
    expectRejected(failure({ evidence: "missing/proof.json" }));
  });

  test("validation: a nonexistent absolute evidence path is rejected", () => {
    expectRejected(failure({ evidence: path.join(folder, "missing.json") }));
  });

  test("validation: a guard-found record cannot be appended without evidence", () => {
    const record: Record<string, unknown> = { ...failure({ found_by: "guard" }) };
    delete record.evidence;
    expectRejected(record);
  });

  test("append: validation reports every problem and preserves prior journal bytes", () => {
    const valid = failure();
    appendFailure(folder, valid);
    expectRejected({ ...failure({ id: "F-5e6f7a8b" }), reason: "\t", evidence: "missing.json" });
    expect(readJournal(folder)).toEqual({ records: [valid], badLines: 0 });
  });

  test("append: folders are created and a valid failure is returned and stored on one JSON line", () => {
    const record = failure({ reason: "first line\nsecond line" });
    expect(fs.existsSync(path.join(folder, ".harness-guard"))).toBe(false);
    expect(appendFailure(folder, record)).toEqual(record);
    const text = journalText();
    expect(text.endsWith("\n")).toBe(true);
    const lines = text.trimEnd().split("\n");
    expect(lines).toHaveLength(1);
    expect(JSON.parse(lines[0]!)).toEqual(record);
    expect(readJournal(folder)).toEqual({ records: [record], badLines: 0 });
  });

  test("append: two failures preserve both lines and the previous journal prefix", () => {
    const first = failure();
    const second = failure({ id: "F-5e6f7a8b", session: "session-b" });
    appendFailure(folder, first);
    const prefix = journalText();
    appendFailure(folder, second);
    expect(journalText().startsWith(prefix)).toBe(true);
    expect(journalText().trimEnd().split("\n").map((line: string) => JSON.parse(line))).toEqual([first, second]);
    expect(readJournal(folder)).toEqual({ records: [first, second], badLines: 0 });
  });

  test("append: a rejected record does not leak planted prompt or output text", () => {
    const record: Record<string, unknown> = {
      ...failure(), input: secret, actual: secret, stdout: secret, stderr: secret,
    };
    delete record.reason;
    expectNoSecret(() => appendFailure(folder, record as unknown as FailureRecord));
    expect(journalText()).toBe("");
  });
});

describe("writeEvidence", () => {
  test("evidence: creates the id JSON file and returns its root-relative path", () => {
    const facts = { stdoutLength: 0, stderrLength: 24, exitCode: 1, ruleIds: ["R12.1-exit"] };
    const relative: string = writeEvidence(folder, "F-1a2b3c4d", facts);
    expect(path.isAbsolute(relative)).toBe(false);
    expect(path.normalize(relative)).toBe(path.join(".harness-guard", "evidence", "F-1a2b3c4d.json"));
    expect(JSON.parse(fs.readFileSync(path.resolve(folder, relative), "utf8"))).toEqual(facts);
  });

  test("evidence: a guard-found failure references an existing evidence file", () => {
    const facts = { stdoutLength: 0, exitCode: 0, ruleIds: ["R12.1-empty-output"] };
    const evidence = writeEvidence(folder, "F-1a2b3c4d", facts);
    const record = failure({ found_by: "guard", evidence });
    appendFailure(folder, record);
    const stored = failuresFor(folder, null);
    expect(stored).toEqual([record]);
    expect(fs.existsSync(path.resolve(folder, stored[0]!.evidence))).toBe(true);
    expect(JSON.parse(fs.readFileSync(path.resolve(folder, stored[0]!.evidence), "utf8"))).toEqual(facts);
  });

  test("evidence: planted raw stdout, stderr, prompts and config values never escape", () => {
    expectNoSecret(() => writeEvidence(folder, "F-1a2b3c4d", {
      stdoutLength: secret.length,
      stderrLength: secret.length,
      stdout: secret,
      stderr: secret,
      prompt: secret,
      config: { token: secret },
    }));
  });
});

describe("appendRecord and readJournal", () => {
  test("read: a missing journal has no records or bad lines and creates no state", () => {
    expect(readJournal(folder)).toEqual({ records: [], badLines: 0 });
    expect(fs.existsSync(path.join(folder, ".harness-guard"))).toBe(false);
  });

  test("read: an empty journal has no records or bad lines", () => {
    writeFile(".harness-guard/journal.jsonl", "");
    expect(readJournal(folder)).toEqual({ records: [], badLines: 0 });
  });

  test("append: touched and guard_error records need no evidence and keep their order", () => {
    const touched: TouchedRecord = {
      kind: "touched", time: "2026-10-15T08:00:00Z", session: "session-a", path: "cases.register.yaml",
    };
    const error: GuardErrorRecord = {
      kind: "guard_error", time: "2026-10-15T08:00:01Z", session: "session-a", message: "journal write failed",
    };
    appendRecord(folder, touched);
    const prefix = journalText();
    appendRecord(folder, error);
    expect(journalText().startsWith(prefix)).toBe(true);
    expect(journalText().trimEnd().split("\n").map((line: string) => JSON.parse(line))).toEqual([touched, error]);
    expect(readJournal(folder)).toEqual({ records: [touched, error], badLines: 0 });
    expect(fs.existsSync(path.join(folder, ".harness-guard", "evidence"))).toBe(false);
  });

  test("append: a guard error never leaks planted raw stderr", () => {
    const record: GuardErrorRecord = {
      kind: "guard_error", time: "2026-10-15T08:00:00Z", session: "session-a", message: `stderr: ${secret}`,
    };
    expectNoSecret(() => appendRecord(folder, record));
  });

  test("read: malformed lines are counted and valid records on either side survive", () => {
    const first = failure();
    const touched: TouchedRecord = {
      kind: "touched", time: first.time, session: first.session, path: "cases.register.yaml",
    };
    const last = failure({ id: "F-5e6f7a8b" });
    const text = [JSON.stringify(first), "{broken", JSON.stringify(touched), "not JSON", JSON.stringify(last)].join("\n") + "\n";
    writeFile(".harness-guard/journal.jsonl", text);
    expect(readJournal(folder)).toEqual({ records: [first, touched, last], badLines: 2 });
    expect(journalText()).toBe(text);
  });

  test("read: a malformed final line does not hide a complete record before it", () => {
    const record = failure();
    writeFile(".harness-guard/journal.jsonl", JSON.stringify(record) + '\n{"kind":');
    expect(readJournal(folder)).toEqual({ records: [record], badLines: 1 });
  });
});

describe("failuresFor", () => {
  test("sessions: a missing journal returns no failures for null or a named session", () => {
    expect(failuresFor(folder, null)).toEqual([]);
    expect(failuresFor(folder, "session-a")).toEqual([]);
  });

  test("sessions: null returns all failures and a session returns only its failures", () => {
    const first = failure();
    const other = failure({ id: "F-5e6f7a8b", session: "session-b" });
    const last = failure({ id: "F-00112233" });
    const none = failure({ id: "F-44556677", session: "none" });
    const records: JournalRecord[] = [
      first,
      { kind: "touched", time: first.time, session: first.session, path: "cases.register.yaml" },
      other,
      { kind: "guard_error", time: first.time, session: first.session, message: "guard failed" },
      last,
      none,
    ];
    writeFile(".harness-guard/journal.jsonl", records.map((record: JournalRecord) => JSON.stringify(record)).join("\n") + "\n{broken\n");
    expect(failuresFor(folder, null)).toEqual([first, other, last, none]);
    expect(failuresFor(folder, "session-a")).toEqual([first, last]);
    expect(failuresFor(folder, "session-b")).toEqual([other]);
    expect(failuresFor(folder, "none")).toEqual([none]);
    expect(failuresFor(folder, "missing-session")).toEqual([]);
  });
});

describe("recordFailureFromArgs", () => {
  test("cli: every specified flag is used in the appended failure", () => {
    failure();
    recordFailureFromArgs(folder, cliArgs());
    const journal = readJournal(folder);
    expect(journal.badLines).toBe(0);
    expect(journal.records).toHaveLength(1);
    const record = journal.records[0]!;
    expect(record).toMatchObject({
      kind: "failure", session: "session-cli", found_by: "worker", engine: "codex", harness: "claude-code",
      check: "R12.1-empty-output", input: "codex answer.txt", expected: "non-empty output", actual: "empty output",
      reason: "the output file has no non-whitespace content", evidence: "proof.json",
    });
    expect(validateFailure(record, folder)).toEqual([]);
    if (record.kind !== "failure") return;
    expect(record.id).toMatch(/^F-[0-9a-f]{8}$/);
    expect(Number.isNaN(Date.parse(record.time))).toBe(false);
  });

  test.each(["--reason", "--evidence"])("cli: missing %s is an error with no default or append", (flag: string) => {
    failure();
    const args = cliArgs();
    args.splice(args.indexOf(flag), 2);
    expect(() => recordFailureFromArgs(folder, args)).toThrow();
    expect(journalText()).toBe("");
  });

  test.each(["--reason", "--evidence"])("cli: empty %s is rejected without an append", (flag: string) => {
    failure();
    const args = cliArgs();
    args[args.indexOf(flag) + 1] = "";
    expect(() => recordFailureFromArgs(folder, args)).toThrow();
    expect(journalText()).toBe("");
  });

  test("cli: whitespace-only reason is rejected without an append", () => {
    failure();
    const args = cliArgs();
    args[args.indexOf("--reason") + 1] = " \n\t";
    expect(() => recordFailureFromArgs(folder, args)).toThrow();
    expect(journalText()).toBe("");
  });

  test("cli: a missing evidence file is rejected without an append", () => {
    failure();
    const args = cliArgs();
    args[args.indexOf("--evidence") + 1] = "missing.json";
    expect(() => recordFailureFromArgs(folder, args)).toThrow();
    expect(journalText()).toBe("");
  });

  test("cli: a usage error never echoes planted prompt, output or config values", () => {
    failure();
    const args = cliArgs();
    args[args.indexOf("--input") + 1] = secret;
    args[args.indexOf("--actual") + 1] = secret;
    args.splice(args.indexOf("--reason"), 2);
    expectNoSecret(() => recordFailureFromArgs(folder, args));
    expect(journalText()).toBe("");
  });
});
