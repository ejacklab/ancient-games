# Brief — the bridge, round 3b: the baseline compares FAIL cases (guard SPEC Round 19, "V7, by case")

You work in the repository root. **Use relative paths only.** Change only
`.claude/skills/workflow-design/guard/src/evaluation.ts` (and `src/cli.ts` for the `--baseline` flag), the progress
file and the result file below. Do not change any test or `SPEC.md`. Do not commit or stage. About 10 minutes.

## Task
Implement "V7, by case" (the last bullet of SPEC Round 19) so that every test in
`.claude/skills/workflow-design/guard/test/round19-evaluation.test.ts` passes (1 fails now: "V7: a new FAIL case in a group
that already failed in the baseline is still a failure"): a group FAIL in the baseline too is a note only when every
one of its FAIL cases was FAIL in the baseline; a case belongs to the group its id starts with (`B1-F1` → `B1`).


## Lessons (from `lessons for --agent mcode --kinds code-edit`)
- When a change sends new cases into an existing code path, list that path's early returns and exemptions first, and
  test each with one of the new cases.

## Pieces and progress (first)
Append one `planned` line per piece to `runs/20261017-evaluator-wiring/nodes/bridge-3.progress.md`, then one line as
each starts and ends: `- <date -Iseconds> · <piece-id> · <planned|start|done|fail> · <note>` (piece id one word).

## Standard
`cd .claude/skills/workflow-design/guard && bun test` all pass; `./node_modules/.bin/tsgo --noEmit -p .` clean.

## Result
`runs/20261017-evaluator-wiring/nodes/bridge-3.result.md`: status, one sentence, files changed, both commands' last
lines, CONTRADICTS or none.
