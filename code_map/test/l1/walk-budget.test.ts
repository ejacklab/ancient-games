import { expect, test } from "bun:test";
import { cpSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

const packageDir = resolve(import.meta.dir, "../..");
const fixtureDir = resolve(import.meta.dir, "fixtures");
const silentStop = "a branch stops early without a reason";

function makeWalkFixture(functionCount: number, shape: "linear" | "wide") {
  const root = mkdtempSync(resolve(fixtureDir, "generated-service-walk-"));
  cpSync(resolve(fixtureDir, "service-long-walk"), root, { recursive: true });
  const hops = Array.from({ length: functionCount }, (_, index) =>
    `export function hop${index}(): number { return ${shape === "linear"
      ? index + 1 === functionCount ? "ledgerTarget()" : `hop${index + 1}()`
      : "1"}; }`);
  const runBody = shape === "linear" ? "  return hop0();" : [
    ...Array.from({ length: functionCount }, (_, index) => `  hop${index}();`),
    "  return delayedBridge();",
  ].join("\n");
  writeFileSync(resolve(root, "hops.ts"), [
    ...hops,
    "export function delayedBridge(): number { return ledgerTarget(); }",
    "export function ledgerTarget(): number { return 23; }",
    "",
  ].join("\n"));
  writeFileSync(resolve(root, "live.ts"), [
    'import { Effect } from "../effect-runtime";',
    'import { Ledger } from "./port";',
    `import { ${shape === "linear" ? "hop0" : [
      ...Array.from({ length: functionCount }, (_, index) => `hop${index}`), "delayedBridge",
    ].join(", ")} } from "./hops";`,
    'export const settle = Effect.fn("Ledger.settle")(function* () {',
    runBody,
    "});",
    "export const ledger = Ledger.of({ settle });",
    "",
  ].join("\n"));
  writeFileSync(resolve(root, "ledger.checks.ts"), [
    'import { submitLedger } from "./workflow";',
    "declare function test(name: string, body: () => unknown): void;",
    'test("settles a generated ledger", () => submitLedger());',
    "",
  ].join("\n"));
  return root;
}

async function runCli(root: string, command: string, questions: string[], json = true) {
  const child = Bun.spawn([
    process.execPath, "src/cli.ts", command, ...questions,
    "--project", resolve(root, "tsconfig.json"), "--root", root,
    "--tests", "*.checks.ts", "--fake-rule", "count", ...(json ? ["--json"] : []),
  ], { cwd: packageDir, stdout: "pipe", stderr: "pipe" });
  const timer = setTimeout(() => child.kill(), 30_000);
  try {
    const [exitCode, stdout, stderr] = await Promise.all([
      child.exited, new Response(child.stdout).text(), new Response(child.stderr).text(),
    ]);
    expect(exitCode, stderr || stdout).toBe(0);
    return json ? JSON.parse(stdout) : stdout;
  } finally {
    clearTimeout(timer);
  }
}

test(`L1 tests short generated service graph control reaches the target — Fails if: "${silentStop}"`, async () => {
  const root = makeWalkFixture(8, "linear");
  try {
    const answer = await runCli(root, "tests", ["ledgerTarget"]);
    expect(answer.tests).toMatchObject({ count: 1, undecided: [] });
    expect(answer.tests.tests[0]).toMatchObject({ file: "ledger.checks.ts", name: "settles a generated ledger" });
    expect(answer.tests.tests[0].path.length).toBeGreaterThan(8);
    expect(answer.tests.tests[0].path.some((link: any) => link.kind === "service-call")).toBe(true);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
}, 35_000);

for (const shape of ["linear", "wide"] as const) {
  test(`L1 tests 450-function ${shape} service walk finds the test or locates its budget stop — Fails if: "${silentStop}"`, async () => {
    const root = makeWalkFixture(450, shape);
    try {
      const answer = await runCli(root, "tests", ["ledgerTarget"]);
      expect(answer.tests.count).toBe(answer.tests.tests.length);
      const found = answer.tests.tests.find((item: any) => item.file === "ledger.checks.ts" && item.name === "settles a generated ledger");
      if (found) {
        const target = found.path.at(-1)?.to;
        expect(target).toMatchObject({ file: "hops.ts", name: "ledgerTarget" });
      } else {
        // A no-test-pattern, unresolved-call or fake-rule limit cannot explain this known static path.
        const stops = answer.limits.filter((limit: any) =>
          limit.reason === "other" && /(?:budget|visit|walk|travers|step|cap|maximum|search.limit)/i.test(limit.text ?? ""));
        expect(stops.length, `the known test was omitted without a traversal reason: ${JSON.stringify(answer.limits)}`)
          .toBeGreaterThan(0);
        for (const stop of stops) {
          expect(stop.at, "the source location where the traversal stopped").toBeDefined();
          expect(["ledger.checks.ts", "workflow.ts", "live.ts", "hops.ts"]).toContain(stop.at.file);
          const lineCount = readFileSync(resolve(root, stop.at.file), "utf8").split("\n").length;
          expect(Number.isInteger(stop.at.line)).toBe(true);
          expect(stop.at.line).toBeGreaterThan(0);
          expect(stop.at.line).toBeLessThanOrEqual(lineCount);
        }
        const text = await runCli(root, "tests", ["ledgerTarget"], false);
        for (const stop of stops) expect(text).toContain(stop.text);
        expect(text.toLowerCase()).toContain("none found by static analysis");
      }
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  }, 65_000);
}

test(`L1 chain default depth marks a longer generated service route — Fails if: "${silentStop}"`, async () => {
  const root = makeWalkFixture(12, "linear");
  try {
    const lines = readFileSync(resolve(root, "workflow.ts"), "utf8").split("\n");
    const positions = lines.flatMap((line, index) => line.includes("export const submitLedger =") ? [index + 1] : []);
    expect(positions).toHaveLength(1);
    const answer = await runCli(root, "chain", [`workflow.ts:${positions[0]}`]);
    const flatten = (steps: any[]): any[] => steps.flatMap(step => [step, ...flatten(step.children)]);
    const steps = flatten(answer.chain.down);
    const boundary = steps.filter(step => step.level === 6);
    expect(boundary.length).toBeGreaterThan(0);
    for (const step of boundary) {
      expect(step.stop).toMatchObject({ reason: "depth" });
      expect(step.children).toEqual([]);
    }
    expect(steps.every(step => step.level <= 6)).toBe(true);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
}, 35_000);
