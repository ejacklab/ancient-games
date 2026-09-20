# State — 20260921-ablation7

Rules: one writer at a time. Read this file before your step; update it after. It holds progress and results
only — never reasoning; put notes in your own output file. Never delete a log line.

## Challenge (verbatim)

> eva and design a dymanic workflow based on the anceint game first

in the context of: run the experiment `docs/ABLATION_6.md:129-131` asks for — a task where the agent must
act, so the run reaches `guard` and stakes 2 and corroboration engages.

## Baseline

`git status --short` before the run folder was created (the run may add files only under its own folder):

```
(clean)
```

HEAD: 13094d4 · suite: 379 passed

## Steps

| # | Step | Status | Output file |
|---|---|---|---|
| 1 | Intake and readiness | done | readiness.md |
| 2 | Algorithm and unclear spots | done | (in workflow-design.md) |
| 3 | Size decision | done | (below) |
| 4 | Workflow design | done | workflow-design.md |
| 5 | P1 ground truth | todo | p1-groundtruth.md |
| 6 | P1V blind verify | todo | p1v-verify.md |
| 7 | P2 pre-registration | todo | docs/ABLATION_7.md |
| 8 | P3 case + packet | todo | p3-scorer-diff.md |
| 9 | P4 the run | todo | ablation/runs/attempt8/GM2.journal.jsonl |
| 10 | P5 score + write up | todo | docs/ABLATION_7.md (Result) |
| 11 | P6 what is missing | todo | p6-gaps.md |

## Size decision

**design** — pieces: 6, unclear spots: 2 (one of kind *information*, which always means a design), risk: high
(an ablation run is expensive and n=1; a wrong fixture makes the whole run unscoreable).

## Unclear spots

| Id | What is unclear | Kind | Blocks | Depends on |
|---|---|---|---|---|
| S1 | Is there a genuinely dead, stakes-2 deletion target in `seza/backtest`? `eval/forecast.py` is disproved (imported by `tools/derive_g4_thresholds.py:57`, six `eval/tests/` files reference it); `loop/graph_memory.py` excluded by rule (its ground truth is the disputed thing) | information | P2–P6 | — |
| S2 | If S1 comes back "none", synthetic fixture or abandon? | decision (EJ) | P2–P6 | S1 |

## Questions for EJ (one batch)

| # | Question | Provisional assumption if unanswered |
|---|---|---|
| 1 | Model for the agent under test | Sonnet, as ablation 6 — one variable |
| 2 | If no real dead target exists | synthetic fixture in `ablation/fixtures.py`, stated plainly |
| 3 | Ceiling | 124, as ablation 6 |
| 4 | Packet names the target, or agent finds it | names it, as ablation 6 |
| 5 | May P1V delete in a scratch worktree | yes, throwaway worktree only |

## Log (append only)

- 2026-09-21 step 1 done: readiness run; 2 tool proofs FAILED first time (scorer invocation; `eval/forecast.py` not dead) and are recorded
- 2026-09-21 step 2-4 done: 6 pieces, 2 unclear spots, sequential; no parallel candidates pass all five tests
- 2026-09-21 awaiting EJ: the 5-question batch above, and go-ahead to run (est. 300-400k tokens)
