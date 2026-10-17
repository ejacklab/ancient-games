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

// Shape: plugin objects `export const Plugin = { id, effect: Effect.fn(...)(function* (ctx) {...}) }`, each yielding
// services and registering its tool through `ctx.tool.transform((editor) => editor.add({...}))`.
// Seen on a real code base: the sibling table had members and 0 rows, with no limit saying why.
const project = "plugin-objects";
const members = ["plugins/edit.ts", "plugins/read.ts", "plugins/view.ts", "plugins/write.ts"];
const writers = ["plugins/edit.ts", "plugins/write.ts"];

function siblingsAnswer() {
  return runCli(project, "map", ["plugins"], ["--siblings", "plugins/*.ts"]);
}

function cellCovers(cell: any, member: string, anchor: string) {
  const expected = loc(project, member, anchor);
  return cell.member === member && cell.at?.file === member &&
    cell.at.line <= expected.line && (cell.at.endLine ?? cell.at.line) >= expected.line;
}

function rowsCovering(answer: any, status: string, anchors: Record<string, string>) {
  return answer.map.siblings.rows.filter((row: any) => row.status === status &&
    Object.entries(anchors).every(([member, anchor]) => row.cells.some((cell: any) => cellCovers(cell, member, anchor))));
}

function expectRowsLocated(table: any) {
  for (const row of table.rows) {
    expect(typeof row.concern).toBe("string");
    expect(row.concern.trim().length).toBeGreaterThan(0);
    expect(row.cells.length).toBeGreaterThan(0);
    for (const cell of row.cells) {
      expect(members).toContain(cell.member);
      expect(typeof cell.text).toBe("string");
      expectLocation(project, cell.at);
      expect(cell.at.file).toBe(cell.member);
    }
  }
}

function describeTable(answer: any) {
  const rows = answer.map?.siblings?.rows ?? [];
  return `rows: ${rows.map((row: any) => `${row.status}:${row.concern}`).join(" | ") || "none"}; limits: ${JSON.stringify(answer.limits)}`;
}

test("A1 real shape r3 map --siblings: plugin objects share FileAccess and ctx.tool.transform, vary in Permission, with locations", async () => {
  const answer = await siblingsAnswer();
  const table = answer.map?.siblings;
  expect(table, "a sibling table for --siblings").toBeDefined();
  expect(table.members.slice().sort()).toEqual(members);
  expect(table.rows.length, `the plugins' known concerns appear as rows; ${describeTable(answer)}`).toBeGreaterThan(0);
  expectRowsLocated(table);

  const sharedAccess = rowsCovering(answer, "shared",
    Object.fromEntries(members.map(member => [member, "const access = yield* FileAccess.Service"])));
  const sharedRegister = rowsCovering(answer, "shared",
    Object.fromEntries(members.map(member => [member, "yield* ctx.tool.transform((editor) => editor.add("])));
  expect(sharedAccess.length + sharedRegister.length,
    `a shared row citing each plugin's FileAccess or its ctx.tool.transform registration; ${describeTable(answer)}`).toBeGreaterThan(0);

  const permissionRows = rowsCovering(answer, "varies",
    Object.fromEntries(writers.map(member => [member, "const permission = yield* Permission.Service"])));
  expect(permissionRows.length, `a varies row citing the writers' Permission.Service; ${describeTable(answer)}`).toBeGreaterThan(0);
  // The readers never touch Permission: a cell placing it in a reader would contradict the code.
  for (const row of permissionRows) {
    for (const cell of row.cells) {
      if (!writers.includes(cell.member)) expect(cell.text, `${cell.member} does not use Permission`).not.toMatch(/Permission/);
    }
  }
}, 20_000);

test("A1 real shape r3 map --siblings: an empty plugin-object table carries a limit saying why the siblings were not compared", async () => {
  const answer = await siblingsAnswer();
  const table = answer.map?.siblings;
  expect(table, "a sibling table for --siblings").toBeDefined();
  expect(table.members.slice().sort()).toEqual(members);
  if (table.rows.length > 0) {
    expectRowsLocated(table);
    const permissionRows = rowsCovering(answer, "varies",
      Object.fromEntries(writers.map(member => [member, "const permission = yield* Permission.Service"])));
    const sharedRows = table.rows.filter((row: any) => row.status === "shared");
    expect(sharedRows.length + permissionRows.length, `rows exist but none is a known shared or varies concern; ${describeTable(answer)}`).toBeGreaterThan(0);
  } else {
    const said = answer.limits.map((limit: any) => typeof limit === "string" ? limit : JSON.stringify(limit));
    expect(said.some((text: string) => /sibling/i.test(text)),
      `no rows and no limit mentioning siblings; ${describeTable(answer)}`).toBe(true);
  }
}, 20_000);

// Same shape in a mixed group: the four plugins plus two members without the Plugin shape.
// Seen on a real code base: rows for 2 or 4 plugins, but 0 rows and no limit for the whole group of 15.
const mixedProject = "plugin-mixed";
const mixedMembers = ["plugins/defaults.ts", "plugins/edit.ts", "plugins/helpers.ts", "plugins/read.ts", "plugins/view.ts", "plugins/write.ts"];
const oddMembers = ["plugins/defaults.ts", "plugins/helpers.ts"];

function mixedRowsCovering(answer: any, status: string, anchors: Record<string, string>) {
  return answer.map.siblings.rows.filter((row: any) => row.status === status &&
    Object.entries(anchors).every(([member, anchor]) => {
      const expected = loc(mixedProject, member, anchor);
      return row.cells.some((cell: any) => cell.member === member && cell.at?.file === member &&
        cell.at.line <= expected.line && (cell.at.endLine ?? cell.at.line) >= expected.line);
    }));
}

test("A1 real shape r3 map --siblings: plugins mixed with non-plugin members still compare, the odd members marked unclear or limited", async () => {
  const answer = await runCli(mixedProject, "map", ["plugins"], ["--siblings", "plugins/*.ts"]);
  const table = answer.map?.siblings;
  expect(table, "a sibling table for --siblings").toBeDefined();
  expect(table.members.slice().sort()).toEqual(mixedMembers);
  expect(table.rows.length, `the plugins' known concerns appear as rows; ${describeTable(answer)}`).toBeGreaterThan(0);
  for (const row of table.rows) {
    expect(typeof row.concern).toBe("string");
    expect(row.concern.trim().length).toBeGreaterThan(0);
    for (const cell of row.cells) {
      expect(mixedMembers).toContain(cell.member);
      expectLocation(mixedProject, cell.at);
      expect(cell.at.file).toBe(cell.member);
    }
  }

  const sharedAccess = mixedRowsCovering(answer, "shared",
    Object.fromEntries(members.map(member => [member, "const access = yield* FileAccess.Service"])));
  expect(sharedAccess.length, `a shared row citing each plugin's FileAccess; ${describeTable(answer)}`).toBeGreaterThan(0);
  // The odd members never touch FileAccess: a cell placing it there would contradict the code.
  for (const row of sharedAccess) {
    for (const cell of row.cells) {
      if (oddMembers.includes(cell.member)) expect(cell.text, `${cell.member} does not use FileAccess`).not.toMatch(/FileAccess/);
    }
  }
  const permissionRows = mixedRowsCovering(answer, "varies",
    Object.fromEntries(writers.map(member => [member, "const permission = yield* Permission.Service"])));
  expect(permissionRows.length, `a varies row citing the writers' Permission.Service; ${describeTable(answer)}`).toBeGreaterThan(0);

  const limitText = answer.limits.map((limit: any) => typeof limit === "string" ? limit : JSON.stringify(limit));
  for (const odd of oddMembers) {
    const unclearCell = table.rows.some((row: any) => row.status === "unclear" && row.cells.some((cell: any) => cell.member === odd));
    const limited = limitText.some((text: string) => text.includes(odd));
    expect(unclearCell || limited, `${odd} appears as an unclear cell or in a limit; ${describeTable(answer)}`).toBe(true);
  }
}, 20_000);
