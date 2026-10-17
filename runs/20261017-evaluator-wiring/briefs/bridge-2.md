# Brief — the bridge, round 3: one failure per group, and a baseline (guard SPEC Round 19, V6 and V7)

You work in the repository root. **Use relative paths only.** Change only
`.claude/skills/workflow-design/guard/src/evaluation.ts` (and `src/cli.ts` for the `--baseline` flag), the progress
file and the result file below. Do not change any test or `SPEC.md`. Do not commit or stage. About 10 minutes.

## Task
Implement V6 and V7 of SPEC Round 19 (`.claude/skills/workflow-design/guard/SPEC.md`, the paragraph "Round 19, after
measuring") so that every test in `.claude/skills/workflow-design/guard/test/round19-evaluation.test.ts` passes (3 fail
now: V1, V6, V7). V6: one failure per failing group, check `evaluator:<group>`, input the group's FAIL ids joined by
", ". V7: `--baseline <verdict.json>` — a group FAIL in the baseline too is a note `- <group> · FAIL in the baseline
too · <ids>`, not a failure.

## Lessons (from `lessons for --agent mcode --kinds code-edit`)
- When a change sends new cases into an existing code path, list that path's early returns and exemptions first, and
  test each with one of the new cases.

## Pieces and progress (first)
Append one `planned` line per piece to `runs/20261017-evaluator-wiring/nodes/bridge-2.progress.md`, then one line as
each starts and ends: `- <date -Iseconds> · <piece-id> · <planned|start|done|fail> · <note>` (piece id one word).

## Standard
`cd .claude/skills/workflow-design/guard && bun test` all pass; `./node_modules/.bin/tsgo --noEmit -p .` clean.

## Result
`runs/20261017-evaluator-wiring/nodes/bridge-2.result.md`: status, one sentence, files changed, both commands' last
lines, CONTRADICTS or none.
