# Brief — fix the localize tool (hybrid UC7)

## Task (one deliverable)
Make `tests/test_hybrid_cases.py::test_case[UC7]` and `::test_uc7_suite_really_goes_red_then_green` pass. Print your
root-cause and the diff summary.

## Context
`ancient_games/hybrid/tools/localize.py` locates a failure in pytest output by stripping ANSI then matching a
`^`-anchored FAILED/ERROR line and a `file.py:line:` frame. The tests fail with `localize ok: False, reason: "no
failure located"`. Root-cause it: run the fixture, inspect the exact pytest output the tool receives, and fix the
matching so it locates the failure reliably with and without ANSI colour.

## Template (fill this exactly)
```
## Root cause
<one line — why localize reports "no failure located">
## Fix
<what changed in localize.py, one line>
## Verified
<the test output, red before / green after>
```

## Example (one good result, short)
```
## Root cause
the ^-anchored FAILED regex does not match the line after ANSI stripping (leading whitespace/prefix).
## Fix
make the FAILED/ERROR match unanchored, or match the leading marker.
## Verified
test_case[UC7]: 1 passed
```

## Standard
`env -u NO_COLOR /usr/bin/python3 -m pytest "tests/test_hybrid_cases.py::test_case[UC7]" "tests/test_hybrid_cases.py::test_uc7_suite_really_goes_red_then_green" -q`
passes, and no other hybrid test regresses. Only `ancient_games/hybrid/tools/localize.py` changes.
