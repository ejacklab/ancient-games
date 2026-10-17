import { mkdir, readdir, readFile, writeFile } from "node:fs/promises";
import { resolve, relative, dirname } from "node:path";
import ts from "typescript";
import { loadCaseFile, type EvalCase, type CaseFile } from "./case-file.ts";
import { isObject } from "./matcher.ts";

type FileTransform = { lines: number[]; original: string; text: string };
export type FixtureTransform = { files: Map<string, FileTransform>; names: Map<string, string> };

function randomForSeed(seed: number) {
  let state = seed >>> 0;
  return () => {
    state = (state + 0x6d2b79f5) >>> 0;
    let value = Math.imul(state ^ state >>> 15, state | 1);
    value ^= value + Math.imul(value ^ value >>> 7, value | 61);
    return ((value ^ value >>> 14) >>> 0) / 4294967296;
  };
}

/** Rename identifier tokens, leaving quoted strings, comments and external module paths alone. */
export function renameCode(text: string, names: Map<string, string>): string {
  const file = ts.createSourceFile("snippet.ts", text, ts.ScriptTarget.Latest, true);
  return renameIdentifiers(file, names);
}

function renameIdentifiers(file: ts.SourceFile, names: Map<string, string>, checker?: ts.TypeChecker): string {
  const edits: { start: number; end: number; name: string }[] = [];
  function visit(node: ts.Node) {
    if (ts.isIdentifier(node) && names.has(node.text)) {
      const declarations = ts.isPropertyAccessExpression(node.parent) && node.parent.name === node
        ? checker?.getSymbolAtLocation(node)?.declarations : undefined;
      // A fixture's parameter name can coincide with a library member, such as IteratorResult.value.
      if (!declarations?.length || !declarations.every(declaration => declaration.getSourceFile().isDeclarationFile)) {
        edits.push({ start: node.getStart(file), end: node.getEnd(), name: names.get(node.text)! });
      }
    }
    ts.forEachChild(node, visit);
  }
  visit(file);
  const text = file.text;
  let result = ""; let end = 0;
  for (const edit of edits.sort((left, right) => left.start - right.start)) {
    result += text.slice(end, edit.start) + edit.name; end = edit.end;
  }
  return result + text.slice(end);
}

const TEST_API = new Set(["test", "it", "describe"]);

function declarationNames(file: ts.SourceFile): string[] {
  const names: string[] = [];
  function visit(node: ts.Node) {
    // All fixture declarations, including parameters, aliases and ambient declarations, are renamed.
    const parent = node.parent;
    const declaration = parent && (ts.isFunctionDeclaration(parent) || ts.isFunctionExpression(parent) || ts.isClassDeclaration(parent) ||
      ts.isClassExpression(parent) || ts.isInterfaceDeclaration(parent) || ts.isTypeAliasDeclaration(parent) ||
      ts.isVariableDeclaration(parent) || ts.isParameter(parent) || ts.isBindingElement(parent) ||
      ts.isMethodDeclaration(parent) || ts.isMethodSignature(parent) || ts.isPropertyDeclaration(parent) ||
      ts.isPropertySignature(parent) || ts.isPropertyAssignment(parent) || ts.isModuleDeclaration(parent) ||
      ts.isImportSpecifier(parent) || ts.isNamespaceImport(parent) || ts.isImportClause(parent) ||
      ts.isTypeParameterDeclaration(parent) || ts.isEnumDeclaration(parent) || ts.isEnumMember(parent));
    // The test API the spec names (test, it, describe) is kept, so a held-out test is still a test (COO fix).
    if (ts.isIdentifier(node) && declaration && "name" in parent && parent.name === node && !TEST_API.has(node.text)) names.push(node.text);
    if (ts.isShorthandPropertyAssignment(node)) names.push(node.name.text);
    ts.forEachChild(node, visit);
  }
  visit(file); return names;
}

export function relocatedLine(transform: FixtureTransform, file: string, line: number): number {
  const mapped = transform.files.get(file)?.lines[line - 1];
  if (mapped === undefined) throw new Error(`No source line for ${file}:${line}`);
  return mapped;
}

function rewriteQuery(text: string, transform: FixtureTransform): string {
  const location = /^(.*\.tsx?):(\d+)$/.exec(text);
  if (location) return `${location[1]}:${relocatedLine(transform, location[1]!, Number(location[2]))}`;
  if (text.startsWith("--") || transform.files.has(text) || text.includes("*.")) return text;
  return renameCode(text, transform.names);
}

/** Rewrites a structured answer/expectation witness using source-derived line and name maps. */
export function rewriteLocations(value: unknown, transform: FixtureTransform): unknown {
  if (Array.isArray(value)) return value.map(item => rewriteLocations(item, transform));
  if (!isObject(value)) return value;
  const copy: Record<string, unknown> = {};
  for (const [key, child] of Object.entries(value)) {
    if ((key === "line" || key === "endLine") && typeof value.file === "string" && typeof child === "number") copy[key] = relocatedLine(transform, value.file, child);
    else if (key === "name" && typeof child === "string") copy[key] = /^[\w$.]+$/.test(child) ? renameCode(child, transform.names) : child;
    else if (key === "text" && typeof child === "string" && isObject(value.at) && value.reason === undefined) {
      const at = value.at;
      const original = transform.files.get(String(at.file))?.original;
      // Recover the matching syntax node after edits so inserted interior comments are retained.
      const file = original ? ts.createSourceFile(String(at.file), original, ts.ScriptTarget.Latest, true) : undefined;
      let replacement: string | undefined;
      function visit(node: ts.Node) {
        if (file && node.getText(file) === child && file.getLineAndCharacterOfPosition(node.getStart(file)).line + 1 === at.line) {
          const changed = transform.files.get(String(at.file))!;
          const start = relocatedLine(transform, String(at.file), Number(at.line));
          const end = relocatedLine(transform, String(at.file), file.getLineAndCharacterOfPosition(node.getEnd() - 1).line + 1);
          const target = ts.createSourceFile(String(at.file), changed.text, ts.ScriptTarget.Latest, true);
          function find(next: ts.Node) {
            if (next.kind === node.kind && target.getLineAndCharacterOfPosition(next.getStart(target)).line + 1 === start &&
                target.getLineAndCharacterOfPosition(next.getEnd() - 1).line + 1 === end) replacement = next.getText(target);
            ts.forEachChild(next, find);
          }
          find(target);
        }
        ts.forEachChild(node, visit);
      }
      if (file) visit(file);
      if (replacement === undefined) throw new Error(`Cannot relocate source text at ${at.file}:${at.line}: ${child}`);
      copy[key] = replacement;
    } else if (key === "query" && Array.isArray(child)) copy[key] = child.map(item => rewriteQuery(String(item), transform));
    else copy[key] = rewriteLocations(child, transform);
  }
  return copy;
}

export function rewriteCase(sample: EvalCase, transform: FixtureTransform): EvalCase {
  const copy = structuredClone(sample);
  copy.args = sample.args.map(arg => rewriteQuery(arg, transform));
  copy.expect.includes = sample.expect.includes.map(check => rewriteLocations(check, transform) as typeof check);
  copy.expect.excludes = sample.expect.excludes.map(check => rewriteLocations(check, transform) as typeof check);
  if (sample.expect.shapes) copy.expect.shapes = sample.expect.shapes.map(check =>
    ({ ...check, value: rewriteLocations(check.value, transform) }));
  copy.expect.equals = sample.expect.equals.map(check => {
    if (check.path === "query" && Array.isArray(check.value)) {
      return { ...check, value: check.value.map(query => rewriteQuery(String(query), transform)) };
    }
    if (/\.(?:line|endLine)$/.test(check.path)) {
      const filePath = check.path.replace(/\.(?:line|endLine)$/, ".file");
      const files = sample.expect.equals.find(item => item.path === filePath)?.value;
      if (Array.isArray(check.value) && Array.isArray(files) && check.value.length === files.length) {
        return { ...check, value: check.value.map((line, index) => relocatedLine(transform, String(files[index]), Number(line))) };
      }
      if (typeof check.value === "number" && typeof files === "string") return { ...check, value: relocatedLine(transform, files, check.value) };
      throw new Error(`Location equality needs a paired file equality: ${sample.id} ${check.path}`);
    }
    const rename = (value: unknown): unknown => {
      if (Array.isArray(value)) return value.map(rename);
      if (typeof value === "string" && check.path.endsWith(".name")) return /^[\w$.]+$/.test(value) ? renameCode(value, transform.names) : value;
      if (typeof value === "string" && check.path.endsWith(".text") && !check.path.startsWith("limits")) return renameCode(value, transform.names);
      return rewriteLocations(value, transform);
    };
    return { ...check, value: rename(check.value) };
  });
  if (sample.expect.textIncludes) copy.expect.textIncludes = sample.expect.textIncludes.map(text => rewriteQuery(text, transform));
  return copy;
}

export async function generateHoldout(seed: number, out: string): Promise<{ caseFile: string; transform: FixtureTransform }> {
  if (!Number.isSafeInteger(seed) || seed < 0 || seed > 0xffffffff) throw new Error("--seed must be an unsigned 32-bit integer");
  const bundled = await loadCaseFile(resolve(import.meta.dir, "cases/fixtures.json"));
  const output = resolve(out);
  if (relative(bundled.root, output) === "" || !relative(bundled.root, output).startsWith("..")) throw new Error("Output must be outside the bundled fixtures");
  const files = new Map<string, FileTransform>(); const names = new Map<string, string>();
  async function collect(path: string) {
    for (const entry of (await readdir(path, { withFileTypes: true })).sort((a, b) => a.name.localeCompare(b.name))) {
      const full = resolve(path, entry.name);
      if (entry.isDirectory()) await collect(full);
      else if (entry.isFile() && /\.(?:ts|json)$/.test(entry.name)) {
        const original = await readFile(full, "utf8");
        files.set(relative(bundled.root, full), { original, text: original, lines: [] });
        if (entry.name.endsWith(".ts")) for (const name of declarationNames(ts.createSourceFile(full, original, ts.ScriptTarget.Latest, true))) names.set(name, "");
      }
    }
  }
  await collect(bundled.root);
  const program = ts.createProgram([...files.keys()].filter(file => file.endsWith(".ts")).map(file => resolve(bundled.root, file)), {
    target: ts.ScriptTarget.Latest, module: ts.ModuleKind.Preserve, moduleResolution: ts.ModuleResolutionKind.Bundler, types: [],
  });
  const checker = program.getTypeChecker();
  const random = randomForSeed(seed);
  for (const name of [...names.keys()].sort()) names.set(name, `${name}_h${seed.toString(36)}_${Math.floor(random() * 0x1000000).toString(36)}`);
  for (const [file, data] of files) {
    {
      const typescript = file.endsWith(".ts");
      const lines: string[] = [];
      const renamed = (typescript ? renameIdentifiers(program.getSourceFile(resolve(bundled.root, file))!, names, checker) : data.original).split("\n");
      renamed.forEach((line, index) => {
        const count = index === 0 || random() < 0.45 ? 1 + Math.floor(random() * 4) : 0;
        for (let padding = 0; padding < count; padding++) lines.push(!typescript || random() < 0.5 ? "" : `// held-out ${seed} ${index} ${padding}`);
        data.lines.push(lines.length + 1); lines.push(line);
      });
      data.text = lines.join("\n");
    }
    const path = resolve(output, file); await mkdir(dirname(path), { recursive: true }); await writeFile(path, data.text);
  }
  const transform = { files, names };
  const suite: CaseFile = { root: output, project: bundled.project.map(project => resolve(output, relative(bundled.root, project))),
    tests: bundled.tests, cases: bundled.cases.map(sample => rewriteCase(sample, transform)) };
  const caseFile = resolve(output, "fixtures.json");
  await writeFile(caseFile, JSON.stringify(suite, null, 2) + "\n");
  return { caseFile, transform };
}

if (import.meta.main) {
  try {
    const args = Bun.argv.slice(2);
    if (args.length !== 4 || args[0] !== "--seed" || args[2] !== "--out" || !/^\d+$/.test(args[1]!)) throw new Error("Usage: bun eval/holdout.ts --seed <n> --out <dir>");
    const result = await generateHoldout(Number(args[1]), args[3]!);
    console.log("Cases:", result.caseFile);
    console.log("R1 runtime marker checks remain bundled-only.");
  } catch (error) { console.error(String(error)); process.exitCode = 2; }
}
