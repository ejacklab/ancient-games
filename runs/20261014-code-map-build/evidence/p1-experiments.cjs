// P1 experiments E1-E4 (COO, 2026-10-14). Measurement only; reads opencode, writes stdout.
// Usage: node p1-experiments.cjs <opencode root> <E1|E2|E3|E4>
const path = require("path");
const root = path.resolve(process.argv[2]);
const which = process.argv[3];
const ts = require(path.join(root, "node_modules/typescript"));

function makeLS(configPaths) {
  const t0 = Date.now();
  let files = [], options;
  for (const c of configPaths) {
    const cfg = ts.getParsedCommandLineOfConfigFile(c, {}, { ...ts.sys, onUnRecoverableConfigFileDiagnostic: d => console.error(ts.flattenDiagnosticMessageText(d.messageText, "\n")) });
    files.push(...cfg.fileNames); options = options || cfg.options;
  }
  files = [...new Set(files)];
  const host = {
    getScriptFileNames: () => files, getScriptVersion: () => "1",
    getScriptSnapshot: f => ts.sys.fileExists(f) ? ts.ScriptSnapshot.fromString(ts.sys.readFile(f)) : undefined,
    getCurrentDirectory: () => path.dirname(configPaths[0]), getCompilationSettings: () => options,
    getDefaultLibFileName: o => ts.getDefaultLibFilePath(o),
    fileExists: ts.sys.fileExists, readFile: ts.sys.readFile, readDirectory: ts.sys.readDirectory,
    directoryExists: ts.sys.directoryExists, getDirectories: ts.sys.getDirectories,
    useSourceOfProjectReferenceRedirect: () => true,
  };
  const ls = ts.createLanguageService(host, ts.createDocumentRegistry());
  const prog = ls.getProgram();
  const dts = prog.getSourceFiles().filter(s => s.fileName.includes("/packages/") && s.fileName.endsWith(".d.ts") && !s.fileName.includes("node_modules")).length;
  console.log(`program: ${files.length} root files, ${prog.getSourceFiles().length} source files, ${dts} repo .d.ts files, ${Date.now() - t0} ms, heap ${Math.round(process.memoryUsage().heapUsed / 1e6)} MB`);
  return { ls, prog };
}
const rel = f => path.relative(root, f);
function loc(prog, f, pos) { const sf = prog.getSourceFile(f); const lc = sf.getLineAndCharacterOfPosition(pos); return `${rel(f)}:${lc.line + 1}`; }
function nodeAt(sf, pos) { let found; (function walk(n) { if (pos >= n.getStart(sf) && pos < n.getEnd()) { found = n; ts.forEachChild(n, walk); } })(sf); return found; }
function enclosingFn(n) { while (n && !(ts.isFunctionLike(n))) n = n.parent; return n; }
function isCallee(id) { // identifier is the called name: x.m(...) or m(...)
  const p = id.parent;
  if (ts.isPropertyAccessExpression(p) && p.name === id) { return ts.isCallExpression(p.parent) && p.parent.expression === p; }
  return ts.isCallExpression(p) && p.expression === id;
}
const core = path.join(root, "packages/core");

if (which === "E1") {
  const { ls, prog } = makeLS([path.join(core, "tsconfig.json")]);
  const f = path.join(core, "src/permission.ts"); const text = ts.sys.readFile(f);
  const pos = text.indexOf("readonly assert:") + "readonly ".length;
  const refs = (ls.findReferences(f, pos) || []).flatMap(r => r.references);
  const kinds = {};
  for (const r of refs) {
    const sf = prog.getSourceFile(r.fileName); const id = nodeAt(sf, r.textSpan.start);
    let kind = r.isDefinition ? "definition" : isCallee(id) ? "call" : ts.isShorthandPropertyAssignment(id.parent) ? "shorthand (Service.of)" : ts.isPropertyAssignment(id.parent) ? "property assignment" : "other reference";
    kinds[kind] = (kinds[kind] || 0) + 1;
    const fn = enclosingFn(id);
    console.log(`${kind.padEnd(24)} ${loc(prog, r.fileName, r.textSpan.start)}  in ${fn ? (fn.name ? fn.name.getText(sf) : ts.SyntaxKind[fn.kind]) : "module top level"}`);
  }
  console.log("summary:", JSON.stringify(kinds));
}

if (which === "E2" || which === "E3") {
  const configs = which === "E2" ? [path.join(core, "tsconfig.json")] : [path.join(core, "tsconfig.json"), path.join(core, "tsconfig.tests.json")];
  const { ls, prog } = makeLS(configs);
  if (which === "E3") {
    const f = path.join(core, "src/tool/plugin/edit.ts"); const text = ts.sys.readFile(f);
    const pos = text.indexOf("permission.assert") + "permission.".length;
    const impls = ls.getImplementationAtPosition(f, pos) || [];
    console.log(`E3 implementations at edit.ts permission.assert: ${impls.length}`);
    for (const i of impls) console.log(`  ${loc(prog, i.fileName, i.textSpan.start)} ${i.kind}`);
    const t = Date.now(); const refs = (ls.findReferences(path.join(core, "src/permission.ts"), ts.sys.readFile(path.join(core, "src/permission.ts")).indexOf("readonly assert:") + 9) || []).flatMap(r => r.references);
    console.log(`E3 references to Permission.assert incl. tests: ${refs.length} in ${new Set(refs.map(r => r.fileName)).size} files, test files ${new Set(refs.filter(r => r.fileName.includes("/test/")).map(r => r.fileName)).size} (${Date.now() - t} ms)`);
  } else {
    // E2: for each `class X extends Context.Service<...>` in core/src, find one member call site and look up its implementation.
    const out = { resolvedToFnBody: 0, resolvedOther: 0, none: 0, multiple: 0, noCallSite: 0 };
    const samples = [];
    for (const sf of prog.getSourceFiles()) {
      if (!sf.fileName.startsWith(path.join(core, "src"))) continue;
      ts.forEachChild(sf, n => {
        if (!ts.isClassDeclaration(n) || !n.heritageClauses || !/Context\.Service</.test(n.heritageClauses[0].getText(sf))) return;
        const cls = n.name.getText(sf);
        // the Interface type: first type argument after Service in Context.Service<Service, Interface>
        const m = n.heritageClauses[0].getText(sf).match(/Context\.Service<\s*\w+\s*,\s*(\w+)/);
        if (!m) { out.noCallSite++; samples.push(`${rel(sf.fileName)} ${cls}: no interface type`); return; }
        const iface = sf.statements.find(s => (ts.isInterfaceDeclaration(s) || ts.isTypeAliasDeclaration(s)) && s.name.getText(sf) === m[1]);
        const members = iface && ts.isInterfaceDeclaration(iface) ? iface.members.filter(x => x.name) : [];
        let done = false;
        for (const mem of members) {
          const refs = (ls.findReferences(sf.fileName, mem.name.getStart(sf)) || []).flatMap(r => r.references).filter(r => !r.isDefinition);
          const call = refs.find(r => { const s2 = prog.getSourceFile(r.fileName); const id = nodeAt(s2, r.textSpan.start); return id && isCallee(id); });
          if (!call) continue;
          const impls = ls.getImplementationAtPosition(call.fileName, call.textSpan.start) || [];
          const s2 = prog.getSourceFile(call.fileName);
          let verdict;
          if (impls.length === 0) verdict = "none";
          else if (impls.length > 1) verdict = "multiple";
          else {
            const isf = prog.getSourceFile(impls[0].fileName); const inode = nodeAt(isf, impls[0].textSpan.start);
            const decl = inode && (ts.isVariableDeclaration(inode.parent) ? inode.parent : inode);
            const init = decl && decl.initializer ? decl.initializer.getText(isf).slice(0, 40) : (inode ? ts.SyntaxKind[inode.parent.kind] : "?");
            verdict = /Effect\.fn|=>|function/.test(init) || ts.isFunctionLike(inode.parent) || ts.isMethodDeclaration(inode.parent) ? "resolvedToFnBody" : "resolvedOther";
          }
          out[verdict]++;
          samples.push(`${verdict.padEnd(17)} ${cls}.${mem.name.getText(sf)} @ ${loc(prog, call.fileName, call.textSpan.start)} -> ${impls.map(i => loc(prog, i.fileName, i.textSpan.start)).join(", ") || "-"}`);
          done = true; break;
        }
        if (!done && members.length) { out.noCallSite++; samples.push(`${"noCallSite".padEnd(17)} ${cls} (${rel(sf.fileName)})`); }
        if (!members.length && iface === undefined) { out.noCallSite++; samples.push(`${"noInterface".padEnd(17)} ${cls} (${rel(sf.fileName)})`); }
      });
    }
    samples.forEach(s => console.log(s));
    console.log("summary:", JSON.stringify(out));
  }
}

if (which === "E4") {
  makeLS([path.join(root, "packages/ai/tsconfig.json")]);
}
console.log(`peak heap ${Math.round(process.memoryUsage().heapUsed / 1e6)} MB`);
