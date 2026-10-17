# Brief — fix the memory-check tools against the accepted review findings (TAG)

You work in the repository root. **Use relative paths only, from the repository root; never `cd` to an absolute
path** — opencode headless auto-rejects them and stops with no work done. Change only `memory_check/src/**` and
`tools/memory_index.py`, the progress file and the result file below. Do not change any test, any doc or the
guidelines. Do not commit or stage anything.

## Task
Make the failing tests pass — one test per accepted finding listed below, each failing now for the reason the finding
names — while every other test keeps passing.

Tests: TESTFILES

Accepted findings:
FINDINGS

## Lessons (from `lessons for --agent opencode --kinds code-edit`)
- When a change sends new cases into an existing code path, list that path's early returns and exemptions first, and
  test each with one of the new cases.
- opencode headless auto-rejects a command with an absolute path, even inside the repo: relative paths only.

## Pieces and progress (first)
One piece per finding. Before starting, append one `planned` line per piece to
`runs/20261018-finish-everything/nodes/mc-fix-TAG.progress.md`, then one line as each starts and ends:
`- <ISO time from date -Iseconds> · <piece-id> · <planned|start|done|fail> · <short note>` (the piece id is one word).

## Standard
`cd memory_check && bun test` passes; `python3 -m pytest -q tests/test_memory_index*.py` passes;
`cd memory_check && ./node_modules/.bin/tsgo --noEmit -p .` is clean.

## Result
`runs/20261018-finish-everything/nodes/mc-fix-TAG.result.md`: `status: done|partial|fail`, one sentence; per finding
what changed (file and function); the test and typecheck commands with their last lines; CONTRADICTS (a finding that
cannot be fixed without breaking a requirement, with the id) or none.
