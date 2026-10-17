// p1-callhierarchy.mjs — written by the researcher, 2026-10-14. NOT RUN: the researcher had no shell.
// Answers brief questions 1 and 5 when run. It loads opencode's own TypeScript (5.8.2 expected), builds a
// LanguageService over packages/core/tsconfig.json, times it, and asks definition / implementation /
// call-hierarchy questions at fixed places. It reads source only; it executes no opencode code.
//
// Usage (from any directory):
//   node runs/20261014-code-map-build/evidence/p1-callhierarchy.mjs \
//     runs/20261014-opencode-code-map/src/opencode > runs/20261014-code-map-build/evidence/p1-callhierarchy-output.txt
import { createRequire } from "node:module"
import fs from "node:fs"
import path from "node:path"

const root = path.resolve(process.argv[2] ?? ".")
const core = path.join(root, "packages/core")
const ts = createRequire(path.join(core, "package.json"))("typescript")
const mb = (n) => (n / 1024 / 1024).toFixed(0) + " MB"
const mem = () => {
  const m = process.memoryUsage()
  return `rss ${mb(m.rss)}, heapUsed ${mb(m.heapUsed)}`
}
console.log(`typescript ${ts.version}; node ${process.version}; before: ${mem()}`)

const t0 = performance.now()
const config = ts.readConfigFile(path.join(core, "tsconfig.json"), ts.sys.readFile)
const parsed = ts.parseJsonConfigFileContent(config.config, ts.sys, core)
const host = {
  getScriptFileNames: () => parsed.fileNames,
  getScriptVersion: () => "0",
  getScriptSnapshot: (f) => (fs.existsSync(f) ? ts.ScriptSnapshot.fromString(fs.readFileSync(f, "utf8")) : undefined),
  getCurrentDirectory: () => core,
  getCompilationSettings: () => parsed.options,
  getDefaultLibFileName: (o) => ts.getDefaultLibFilePath(o),
  fileExists: ts.sys.fileExists,
  readFile: ts.sys.readFile,
  readDirectory: ts.sys.readDirectory,
  directoryExists: ts.sys.directoryExists,
  getDirectories: ts.sys.getDirectories,
}
const ls = ts.createLanguageService(host, ts.createDocumentRegistry())
const program = ls.getProgram()
const t1 = performance.now()
console.log(`program: ${parsed.fileNames.length} root files, ${program.getSourceFiles().length} source files; ` +
  `${((t1 - t0) / 1000).toFixed(1)} s; ${mem()}`)
let errors = 0
for (const sf of program.getSourceFiles()) if (!sf.isDeclarationFile) errors += program.getSemanticDiagnostics(sf).length
const t2 = performance.now()
console.log(`full type check: ${errors} semantic diagnostics; ${((t2 - t1) / 1000).toFixed(1)} s; ${mem()}`)

const rel = (f) => path.relative(root, f)
const line = (f, pos) => (program.getSourceFile(f)?.getLineAndCharacterOfPosition(pos).line ?? -1) + 1
const loc = (f, span) => `${rel(f)}:${line(f, span.start)}`
const item = (i) => `${i.kind} ${i.containerName ? i.containerName + "." : ""}${i.name} @ ${loc(i.file, i.selectionSpan)}`

function at(file, needle, offset) {
  const text = fs.readFileSync(file, "utf8")
  const i = text.indexOf(needle)
  if (i < 0) throw new Error(`not found in ${rel(file)}: ${needle}`)
  return i + offset
}

function probe(label, file, needle, offset) {
  const pos = at(file, needle, offset)
  console.log(`\n## ${label} — ${rel(file)}:${line(file, pos)} "${needle}" (+${offset})`)
  const defs = ls.getDefinitionAtPosition(file, pos) ?? []
  console.log(`definition: ${defs.length}`)
  for (const d of defs) console.log(`  ${d.kind} ${d.name} @ ${loc(d.fileName, d.textSpan)}`)
  const impls = ls.getImplementationAtPosition(file, pos) ?? []
  console.log(`implementation: ${impls.length}`)
  for (const d of impls) console.log(`  ${d.kind} @ ${loc(d.fileName, d.textSpan)}`)
  const prepared = ls.prepareCallHierarchy(file, pos)
  const items = prepared === undefined ? [] : Array.isArray(prepared) ? prepared : [prepared]
  console.log(`prepareCallHierarchy: ${items.length}`)
  for (const i of items) {
    console.log(`  item: ${item(i)}`)
    const p = i.selectionSpan.start
    const incoming = ls.provideCallHierarchyIncomingCalls(i.file, p)
    console.log(`  incoming: ${incoming.length}`)
    for (const c of incoming.slice(0, 15)) console.log(`    from ${item(c.from)} (${c.fromSpans.length} site(s))`)
    const outgoing = ls.provideCallHierarchyOutgoingCalls(i.file, p)
    console.log(`  outgoing: ${outgoing.length}`)
    for (const c of outgoing.slice(0, 25)) console.log(`    to ${item(c.to)} (${c.fromSpans.length} site(s))`)
  }
}

const src = (p) => path.join(core, "src", p)
probe("call on the injected service", src("tool/plugin/edit.ts"), "permission.assert(", "permission.".length)
probe("the injection itself", src("tool/plugin/edit.ts"), "yield* Permission.Service", "yield* Permission.".length)
probe("interface member", src("permission.ts"), "readonly assert:", "readonly ".length)
probe("implementation const", src("permission.ts"), "const assert = Effect.fn", "const ".length)
probe("shorthand in Service.of", src("permission.ts"), "Service.of({ ask, assert", "Service.of({ ask, ".length)
probe("a plain function, as a control", src("permission.ts"), "export function merge(", "export function ".length)
const t3 = performance.now()
console.log(`\nqueries: ${((t3 - t2) / 1000).toFixed(1)} s; end: ${mem()}`)
