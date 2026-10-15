# Brief — tests-hooks6

You are working in a git worktree; the current folder is the repository root. Work only inside it. Other workers are
writing other files in this worktree at the same time: touch only the files your Limits allow.

## Task

Write acceptance tests for Round 6 **K2 and K3** in `.claude/skills/workflow-design/guard/test/round6-hooks.test.ts`, from SPEC.md alone: drive `handleHook(payload, env)` (UserPromptSubmit, PostToolUse Write on a criteria file, Stop) with a temporary git repo, check the journal with `readJournal`, and the path skeleton with `skeleton` from `src/paths.ts`. The code is being written now by a different engine; read `src/` only for existing names and signatures.

## Context

- `.claude/skills/workflow-design/guard/SPEC.md` — read **Round 6 — the score** in full, and the parts it refers to (M4 register/units, Round 5 S1/S5,
  D6 raised records, the journal).
- `.claude/skills/workflow-design/guard/src/types.ts` — fixed (Round 6 types are there). Import them; never change the file.
- bun 1.4.3, TypeScript, no npm dependencies. bun pitfall: in `test.each` tables wrap each element in its own array.

## Standard

- Every K2/K3 Fails-if line has a test; run `bun test test/round6-hooks.test.ts` and report counts.
- `cd .claude/skills/workflow-design/guard && ./node_modules/.bin/tsgo --noEmit -p .` — no error in your files (report others').
- Never put request text, criterion text, command text or output into anything the guard writes or prints beyond what
  SPEC names (plant `SECRET-PLANT-7f3a9c` where it applies).

## Limits

- May change: `.claude/skills/workflow-design/guard/test/round6-hooks.test.ts` only; plus your result file. Nothing else. Do not commit. No other AI engine. Foreground commands only.

## Result

Write `runs/20261015-score/nodes/tests-hooks6.result.md` first as `status: partial`, update it at the end: one sentence; files;
commands and last lines; CONTRADICTS (with the SPEC line) or none.
