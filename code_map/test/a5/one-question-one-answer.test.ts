import { expect, test } from "bun:test";
import { readFileSync } from "node:fs";
import { isAbsolute, resolve } from "node:path";

const packageDir = resolve(import.meta.dir, "../..");
const fixtureDir = resolve(import.meta.dir, "fixtures");
const service = "service-dispatch";
const credit = "credit-pipeline";
const failsIf = "an answer comes only inside a dump or without its evidence or limits, or a whole map is produced unasked.";
const nodeKinds = ["function", "method", "arrow", "effect-fn", "property", "class", "variable", "interface-member", "other"];
const limitReasons = ["depth", "dynamic", "outside-repo", "other-process", "not-found", "seen", "other"];

type Loc = { file: string; line: number };

function loc(project: string, file: string, anchor: string): Loc {
  const lines = readFileSync(resolve(fixtureDir, project, file), "utf8").split("\n");
  const positions = lines.flatMap((line, index) => line.includes(anchor) ? [index + 1] : []);
  expect(positions, `unique fixture anchor: ${project}/${file}: ${anchor}`).toHaveLength(1);
  return { file, line: positions[0]! };
}

function query(at: Loc) { return `${at.file}:${at.line}`; }

const dispatch = loc(service, "module/workflow.ts", "export const dispatchTicket =");
const route = loc(service, "module/live.ts", "const routeTicket =");
const routeSite = loc(service, "module/workflow.ts", "router.routeTicket(ticket)");
const receive = loc(service, "caller.ts", "export function receiveTicket");
const receiveSite = loc(service, "caller.ts", "return dispatchTicket(ticket)");
const creditLeaf = loc(credit, "module/amount.ts", "export function unitCredit");
const creditMiddle = loc(credit, "module/amount.ts", "export function paddedCredit");

async function runCli(project: string, command: string, questions: string[], options: string[] = [], patterns = ["*.checks.ts"]) {
  const root = resolve(fixtureDir, project);
  const child = Bun.spawn([
    process.execPath, "src/cli.ts", command, ...questions, ...options,
    "--project", resolve(root, "tsconfig.json"), "--root", root,
    ...patterns.flatMap(pattern => ["--tests", pattern]), "--json",
  ], { cwd: packageDir, stdout: "pipe", stderr: "pipe" });
  const timer = setTimeout(() => child.kill(), 15_000);
  try {
    const [exitCode, stdout, stderr] = await Promise.all([
      child.exited, new Response(child.stdout).text(), new Response(child.stderr).text(),
    ]);
    expect(exitCode, stderr || stdout).toBe(0);
    const answer = JSON.parse(stdout);
    expect(answer.command).toBe(command);
    expect(answer.query).toEqual(questions);
    expect(Array.isArray(answer.limits)).toBe(true);
    for (const limit of answer.limits) {
      expect(limitReasons).toContain(limit.reason);
      if (limit.at !== undefined) expectLoc(limit.at);
      if (limit.ref !== undefined) expectLoc(limit.ref);
      if (limit.text !== undefined) expect(typeof limit.text).toBe("string");
    }
    return answer;
  } finally {
    clearTimeout(timer);
  }
}

// Check the public envelope as well as the requested payload: putting the answer inside map is a failure.
function expectFocused(answer: any, payload: "matches" | "links" | "chain" | "tests" | "map") {
  const allowed = new Set(["command", "query", "ambiguous", "limits", "empty", payload]);
  expect(Object.keys(answer).filter(key => !allowed.has(key)), "unasked answer sections").toEqual([]);
  expect(answer[payload]).toBeDefined();
  if (payload !== "map") expect(answer.map).toBeUndefined();
}

function expectLoc(at: any) {
  expect(typeof at.file).toBe("string");
  expect(at.file.length).toBeGreaterThan(0);
  expect(isAbsolute(at.file)).toBe(false);
  expect(Number.isInteger(at.line)).toBe(true);
  expect(at.line).toBeGreaterThan(0);
  if (at.endLine !== undefined) expect(at.endLine).toBeGreaterThanOrEqual(at.line);
}

function expectNode(node: any) {
  expectLoc(node);
  expect(typeof node.name).toBe("string");
  expect(node.name.length).toBeGreaterThan(0);
  expect(nodeKinds).toContain(node.kind);
}

function expectLink(link: any) {
  expectNode(link.from);
  expectLoc(link.site);
  expect(["call", "new", "service-call"]).toContain(link.kind);
  expect(["definition", "implementation-lookup"]).toContain(link.via);
  expect(["implementation", "unresolved", "ambiguous"]).toContain(link.resolution);
  if (link.declaration !== undefined) expectLoc(link.declaration);
  expect(Array.isArray(link.candidates)).toBe(true);
  for (const candidate of link.candidates) {
    expectNode(candidate);
    expect(typeof candidate.testFake).toBe("boolean");
  }
  if (link.resolution === "implementation") expectNode(link.to);
  else expect(link.to).toBeUndefined();
  if (link.resolution === "unresolved") {
    expect(typeof link.reason).toBe("string");
    expect(link.reason.trim().length).toBeGreaterThan(0);
  }
}

function atSite(links: any[], at: Loc) {
  const found = links.filter(link => link.site.file === at.file && link.site.line === at.line);
  expect(found, `evidence for ${query(at)}`).toHaveLength(1);
  return found[0];
}

test(`A5 where returns only the requested service definition — Fails if: "${failsIf}"`, async () => {
  const answer = await runCli(service, "where", ["dispatchTicket"]);
  expectFocused(answer, "matches");
  expect(answer.ambiguous).toBe(false);
  expect(answer.matches).toHaveLength(1);
  expectNode(answer.matches[0]);
  expect(answer.matches[0]).toMatchObject({ ...dispatch, name: "dispatchTicket", kind: "effect-fn" });
  expect(answer.empty).toBeUndefined();
}, 20_000);

test(`A5 find returns the matching service place with its source — Fails if: "${failsIf}"`, async () => {
  const answer = await runCli(service, "find", ["router.routeTicket(ticket)"]);
  expectFocused(answer, "matches");
  expect(answer.ambiguous).toBe(false);
  expect(answer.matches).toHaveLength(1);
  expectNode(answer.matches[0]);
  // A place may identify the snippet or the named function containing it.
  expect(answer.matches[0].file).toBe(routeSite.file);
  expect([dispatch.line, routeSite.line]).toContain(answer.matches[0].line);
  expect(answer.empty).toBeUndefined();
}, 20_000);

test(`A5 callers returns only callers with call-site evidence — Fails if: "${failsIf}"`, async () => {
  const answer = await runCli(service, "callers", [query(dispatch)]);
  expectFocused(answer, "links");
  expect(answer.links).toHaveLength(2);
  answer.links.forEach(expectLink);
  const link = atSite(answer.links, receiveSite);
  expect(link.from).toMatchObject({ ...receive, name: "receiveTicket" });
  expect(link.to).toMatchObject({ ...dispatch, name: "dispatchTicket" });
  expect(atSite(answer.links, loc(service, "dispatch.checks.ts", 'dispatchTicket("incident-83")')).to)
    .toMatchObject(dispatch);
  expect(answer.empty).toBeUndefined();
}, 20_000);

test(`A5 callees returns the typed service answer with declaration and implementation evidence — Fails if: "${failsIf}"`, async () => {
  const answer = await runCli(service, "callees", [query(dispatch)]);
  expectFocused(answer, "links");
  expect(answer.links).toHaveLength(1);
  answer.links.forEach(expectLink);
  const link = atSite(answer.links, routeSite);
  expect(link).toMatchObject({
    from: dispatch, kind: "service-call", via: "implementation-lookup", resolution: "implementation",
    declaration: loc(service, "port.ts", "readonly routeTicket:"), to: { ...route, name: "routeTicket" },
  });
  expect(answer.empty).toBeUndefined();
}, 20_000);

test(`A5 chain returns only the requested service branch and its depth limit — Fails if: "${failsIf}"`, async () => {
  const answer = await runCli(service, "chain", [query(dispatch)], ["--up", "0", "--down", "1"]);
  expectFocused(answer, "chain");
  expect(answer.chain.up).toEqual([]);
  expect(answer.chain.down).toHaveLength(1);
  const step = answer.chain.down[0];
  expectLink(step.link);
  expect(step).toMatchObject({ level: 1, link: { site: routeSite, to: route }, children: [], stop: { reason: "depth" } });
  expect(answer.limits).toEqual(expect.arrayContaining([expect.objectContaining({ reason: "depth" })]));
  expect(answer.empty).toBeUndefined();
}, 20_000);

test(`A5 tests returns only the selected function's static paths as evidence — Fails if: "${failsIf}"`, async () => {
  const answer = await runCli(service, "tests", [query(route)], ["--fake-rule", "count"]);
  expectFocused(answer, "tests");
  expect(answer.tests).toMatchObject({ label: "static-call-path", count: 1, undecided: [] });
  expect(answer.tests.tests).toHaveLength(1);
  const reached = answer.tests.tests[0];
  expect(reached).toMatchObject({
    ...loc(service, "dispatch.checks.ts", 'test("dispatches an incident ticket"'),
    name: "dispatches an incident ticket", throughFake: true,
  });
  expect(reached.path).toHaveLength(2);
  reached.path.forEach(expectLink);
  expect(reached.path[0].to).toMatchObject(dispatch);
  expect(reached.path[1]).toMatchObject({ from: dispatch, site: routeSite, to: route });
  expect(answer.empty).toBeUndefined();
}, 20_000);

test(`A5 undecided service test answer preserves its evidence and fake-rule limit — Fails if: "${failsIf}"`, async () => {
  const answer = await runCli(service, "tests", [query(route)]);
  expectFocused(answer, "tests");
  expect(answer.tests).toMatchObject({ label: "static-call-path", count: 0, tests: [] });
  expect(answer.tests.undecided).toHaveLength(1);
  const undecided = answer.tests.undecided[0];
  expect(undecided).toMatchObject({
    ...loc(service, "dispatch.checks.ts", 'test("dispatches an incident ticket"'),
    name: "dispatches an incident ticket", throughFake: true,
  });
  expect(undecided.path).toHaveLength(2);
  undecided.path.forEach(expectLink);
  expect(undecided.path[1].to).toMatchObject(route);
  expect(answer.limits).toEqual(expect.arrayContaining([
    expect.objectContaining({ reason: "other", text: "fake rule not set (A3)" }),
  ]));
}, 20_000);

test(`A5 missing name returns a limited empty answer without a fallback map — Fails if: "${failsIf}"`, async () => {
  const answer = await runCli(service, "where", ["missingNebulaDispatch"]);
  expectFocused(answer, "matches");
  expect(answer.matches).toEqual([]);
  expect(answer.ambiguous).toBe(false);
  expect(answer.empty).toBe("none found by static analysis");
  expect(answer.limits).toEqual(expect.arrayContaining([expect.objectContaining({ reason: "not-found" })]));
}, 20_000);

test(`A5 ambiguous service-project name returns candidates without a map or guessed links — Fails if: "${failsIf}"`, async () => {
  const answer = await runCli(service, "callees", ["duplicatedDesk"]);
  expectFocused(answer, "matches");
  expect(answer.ambiguous).toBe(true);
  expect(answer.matches).toHaveLength(2);
  answer.matches.forEach(expectNode);
  expect(answer.matches).toEqual(expect.arrayContaining([
    expect.objectContaining(loc(service, "unrelated.ts", "export function duplicatedDesk")),
    expect.objectContaining(loc(service, "other-desk.ts", "export function duplicatedDesk")),
  ]));
}, 20_000);

test(`A5 callees without test classification keeps its stated limit — Fails if: "${failsIf}"`, async () => {
  const answer = await runCli(service, "callees", [query(dispatch)], [], []);
  expectFocused(answer, "links");
  expect(answer.links).toHaveLength(1);
  answer.links.forEach(expectLink);
  expect(atSite(answer.links, routeSite).resolution).toBe("ambiguous");
  expect(answer.limits).toEqual(expect.arrayContaining([
    expect.objectContaining({ reason: "other", text: "no test-file pattern given" }),
  ]));
}, 20_000);

test(`A5 direct-function question keeps only its call and source evidence — Fails if: "${failsIf}"`, async () => {
  const answer = await runCli(credit, "callees", ["paddedCredit"]);
  expectFocused(answer, "links");
  expect(answer.links).toHaveLength(1);
  const link = answer.links[0];
  expectLink(link);
  expect(link).toMatchObject({
    from: creditMiddle, site: loc(credit, "module/amount.ts", "return unitCredit(quantity)"),
    to: { ...creditLeaf, name: "unitCredit" }, kind: "call",
  });
}, 20_000);

test(`A5 map of a requested service module excludes unrelated repository definitions — Fails if: "${failsIf}"`, async () => {
  const answer = await runCli(service, "map", ["module"]);
  expectFocused(answer, "map");
  expect(answer.map.definitions).toEqual(expect.arrayContaining([
    expect.objectContaining(dispatch), expect.objectContaining(route),
  ]));
  for (const definition of answer.map.definitions) {
    expectNode(definition);
    expect(definition.file.startsWith("module/")).toBe(true);
  }
  expect(answer.map.links.length).toBeGreaterThan(0);
  for (const link of answer.map.links) {
    expectLink(link);
    expect(link.site.file.startsWith("module/")).toBe(true);
  }
  expect(answer.map.entries).toEqual(expect.arrayContaining([
    expect.objectContaining({ fn: expect.objectContaining(dispatch) }),
  ]));
  expect(answer.limits).toEqual(expect.arrayContaining([
    expect.objectContaining({ reason: "other", text: "no sibling rule given (A1)" }),
  ]));
}, 20_000);

test(`A5 map of one file excludes its external callers and warehouse — Fails if: "${failsIf}"`, async () => {
  const answer = await runCli(credit, "map", ["module/amount.ts"]);
  expectFocused(answer, "map");
  expect(answer.map.definitions).toHaveLength(2);
  expect(answer.map.definitions).toEqual(expect.arrayContaining([
    expect.objectContaining(creditLeaf), expect.objectContaining(creditMiddle),
  ]));
  for (const definition of answer.map.definitions) {
    expectNode(definition);
    expect(definition.file).toBe("module/amount.ts");
  }
  expect(answer.map.links).toHaveLength(1);
  expectLink(answer.map.links[0]);
  expect(answer.map.links[0]).toMatchObject({ from: creditMiddle, to: creditLeaf });
  expect(answer.map.entries).toHaveLength(1);
  expect(answer.map.entries[0].fn).toMatchObject(creditMiddle);
  expect(answer.limits).toEqual(expect.arrayContaining([
    expect.objectContaining({ reason: "other", text: "no sibling rule given (A1)" }),
  ]));
}, 20_000);
