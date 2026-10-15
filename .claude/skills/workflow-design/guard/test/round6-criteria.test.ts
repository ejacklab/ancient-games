import { afterEach, beforeEach, describe, expect, spyOn, test } from "bun:test";
import * as fs from "node:fs";
import * as path from "node:path";
import {
  checkCriteria, CriteriaError, findCriteriaFiles, fromRegister, isCriteriaFile, loadCriteria, score, skeleton,
} from "../src/criteria.ts";
import type { CriteriaFile, Criterion, Finding, Register, Score } from "../src/types.ts";

const secret = "SECRET-PLANT-7f3a9c";
let root: string;

beforeEach(() => {
  root = fs.mkdtempSync(path.join(import.meta.dir, ".round6-criteria-"));
});

afterEach(() => {
  fs.rmSync(root, { recursive: true, force: true });
});

function writeFile(name: string, text: string): string {
  const file = path.join(root, name);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, text);
  return file;
}

function criteriaFile(items: Criterion[] = [{ id: "C1", text: "Preserve the saved file" }]): CriteriaFile {
  return { criteria: 1, session: "session-a", request: "Check the saved result", items };
}

function writeYaml(name: string, value: object): string {
  // JSON on YAML mapping lines preserves planted strings without hand escaping YAML.
  return writeFile(name, Object.entries(value)
    .map(([key, item]) => `${key}: ${JSON.stringify(item)}`).join("\n") + "\n");
}

function loadItems(items: Criterion[]): CriteriaFile {
  return loadCriteria(writeYaml("runs/run/criteria.yaml", criteriaFile(items)));
}

function expectFailure(findings: Finding[], rule: string): void {
  expect(findings).toContainEqual(expect.objectContaining({ rule, severity: "fail" }));
}

describe("K1 criteria discovery and loading", () => {
  test.each([["criteria.yaml"], ["criteria-next.yaml"], ["criteria2.yaml"], ["any/folder/criteria.yaml"]])(
    "recognises criteria file names in any folder: %s", (name: string) => {
      const file = writeYaml(name, criteriaFile());
      expect(isCriteriaFile(name)).toBe(true);
      expect(isCriteriaFile(file)).toBe(true);
    },
  );

  test.each([["criteria.yml"], ["criteria.yaml.bak"], ["not-criteria.yaml"], ["criteria.yaml/other.yaml"]])(
    "rejects names outside criteria*.yaml: %s", (name: string) => {
      expect(isCriteriaFile(writeYaml(name, criteriaFile()))).toBe(false);
    },
  );

  test("an empty root has no criteria files", () => {
    expect(findCriteriaFiles(root)).toEqual([]);
  });

  test("finds only specified locations, sorted and relative, including zero and many run folders", () => {
    const included = [
      "runs/z/deep/criteria-two.yaml", "runs/criteria.yaml", "runs/a/criteria-one.yaml",
      ".harness-guard/criteria/criteria.yaml", ".harness-guard/criteria/criteria-next.yaml",
      ".harness-guard/criteria/a.yaml", ".harness-guard/criteria/z.yaml",
    ];
    for (const name of included) writeYaml(name, criteriaFile());
    for (const name of [
      "criteria.yaml", "other/criteria.yaml", "runs/a/result.yaml", "runs/a/criteria.yml",
      "runs/a/criteria.yaml.bak", ".harness-guard/criteria/nested/criteria.yaml", ".harness-guard/criteria/a.yml",
    ]) writeYaml(name, criteriaFile());
    const files: string[] = findCriteriaFiles(root);
    expect(files).toEqual([...included].sort());
    expect(files.every((file) => !path.isAbsolute(file))).toBe(true);
  });

  test("loads YAML and preserves false, null, absent marks and evidence", () => {
    const value = criteriaFile([
      { id: "C1", text: "First", met: true, evidence: "runs/run/proof.md" },
      { id: "C2", text: "Second", met: false, evidence: "Observed a mismatch" },
      { id: "C3", text: "Third", met: null }, { id: "C4", text: "Fourth" },
    ]);
    const loaded: CriteriaFile = loadCriteria(writeYaml("runs/run/criteria.yaml", value));
    expect(loaded).toEqual(value);
  });

  test.each([
    ["criteria: [unterminated\n"], ["session: session-a\n"], ["criteria: 2\n"],
    ["criteria: '1'\n"], [""], ["null\n"], ["[]\n"],
  ])("bad YAML or absent numeric version throws CriteriaError: %j", (text: string) => {
    const file = writeFile("runs/run/criteria.yaml", text);
    expect(() => loadCriteria(file)).toThrow(CriteriaError);
  });
});

describe("K1 checkCriteria", () => {
  test("met true with no evidence fails (K1 Fails-if)", () => {
    expectFailure(checkCriteria(loadItems([{ id: "C1", text: "Saved", met: true }])), "R12.7-criterion-evidence");
  });

  test.each([[true, ""], [true, " \t\n"], [false, undefined], [false, ""], [false, " \t\n"]])(
    "boolean met %j requires nonempty evidence %j", (met: boolean, evidence: string | undefined) => {
      expectFailure(checkCriteria(loadItems([{ id: "C1", text: "Saved", met, evidence }])), "R12.7-criterion-evidence");
    },
  );

  test("repeated ids fail even when texts and marks differ (K1 Fails-if)", () => {
    expectFailure(checkCriteria(loadItems([
      { id: "C1", text: "First", met: true, evidence: "proof.md" },
      { id: "C1", text: "Second", met: false, evidence: "Mismatch observed" },
    ])), "R12.7-criterion-text");
  });

  test("no items fails (K1 Fails-if)", () => {
    expectFailure(checkCriteria(loadItems([])), "R12.7-criteria-empty");
  });

  test("an absent items collection fails", () => {
    const file = writeYaml("runs/run/criteria.yaml", { criteria: 1, session: "session-a", request: "No items" });
    expectFailure(checkCriteria(loadCriteria(file)), "R12.7-criteria-empty");
  });

  test.each([["id", undefined], ["id", ""], ["id", " \t"], ["text", undefined], ["text", ""], ["text", " \t"]])(
    "missing or blank item %s fails: %j", (field: string, value: string | undefined) => {
      const item: Record<string, unknown> = { id: "C1", text: "Saved" };
      if (value === undefined) delete item[field];
      else item[field] = value;
      const loaded = loadCriteria(writeYaml("runs/run/criteria.yaml", criteriaFile([item as unknown as Criterion])));
      expectFailure(checkCriteria(loaded), "R12.7-criterion-text");
    },
  );

  test("marked true and false with evidence pass; evidence need not be a path", () => {
    expect(checkCriteria(loadItems([
      { id: "C1", text: "Saved", met: true, evidence: "proof.md" },
      { id: "C2", text: "Reopened", met: false, evidence: "Reopen returned a mismatch" },
    ]))).toEqual([]);
  });

  test("absent and null marks need no evidence at the K1 shape check", () => {
    expect(checkCriteria(loadItems([{ id: "C1", text: "Saved" }, { id: "C2", text: "Reopened", met: null }]))).toEqual([]);
  });
});

describe("K1 score", () => {
  test("2 of 3 met scores 66.7 (K1 Fails-if)", () => {
    const result: Score = score(loadItems([
      { id: "C1", text: "First", met: true, evidence: "proof.md" },
      { id: "C2", text: "Second", met: true, evidence: "proof.md" },
      { id: "C3", text: "Third", met: false, evidence: "Mismatch" },
    ]));
    expect(result).toEqual({ met: 2, total: 3, percent: 66.7, unmarked: [] });
  });

  test("unmarked items stay in total and are reported separately from false (K1 Fails-if)", () => {
    expect(score(loadItems([
      { id: "C1", text: "True", met: true }, { id: "C2", text: "False", met: false },
      { id: "C3", text: "Absent" }, { id: "C4", text: "Null", met: null },
    ]))).toEqual({ met: 1, total: 4, percent: 25, unmarked: ["C3", "C4"] });
  });

  test("nonboolean YAML values are unmarked rather than coerced", () => {
    const items = ["true", "false", 1, 0].map((met, index) => ({ id: `C${index + 1}`, text: "Planted", met }));
    const loaded = loadCriteria(writeYaml("runs/run/criteria.yaml", { ...criteriaFile(), items }));
    expect(score(loaded)).toEqual({ met: 0, total: 4, percent: 0, unmarked: ["C1", "C2", "C3", "C4"] });
  });

  test("no items has null percent", () => {
    expect(score(loadItems([]))).toEqual({ met: 0, total: 0, percent: null, unmarked: [] });
  });

  test.each([[true, 100], [false, 0]])("all marks %j produce percent %s", (met: boolean, percent: number) => {
    expect(score(loadItems([{ id: "C1", text: "Saved", met, evidence: "Observed" }]))).toEqual({
      met: met ? 1 : 0, total: 1, percent, unmarked: [],
    });
  });
});

describe("K1 fromRegister", () => {
  test("converts accepted M4 units, preserving ids and text, excluding declined and unaccepted entries and variants", () => {
    const register: Register = {
      register: 1,
      use_cases: [
        { id: "UC1", origin: "user", safety: true, purpose: "Save", fails_if: ["File IS lost", "Second failure"], min_acceptance: ["Can reopen"] },
        { id: "UC2", origin: "ai", decision: { by: "owner", verdict: "accepted" }, purpose: "Check", fails_if: [" file   is LOST "], min_acceptance: ["Another acceptance"] },
        { id: "UC3", origin: "user", decision: { by: "owner", verdict: "declined" }, fails_if: ["Declined"] },
        { id: "UC4", origin: "ai", fails_if: ["Unaccepted"] },
      ],
      requirements: [
        { id: "RQ1", origin: "user", purpose: "Verify", serves: ["UC1"], fails_if: ["CAN\tREOPEN", "Requirement fails"] },
        { id: "RQ2", origin: "ai", decision: { by: "owner", verdict: "accepted" }, purpose: "Verify more", serves: ["vision"], fails_if: ["Accepted AI requirement"] },
        { id: "RQ3", origin: "ai", fails_if: ["Not binding"] },
        { id: "RQ4", origin: "user", decision: { by: "owner", verdict: "declined" }, fails_if: ["Declined requirement"] },
      ],
    };
    const file = writeYaml("runs/run/task.register.yaml", register);
    const planted = Bun.YAML.parse(fs.readFileSync(file, "utf8")) as Register;
    const result: CriteriaFile = fromRegister(planted, "session-b", "Verify units");
    expect(result).toEqual({ criteria: 1, session: "session-b", request: "Verify units", items: [
      { id: "UC1/f1", text: "File IS lost" }, { id: "UC1/f2", text: "Second failure" },
      { id: "UC1/m1", text: "Can reopen" }, { id: "UC2/m1", text: "Another acceptance" },
      { id: "RQ1/f2", text: "Requirement fails" }, { id: "RQ2/f1", text: "Accepted AI requirement" },
    ] });
    expect(result.items.every((item) => !Object.hasOwn(item, "met"))).toBe(true);
  });

  test("a register without units produces no placeholder criteria", () => {
    const file = writeYaml("runs/run/task.register.yaml", { register: 1 });
    const register = Bun.YAML.parse(fs.readFileSync(file, "utf8")) as Register;
    expect(fromRegister(register, "session-a", "Empty task")).toEqual({
      criteria: 1, session: "session-a", request: "Empty task", items: [],
    });
  });
});

describe("K1 skeleton", () => {
  test("returns loadable YAML with session, request and two distinct unmarked placeholder items", () => {
    const request = 'Check: "quoted"\nnew line';
    const text: string = skeleton("session-a", request);
    const result = loadCriteria(writeFile("runs/run/criteria.yaml", text));
    expect(result.criteria).toBe(1);
    expect(result.session).toBe("session-a");
    expect(result.request).toBe(request);
    expect(result.items).toHaveLength(2);
    expect(new Set(result.items.map((item) => item.id)).size).toBe(2);
    expect(result.items.every((item) => typeof item.met !== "boolean")).toBe(true);
  });

  test.each([[119], [120], [121], [200]])("cuts the request at 120 characters: input length %s", (length: number) => {
    const request = "x".repeat(length);
    const result = loadCriteria(writeFile("runs/run/criteria.yaml", skeleton("session-a", request)));
    expect(result.request).toBe(request.slice(0, 120));
  });
});

test("K1 preserves named source fields but never leaks planted content through diagnostics or incidental output", () => {
  const file = writeYaml("runs/run/criteria.yaml", {
    ...criteriaFile([{ id: "C1", text: secret, met: true }, { id: "C1", text: secret }]),
    request: secret, command: secret, stdout: secret, stderr: secret, prompt: secret,
  });
  const malformed = writeFile("runs/bad/criteria.yaml", `criteria: [\n${secret}: [\n`);
  const originalFiles = fs.readdirSync(root, { recursive: true }).sort();
  const originalContent = fs.readFileSync(file, "utf8");
  const printed: string[] = [];
  const spies = [
    spyOn(console, "log").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
    spyOn(console, "warn").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
    spyOn(console, "error").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
    spyOn(process.stdout, "write").mockImplementation((chunk) => { printed.push(String(chunk)); return true; }),
    spyOn(process.stderr, "write").mockImplementation((chunk) => { printed.push(String(chunk)); return true; }),
  ];
  let findings: Finding[] = [];
  let result: Score | undefined;
  let thrown: unknown;
  let generated: CriteriaFile | undefined;
  try {
    const loaded = loadCriteria(file);
    expect(loaded.request).toBe(secret);
    expect(loaded.items[0]!.text).toBe(secret);
    findings = checkCriteria(loaded);
    result = score(loaded);
    try { loadCriteria(malformed); } catch (error) { thrown = error; }
    // Request and criterion text belong in criteria data; they do not belong in diagnostics.
    generated = fromRegister({ register: 1, use_cases: [
      { id: "UC1", origin: "user", fails_if: [secret], min_acceptance: ["Reopens"] },
    ] }, "session-a", secret);
    skeleton("session-a", secret);
    findCriteriaFiles(root);
  } finally {
    for (const spy of spies) spy.mockRestore();
  }
  expectFailure(findings, "R12.7-criterion-text");
  expectFailure(findings, "R12.7-criterion-evidence");
  expect(JSON.stringify(findings)).not.toContain(secret);
  expect(JSON.stringify(result)).not.toContain(secret);
  expect(thrown).toBeInstanceOf(CriteriaError);
  expect(String(thrown)).not.toContain(secret);
  expect(printed.join("\n")).not.toContain(secret);
  expect(generated!.request).toBe(secret);
  expect(generated!.items[0]!.text).toBe(secret);
  expect(fs.readdirSync(root, { recursive: true }).sort()).toEqual(originalFiles);
  expect(fs.readFileSync(file, "utf8")).toBe(originalContent);
});
