import { afterEach, beforeEach, describe, expect, spyOn, test } from "bun:test";
import { createHash } from "node:crypto";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { coverage, freezeHash, isRegisterFile, loadRegister, units, validateRegister } from "../src/register.ts";
import type { CoverageReport, Finding, Register, Requirement, Unit, UseCase } from "../src/types.ts";

const secret = "SECRET-PLANT-7f3a9c";
let folder: string;

beforeEach(() => {
  folder = fs.mkdtempSync(path.join(os.tmpdir(), "hg-"));
});

afterEach(() => {
  fs.rmSync(folder, { recursive: true, force: true });
});

function useCase(changes: Partial<UseCase> = {}): UseCase {
  return {
    id: "UC1",
    origin: "user",
    purpose: "preserve the owner's work",
    fails_if: ["an existing file is lost"],
    min_acceptance: ["the saved file can be reopened"],
    ...changes,
  };
}

function requirement(changes: Partial<Requirement> = {}): Requirement {
  return {
    id: "RQ1",
    origin: "user",
    purpose: "keep the saved work recoverable",
    serves: ["UC1"],
    fails_if: ["a failed save removes the previous version"],
    ...changes,
  };
}

function register(changes: Partial<Register> = {}): Register {
  return { register: 1, use_cases: [useCase()], ...changes };
}

function baseUnits(safety = false): Unit[] {
  return [
    { id: "UC1/f1", text: "an existing file is lost", safety },
    { id: "UC1/m1", text: "the saved file can be reopened", safety },
  ];
}

function hash(list: Unit[]): string {
  return createHash("sha256").update(JSON.stringify(list.map(({ id, text }) => [id, text]))).digest("hex");
}

function coveredRegister(changes: Partial<Register> = {}): Register {
  return register({
    frozen: hash(baseUnits()),
    coverage: [
      { unit: "UC1/f1", covered_by: ["test/save.test.ts: preserves the existing file"] },
      { unit: "UC1/m1", covered_by: ["test/save.test.ts: reopens the saved file"] },
    ],
    ...changes,
  });
}

function writeFile(name: string, text: string): string {
  const file = path.join(folder, name);
  fs.writeFileSync(file, text);
  return file;
}

function expectFailure(findings: Finding[], rule: string): void {
  expect(findings).toContainEqual(expect.objectContaining({ rule, severity: "fail" }));
}

function expectNoRule(findings: Finding[], rule: string): void {
  expect(findings.filter((finding: Finding) => finding.rule === rule)).toEqual([]);
}

function expectRegisterError(file: string): Error {
  let thrown: unknown;
  try {
    loadRegister(file);
  } catch (error) {
    thrown = error;
  }
  expect(thrown).toBeInstanceOf(Error);
  if (!(thrown instanceof Error)) throw new Error("expected a RegisterError");
  expect(thrown.name).toBe("RegisterError");
  return thrown;
}

function expectNoSecret(action: () => void, inputFiles: string[] = []): void {
  const printed: string[] = [];
  const spies = [
    spyOn(console, "log").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
    spyOn(console, "warn").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
    spyOn(console, "error").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
    spyOn(process.stdout, "write").mockImplementation((chunk) => { printed.push(String(chunk)); return true; }),
    spyOn(process.stderr, "write").mockImplementation((chunk) => { printed.push(String(chunk)); return true; }),
  ];
  try {
    action();
  } finally {
    for (const spy of spies) spy.mockRestore();
  }
  expect(printed.join("\n")).not.toContain(secret);
  for (const name of fs.readdirSync(folder, { recursive: true, encoding: "utf8" })) {
    const file = path.join(folder, name);
    if (!inputFiles.includes(file) && fs.statSync(file).isFile()) {
      expect(fs.readFileSync(file, "utf8")).not.toContain(secret);
    }
  }
}

describe("loadRegister", () => {
  test("load: YAML with register 1 preserves the shared register fields", () => {
    const file = writeFile("cases.register.yaml", [
      "register: 1",
      "frozen: old-freeze",
      "use_cases:",
      "  - id: UC1",
      "    origin: ai",
      "    decision: { by: owner, verdict: accepted }",
      "    purpose: preserve work",
      "    fails_if: [work is lost]",
      "    min_acceptance: [work can be reopened]",
      "    safety: true",
      "requirements:",
      "  - id: RQ1",
      "    origin: user",
      "    purpose: retain the previous version",
      "    serves: [UC1, vision]",
      "    fails_if: [the previous version is removed]",
      "    targets: { format: text }",
      "conflicts:",
      "  - { use_case: UC1, requirement: RQ1, shown_to_owner: true, result: disclosed, resolution: keep both }",
      "coverage:",
      "  - { unit: UC1/f1, covered_by: [test/save.test.ts] }",
      "  - { unit: RQ1/f1, skippable: { reason: deferred by owner } }",
    ].join("\n"));
    const loaded: Register = loadRegister(file);
    expect(loaded).toEqual({
      register: 1,
      frozen: "old-freeze",
      use_cases: [useCase({
        origin: "ai", decision: { by: "owner", verdict: "accepted" }, purpose: "preserve work",
        fails_if: ["work is lost"], min_acceptance: ["work can be reopened"], safety: true,
      })],
      requirements: [requirement({
        purpose: "retain the previous version", serves: ["UC1", "vision"],
        fails_if: ["the previous version is removed"], targets: { format: "text" },
      })],
      conflicts: [{ use_case: "UC1", requirement: "RQ1", shown_to_owner: true, result: "disclosed", resolution: "keep both" }],
      coverage: [
        { unit: "UC1/f1", covered_by: ["test/save.test.ts"] },
        { unit: "RQ1/f1", skippable: { reason: "deferred by owner" } },
      ],
    });
  });

  test("load: register 1 alone is parseable even before validation", () => {
    expect(loadRegister(writeFile("register.yaml", "register: 1\n"))).toEqual({ register: 1 });
  });

  test.each(["register: 1\nuse_cases: [", "register: 1\nvalue: \"unterminated"])(
    "load: invalid YAML %j throws RegisterError",
    (text: string) => { expectRegisterError(writeFile("broken.yaml", text)); },
  );

  test.each(["", "null\n", "[]\n", "use_cases: []\n", "register: 0\n", "register: 2\n", "register: '1'\n", "register: true\n"])(
    "load: YAML without the numeric register 1 marker %j throws RegisterError",
    (text: string) => { expectRegisterError(writeFile("wrong.yaml", text)); },
  );

  test("load: a malformed source containing a secret is never echoed in diagnostics or state", () => {
    const file = writeFile("broken.yaml", `register: 1\nprompt: [${secret}\n`);
    expectNoSecret(() => {
      const error = expectRegisterError(file);
      expect(String(error)).not.toContain(secret);
      expect(error.stack ?? "").not.toContain(secret);
    }, [file]);
  });
});

describe("isRegisterFile", () => {
  test.each(["register.yaml", "cases.register.yaml", "nested/register.yaml", "nested/release.register.yaml"])(
    "file: %s is a register filename even when the file does not exist",
    (name: string) => { expect(isRegisterFile(path.join(folder, name))).toBe(true); },
  );

  test.each(["notregister.yaml", "register.yml", "cases.register.yml", "register.yaml.bak", "cases.register.yaml.txt", "register.yaml/notes.md", "notes.yaml"])(
    "file: %s is not a register filename",
    (name: string) => { expect(isRegisterFile(path.join(folder, name))).toBe(false); },
  );
});

describe("validateRegister", () => {
  test("validate: complete user and accepted AI entries with valid references pass", () => {
    const r = coveredRegister({
      use_cases: [useCase(), useCase({ id: "UC2", origin: "ai", decision: { by: "owner", verdict: "accepted" } })],
      requirements: [requirement(), requirement({ id: "RQ2", origin: "ai", decision: { by: "owner", verdict: "accepted" }, serves: ["vision", "RQ1"] })],
      conflicts: [{ use_case: "UC1", requirement: "RQ1", shown_to_owner: true }],
    });
    expect(validateRegister(r)).toEqual([]);
  });

  test("validate: an AI use case without a decision fails", () => {
    expectFailure(validateRegister(register({ use_cases: [useCase({ origin: "ai" })] })), "R13.1-no-decision");
  });

  test("validate: an AI requirement without a decision fails and is nonbinding", () => {
    const findings: Finding[] = validateRegister(register({ requirements: [requirement({ origin: "ai" })] }));
    expectFailure(findings, "R13.1-no-decision");
    expect(findings).toContainEqual(expect.objectContaining({ rule: "R13.5-not-binding", severity: "warn" }));
  });

  test.each(["user", "ai"] as const)("validate: a %s use-case decision without by fails", (origin) => {
    expectFailure(validateRegister(register({ use_cases: [useCase({ origin, decision: { verdict: "accepted" } })] })), "R13.1-no-decision");
  });

  test.each(["user", "ai"] as const)("validate: a %s requirement decision without by fails", (origin) => {
    expectFailure(validateRegister(register({ requirements: [requirement({ origin, decision: { verdict: "accepted" } })] })), "R13.1-no-decision");
  });

  test("validate: an empty decision by does not identify a decision maker", () => {
    const r = register({
      use_cases: [useCase({ origin: "ai", decision: { by: "", verdict: "accepted" } })],
      requirements: [requirement({ origin: "ai", decision: { by: "", verdict: "accepted" } })],
    });
    expectFailure(validateRegister(r), "R13.1-no-decision");
  });

  test.each(["user", "ai"] as const)("validate: an accepted %s case missing purpose fails", (origin) => {
    const uc = useCase({ origin, decision: { by: "owner", verdict: "accepted" } });
    delete uc.purpose;
    expectFailure(validateRegister(register({ use_cases: [uc] })), "R13.2-missing");
  });

  for (const origin of ["user", "ai"] as const) {
    test.each(["fails_if", "min_acceptance"] as const)(`validate: an accepted ${origin} case missing %s fails`, (field) => {
      const uc = useCase({ origin, decision: { by: "owner", verdict: "accepted" } });
      delete uc[field];
      expectFailure(validateRegister(register({ use_cases: [uc] })), "R13.2-missing");
    });

    test.each(["fails_if", "min_acceptance"] as const)(`validate: an accepted ${origin} case with an empty %s list fails`, (field) => {
      const uc = useCase({ origin, decision: { by: "owner", verdict: "accepted" }, [field]: [] });
      expectFailure(validateRegister(register({ use_cases: [uc] })), "R13.2-missing");
    });
  }

  test.each(["user", "ai"] as const)("validate: a declined %s case does not need acceptance fields", (origin) => {
    const r = register({ use_cases: [{ id: "UC1", origin, decision: { by: "owner", verdict: "declined" } }] });
    expect(validateRegister(r)).toEqual([]);
  });

  test("validate: an undecided AI case is not yet subject to accepted-case completeness", () => {
    const findings: Finding[] = validateRegister(register({ use_cases: [{ id: "UC1", origin: "ai" }] }));
    expectFailure(findings, "R13.1-no-decision");
    expectNoRule(findings, "R13.2-missing");
  });

  test("validate: a requirement with no purpose fails", () => {
    const rq = requirement();
    delete rq.purpose;
    expectFailure(validateRegister(register({ requirements: [rq] })), "R13.5-no-purpose");
  });

  test("validate: a requirement with no serves fails", () => {
    const rq = requirement();
    delete rq.serves;
    expectFailure(validateRegister(register({ requirements: [rq] })), "R13.5-no-purpose");
  });

  test("validate: a requirement with an empty serves list fails", () => {
    expectFailure(validateRegister(register({ requirements: [requirement({ serves: [] })] })), "R13.5-no-purpose");
  });

  test("validate: a declined AI requirement is a warning and contributes no units", () => {
    const r = register({ requirements: [requirement({ origin: "ai", decision: { by: "owner", verdict: "declined" } })] });
    expect(validateRegister(r)).toEqual([expect.objectContaining({ rule: "R13.5-not-binding", severity: "warn" })]);
    expect(units(r)).toEqual(baseUnits());
  });

  test.each([undefined, false])("validate: a conflict with shown_to_owner %j fails", (shown_to_owner) => {
    const r = register({ requirements: [requirement()], conflicts: [{ use_case: "UC1", requirement: "RQ1", shown_to_owner }] });
    expectFailure(validateRegister(r), "R13.7-conflict-not-shown");
  });

  test("validate: an unknown serves id fails", () => {
    expectFailure(validateRegister(register({ requirements: [requirement({ serves: ["UC-missing"] })] })), "R13-unknown-ref");
  });

  test.each(["use_case", "requirement"] as const)("validate: an unknown conflict %s id fails", (field) => {
    const r = register({
      requirements: [requirement()],
      conflicts: [{ use_case: "UC1", requirement: "RQ1", shown_to_owner: true, [field]: "missing" }],
    });
    expectFailure(validateRegister(r), "R13-unknown-ref");
  });

  test.each(["UC-missing/f1", "UC1/f99", "UC1/m99", "RQ-missing/f1"])("validate: an unknown coverage unit %s fails", (unit: string) => {
    expectFailure(validateRegister(register({ coverage: [{ unit, covered_by: ["test/save.test.ts"] }] })), "R13-unknown-ref");
  });

  test("validate: existing requirement units are valid coverage references", () => {
    const r = register({ requirements: [requirement()], coverage: [{ unit: "RQ1/f1", covered_by: ["test/backup.test.ts"] }] });
    expect(validateRegister(r)).toEqual([]);
  });
});

describe("units", () => {
  test("units: accepted cases yield indexed failure and acceptance units with their safety flag", () => {
    const list: Unit[] = units(register({ use_cases: [useCase({
      origin: "ai", decision: { by: "owner", verdict: "accepted" }, safety: true,
      fails_if: ["first failure", "second failure"], min_acceptance: ["first acceptance", "second acceptance"],
    })] }));
    expect(list).toEqual([
      { id: "UC1/f1", text: "first failure", safety: true },
      { id: "UC1/f2", text: "second failure", safety: true },
      { id: "UC1/m1", text: "first acceptance", safety: true },
      { id: "UC1/m2", text: "second acceptance", safety: true },
    ]);
  });

  test("units: user cases are accepted by default and omitted safety is false", () => {
    expect(units(register())).toEqual(baseUnits());
  });

  test("units: declined user and AI cases and undecided AI cases contribute nothing", () => {
    expect(units(register({ use_cases: [
      useCase({ id: "UC1", decision: { by: "owner", verdict: "declined" } }),
      useCase({ id: "UC2", origin: "ai", decision: { by: "owner", verdict: "declined" } }),
      useCase({ id: "UC3", origin: "ai" }),
      useCase({ id: "UC4", origin: "ai", decision: { by: "owner" } }),
    ] }))).toEqual([]);
  });

  test("units: accepted requirements yield only their indexed fails_if items", () => {
    const r = register({ requirements: [
      requirement({ fails_if: ["first requirement failure", "second requirement failure"], targets: { count: "5" } }),
      requirement({ id: "RQ2", origin: "ai", decision: { by: "owner", verdict: "accepted" }, fails_if: ["third requirement failure"] }),
    ] });
    expect(units(r)).toEqual([
      ...baseUnits(),
      { id: "RQ1/f1", text: "first requirement failure", safety: false },
      { id: "RQ1/f2", text: "second requirement failure", safety: false },
      { id: "RQ2/f1", text: "third requirement failure", safety: false },
    ]);
  });

  test("units: an AI requirement without acceptance contributes nothing", () => {
    const r = register({ requirements: [
      requirement({ origin: "ai" }),
      requirement({ id: "RQ2", origin: "ai", decision: { by: "owner" } }),
      requirement({ id: "RQ3", origin: "ai", decision: { by: "owner", verdict: "declined" } }),
    ] });
    expect(units(r)).toEqual(baseUnits());
  });

  test("units: absent optional collections and requirement fails_if yield no units", () => {
    expect(units({ register: 1 })).toEqual([]);
    const rq = requirement({ serves: ["vision"] });
    delete rq.fails_if;
    expect(units({ register: 1, requirements: [rq, requirement({ id: "RQ2", serves: ["vision"], fails_if: [] })] })).toEqual([]);
  });

  test("units: case and whitespace variants across cases and requirements retain only the first text and id", () => {
    const r = register({
      use_cases: [
        useCase({ fails_if: ["File IS lost", "file\tis\n lost", "a distinct failure"], min_acceptance: ["FILE is LOST", "can reopen"] }),
        useCase({ id: "UC2", fails_if: ["file is lost"], min_acceptance: ["CAN   REOPEN"] }),
      ],
      requirements: [requirement({ fails_if: ["can\treopen", "requirement alone fails"] })],
    });
    expect(units(r)).toEqual([
      { id: "UC1/f1", text: "File IS lost", safety: false },
      { id: "UC1/f3", text: "a distinct failure", safety: false },
      { id: "UC1/m2", text: "can reopen", safety: false },
      { id: "RQ1/f2", text: "requirement alone fails", safety: false },
    ]);
  });
});

describe("freezeHash", () => {
  test("freeze: sha256 hashes canonical JSON of ordered id and text pairs", () => {
    const list: Unit[] = [
      { id: "UC1/f1", text: "quotes \" and newline\n雪", safety: true },
      { id: "RQ1/f1", text: "second", safety: false },
    ];
    const expected = createHash("sha256").update('[["UC1/f1","quotes \\" and newline\\n雪"],["RQ1/f1","second"]]').digest("hex");
    const actual: string = freezeHash(list);
    expect(actual).toMatch(/^[0-9a-f]{64}$/);
    expect(actual).toBe(expected);
    expect(freezeHash(list)).toBe(actual);
  });

  test("freeze: an empty list hashes the JSON empty array", () => {
    expect(freezeHash([])).toBe(createHash("sha256").update("[]").digest("hex"));
  });

  test("freeze: changing id, text, order or count changes the hash", () => {
    const original = baseUnits();
    const frozen = freezeHash(original);
    expect(freezeHash([{ ...original[0]!, id: "UC2/f1" }, original[1]!])).not.toBe(frozen);
    expect(freezeHash([{ ...original[0]!, text: "changed failure" }, original[1]!])).not.toBe(frozen);
    expect(freezeHash([...original].reverse())).not.toBe(frozen);
    expect(freezeHash(original.slice(0, 1))).not.toBe(frozen);
  });

  test("freeze: safety is excluded and text is not lowercased or whitespace-normalised", () => {
    expect(freezeHash(baseUnits(true))).toBe(freezeHash(baseUnits(false)));
    const original = baseUnits();
    expect(freezeHash([{ ...original[0]!, text: original[0]!.text.toUpperCase() }, original[1]!])).not.toBe(freezeHash(original));
    expect(freezeHash([{ ...original[0]!, text: ` ${original[0]!.text} ` }, original[1]!])).not.toBe(freezeHash(original));
  });
});

describe("coverage", () => {
  test("coverage: a frozen fully covered register has no findings", () => {
    const report: CoverageReport = coverage(coveredRegister());
    expect(report).toEqual({ total: 2, covered: 2, percent: 100, target: 80, findings: [] });
  });

  test("coverage: a missing freeze fails", () => {
    const r = coveredRegister();
    delete r.frozen;
    expectFailure(coverage(r).findings, "R11.1-not-frozen");
  });

  test("coverage: an incorrect freeze fails", () => {
    expectFailure(coverage(coveredRegister({ frozen: "0".repeat(64) })).findings, "R11.1-frozen-mismatch");
  });

  test("coverage: changing a unit's text invalidates the old freeze", () => {
    const r = coveredRegister({ use_cases: [useCase({ fails_if: ["a different failure"] })] });
    expectFailure(coverage(r).findings, "R11.1-frozen-mismatch");
  });

  test("coverage: adding a unit invalidates the old freeze", () => {
    const r = coveredRegister({ use_cases: [useCase({ fails_if: ["an existing file is lost", "another failure"] })] });
    expectFailure(coverage(r).findings, "R11.1-frozen-mismatch");
  });

  test("coverage: a unit with no coverage entry is an uncovered basic unit", () => {
    const report: CoverageReport = coverage(coveredRegister({ coverage: [{ unit: "UC1/f1", covered_by: ["save.test.ts"] }] }));
    expect(report.total).toBe(2);
    expect(report.covered).toBe(1);
    expect(report.percent).toBe(50);
    expectFailure(report.findings, "R11.1-basic-uncovered");
  });

  test("coverage: an entry without covered_by is an uncovered basic unit", () => {
    expectFailure(coverage(coveredRegister({ coverage: [{ unit: "UC1/f1" }, { unit: "UC1/m1", covered_by: ["reopen.test.ts"] }] })).findings, "R11.1-basic-uncovered");
  });

  test("coverage: an empty covered_by list does not cover a basic unit", () => {
    const report: CoverageReport = coverage(coveredRegister({ coverage: [{ unit: "UC1/f1", covered_by: [] }, { unit: "UC1/m1", covered_by: ["reopen.test.ts"] }] }));
    expect(report.covered).toBe(1);
    expectFailure(report.findings, "R11.1-basic-uncovered");
  });

  test("coverage: multiple tests for a unit count it only once", () => {
    const report: CoverageReport = coverage(coveredRegister({ coverage: [{ unit: "UC1/f1", covered_by: ["first.test.ts", "second.test.ts"] }] }));
    expect(report.covered).toBe(1);
    expect(report.percent).toBe(50);
  });

  test("coverage: a non-safety skip with a reason avoids a basic failure but is not covered", () => {
    const report: CoverageReport = coverage(coveredRegister({ coverage: [
      { unit: "UC1/f1", covered_by: ["save.test.ts"] },
      { unit: "UC1/m1", skippable: { reason: "owner deferred reopening" } },
    ] }));
    expect(report).toEqual({
      total: 2, covered: 1, percent: 50, target: 80,
      findings: [expect.objectContaining({ rule: "R11.1-below-target", severity: "warn" })],
    });
  });

  test.each([undefined, "", " \t\n"])("coverage: skippable with reason %j fails", (reason) => {
    const r = coveredRegister({ coverage: [
      { unit: "UC1/f1", skippable: { reason } },
      { unit: "UC1/m1", covered_by: ["reopen.test.ts"] },
    ] });
    expectFailure(coverage(r).findings, "R11.1-skip-no-reason");
  });

  test.each(["UC1/f1", "UC1/m1"])("coverage: a skippable safety unit %s fails even with a reason", (unit: string) => {
    const r = coveredRegister({
      use_cases: [useCase({ safety: true })],
      coverage: baseUnits().map((item: Unit) => item.id === unit
        ? { unit: item.id, skippable: { reason: "owner deferred it" } }
        : { unit: item.id, covered_by: ["safety.test.ts"] }),
    });
    expectFailure(coverage(r).findings, "R11.1-safety-skipped");
  });

  test("coverage: a covered safety unit still cannot be marked skippable", () => {
    const r = coveredRegister({
      use_cases: [useCase({ safety: true })],
      coverage: [
        { unit: "UC1/f1", covered_by: ["safety.test.ts"], skippable: { reason: "owner deferred it" } },
        { unit: "UC1/m1", covered_by: ["safety.test.ts"] },
      ],
    });
    expectFailure(coverage(r).findings, "R11.1-safety-skipped");
  });

  test("coverage: below 80 percent is a warning and never a failure", () => {
    const report: CoverageReport = coverage(coveredRegister({ coverage: [
      { unit: "UC1/f1", covered_by: ["save.test.ts"] },
      { unit: "UC1/m1", skippable: { reason: "owner deferred it" } },
    ] }));
    expect(report.percent).toBe(50);
    expect(report.target).toBe(80);
    expect(report.findings).toContainEqual(expect.objectContaining({ rule: "R11.1-below-target", severity: "warn" }));
    expect(report.findings.filter((finding: Finding) => finding.severity === "fail")).toEqual([]);
  });

  test("coverage: exactly 80 percent meets the target", () => {
    const list: Unit[] = [
      ...["first", "second", "third", "fourth"].map((text, i) => ({ id: `UC1/f${i + 1}`, text, safety: false })),
      { id: "UC1/m1", text: "fifth", safety: false },
    ];
    const r = register({
      use_cases: [useCase({ fails_if: ["first", "second", "third", "fourth"], min_acceptance: ["fifth"] })],
      frozen: hash(list),
      coverage: list.map((item: Unit, i) => i < 4
        ? { unit: item.id, covered_by: ["save.test.ts"] }
        : { unit: item.id, skippable: { reason: "owner deferred it" } }),
    });
    expect(coverage(r)).toEqual({ total: 5, covered: 4, percent: 80, target: 80, findings: [] });
  });

  test("coverage: percent is rounded to one decimal place", () => {
    const list: Unit[] = [...baseUnits(), { id: "RQ1/f1", text: "a failed save removes the previous version", safety: false }];
    const r = coveredRegister({ requirements: [requirement()], frozen: hash(list) });
    const report: CoverageReport = coverage(r);
    expect(report.total).toBe(3);
    expect(report.covered).toBe(2);
    expect(report.percent).toBe(66.7);
  });

  test("coverage: covered variants do not inflate the percentage or change the freeze", () => {
    const original = coveredRegister({ coverage: [{ unit: "UC1/f1", covered_by: ["save.test.ts"] }] });
    const variant = coveredRegister({
      use_cases: [useCase(), useCase({
        id: "UC2", fails_if: ["AN EXISTING   FILE IS LOST"], min_acceptance: ["the saved file\tcan be reopened"],
      })],
      coverage: [
        ...original.coverage!,
        { unit: "UC2/f1", covered_by: ["variant.test.ts"] },
        { unit: "UC2/m1", covered_by: ["variant.test.ts"] },
      ],
    });
    const before: CoverageReport = coverage(original);
    const after: CoverageReport = coverage(variant);
    expect(after.total).toBe(2);
    expect(after.covered).toBe(1);
    expect(after.percent).toBe(50);
    expect(after.percent).toBe(before.percent);
    expectNoRule(after.findings, "R11.1-frozen-mismatch");
    expectFailure(after.findings, "R11.1-basic-uncovered");
  });

  test("coverage: changing only coverage entries preserves the freeze", () => {
    const report: CoverageReport = coverage(coveredRegister({ coverage: [] }));
    expect(report.covered).toBe(0);
    expect(report.percent).toBe(0);
    expectNoRule(report.findings, "R11.1-frozen-mismatch");
    expectFailure(report.findings, "R11.1-basic-uncovered");
  });
});

test("output: raw register content never leaks through findings, console, journal or evidence", () => {
  const r = register({
    use_cases: [useCase({ purpose: secret, fails_if: [secret], min_acceptance: ["safe acceptance"] })],
    requirements: [requirement({ purpose: secret, serves: ["missing"] })],
    conflicts: [{ use_case: "UC1", requirement: "RQ1", result: secret, resolution: secret }],
    coverage: [{ unit: "UC1/f1", skippable: { reason: "" } }],
  });
  const file = writeFile("secret.register.yaml", JSON.stringify({ ...r, prompt: secret, config: { token: secret } }));
  expectNoSecret(() => {
    const loaded: Register = loadRegister(file);
    const list: Unit[] = units(loaded);
    // Loading and unit extraction preserve source text; diagnostics must not echo it.
    expect(list[0]!.text).toBe(secret);
    expect(isRegisterFile(file)).toBe(true);
    const frozen: string = freezeHash(list);
    expect(frozen).not.toContain(secret);
    const findings: Finding[] = validateRegister(loaded);
    expectFailure(findings, "R13-unknown-ref");
    expectFailure(findings, "R13.7-conflict-not-shown");
    expect(JSON.stringify(findings)).not.toContain(secret);
    const report: CoverageReport = coverage({ ...loaded, frozen });
    expectFailure(report.findings, "R11.1-basic-uncovered");
    expectFailure(report.findings, "R11.1-skip-no-reason");
    expect(JSON.stringify(report)).not.toContain(secret);
  }, [file]);
});
