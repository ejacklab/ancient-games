import { expect, test } from "bun:test";
import { readFileSync } from "node:fs";
import { isAbsolute, resolve } from "node:path";

const packageDir = resolve(import.meta.dir, "../..");
const fixtureDir = resolve(import.meta.dir, "fixtures");
type Loc = { file: string; line: number };

// Hand-chosen source anchors are the answer key; the tool's parser does not supply it.
function loc(project: string, file: string, anchor: string): Loc {
  const lines = readFileSync(resolve(fixtureDir, project, file), "utf8").split("\n");
  const positions = lines.flatMap((line, index) => line.includes(anchor) ? [index + 1] : []);
  expect(positions, `unique anchor: ${project}/${file}: ${anchor}`).toHaveLength(1);
  return { file, line: positions[0]! };
}

function query(at: Loc) { return `${at.file}:${at.line}`; }
function matchesLoc(actual: any, at: Loc) { return actual?.file === at.file && actual?.line === at.line; }

async function runCli(project: string, command: string, args: string[], extra: string[] = []) {
  const root = resolve(fixtureDir, project);
  const child = Bun.spawn([
    process.execPath, "src/cli.ts", command, ...args,
    "--project", resolve(root, "tsconfig.json"), "--root", root, ...extra, "--json",
  ], { cwd: packageDir, stdout: "pipe", stderr: "pipe" });
  const timer = setTimeout(() => child.kill(), 15_000);
  try {
    const [exitCode, stdout, stderr] = await Promise.all([
      child.exited, new Response(child.stdout).text(), new Response(child.stderr).text(),
    ]);
    expect(exitCode, stderr || stdout).toBe(0);
    const answer = JSON.parse(stdout);
    expect(answer.command).toBe(command);
    expect(answer.query).toEqual(args);
    expect(Array.isArray(answer.limits)).toBe(true);
    return answer;
  } finally {
    clearTimeout(timer);
  }
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

// Shape 1: `where Permission.assert` for an Effect service re-exported as a namespace.
const serviceProject = "service-namespace";
const unrelatedFiles = ["audit.ts", "sandbox.ts"];

test("A1 real shape r2-1 where: Permission.assert includes the layer's assert constant", async () => {
  const project = serviceProject;
  const layerAssert = loc(project, "permission.ts", "const assert = Effect.fn(\"Permission.assert\")");
  const answer = await runCli(project, "where", ["Permission.assert"]);
  expect(Array.isArray(answer.matches), "where answers with matches").toBe(true);
  for (const match of answer.matches) expectLocation(project, match);
  const listed = answer.matches.map((match: any) => query(match));
  expect(listed, "the written Permission.assert is among the matches").toContain(query(layerAssert));
}, 20_000);

test("A1 real shape r2-1 where: unrelated permission.assert property paths are never the answer alone", async () => {
  const project = serviceProject;
  const service = [
    loc(project, "permission.ts", "const assert = Effect.fn(\"Permission.assert\")"),
    loc(project, "permission.ts", "readonly assert:"),
  ].map(query);
  const answer = await runCli(project, "where", ["Permission.assert"]);
  expect(Array.isArray(answer.matches), "where answers with matches").toBe(true);
  const matches: any[] = answer.matches;
  const fromService = matches.filter(match => service.includes(query(match)));
  const fromUnrelated = matches.filter(match => unrelatedFiles.includes(match.file));
  expect(fromService.length, `matches: ${matches.map(query).join(", ") || "none"}`).toBeGreaterThan(0);
  // Listing an unrelated object is allowed only when the answer says it is ambiguous.
  if (fromUnrelated.length > 0) expect(answer.ambiguous, "unrelated matches make the answer ambiguous").toBe(true);
}, 20_000);

// Shape 2: plugin tools built by `Tool.make({ ..., execute: Effect.fn(...)(...) })`.
const toolsProject = "plugin-tools";
const toolMembers = ["tools/edit.ts", "tools/read.ts", "tools/view.ts", "tools/write.ts"];

function rowsCovering(project: string, answer: any, status: string, anchors: Record<string, string>) {
  return answer.map.siblings.rows.filter((row: any) => row.status === status &&
    Object.entries(anchors).every(([member, anchor]) => {
      const expected = loc(project, member, anchor);
      return row.cells.some((cell: any) => cell.member === member && cell.at?.file === member &&
        cell.at.line <= expected.line && (cell.at.endLine ?? cell.at.line) >= expected.line);
    }));
}

function expectSiblingTable(project: string, answer: any) {
  const table = answer.map?.siblings;
  expect(table, "a sibling table for --siblings").toBeDefined();
  expect(table.members.slice().sort()).toEqual(toolMembers);
  expect(table.rows.length, "the tools' known concerns appear as rows").toBeGreaterThan(0);
  for (const row of table.rows) {
    expect(typeof row.concern).toBe("string");
    expect(row.concern.trim().length).toBeGreaterThan(0);
    expect(row.cells.length).toBeGreaterThan(0);
    for (const cell of row.cells) {
      expect(toolMembers).toContain(cell.member);
      expect(typeof cell.text).toBe("string");
      expectLocation(project, cell.at);
      expect(cell.at.file).toBe(cell.member);
    }
  }
}

test("A1 real shape r2-2 map --siblings: Tool.make tools share their permission check, with locations", async () => {
  const project = toolsProject;
  const answer = await runCli(project, "map", ["tools"], ["--siblings", "tools/*.ts"]);
  expectSiblingTable(project, answer);
  const anchors = Object.fromEntries(toolMembers.map(member => [member, "const allowed = yield* checkPermission(input.path);"]));
  expect(rowsCovering(project, answer, "shared", anchors).length,
    "a shared row whose cells cite each tool's permission check").toBeGreaterThan(0);
}, 20_000);

test("A1 real shape r2-2 map --siblings: Tool.make tools vary in reading against writing, with locations", async () => {
  const project = toolsProject;
  const answer = await runCli(project, "map", ["tools"], ["--siblings", "tools/*.ts"]);
  expectSiblingTable(project, answer);
  const anchors = {
    "tools/read.ts": "const content = yield* readFile(input.path);",
    "tools/view.ts": "const shown = yield* readFile(",
    "tools/write.ts": "const written = yield* writeFile(input.path, input.content);",
    "tools/edit.ts": "const edited = yield* writeFile(input.path, input.replacement);",
  };
  expect(rowsCovering(project, answer, "varies", anchors).length,
    "a varies row whose cells cite each tool's read or write").toBeGreaterThan(0);
}, 20_000);

// Shape 3: Transport implementations are objects returned from factories in different files.
for (const command of ["map", "callees"]) {
  test(`A1 real shape r2-3 ${command}: transport.prepare lists every factory-built prepare, marked ambiguous`, async () => {
    const project = "transport-factories";
    const caller = loc(project, "send.ts", "export function send(");
    const site = loc(project, "send.ts", "return transport.prepare(payload);");
    const implementations = [
      loc(project, "http.ts", "prepare: (payload) => `POST"),
      loc(project, "queue.ts", "prepare(payload) { return `ENQUEUE"),
      loc(project, "file.ts", "prepare: (payload) => `${directory}"),
    ];
    const answer = await runCli(project, command, [command === "map" ? "send.ts" : query(caller)]);
    const links = command === "map" ? answer.map?.links : answer.links;
    expect(Array.isArray(links)).toBe(true);
    const found = links.filter((link: any) => matchesLoc(link.site, site));
    expect(found, `one call link at ${query(site)}`).toHaveLength(1);
    const link = found[0];
    expectLocation(project, link.from);
    expectLocation(project, link.site);
    for (const candidate of link.candidates) expectLocation(project, candidate);
    const listed = link.candidates.filter((candidate: any) => !candidate.testFake).map(query);
    expect(listed, "every factory's prepare is a candidate").toEqual(expect.arrayContaining(implementations.map(query)));
    (expect as any)(link.resolution, link.reason ?? "").toBe("ambiguous");
    expect(link.to).toBeUndefined();
  }, 20_000);
}
