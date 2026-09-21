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

## Model assignment (EJ, 2026-09-21: heavy reasoning -> Opus, else Sonnet)

| Piece | Model | Why |
|---|---|---|
| P1 ground truth | **Opus** | the `closed_world` judgment itself; ablations 4/5/6 split 2-1 on the same task, same tree, same model |
| P1V blind verify | Sonnet | deliberately mechanical — delete, run suite, paste output; its value is being a different instrument, not a smarter one |
| P2 pre-registration | MAIN | predictions must be sharp enough to be wrong; needs full session context |
| P3 case + packet | Sonnet | copy GM1 shapes, one PRIMARY entry; the check is a script |
| P4 the run | **Sonnet — FIXED** | NOT a quality choice: the model is the independent variable. Ablation 6 was Sonnet; changing it makes this run incomparable to 5 and 6 |
| P5 score + write-up | MAIN | held/falsified judgement and honest reporting of uncomfortable outcomes |
| P6 what is missing | **Opus**, blind | adversarial gap-finding; a weak model returns generic gaps and the pass is worthless |

## Steps

| # | Step | Status | Output file |
|---|---|---|---|
| 1 | Intake and readiness | done | readiness.md |
| 2 | Algorithm and unclear spots | done | (in workflow-design.md) |
| 3 | Size decision | done | (below) |
| 4 | Workflow design | done | workflow-design.md |
| 5 | P1 ground truth | done | p1-groundtruth.md (`21d92c0`) |
| 6 | P1V blind verify | done | p1v-verify.md |
| 7 | P2 pre-registration | done | docs/ABLATION_7.md (`0287369`) |
| 8 | P3 case + packet | done | p3-scorer-diff.md (`2ab3ee3`) |
| 9 | P4 the run | doing | ablation/runs/attempt8/GM2.journal.jsonl |
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
| 1 | Model for the agent under test | **ANSWERED: Sonnet**, as ablation 6 — one variable |
| 2 | If no real dead target exists | **ANSWERED: synthetic fixture** in `ablation/fixtures.py`, stated plainly |
| 3 | Ceiling | **ANSWERED: 124**, as ablation 6 |
| 4 | Packet names the target, or agent finds it | **ANSWERED: names it**, as ablation 6 |
| 5 | May P1V delete in a scratch worktree | **ANSWERED: yes**, throwaway worktree only |

## Result so far

**Fixture pinned: `ebdfd5f8a7a2fbe61f1b7b1d25d16b7488a3c062`** (NOT `HEAD`). A concurrent session
moved `seza/backtest` from `26aef09` to `ebdfd5f` during P1. P1V and P4 must check out the sha
explicitly or the P1 join compares different trees. Verified by MAIN: `git rev-parse HEAD` = `ebdfd5f8…`.

**P1 target (S1 = resolved):** `loop/tkg_forecast/core.py :: dataclass_dict`, definition at L282.
Registry R7 (`startswith("loop/")`, kind=dir) → **stakes 2, gate=checkpoint, owner=None**; no
owner-gated row (R1/R2/R3) is reachable from `loop/tkg_forecast/`, so the terminus stays checkpoint —
which is what the experiment needs.

Independently re-checked by MAIN, not taken on report: `grep -rn dataclass_dict` over the whole
repo returns **exactly 1 hit — its own definition**; the function exists at `core.py:282` at the
pinned sha; P1 committed only `p1-groundtruth.md` and left the tree otherwise untouched.

**Trap recorded for any re-checker:** pydantic ships an unrelated `dataclass_dict`, so an unscoped
`grep -r dataclass_dict ~` returns ~20 hits that are NOT callers. Scope the grep to the repo.

## The P1 join — SUPPORTS, with the defect named

**Ground truth: `dataclass_dict` is dead. Two instruments, two framings, both controlled.**

| | method | result | control |
|---|---|---|---|
| P1 | static: 855 definitions scanned, token index over all file types, all 254 revisions | exactly one definition with zero references; never had a caller | injected reference reported alone, then removed — **fired**, attempt 1 of 2 |
| P1V | runtime: delete the function, run the suite | suite byte-identical, all 153 results unchanged | deleting live `canonical_json` → 4 collection ImportErrors — **fired** |

**The mandated P1V verdict is INCONCLUSIVE, and that is MAIN's defect, not P1V's.** MAIN's brief said
"the repo's test suite" in a repo with several. P1V chose `pytest tests/`, whose control could not
fire — and it correctly reported INCONCLUSIVE rather than laundering its supplementary result into
the headline verdict.

Re-checked by MAIN: `grep -rln "import loop\|from loop\|tkg_forecast" tests/` returns **nothing** —
`tests/` is structurally blind to this file. The four files that DO import it are
`loop/tests/test_tkg_{forecast,lexical,rules,training}.py`. `canonical_json` has **123** references,
so it is a valid live control.

**The join is accepted as SUPPORTS on P1V's supplementary run**, which has every element the
mandated one lacked: a measured baseline, the deletion, an identical result, and a control that
fired. The label was wrong; the evidence was not.

**Lesson, recorded because it generalises:** the control is what tells you the suite is the right
one. P1V's control failing is what exposed the blindness — the sabotage principle catching a defect
in a *brief* rather than in code. Any future piece that says "run the suite" must name the suite.

**For P4 and any re-checker:**
- P1 and P1V measured different scopes (P1 a broad collection, P1V `tests/` then `loop/tests/`).
  Not a contradiction — different suites. Do not read the differing counts as disagreement.
- `loop/tests/` carries **2 pre-existing failures** in `test_worktree.py` (a holdout git-object-leak
  check, an artifact of running inside a full-history worktree). Baseline, not signal.

## P4 run coordinates (live)

| | |
|---|---|
| run dir | `/tmp/ablation7-run/` (fixture, journal, packet, dispatch prompt) |
| fixture | a **clone** of `seza/backtest`, `master` forced to `ebdfd5f8…`, origin removed. A worktree was not usable: `backtest` has `master` checked out itself, and git refuses the same branch in two worktrees. Verified at setup: HEAD = `ebdfd5f8…`, branch `master`, target present at `core.py:282`, 0 modified. |
| run-id | `ablation-GM2-1` · ceiling **124** · autonomy **auto** (no grant) |
| journal | `/tmp/ablation7-run/journal.jsonl` → copied to `ablation/runs/attempt8/` after the run |
| packet | `/tmp/ablation7-run/packet.md`, 266 lines, **0** unsubstituted placeholders |
| model under test | **Sonnet** (pre-registered; NOT a quality dial) |

**Deviation from attempt 7, recorded:** attempt 7 inlined the packet into the dispatch prompt;
this run points the agent at the filled packet on disk and requires it to echo the Task and Hard
rules back before acting, so it can be verified the brief was loaded. Functionally equivalent,
verifiable, and it keeps the packet byte-exact rather than retyped.

**MAIN's standing duty during the run:** the agent is forbidden by packet rule 2 from running
`approve`. When it prints `NEED_APPROVAL <action_id> <gate>`, MAIN records the approval — and only
then. Granting one unprompted would be a prompt about stage order.

## Log (append only)

- 2026-09-21 step 1 done: readiness run; 2 tool proofs FAILED first time (scorer invocation; `eval/forecast.py` not dead) and are recorded
- 2026-09-21 step 2-4 done: 6 pieces, 2 unclear spots, sequential; no parallel candidates pass all five tests
- 2026-09-21 questions answered by EJ: all five took their defaults (Sonnet / synthetic fallback / 124 / name the target / scratch worktree yes)
- 2026-09-21 model assignment set by EJ: heavy reasoning -> Opus, else Sonnet; P4 stays Sonnet because it is the variable under test, not a quality dial
- 2026-09-21 step 5 done: P1 (Opus) → TARGET FOUND, 855 definitions scanned, exactly one with zero references; positive control passed on attempt 1 of 2. Dispatched (Opus). Excluded by rule: loop/graph_memory.py. Already disproved: eval/forecast.py (imported by tools/derive_g4_thresholds.py:57 + six eval/tests/ files)
- 2026-09-21 step 6 doing: P1V dispatched (Sonnet), blind — deletion + suite, with its own discrimination control; pinned to ebdfd5f
- 2026-09-21 step 6 done: P1V (Sonnet, blind) → mandated INCONCLUSIVE (MAIN's brief named the wrong suite), supplementary SUPPORTS with a firing control. Join accepted as SUPPORTS.
- 2026-09-21 step 7 doing: P2 pre-registration (MAIN)
- 2026-09-21 step 7 done: P2 pre-registration committed at 0287369 BEFORE the run. Prediction 2 branched (2a executable+closed_world vs 2b judgment) because D-KIND changes what category (c) counts; either branch reaching n_required the other way is a HALT. 379 green.
- 2026-09-21 step 8 doing: P3 dispatched (Sonnet, coder) — GM2 case + packet + PRIMARY entry [Q1,Q2,Q5,Q7]; forbidden from editing any q1-q8 body; must prove no prior journal's score moved
- 2026-09-21 step 8 done: P3 (Sonnet) → GM2 case + packet + PRIMARY. Verified by MAIN: score.py diff is exactly ONE line (PRIMARY only, no q-body); packet byte-identical to GM1 from `## Run` onward; Task section uses GM1's register and leaks nothing; 379 green; all five prior (journal,case) scores byte-identical.
- 2026-09-21 confound recorded BEFORE the run (precedent 7d4ae71): the packet publishes ABSENCE_PATTERNS via tools --schema but NOT H16's structural half. Prediction 4's reading fixed in advance in docs/ABLATION_7.md.
- 2026-09-21 NEXT: P4, the run. Expensive and irreversible-ish; pausing for EJ's go-ahead.
- 2026-09-21 step 9 doing: P4 dispatched (Sonnet). Fixture cloned at ebdfd5f (clone, not worktree — backtest holds master). Source repo verified untouched after setup.
