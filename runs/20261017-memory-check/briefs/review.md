# Brief — review memory-check v1 (read-only)

Review the tool in `memory_check/` in this repository (the current folder is its root). Do not change any file; your
final message is the review.

The change: `git diff dd12aed..eb3b899 -- memory_check` — or simply read `memory_check/src/` as it stands; the
specification is `memory_check/REQUIREMENTS.md` and `memory_check/USE_CASES.md`, the guidelines it checks are
`docs/memory-system/SOURCE_OF_TRUTH_REQUIREMENTS.yaml` and `docs/memory-system/CACHES.md`.

## Lessons (from `lessons for --agent dsh --kinds code-edit,test`)
- When a change sends new cases into an existing code path, list that path's early returns and exemptions first, and
  test each with one of the new cases.

Find defects: a requirement of the guidelines reported pass or fail when the tool cannot decide it, or the reverse;
a result without evidence; a write anywhere but `--out` (F3); a path or git call that reads the wrong snapshot (C5);
`memory_index.py` output parsed in a way that loses a failure (C3); the warning holding anything but failing MUSTs and
a missing `AGENTS.md` (R2); a wrong exit code (R3); a spec line the code does not do, or a contradiction between two
spec lines (C4 against C6 on `CACHES:B2.2` with no cache is one to judge). Return `status: done`, then a heading
`Findings` with one numbered finding per defect — severity, file:line, what is wrong, the input that shows it, the fix —
and "Checked and found nothing" for each area that is clean.
