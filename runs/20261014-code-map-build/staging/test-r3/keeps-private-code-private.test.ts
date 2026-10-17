import { expect, test } from "bun:test";
import { createHash } from "node:crypto";
import { cpSync, lstatSync, mkdtempSync, mkdirSync, readFileSync, readdirSync, readlinkSync, rmSync, writeFileSync } from "node:fs";
import { isAbsolute, resolve } from "node:path";
import ts from "typescript";

const packageDir = resolve(import.meta.dir, "../..");
const fixtureDir = resolve(import.meta.dir, "fixtures/private-ledger");
const observer = resolve(import.meta.dir, "fixtures/observe-effects.ts");
const failsIf = "protected content leaves the machine or enters git.";
const auditPrefix = "R3_EFFECT ";
const token = "sk-live-R3-private-ledger-DO-NOT-EXPORT-73e2a9";
type Effect = { kind: string; api: string; target?: unknown };
type Workspace = { directory: string; root: string; cwd: string; out: string };
type CommandCase = { command: string; query: string[]; options?: string[] };

function fixtureLine(anchor: string) {
  const lines = readFileSync(resolve(fixtureDir, "module/ledger.ts"), "utf8").split("\n");
  const found = lines.flatMap((line, index) => line.includes(anchor) ? [index + 1] : []);
  expect(found, `unique fixture anchor: ${anchor}`).toHaveLength(1);
  return found[0]!;
}
const total = { file: "module/ledger.ts", line: fixtureLine("export function privateTotal"), name: "privateTotal" };
const base = { file: "module/ledger.ts", line: fixtureLine("export function baseAmount"), name: "baseAmount" };

function createWorkspace(command: string): Workspace {
  const directory = mkdtempSync(resolve(import.meta.dir, `fixtures/.r3-${command}-`));
  const root = resolve(directory, "private-target");
  const cwd = resolve(directory, "working");
  cpSync(fixtureDir, root, { recursive: true });
  mkdirSync(resolve(cwd, ".existing"), { recursive: true });
  mkdirSync(resolve(directory, "exports"));
  writeFileSync(resolve(cwd, ".existing/notes.txt"), token);
  return { directory, root, cwd, out: resolve(directory, "exports/answer.json") };
}

// Include hidden files, metadata-only changes, and changed content of the same length.
// Do not follow symlinks into unrelated trees.
function snapshotFiles(roots: string[]) {
  const files: Record<string, unknown> = {};
  function visit(path: string) {
    const stat = lstatSync(path, { bigint: true });
    if (stat.isDirectory()) {
      for (const name of readdirSync(path).sort()) visit(resolve(path, name));
      return;
    }
    files[path] = {
      size: String(stat.size), mtimeNs: String(stat.mtimeNs), ctimeNs: String(stat.ctimeNs), mode: String(stat.mode),
      content: stat.isFile() ? createHash("sha256").update(readFileSync(path)).digest("hex")
        : stat.isSymbolicLink() ? readlinkSync(path) : "special",
    };
  }
  for (const root of roots) visit(root);
  return files;
}

function expectOfflineSource() {
  const violations: string[] = [];
  const forbiddenModules = new Set(["net", "http", "https", "dgram", "tls", "dns", "fetch", "WebSocket"]);
  function scan(directory: string) {
    for (const entry of readdirSync(directory, { withFileTypes: true })) {
      const path = resolve(directory, entry.name);
      if (entry.isDirectory()) { scan(path); continue; }
      if (!/\.[cm]?[jt]sx?$/.test(entry.name)) continue;
      const source = ts.createSourceFile(path, readFileSync(path, "utf8"), ts.ScriptTarget.Latest, true);
      function report(node: ts.Node, text: string) {
        violations.push(`${path}:${source.getLineAndCharacterOfPosition(node.getStart(source)).line + 1}: ${text}`);
      }
      function moduleName(node: ts.Node, name: ts.Expression | undefined) {
        if (!name || !ts.isStringLiteralLike(name)) return;
        const module = name.text.replace(/^node:/, "").split("/")[0]!;
        if (forbiddenModules.has(module) || /^https?:/.test(name.text)) report(node, name.text);
      }
      function visit(node: ts.Node) {
        if (ts.isImportDeclaration(node) || ts.isExportDeclaration(node)) moduleName(node, node.moduleSpecifier);
        if (ts.isImportEqualsDeclaration(node) && ts.isExternalModuleReference(node.moduleReference)) {
          moduleName(node, node.moduleReference.expression);
        }
        if (ts.isCallExpression(node) && (node.expression.kind === ts.SyntaxKind.ImportKeyword ||
            ts.isIdentifier(node.expression) && node.expression.text === "require")) moduleName(node, node.arguments[0]);
        if (ts.isIdentifier(node) && ["fetch", "WebSocket"].includes(node.text)) report(node, node.text);
        if (ts.isElementAccessExpression(node) && node.argumentExpression &&
            ts.isStringLiteralLike(node.argumentExpression) && ["fetch", "WebSocket"].includes(node.argumentExpression.text)) {
          report(node, node.argumentExpression.text);
        }
        ts.forEachChild(node, visit);
      }
      visit(source);
    }
  }
  scan(resolve(packageDir, "src"));
  expect(violations, "network imports and fetch/WebSocket use in src").toEqual([]);
}

async function capture(command: string[], cwd: string) {
  const child = Bun.spawn(command, { cwd, stdin: "ignore", stdout: "pipe", stderr: "pipe" });
  const timer = setTimeout(() => child.kill(), 15_000);
  try {
    const [exitCode, stdout, stderr] = await Promise.all([
      child.exited, new Response(child.stdout).text(), new Response(child.stderr).text(),
    ]);
    const effects: Effect[] = stderr.split("\n").filter(line => line.startsWith(auditPrefix))
      .map(line => JSON.parse(line.slice(auditPrefix.length)));
    return { exitCode, stdout, stderr, effects };
  } finally {
    clearTimeout(timer);
  }
}

async function runCli(workspace: Workspace, entry: CommandCase, mode: "stdout" | "isolated" | "out" = "stdout") {
  const args = [
    process.execPath, "--preload", observer, resolve(packageDir, "src/cli.ts"), entry.command, ...entry.query,
    ...entry.options ?? [], "--project", resolve(workspace.root, "tsconfig.json"), "--root", workspace.root,
    "--tests", "*.checks.ts", "--json", ...mode === "out" ? ["--out", workspace.out] : [],
  ];
  const before = snapshotFiles([workspace.root, workspace.cwd]);
  const allBefore = snapshotFiles([workspace.directory]);
  const result = await capture(mode === "isolated" ? ["unshare", "-rn", "--", ...args] : args, workspace.cwd);
  const after = snapshotFiles([workspace.root, workspace.cwd]);
  const allAfter = snapshotFiles([workspace.directory]);
  // Check effects before exit/JSON: even a crashing or malformed tool must not hide a write.
  expect(after, `${entry.command}: fixture/root or cwd changed (size/mtime/content)`).toEqual(before);
  if (mode === "out") delete allAfter[workspace.out];
  expect(allAfter, `${entry.command}: unexpected file in sibling directories`).toEqual(allBefore);
  const forbidden = result.effects.filter(effect => {
    if (effect.kind !== "file" || mode !== "out" || typeof effect.target !== "string") return true;
    const target = isAbsolute(effect.target) ? effect.target : resolve(workspace.cwd, effect.target);
    return target !== workspace.out;
  });
  expect(forbidden, "writes outside stdout/--out, network attempts, or unobserved subprocesses").toEqual([]);
  expect(result.exitCode, result.stderr || result.stdout).toBe(0);
  if (mode === "out") expect(result.effects).toContainEqual(expect.objectContaining({ kind: "file", target: workspace.out }));
  const output = mode === "out" ? readFileSync(workspace.out, "utf8") : result.stdout;
  const answer = JSON.parse(output);
  expect(answer.command).toBe(entry.command);
  expect(answer.query).toEqual(entry.query);
  expect(Array.isArray(answer.limits)).toBe(true);
  // --out may replace stdout or duplicate it; the spec permits both.
  if (mode === "out" && result.stdout.trim()) expect(JSON.parse(result.stdout)).toEqual(answer);
  return answer;
}

function expectKnownAnswer(answer: any, command: string) {
  expect(answer.empty).toBeUndefined();
  if (command === "where") expect(answer.matches).toEqual([expect.objectContaining(base)]);
  if (command === "find") expect(answer.matches).toContainEqual(expect.objectContaining(total));
  if (command === "callers") expect(answer.links).toContainEqual(expect.objectContaining({
    from: expect.objectContaining(total), to: expect.objectContaining(base),
  }));
  if (command === "callees") expect(answer.links).toContainEqual(expect.objectContaining({
    from: expect.objectContaining(total), to: expect.objectContaining(base),
  }));
  if (command === "chain") expect(answer.chain.down).toContainEqual(expect.objectContaining({
    level: 1, link: expect.objectContaining({ from: expect.objectContaining(total), to: expect.objectContaining(base) }),
  }));
  if (command === "tests") {
    expect(answer.tests.count).toBe(1);
    expect(answer.tests.tests).toContainEqual(expect.objectContaining({ name: "submits a private ledger" }));
  }
  if (command === "map") expect(answer.map.definitions).toEqual(expect.arrayContaining([
    expect.objectContaining(base), expect.objectContaining(total),
  ]));
}

function expectRebuiltAnswer(answer: any, command: string) {
  if (["where", "find", "callers", "tests"].includes(command)) {
    expect(answer.empty).toBe("none found by static analysis");
    expect(answer.matches ?? []).toEqual([]);
    expect(answer.links ?? []).toEqual([]);
    expect(answer.tests?.count ?? 0).toBe(0);
  } else if (command === "callees") {
    expect(answer.links).toContainEqual(expect.objectContaining({ to: expect.objectContaining({ name: "freshAmount" }) }));
    expect(answer.links.some((link: any) => link.to?.name === "baseAmount")).toBe(false);
  } else if (command === "chain") {
    expect(answer.chain.down).toContainEqual(expect.objectContaining({
      link: expect.objectContaining({ to: expect.objectContaining({ name: "freshAmount" }) }),
    }));
    expect(answer.chain.down.some((step: any) => step.link.to?.name === "baseAmount")).toBe(false);
  } else if (command === "map") {
    expect(answer.map.definitions).toContainEqual(expect.objectContaining({ name: "freshAmount" }));
    expect(answer.map.definitions.some((node: any) => node.name === "baseAmount")).toBe(false);
  }
}

function commandTests(entry: CommandCase) {
  for (const mode of ["stdout", "isolated", "out"] as const) {
    const behavior = {
      stdout: "answers with unchanged target/cwd and no observed writes or network attempts",
      isolated: "answers under unshare -rn with unchanged target/cwd",
      out: "writes only the named --out file for secret-bearing source",
    }[mode];
    test(`R3 ${entry.command} ${behavior} — Fails if: "${failsIf}"`, async () => {
      const workspace = createWorkspace(entry.command);
      try {
        if (mode === "stdout") expectOfflineSource();
        expect(readFileSync(resolve(workspace.root, "module/ledger.ts"), "utf8")).toContain(token);
        expectKnownAnswer(await runCli(workspace, entry, mode), entry.command);
      } finally {
        rmSync(workspace.directory, { recursive: true, force: true });
      }
    }, 20_000);
  }
  test(`R3 ${entry.command} rebuilds from changed files without a stored index — Fails if: "${failsIf}"`, async () => {
    const workspace = createWorkspace(entry.command);
    try {
      expectKnownAnswer(await runCli(workspace, entry), entry.command);
      const file = resolve(workspace.root, "module/ledger.ts");
      writeFileSync(file, readFileSync(file, "utf8").replaceAll("baseAmount", "freshAmount"));
      expectRebuiltAnswer(await runCli(workspace, entry), entry.command);
    } finally {
      rmSync(workspace.directory, { recursive: true, force: true });
    }
  }, 40_000);
}

test(`R3 observer detects transient writes outside target/cwd and caught network API calls — Fails if: "${failsIf}"`, async () => {
  const workspace = createWorkspace("observer");
  try {
    const canary = resolve(workspace.directory, "transient-canary.txt");
    const script = `
      const fs = await import("node:fs");
      const promises = await import("node:fs/promises");
      const path = ${JSON.stringify(canary)};
      fs.writeFileSync(path, "observer canary");
      await promises.writeFile(path, "observer canary");
      await Bun.write(path, "observer canary");
      const writer = Bun.file(path).writer();
      writer.write("observer canary");
      writer.end();
      fs.unlinkSync(path);
      try { await fetch("invalid-url"); } catch {}
      try { new WebSocket("invalid-url"); } catch {}
    `;
    const before = snapshotFiles([workspace.directory]);
    const result = await capture([
      "unshare", "-rn", "--", process.execPath, "--preload", observer, "--eval", script,
    ], workspace.cwd);
    expect(result.exitCode, result.stderr || result.stdout).toBe(0);
    expect(snapshotFiles([workspace.directory])).toEqual(before);
    for (const api of ["fs.writeFileSync", "fs.promises.writeFile", "Bun.write", "Bun.file.writer", "fs.unlinkSync"]) {
      expect(result.effects).toContainEqual({ kind: "file", api, target: canary });
    }
    expect(result.effects).toContainEqual({ kind: "network", api: "globalThis.fetch", target: "invalid-url" });
    expect(result.effects).toContainEqual({ kind: "network", api: "WebSocket", target: "invalid-url" });
  } finally {
    rmSync(workspace.directory, { recursive: true, force: true });
  }
}, 20_000);

commandTests({ command: "where", query: ["baseAmount"] });
commandTests({ command: "find", query: ["return baseAmount(units);"] });
commandTests({ command: "callers", query: ["baseAmount"] });
commandTests({ command: "callees", query: ["privateTotal"] });
commandTests({ command: "chain", query: [`${total.file}:${total.line}`], options: ["--up", "2", "--down", "2"] });
commandTests({ command: "tests", query: ["baseAmount"] });
commandTests({ command: "map", query: ["module"] });
