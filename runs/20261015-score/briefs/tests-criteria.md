# Brief — tests-criteria

You are working in a git worktree; the current folder is the repository root. Work only inside it. Other workers are
writing other files in this worktree at the same time: touch only the files your Limits allow.

## Task

Write acceptance tests for Round 6 **K1** (`src/criteria.ts`) in `.claude/skills/workflow-design/guard/test/round6-criteria.test.ts`, from SPEC.md alone; the module is being written now by a different engine — do not read it. Temporary folders for files.

## Context

- `.claude/skills/workflow-design/guard/SPEC.md` — read **Round 6 — the score** in full, and the parts it refers to (M4 register/units, Round 5 S1/S5,
  D6 raised records, the journal).
- `.claude/skills/workflow-design/guard/src/types.ts` — fixed (Round 6 types are there). Import them; never change the file.
- bun 1.4.3, TypeScript, no npm dependencies. bun pitfall: in `test.each` tables wrap each element in its own array.

## Standard

- Every K1 Fails-if line has a test with a planted file; run `bun test test/round6-criteria.test.ts` and report counts (failures expected until the code lands).
- `cd .claude/skills/workflow-design/guard && ./node_modules/.bin/tsgo --noEmit -p .` — no error in your files (report others').
- Never put request text, criterion text, command text or output into anything the guard writes or prints beyond what
  SPEC names (plant `SECRET-PLANT-7f3a9c` where it applies).

## Limits

- May change: `.claude/skills/workflow-design/guard/test/round6-criteria.test.ts` only; plus your result file. Nothing else. Do not commit. No other AI engine. Foreground commands only.

## Result

Write `runs/20261015-score/nodes/tests-criteria.result.md` first as `status: partial`, update it at the end: one sentence; files;
commands and last lines; CONTRADICTS (with the SPEC line) or none.
