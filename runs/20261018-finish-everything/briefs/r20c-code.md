# Brief — after the Codex review: guard XB4 and memory-check findings 1–3

You work in the repository root. Use relative paths only, from the repository root; never `cd` to an absolute path.
Change only `memory_check/src/**`,
`.claude/workflows/crossed-build-check.js`, and the progress and result files below. Do not change any test, the SPEC
or any doc. Do not commit or stage anything. Another session works in this repository: touch nothing else.

## Task
Implement XB4 of the last paragraph of `.claude/skills/workflow-design/guard/SPEC.md` ("Round 20, after the Codex review"), and fix memory-check findings 1, 2 and 3 of `runs/20261018-finish-everything/nodes/codex-review.md` (the judge reproduced each; read them there).
The tests written from them fail now and must pass:
- `cd memory_check && bun test test/review3.test.ts`
- `node tests/workflows/crossed_build_check_harness.mjs`

## Lessons
- When a change sends new cases into an existing code path, list that path's early returns and exemptions first, and
  test each with one of the new cases.
- Keep the existing behaviour where the spec says "unchanged" or "as before": the full suite freezes it.
- Write your result file first, as `status: partial`, and update it at the end.

## Pieces and progress (first)
Pieces: `f1`, `f2`, `f3` (memory_check/src), `xb4` (crossed-build-check.js). Append one `planned` line per
piece to `runs/20261018-finish-everything/nodes/r20c-code.progress.md`, then one line as each starts and ends:
`- <date -Iseconds> · <piece> · <planned|start|done|fail> · <note>`.

## Standard
- `cd memory_check && bun test` all pass, `cd memory_check && ./node_modules/.bin/tsgo --noEmit -p .` clean;
- `cd .claude/skills/workflow-design/guard && bun test` all pass;
- `cd .claude/skills/workflow-design/guard && ./node_modules/.bin/tsgo --noEmit -p .` clean;
- `node tests/workflows/crossed_build_check_harness.mjs` all pass.

## Result
`runs/20261018-finish-everything/nodes/r20c-code.result.md`: `status: done|partial|fail`, one sentence; per piece what
changed (file and function); the three commands' last lines; CONTRADICTS (a spec line that cannot be met as written,
quoted) or none.
