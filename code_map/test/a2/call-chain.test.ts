import { expect, test } from "bun:test";
import { readFileSync } from "node:fs";
import { isAbsolute, resolve } from "node:path";

const packageDir = resolve(import.meta.dir, "../..");
const fixtureDir = resolve(import.meta.dir, "fixtures");
const missingPlace = "a known place is not found";
const ambiguousPlace = "an ambiguous match is treated as certain, or a candidate not built is not named";
const missingLink = "a known link within the depth is missing with no limit at its site naming why";
const contradictoryLink = "a shown link contradicts the code";
const missingEvidence = "a link lacks its kind or location";
const repeatedFunction = "a function reached twice is shown twice";

type Loc = { file: string; line: number };

// The expected graph is read from the fixture source, never from the tool's own analysis.
function loc(project: string, file: string, anchor: string): Loc {
  const lines = readFileSync(resolve(fixtureDir, project, file), "utf8").split("\n");
  const positions = lines.flatMap((line, index) => line.includes(anchor) ? [index + 1] : []);
  expect(positions, `unique fixture anchor: ${project}/${file}: ${anchor}`).toHaveLength(1);
  return { file, line: positions[0]! };
}

function query(at: Loc) { return `${at.file}:${at.line}`; }

async function runCli(project: string, args: string[]) {
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
    expect(answer.query).toEqual(args.slice(1).filter((value, index, values) =>
      !value.startsWith("--") && !values[index - 1]?.startsWith("--")));
    expect(Array.isArray(answer.limits)).toBe(true);
    return answer;
  } finally {
    clearTimeout(timer);
  }
}

function flatten(steps: any[]): any[] {
  expect(Array.isArray(steps)).toBe(true);
  return steps.flatMap(step => [step, ...flatten(step.children)]);
}

function stepsAt(steps: any[], site: Loc): any[] {
  return flatten(steps).filter(step => step.link.site.file === site.file && step.link.site.line === site.line);
}

function stepAt(steps: any[], site: Loc): any {
  const found = stepsAt(steps, site);
  expect(found, `one call link at ${query(site)}`).toHaveLength(1);
  return found[0];
}

function matchesLoc(value: any, at: Loc): boolean {
  return value?.file === at.file && value?.line === at.line;
}

function expectKnownStep(answer: any, direction: "up" | "down", site: Loc, expected: any) {
  const steps = flatten(answer.chain[direction]);
  const found = steps.filter(step => matchesLoc(step.link.site, site));
  expect(found.length, `no duplicated call link at ${query(site)}`).toBeLessThanOrEqual(1);
  const step = found[0];
  if (step?.link.resolution === "implementation") {
    expect(step).toMatchObject(expected);
    return step;
  }
  // A2 permits a limited link; the explanation must belong to this call site.
  const limits = [...answer.limits, ...steps.flatMap(item => item.stop
    ? [{ ...item.stop, at: item.stop.at ?? item.link.site }] : [])];
  expect(limits.some(limit => matchesLoc(limit.at, site) && !["depth", "seen"].includes(limit.reason) &&
    (typeof limit.text === "string" && limit.text.trim().length > 0 ||
      typeof step?.link.reason === "string" && step.link.reason.trim().length > 0)),
  `known call at ${query(site)} or a limit at its site naming why`).toBe(true);
  if (step) expect(step.level).toBe(expected.level);
  return undefined;
}

function expectMatches(answer: any, expected: Loc[]) {
  expect(Array.isArray(answer.matches)).toBe(true);
  const order = (left: Loc, right: Loc) => left.file.localeCompare(right.file) || left.line - right.line;
  expect(answer.matches.map((match: any) => ({ file: match.file, line: match.line })).sort(order))
    .toEqual([...expected].sort(order));
  for (const match of answer.matches) {
    expect(typeof match.name).toBe("string");
    expect(match.name.length).toBeGreaterThan(0);
  }
  expect(answer.empty).toBeUndefined();
}

const dispatch = loc("service-post", "workflow.ts", "export const dispatchParcel =");
const stamp = loc("service-post", "live.ts", "const stamp =");
const archive = loc("service-post", "live.ts", "const archive =");
const nestedBody = loc("service-post", "workflow.ts", "    function* () {");
const nestedStamp = loc("service-post", "workflow.ts", 'post.stamp("cobalt-inspection")');

test(`A2 exact service code locates its place — Fails if: "${missingPlace}"`, async () => {
  const answer = await runCli("service-post", ["find", "return yield* post.stamp(parcel);"]);
  expectMatches(answer, [dispatch]);
  expect(answer.ambiguous).toBe(false);
}, 20_000);

test(`A2 description over a comment locates its place — Fails if: "${missingPlace}"`, async () => {
  const answer = await runCli("service-post", ["find", "prepare cobalt parcel dispatch"]);
  expectMatches(answer, [dispatch]);
  expect(answer.ambiguous).toBe(false);
}, 20_000);

test(`A2 description over a string locates its place — Fails if: "${missingPlace}"`, async () => {
  const answer = await runCli("service-post", ["find", "amber parcel retention"]);
  expectMatches(answer, [loc("service-post", "workflow.ts", "export const rememberParcel =")]);
  expect(answer.ambiguous).toBe(false);
}, 20_000);

test(`A2 inline generator code locates the body holding the call — Fails if: "${missingPlace}"`, async () => {
  const answer = await runCli("service-post", ["find", 'post.stamp("cobalt-inspection")']);
  expectMatches(answer, [nestedBody]);
  expect(answer.ambiguous).toBe(false);
  const chain = await runCli("service-post", ["chain", query(answer.matches[0]), "--up", "0", "--down", "1"]);
  expect(stepAt(chain.chain.down, nestedStamp)).toMatchObject({ level: 1, link: { from: nestedBody, to: stamp } });
}, 20_000);

test(`A2 a line inside a service body is a known place — Fails if: "${missingPlace}"`, async () => {
  const site = loc("service-post", "workflow.ts", "post.stamp(parcel)");
  const answer = await runCli("service-post", ["chain", query(site), "--up", "0", "--down", "1"]);
  expect(answer.empty).toBeUndefined();
  expect(stepAt(answer.chain.down, site)).toMatchObject({ level: 1, link: { from: dispatch, to: stamp } });
}, 20_000);

const reconciliationPlaces = [
  loc("service-post", "east.ts", "export const reconcileParcel ="),
  loc("service-post", "west.ts", "export const reconcileParcel ="),
];

for (const [source, text] of [
  ["exact code", 'return "violet dispatch receipt";'],
  ["description", "reconcile violet parcel"],
] as const) {
  test(`A2 ambiguous ${source} lists every place — Fails if: "${ambiguousPlace}"`, async () => {
    const answer = await runCli("service-post", ["find", text]);
    expect(answer.ambiguous).toBe(true);
    expectMatches(answer, reconciliationPlaces);
  }, 20_000);
}

for (const command of ["where", "callers", "callees", "chain"] as const) {
  test(`A2 ambiguous name in ${command} lists every place — Fails if: "${ambiguousPlace}"`, async () => {
    const answer = await runCli("service-post", [command, "reconcileParcel"]);
    expect(answer.ambiguous).toBe(true);
    expectMatches(answer, reconciliationPlaces);
    expect(answer.chain).toBeUndefined();
    expect(answer.links).toBeUndefined();
  }, 20_000);
}

const warehouseBefore = ["dockOne", "dockTwo", "dockThree", "dockFour", "dockFive", "dockSix", "dockSeven", "dockEight"];
const warehouseAfter = ["shelfOne", "shelfTwo", "shelfThree", "shelfFour", "shelfFive", "shelfSix", "shelfSeven", "shelfEight"];
const center = loc("service-depth", "live.ts", "const dispatchCenter =");

function warehousePlace(name: string): Loc { return loc("service-depth", "live.ts", `const ${name} =`); }
function warehouseSite(name: string): Loc { return loc("service-depth", "live.ts", `warehouse.${name}()`); }

function expectWarehouseChain(answer: any, up: number, down: number) {
  expect(answer.chain).toBeDefined();
  for (const [direction, depth, names] of [["up", up, warehouseBefore], ["down", down, warehouseAfter]] as const) {
    const steps = flatten(answer.chain[direction]);
    expect(steps.length).toBeLessThanOrEqual(depth);
    for (const step of steps) {
      expect(step.level).toBeGreaterThan(0);
      expect(step.level).toBeLessThanOrEqual(depth);
    }
    for (let index = 0; index < depth; index++) {
      const current = names[index]!;
      const previous = index === 0 ? "dispatchCenter" : names[index - 1]!;
      const site = warehouseSite(direction === "up" ? previous : current);
      const step = expectKnownStep(answer, direction, site, {
        level: index + 1,
        link: {
          from: warehousePlace(direction === "up" ? current : previous),
          to: warehousePlace(direction === "up" ? previous : current),
          kind: "service-call", resolution: "implementation",
        },
      });
      if (step && index + 1 === depth) expect(step).toMatchObject({ children: [], stop: { reason: "depth" } });
    }
  }
}

test(`A2 defaults to six call links each way through services — Fails if: "${missingLink}"`, async () => {
  const answer = await runCli("service-depth", ["chain", query(center)]);
  expectWarehouseChain(answer, 6, 6);
}, 20_000);

test(`A2 honors independent caller and callee depths — Fails if: "${missingLink}"`, async () => {
  const answer = await runCli("service-depth", ["chain", query(center), "--up", "2", "--down", "3"]);
  expectWarehouseChain(answer, 2, 3);
}, 20_000);

for (const direction of ["up", "down"] as const) {
  test(`A2 setting only ${direction} preserves the other default — Fails if: "${missingLink}"`, async () => {
    const answer = await runCli("service-depth", ["chain", query(center), `--${direction}`, "1"]);
    expectWarehouseChain(answer, direction === "up" ? 1 : 6, direction === "down" ? 1 : 6);
  }, 20_000);
}

test(`A2 level zero excludes every call link — Fails if: "${missingLink}"`, async () => {
  const answer = await runCli("service-depth", ["chain", query(center), "--up", "0", "--down", "0"]);
  expect(answer.chain).toEqual({ up: [], down: [] });
  expect(answer.limits).toEqual(expect.arrayContaining([expect.objectContaining({ reason: "depth" })]));
}, 20_000);

for (const [name, flags, up, down] of [
  ["callers only", ["--up", "2", "--down", "0"], 2, 0],
  ["callees only", ["--up", "0", "--down", "2"], 0, 2],
] as const) {
  test(`A2 ${name} keeps the enabled direction — Fails if: "${missingLink}"`, async () => {
    const answer = await runCli("service-depth", ["chain", query(center), ...flags]);
    expectWarehouseChain(answer, up, down);
  }, 20_000);
}

for (const entry of ["launchDetourFirst", "launchShortcutFirst"]) {
  test(`A2 service shortest callee route from ${entry} preserves its tail — Fails if: "${missingLink}"`, async () => {
    const root = loc("service-routes", "live.ts", `const ${entry} =`);
    const answer = await runCli("service-routes", ["chain", query(root), "--up", "0", "--down", "3"]);
    expectKnownStep(answer, "down", loc("service-routes", "live.ts", "routing.recordDispatch()"),
      { level: 2, link: { to: loc("service-routes", "live.ts", "const recordDispatch =") } });
    expectKnownStep(answer, "down", loc("service-routes", "live.ts", "routing.sealDispatch()"),
      { level: 3, link: { to: loc("service-routes", "live.ts", "const sealDispatch =") } });
  }, 20_000);
}

test(`A2 service shortest caller route preserves its tail — Fails if: "${missingLink}"`, async () => {
  const root = loc("service-routes", "live.ts", "const receiveCenter =");
  const answer = await runCli("service-routes", ["chain", query(root), "--up", "3", "--down", "0"]);
  expectKnownStep(answer, "up", loc("service-routes", "live.ts", "routing.receiveShared()"),
    { level: 2, link: { from: loc("service-routes", "live.ts", "const receiveAudit =") } });
  expectKnownStep(answer, "up", loc("service-routes", "live.ts", "routing.receiveAudit()"),
    { level: 3, link: { from: loc("service-routes", "live.ts", "const receiveArchive =") } });
}, 20_000);

for (const direction of ["up", "down"] as const) {
  test(`A2 direct shortest ${direction} route preserves its tail — Fails if: "${missingLink}"`, async () => {
    const rootName = direction === "down" ? "beginInspection" : "receiveInspection";
    const root = loc("direct-graph", "logic.ts", `export function ${rootName}()`);
    const answer = await runCli("direct-graph", ["chain", query(root), "--up", direction === "up" ? "3" : "0",
      "--down", direction === "down" ? "3" : "0"]);
    const site = loc("direct-graph", "logic.ts", direction === "down" ? "return sealInspection()" : "return receiveRecord()");
    expectKnownStep(answer, direction, site, { level: 3 });
  }, 20_000);
}

test(`A2 entering an inline Effect body adds no callee level — Fails if: "${missingLink}"`, async () => {
  const root = loc("service-post", "workflow.ts", "export const inspectParcel =");
  const answer = await runCli("service-post", ["chain", query(root), "--up", "0", "--down", "1"]);
  expectKnownStep(answer, "down", nestedStamp, { level: 1, link: { from: nestedBody, to: stamp } });
}, 20_000);

test(`A2 leaving an inline Effect body adds no caller level — Fails if: "${missingLink}"`, async () => {
  const answer = await runCli("service-post", ["chain", query(stamp), "--up", "2", "--down", "0"]);
  expectKnownStep(answer, "up", nestedStamp, { level: 1, link: { from: nestedBody, to: stamp } });
  const doorCall = loc("service-post", "workflow.ts", "return inspectParcel()");
  expectKnownStep(answer, "up", doorCall, {
    level: 2, link: { from: loc("service-post", "workflow.ts", "export function inspectFromDoor()") },
  });
}, 20_000);

function expectLoc(at: any) {
  expect(at).toBeDefined();
  expect(typeof at.file).toBe("string");
  expect(at.file.length).toBeGreaterThan(0);
  expect(isAbsolute(at.file)).toBe(false);
  expect(Number.isInteger(at.line)).toBe(true);
  expect(at.line).toBeGreaterThan(0);
  if (at.endLine !== undefined) {
    expect(Number.isInteger(at.endLine)).toBe(true);
    expect(at.endLine).toBeGreaterThanOrEqual(at.line);
  }
}

function expectNode(node: any) {
  expectLoc(node);
  expect(typeof node.name).toBe("string");
  expect(node.name.length).toBeGreaterThan(0);
  expect(["function", "method", "arrow", "effect-fn", "property", "class", "variable", "interface-member", "other"])
    .toContain(node.kind);
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

test(`A2 service links in both directions give kind and locations — Fails if: "${missingEvidence}"`, async () => {
  const answer = await runCli("service-depth", ["chain", query(center), "--up", "2", "--down", "2"]);
  for (const direction of ["up", "down"]) {
    const steps = flatten(answer.chain[direction]);
    expect(steps.length).toBeGreaterThan(0);
    steps.forEach(step => expectLink(step.link));
  }
}, 20_000);

test(`A2 direct and constructor links give kind and locations — Fails if: "${missingEvidence}"`, async () => {
  for (const name of ["splitInspection", "createReceipt"]) {
    const root = loc("direct-graph", "logic.ts", `export function ${name}()`);
    const answer = await runCli("direct-graph", ["chain", query(root), "--up", "0", "--down", "3"]);
    const steps = flatten(answer.chain.down);
    expect(steps.length).toBeGreaterThan(0);
    steps.forEach(step => expectLink(step.link));
    expect(steps.some(step => step.link.kind === (name === "createReceipt" ? "new" : "call"))).toBe(true);
  }
}, 20_000);

function expectDynamicSite(answer: any, site: Loc) {
  const steps = flatten(answer.chain.down);
  const local = steps.filter(step => matchesLoc(step.link.site, site));
  const limits = [...answer.limits, ...steps.flatMap(step => step.stop
    ? [{ ...step.stop, at: step.stop.at ?? step.link.site }] : [])];
  const explained = limits.some(limit => matchesLoc(limit.at, site) && limit.reason === "dynamic" &&
    (typeof limit.text === "string" && limit.text.trim().length > 0 || local.some(step =>
      typeof step.link.reason === "string" && step.link.reason.trim().length > 0)));
  expect(explained, `dynamic limit at ${query(site)} naming why`).toBe(true);
  for (const step of local) {
    expect(step.link.resolution).toBe("unresolved");
    expect(step.link.to).toBeUndefined();
  }
}

test(`A2 a dynamic callback may stop with an explanation at its site — Fails if: "${missingLink}"`, async () => {
  const root = loc("service-post", "workflow.ts", "export const invokeParcel =");
  const answer = await runCli("service-post", ["chain", query(root), "--up", "0", "--down", "2"]);
  expectDynamicSite(answer, loc("service-post", "workflow.ts", "return callback()"));
}, 20_000);

test(`A2 every computed service call has its own dynamic limit — Fails if: "${missingLink}"`, async () => {
  const root = loc("service-post", "workflow.ts", "export const chooseParcel =");
  const answer = await runCli("service-post", ["chain", query(root), "--up", "0", "--down", "2"]);
  for (const anchor of ['post[key]("chosen"', "return post[key](19"]) {
    expectDynamicSite(answer, loc("service-post", "workflow.ts", anchor));
  }
}, 20_000);

const linkFailure = `${missingLink}, or ${contradictoryLink}`;

test(`A2 shown service links agree with source in both directions — Fails if: "${linkFailure}"`, async () => {
  const submit = loc("service-post", "workflow.ts", "export function submitParcel");
  const open = loc("service-post", "workflow.ts", "export function openDispatch");
  const expected = {
    up: [
      { level: 1, site: loc("service-post", "workflow.ts", "return dispatchParcel(parcel)"), from: submit, to: dispatch, kind: "call" },
      { level: 2, site: loc("service-post", "workflow.ts", "return submitParcel(parcel)"), from: open, to: submit, kind: "call" },
    ],
    down: [
      { level: 1, site: loc("service-post", "workflow.ts", "post.stamp(parcel)"), from: dispatch, to: stamp, kind: "service-call" },
      { level: 2, site: loc("service-post", "live.ts", "post.archive(parcel.length)"), from: stamp, to: archive, kind: "service-call" },
    ],
  };
  const answer = await runCli("service-post", ["chain", query(dispatch), "--up", "2", "--down", "2"]);
  for (const direction of ["up", "down"] as const) {
    for (const edge of expected[direction]) {
      const { level, ...link } = edge;
      expectKnownStep(answer, direction, edge.site, { level, link });
    }
    for (const step of flatten(answer.chain[direction])) {
      const edge = expected[direction].find(item => matchesLoc(step.link.site, item.site));
      expect(edge, `source-defined ${direction} call at ${query(step.link.site)}`).toBeDefined();
      expect(step.level).toBe(edge!.level);
      expect(step.link).toMatchObject({ from: edge!.from, site: edge!.site, kind: edge!.kind });
      if (step.link.resolution === "implementation") expect(step.link.to).toMatchObject(edge!.to);
    }
  }
}, 20_000);

test(`A2 a stored function reference is not a caller — Fails if: "${contradictoryLink}"`, async () => {
  const root = loc("direct-graph", "logic.ts", "export function combineInspection()");
  const answer = await runCli("direct-graph", ["chain", query(root), "--up", "1", "--down", "0"]);
  const expected = [
    loc("direct-graph", "logic.ts", "export function inspectLeft()"),
    loc("direct-graph", "logic.ts", "export function inspectRight()"),
    loc("direct-graph", "logic.ts", "export function repeatInspection()"),
  ];
  const steps = flatten(answer.chain.up);
  expect(steps).toHaveLength(4);
  for (const step of steps) {
    expect(step.level).toBe(1);
    expect(expected.some(at => matchesLoc(step.link.from, at))).toBe(true);
    expect(step.link.to).toMatchObject(root);
    expect(step.link.kind).toBe("call");
  }
  const reference = loc("direct-graph", "logic.ts", "return combineInspection;");
  expect(stepsAt(answer.chain.up, reference)).toEqual([]);
}, 20_000);

function expectReferences(steps: any[], direction: "up" | "down", root: Loc) {
  const all = flatten(steps);
  const expanded = new Map<string, Loc>([[query(root), root]]);
  const references: any[] = [];
  for (const step of all) {
    const target = direction === "up" ? step.link.from : step.link.to;
    if (!target) continue;
    if (step.stop?.reason === "seen") {
      expect(step.children).toEqual([]);
      expectLoc(step.stop.ref);
      references.push(step);
    } else {
      expect(expanded.has(query(target)), `function ${query(target)} expanded only once`).toBe(false);
      expanded.set(query(target), target);
    }
  }
  expect(references.length).toBeGreaterThan(0);
  for (const step of references) {
    const target = direction === "up" ? step.link.from : step.link.to;
    expect(step.stop.ref).toMatchObject({ file: target.file, line: target.line });
    expect(expanded.has(query(step.stop.ref)), `reference points to shown function ${query(step.stop.ref)}`).toBe(true);
  }
}

test(`A2 diamond callees show the shared function once with a reference back — Fails if: "${repeatedFunction}"`, async () => {
  const root = loc("direct-graph", "logic.ts", "export function splitInspection()");
  const shared = loc("direct-graph", "logic.ts", "export function combineInspection()");
  const answer = await runCli("direct-graph", ["chain", query(root), "--up", "0", "--down", "3"]);
  expectReferences(answer.chain.down, "down", root);
  const repeated = flatten(answer.chain.down).filter(step => matchesLoc(step.link.to, shared));
  expect(repeated).toHaveLength(2);
  expect(repeated.filter(step => step.stop?.reason === "seen")).toHaveLength(1);
  expect(stepsAt(answer.chain.down, loc("direct-graph", "logic.ts", "return finishInspection()"))).toHaveLength(1);
}, 20_000);

test(`A2 diamond callers show the shared caller once with a reference back — Fails if: "${repeatedFunction}"`, async () => {
  const root = loc("direct-graph", "logic.ts", "export function finishInspection()");
  const shared = loc("direct-graph", "logic.ts", "export function splitInspection()");
  const answer = await runCli("direct-graph", ["chain", query(root), "--up", "3", "--down", "0"]);
  expectReferences(answer.chain.up, "up", root);
  const repeated = flatten(answer.chain.up).filter(step => matchesLoc(step.link.from, shared));
  expect(repeated).toHaveLength(2);
  expect(repeated.filter(step => step.stop?.reason === "seen")).toHaveLength(1);
}, 20_000);

test(`A2 repeated call sites keep both links and one expansion — Fails if: "${repeatedFunction}"`, async () => {
  const root = loc("direct-graph", "logic.ts", "export function repeatInspection()");
  const shared = loc("direct-graph", "logic.ts", "export function combineInspection()");
  const answer = await runCli("direct-graph", ["chain", query(root), "--up", "0", "--down", "2"]);
  expectReferences(answer.chain.down, "down", root);
  expect(answer.chain.down).toHaveLength(2);
  expect(answer.chain.down.map((step: any) => query(step.link.site)).filter((site: string, index: number, sites: string[]) =>
    sites.indexOf(site) === index)).toHaveLength(2);
  answer.chain.down.forEach((step: any) => expect(step.link.to).toMatchObject(shared));
  expect(stepsAt(answer.chain.down, loc("direct-graph", "logic.ts", "return finishInspection()"))).toHaveLength(1);
}, 20_000);

for (const name of ["inspectSelf", "inspectCycle"]) {
  for (const direction of ["up", "down"] as const) {
    test(`A2 ${name} ${direction} returns a reference to level zero — Fails if: "${repeatedFunction}"`, async () => {
      const root = loc("direct-graph", "logic.ts", `export function ${name}()`);
      const answer = await runCli("direct-graph", ["chain", query(root), "--up", direction === "up" ? "6" : "0",
        "--down", direction === "down" ? "6" : "0"]);
      expectReferences(answer.chain[direction], direction, root);
      const references = flatten(answer.chain[direction]).filter(step => step.stop?.reason === "seen");
      expect(references).toHaveLength(1);
      expect(references[0].stop.ref).toMatchObject(root);
      expect(flatten(answer.chain[direction])).toHaveLength(name === "inspectSelf" ? 1 : 2);
    }, 20_000);
  }
}

test(`A2 repeated service target names where it was shown — Fails if: "${repeatedFunction}"`, async () => {
  const root = loc("service-routes", "live.ts", "const launchShortcutFirst =");
  const shared = loc("service-routes", "live.ts", "const sharedDispatch =");
  const answer = await runCli("service-routes", ["chain", query(root), "--up", "0", "--down", "4"]);
  expectReferences(answer.chain.down, "down", root);
  const repeated = flatten(answer.chain.down).filter(step => matchesLoc(step.link.to, shared));
  expect(repeated).toHaveLength(2);
  expect(repeated.filter(step => step.stop?.reason === "seen")).toHaveLength(1);
}, 20_000);
