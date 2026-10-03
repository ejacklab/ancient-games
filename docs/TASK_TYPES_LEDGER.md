# Task-types ledger — defaults vs challengers

One row per run that used a TASK_TYPES.md default or challenged one. Append only; reconcile at the run's end.
A challenger that beats its projection twice becomes a candidate new default; a default repeatedly overridden
gets its row rewritten. This file is state, not knowledge (method §4) — TASK_TYPES.md is the knowledge.

| Date | Run id | Category | Design source | Claimed margin | Basis | Projected cost | Actual cost | Coverage outcome | Reconciled |
|---|---|---|---|---|---|---|---|---|---|
| 2026-10-03 | 20261003-node-workdir | code generation (build a feature, case C) | default | — | — | 210k–460k tokens, about 4 engine calls, 10–20 min (token measure not named — a flaw) | Codex dev, 2 rounds: new input 68.8k · cache read 703k · output 5.5k; agy 3 calls not measurable (protobuf); 5 engine calls plus 4 script steps; engine time 417 s (dev and cases in parallel) | R1–R7 pass (8 blind cases, failed 7/8 on the old code first); baseline 463/463 still pass; scope, must-not and tamper ok; review: accept, no findings | yes |

<!-- Row rules — validated by `design_gate.py --ledger docs/TASK_TYPES_LEDGER.md` (G7): every column
     filled; claimed margin (a number >= 0.20) and basis filled for challengers, "—" for defaults; a row is
     reconciled only with its actual cost recorded. -->
