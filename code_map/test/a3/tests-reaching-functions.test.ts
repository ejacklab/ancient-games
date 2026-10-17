import { expect, test } from "bun:test";
import { readFileSync } from "node:fs";
import { isAbsolute, resolve } from "node:path";

const packageDir = resolve(import.meta.dir, "../..");
const fixtureDir = resolve(import.meta.dir, "fixtures");
const service = "sealed-parcels";
const direct = "stamp-ledger";
const countOrEvidence = "the count differs from the list, or a link lacks its evidence;";
const knownPath = "a test with a known path is missing;";
const staticWording = "static links are called coverage;";
const fileReport = "the per-function file report runs without the user's request.";

type Loc = { file: string; line: number };
type Hop = { site: Loc | Loc[]; to: Loc; kind: "call" | "service-call" };

function loc(project: string, file: string, anchor: string): Loc {
  const lines = readFileSync(resolve(fixtureDir, project, file), "utf8").split("\n");
  const positions = lines.flatMap((line, index) => line.includes(anchor) ? [index + 1] : []);
  expect(positions, `unique fixture anchor: ${project}/${file}: ${anchor}`).toHaveLength(1);
  return { file, line: positions[0]! };
}

function query(at: Loc) { return `${at.file}:${at.line}`; }

const receipt = loc(service, "live.ts", "export function receiptDigits");
const seal = loc(service, "live.ts", 'const seal = Effect.fn("ParcelDesk.seal")');
const dispatch = loc(service, "workflow.ts", "export const dispatchParcel =");
const relay = loc(service, "workflow.ts", "export function relayParcel");
const stamp = loc(direct, "amounts.ts", "export function unitStamp");
const padded = loc(direct, "amounts.ts", "export function paddedStamp");
const serviceHop: Hop = {
  site: loc(service, "workflow.ts", "return yield* desk.seal(parcel)"), to: seal, kind: "service-call",
};
const receiptHop: Hop = {
  site: loc(service, "live.ts", "const digits = receiptDigits(prefix + parcel)"), to: receipt, kind: "call",
};
const dispatchHop: Hop = {
  site: loc(service, "workflow.ts", "return dispatchParcel(parcel)"), to: dispatch, kind: "call",
};

async function runRaw(project: string, args: string[], options: {
  patterns?: string[]; json?: boolean;
} = {}) {
  const root = resolve(fixtureDir, project);
  const child = Bun.spawn([
    process.execPath, "src/cli.ts", "tests", ...args,
    "--project", resolve(root, "tsconfig.json"), "--root", root,
    ...(options.patterns ?? ["*.checks.ts"]).flatMap(pattern => ["--tests", pattern]),
    ...(options.json === false ? [] : ["--json"]),
  ], { cwd: packageDir, stdout: "pipe", stderr: "pipe" });
  const timer = setTimeout(() => child.kill(), 15_000);
  try {
    const [exitCode, stdout, stderr] = await Promise.all([
      child.exited, new Response(child.stdout).text(), new Response(child.stderr).text(),
    ]);
    return { exitCode, stdout, stderr };
  } finally {
    clearTimeout(timer);
  }
}

async function runCli(project: string, args: string[], patterns = ["*.checks.ts"]) {
  const result = await runRaw(project, args, { patterns });
  expect(result.exitCode, result.stderr || result.stdout).toBe(0);
  const answer = JSON.parse(result.stdout);
  expect(answer.command).toBe("tests");
  expect(Array.isArray(answer.limits)).toBe(true);
  expect(answer.ambiguous).not.toBe(true);
  expect(answer.tests.label).toBe("static-call-path");
  expect(Array.isArray(answer.tests.tests)).toBe(true);
  expect(Array.isArray(answer.tests.undecided)).toBe(true);
  expect(answer.tests.count).toBe(answer.tests.tests.length);
  return answer;
}

function expectLoc(project: string, at: any) {
  expect(typeof at.file).toBe("string");
  expect(at.file.length).toBeGreaterThan(0);
  expect(isAbsolute(at.file)).toBe(false);
  const lines = readFileSync(resolve(fixtureDir, project, at.file), "utf8").split("\n");
  expect(Number.isInteger(at.line)).toBe(true);
  expect(at.line).toBeGreaterThan(0);
  expect(at.line).toBeLessThanOrEqual(lines.length);
  if (at.endLine !== undefined) {
    expect(Number.isInteger(at.endLine)).toBe(true);
    expect(at.endLine).toBeGreaterThanOrEqual(at.line);
    expect(at.endLine).toBeLessThanOrEqual(lines.length);
  }
}

function expectNode(project: string, node: any) {
  expectLoc(project, node);
  expect(typeof node.name).toBe("string");
  expect(node.name.length).toBeGreaterThan(0);
  expect(["function", "method", "arrow", "effect-fn", "property", "class", "variable", "interface-member", "other"])
    .toContain(node.kind);
}

function expectLink(project: string, link: any) {
  expectNode(project, link.from);
  expectLoc(project, link.site);
  expect(["call", "new", "service-call"]).toContain(link.kind);
  expect(["definition", "implementation-lookup"]).toContain(link.via);
  expect(["implementation", "unresolved", "ambiguous"]).toContain(link.resolution);
  if (link.declaration !== undefined) expectLoc(project, link.declaration);
  expect(Array.isArray(link.candidates)).toBe(true);
  for (const candidate of link.candidates) {
    expectNode(project, candidate);
    expect(typeof candidate.testFake).toBe("boolean");
  }
  if (link.resolution === "implementation") expectNode(project, link.to);
  else expect(link.to).toBeUndefined();
  if (link.resolution === "unresolved") {
    expect(typeof link.reason).toBe("string");
    expect(link.reason.trim().length).toBeGreaterThan(0);
  }
}

function expectCase(project: string, cases: any[], name: string, at: Loc, hops: Hop[], throughFake: boolean) {
  const found = cases.filter(item => item.name === name);
  expect(found, `one test case named ${name}`).toHaveLength(1);
  const item = found[0];
  expect(item).toMatchObject({ ...at, name, throughFake });
  expectLoc(project, item);
  expect(item.path).toHaveLength(hops.length);
  let previous = at;
  for (const [index, hop] of hops.entries()) {
    const link = item.path[index];
    expectLink(project, link);
    expect(link).toMatchObject({ from: previous, to: hop.to, kind: hop.kind, resolution: "implementation" });
    const possibleSites = Array.isArray(hop.site) ? hop.site : [hop.site];
    expect(possibleSites).toContainEqual({ file: link.site.file, line: link.site.line });
    if (hop.kind === "service-call") {
      expect(link).toMatchObject({
        via: "implementation-lookup", declaration: loc(service, "port.ts", "readonly seal:"),
      });
      expect(link.candidates).toEqual(expect.arrayContaining([
        expect.objectContaining({ ...seal, testFake: false }),
        expect.objectContaining({ ...loc(service, "parcels.checks.ts", "seal: () =>"), testFake: true }),
      ]));
    }
    previous = hop.to;
  }
}

function expectServiceCases(cases: any[], target: "seal" | "receipt") {
  const tail = target === "receipt" ? [receiptHop] : [];
  expectCase(service, cases, "submits a sealed parcel",
    loc(service, "parcels.checks.ts", 'test("submits a sealed parcel"'), [
      { site: loc(service, "parcels.checks.ts", 'const task = relayParcel("amber-72")'), to: relay, kind: "call" },
      dispatchHop, serviceHop, ...tail,
    ], true);
  expectCase(service, cases, "queues a second parcel",
    loc(service, "parcels.checks.ts", 'it("queues a second parcel"'), [
      { site: loc(service, "parcels.checks.ts", 'const task = dispatchParcel("blue-19")'), to: dispatch, kind: "call" },
      serviceHop, ...tail,
    ], true);
}

function expectDirectReceipt(cases: any[]) {
  expectCase(service, cases, "hashes receipt directly",
    loc(service, "parcels.checks.ts", 'test("hashes receipt directly"'), [
      { site: loc(service, "parcels.checks.ts", 'receiptDigits("direct-88")'), to: receipt, kind: "call" },
    ], false);
}

test(`A3 direct count counts cases, not calls — Fails if: "${countOrEvidence}"`, async () => {
  const answer = await runCli(direct, [query(stamp)]);
  expect(answer.tests.count).toBe(3);
  expect(answer.tests.undecided).toEqual([]);
  expectCase(direct, answer.tests.tests, "two calls are one test case",
    loc(direct, "stamps.checks.ts", 'test("two calls are one test case"'), [
      { site: [loc(direct, "stamps.checks.ts", "actualStamp(2)"), loc(direct, "stamps.checks.ts", "actualStamp(7)")],
        to: stamp, kind: "call" },
    ], false);
  expectCase(direct, answer.tests.tests, "walks through a helper",
    loc(direct, "stamps.checks.ts", 'it("walks through a helper"'), [
      { site: loc(direct, "stamps.checks.ts", "paddedStamp(4)"), to: padded, kind: "call" },
      { site: loc(direct, "amounts.ts", "return unitStamp(quantity)"), to: stamp, kind: "call" },
    ], false);
  expectCase(direct, answer.tests.tests, "nested ledger case",
    loc(direct, "stamps.checks.ts", 'test("nested ledger case"'), [
      { site: loc(direct, "stamps.checks.ts", "actualStamp(6)"), to: stamp, kind: "call" },
    ], false);
}, 20_000);

test(`A3 counted Effect paths retain every link's evidence — Fails if: "${countOrEvidence}"`, async () => {
  const answer = await runCli(service, [query(receipt), "--fake-rule", "count"]);
  expect(answer.tests.count).toBe(3);
  expect(answer.tests.undecided).toEqual([]);
  expectServiceCases(answer.tests.tests, "receipt");
  expectDirectReceipt(answer.tests.tests);
}, 20_000);

test(`A3 undecided Effect paths retain evidence outside the count — Fails if: "${countOrEvidence}"`, async () => {
  const answer = await runCli(service, [query(receipt)]);
  expect(answer.tests.count).toBe(1);
  expectDirectReceipt(answer.tests.tests);
  expect(answer.tests.undecided).toHaveLength(2);
  expectServiceCases(answer.tests.undecided, "receipt");
  expect(answer.limits).toEqual(expect.arrayContaining([
    expect.objectContaining({ reason: "other", text: "fake rule not set (A3)" }),
  ]));
}, 20_000);

test(`A3 fake-rule count includes the real Effect implementation — Fails if: "${knownPath}"`, async () => {
  const answer = await runCli(service, [query(seal), "--fake-rule", "count"]);
  expect(answer.tests.count).toBe(2);
  expect(answer.tests.undecided).toEqual([]);
  expectServiceCases(answer.tests.tests, "seal");
}, 20_000);

test(`A3 fake-rule exclude omits fake-only paths from both lists — Fails if: "${knownPath}"`, async () => {
  const answer = await runCli(service, [query(seal), "--fake-rule", "exclude"]);
  expect(answer.tests).toMatchObject({ count: 0, tests: [], undecided: [] });
  expect(answer.limits.some((limit: any) => limit.text === "fake rule not set (A3)")).toBe(false);
}, 20_000);

test(`A3 unset fake rule preserves all known service paths as undecided — Fails if: "${knownPath}"`, async () => {
  const answer = await runCli(service, [query(seal)]);
  expect(answer.tests).toMatchObject({ count: 0, tests: [] });
  expect(answer.tests.undecided).toHaveLength(2);
  expectServiceCases(answer.tests.undecided, "seal");
  expect(answer.limits).toEqual(expect.arrayContaining([
    expect.objectContaining({ reason: "other", text: "fake rule not set (A3)" }),
  ]));
}, 20_000);

test(`A3 fake-rule exclude retains the direct path to the same leaf — Fails if: "${knownPath}"`, async () => {
  const answer = await runCli(service, [query(receipt), "--fake-rule", "exclude"]);
  expect(answer.tests.count).toBe(1);
  expect(answer.tests.undecided).toEqual([]);
  expectDirectReceipt(answer.tests.tests);
}, 20_000);

test(`A3 no test pattern classifies no service-project files as tests — Fails if: "${knownPath}"`, async () => {
  const answer = await runCli(service, [query(receipt), "--fake-rule", "count"], []);
  expect(answer.tests).toMatchObject({ count: 0, tests: [], undecided: [] });
  expect(answer.limits).toEqual(expect.arrayContaining([
    expect.objectContaining({ reason: "other", text: "no test-file pattern given" }),
  ]));
}, 20_000);

test(`A3 explicit and repeated patterns select the service project's test files — Fails if: "${knownPath}"`, async () => {
  const selected = await runCli(service, [query(receipt), "--fake-rule", "count"], ["*.specimen.ts"]);
  expect(selected.tests.count).toBe(1);
  expect(selected.tests.undecided).toEqual([]);
  const explicitAt = loc(service, "loose.specimen.ts", 'test("selected only by an explicit spec pattern"');
  const explicitHop: Hop = {
    site: loc(service, "loose.specimen.ts", 'receiptDigits("loose-46")'), to: receipt, kind: "call",
  };
  expectCase(service, selected.tests.tests, "selected only by an explicit spec pattern", explicitAt, [explicitHop], false);

  const combined = await runCli(service, [query(receipt), "--fake-rule", "count"], ["*.checks.ts", "*.specimen.ts"]);
  expect(combined.tests.count).toBe(4);
  expect(combined.tests.undecided).toEqual([]);
  expectServiceCases(combined.tests.tests, "receipt");
  expectDirectReceipt(combined.tests.tests);
  expectCase(service, combined.tests.tests, "selected only by an explicit spec pattern", explicitAt, [explicitHop], false);
}, 20_000);

test(`A3 direct, aliased, it and describe-nested paths exclude a same-name decoy — Fails if: "${knownPath}"`, async () => {
  const answer = await runCli(direct, [query(stamp)]);
  expect(answer.tests.tests.map((item: any) => item.name).sort()).toEqual([
    "nested ledger case", "two calls are one test case", "walks through a helper",
  ]);
  expect(answer.tests.undecided).toEqual([]);
}, 20_000);

function answerFieldNames(value: unknown): string[] {
  if (Array.isArray(value)) return value.flatMap(answerFieldNames);
  if (value === null || typeof value !== "object") return [];
  return Object.entries(value).flatMap(([key, child]) => [key, ...answerFieldNames(child)]);
}

test(`A3 JSON uses static-path labels and no execution-claim field in every fake mode — Fails if: "${staticWording}"`, async () => {
  for (const rule of [[], ["--fake-rule", "count"], ["--fake-rule", "exclude"]]) {
    const answer = await runCli(service, [query(receipt), ...rule]);
    expect(answerFieldNames(answer).filter(field => /coverage|covered/i.test(field))).toEqual([]);
  }
}, 20_000);

test(`A3 default text for counted Effect tests uses only static-path wording — Fails if: "${staticWording}"`, async () => {
  const result = await runRaw(service, [query(receipt), "--fake-rule", "count"], { json: false });
  expect(result.exitCode, result.stderr || result.stdout).toBe(0);
  expect(result.stdout).toContain("static-call-path");
  expect(result.stdout).toContain("submits a sealed parcel");
  // A disclaimer that the links are "not execution coverage" does not call them coverage (COO fix, 2026-10-17).
  expect(result.stdout.replace(/\bnot execution coverage\b/gi, "")).not.toMatch(/\b(?:coverage|covered)\b/i);
}, 20_000);

test(`A3 default text for undecided Effect tests uses only static-path wording — Fails if: "${staticWording}"`, async () => {
  const result = await runRaw(service, [query(seal)], { json: false });
  expect(result.exitCode, result.stderr || result.stdout).toBe(0);
  expect(result.stdout).toContain("static-call-path");
  expect(result.stdout).toContain("fake rule not set (A3)");
  // A disclaimer that the links are "not execution coverage" does not call them coverage (COO fix, 2026-10-17).
  expect(result.stdout.replace(/\bnot execution coverage\b/gi, "")).not.toMatch(/\b(?:coverage|covered)\b/i);
}, 20_000);

test(`A3 default text for direct tests uses only static-path wording — Fails if: "${staticWording}"`, async () => {
  const result = await runRaw(direct, [query(stamp)], { json: false });
  expect(result.exitCode, result.stderr || result.stdout).toBe(0);
  expect(result.stdout).toContain("static-call-path");
  expect(result.stdout).toContain("two calls are one test case");
  // A disclaimer that the links are "not execution coverage" does not call them coverage (COO fix, 2026-10-17).
  expect(result.stdout.replace(/\bnot execution coverage\b/gi, "")).not.toMatch(/\b(?:coverage|covered)\b/i);
}, 20_000);

async function expectFileReportDeclined(project: string, file: string) {
  const result = await runRaw(project, ["--file", file, "--fake-rule", "count"]);
  expect([0, 2], result.stderr || result.stdout).toContain(result.exitCode);
  if (result.exitCode === 2) {
    expect(result.stdout.trim()).toBe("");
    expect(result.stderr.trim().length).toBeGreaterThan(0);
    return;
  }
  const answer = JSON.parse(result.stdout);
  expect(answer.command).toBe("tests");
  expect(Array.isArray(answer.limits)).toBe(true);
  const allowed = new Set(["command", "query", "limits", "empty"]);
  expect(Object.keys(answer).filter(key => !allowed.has(key)), "no report payload without --per-function").toEqual([]);
}

test(`A3 Effect file JSON requires explicit per-function permission — Fails if: "${fileReport}"`, async () => {
  await expectFileReportDeclined(service, "live.ts");
}, 20_000);

test(`A3 direct file JSON requires explicit per-function permission — Fails if: "${fileReport}"`, async () => {
  await expectFileReportDeclined(direct, "amounts.ts");
}, 20_000);

test(`A3 default text also declines the unrequested Effect file report — Fails if: "${fileReport}"`, async () => {
  const result = await runRaw(service, ["--file", "live.ts", "--fake-rule", "count"], { json: false });
  expect([0, 2], result.stderr || result.stdout).toContain(result.exitCode);
  expect(result.stdout).not.toContain("static-call-path");
  expect(result.stdout).not.toContain("submits a sealed parcel");
  expect(result.stdout).not.toContain("queues a second parcel");
  expect(result.stdout).not.toContain("hashes receipt directly");
}, 20_000);

test(`A3 explicit per-function flag enables the Effect file answer — Fails if: "${fileReport}"`, async () => {
  const answer = await runCli(service, ["--file", "live.ts", "--per-function", "--fake-rule", "count"]);
  expect(answer.tests.tests.length).toBeGreaterThan(0);
  expect(answer.tests.undecided).toEqual([]);
  expect([...new Set(answer.tests.tests.map((item: any) => item.name))].sort()).toEqual([
    "hashes receipt directly", "queues a second parcel", "submits a sealed parcel",
  ]);
  const terminalLocations: Loc[] = [];
  for (const item of answer.tests.tests) {
    expect(item.path.length).toBeGreaterThan(0);
    item.path.forEach((link: any) => expectLink(service, link));
    const terminal = item.path.at(-1).to;
    expect(terminal.file).toBe("live.ts");
    terminalLocations.push({ file: terminal.file, line: terminal.line });
  }
  expect(terminalLocations).toContainEqual(receipt);
  expect(terminalLocations).toContainEqual(seal);
}, 20_000);
