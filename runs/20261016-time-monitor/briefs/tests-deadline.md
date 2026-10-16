# Brief — tests-deadline

You work in the repository root. Another worker is writing `src/deadline.ts`, `src/hooks.ts` and `src/cli.ts` at the
same time: do not read or change them.

## Task
Write acceptance tests for guard **Round 10** (T1–T6) in `.claude/skills/workflow-design/guard/test/round10-deadline.test.ts`,
from `.claude/skills/workflow-design/guard/SPEC.md` Round 10 alone (and the parts it names: K2 reminder, `raised`
records, hook payloads as in `test/round9-warnings.test.ts`). Types are fixed in `src/types.ts` (`Deadline`,
`ProgressSummary`). Import `handleHook` from `src/hooks.ts` and the module's functions from `src/deadline.ts`:
`startDeadline(root, { minutes, run, marks }, now): Deadline`, `deadlineStatus(root, session, now)`,
`progressSummary(file, now): ProgressSummary`. Use an injected clock (`env.now`) for every time; never sleep in a test
except one CLI `deadline wait` test with a deadline a few seconds long.

## Pieces and progress (do this first)
Divide the work into small pieces (one per Fails-if line is fine). Before you start, append one `planned` line per
piece to `runs/20261016-time-monitor/nodes/tests-deadline.progress.md`, then one line when each piece starts and when it
is done or fails, in this exact form (get the time with `date -Iseconds`):
`- <ISO time> · <piece id> · <planned|start|done|fail> · <short note>`

## Standard
- Every Round 10 Fails-if line has a test with a planted input.
- `cd .claude/skills/workflow-design/guard && bun test test/round10-deadline.test.ts` (failures expected until the
  code lands) and `./node_modules/.bin/tsgo --noEmit -p .` — report counts and type errors in your file.

## Limits
May change: the test file, the progress file, and your result file only. Do not commit. No other AI engine.
Foreground commands only. Stop by 11:05 +0800 whatever state you are in, and say so in the result.

## Result
`runs/20261016-time-monitor/nodes/tests-deadline.result.md`: `status: done|partial|fail`, one sentence; files; commands
and last lines; CONTRADICTS (with the SPEC line) or none.
