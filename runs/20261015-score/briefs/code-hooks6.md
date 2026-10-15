# Brief — code-hooks6

You are working in a git worktree; the current folder is the repository root. Work only inside it. Other workers are
writing other files in this worktree at the same time: touch only the files your Limits allow.

## Task

Implement Round 6 **K2 and K3**: `src/hooks.ts` (UserPromptSubmit reminder, touched records for criteria files, the Stop criteria step), `src/install.ts` (UserPromptSubmit in the snippet), `src/cli.ts` (`criteria new|score`), `src/paths.ts` (`skeleton` fills `measures.score`). Use the K1 exports from `src/criteria.ts`, which another worker is writing now with the signatures SPEC K1 gives. Tests are being written at the same time by a different engine.

## Context

- `.claude/skills/workflow-design/guard/SPEC.md` — read **Round 6 — the score** in full, and the parts it refers to (M4 register/units, Round 5 S1/S5,
  D6 raised records, the journal).
- `.claude/skills/workflow-design/guard/src/types.ts` — fixed (Round 6 types are there). Import them; never change the file.
- bun 1.4.3, TypeScript, no npm dependencies. bun pitfall: in `test.each` tables wrap each element in its own array.

## Standard

- `cd .claude/skills/workflow-design/guard && bun test` — every existing test still passes (1078), except where Round 6 changes behaviour (e.g. the install snippet's event list): report each such test by name; round-6 hooks tests that exist when you finish: report counts. Follow SPEC.md, not a test.
- `cd .claude/skills/workflow-design/guard && ./node_modules/.bin/tsgo --noEmit -p .` — no error in your files (report others').
- Never put request text, criterion text, command text or output into anything the guard writes or prints beyond what
  SPEC names (plant `SECRET-PLANT-7f3a9c` where it applies).

## Limits

- May change: `.claude/skills/workflow-design/guard/src/hooks.ts`, `.claude/skills/workflow-design/guard/src/install.ts`, `.claude/skills/workflow-design/guard/src/cli.ts`, `.claude/skills/workflow-design/guard/src/paths.ts`; plus your result file. Nothing else. Do not commit. No other AI engine. Foreground commands only.

## Result

Write `runs/20261015-score/nodes/code-hooks6.result.md` first as `status: partial`, update it at the end: one sentence; files;
commands and last lines; CONTRADICTS (with the SPEC line) or none.
