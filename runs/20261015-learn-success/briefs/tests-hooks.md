# Brief — tests-hooks

You are working in a git worktree; the current folder is the repository root. Work only inside it. Other workers are
writing other files in this worktree at the same time: touch only the files your Limits allow.

## Task

Write acceptance tests for Round 5 **S1, S2 and S5** in `.claude/skills/workflow-design/guard/test/round5-hooks.test.ts`, from SPEC.md alone. The code is being written now by a different engine; read `src/` only for existing function names and signatures (`handleHook`, `HookEnv`, `readJournal`), never to shape expectations. Drive hooks through `handleHook(payload, env)` with a temporary git repo (`fs.mkdtempSync(path.join(os.tmpdir(), "hg-"))` + `git init`); `rates` is imported from `../src/rates.ts`.

## Context

- `.claude/skills/workflow-design/guard/SPEC.md` — read **Round 5 — learn from success** in full, and the earlier parts it refers to (M1 traps, M2
  journal, M3 insight, M5 hooks, D1/D3/D6 in Round 4).
- `.claude/skills/workflow-design/guard/src/types.ts` — fixed (Round 5 types are already there). Import them; never change the file.
- Runtime: bun 1.4.3, TypeScript, no npm dependencies. bun pitfall: in `test.each` tables wrap each element in its own
  array (`[[x]]`), or bun takes the parameter as a `done` callback and times out.

## Standard

- Every S1/S2/S5 Fails-if line has a test with a planted input; run `bun test test/round5-hooks.test.ts` and report the counts (failures are expected until the code lands).
- `cd .claude/skills/workflow-design/guard && ./node_modules/.bin/tsgo --noEmit -p .` — no error in your files (errors in files other workers have not
  finished yet are not yours: report them).
- Never put command text, prompt text or test output into anything the guard writes or prints (plant
  `SECRET-PLANT-7f3a9c` in a test where it applies).

## Limits

- May change: `.claude/skills/workflow-design/guard/test/round5-hooks.test.ts` only; plus your result file.
- Must not change anything else. Do not commit. Do not start another AI engine. Run commands in the foreground.

## Result

Write `runs/20261015-learn-success/nodes/tests-hooks.result.md` first as `status: partial`, and update it at the end: one
sentence; files written; the commands you ran and their last lines; CONTRADICTS (where SPEC.md cannot be met or
contradicts itself, with the line), or none.
