# Run trace — T1: delete six consequentially-dead helpers from loop/program_db.py (2026-09-06)

Second end-to-end run. First run to exercise Guard on a journal-adjacent file, a tripwire, and Corroborate at n=2.

## Stage exits
```
Gate:        PLAN_NEEDED(count=1, role=researcher/historian, difficulty=MED) — audit done by cheap means (AST scan + grep, two methods agree); one further zero-ref found (eval/forecast.py NetOutcomeResolver)
Guard:       mutate loop/program_db.py → stakes 2; hub = loop/program_db.jsonl; tripwire = sha256 fdfa84bc… / 42 lines, run by MAIN ×3; checkpoint before commit
Corroborate: n=2 — MAIN text-reference scan + historian dispatch-code read, isolated, different methods → same verdict on all six
Filter:      KEEP delete six + orphaned `Tuple` import · CUT NetOutcomeResolver (eval/ is the frozen-oracle surface → EJ) · FOLLOW_ON stale worktree copies of program_db.py
Prove:       PASS — every claim has its command; four suites at baseline counts; tripwire unchanged
```

## Actions and checks
| action | check | result |
|---|---|---|
| verify the six at zero refs | AST scan over 31 files + `grep -rnw` | both: 0 refs each; 1 extra candidate `NetOutcomeResolver` |
| journal event types present | `grep -o event_type … \| uniq -c` | proposed 12, guard_passed 12, evaluated 8, generation_reserved 7, evaluation_failed 3 — none of the deleted flows |
| historian (dispatched, isolated) | reads `validate_event` dispatch | all six TRULY_DEAD; `_validate_*_payload` reached at :573/:611/:648 by `event_type` string; no consequential dead code; `Tuple` orphaned |
| delete by AST span | Python, `ast.end_lineno` | 6 functions, lines 944–1097, 154 lines; `Tuple` dropped from typing import |
| compile + import | `py_compile`; `import loop.program_db` | ok; `validate_event` present |
| gate | `loop/tests`, `make test`, `make test-eval`, `make test-memory`, `make blocks` | 111+1 / 274 / 497 / 18 / passed — all at baseline |
| tripwire | `sha256sum loop/program_db.jsonl` before, after historian, after suites | unchanged all three times |
| scope | `git status --short` | `M loop/program_db.py` only |

## Cost
1 agent (historian, ~117k tokens) · 7 MAIN tool calls · ~8 min wall (suites ≈ 2 min). The four experiment plans proposed 2 / 2 / 3 / 3 agents for this task. A coder dispatch was not needed: the delete list was corroborated and the deletion is mechanical.

## Return fields (MAIN as executing agent)
- `CLAIMS`: table above.
- `SCOPE_DELTA`: **added** — remove orphaned `Tuple` from `from typing import` (consequence of the six; `closure: floor`). Dropped: none.
- `FOLLOW_ON`: (1) `eval/forecast.py:255 NetOutcomeResolver` — dead by both methods; in `eval/` → disposition **EJ decision**; (2) 11 stale `.claude/worktrees/agent-*` trees hold an older `program_db.py` where these names still have callers — disposition **out-of-scope** unless a branch merges; (3) `loop/program_db.py` `DB_PATH` per-worktree fork (from wave 1) — still open, **EJ decision**.
- `NOT_DONE`: commit — awaiting checkpoint.

## What the framework got right
- Two methods on the delete list, isolated, agreeing — and the historian produced the one fact grep cannot: the exact lines where the validators are reached independently of the six.
- The tripwire was run by MAIN three times, not reported by any agent (condition 1: independently checked).
- count=1, not the 2–3 every plan proposed. Cheap means did the audit; corroboration justified exactly one extra head.
- `SCOPE_DELTA` non-empty and reported — the field built after last time's six-surprise report did its job on the same file.

## What the framework needs (v3 inputs)
1. **`hub` ≠ "the artifact mutated."** The mutated artifact was `program_db.py`; the hub whose integrity mattered was `program_db.jsonl`, which nothing was supposed to touch. Schema §1 says hub = "invoked or mutated" — refine to: *the artifact whose integrity the change could compromise, directly or indirectly*. This is the S1 definition.
2. **`WRITE_BOUNDARY` was over-broad and the agent honored it literally** — "never call append_event/record_*" made the historian decline to run `pytest loop/tests/` even though the tests isolate the journal. State the boundary as a *path* ("never write to `<hub>`"), not as function names.
3. **`DOMAIN` field: no observable effect** on a concrete task. Expect it to matter on research dispatches, not execution ones.
4. Still nothing needed the store. Lints were a 9-row table by eye.
