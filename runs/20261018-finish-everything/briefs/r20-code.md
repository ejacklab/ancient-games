# Brief — guard Round 20: one deadline at a time, criteria at the end, crossed-build-check timeout

You work in the repository root. Use relative paths. Change only `.claude/skills/workflow-design/guard/src/cli.ts`,
`.claude/skills/workflow-design/guard/src/deadline.ts`, `.claude/skills/workflow-design/guard/src/hooks.ts`,
`.claude/workflows/crossed-build-check.js`, and the progress and result files below. Do not change any test, the
SPEC or any doc. Do not commit or stage anything. Another session works in this repository: touch nothing else.

## Task
Implement Round 20 of `.claude/skills/workflow-design/guard/SPEC.md` (the last section: DL1–DL4, CR1, XB1; C17 is
already done in the tests). The tests written from it fail now and must pass:
- `cd .claude/skills/workflow-design/guard && bun test test/round20-deadline.test.ts test/round20-criteria.test.ts`
- `node tests/workflows/crossed_build_check_harness.mjs`

## Lessons
- When a change sends new cases into an existing code path, list that path's early returns and exemptions first, and
  test each with one of the new cases.
- Keep the existing behaviour where the spec says "unchanged" or "as before": the full suite freezes it.

## Pieces and progress (first)
Pieces: `dl` (DL1–DL4 in cli.ts and deadline.ts), `cr` (CR1 in hooks.ts), `xb` (XB1 in crossed-build-check.js).
Append one `planned` line per piece to `runs/20261018-finish-everything/nodes/r20-code.progress.md`, then one line as
each starts and ends: `- <date -Iseconds> · <piece> · <planned|start|done|fail> · <note>`.

## Standard
- `cd .claude/skills/workflow-design/guard && bun test` all pass (about 1530 tests);
- `cd .claude/skills/workflow-design/guard && ./node_modules/.bin/tsgo --noEmit -p .` clean;
- `node tests/workflows/crossed_build_check_harness.mjs` all pass.

## Result
`runs/20261018-finish-everything/nodes/r20-code.result.md`: `status: done|partial|fail`, one sentence; per piece what
changed (file and function); the three commands' last lines; CONTRADICTS (a spec line that cannot be met as written,
quoted) or none.
