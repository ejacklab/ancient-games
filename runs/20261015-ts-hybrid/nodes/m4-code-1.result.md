---
node: m4-code
attempt: 1
engine: opencode
model: MiniMax-M3.1-Flash-Preview
status: ok
started: 2026-10-15T08:24:00Z
ended: 2026-10-15T08:44:00Z
evidence: runs/20261015-ts-hybrid/nodes/m4-code-1.evidence.txt
---
M4 is implemented in `tools/harness-guard/src/register.ts` (loadRegister, isRegisterFile, validateRegister, units, freezeHash, coverage) and all 92 of the frozen `test/register.test.ts` cases pass with no type error in that file, while the whole suite and the typecheck still exit non-zero only on the two M5 test files whose modules (`src/hooks.ts`, `src/install.ts`) do not exist yet.
- Files written: tools/harness-guard/src/register.ts, runs/20261015-ts-hybrid/nodes/m4-code-1.result.md, runs/20261015-ts-hybrid/nodes/m4-code-1.evidence.txt
- Check: `cd tools/harness-guard && bun test test/register.test.ts` — 92 pass, 0 fail, 144 expect() calls; `cd tools/harness-guard && bun test` — 443 pass, 2 fail, 2 module-load errors (`test/cli.test.ts` and `test/hooks.test.ts`: `Cannot find module '../src/install.ts'` / `'../src/hooks.ts'`, both M5 modules, absent before this attempt — baseline before the attempt was 351 pass, 3 fail, 3 errors); `cd tools/harness-guard && ./node_modules/.bin/tsgo --noEmit -p .` — exit 2 with exactly 2 errors, both `TS2307 Cannot find module` in `test/cli.test.ts(7,32)` and `test/hooks.test.ts(6,28)` (the same M5 files), and none in `src/register.ts`; planted wrong inputs of my own (non-list `use_cases`, a scalar where a list belongs, `decision` as a bare string, blank `fails_if`/`reason`, `skippable: null`, blank `frozen`, blank `covered_by`, a conflict naming no ids) are reported as findings or ignored without a crash and without printing any source text (evidence section 5).
- CONTRADICTS: none in SPEC.md or src/types.ts. Two conditions outside this module prevent the literal "every test passes" and "exit 0" standards, and neither can be met from `src/register.ts` (the limits allow changing only that file and new `src/` files that only it imports): (1) `test/hooks.test.ts` imports `handleHook` from `../src/hooks.ts` and `test/cli.test.ts` imports `installSnippet` from `../src/install.ts`, and SPEC.md M5 (lines 200-254) has those files unwritten, so both files error at load in `bun test` and in `tsgo`; (2) SPEC.md M4 does not say whether a `covered_by` list holding only blank strings counts as coverage, so `coverage()` counts a unit as covered only when a `covered_by` entry is non-blank (the pinned case, an empty list, fails either way).