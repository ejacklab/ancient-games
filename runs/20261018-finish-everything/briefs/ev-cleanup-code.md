# Brief — the evaluator removes the judge's /tmp folder after the merge (item 8)

You work in the repository root. Use relative paths. Change only `tools/evaluator/model_io.py`, the progress file and
the result file below. Do not change any test or doc. Do not commit or stage anything.

## Task
`model_io.py judged-merge` reads `judge-1.json` from the judge's folder (`_judge_folder(run)`, under `/tmp`), copies it
into the run folder, and leaves the folder behind. Make `judged_merge` remove that folder (and everything in it) once
it has read what it needs (judge-1.json copied, code quotes checked), on every path that reaches it, including when it
raises after the folder was read. A folder that does not exist is not an error. Never remove anything else: only the
path `_judge_folder(run)` returns, and only when it is a real directory (not a symlink).
`judge-input` already recreates the folder for a second attempt (F7), so nothing else changes.

The new tests fail now and must pass: `python3 -m pytest -q tests/test_evaluator_judge_cleanup.py`; every other
evaluator test keeps passing: `python3 -m pytest -q tests/test_evaluator_*.py`.

## Lessons
- When a change sends new cases into an existing code path, list that path's early returns and exemptions first, and
  test each with one of the new cases.

## Pieces and progress (first)
One piece, `cleanup`. Append `- <date -Iseconds> · cleanup · <planned|start|done|fail> · <note>` lines to
`runs/20261018-finish-everything/nodes/ev-cleanup.progress.md`.

## Result
`runs/20261018-finish-everything/nodes/ev-cleanup.result.md`: `status: done|partial|fail`, one sentence, what changed
(function), the two commands' last lines, CONTRADICTS or none.
