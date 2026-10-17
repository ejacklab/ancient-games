# Brief — the evaluator's parser reads the paragraph form (DATA.md E1 rule 9)

You work in this repository's root (a worktree on branch `fix/evaluator-parser`). **Use relative paths only; never
`cd` to an absolute path** — opencode headless auto-rejects them and stops. Change only
`tools/evaluator/spec_parse.py`, the progress file and the result file below. Do not change any test, fixture or doc.
Do not commit or stage.

## Task
Implement rule 9 of `docs/evaluator/DATA.md` § E1 (the paragraph form) in `tools/evaluator/spec_parse.py`, so that
`tests/test_evaluator_spec_parse_paragraph.py` passes (6 of its 7 fail now with "no requirement ids found") and every
other evaluator test keeps passing: `python3 -m pytest -q tests/test_evaluator_*.py`. Rules 1–8 must keep giving the
same output on their fixtures (`tests/test_evaluator_spec_parse.py` freezes it). Keep the module stdlib only.

## Lessons (from `lessons for --agent opencode --kinds code-edit`)
- When a change sends new cases into an existing code path, list that path's early returns and exemptions first, and
  test each with one of the new cases.
- opencode headless auto-rejects a command with an absolute path, even inside the repo: relative paths only.

## Pieces and progress (first)
Append one `planned` line per piece to `runs/20261018-evaluator-parser/progress.md`, then one line as each starts and
ends: `- <date -Iseconds> · <piece-id> · <planned|start|done|fail> · <note>` (piece id one word).

## Standard
`python3 -m pytest -q tests/test_evaluator_*.py` all pass.

## Result
`runs/20261018-evaluator-parser/result.md`: status, one sentence, what changed in `spec_parse.py`, the command's last
lines, CONTRADICTS (a line of rule 9 that cannot be met as written) or none.
