# Brief — code-health

You are working in a git worktree; the current folder is the repository root. Work only inside it. Other workers are
writing other files in this worktree at the same time: touch only the files your Limits allow.

## Task

Implement `runs/20261016-integrate-r11-r13/spec-harness-health.md` (H1–H5) in
`.claude/skills/workflow-design/scripts/harness_health.py`. Tests for it are being written now by a different engine
from the spec; do not write tests.

## Context

- The spec above, in full. The guard commands it calls are specified in `.claude/skills/workflow-design/guard/SPEC.md`,
  section **Round 7** (already implemented: try `bun .claude/skills/workflow-design/guard/src/cli.ts doctor --json`,
  `rates --json`, `insight --json`).
- The current `harness_health.py` and `readiness.py` beside it (reuse `CMD_TIMEOUT`, the status constants and
  `Where.show`). Python 3.11+, standard library only.
- Match the file's style: short functions, the existing comment density, `Finding`/`Help` as they are.

## Standard

- `python3 .claude/skills/workflow-design/scripts/harness_health.py` and `--json` run and show the new lines;
  `--self-test` still passes.
- `env -u NO_COLOR python3 -m pytest -q tests/test_harness_health.py` — report the counts. Old tests that assert
  the ten-row table or R10 for hooks are expected to fail until the test writer updates them; name them.
- Never print a guard command's raw output; never write a file; never let a guard failure raise.

## Limits

- May change: `.claude/skills/workflow-design/scripts/harness_health.py` only; plus your result file. Nothing else.
  Do not commit. No other AI engine. Foreground commands only.

## Result

Write `runs/20261016-integrate-r11-r13/nodes/code-health.result.md` first as `status: partial`, update it at the end:
`status: done|partial|fail`, one sentence; files; commands and last lines; CONTRADICTS (with the spec line) or none.
