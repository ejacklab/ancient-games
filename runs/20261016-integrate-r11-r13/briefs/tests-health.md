# Brief — tests-health

You are working in a git worktree; the current folder is the repository root. Work only inside it. Other workers are
writing other files in this worktree at the same time: touch only the files your Limits allow.

## Task

Write acceptance tests for `runs/20261016-integrate-r11-r13/spec-harness-health.md` (H1–H5) in
`tests/test_harness_health.py`, from the spec alone: new tests named `test_hh_18_…` onward, and update the existing
tests only where the spec changes what they assert (the ten-row table, `## Ten requirements`, hooks as R10). The code
is being written now by a different engine — do not read the new parts of `harness_health.py` beyond what the old tests
already use, and do not change it.

## Context

- The spec, in full; the guard's Round 7 in `.claude/skills/workflow-design/guard/SPEC.md` (the JSON shapes).
- The existing test file: its `box` fixture (isolated HOME, a `bin` folder as the whole PATH, fake executables).
- A fake `bun` in `box.bin` lets you plant each guard answer: a script that reads its argv (`… cli.ts doctor --json`)
  and prints planted JSON with a planted exit code, or sleeps past the timeout, or prints non-JSON. The guard's
  location is fixed by the spec (`scripts/../guard/src/cli.ts`); for the "guard missing" case use `hh.gather` with a
  temporary `scripts` folder, as HH-06 does.
- One test with the **real** guard when `bun` is installed on this machine (skip otherwise): put the real bun's folder
  on the box PATH, run against an empty project and a project with a planted `.harness-guard/journal.jsonl` holding one
  failure record, and assert the open-failure line and that no file under HOME or the project changed (`tree_hash`).

## Standard

- Every spec Fails-if line has a test with a planted input (plant `SECRET-PLANT-7f3a9c` in guard output to prove raw
  output never reaches the report).
- `env -u NO_COLOR python3 -m pytest -q tests/test_harness_health.py` — report counts (failures expected until the
  code lands; say which).

## Limits

- May change: `tests/test_harness_health.py` only; plus your result file. Nothing else. Do not commit. No other AI
  engine. Foreground commands only.

## Result

Write `runs/20261016-integrate-r11-r13/nodes/tests-health.result.md` first as `status: partial`, update it at the end:
`status: done|partial|fail`, one sentence; files; commands and last lines; CONTRADICTS (with the spec line) or none.
