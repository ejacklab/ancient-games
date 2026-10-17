import { afterEach, beforeEach, expect, test } from "bun:test";
import { existsSync } from "node:fs";
import { rm } from "node:fs/promises";
import { resolve } from "node:path";

const packageDir = resolve(import.meta.dir, "../..");
const fixtureDir = resolve(import.meta.dir, "fixtures/passive-ledger");
const markers = ["ledger-ran.marker", "dependency-ran.marker", "test-file-ran.marker", "trap-ran.marker"];
const failsIf = "mapping a fixture whose top level writes a marker creates that marker.";

async function removeMarkers() {
  await Promise.all(markers.map(marker => rm(resolve(fixtureDir, marker), { force: true })));
}

beforeEach(removeMarkers);
afterEach(removeMarkers);

async function runCli(args: string[]) {
  const child = Bun.spawn([
    process.execPath, "src/cli.ts", ...args,
    "--project", resolve(fixtureDir, "tsconfig.json"),
    "--root", fixtureDir,
    "--tests", "*.checks.ts",
    "--json",
  ], { cwd: packageDir, stdout: "pipe", stderr: "pipe" });
  const timer = setTimeout(() => child.kill(), 15_000);
  try {
    const [exitCode, stdout, stderr] = await Promise.all([
      child.exited,
      new Response(child.stdout).text(),
      new Response(child.stderr).text(),
    ]);

    // Check effects before parsing: a marker remains a failure even with broken JSON or a crash.
    expect(markers.filter(marker => existsSync(resolve(fixtureDir, marker)))).toEqual([]);
    expect(exitCode, stderr || stdout).toBe(0);
    const answer = JSON.parse(stdout);
    expect(answer.command).toBe(args[0]);
    expect(Array.isArray(answer.query)).toBe(true);
    expect(Array.isArray(answer.limits)).toBe(true);
    expect(answer.empty).toBeUndefined();
    return answer;
  } finally {
    clearTimeout(timer);
  }
}

const recordTotal = { file: "ledger.ts", line: 9, name: "recordTotal", kind: "function" };
const adjustTotal = { file: "adjustment.ts", line: 8, name: "adjustTotal", kind: "function" };
const submitLedger = { file: "ledger.ts", line: 14, name: "submitLedger", kind: "function" };

test(`R1 map — Fails if: ${failsIf}`, async () => {
  const answer = await runCli(["map", "."]);
  expect(answer.map.definitions).toEqual(expect.arrayContaining([
    expect.objectContaining(recordTotal),
    expect.objectContaining(adjustTotal),
    expect.objectContaining(submitLedger),
    expect.objectContaining({ file: "trap.ts", line: 10, name: "dormantReceipt", kind: "function" }),
  ]));
}, 20_000);

test(`R1 chain — Fails if: ${failsIf}`, async () => {
  const answer = await runCli(["chain", "ledger.ts:9"]);
  expect(answer.chain.up).toEqual(expect.arrayContaining([
    expect.objectContaining({ level: 1, link: expect.objectContaining({
      from: expect.objectContaining(submitLedger), to: expect.objectContaining(recordTotal),
    }) }),
  ]));
  expect(answer.chain.down).toEqual(expect.arrayContaining([
    expect.objectContaining({ level: 1, link: expect.objectContaining({
      from: expect.objectContaining(recordTotal), to: expect.objectContaining(adjustTotal),
    }) }),
  ]));
}, 20_000);

test(`R1 tests — Fails if: ${failsIf}`, async () => {
  const answer = await runCli(["tests", "recordTotal"]);
  expect(answer.tests.label).toBe("static-call-path");
  expect(answer.tests.count).toBe(1);
  expect(answer.tests.tests).toHaveLength(1);
  expect(answer.tests.tests[0]).toMatchObject({
    file: "ledger.checks.ts", line: 9, name: "submits an adjusted ledger", throughFake: false,
  });
  expect(answer.tests.tests[0].path.length).toBeGreaterThan(0);
  expect(answer.tests.tests[0].path.at(-1).to).toMatchObject(recordTotal);
}, 20_000);

test(`R1 callers — Fails if: ${failsIf}`, async () => {
  const answer = await runCli(["callers", "recordTotal"]);
  expect(answer.links).toEqual(expect.arrayContaining([
    expect.objectContaining({
      from: expect.objectContaining(submitLedger), to: expect.objectContaining(recordTotal),
      kind: "call", resolution: "implementation", site: expect.objectContaining({ file: "ledger.ts", line: 15 }),
    }),
  ]));
}, 20_000);

test(`R1 callees — Fails if: ${failsIf}`, async () => {
  const answer = await runCli(["callees", "recordTotal"]);
  expect(answer.links).toEqual(expect.arrayContaining([
    expect.objectContaining({
      from: expect.objectContaining(recordTotal), to: expect.objectContaining(adjustTotal),
      kind: "call", resolution: "implementation", site: expect.objectContaining({ file: "ledger.ts", line: 10 }),
    }),
  ]));
}, 20_000);

test(`R1 where — Fails if: ${failsIf}`, async () => {
  const answer = await runCli(["where", "recordTotal"]);
  expect(answer.ambiguous).toBe(false);
  expect(answer.matches).toEqual([expect.objectContaining(recordTotal)]);
}, 20_000);

test(`R1 find — Fails if: ${failsIf}`, async () => {
  const answer = await runCli(["find", "return adjustTotal(amount);"]);
  expect(answer.matches.length).toBeGreaterThan(0);
  expect(answer.matches).toEqual(expect.arrayContaining([
    expect.objectContaining({ file: "ledger.ts", line: expect.any(Number) }),
  ]));
}, 20_000);
