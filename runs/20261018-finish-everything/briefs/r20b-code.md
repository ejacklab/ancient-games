# Brief — guard Round 20, after its review: CR1a, DL5, XB2, XB3

You work in the repository root. Use relative paths only, from the repository root; never `cd` to an absolute path.
Change only `.claude/skills/workflow-design/guard/src/hooks.ts`, `.claude/skills/workflow-design/guard/src/cli.ts`,
`.claude/workflows/crossed-build-check.js`, and the progress and result files below. Do not change any test, the SPEC
or any doc. Do not commit or stage anything. Another session works in this repository: touch nothing else.

## Task
Implement the last paragraph of `.claude/skills/workflow-design/guard/SPEC.md` ("Round 20, after its review": CR1a,
DL5, XB2, XB3). The tests written from it fail now and must pass:
- `cd .claude/skills/workflow-design/guard && bun test test/round20b.test.ts`
- `node tests/workflows/crossed_build_check_harness.mjs`

## Lessons
- When a change sends new cases into an existing code path, list that path's early returns and exemptions first, and
  test each with one of the new cases.
- Keep the existing behaviour where the spec says "unchanged" or "as before": the full suite freezes it.
- Write your result file first, as `status: partial`, and update it at the end.

## Pieces and progress (first)
Pieces: `cr1a` (hooks.ts), `dl5` (cli.ts), `xb` (XB2 and XB3 in crossed-build-check.js). Append one `planned` line per
piece to `runs/20261018-finish-everything/nodes/r20b-code.progress.md`, then one line as each starts and ends:
`- <date -Iseconds> · <piece> · <planned|start|done|fail> · <note>`.

## Standard
- `cd .claude/skills/workflow-design/guard && bun test` all pass;
- `cd .claude/skills/workflow-design/guard && ./node_modules/.bin/tsgo --noEmit -p .` clean;
- `node tests/workflows/crossed_build_check_harness.mjs` all pass.

## Result
`runs/20261018-finish-everything/nodes/r20b-code.result.md`: `status: done|partial|fail`, one sentence; per piece what
changed (file and function); the three commands' last lines; CONTRADICTS (a spec line that cannot be met as written,
quoted) or none.
