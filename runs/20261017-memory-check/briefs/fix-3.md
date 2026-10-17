# Brief — memory-check enhance round

You work in the repository root. **Use relative paths only, from the repository root; never `cd` to an absolute
path** — opencode headless auto-rejects them and stops with no work done. Change only `memory_check/src/`, the
progress file and the result file below. Do not change any test, the four docs or the guidelines. Do not commit or
stage anything.

## Task
Make `memory_check/test/enhance.test.ts` pass (4 tests, failing now) while `acceptance.test.ts` and
`review.test.ts` keep passing. The requirements, changed today: `memory_check/REQUIREMENTS.md` R1 and R2,
`memory_check/USE_CASES.md` U3.

1. **R1, Not applicable section:** every "not applicable" result is printed in a last section headed exactly
   `## Not applicable`, and nowhere else; each keeps its own row in the same row format as now.
2. **R1, unstaged count:** a line `<N> files under project-memory/ changed but not staged` — modified, deleted or
   untracked files under `project-memory/` that the staged snapshot does not hold (`git status --porcelain --
   project-memory`, read only, with `GIT_OPTIONAL_LOCKS=0`); 0 when there are none.
3. **R2/U3:** the warning (`--warn`) has one line for every MUST that fails **or could not run** (now it holds only
   fails), plus a missing `AGENTS.md`; still never entry text.

## Lessons (from `lessons for --agent opencode --kinds code-edit`)
- When a change sends new cases into an existing code path, list that path's early returns and exemptions first, and
  test each with one of the new cases.
- opencode headless auto-rejects a command with an absolute path, even inside the repo: relative paths only.

## Pieces and progress (first)
One piece per numbered item. Before starting, append one `planned` line per piece to
`runs/20261017-memory-check/nodes/fix-3.progress.md`, then one line as each starts and ends:
`- <ISO time from date -Iseconds> · <piece-id> · <planned|start|done|fail> · <short note>` (the piece id is one word).

## Standard
- `cd memory_check && bun test` — all tests of the three files pass; `cd memory_check && ./node_modules/.bin/tsgo --noEmit -p .` clean.

## Limits
May change: `memory_check/src/**`, the progress file, and `runs/20261017-memory-check/nodes/fix-3.result.md`. No other
AI engine. Foreground commands only.

## Result
`runs/20261017-memory-check/nodes/fix-3.result.md`: `status: done|partial|fail`, one sentence; per item what changed;
the test and typecheck commands with their last lines; CONTRADICTS or none.
