# Brief — fix the readiness sanitization test

## Task (one deliverable)
Make `tests/test_readiness.py::test_rt_01_sanitized_full_inventory` pass. Print your root-cause and the diff summary.

## Context
The test runs `.claude/skills/workflow-design/scripts/readiness.py` in an isolated HOME and asserts the output has NO
absolute home path and NO repo-root path — the inventory must be portable. It currently fails: readiness reports
`str(p)` (full absolute paths) in the Probe `path` field and in reasons. Fix: sanitize — replace the home path with
`~` and the repo root with a relative marker, in every place a path is reported. Do not change what is probed, only
how paths are rendered.

Decided (2026-10-09), do not re-ask. **Root cause**: pytest's basetemp is now under `/home/smoke01` (the hermes
cache), so the sandbox's `tmp_path` (and therefore `sandbox.home`) is under the REAL home `/home/smoke01`. The test
asserts the real home is not in the output, but the proof column legitimately holds `sandbox.home`, which contains
`/home/smoke01` — so the two assertions conflict only because the sandbox overlaps the real home.

**Fix** (a test-fixture fix, not readiness.py): make the sandbox home not overlap the real home. In the sandbox
fixture, create the home under `/tmp` (`tempfile.mkdtemp(dir="/tmp")`) instead of pytest's `tmp_path`, so
`sandbox.home` is `/tmp/...` and contains no `/home/smoke01`. Then both assertions hold without touching
readiness.py. You may change `tests/test_readiness.py` (or its fixture) — my earlier "only readiness.py" was wrong.

## Template (fill this exactly)
```
## Root cause
<one line — why the test fails>
## Fix
<what changed in readiness.py, one line>
## Verified
<the test output, red before / green after>
```

## Example (one good result, short)
```
## Root cause
readiness reports str(p) for every path; the sandbox home is under the real home, so the absolute path leaks.
## Fix
a sanitize() helper replaces str(home) with ~ and the repo root with a relative marker, applied to the path field.
## Verified
test_rt_01_sanitized_full_inventory: 1 passed
```

## Standard
`env -u NO_COLOR /usr/bin/python3 -m pytest tests/test_readiness.py::test_rt_01_sanitized_full_inventory -q` passes,
and no other readiness test regresses. Only `readiness.py` changes.
