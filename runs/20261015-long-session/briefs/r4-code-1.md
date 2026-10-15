# Brief — r4-code, attempt 1

You are working in a git worktree; the current folder is the repository root. Work only inside it.

## Task

Change `.claude/skills/workflow-design/guard/src/` so the package meets **Round 4** at the end of
`.claude/skills/workflow-design/guard/SPEC.md` (D1–D5) and every test passes. The new tests are
`.claude/skills/workflow-design/guard/test/round4.test.ts` (written by a different engine from SPEC.md) and are frozen.

## Standard

- `cd .claude/skills/workflow-design/guard && bun test` — every test passes (918 now; 76 fail before your change).
- `cd .claude/skills/workflow-design/guard && ./node_modules/.bin/tsgo --noEmit -p .` — exit 0.
- Where a test and SPEC.md disagree, do not bend the code to the test: report it under CONTRADICTS.
- No test output text, prompt or command text in anything the guard writes or prints (tests plant `SECRET-PLANT-7f3a9c`).
- `src/types.ts` is fixed; report a needed type change instead of making it.

## Limits

- May change: files under `.claude/skills/workflow-design/guard/src/` only; plus the result and evidence files.
- Must not change: `test/`, `SPEC.md`, `src/types.ts`, `data/`, anything else. Do not commit. No other AI engine.
  Run checks in the foreground.

## Write the result to

`runs/20261015-long-session/nodes/r4-code-1.result.md` — write it **first** as `status: partial` and update it at
the end, so a stop leaves a trace. Header: node r4-code · attempt 1 · engine opencode · model · status · started ·
ended · evidence: runs/20261015-long-session/nodes/r4-code-1.evidence.txt. Body: one sentence; files written; the two
check commands and their last lines; CONTRADICTS (each, or none).
