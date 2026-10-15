status: done
Wrote Round 7 acceptance tests from SPEC alone: 16 pass and 3 expose empty stdout through consumer pipes; type checking passes.

files:
- .claude/skills/workflow-design/guard/test/round7-json.test.ts
- runs/20261016-integrate-r11-r13/nodes/tests-json.result.md

commands and last lines:
- `cd .claude/skills/workflow-design/guard && bun test test/round7-json.test.ts` — exit 1; `16 pass`, `3 fail`, `195 expect() calls`, `Ran 19 tests across 1 file. [527.00ms]`.
- `cd .claude/skills/workflow-design/guard && ./node_modules/.bin/tsgo --noEmit -p .` — exit 0, no output; no type errors in this file or elsewhere in the project at this check.
- `git diff --check -- .claude/skills/workflow-design/guard/test/round7-json.test.ts runs/20261016-integrate-r11-r13/nodes/tests-json.result.md` — exit 0, no output.

CONTRADICTS:
- SPEC.md:493, `Fails-if: --json output does not parse` (J1–J3 at lines 484–490): doctor, rates and insight each return empty stdout and exit 0 when captured through spawnSync's stdout pipe with a valid answered failure planted. JSON.parse throws `Unexpected EOF` in all three pipe tests. The same commands return valid reports through regular-file stdout descriptors. This is an observed contract failure in this environment; its implementation cause was not established.

Coverage: populated reports (including doctor health ok/summary and every harness field), rates counts/session filtering, open and answered failures, invalid sections and rule ids, unreadable insight paths, no-state roots, text format and exits, text equality across JSON calls, and SHA-256 tree comparisons around every CLI invocation. Text assertions pin the SPEC's documented format and compare before/after JSON calls; they cannot establish byte-for-byte identity with an unavailable earlier CLI version.

These checks were authored by this worker from SPEC Round 7 and the referenced contracts, not independently reviewed. No src/cli.ts content was read or changed. No source fixes, commits, other AI engines, or background commands were used. Bun's runtime transpiler cache is disabled in child processes to avoid runtime cache creation inside the planted HOME; stdout/stderr capture scratch files live outside the hashed root and are removed after each call.
