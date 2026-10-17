import { expect, test } from "bun:test";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

// The owner's rule: a body written straight into a call (a callback or a generator passed as an argument) is its own
// place, and going into it adds no level. Calls inside such bodies, however deeply nested, are callees of the named
// function that holds them; a call inside a separately named const arrow belongs to that arrow.

const packageDir = resolve(import.meta.dir, "../..");
const fixtureDir = resolve(import.meta.dir, "fixtures");
const project = "nested-inline";
const missingLink = "a known link within the depth is missing";
const contradictoryLink = "a shown link contradicts the code";
const linkFailure = `${missingLink}, or ${contradictoryLink}`;

type Loc = { file: string; line: number };

// The expected graph is read from the fixture source, never from the tool's own analysis.
function loc(file: string, anchor: string): Loc {
  const lines = readFileSync(resolve(fixtureDir, project, file), "utf8").split("\n");
  const positions = lines.flatMap((line, index) => line.includes(anchor) ? [index + 1] : []);
  expect(positions, `unique fixture anchor: ${project}/${file}: ${anchor}`).toHaveLength(1);
  return { file, line: positions[0]! };
}

function query(at: Loc): string { return `${at.file}:${at.line}`; }

async function runCli(args: string[]): Promise<any> {
  const root = resolve(fixtureDir, project);
  const child = Bun.spawn([
    process.execPath, "src/cli.ts", ...args,
    "--project", resolve(root, "tsconfig.json"), "--root", root,
    "--tests", "*.checks.ts", "--json",
  ], { cwd: packageDir, stdout: "pipe", stderr: "pipe" });
  const timer = setTimeout(() => child.kill(), 15_000);
  try {
    const [exitCode, stdout, stderr] = await Promise.all([
      child.exited, new Response(child.stdout).text(), new Response(child.stderr).text(),
    ]);
    expect(exitCode, stderr || stdout).toBe(0);
    const answer = JSON.parse(stdout);
    expect(answer.command).toBe(args[0]);
    expect(Array.isArray(answer.limits)).toBe(true);
    return answer;
  } finally {
    clearTimeout(timer);
  }
}

function flatten(steps: any[]): any[] {
  expect(Array.isArray(steps)).toBe(true);
  return steps.flatMap((step: any): any[] => [step, ...flatten(step.children)]);
}

function matchesLoc(value: any, at: Loc): boolean {
  return value?.file === at.file && value?.line === at.line;
}

function linksAt(answer: any, site: Loc): any[] {
  expect(Array.isArray(answer.links), `callees answer has links (${JSON.stringify(answer.empty ?? null)})`).toBe(true);
  return answer.links.filter((link: any) => matchesLoc(link.site, site));
}

// Places in the fixture.
const attempt = loc("step.ts", "export const attempt =");
const executeTool = loc("step.ts", "const executeTool =");
const publish = loc("step.ts", "export const publish =");
const flatMap = loc("runtime.ts", "export function flatMap");

// Inline bodies inside attempt: each is its own place, but none adds a level.
const eachEvent = loc("step.ts", "yield* Stream.runForEach(stream, (event) =>");
// Four spaces: the generator on its own line, not the one after `(update) =>` below.
const genBody = loc("step.ts", "    Effect.gen(function* () {");
const maskBody = loc("step.ts", "yield* Effect.uninterruptibleMask((restore) =>");

// Call sites, each on its own line.
const publishSite = loc("step.ts", "yield* publish(event);");
const executeSite = loc("step.ts", "executeTool(event),");
// `store` is passed, not called: the call on this line is Effect.flatMap(store), whose target is flatMap.
const storeSite = loc("step.ts", "Effect.flatMap(store),");
const runSite = loc("step.ts", "return input.run(call);");

const expected = [
  { name: "publish(event)", site: publishSite, to: publish, holders: [attempt, eachEvent, genBody] },
  { name: "executeTool(event)", site: executeSite, to: executeTool, holders: [attempt, eachEvent, genBody, maskBody] },
  { name: "Effect.flatMap(store)", site: storeSite, to: flatMap, holders: [attempt, eachEvent, genBody, maskBody] },
];

function expectHeldByAttempt(link: any, holders: Loc[], name: string) {
  expect(holders.some(at => matchesLoc(link.from, at)),
    `${name}: from ${JSON.stringify(link.from)} is attempt or an inline body inside it`).toBe(true);
  expect(matchesLoc(link.from, executeTool), `${name}: not attributed to executeTool`).toBe(false);
}

test(`A2 calls in nested inline bodies are level-1 callees of the named function — Fails if: "${linkFailure}"`, async () => {
  const callees = await runCli(["callees", query(attempt)]);
  for (const edge of expected) {
    const found = linksAt(callees, edge.site);
    expect(found, `callees of attempt include ${edge.name} at ${query(edge.site)}`).toHaveLength(1);
    const link = found[0];
    expectHeldByAttempt(link, edge.holders, edge.name);
    expect(link.resolution, `${edge.name} resolves`).toBe("implementation");
    expect(matchesLoc(link.to, edge.to), `${edge.name}: to ${JSON.stringify(link.to)} is ${query(edge.to)}`).toBe(true);
  }

  const chain = await runCli(["chain", query(attempt), "--down", "1"]);
  const steps = flatten(chain.chain.down);
  for (const edge of expected) {
    const found = steps.filter(step => matchesLoc(step.link.site, edge.site));
    expect(found, `chain --down 1 shows ${edge.name} at ${query(edge.site)}`).toHaveLength(1);
    expect(found[0].level, `${edge.name} adds no level for the inline bodies`).toBe(1);
    expectHeldByAttempt(found[0].link, edge.holders, edge.name);
    expect(matchesLoc(found[0].link.to, edge.to), `${edge.name}: chain target is ${query(edge.to)}`).toBe(true);
  }
}, 20_000);

test(`A2 a call inside a named const arrow belongs to that arrow, one level further — Fails if: "${linkFailure}"`, async () => {
  const callees = await runCli(["callees", query(attempt)]);
  expect(linksAt(callees, runSite), `callees of attempt exclude input.run(call) at ${query(runSite)}`).toEqual([]);

  const chainOne = await runCli(["chain", query(attempt), "--down", "1"]);
  expect(flatten(chainOne.chain.down).filter(step => matchesLoc(step.link.site, runSite)),
    `chain --down 1 does not show input.run(call) at ${query(runSite)}`).toEqual([]);

  // The link is not lost: it is executeTool's callee, and level 2 from attempt.
  const own = await runCli(["callees", query(executeTool)]);
  const ownLinks = linksAt(own, runSite);
  expect(ownLinks, `callees of executeTool include input.run(call) at ${query(runSite)}`).toHaveLength(1);
  expect(matchesLoc(ownLinks[0].from, executeTool), `input.run(call) is held by executeTool`).toBe(true);

  const chainTwo = await runCli(["chain", query(attempt), "--down", "2"]);
  const deeper = flatten(chainTwo.chain.down).filter(step => matchesLoc(step.link.site, runSite));
  expect(deeper, `chain --down 2 shows input.run(call) at ${query(runSite)}`).toHaveLength(1);
  expect(deeper[0].level).toBe(2);
  expect(matchesLoc(deeper[0].link.from, executeTool), `input.run(call) is held by executeTool`).toBe(true);
}, 20_000);

// The inline callback sits in a call chain whose result a const holds: `const providerStream = source(input).pipe(
// Stream.runForEach((update) => Effect.gen(function* () { ... })))`. The const names the call result, not the callback,
// so the callback and its generator are inline bodies, and their calls are level-1 callees of attempt.
const chainCallback = loc("step.ts", "Stream.runForEach((update) => Effect.gen(function* () {");
const chainMask = loc("step.ts", "yield* Effect.uninterruptibleMask((restoreNext) =>");
const chained = [
  { name: "publish(update)", site: loc("step.ts", "yield* publish(update);"), to: publish,
    holders: [attempt, chainCallback] },
  { name: "executeTool(update)", site: loc("step.ts", "executeTool(update),"), to: executeTool,
    holders: [attempt, chainCallback, chainMask] },
];

test(`A2 an inline callback in a call chain held by a const is part of the named function — Fails if: "${linkFailure}"`, async () => {
  const callees = await runCli(["callees", query(attempt)]);
  for (const edge of chained) {
    const found = linksAt(callees, edge.site);
    expect(found, `callees of attempt include ${edge.name} at ${query(edge.site)}`).toHaveLength(1);
    const link = found[0];
    expectHeldByAttempt(link, edge.holders, edge.name);
    expect(link.resolution, `${edge.name} resolves`).toBe("implementation");
    expect(matchesLoc(link.to, edge.to), `${edge.name}: to ${JSON.stringify(link.to)} is ${query(edge.to)}`).toBe(true);
  }
}, 20_000);
