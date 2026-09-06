# Run trace — T2: research/stability.py import fix + class-level guard (2026-09-06)

First end-to-end execution of The Ancient Games on a real task. Every stage's exit line recorded.

## Stage exits
```
Gate:        PLAN_NEEDED(count=0, difficulty=LOW) — cheap means diagnosed (3 commands), MAIN executes
Guard:       research/ + tests/ edits → REVERSIBLE stakes 1; commit to master → stakes 2, checkpoint (show diff, ask)
Corroborate: n=1; independent check = red-then-green on the new test
Filter:      KEEP import fix, docstring fix, importability test (excl. __init__, _scratch_*) · CUT Makefile change (tests/ already globbed) · FOLLOW_ON extend pattern to eval/, loop/
Prove:       PASS — every claim below has its command
```

## Actions and checks (command → output)
| action | check | result |
|---|---|---|
| verify break still present | `python3 -c "import research.stability"` | `ImportError: cannot import name '_WF_GRID' from 'research.sweep'` |
| locate symbol | `grep -n _WF_GRID research/*.py` | `research/walkforward.py:30` defines it |
| write `tests/test_research_importable.py` **before** fixing | `pytest tests/test_research_importable.py -q` | **1 failed, 13 passed** — failure names `research.stability` with the real ImportError (red proven, no stash needed) |
| fix `research/stability.py:45` → two imports; docstring `:110` | `sed -n 45,46p; sed -n 110p` | `from research.walkforward import _WF_GRID`; docstring now names walkforward |
| re-run new test | same | **14 passed** (green) |
| direct import | `python3 -c "import research.stability; ..."` | `import ok; 3 grid keys` |
| acceptance gate | `make test` (foreground, 68.9 s) | **274 passed** = 260 baseline + 14 new |
| diff scope | `git diff --stat` | `research/stability.py | 5 +++--`; `tests/test_research_importable.py` new |

## Cost
0 agents · 4 tool calls · ~3 min wall (68.9 s of it the suite). The four experiment plans for this task proposed 0 / 1 / 1 / 2 agents; the 2-agent plan (F4) was built on the wrong fact (planned to rebuild a grid that exists). Gate's cheap-means step made that error impossible here: the grep ran before anything was planned.

## Return fields (MAIN as the executing agent)
- `CLAIMS`: all in the table above, each with its command.
- `SCOPE_DELTA`: none — two files, as filtered.
- `FOLLOW_ON`: (1) extend the importability pattern to `eval/*.py` and `loop/*.py` — disposition **new-task**; (2) `_scratch_pivot_dense_scan.py` runs heavy work at import (F4 finding) — excluded, disposition **out-of-scope**.
- `NOT_DONE`: none — commit `3390749` landed on master after EJ's checkpoint approval.

## What the framework got right
- Cheap means before planning caught the fact every plan needed and one plan got wrong.
- count=0 fell out of the decision tree; no dispatch overhead for a two-line change.
- Writing the test first produced the red run naturally — cleaner than all four plans' "revert and re-run" idiom. SE-native name: **TDD**. Promote this over revert-and-rerun.

## What the framework needs (v3 inputs)
1. **Gate has two distinct exits that v1/v2 conflate:** `RESOLVED` (cheap means *answered* the task, nothing to do) vs `PLAN_NEEDED(count=0)` (cheap means *diagnosed* it, MAIN still acts). T2 is the second; the drafters' trace called it the first. Define both.
2. **Environment policy is a non-delegable constraint that isn't in the 24:** "commit only when the user asks; branch if on the default branch" comes from the harness, not from any principle. It belongs in CORE `NON_DELEGABLE` for MAIN as well as agents — the same slot `PRECEDENCE` occupies.
3. **`MAIN` is an agent too.** When count=0 the schema generates no payload — but the *return* fields (CLAIMS, SCOPE_DELTA, FOLLOW_ON, NOT_DONE) still apply to MAIN's own work. The schema should generate the return contract even when count=0.
4. Nothing in this run needed the store. Lints were done by eye over a 7-row table. Consistent with "build the query when a lint hurts."
