# Brief — code-paths

You are working in a git worktree; the current folder is the repository root. Work only inside it. Other workers are
writing other files in this worktree at the same time: touch only the files your Limits allow.

## Task

Implement Round 5 **S3** in a new file `src/paths.ts` with exactly the exports and signatures SPEC S3 gives (`findPathFiles`, `loadPath`, `PathError`, `checkPath`, `skeleton`, `parents`). Another worker wires the CLI and the Stop hook to these exports; tests are being written at the same time by a different engine in `test/round5-paths.test.ts`.

## Context

- `.claude/skills/workflow-design/guard/SPEC.md` — read **Round 5 — learn from success** in full, and the earlier parts it refers to (M1 traps, M2
  journal, M3 insight, M5 hooks, D1/D3/D6 in Round 4).
- `.claude/skills/workflow-design/guard/src/types.ts` — fixed (Round 5 types are already there). Import them; never change the file.
- Runtime: bun 1.4.3, TypeScript, no npm dependencies. bun pitfall: in `test.each` tables wrap each element in its own
  array (`[[x]]`), or bun takes the parameter as a `done` callback and times out.

## Standard

- `cd .claude/skills/workflow-design/guard && bun test` — every test that existed before this round still passes; round-5 path tests that exist when you finish: report their counts.\n- Follow SPEC.md, not a test: where a test and SPEC disagree, report it.
- `cd .claude/skills/workflow-design/guard && ./node_modules/.bin/tsgo --noEmit -p .` — no error in your files (errors in files other workers have not
  finished yet are not yours: report them).
- Never put command text, prompt text or test output into anything the guard writes or prints (plant
  `SECRET-PLANT-7f3a9c` in a test where it applies).

## Limits

- May change: `.claude/skills/workflow-design/guard/src/paths.ts` (new) only; plus your result file.
- Must not change anything else. Do not commit. Do not start another AI engine. Run commands in the foreground.

## Result

Write `runs/20261015-learn-success/nodes/code-paths.result.md` first as `status: partial`, and update it at the end: one
sentence; files written; the commands you ran and their last lines; CONTRADICTS (where SPEC.md cannot be met or
contradicts itself, with the line), or none.
