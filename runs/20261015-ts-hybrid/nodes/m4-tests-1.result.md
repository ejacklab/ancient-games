---
node: m4-tests
attempt: 1
engine: codex
model: unavailable (tools expose no model identifier)
status: ok
started: 2026-10-15T08:31:13Z
ended: 2026-10-15T08:34:56Z
evidence: runs/20261015-ts-hybrid/nodes/m4-tests-1.evidence.txt
---
M4 acceptance tests are written; Bun fails only on the missing register implementation, and TypeScript reports only missing modules.
- Files written: tools/harness-guard/test/register.test.ts; runs/20261015-ts-hybrid/nodes/m4-tests-1.evidence.txt; runs/20261015-ts-hybrid/nodes/m4-tests-1.result.md
- Check: `cd tools/harness-guard && bun test test/register.test.ts` — exit 1; `error: Cannot find module '../src/register.ts' from '/home/smoke01/dev/ancient-games-ts-hybrid/tools/harness-guard/test/register.test.ts'`; `0 pass, 1 fail, 1 error`.
- Check: `cd tools/harness-guard && ./node_modules/.bin/tsgo --noEmit -p .` — exit 2; `test/register.test.ts(6,93): error TS2307: Cannot find module '../src/register.ts' or its corresponding type declarations.` Also reports the pre-existing missing `../src/insight.ts` at `test/insight.test.ts(5,86)`. No other diagnostics.
- CONTRADICTS: none
