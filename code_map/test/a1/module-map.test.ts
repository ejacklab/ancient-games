import { expect, test } from "bun:test";
import { readFileSync } from "node:fs";
import { isAbsolute, resolve } from "node:path";

const packageDir = resolve(import.meta.dir, "../..");
const fixtureDir = resolve(import.meta.dir, "fixtures");
const siblingMembers = ["tools/chilled.ts", "tools/sealed.ts", "tools/stamped.ts"];
type Loc = { file: string; line: number; endLine?: number };

function source(project: string, file: string) {
  return readFileSync(resolve(fixtureDir, project, file), "utf8");
}

// The answer key comes from hand-chosen fixture lines, without the tool's parser.
function loc(project: string, file: string, anchor: string): Loc {
  const positions = source(project, file).split("\n")
    .flatMap((line, index) => line.includes(anchor) ? [index + 1] : []);
  expect(positions, `unique anchor: ${project}/${file}: ${anchor}`).toHaveLength(1);
  return { file, line: positions[0]! };
}

async function mapModule(project: string, paths = ["module"], siblings: string[] = []) {
  const root = resolve(fixtureDir, project);
  const child = Bun.spawn([
    process.execPath, "src/cli.ts", "map", ...paths,
    "--project", resolve(root, "tsconfig.json"), "--root", root,
    ...siblings.flatMap(pattern => ["--siblings", pattern]), "--json",
  ], { cwd: packageDir, stdout: "pipe", stderr: "pipe" });
  const timer = setTimeout(() => child.kill(), 15_000);
  try {
    const [exitCode, stdout, stderr] = await Promise.all([
      child.exited, new Response(child.stdout).text(), new Response(child.stderr).text(),
    ]);
    expect(exitCode, stderr || stdout).toBe(0);
    const answer = JSON.parse(stdout);
    expect(answer.command).toBe("map");
    expect(answer.query).toEqual(paths);
    expect(Array.isArray(answer.limits)).toBe(true);
    expect(Array.isArray(answer.map.definitions)).toBe(true);
    expect(Array.isArray(answer.map.links)).toBe(true);
    expect(Array.isArray(answer.map.entries)).toBe(true);
    return answer;
  } finally {
    clearTimeout(timer);
  }
}

function expectLoc(project: string, at: any) {
  expect(at).toBeDefined();
  expect(typeof at.file).toBe("string");
  expect(at.file.length).toBeGreaterThan(0);
  expect(isAbsolute(at.file)).toBe(false);
  const lines = source(project, at.file).split("\n");
  expect(Number.isInteger(at.line)).toBe(true);
  expect(at.line).toBeGreaterThan(0);
  expect(at.line).toBeLessThanOrEqual(lines.length);
  if (at.endLine !== undefined) {
    expect(Number.isInteger(at.endLine)).toBe(true);
    expect(at.endLine).toBeGreaterThanOrEqual(at.line);
    expect(at.endLine).toBeLessThanOrEqual(lines.length);
  }
}

function flattenSteps(steps: any[]): any[] {
  return steps.flatMap(step => [step, ...flattenSteps(step.children ?? [])]);
}

function expectMapLocations(project: string, answer: any) {
  for (const definition of answer.map.definitions) expectLoc(project, definition);
  for (const link of answer.map.links) {
    expectLoc(project, link.from);
    expectLoc(project, link.site);
    if (link.declaration !== undefined) expectLoc(project, link.declaration);
    if (link.resolution === "implementation") expectLoc(project, link.to);
    for (const candidate of link.candidates) expectLoc(project, candidate);
  }
  for (const entry of answer.map.entries) {
    expectLoc(project, entry.fn);
    for (const step of flattenSteps(entry.steps)) expectLoc(project, step.at);
  }
  if (answer.map.siblings) {
    for (const row of answer.map.siblings.rows) {
      expect(["shared", "varies", "unclear"]).toContain(row.status);
      for (const cell of row.cells) expectLoc(project, cell.at);
    }
  }
  for (const limit of answer.limits) {
    if (limit.at !== undefined) expectLoc(project, limit.at);
    if (limit.ref !== undefined) expectLoc(project, limit.ref);
  }
}

test('A1 service definitions, call evidence and entry decisions — "a claim lacks its location"', async () => {
  const answer = await mapModule("service-intake");
  expect(answer.map.definitions.length).toBeGreaterThan(0);
  expect(answer.map.links.length).toBeGreaterThan(0);
  expect(answer.map.entries.length).toBeGreaterThan(0);
  expect(flattenSteps(answer.map.entries[0].steps).length).toBeGreaterThan(0);
  expectMapLocations("service-intake", answer);
}, 20_000);

test('A1 class methods and nested loop, else and catch evidence — "a claim lacks its location"', async () => {
  const answer = await mapModule("manifest-flow");
  expect(answer.map.definitions.length).toBeGreaterThan(0);
  expect(answer.map.links.length).toBeGreaterThan(0);
  expect(answer.map.entries.length).toBeGreaterThan(0);
  const kinds = flattenSteps(answer.map.entries[0].steps).map(step => step.kind);
  expect(kinds).toEqual(expect.arrayContaining(["loop", "if", "else", "try", "catch", "return"]));
  expectMapLocations("manifest-flow", answer);
}, 20_000);

test('A1 sibling concern cells identify their source — "a claim lacks its location" or "a checked example misses a known item"', async () => {
  const answer = await mapModule("tool-siblings", ["tools"], ["tools/*.ts"]);
  expect(answer.map.siblings).toBeDefined();
  expect(answer.map.siblings.members.slice().sort()).toEqual(siblingMembers);
  const rows = answer.map.siblings.rows;
  // A stated inability to compare is allowed; a silently empty table is not.
  if (rows.length === 0) {
    expect(answer.limits.some((limit: any) =>
      typeof limit.text === "string" && limit.text.trim().length > 0 &&
      limit.text !== "no test-file pattern given",
    ), "empty sibling table needs an explanation").toBe(true);
  }
  expectMapLocations("tool-siblings", answer);
  for (const row of rows) {
    expect(row.cells.length).toBeGreaterThan(0);
    for (const cell of row.cells) {
      expect(siblingMembers).toContain(cell.member);
      expect(cell.at.file).toBe(cell.member);
    }
  }
}, 20_000);

function entryNamed(answer: any, name: string) {
  const entries = answer.map.entries.filter((entry: any) => entry.fn.name === name);
  expect(entries, `entry ${name}`).toHaveLength(1);
  return entries[0];
}

function expectStepText(project: string, steps: any[]) {
  let previousLine = 0;
  for (const step of steps) {
    expectLoc(project, step.at);
    expect(step.at.line, "steps follow source order").toBeGreaterThanOrEqual(previousLine);
    previousLine = step.at.line;
    expect(typeof step.text).toBe("string");
    expect(step.text.trim().length).toBeGreaterThan(0);
    const lines = source(project, step.at.file).split("\n");
    const evidence = lines.slice(step.at.line - 1, step.at.endLine ?? lines.length).join("\n");
    expect(evidence, `source text at ${step.at.file}:${step.at.line}`).toContain(step.text);
    if (step.children) expectStepText(project, step.children);
  }
}

test('A1 Effect entry selection respects exports and the requested module boundary — "contradicts the code"', async () => {
  const answer = await mapModule("service-intake");
  expect(answer.map.entries.map((entry: any) => entry.fn.name)).toEqual(["intakeCrate"]);
  expect(entryNamed(answer, "intakeCrate").fn)
    .toMatchObject(loc("service-intake", "module/intake.ts", "export const intakeCrate ="));
  // Once the consumer is inside the requested paths it no longer establishes an entry.
  const expanded = await mapModule("service-intake", ["module", "consumer.ts"]);
  expect(expanded.map.entries).toEqual([]);
}, 20_000);

test('A1 ordinary entry excludes an uncalled export and a private helper — "contradicts the code"', async () => {
  const answer = await mapModule("manifest-flow");
  expect(answer.map.entries.map((entry: any) => entry.fn.name)).toEqual(["compileManifest"]);
  expect(entryNamed(answer, "compileManifest").fn)
    .toMatchObject(loc("manifest-flow", "module/manifest.ts", "export function compileManifest"));
}, 20_000);

test('A1 Effect flow preserves source order and both decision branches — "contradicts the code"', async () => {
  const answer = await mapModule("service-intake");
  const entry = entryNamed(answer, "intakeCrate");
  expectStepText("service-intake", entry.steps);
  const expectedTopLines = [
    "const depot = yield* Depot.Service;", "const accepted = yield* depot.acceptCrate(label);",
    "if (!accepted)", "return yield* localReceipt(label);",
  ].map(anchor => loc("service-intake", "module/intake.ts", anchor).line);
  expect(entry.steps.map((step: any) => step.at.line)).toEqual(expectedTopLines);
  const decisions = flattenSteps(entry.steps);
  for (const [kind, anchor] of [
    ["if", "if (!accepted)"], ["else", "} else {"],
    ["return", 'return "rejected";'], ["yield*", "yield* depot.recordCrate(label);"],
  ]) {
    expect(decisions).toEqual(expect.arrayContaining([expect.objectContaining({
      kind, at: expect.objectContaining(loc("service-intake", "module/intake.ts", anchor!)),
    })]));
  }
}, 20_000);

test('A1 long and multiline step text is complete and cites the actual source — "contradicts the code"', async () => {
  const answer = await mapModule("manifest-flow");
  const entry = entryNamed(answer, "compileManifest");
  expectStepText("manifest-flow", entry.steps);
  const steps = flattenSteps(entry.steps);
  const at = loc("manifest-flow", "module/manifest.ts", "    logManifest(");
  const auditCalls = steps.filter(step => step.kind === "call" && step.at.file === at.file && step.at.line === at.line);
  expect(auditCalls.length).toBeGreaterThan(0);
  const lines = source("manifest-flow", "module/manifest.ts").split("\n");
  const completeCall = lines.slice(at.line - 1, at.line + 2).join("\n").trim();
  expect(auditCalls.some(step => step.text === completeCall || step.text === completeCall.slice(0, -1)),
    "full call, with or without its statement semicolon").toBe(true);
  for (const kind of ["loop", "if", "else", "try", "catch"]) {
    expect(steps.some(step => step.kind === kind)).toBe(true);
  }
}, 20_000);

test('A1 typed service call cites its real layer implementation and module-local caller — "contradicts the code"', async () => {
  const answer = await mapModule("service-intake");
  const site = loc("service-intake", "module/intake.ts", "const accepted = yield* depot.acceptCrate(label);");
  const links = answer.map.links.filter((link: any) => link.site.file === site.file && link.site.line === site.line);
  expect(links).toHaveLength(1);
  expect(links[0]).toMatchObject({
    kind: "service-call", via: "implementation-lookup", resolution: "implementation",
    from: { name: "intakeCrate", ...loc("service-intake", "module/intake.ts", "export const intakeCrate =") },
    declaration: loc("service-intake", "port.ts", "readonly acceptCrate:"),
    to: { name: "acceptCrate", ...loc("service-intake", "module/live.ts", "const acceptCrate =") },
  });
  // External consumers establish entries; the module's links are calls made inside it.
  for (const link of answer.map.links) expect(link.site.file.startsWith("module/")).toBe(true);
}, 20_000);

test('A1 definitions include Effect constants and both forms of layer service method — "a checked example misses a known item"', async () => {
  const answer = await mapModule("service-intake");
  for (const [file, name, kind, anchor] of [
    ["module/intake.ts", "intakeCrate", "effect-fn", "export const intakeCrate ="],
    ["module/intake.ts", "localReceipt", "effect-fn", "export const localReceipt ="],
    ["module/intake.ts", "unusedIntake", "effect-fn", "export const unusedIntake ="],
    ["module/live.ts", "depotLayer", "effect-fn", "export const depotLayer ="],
    ["module/live.ts", "acceptCrate", "effect-fn", "const acceptCrate ="],
    ["module/live.ts", "recordCrate", "method", "*recordCrate(label:"],
  ]) {
    expect(answer.map.definitions).toEqual(expect.arrayContaining([expect.objectContaining({
      name, kind, ...loc("service-intake", file!, anchor!),
    })]));
  }
  for (const definition of answer.map.definitions) expect(definition.file.startsWith("module/")).toBe(true);
}, 20_000);

test('A1 definitions include ordinary functions, a class and its method — "a checked example misses a known item"', async () => {
  const answer = await mapModule("manifest-flow");
  for (const [name, kind, anchor] of [
    ["ManifestBook", "class", "export class ManifestBook"],
    ["ManifestBook.record", "method", "  record(label:"],
    ["compileManifest", "function", "export function compileManifest"],
    ["exportedButUncalled", "function", "export function exportedButUncalled"],
    ["privateManifest", "function", "function privateManifest"],
  ]) {
    expect(answer.map.definitions).toEqual(expect.arrayContaining([expect.objectContaining({
      name, kind, ...loc("manifest-flow", "module/manifest.ts", anchor!),
    })]));
  }
}, 20_000);

test('A1 outgoing links include construction, a method call and calls outside the module — "a checked example misses a known item"', async () => {
  const answer = await mapModule("manifest-flow");
  for (const [anchor, kind, targetFile, targetAnchor] of [
    ["const book = new ManifestBook();", "new", "module/manifest.ts", "export class ManifestBook"],
    ["book.record(label);", "call", "module/manifest.ts", "  record(label:"],
    ["return normalizeManifest(label);", "call", "support.ts", "export function normalizeManifest"],
    ["    logManifest(", "call", "support.ts", "export function logManifest"],
  ]) {
    expect(answer.map.links).toEqual(expect.arrayContaining([expect.objectContaining({
      site: expect.objectContaining(loc("manifest-flow", "module/manifest.ts", anchor!)),
      kind, resolution: "implementation",
      to: expect.objectContaining(loc("manifest-flow", targetFile!, targetAnchor!)),
    })]));
  }
}, 20_000);

test('A1 inline Service.of method has an incoming service-call link in the module map — "a checked example misses a known item"', async () => {
  const answer = await mapModule("service-intake");
  expect(answer.map.links).toEqual(expect.arrayContaining([expect.objectContaining({
    kind: "service-call", resolution: "implementation",
    site: expect.objectContaining(loc("service-intake", "module/intake.ts", "yield* depot.recordCrate(label);")),
    declaration: expect.objectContaining(loc("service-intake", "port.ts", "readonly recordCrate:")),
    to: expect.objectContaining(loc("service-intake", "module/live.ts", "*recordCrate(label:")),
  })]));
}, 20_000);

function concernAt(answer: any, status: string, anchors: Record<string, string>) {
  const table = answer.map.siblings;
  expect(table).toBeDefined();
  expect(table.members.slice().sort()).toEqual(Object.keys(anchors).sort());
  expect(table.rows.length, "known sibling concerns must appear in the table").toBeGreaterThan(0);
  const rows = table.rows.filter((row: any) => row.status === status &&
    Object.entries(anchors).every(([member, anchor]) => {
      const expected = loc("tool-siblings", member, anchor);
      return row.cells.some((cell: any) => cell.member === member && cell.at.file === member &&
        cell.at.line <= expected.line && (cell.at.endLine ?? cell.at.line) >= expected.line);
    }));
  expect(rows.length, `${status} concern with evidence for each known step`).toBeGreaterThan(0);
  for (const row of rows) {
    expect(typeof row.concern).toBe("string");
    expect(row.concern.trim().length).toBeGreaterThan(0);
    for (const cell of row.cells) {
      expect(typeof cell.text).toBe("string");
      expect(cell.text.trim().length).toBeGreaterThan(0);
      expectLoc("tool-siblings", cell.at);
    }
  }
}

test('A1 Effect-constant siblings report their shared validation step — "a checked example misses a known item"', async () => {
  const answer = await mapModule("tool-siblings", ["tools"], ["tools/*.ts"]);
  concernAt(answer, "shared", Object.fromEntries(siblingMembers.map(member => [member, "const checked = validateParcel(parcel);"])));
}, 20_000);

test('A1 Effect-constant siblings report their differing preparation steps — "a checked example misses a known item"', async () => {
  const answer = await mapModule("tool-siblings", ["tools"], ["tools/*.ts"]);
  concernAt(answer, "varies", {
    "tools/chilled.ts": "const prepared = chillParcel(checked);",
    "tools/sealed.ts": "const prepared = sealParcel(checked);",
    "tools/stamped.ts": "const prepared = stampParcel(checked);",
  });
}, 20_000);

test('A1 omitting the sibling rule omits the table and states the A1 limit — "a checked example misses a known item"', async () => {
  const answer = await mapModule("tool-siblings", ["tools"]);
  expect(answer.map.siblings).toBeUndefined();
  expect(answer.limits).toEqual(expect.arrayContaining([expect.objectContaining({
    reason: "other", text: "no sibling rule given (A1)",
  })]));
  for (const member of siblingMembers) {
    expect(answer.map.definitions).toEqual(expect.arrayContaining([expect.objectContaining({
      name: "execute", kind: "effect-fn", ...loc("tool-siblings", member, "export const execute ="),
    })]));
  }
}, 20_000);

test('A1 the user glob selects the sibling members rather than every similar tool — "contradicts the code"', async () => {
  const answer = await mapModule("tool-siblings", ["tools"], ["tools/[cs]e*.ts"]);
  expect(answer.map.siblings).toBeDefined();
  expect(answer.map.siblings.members).toEqual(["tools/sealed.ts"]);
  expect(answer.map.definitions.filter((definition: any) => definition.name === "execute")).toHaveLength(3);
}, 20_000);
