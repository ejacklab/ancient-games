# Brief — tests-json

You are working in a git worktree; the current folder is the repository root. Work only inside it. Other workers are
writing other files in this worktree at the same time: touch only the files your Limits allow.

## Task

Write acceptance tests for the guard's **Round 7** (`--json` on `doctor`, `rates`, `insight`) in
`.claude/skills/workflow-design/guard/test/round7-json.test.ts`, from `.claude/skills/workflow-design/guard/SPEC.md`
Round 7 alone. Do not read or change `src/cli.ts`.

## Context

- SPEC.md Round 7 in full, and the parts it refers to (M5 doctor, Round 5 S2 rates, M3 insight, the journal record).
- How the existing CLI tests run the CLI in a temporary root: `test/cli.test.ts` (read it for the helper pattern).
- bun 1.4.3, TypeScript, no npm dependencies. bun pitfall: in `test.each` tables wrap each element in its own array.

## Standard

- Every Round 7 Fails-if line has a test with a planted root (journal records, insight files): JSON parses and has
  each field; `insight --json` exits 1 with an open failure and 0 without; text output and exit code unchanged without
  `--json`; no file under the root changes (hash the tree before and after).
- `cd .claude/skills/workflow-design/guard && bun test test/round7-json.test.ts` and `./node_modules/.bin/tsgo --noEmit -p .`
  — report counts and any type error in your file.

## Limits

- May change: `.claude/skills/workflow-design/guard/test/round7-json.test.ts` only; plus your result file. Nothing
  else. Do not commit. No other AI engine. Foreground commands only.

## Result

Write `runs/20261016-integrate-r11-r13/nodes/tests-json.result.md` first as `status: partial`, update it at the end:
`status: done|partial|fail`, one sentence; files; commands and last lines; CONTRADICTS (with the SPEC line) or none.
