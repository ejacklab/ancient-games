# ev-cleanup result

status: done

The evaluator's judge folder under /tmp is now removed by `judged_merge` on every path that reaches it, including the two that raise after the folder is read.

## What changed

- `tools/evaluator/model_io.py` — new `_remove_judge_folder(folder)` (model_io.py:247): removes the path only when it is a real directory, never a symlink, and a missing path is nothing.
- `judged_merge` (model_io.py:364) — the block that needs the folder (`_require_model_file` for call 1 and, with a plant, call 2; `_read_json` of `judge-1.json`; the copy into the run folder; the code-quote check against `folder/product`) now runs inside `try:` with `_remove_judge_folder(folder)` in `finally:`. Nothing else moved; the no-rows path still never touches the folder, and `judge-input` still recreates it for attempt 2.

## Commands

- `python3 -m pytest -q tests/test_evaluator_judge_cleanup.py` → `7 passed in 0.47s`
- `python3 -m pytest -q tests/test_evaluator_*.py` → `191 passed in 52.07s`

## CONTRADICTS

none.