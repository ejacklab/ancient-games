---
node: m2-tests
attempt: 1
engine: codex
model: unavailable (tools expose no model identifier)
status: ok
started: 2026-10-15T08:13:13Z
ended: 2026-10-15T08:17:55Z
evidence: runs/20261015-ts-hybrid/nodes/m2-tests-1.evidence.txt
---
M2 acceptance tests are written, and both required checks fail only because src/journal.ts is missing.
- Files written: tools/harness-guard/test/journal.test.ts; runs/20261015-ts-hybrid/nodes/m2-tests-1.evidence.txt; runs/20261015-ts-hybrid/nodes/m2-tests-1.result.md
- Check: `cd tools/harness-guard && bun test test/journal.test.ts` — exit 1; `error: Cannot find module '../src/journal.ts' from '/home/smoke01/dev/ancient-games-ts-hybrid/tools/harness-guard/test/journal.test.ts'`; `0 pass, 1 fail, 1 error`.
- Check: `cd tools/harness-guard && ./node_modules/.bin/tsgo --noEmit -p .` — exit 2; `test/journal.test.ts(16,8): error TS2307: Cannot find module '../src/journal.ts' or its corresponding type declarations.` No other diagnostics.
- CONTRADICTS: SPEC.md:10–11 forbids raw prompt/output/config content in outputs, while SPEC.md:83–89 accepts arbitrary non-empty record strings and extra fields and says appendFailure returns the record. For a record containing raw content, the specification does not resolve rejection, redaction or caller sanitization. Secret tests accept rejection or redaction without prescribing a format.
