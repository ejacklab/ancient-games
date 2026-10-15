---
node: m5-tests
attempt: 1
engine: codex
model: unavailable (tools expose no model identifier)
status: partial
started: 2026-10-15T08:35:31Z
ended: 2026-10-15T08:43:00Z
evidence: runs/20261015-ts-hybrid/nodes/m5-tests-1.evidence.txt
---
Hook, install and CLI acceptance tests are written; direct doctor and opencode plugin tests remain pending their unspecified callable interfaces.
- Files written: tools/harness-guard/test/hooks.test.ts; tools/harness-guard/test/cli.test.ts; runs/20261015-ts-hybrid/nodes/m5-tests-1.evidence.txt; runs/20261015-ts-hybrid/nodes/m5-tests-1.result.md
- Check: `cd tools/harness-guard && bun --version` — `1.4.3`, exit 0.
- Check: `cd tools/harness-guard && bun test test/hooks.test.ts, test/cli.test.ts` — exit 1; `0 pass, 1 fail, 1 error`; the comma selects only cli.test.ts; exact error: `error: Cannot find module '../src/install.ts' from '/home/smoke01/dev/ancient-games-ts-hybrid/tools/harness-guard/test/cli.test.ts'`.
- Check: `cd tools/harness-guard && bun test test/hooks.test.ts test/cli.test.ts` — exit 1; `0 pass, 2 fail, 2 errors`; exact errors: `error: Cannot find module '../src/install.ts' from '/home/smoke01/dev/ancient-games-ts-hybrid/tools/harness-guard/test/cli.test.ts'` and `error: Cannot find module '../src/hooks.ts' from '/home/smoke01/dev/ancient-games-ts-hybrid/tools/harness-guard/test/hooks.test.ts'`. No assertions ran.
- Check: `cd tools/harness-guard && ./node_modules/.bin/tsgo --noEmit -p .` — final exit 2; only `test/cli.test.ts(7,32): error TS2307: Cannot find module '../src/install.ts' or its corresponding type declarations.` and `test/hooks.test.ts(6,28): error TS2307: Cannot find module '../src/hooks.ts' or its corresponding type declarations.` No other final diagnostics.
- Check: `git status --short` — exit 0; full output in evidence.
- CONTRADICTS: tools/harness-guard/SPEC.md:246 declares `doctor(opts): DoctorReport` without defining opts; src/types.ts defines DoctorReport but no options type or settings/health injection contract. Its exact signature and machine-independent fixtures cannot be tested from SPEC.md alone. Clarification requested.
- CONTRADICTS: tools/harness-guard/SPEC.md:235 specifies a default opencode plugin and its event name, but no factory or callback arguments, return type, or cwd/running injection contract. Its exact callable signature cannot be tested from SPEC.md alone. Clarification requested.
