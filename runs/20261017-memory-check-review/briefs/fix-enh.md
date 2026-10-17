# Brief — fix the memory-check tools, round enh

You work in the repository root. **Use relative paths only, from the repository root; never `cd` to an absolute
path** — opencode headless auto-rejects them and stops with no work done. Change only `memory_check/src/**` and
`tools/memory_index.py`, the progress file and the result file below. Do not change any test, any doc or the
guidelines. Do not commit or stage anything.

## Task
Make `memory_check/test/review-enh.test.ts` pass — one test per accepted finding of `runs/20261017-memory-check-review/enhance.md`,
each failing now for the reason the finding names — while every other test keeps passing:
`cd memory_check && bun test`, and `python3 -m pytest -q tests/test_memory_index.py tests/test_memory_index_unit.py`.

## Lessons (from `lessons for --agent opencode --kinds code-edit`)
- When a change sends new cases into an existing code path, list that path's early returns and exemptions first, and
  test each with one of the new cases.
- opencode headless auto-rejects a command with an absolute path, even inside the repo: relative paths only.

## Pieces and progress (first)
One piece per finding. Before starting, append one `planned` line per piece to
`runs/20261017-memory-check-review/nodes/fix-enh.progress.md`, then one line as each starts and ends:
`- <ISO time from date -Iseconds> · <piece-id> · <planned|start|done|fail> · <short note>` (the piece id is one word).

## Standard
Both test commands pass; `cd memory_check && ./node_modules/.bin/tsgo --noEmit -p .` is clean.

## Result
`runs/20261017-memory-check-review/nodes/fix-enh.result.md`: `status: done|partial|fail`, one sentence; per finding
what changed (file and function); the test and typecheck commands with their last lines; CONTRADICTS or none.
