# Brief — review the two fixes and run the full suite

## Task (one deliverable)
Review the diff to `readiness.py` and `localize.py`, then run the full suite. Print a clean pass or findings with
file:line.

## Context
The two fixes are minimal and targeted. Read the two diffs (never the workers' reasoning) and check: is each fix the
smallest change that makes its test pass? Does either change behaviour beyond the failing test?

## Template (fill this exactly)
```
## Checklist
- [ ] each fix is the smallest change that makes its test pass
- [ ] full suite: 0 failures
## Findings
<each with file:line, or "clean pass">
```

## Example (one good result, short)
```
## Checklist
- [x] readiness fix touches only the path rendering
- [x] localize fix touches only the regex
- [x] full suite: 0 failures
## Findings
clean pass
```

## Standard
`env -u NO_COLOR /usr/bin/python3 -m pytest -q` reports 0 failures. Review only — change nothing.
