# Round 1 — prompts p001–p100 (90 real operator prompts + 10 edge cases)

Date: 2026-10-02. Classifier: COO (main session). Independent samples: codex `gpt-6.1-sol` medium (p001–p025),
agy `gemini-3.8-flash-medium` (p050–p074). Canary: both kinds pass before sampling (agy needed 3 attempts;
see state.md — two failure modes logged, one is the documented soft-denial trap caught by the house rule).

## Bugs found (35 by the script gate, 41 executor disagreements)

| # | Class | Count | Root cause | Fix applied this round |
|---|---|---|---|---|
| B1 | GAP + G1 | 10+10 | `document and explain` (7 prompts) and `grade a run` (3) had no table rows | two rows added to TASK_TYPES.md |
| B2 | G2 false positive | 6 | `Touches product` was binary; diagnostic debugging / fixture validation are read-only runs of write-capable categories | tri-state column: yes / **mixed** / no; gate branch 2 fires only on `yes` |
| B3 | G6 false positive | 6 | consequence of B2 — diagnosis-only designs were demanded a review node | builders = `yes` nodes, or `mixed` nodes when design `builds` |
| B4 | EXEC strict disagreement | 41 (codex 12%, agy 24% agreement) | D1 over-labelling (passenger `information extraction`), D2 review-vs-research boundary, D3 contradictory builds instruction (said docs count; corpus says findings files don't), D4 one dual-readable prompt (p020) | **Labelling rules** section added to TASK_TYPES.md (6 rules); round-2/3 batch instructions carry them |

After enhancement: checker exit 0 (0 bugs) on round 1; `design_gate --self-test` PASS; task-types tests 15/15.

## Executor agreement (round 1 = baseline, rules not yet given to the executors)

| Mode | codex (25) | agy (25) |
|---|---|---|
| strict (exact set + tiny + builds) | 3/25 (12%) | 6/25 (24%) |
| lenient (expected ⊆ result, tiny match) | 8/25 (32%) | 18/25 (72%) |

Codex residual disagreements concentrate on D2 (it calls every DSD-vs-JS comparison "code review"); agy
residual is mostly passenger labels. Round 2 tests whether the written labelling rules close the gap — that is
the campaign's actual experiment.

## Lessons learned

- L0 (canary): agy headless needs "Do not use any tools." prefix + duration suffix (`120s`); exit 0 with empty
  stdout + stderr denial notice = FAIL. The house rule "an exit code is never the check on its own" earned its
  first live catch. Candidate for EXECUTOR_KINDS.
- L1: category attributes like `touches_product` belong to the *piece in context*, not the category — any
  binary flag on a category will produce false accusations; prefer tri-state with the design's facts deciding.
- L2: a taxonomy without labelling rules measures the annotator, not the model. Strict agreement is only
  meaningful once the primary-label rule, passenger-label ban, and builds definition are written down.
- L3: batch instructions are part of the tested system — a contradiction between instruction and corpus
  convention (D3) shows up as "model disagreement". Version the instruction with the rules.
- L4: the real distribution is ~60% read-only cited research; the research row's default check was upgraded to
  the corpus's native epistemics (both-side citations + CONFIRMED/INFERRED/GAP/UNPROVEN; missing proof never PASS).

## Principle changes

None. All fixes are refinements inside the existing principles (schema gates, category-vs-facts stop, risk
tiering). No method principle was weakened or reversed.
