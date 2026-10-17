# Brief — tests-clock

You work in the repository root. Do not change any file outside the ones named under Limits. Do not commit.

## Task
Write acceptance tests in `.claude/skills/workflow-design/guard/test/round10-clock-only.test.ts` for the guard's clock
as it is now (guard `SPEC.md`, section "Round 10", T5 "Clock" and the notes after it): with a deadline recorded for the
session, every PostToolUse or PostToolUseFailure call the hooks see adds exactly one line `harness-guard clock:
<used>/<minutes> min (<percent>%), <left> left`; there is no fuller block and no reminder at 50%, 80% or 100%, and no
`raised` record for a mark; after the deadline every call adds the time-up line instead. Import `handleHook` from
`src/hooks.ts` and `startDeadline`, `claimDeadlines` from `src/deadline.ts`; use an injected clock (`env.now`), never
sleep. Read `test/round10-deadline.test.ts` only for how a temporary root and a hook payload are set up — do not copy
its assertions.

## Pieces and progress (first)
Divide the work into small pieces. Before starting, append one `planned` line per piece to
`runs/20261017-workflows/nodes/tests-clock.progress.md`, then a line as each starts and ends:
`- <ISO time from date -Iseconds> · <piece-id> · <planned|start|done|fail> · <short note>` (the piece id is one word).

## Standard
- At least: the clock at 10%, 49%, 50%, 51%, 80% and 99% of the deadline is one line and carries no mark text; no
  `deadline:<id>:<mark>` raised record is ever written; time-up after the deadline on two calls in a row; a deadline
  of another session adds nothing.
- `cd .claude/skills/workflow-design/guard && bun test test/round10-clock-only.test.ts` — report the counts.

## Limits
May change: that test file, the progress file, and `runs/20261017-workflows/nodes/tests-clock.result.md` only. No
other AI engine. Foreground commands only.

## Result
`runs/20261017-workflows/nodes/tests-clock.result.md`: `status: done|partial|fail`, one sentence; the test file; the
command and its last lines; CONTRADICTS (with the SPEC line) or none.
