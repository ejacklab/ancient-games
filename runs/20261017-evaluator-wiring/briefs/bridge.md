# Brief — the evaluator's verdict reaches the guard (guard SPEC Round 19)

You work in the repository root. **Use relative paths only; never `cd` to an absolute path** — opencode headless
auto-rejects them and stops. Change only `.claude/skills/workflow-design/guard/src/**` (a new `src/evaluation.ts` and
the `evaluation` command in `src/cli.ts`), the progress file and the result file below. Do not change any test or
`SPEC.md`. Do not commit or stage. Time is short: about 15 minutes.

## Task
Implement SPEC Round 19 (`.claude/skills/workflow-design/guard/SPEC.md`, the last section, V1–V5) so that
`.claude/skills/workflow-design/guard/test/round19-evaluation.test.ts` passes (7 tests, failing now with a usage
error). Record failures with the guard's own journal functions (`src/journal.ts`: `appendFailure`, `newFailureId`,
`writeEvidence`, `guardRoot`), the way `src/cli.ts` `fail` does; once-per-verdict by a hash of the file's bytes.

## Lessons (from `lessons for --agent opencode --kinds code-edit`)
- When a change sends new cases into an existing code path, list that path's early returns and exemptions first, and
  test each with one of the new cases.
- Relative paths only.

## Pieces and progress (first)
Append one `planned` line per piece to `runs/20261017-evaluator-wiring/nodes/bridge.progress.md`, then one line as
each starts and ends: `- <date -Iseconds> · <piece-id> · <planned|start|done|fail> · <note>` (piece id one word).

## Standard
`cd .claude/skills/workflow-design/guard && bun test` all pass; `./node_modules/.bin/tsgo --noEmit -p .` clean.

## Result
`runs/20261017-evaluator-wiring/nodes/bridge.result.md`: status, one sentence, files changed, the two commands' last
lines, CONTRADICTS or none.
