// Probe: does the TypeScript 5.8 LanguageService call hierarchy follow a call on an Effect-injected service?
// Usage: node p1-callhierarchy-probe.cjs <opencode root>
const path = require("path");
const root = path.resolve(process.argv[2]);
const ts = require(path.join(root, "node_modules/typescript"));
const t0 = Date.now();
const cfgPath = path.join(root, "packages/core/tsconfig.json");
const cfg = ts.getParsedCommandLineOfConfigFile(cfgPath, {}, { ...ts.sys, onUnRecoverableConfigFileDiagnostic: d => console.error(d) });
const versions = {};
const host = {
  getScriptFileNames: () => cfg.fileNames,
  getScriptVersion: f => "1",
  getScriptSnapshot: f => ts.sys.fileExists(f) ? ts.ScriptSnapshot.fromString(ts.sys.readFile(f)) : undefined,
  getCurrentDirectory: () => path.dirname(cfgPath),
  getCompilationSettings: () => cfg.options,
  getDefaultLibFileName: o => ts.getDefaultLibFilePath(o),
  fileExists: ts.sys.fileExists, readFile: ts.sys.readFile, readDirectory: ts.sys.readDirectory,
  directoryExists: ts.sys.directoryExists, getDirectories: ts.sys.getDirectories,
};
const ls = ts.createLanguageService(host, ts.createDocumentRegistry());
const prog = ls.getProgram();
console.log(`program: ${cfg.fileNames.length} root files, ${prog.getSourceFiles().length} source files, ${Date.now() - t0} ms, heap ${Math.round(process.memoryUsage().heapUsed / 1e6)} MB`);
function at(rel, needle, nth = 0) {
  const f = path.join(root, rel); const text = ts.sys.readFile(f);
  let i = -1; for (let k = 0; k <= nth; k++) i = text.indexOf(needle, i + 1);
  if (i < 0) throw new Error(`not found: ${needle} in ${rel}`);
  const line = text.slice(0, i).split("\n").length;
  return { f, pos: i, line };
}
function loc(fileName, pos) { const sf = prog.getSourceFile(fileName); const lc = sf.getLineAndCharacterOfPosition(pos); return `${path.relative(root, fileName)}:${lc.line + 1}`; }
// The call site: permission.assert in edit.ts
const site = at("packages/core/src/tool/plugin/edit.ts", "permission.assert");
const assertPos = site.pos + "permission.".length;
console.log(`call site ${path.relative(root, site.f)}:${site.line}`);
const defs = ls.getDefinitionAtPosition(site.f, assertPos) || [];
console.log("definition:", defs.map(d => loc(d.fileName, d.textSpan.start)).join(", ") || "none");
const impls = ls.getImplementationAtPosition(site.f, assertPos) || [];
console.log("implementations:", impls.map(d => loc(d.fileName, d.textSpan.start)).join(", ") || "none");
// Call hierarchy from the interface member: who calls Permission's assert?
const t1 = Date.now();
for (const d of defs) {
  const items = ls.prepareCallHierarchy(d.fileName, d.textSpan.start);
  const arr = Array.isArray(items) ? items : items ? [items] : [];
  for (const it of arr) {
    const inc = ls.provideCallHierarchyIncomingCalls(it.file, it.selectionSpan.start);
    console.log(`incoming calls to ${it.name} (${loc(it.file, it.selectionSpan.start)}): ${inc.length}`);
    for (const c of inc.slice(0, 40)) console.log(`  from ${c.from.name} @ ${loc(c.from.file, c.from.selectionSpan.start)} (${c.fromSpans.length} site(s))`);
  }
}
console.log(`incoming-call query ${Date.now() - t1} ms`);
// Outgoing calls from the edit tool's enclosing function at the call site
const t2 = Date.now();
const encl = ls.prepareCallHierarchy(site.f, site.pos);
const ea = Array.isArray(encl) ? encl : encl ? [encl] : [];
console.log(`prepare at call site -> ${ea.map(e => e.name + "@" + loc(e.file, e.selectionSpan.start)).join(", ") || "none"}`);
console.log(`total ${Date.now() - t0} ms, heap ${Math.round(process.memoryUsage().heapUsed / 1e6)} MB`);
// Part 2: callers of Permission.assert via findReferences on the interface member
const t3 = Date.now();
for (const d of defs) {
  const refs = ls.findReferences(d.fileName, d.textSpan.start) || [];
  const all = refs.flatMap(r => r.references.filter(x => !x.isDefinition));
  console.log(`references to interface member ${loc(d.fileName, d.textSpan.start)}: ${all.length} in ${new Set(all.map(x => x.fileName)).size} files (${Date.now() - t3} ms)`);
  for (const x of all.slice(0, 12)) console.log(`  ${loc(x.fileName, x.textSpan.start)}`);
}
// Call hierarchy prepared at the implementation
const ip = impls[0];
if (ip) {
  const items = ls.prepareCallHierarchy(ip.fileName, ip.textSpan.start);
  const arr = Array.isArray(items) ? items : items ? [items] : [];
  console.log(`prepare at implementation -> ${arr.map(e => e.kind + " " + e.name).join(", ") || "none"}`);
  for (const it of arr) {
    const inc = ls.provideCallHierarchyIncomingCalls(it.file, it.selectionSpan.start);
    console.log(`  incoming: ${inc.length}`);
  }
}
