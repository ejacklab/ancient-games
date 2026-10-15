# Brief — tests-insight

You are working in a git worktree; the current folder is the repository root. Work only inside it. Other workers are
writing other files in this worktree at the same time: touch only the files your Limits allow.

## Task

Write acceptance tests for Round 5 **S4** (great-success sections in `src/insight.ts`: parseInsight, checkGreatSection, greatAnswered) in `.claude/skills/workflow-design/guard/test/round5-insight.test.ts`, from SPEC.md alone. The code is being written now by a different engine; read `src/insight.ts` only for existing exports, never to shape expectations.

## Context

- `.claude/skills/workflow-design/guard/SPEC.md` — read **Round 5 — learn from success** in full, and the earlier parts it refers to (M1 traps, M2
  journal, M3 insight, M5 hooks, D1/D3/D6 in Round 4).
- `.claude/skills/workflow-design/guard/src/types.ts` — fixed (Round 5 types are already there). Import them; never change the file.
- Runtime: bun 1.4.3, TypeScript, no npm dependencies. bun pitfall: in `test.each` tables wrap each element in its own
  array (`[[x]]`), or bun takes the parameter as a `done` callback and times out.

## Standard

- Every S4 Fails-if line has a test; a file holding both a failure section and a great section keeps them apart; run `bun test test/round5-insight.test.ts` and report the counts.
- `cd .claude/skills/workflow-design/guard && ./node_modules/.bin/tsgo --noEmit -p .` — no error in your files (errors in files other workers have not
  finished yet are not yours: report them).
- Never put command text, prompt text or test output into anything the guard writes or prints (plant
  `SECRET-PLANT-7f3a9c` in a test where it applies).

## Limits

- May change: `.claude/skills/workflow-design/guard/test/round5-insight.test.ts` only; plus your result file.
- Must not change anything else. Do not commit. Do not start another AI engine. Run commands in the foreground.

## Result

Write `runs/20261015-learn-success/nodes/tests-insight.result.md` first as `status: partial`, and update it at the end: one
sentence; files written; the commands you ran and their last lines; CONTRADICTS (where SPEC.md cannot be met or
contradicts itself, with the line), or none.
