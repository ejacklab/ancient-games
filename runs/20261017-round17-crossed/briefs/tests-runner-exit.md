# Brief — tests-runner-exit

You work in the repository root. Do not change any file outside the ones named under Limits. Do not commit.

## Task
Write acceptance tests in `.claude/skills/workflow-design/guard/test/round17-crossed.test.ts` for the guard's rule
"a test failure only when the runner made the exit" as the guard's `SPEC.md` states it: section "Round 17" (V1, V2
and its Fails-if line), read together with "Round 4" D1 and D2 (what `R12.2-test-failed` and `R12.2-command-error`
records hold) and "Round 9" (a guess is a `warning` record, not a `failure`).

Import `handleHook` from `src/hooks.ts` and `readJournal` from `src/journal.ts`. Feed the hook
`PostToolUseFailure` payloads for Bash (`error: "Exit code N\n<output>"`) and, where a case needs it, `PostToolUse`
payloads with a `tool_response` of stdout and stderr. Read `test/round4.test.ts` only for how a temporary git root, the
`HookEnv` and a payload are set up; do not copy its assertions. Do not open `test/round17-runner-exit.test.ts`.

## Pieces and progress (first)
Divide the work into small pieces. Before starting, append one `planned` line per piece to
`runs/20261017-round17-crossed/nodes/tests-runner-exit.progress.md`, then a line as each starts and ends:
`- <ISO time from date -Iseconds> · <piece-id> · <planned|start|done|fail> · <short note>` (the piece id is one word).

## Standard
- Cover at least: a test runner followed by `;` and another command that exits non-zero, with no failure summary; a
  runner followed by `&&` and another command; a runner followed by `||`; a runner piped to `tail` or `grep`; a runner
  that is last after `cd … &&`; two runners where the last one is last; a runner that is not last but whose output
  holds a failure summary; M1's wrappers (`timeout 60 …`, `env -u NO_COLOR …`) on a runner that is not last.
- For each case assert which record kind is written (`failure` or `warning`), its `check`, its `input` and its `actual`,
  and that no other failure or warning is written.
- `cd .claude/skills/workflow-design/guard && bun test test/round17-crossed.test.ts` — report the counts.

## Limits
May change: that test file, the progress file, and `runs/20261017-round17-crossed/nodes/tests-runner-exit.result.md`
only. No other AI engine. Foreground commands only.

## Result
`runs/20261017-round17-crossed/nodes/tests-runner-exit.result.md`: `status: done|partial|fail`, one sentence; the test
file; the command and its last lines; CONTRADICTS (with the SPEC line) or none.
