import { expect, test } from "bun:test";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const packageDir = resolve(import.meta.dir, "../..");
const fixtureDir = resolve(import.meta.dir, "fixtures");
const missingLink = "an implementation the lookup finds has no link;";
const declarationAsProof = "a declaration is presented as proof of an implementation;";
const fakeAsReal = "a test fake is unlabelled or presented as the real implementation;";
const unmarkedTarget = "an unresolved or ambiguous target is unmarked.";
const live = "shorthand-permission";
const competing = "competing-capacity";
const fakeOnly = "fake-only-permission";
const parcel = "parcel-interface";

type Loc = { file: string; line: number };

// These anchors describe fixture source, independently of the tool's output.
// TypeScript's implementation lookup was checked on every fixture call before writing these expectations.
function loc(project: string, file: string, anchor: string, exact = false): Loc {
  const lines = readFileSync(resolve(fixtureDir, project, file), "utf8").split("\n");
  const matches = lines.flatMap((line, index) => (exact ? line === anchor : line.includes(anchor)) ? [index + 1] : []);
  expect(matches, `unique fixture anchor: ${project}/${file}: ${anchor}`).toHaveLength(1);
  return { file, line: matches[0]! };
}

function query(location: Loc) {
  return `${location.file}:${location.line}`;
}

async function runCli(project: string, args: string[], testPatterns = ["*.checks.ts"]) {
  const root = resolve(fixtureDir, project);
  const child = Bun.spawn([
    process.execPath, "src/cli.ts", ...args,
    "--project", resolve(root, "tsconfig.json"), "--root", root,
    ...testPatterns.flatMap(pattern => ["--tests", pattern]), "--json",
  ], { cwd: packageDir, stdout: "pipe", stderr: "pipe" });
  const timer = setTimeout(() => child.kill(), 15_000);
  try {
    const [exitCode, stdout, stderr] = await Promise.all([
      child.exited, new Response(child.stdout).text(), new Response(child.stderr).text(),
    ]);
    expect(exitCode, stderr || stdout).toBe(0);
    const answer = JSON.parse(stdout);
    expect(answer.command).toBe(args[0]);
    expect(Array.isArray(answer.query)).toBe(true);
    expect(Array.isArray(answer.limits)).toBe(true);
    expect(Array.isArray(answer.links)).toBe(true);
    expect(answer.empty).toBeUndefined();
    expect(answer.ambiguous).not.toBe(true);
    return answer;
  } finally {
    clearTimeout(timer);
  }
}

function linkAt(answer: any, site: Loc) {
  const links = answer.links.filter((link: any) => link.site.file === site.file && link.site.line === site.line);
  expect(links, `one link for call at ${query(site)}`).toHaveLength(1);
  return links[0];
}

function candidate(project: string, file: string, anchor: string, testFake: boolean) {
  return { ...loc(project, file, anchor), testFake };
}

function expectCandidates(link: any, expected: ReturnType<typeof candidate>[]) {
  const kinds = ["function", "method", "arrow", "effect-fn", "property", "class", "variable", "interface-member", "other"];
  for (const item of link.candidates) {
    expect(typeof item.name).toBe("string");
    expect(item.name.length).toBeGreaterThan(0);
    expect(kinds).toContain(item.kind);
  }
  const order = (a: Loc, b: Loc) => a.file.localeCompare(b.file) || a.line - b.line;
  expect(link.candidates.map((item: any) => ({ file: item.file, line: item.line, testFake: item.testFake })).sort(order))
    .toEqual([...expected].sort(order));
}

const liveAssert = loc(live, "live-layer.ts", 'const assert = Effect.fn("Permission.assert")');
const liveAsk = loc(live, "live-layer.ts", 'const ask = Effect.fn("Permission.ask")');
const draft = loc(live, "actions.ts", "export const approveDraft =");
const batch = loc(live, "actions.ts", "export const approveBatch =");
const assertDeclaration = loc(live, "contract.ts", "readonly assert:");
const assertSites = [
  loc(live, "actions.ts", "const allowed = yield* permission.assert"),
  loc(live, "actions.ts", 'yield* permission.assert({ resource: "draft/first"'),
  loc(live, "actions.ts", "  yield* permission", true),
];
const assertCandidates = [
  { ...liveAssert, testFake: false },
  candidate(live, "permission.checks.ts", "assert: () =>", true),
];
const reservation = loc(competing, "work.ts", "capacity.reserve(4)");
const reservationCaller = loc(competing, "work.ts", "export const scheduleJob =");
const reservationDeclaration = loc(competing, "contract.ts", "readonly reserve:");
const reservationCandidates = [
  candidate(competing, "layers.ts", 'const reserve = Effect.fn("Local.reserve")', false),
  candidate(competing, "layers.ts", 'const reserve = Effect.fn("Remote.reserve")', false),
  candidate(competing, "capacity.checks.ts", "reserve: () =>", true),
];

test(`R2 service callees include both shorthand members — Fails if: "${missingLink}"`, async () => {
  const answer = await runCli(live, ["callees", query(draft)]);
  const assert = linkAt(answer, assertSites[0]!);
  expectCandidates(assert, assertCandidates);
  expect(assert).toMatchObject({
    from: { ...draft, name: "approveDraft", kind: "effect-fn" },
    kind: "service-call", via: "implementation-lookup", resolution: "implementation",
    declaration: assertDeclaration, to: { ...liveAssert, name: "assert", kind: "effect-fn" },
  });
  const ask = linkAt(answer, loc(live, "actions.ts", 'permission.ask("publish draft?")'));
  expectCandidates(ask, [
    { ...liveAsk, testFake: false }, candidate(live, "permission.checks.ts", "ask: () =>", true),
  ]);
  expect(ask).toMatchObject({
    from: { ...draft, name: "approveDraft", kind: "effect-fn" },
    kind: "service-call", via: "implementation-lookup", resolution: "implementation",
    declaration: loc(live, "contract.ts", "readonly ask:"),
    to: { ...liveAsk, name: "ask", kind: "effect-fn" },
  });
}, 20_000);

test(`R2 callers list every assert call, including split-line access, without the layer shorthand — Fails if: "${missingLink}"`, async () => {
  const answer = await runCli(live, ["callers", query(liveAssert)]);
  expect(answer.links).toHaveLength(assertSites.length);
  for (const [index, site] of assertSites.entries()) {
    const link = linkAt(answer, site);
    expectCandidates(link, assertCandidates);
    expect(link).toMatchObject({
      kind: "service-call", via: "implementation-lookup", resolution: "implementation",
      declaration: assertDeclaration, to: { ...liveAssert, name: "assert", kind: "effect-fn" },
      from: index === 0
        ? { ...draft, name: "approveDraft", kind: "effect-fn" }
        : { ...batch, name: "approveBatch", kind: "effect-fn" },
    });
  }
}, 20_000);

test(`R2 split-line service callee resolves to the assert constant — Fails if: "${missingLink}"`, async () => {
  const answer = await runCli(live, ["callees", query(batch)]);
  for (const site of assertSites.slice(1)) {
    const link = linkAt(answer, site);
    expectCandidates(link, assertCandidates);
    expect(link).toMatchObject({
      from: { ...batch, name: "approveBatch", kind: "effect-fn" },
      kind: "service-call", via: "implementation-lookup", resolution: "implementation",
      to: { ...liveAssert, name: "assert", kind: "effect-fn" },
    });
  }
}, 20_000);

test(`R2 competing service layers retain every implementation — Fails if: "${missingLink}"`, async () => {
  const answer = await runCli(competing, ["callees", query(reservationCaller)]);
  expectCandidates(linkAt(answer, reservation), reservationCandidates);
}, 20_000);

test(`R2 interface lookup includes all typed implementations and excludes a same-name decoy — Fails if: "${missingLink}"`, async () => {
  const answer = await runCli(parcel, ["callees", "submitParcel"], ["*.records.ts"]);
  const link = linkAt(answer, loc(parcel, "submit.ts", 'port.dispatch("fragile")'));
  expectCandidates(link, [
    candidate(parcel, "adapters.ts", "dispatch(parcel: string): number {", false),
    candidate(parcel, "adapters.ts", "dispatch(shipment: string): number {", false),
    candidate(parcel, "simulation.records.ts", "dispatch(_parcel: string): number", true),
  ]);
}, 20_000);

test(`R2 implemented service keeps its declaration separate from its concrete target — Fails if: "${declarationAsProof}"`, async () => {
  const answer = await runCli(live, ["callees", query(draft)]);
  const link = linkAt(answer, assertSites[0]!);
  expect(link.declaration).toMatchObject(assertDeclaration);
  expect(link.resolution).toBe("implementation");
  expect(link.to).toMatchObject({ ...liveAssert, name: "assert", kind: "effect-fn" });
  expect(link.to.kind).not.toBe("interface-member");
  expectCandidates(link, assertCandidates);
}, 20_000);

test(`R2 bodyless readonly interface member is not an implementation — Fails if: "${declarationAsProof}"`, async () => {
  const answer = await runCli(parcel, ["callees", "collectReceipt"], ["*.records.ts"]);
  const link = linkAt(answer, loc(parcel, "submit.ts", 'port.receipt("ticket-42")'));
  expect(link.declaration).toMatchObject(loc(parcel, "port.ts", "readonly receipt:"));
  expect(link.resolution).toBe("unresolved");
  expect(link.to).toBeUndefined();
  expectCandidates(link, []);
  expect(typeof link.reason).toBe("string");
  expect(link.reason.trim().length).toBeGreaterThan(0);
}, 20_000);

test(`R2 ambient function declaration is not an implementation — Fails if: "${declarationAsProof}"`, async () => {
  const answer = await runCli(parcel, ["callees", "collectExternalReceipt"], ["*.records.ts"]);
  const link = linkAt(answer, loc(parcel, "submit.ts", 'externalReceipt("ticket-99")'));
  expect(link.declaration).toMatchObject(loc(parcel, "port.ts", "export declare function externalReceipt"));
  expect(link.resolution).toBe("unresolved");
  expect(link.to).toBeUndefined();
  expectCandidates(link, []);
  expect(typeof link.reason).toBe("string");
  expect(link.reason.trim().length).toBeGreaterThan(0);
}, 20_000);

test(`R2 fake is labelled with its file and leaves the live target certain — Fails if: "${fakeAsReal}"`, async () => {
  const answer = await runCli(live, ["callees", query(draft)]);
  const link = linkAt(answer, assertSites[0]!);
  expectCandidates(link, assertCandidates);
  expect(link.resolution).toBe("implementation");
  expect(link.to).toMatchObject(liveAssert);
  expect(link.to.file).not.toBe("permission.checks.ts");
}, 20_000);

test(`R2 fake-only service labels the fake and never chooses it — Fails if: "${fakeAsReal}"`, async () => {
  const answer = await runCli(fakeOnly, ["callees", "reconcileAccount"]);
  const link = linkAt(answer, loc(fakeOnly, "reconcile.ts", "permission.assert({ account })"));
  expectCandidates(link, [candidate(fakeOnly, "substitute.checks.ts", "assert: () =>", true)]);
  expect(link.declaration).toMatchObject(loc(fakeOnly, "contract.ts", "readonly assert:"));
  expect(link.resolution).toBe("unresolved");
  expect(link.to).toBeUndefined();
  expect(typeof link.reason).toBe("string");
  expect(link.reason.trim().length).toBeGreaterThan(0);
}, 20_000);

test(`R2 user-selected test pattern labels an interface fake — Fails if: "${fakeAsReal}"`, async () => {
  const answer = await runCli(parcel, ["callees", "submitParcel"], ["*.records.ts"]);
  const link = linkAt(answer, loc(parcel, "submit.ts", 'port.dispatch("fragile")'));
  const fake = candidate(parcel, "simulation.records.ts", "dispatch(_parcel: string): number", true);
  expect(link.candidates).toEqual(expect.arrayContaining([expect.objectContaining(fake)]));
  expect(link.resolution).toBe("ambiguous");
  expect(link.to).toBeUndefined();
}, 20_000);

test(`R2 multiple live service targets are marked ambiguous even with a fake — Fails if: "${unmarkedTarget}"`, async () => {
  const answer = await runCli(competing, ["callees", query(reservationCaller)]);
  const link = linkAt(answer, reservation);
  expect(link).toMatchObject({
    from: { ...reservationCaller, name: "scheduleJob", kind: "effect-fn" },
    kind: "service-call", via: "implementation-lookup", declaration: reservationDeclaration,
    resolution: "ambiguous",
  });
  expect(link.to).toBeUndefined();
  expectCandidates(link, reservationCandidates);
}, 20_000);

test(`R2 zero live service targets are marked unresolved even when a fake exists — Fails if: "${unmarkedTarget}"`, async () => {
  const answer = await runCli(fakeOnly, ["callees", "reconcileAccount"]);
  const link = linkAt(answer, loc(fakeOnly, "reconcile.ts", "permission.assert({ account })"));
  expect(link).toMatchObject({ kind: "service-call", via: "implementation-lookup", resolution: "unresolved" });
  expect(link.to).toBeUndefined();
  expectCandidates(link, [candidate(fakeOnly, "substitute.checks.ts", "assert: () =>", true)]);
  expect(typeof link.reason).toBe("string");
  expect(link.reason.trim().length).toBeGreaterThan(0);
}, 20_000);

test(`R2 no implementations marks the interface target unresolved with a reason — Fails if: "${unmarkedTarget}"`, async () => {
  const answer = await runCli(parcel, ["callees", "collectReceipt"], ["*.records.ts"]);
  const link = linkAt(answer, loc(parcel, "submit.ts", 'port.receipt("ticket-42")'));
  expect(link.resolution).toBe("unresolved");
  expect(link.to).toBeUndefined();
  expectCandidates(link, []);
  expect(typeof link.reason).toBe("string");
  expect(link.reason.trim().length).toBeGreaterThan(0);
}, 20_000);

test(`R2 without a test pattern both service implementations make the target ambiguous — Fails if: "${unmarkedTarget}"`, async () => {
  const answer = await runCli(live, ["callees", query(draft)], []);
  const link = linkAt(answer, assertSites[0]!);
  expectCandidates(link, assertCandidates.map(item => ({ ...item, testFake: false })));
  expect(link.resolution).toBe("ambiguous");
  expect(link.to).toBeUndefined();
  expect(answer.limits).toEqual(expect.arrayContaining([
    expect.objectContaining({ reason: "other", text: "no test-file pattern given" }),
  ]));
}, 20_000);
