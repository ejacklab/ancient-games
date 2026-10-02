# Task-types ledger — defaults vs challengers

One row per run that used a TASK_TYPES.md default or challenged one. Append only; reconcile at the run's end.
A challenger that beats its projection twice becomes a candidate new default; a default repeatedly overridden
gets its row rewritten. This file is state, not knowledge (method §4) — TASK_TYPES.md is the knowledge.

| Date | Run id | Category | Design source | Claimed margin | Basis | Projected cost | Actual cost | Coverage outcome | Reconciled |
|---|---|---|---|---|---|---|---|---|---|

<!-- Row rules — validated by `design_gate.py --ledger docs/TASK_TYPES_LEDGER.md` (G7): every column
     filled; claimed margin (a number >= 0.20) and basis filled for challengers, "—" for defaults; a row is
     reconciled only with its actual cost recorded. -->
