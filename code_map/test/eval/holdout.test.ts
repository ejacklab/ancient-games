import { afterEach, expect, test } from "bun:test";
import { mkdtemp, readFile, rm } from "node:fs/promises";
import { resolve, dirname } from "node:path";
import { tmpdir } from "node:os";
import ts from "typescript";
import { generateHoldout, rewriteLocations, relocatedLine, renameCode } from "../../eval/holdout.ts";
import { loadCaseFile } from "../../eval/case-file.ts";
import { matchAnswer } from "../../eval/matcher.ts";
import { validateAnswer } from "../../eval/contract.ts";
import { captureProcess, shellQuote } from "../../eval/process.ts";
import { evaluate } from "../../eval/run.ts";

const evalDir = resolve(import.meta.dir, "../../eval");
const scratch: string[] = [];
afterEach(async () => { for (const path of scratch.splice(0)) await rm(path, { recursive: true, force: true }); });
async function directory() { const path = await mkdtemp(resolve(tmpdir(), "cm-holdout-")); scratch.push(path); return path; }

function diagnostics(project: string) {
  const config = ts.readConfigFile(project, ts.sys.readFile);
  const parsed = ts.parseJsonConfigFileContent(config.config, ts.sys, dirname(project));
  const program = ts.createProgram(parsed.fileNames, parsed.options);
  return [...(config.error ? [config.error] : []), ...parsed.errors, ...ts.getPreEmitDiagnostics(program)].map(item => ts.flattenDiagnosticMessageText(item.messageText, "\n"));
}

for (const seed of [0, 1, 49271]) test(`held-out seed ${seed} type-checks and preserves every case's source expectations`, async () => {
  const out = await directory();
  const { caseFile, transform } = await generateHoldout(seed, out);
  const suite = await loadCaseFile(caseFile);
  for (const project of suite.project) expect(diagnostics(project)).toEqual([]);
  expect(suite.root).toBe(out);
  const originalProgram = ts.createProgram([...transform.files.keys()].filter(file => file.endsWith(".ts")).map(file => resolve(evalDir, "fixtures", file)), {
    target: ts.ScriptTarget.Latest, module: ts.ModuleKind.Preserve, moduleResolution: ts.ModuleResolutionKind.Bundler, types: [],
  });
  const checker = originalProgram.getTypeChecker();
  for (const [file, data] of transform.files) {
    if (!file.endsWith(".ts")) continue;
    expect(data.lines[0]).toBeGreaterThan(1);
    expect(data.lines.length).toBe(data.original.split("\n").length);
    // Independent token observations verify renaming and line remapping against the written file.
    const original = originalProgram.getSourceFile(resolve(evalDir, "fixtures", file))!;
    const changed = ts.createSourceFile(file, await readFile(resolve(out, file), "utf8"), ts.ScriptTarget.Latest, true);
    function identifiers(node: ts.Node): ts.Identifier[] {
      return [...(ts.isIdentifier(node) ? [node] : []), ...node.getChildren().flatMap(identifiers)];
    }
    const before = identifiers(original); const after = identifiers(changed);
    expect(after.length).toBe(before.length);
    before.forEach((node, index) => {
      const rewritten = after[index]!;
      const declarations = ts.isPropertyAccessExpression(node.parent) && node.parent.name === node
        ? checker.getSymbolAtLocation(node)?.declarations : undefined;
      const libraryMember = declarations?.length && declarations.every(declaration => declaration.getSourceFile().isDeclarationFile);
      expect(rewritten.text).toBe(libraryMember ? node.text : transform.names.get(node.text) ?? node.text);
      expect(changed.getLineAndCharacterOfPosition(rewritten.getStart(changed)).line + 1).toBe(
        relocatedLine(transform, file, original.getLineAndCharacterOfPosition(node.getStart(original)).line + 1));
    });
  }
  expect([...transform.names].every(([name, renamed]) => name !== renamed)).toBe(true);
  const support = transform.files.get("const-held/support.ts")!.text;
  expect(support).toContain(".next().value");
  const flow = transform.files.get("const-held/module/flow.ts")!.text;
  expect(flow).toContain(`${transform.names.get("Service")}.${transform.names.get("of")}({ ${transform.names.get("get")} })`);
  expect(flow).toContain(`${transform.names.get("Effect")}.${transform.names.get("fn")}("Compute")(function*`);
  for (const words of ["lunar ledger reconciliation", "copper orchard receipt"]) {
    expect(flow).toContain(words);
    expect(suite.cases.find(sample => sample.args[0] === "find" && sample.args[1] === words)).toBeDefined();
  }
  const exactCallees = suite.cases.find(sample => sample.id === "A5-exact-callees")!;
  expect(exactCallees.args[1]).toBe(`answer-scope/logic.ts:${relocatedLine(transform, "answer-scope/logic.ts", 1)}`);
  expect(exactCallees.expect.equals.find(check => check.path === "query")!.value).toEqual(exactCallees.args.slice(1));
  const inline = suite.cases.find(sample => sample.id === "A2-inline-generator-owner")!;
  expect(inline.expect.excludes[0]!.line).toBe(relocatedLine(transform, "effect-inline/use.ts", 3));
  const shadow = suite.cases.find(sample => sample.id === "A2-same-name-helper-fake")!;
  expect(shadow.expect.excludes.map(check => check.line)).toEqual([
    relocatedLine(transform, "effect-shadow/helper.ts", 1),
    relocatedLine(transform, "effect-shadow/fake.testcase.ts", 3),
    relocatedLine(transform, "effect-shadow/helper.ts", 1),
  ]);
  const twins = suite.cases.find(sample => sample.id === "A2-effect-step-ambiguous")!;
  expect(twins.args[1]).toBe(transform.names.get("relayStep")!);
  expect(twins.expect.shapes![0]!.value).toEqual(["one", "two"].map(variant => ({
    file: `effect-twins/${variant}.ts`, line: relocatedLine(transform, `effect-twins/${variant}.ts`, 2),
    name: transform.names.get("relayStep"), kind: "effect-fn",
  })));
  const defaultText = suite.cases.find(sample => sample.id === "A5-default-text")!;
  expect(defaultText.expect.excludes[0]!.line).toBe(relocatedLine(transform, "chain/logic.ts", 4));
  for (const direction of ["down", "up"]) for (const suffix of ["", "-reversed"]) {
    const file = `route-depth/${direction}${suffix}.ts`;
    const sample = suite.cases.find(sample => sample.id === `A2-shorter-route-${direction}${suffix}`)!;
    const tailLine = direction === "down" ? 8 : 5;
    expect(sample.args[1]).toBe(`${file}:${relocatedLine(transform, file, 1)}`);
    expect(sample.expect.includes[0]!.line).toBe(relocatedLine(transform, file, tailLine));
    expect(transform.files.get(file)!.text).toContain(transform.names.get("routeTail")!);
  }
  for (const sample of suite.cases) {
    const original: any = JSON.parse(await readFile(resolve(evalDir, "stub/answers", sample.id + ".json"), "utf8"));
    const answer: any = rewriteLocations(original, transform);
    if (["R1", "R3"].includes(sample.requirement)) continue;
    if (sample.format === "text") {
      const text = answer.matches.map((node: any) => `${node.name} — ${node.file}:${node.line}`).join("\n");
      expect(matchAnswer(text, sample.expect)).toEqual([]);
    } else {
      expect(matchAnswer(answer, sample.expect)).toEqual([]);
      expect(validateAnswer(answer, sample.args, sample.tests ?? suite.tests, suite.root)).toEqual([]);
    }
  }
}, 30_000);

test("same seed reproduces source and expectations; a different seed changes them", async () => {
  const left = await generateHoldout(3, await directory());
  const right = await generateHoldout(3, await directory());
  const other = await generateHoldout(4, await directory());
  for (const [file, data] of left.transform.files) expect(data.text).toBe(right.transform.files.get(file)!.text);
  expect((await loadCaseFile(left.caseFile)).cases).toEqual((await loadCaseFile(right.caseFile)).cases);
  expect(left.transform.files.get("chain/logic.ts")!.text).not.toBe(other.transform.files.get("chain/logic.ts")!.text);
  expect(renameCode('leaf("leaf") // leaf', left.transform.names)).toBe(`${left.transform.names.get("leaf")}("leaf") // leaf`);
});

test("held-out CLI and --cases loading work; bundled stub table does not match the copy", async () => {
  const out = await directory();
  const result = await captureProcess([process.execPath, resolve(evalDir, "holdout.ts"), "--seed", "19", "--out", out], resolve(evalDir, ".."));
  expect(result.exitCode).toBe(0);
  const suite = await loadCaseFile(resolve(out, "fixtures.json"));
  expect(suite.cases.length).toBeGreaterThan(37);
  // One case suffices to demonstrate black-box use of the relocated root without running all fixtures again.
  const path = resolve(out, "single.json");
  await Bun.write(path, JSON.stringify({ ...suite, cases: suite.cases.filter(sample => sample.id === "A5-specific-answer") }));
  const report = await evaluate({ tool: `${shellQuote(process.execPath)} ${shellQuote(resolve(evalDir, "stub/stub.ts"))}`,
    cases: [path], out: resolve(out, "report"), cwd: out });
  expect(report.cases[0]!.status).toBe("NOT MET");
  expect(report.cases[0]!.markerCreated).toBeUndefined();
});

test("holdout rejects invalid seeds and overwriting the bundled fixtures", async () => {
  const out = await directory();
  for (const seed of [-1, 1.5, NaN, 0x100000000]) expect(generateHoldout(seed, out)).rejects.toThrow();
  expect(generateHoldout(1, resolve(evalDir, "fixtures"))).rejects.toThrow();
});
