---
node: m1-tests
attempt: 1
engine: codex
model: unreported-by-available-tools
status: ok
started: 2026-10-15T08:07:51Z
ended: 2026-10-15T08:11:44Z
evidence: runs/20261015-ts-hybrid/nodes/m1-tests-1.evidence.txt
---
Wrote M1 acceptance tests covering every Fails-if case and all six exports; both required checks report only the intentionally missing implementation.
- Files written: tools/harness-guard/test/traps.test.ts; runs/20261015-ts-hybrid/nodes/m1-tests-1.evidence.txt; runs/20261015-ts-hybrid/nodes/m1-tests-1.result.md.
- Check: `cd tools/harness-guard && bun test test/traps.test.ts` — exit 1; `error: Cannot find module '../src/traps.ts' from '/home/smoke01/dev/ancient-games-ts-hybrid/tools/harness-guard/test/traps.test.ts'`; `0 pass, 1 fail, 1 error; Ran 1 test across 1 file. [5.00ms]`.
- Check: `cd tools/harness-guard && ./node_modules/.bin/tsgo --noEmit -p .` — exit 2; `test/traps.test.ts(12,8): error TS2307: Cannot find module '../src/traps.ts' or its corresponding type declarations.`; no other diagnostics.
- Check: `git status --short --untracked-files=all` — exit 0; only the new test and the pre-existing brief and brief generator were present before writing these result artifacts.
- CONTRADICTS: tools/harness-guard/SPEC.md:40 says recognition background status can come from the caller, but its signature at :33 accepts only a command and engine specs; src/types.ts:38-45 provides no caller background field. That caller-input branch cannot be exercised through the specified recognition signature; lint's ctx.background is tested.
- CONTRADICTS: tools/harness-guard/SPEC.md:35 and :38-39 make wrapper --out DIR both outputFile and a directory containing status.json; :56-57 describes checking outputFile for non-whitespace file content without defining directory handling. Tests cover recognition and status checking separately without inventing directory-content semantics.
- CONTRADICTS: tools/harness-guard/SPEC.md:8-9 lists permitted node modules without node:os, while the brief requires fs.mkdtempSync(path.join(os.tmpdir(), "hg-")). The tests follow the brief and import node:os.
