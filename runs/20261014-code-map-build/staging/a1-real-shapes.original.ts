import { afterAll, beforeAll, expect, test } from "bun:test";
import { mkdirSync, readFileSync, rmSync, symlinkSync } from "node:fs";
import { dirname, isAbsolute, resolve } from "node:path";

const packageDir = resolve(import.meta.dir, "../..");
const fixtureDir = resolve(import.meta.dir, "fixtures");
type Loc = { file: string; line: number };

// Hand-chosen source anchors are the answer key; the map's parser does not supply it.
function loc(project: string, file: string, anchor: string): Loc {
  const lines = readFileSync(resolve(fixtureDir, project, file), "utf8").split("\n");
  const positions = lines.flatMap((line, index) => line.includes(anchor) ? [index + 1] : []);
  expect(positions, `unique anchor: ${project}/${file}: ${anchor}`).toHaveLength(1);
  return { file, line: positions[0]! };
}

function query(at: Loc) { return `${at.file}:${at.line}`; }
function matchesLoc(actual: any, at: Loc) { return actual?.file === at.file && actual?.line === at.line; }

async function runCli(project: string, command: string, paths: string[]) {
  const root = resolve(fixtureDir, project);
  const child = Bun.spawn([
    process.execPath, "src/cli.ts", command, ...paths,
    "--project", resolve(root, "tsconfig.json"), "--root", root, "--json",
  ], { cwd: packageDir, stdout: "pipe", stderr: "pipe" });
  const timer = setTimeout(() => child.kill(), 15_000);
  try {
    const [exitCode, stdout, stderr] = await Promise.all([
      child.exited, new Response(child.stdout).text(), new Response(child.stderr).text(),
    ]);
    expect(exitCode, stderr || stdout).toBe(0);
    const answer = JSON.parse(stdout);
    expect(answer.command).toBe(command);
    expect(answer.query).toEqual(paths);
    expect(Array.isArray(answer.limits)).toBe(true);
    expect(Array.isArray(command === "map" ? answer.map?.links : answer.links)).toBe(true);
    return answer;
  } finally {
    clearTimeout(timer);
  }
}

function linkAt(answer: any, site: Loc) {
  const links = answer.command === "map" ? answer.map.links : answer.links;
  const found = links.filter((link: any) => matchesLoc(link.site, site));
  expect(found, `one call link at ${query(site)}`).toHaveLength(1);
  return found[0];
}

function expectLocation(project: string, at: any) {
  expect(at).toBeDefined();
  expect(typeof at.file).toBe("string");
  expect(isAbsolute(at.file)).toBe(false);
  const lines = readFileSync(resolve(fixtureDir, project, at.file), "utf8").split("\n");
  expect(Number.isInteger(at.line)).toBe(true);
  expect(at.line).toBeGreaterThan(0);
  expect(at.line).toBeLessThanOrEqual(lines.length);
  if (at.endLine !== undefined) {
    expect(at.endLine).toBeGreaterThanOrEqual(at.line);
    expect(at.endLine).toBeLessThanOrEqual(lines.length);
  }
}

function expectLinkLocations(project: string, link: any) {
  expectLocation(project, link.from);
  expectLocation(project, link.site);
  if (link.declaration) expectLocation(project, link.declaration);
  if (link.to) expectLocation(project, link.to);
  expect(Array.isArray(link.candidates)).toBe(true);
  for (const candidate of link.candidates) expectLocation(project, candidate);
}

function expectInsideRepository(answer: any, site: Loc, link: any) {
  expect(link.reason ?? "", `local call at ${query(site)}`).not.toMatch(/outside (?:the )?repository/i);
  expect(answer.limits.filter((limit: any) => matchesLoc(limit.at, site) && limit.reason === "outside-repo"),
    `local call limit at ${query(site)}`).toEqual([]);
}

for (const command of ["map", "callees"]) {
  test(`A1 real shape 1 ${command}: inherited constructor reaches LocalError`, async () => {
    const project = "local-constructor";
    const caller = loc(project, "errors.ts", "export function rejectParcel");
    const site = loc(project, "errors.ts", "return new LocalError(label);");
    const target = loc(project, "errors.ts", "export class LocalError extends Base");
    const answer = await runCli(project, command, [command === "map" ? "errors.ts" : query(caller)]);
    const link = linkAt(answer, site);
    expectLinkLocations(project, link);
    expectInsideRepository(answer, site, link);
    expect(link).toMatchObject({ kind: "new", resolution: "implementation", to: target });
  }, 20_000);
}

function expectImplementation(link: any, target: Loc) {
  expect(link.resolution, link.reason ?? "").toBe("implementation");
  expect({ file: link.to?.file, line: link.to?.line }).toEqual(target);
}

for (const command of ["map", "callees"]) {
  test(`A1 real shape 2 ${command}: steps.attempt on a factory value taken with yield* is not outside the repository`, async () => {
    const project = "factory-steps";
    const caller = loc(project, "runner.ts", "export const runStep");
    const site = loc(project, "runner.ts", "return yield* steps.attempt(label);");
    const start = loc(project, "steps.ts", "const attempt = Effect.fn(\"Steps.attempt\")");
    const end = loc(project, "steps.ts", "}); // end of attempt");
    const answer = await runCli(project, command, [command === "map" ? "runner.ts" : query(caller)]);
    const link = linkAt(answer, site);
    expectLinkLocations(project, link);
    expectInsideRepository(answer, site, link);
    // Either the link reaches the written attempt, or it stays unresolved with a limit that is not "outside".
    if (link.resolution === "implementation") {
      expect(link.to.file).toBe("steps.ts");
      expect(link.to.line).toBeGreaterThanOrEqual(start.line);
      expect(link.to.line).toBeLessThanOrEqual(end.line);
    } else {
      expect(link.resolution).toBe("unresolved");
      expect(typeof link.reason).toBe("string");
      expect(answer.limits.some((limit: any) => matchesLoc(limit.at, site))).toBe(true);
    }
  }, 20_000);
}

for (const command of ["map", "callees"]) {
  test(`A1 real shape 3 ${command}: overloaded Auth.header through a namespace import reaches its implementation`, async () => {
    const project = "overloaded-auth";
    const target = loc(project, "auth.ts", "export function header(first: string, second?: string)");
    const callers = [
      { fn: loc(project, "client.ts", "export function authorize("), site: loc(project, "client.ts", "return Auth.header(token);") },
      { fn: loc(project, "client.ts", "export function authorizeUser("), site: loc(project, "client.ts", "return Auth.header(user, secret);") },
    ];
    for (const { fn, site } of callers) {
      const answer = await runCli(project, command, [command === "map" ? "client.ts" : query(fn)]);
      const link = linkAt(answer, site);
      expectLinkLocations(project, link);
      expect(link.reason ?? "", `overloaded call at ${query(site)}`).not.toMatch(/no implementation/i);
      expectImplementation(link, target);
    }
  }, 30_000);
}

test("A1 real shape 3 callers: the implementation of an overloaded function lists both namespace calls", async () => {
  const project = "overloaded-auth";
  const target = loc(project, "auth.ts", "export function header(first: string, second?: string)");
  const sites = [loc(project, "client.ts", "return Auth.header(token);"), loc(project, "client.ts", "return Auth.header(user, secret);")];
  const answer = await runCli(project, "callers", [query(target)]);
  for (const site of sites) {
    const link = linkAt(answer, site);
    expectLinkLocations(project, link);
    expectImplementation(link, target);
  }
}, 20_000);

for (const command of ["map", "callees"]) {
  test(`A1 real shape 4 ${command}: transport.prepare lists every Transport implementation, marked ambiguous`, async () => {
    const project = "transport-ring";
    const caller = loc(project, "send.ts", "export function send(");
    const site = loc(project, "send.ts", "return transport.prepare(payload);");
    const implementations = [
      loc(project, "transports.ts", "prepare(payload) { return `POST"),
      loc(project, "transports.ts", "prepare(payload: string) { return `ENQUEUE"),
      loc(project, "transports.ts", "prepare(payload) { return `${directory}"),
    ];
    const answer = await runCli(project, command, [command === "map" ? "send.ts" : query(caller)]);
    const link = linkAt(answer, site);
    expectLinkLocations(project, link);
    expect(link.resolution).toBe("ambiguous");
    expect(link.to).toBeUndefined();
    const listed = link.candidates.filter((candidate: any) => !candidate.testFake)
      .map((candidate: any) => query(candidate)).sort();
    expect(listed).toEqual(implementations.map(query).sort());
  }, 20_000);
}

const workspaceLink = resolve(fixtureDir, "workspace-link/packages/app/node_modules/@fixture/core");

beforeAll(() => {
  // The workspace link is made here, as a package manager would, so the fixture holds no symlink of its own.
  rmSync(resolve(fixtureDir, "workspace-link/packages/app/node_modules"), { recursive: true, force: true });
  mkdirSync(dirname(workspaceLink), { recursive: true });
  symlinkSync("../../../core", workspaceLink, "dir");
});

afterAll(() => {
  rmSync(resolve(fixtureDir, "workspace-link/packages/app/node_modules"), { recursive: true, force: true });
});

for (const command of ["map", "callees"]) {
  test(`A1 real shape 5 ${command}: calls into a linked workspace package are not outside the repository`, async () => {
    const project = "workspace-link";
    const caller = loc(project, "packages/app/src/billing.ts", "export function bill(");
    const opened = loc(project, "packages/app/src/billing.ts", "const ledger = openLedger();");
    const recorded = loc(project, "packages/app/src/billing.ts", "return ledger.record(");
    const answer = await runCli(project, command, [command === "map" ? "packages/app/src" : query(caller)]);
    const expected = [
      { site: opened, target: loc(project, "packages/core/src/index.ts", "export function openLedger") },
      { site: recorded, target: loc(project, "packages/core/src/index.ts", "record(entry: string) {") },
    ];
    for (const { site, target } of expected) {
      const link = linkAt(answer, site);
      expectLinkLocations(project, link);
      expectInsideRepository(answer, site, link);
      expectImplementation(link, target);
    }
  }, 20_000);
}

test("A1 real shape 6 map: map src/a lists the src/b callers or names the scope it did not search", async () => {
  const project = "scope-edges";
  const target = loc(project, "src/a/store.ts", "export function saveRecord");
  const site = loc(project, "src/b/job.ts", "return saveRecord(\"nightly\");");
  const answer = await runCli(project, "map", ["src/a"]);
  const listed = answer.map.links.some((link: any) => matchesLoc(link.site, site) && matchesLoc(link.to, target));
  const scopeNamed = answer.limits.some((limit: any) =>
    typeof limit.text === "string" && /src\/a|src\/b/.test(limit.text));
  expect({ callerListed: listed, scopeLimitNamed: scopeNamed, limits: answer.limits },
    "the src/b caller of saveRecord, or a limit naming the scope").toMatchObject(
    listed ? { callerListed: true } : { scopeLimitNamed: true });
}, 20_000);

test("A1 real shape 6 callers: callers of a src/a function finds the src/b call", async () => {
  const project = "scope-edges";
  const target = loc(project, "src/a/store.ts", "export function saveRecord");
  const site = loc(project, "src/b/job.ts", "return saveRecord(\"nightly\");");
  const answer = await runCli(project, "callers", [query(target)]);
  const link = linkAt(answer, site);
  expectLinkLocations(project, link);
  expectImplementation(link, target);
}, 20_000);
