import { expect, test } from "bun:test";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const packageDir = resolve(import.meta.dir, "../..");
const fixtureDir = resolve(import.meta.dir, "fixtures");
const silentStop = "a branch stops early without a reason";
const falseAbsence = "an empty result is presented as proof of absence";
const limitReasons = ["depth", "dynamic", "outside-repo", "other-process", "not-found", "seen", "other"];
type Loc = { file: string; line: number };

function loc(project: string, file: string, anchor: string): Loc {
  const lines = readFileSync(resolve(fixtureDir, project, file), "utf8").split("\n");
  const positions = lines.flatMap((line, index) => line.includes(anchor) ? [index + 1] : []);
  expect(positions, `unique fixture anchor: ${project}/${file}: ${anchor}`).toHaveLength(1);
  return { file, line: positions[0]! };
}

function query(at: Loc) { return `${at.file}:${at.line}`; }

async function runCli(project: string, command: string, questions: string[], options: string[] = [], json = true) {
  const root = resolve(fixtureDir, project);
  const child = Bun.spawn([
    process.execPath, "src/cli.ts", command, ...questions, ...options,
    "--project", resolve(root, "tsconfig.json"), "--root", root,
    "--tests", "*.checks.ts", ...(json ? ["--json"] : []),
  ], { cwd: packageDir, stdout: "pipe", stderr: "pipe" });
  const timer = setTimeout(() => child.kill(), 30_000);
  try {
    const [exitCode, stdout, stderr] = await Promise.all([
      child.exited, new Response(child.stdout).text(), new Response(child.stderr).text(),
    ]);
    expect(exitCode, stderr || stdout).toBe(0);
    if (!json) return stdout;
    const answer = JSON.parse(stdout);
    expect(answer.command).toBe(command);
    expect(answer.query).toEqual(questions);
    expect(Array.isArray(answer.limits)).toBe(true);
    for (const limit of answer.limits) {
      expect(limitReasons).toContain(limit.reason);
      if (limit.reason === "other") expect(limit.text?.trim().length).toBeGreaterThan(0);
    }
    return answer;
  } finally {
    clearTimeout(timer);
  }
}

function expectOmissionLimit(answer: any, cause: RegExp) {
  const limits = answer.limits.filter((limit: any) =>
    limit.reason === "other" && typeof limit.text === "string" && cause.test(limit.text));
  expect(limits.length, `an explicit omission limit, not an unrelated limit: ${JSON.stringify(answer.limits)}`)
    .toBeGreaterThan(0);
}

test(`L1 find ranked names retain comment/string matches or explain omissions — Fails if: "${silentStop}"`, async () => {
  const answer = await runCli("service-search", "find", ["archive parcel"]);
  const expected = ["archiveParcel", "queuedDispatch", "auditDispatch"].map(name =>
    loc("service-search", "workflow.ts", `export const ${name} =`));
  expect(answer.matches).toEqual(expect.arrayContaining([expect.objectContaining(expected[0]!)]));
  const missing = expected.filter(at => !answer.matches.some((match: Loc) => match.file === at.file && match.line === at.line));
  if (missing.length) {
    expectOmissionLimit(answer, /(?:rank|weaker|lower.scor|best.match|omit|discard|filter|truncat)/i);
  } else {
    expect(answer.ambiguous).toBe(true);
  }
}, 35_000);

for (const [description, name] of [["delayed vault", "queuedDispatch"], ["retention ledger", "auditDispatch"]]) {
  test(`L1 find ${description} control reads service comments/strings — Fails if: "${silentStop}"`, async () => {
    const answer = await runCli("service-search", "find", [description!]);
    expect(answer.matches).toEqual(expect.arrayContaining([
      expect.objectContaining(loc("service-search", "workflow.ts", `export const ${name} =`)),
    ]));
  }, 35_000);
}

function expectLimitAt(answer: any, at: Loc, reason: string) {
  expect(answer.limits, `${reason} limit at the stopped site ${query(at)}`).toEqual(expect.arrayContaining([
    expect.objectContaining({ reason, at: expect.objectContaining(at) }),
  ]));
}

function chainSteps(steps: any[]): any[] {
  return steps.flatMap(step => [step, ...chainSteps(step.children)]);
}

for (const [name, anchor, reason] of [
  ["applyCallback", "return callback();", "dynamic"],
  ["chooseRoute", "return routes[key]();", "dynamic"],
  ["roundInvoice", "return Math.abs(amount);", "outside-repo"],
  ["missingReceipt", "return yield* receipt.fetchReceipt();", "not-found"],
]) {
  test(`L1 callees ${name} locates its ${reason} stop — Fails if: "${silentStop}"`, async () => {
    const answer = await runCli("service-stops", "callees", [name!]);
    expectLimitAt(answer, loc("service-stops", "workflow.ts", anchor!), reason!);
  }, 35_000);
}

test(`L1 map keeps the computed service call's dynamic limit — Fails if: "${silentStop}"`, async () => {
  const answer = await runCli("service-stops", "map", ["workflow.ts"]);
  expect(answer.map.definitions.length).toBeGreaterThan(0);
  expectLimitAt(answer, loc("service-stops", "workflow.ts", "return routes[key]();"), "dynamic");
}, 35_000);

test(`L1 chain locates an unresolved service branch — Fails if: "${silentStop}"`, async () => {
  const at = loc("service-stops", "workflow.ts", "export const missingReceipt =");
  const answer = await runCli("service-stops", "chain", [query(at)], ["--up", "0", "--down", "4"]);
  const site = loc("service-stops", "workflow.ts", "return yield* receipt.fetchReceipt();");
  expectLimitAt(answer, site, "not-found");
  const stopped = chainSteps(answer.chain.down).find(step => step.link.site.file === site.file && step.link.site.line === site.line);
  expect(stopped, "the unresolved call stays visible in its branch").toBeDefined();
  expect(stopped.link.resolution).toBe("unresolved");
  expect(stopped.link.reason.trim().length).toBeGreaterThan(0);
}, 35_000);

test(`L1 chain service down-depth marks the truncated branch — Fails if: "${silentStop}"`, async () => {
  const at = loc("service-stops", "workflow.ts", "export const submitInvoice =");
  const answer = await runCli("service-stops", "chain", [query(at)], ["--up", "0", "--down", "1"]);
  const settle = loc("service-stops", "live.ts", "export const settle =");
  const step = chainSteps(answer.chain.down).find(step => step.link.to?.file === settle.file && step.link.to?.line === settle.line);
  expect(step, "the service branch at the requested depth").toBeDefined();
  expect(step.stop).toMatchObject({ reason: "depth" });
  expect(step.children).toEqual([]);
}, 35_000);

test(`L1 chain direct up-depth marks the truncated branch — Fails if: "${silentStop}"`, async () => {
  const at = loc("direct-stops", "logic.ts", "export function leaf(");
  const answer = await runCli("direct-stops", "chain", [query(at)], ["--up", "1", "--down", "0"]);
  const middle = loc("direct-stops", "logic.ts", "export function middle(");
  const step = chainSteps(answer.chain.up).find(step => step.link.from.file === middle.file && step.link.from.line === middle.line);
  expect(step, "the caller branch at the requested depth").toBeDefined();
  expect(step.stop).toMatchObject({ reason: "depth" });
  expect(step.children).toEqual([]);
}, 35_000);

test(`L1 chain zero-depth locates the stop at the selected service — Fails if: "${silentStop}"`, async () => {
  const at = loc("service-stops", "workflow.ts", "export const submitInvoice =");
  const answer = await runCli("service-stops", "chain", [query(at)], ["--up", "0", "--down", "0"]);
  expect(answer.chain).toEqual({ up: [], down: [] });
  expectLimitAt(answer, at, "depth");
}, 35_000);

for (const direction of ["up", "down"]) {
  test(`L1 chain ${direction} cycle names the previously shown location — Fails if: "${silentStop}"`, async () => {
    const at = loc("direct-stops", "logic.ts", "export function loopA(");
    const answer = await runCli("direct-stops", "chain", [query(at)], ["--up", "6", "--down", "6"]);
    const repeated = chainSteps(answer.chain[direction]).filter(step => step.stop?.reason === "seen");
    expect(repeated.length).toBeGreaterThan(0);
    for (const step of repeated) {
      expect(step.stop.ref).toMatchObject(at);
      expect(step.children).toEqual([]);
    }
  }, 35_000);
}

for (const command of ["find", "where", "callers", "callees", "chain", "tests", "map"]) {
  test(`L1 ${command} missing query names not-found and qualifies emptiness — Fails if: "${silentStop}"; "${falseAbsence}"`, async () => {
    const questions = [command === "map" ? "missing-nebula-module" : "absentNebulaSettlement"];
    const answer = await runCli("service-stops", command, questions);
    expect(answer.empty).toBe("none found by static analysis");
    expect(answer.limits).toEqual(expect.arrayContaining([expect.objectContaining({ reason: "not-found" })]));
    if (command === "map") {
      expect(answer.map).toMatchObject({ definitions: [], links: [], entries: [] });
    } else {
      expect(answer.matches).toEqual([]);
    }
    const text = await runCli("service-stops", command, questions, [], false);
    expect(text.toLowerCase()).toContain("none found by static analysis");
    expect(text.toLowerCase()).toContain("not-found");
  }, 65_000);
}

for (const command of ["callers", "callees", "chain", "tests"]) {
  test(`L1 ${command} existing idle service scopes its empty result in JSON and text — Fails if: "${falseAbsence}"`, async () => {
    const at = loc("service-stops", "workflow.ts", "export const idleInvoice =");
    const questions = [query(at)];
    const answer = await runCli("service-stops", command, questions);
    expect(answer.empty).toBe("none found by static analysis");
    if (command === "chain") expect(answer.chain).toEqual({ up: [], down: [] });
    else if (command === "tests") expect(answer.tests).toMatchObject({ count: 0, tests: [], undecided: [] });
    else expect(answer.links).toEqual([]);
    const text = await runCli("service-stops", command, questions, [], false);
    // A positive qualification allows wording such as "this is not proof of absence".
    expect(text.toLowerCase()).toContain("none found by static analysis");
  }, 65_000);
}
