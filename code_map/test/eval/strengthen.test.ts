import { afterEach, expect, test } from "bun:test";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { loadCaseFile } from "../../eval/case-file.ts";
import { validateAnswer } from "../../eval/contract.ts";
import { matchAnswer } from "../../eval/matcher.ts";
import { shellQuote } from "../../eval/process.ts";
import { evaluate } from "../../eval/run.ts";

const evalDir = resolve(import.meta.dir, "../../eval");
const suite = await loadCaseFile(resolve(evalDir, "cases/fixtures.json"));
const canned = async (id: string) => JSON.parse(await readFile(resolve(evalDir, "stub/answers", id + ".json"), "utf8"));
const scratch: string[] = [];
afterEach(async () => { for (const path of scratch.splice(0)) await rm(path, { recursive: true, force: true }); });

// A depth-first walk can produce a contract-valid tree that loses a reachable tail.
function loseShorterRoute(answer: any, direction: "up" | "down") {
  const steps = answer.chain[direction];
  const short = steps.find((step: any) => step.children[0]?.children.length);
  const long = steps.find((step: any) => step !== short);
  const shared = long.children[0];
  const leaf = structuredClone(short.children[0]);
  leaf.level = 3; leaf.children = []; leaf.stop = { reason: "depth" };
  shared.children = [leaf]; delete shared.stop;
  short.children = [];
  short.stop = { reason: "seen", ref: shared.link[direction === "down" ? "to" : "from"] };
  answer.chain[direction] = [long, short];
}

const mutations: [string, (answer: any) => void][] = [
  ["A5-exact-callees", answer => answer.links.push(structuredClone(answer.links[0]))],
  ["A5-exact-not-found", answer => answer.limits.push({ reason: "dynamic" })],
  ["A5-exact-depth-stop", answer => answer.chain.down[0].stop.reason = "dynamic"],
  ["A2-inline-generator-owner", answer => { answer.links[0].from.line = 3; answer.links[0].from.name = "launchInline"; }],
  ["A2-same-name-helper-fake", answer => {
    const edge = answer.links[0];
    const helper = { file: "effect-shadow/helper.ts", line: 1, name: "deliver", kind: "function" };
    edge.to = helper; edge.candidates = [{ ...helper, testFake: false }];
  }],
  ["A2-effect-step-ambiguous", answer => { answer.matches.pop(); answer.ambiguous = false; }],
  ...(["down", "up"] as const).flatMap(direction => ["", "-reversed"].map(suffix =>
    [`A2-shorter-route-${direction}${suffix}`, (answer: any) => loseShorterRoute(answer, direction)] as [string, (answer: any) => void])),
];

// These variations come from the spec's Loc, Node, Link and Limit shapes, not tool output.
function allowedVariant(answer: any) {
  const ends: Record<string, number> = {
    "effect-inline/use.ts:4": 7, "effect-shadow/use.ts:3": 6,
    "effect-twins/one.ts:2": 4, "effect-twins/two.ts:2": 4,
    "route-depth/down.ts:1": 4, "route-depth/down-reversed.ts:1": 4,
  };
  function visit(value: any) {
    if (Array.isArray(value)) { value.forEach(visit); return; }
    if (!value || typeof value !== "object") return;
    if (typeof value.file === "string" && typeof value.line === "number") {
      value.endLine = ends[`${value.file}:${value.line}`] ?? value.line;
    }
    if (value.site && value.to) {
      value.declaration = value.kind === "service-call"
        ? { file: value.site.file.replace("use.ts", "api.ts"), line: 2 }
        : { file: value.to.file, line: value.to.line };
      value.to.testFake = false;
    }
    if (value.candidates) value.candidates.reverse();
    if (value.matches) value.matches.reverse();
    if (value.chain) { value.chain.up.reverse(); value.chain.down.reverse(); }
    if (value.stop?.reason === "depth") value.stop.text = "requested depth reached";
    Object.values(value).forEach(visit);
  }
  visit(answer);
  if (answer.links?.[0]?.from.file === "effect-inline/use.ts") answer.links[0].from.name = "generator callback";
  return answer;
}

for (const [id, mutate] of mutations) test(`${id}: stub is MET; its targeted wrong answer is NOT MET`, async () => {
  const cwd = await mkdtemp(resolve(import.meta.dir, ".strengthen-")); scratch.push(cwd);
  const sample = suite.cases.find(sample => sample.id === id)!;
  const caseFile = resolve(cwd, "case.json");
  await writeFile(caseFile, JSON.stringify({ ...suite, cases: [sample] }));
  const baseline = await evaluate({ tool: `${shellQuote(process.execPath)} ${shellQuote(resolve(evalDir, "stub/stub.ts"))}`,
    cases: [caseFile], out: resolve(cwd, "baseline"), cwd });
  expect(baseline.cases[0]!.status).toBe("MET");
  const allowed = allowedVariant(await canned(id));
  expect(validateAnswer(allowed, sample.args, suite.tests, suite.root)).toEqual([]);
  expect(matchAnswer(allowed, sample.expect)).toEqual([]);
  const toolPath = resolve(cwd, "answer.ts");
  await writeFile(toolPath, `console.log(${JSON.stringify(JSON.stringify(allowed))});\n`);
  const variant = await evaluate({ tool: `${shellQuote(process.execPath)} ${shellQuote(toolPath)}`,
    cases: [caseFile], out: resolve(cwd, "allowed"), cwd });
  expect(variant.cases[0]!.status).toBe("MET");
  const broken = structuredClone(allowed); mutate(broken);
  if (id.startsWith("A2-shorter-route-")) {
    expect(validateAnswer(broken, sample.args, suite.tests, suite.root)).toEqual([]);
    expect(matchAnswer(broken, sample.expect).length).toBeGreaterThan(0);
  }
  await writeFile(toolPath, `console.log(${JSON.stringify(JSON.stringify(broken))});\n`);
  const result = await evaluate({ tool: `${shellQuote(process.execPath)} ${shellQuote(toolPath)}`,
    cases: [caseFile], out: resolve(cwd, "mutated"), cwd });
  expect(result.cases[0]!.process.exitCode).toBe(0);
  expect(result.cases[0]!.status).toBe("NOT MET");
  expect(result.requirements.find(requirement => requirement.requirement === sample.requirement)!.status).toBe("NOT MET");
}, 30_000);

test("link shapes reject changed endpoints, changed sites, extra links, and unasked sections", async () => {
  for (const id of ["A5-exact-callees", "A2-inline-generator-owner", "A2-same-name-helper-fake"]) {
    const sample = suite.cases.find(sample => sample.id === id)!;
    for (const field of ["from", "site", "to"]) {
      const broken = await canned(id); broken.links[0][field].line += 1;
      expect(matchAnswer(broken, sample.expect).length).toBeGreaterThan(0);
    }
    const extra = await canned(id); extra.links.push(structuredClone(extra.links[0]));
    expect(matchAnswer(extra, sample.expect).length).toBeGreaterThan(0);
    const missing = await canned(id); missing.links = [];
    expect(matchAnswer(missing, sample.expect).length).toBeGreaterThan(0);
    const split = await canned(id);
    split.links = ["from", "site", "to"].map(field => {
      const edge = structuredClone(split.links[0]); edge[field].line += 1; return edge;
    });
    expect(matchAnswer(split, sample.expect).length).toBeGreaterThan(0);
  }
  const sample = suite.cases.find(sample => sample.id === "A5-exact-callees")!;
  for (const section of ["map", "chain", "tests"]) {
    const broken = await canned(sample.id); broken[section] = {};
    expect(validateAnswer(broken, sample.args, suite.tests, suite.root).some(failure => failure.path === section)).toBe(true);
  }
  const withMatches = await canned(sample.id);
  withMatches.matches = [withMatches.links[0].to]; withMatches.ambiguous = false;
  expect(validateAnswer(withMatches, sample.args, suite.tests, suite.root).some(failure => failure.path === "matches")).toBe(true);
});

test("optional declarations can be omitted without losing holder names or candidate checks", async () => {
  for (const id of ["A2-inline-generator-owner", "A2-same-name-helper-fake"]) {
    const sample = suite.cases.find(sample => sample.id === id)!;
    const allowed = allowedVariant(await canned(id)); delete allowed.links[0].declaration;
    expect(validateAnswer(allowed, sample.args, suite.tests, suite.root)).toEqual([]);
    expect(matchAnswer(allowed, sample.expect)).toEqual([]);
    const missingCandidate = structuredClone(allowed); missingCandidate.links[0].candidates.pop();
    expect(matchAnswer(missingCandidate, sample.expect).length).toBeGreaterThan(0);
    const extraCandidate = structuredClone(allowed);
    extraCandidate.links[0].candidates.push(structuredClone(extraCandidate.links[0].candidates[0]));
    expect(matchAnswer(extraCandidate, sample.expect).length).toBeGreaterThan(0);
  }
  const sample = suite.cases.find(sample => sample.id === "A2-same-name-helper-fake")!;
  const wrongHolder = await canned(sample.id); wrongHolder.links[0].from.name = "anonymous";
  expect(matchAnswer(wrongHolder, sample.expect).length).toBeGreaterThan(0);
});

test("ambiguous candidates form an exact unordered list with fixed source locations", async () => {
  const sample = suite.cases.find(sample => sample.id === "A2-effect-step-ambiguous")!;
  for (const mutate of [
    (answer: any) => answer.matches.pop(),
    (answer: any) => answer.matches.push(structuredClone(answer.matches[0])),
    (answer: any) => answer.matches[0].line++,
    (answer: any) => answer.matches[0].name = "wrongStep",
  ]) {
    const broken = allowedVariant(await canned(sample.id)); mutate(broken);
    expect(matchAnswer(broken, sample.expect).length).toBeGreaterThan(0);
  }
});

test("one-level depth requires the stop and rejects extra reasons or branches", async () => {
  const sample = suite.cases.find(sample => sample.id === "A5-exact-depth-stop")!;
  const allowed = allowedVariant(await canned(sample.id)); allowed.limits = [];
  expect(validateAnswer(allowed, sample.args, suite.tests, suite.root)).toEqual([]);
  expect(matchAnswer(allowed, sample.expect)).toEqual([]);
  for (const mutate of [
    (answer: any) => delete answer.chain.down[0].stop,
    (answer: any) => answer.limits.push({ reason: "dynamic" }),
    (answer: any) => answer.chain.down[0].stop.reason = "dynamic",
    (answer: any) => answer.chain.down[0].children.push(structuredClone(answer.chain.down[0])),
    (answer: any) => answer.chain.up.push(structuredClone(answer.chain.down[0])),
  ]) {
    const broken = structuredClone(allowed); mutate(broken);
    expect(matchAnswer(broken, sample.expect).length).toBeGreaterThan(0);
  }
});

test("not-found still requires exactly its reason, including when reasons are missing", async () => {
  const sample = suite.cases.find(sample => sample.id === "A5-exact-not-found")!;
  for (const limits of [[], [{ reason: "dynamic" }], [{ reason: "not-found" }, { reason: "dynamic" }]]) {
    const broken = await canned(sample.id); broken.limits = limits;
    expect(matchAnswer(broken, sample.expect).length).toBeGreaterThan(0);
  }
});

test("service fake stays a candidate and cannot replace the real link", async () => {
  const sample = suite.cases.find(sample => sample.id === "A2-same-name-helper-fake")!;
  const broken = await canned(sample.id);
  broken.links[0].to = broken.links[0].candidates[1];
  expect(matchAnswer(broken, sample.expect).some(failure => failure.message === "excludes location check failed")).toBe(true);
});

test("computed-member rejects an invented link even with its dynamic limit", async () => {
  const sample = suite.cases.find(sample => sample.id === "A2-computed-member")!;
  const broken = await canned(sample.id);
  const edge = (await canned("A5-exact-callees")).links[0];
  edge.from = { file: "computed/use.ts", line: 1, name: "computed", kind: "function" };
  edge.site = { file: "computed/use.ts", line: 2 };
  broken.links = [edge]; delete broken.empty;
  expect(validateAnswer(broken, sample.args, suite.tests, suite.root)).toEqual([]);
  expect(matchAnswer(broken, sample.expect).map(failure => failure.path)).toEqual(["links"]);
});

test("default text rejects an unrelated definition in an otherwise correct answer", async () => {
  const sample = suite.cases.find(sample => sample.id === "A5-default-text")!;
  const text = "leaf — chain/logic.ts:3\n";
  expect(matchAnswer(text, sample.expect)).toEqual([]);
  expect(matchAnswer(text + "recursive — chain/logic.ts:4\n", sample.expect)).toHaveLength(1);
});

test("shared-chain checks allow either output sibling order and reject dangling seen references", async () => {
  for (const direction of ["down", "up"] as const) for (const suffix of ["", "-reversed"]) {
    const id = `A2-shorter-route-${direction}${suffix}`;
    const sample = suite.cases.find(sample => sample.id === id)!;
    const answer = await canned(id); answer.chain[direction].reverse();
    expect(matchAnswer(answer, sample.expect)).toEqual([]);
    expect(validateAnswer(answer, sample.args, suite.tests, suite.root)).toEqual([]);
    const [, canonical] = answer.chain[direction];
    canonical.stop = answer.chain[direction][0].children[0].stop; canonical.children = [];
    expect(validateAnswer(answer, sample.args, suite.tests, suite.root).length).toBeGreaterThan(0);
  }
});
