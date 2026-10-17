# Brief — review the memory-check tools (read-only)

Review two tools in this repository (the current folder is its root). **Do not change any file; do not run shell
commands that write; your final message is the review.** Use relative paths only.

- `memory_check/` — TypeScript: `memory_check/src/`, its tests `memory_check/test/`.
- `tools/memory_index.py` — Python, which `memory_check` runs for its index checks; its tests
  `tests/test_memory_index.py`, `tests/test_memory_index_unit.py`.

## The judge
`memory_check/VISION.md`, `memory_check/USE_CASES.md` (U1–U6), `memory_check/REQUIREMENTS.md` (F, C, R, T ids), and,
for `memory_index.py`, the requirement ids it checks in `docs/memory-system/SOURCE_OF_TRUTH_REQUIREMENTS.yaml`
(K6.1a, K6.2, K6.3a, W1.1a/b, W1.2a, W1.3a, W4.1b, Rd3.1a). **A finding counts only if it names the use case or
requirement id it breaks and the input that shows it.** Do not propose new features; do not repeat a finding already
listed in `runs/20261017-memory-check-review/findings.md` (accepted or dropped) if that file exists.

## Lessons (from `lessons for --agent codex --kinds code-edit,test`)
- When a change sends new cases into an existing code path, list that path's early returns and exemptions first, and
  test each with one of the new cases.
- A known answer must be computed by a different method from the rule under test.

## Return
`status: done`, then a heading `## Findings` with one numbered finding per defect: severity (P1 wrong answer, P2
other), file:line, the requirement or use case id broken, the input that shows it, the fix in one line. Then
"Checked and found nothing" for each area that is clean. If you find nothing, write `## Findings` and `none`.
