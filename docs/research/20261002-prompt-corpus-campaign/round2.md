# Round 2 — prompts p101–p200 (40 InterOp variants, 25 ancient-games, 20 general dev, 10 combos, 5 edge)

Date: 2026-10-02. Classifier: COO. Independent samples **with the round-1 labelling rules embedded** (extracted
verbatim from TASK_TYPES.md — the instruction never gets its own copy): codex `gpt-6.1-sol` on p126–p150,
agy `gemini-3.8-flash-medium` on p176–p200.

## The round-1 experiment, answered

| Agreement | codex r1 → r2 | agy r1 → r2 |
|---|---|---|
| strict (exact labels + tiny + builds) | 12% → **84%** | 24% → **72%** |
| lenient (expected ⊆ result, tiny match) | 32% → **88%** | 72% → **72%** |

Written labelling rules moved the strong tier from near-noise to near-agreement on fresh prompts. The cheap
tier improved sharply but retains a systematic failure mode (C4 below). Lesson L2 from round 1 is confirmed
with measurements: the taxonomy, not the model, was the bottleneck.

## Bugs and disagreements (11, all EXEC class; the script gate found 0 on this round)

| # | Class | Prompts | Root cause | Fix applied |
|---|---|---|---|---|
| C1 | cases-vs-script confusion | p139, p143 (codex), p187, p190 (agy) | no boundary defined between `test cases gen` and `test script gen` | new labelling rule 7: cases = assertions, script = machinery; "would it make sense with a different runner?" |
| C2 | finding re-validation boundary | p141 (codex: code review) | review-vs-research rule silent on re-validating findings | rule 3 extended: re-validation updates a findings list → research |
| C3 | fixtures counted as non-builds | p130 (codex) | rule 5 listed test files but not generated data | rule 5: generated fixture/data files are test surface → builds=true |
| C4 | **vague collapsed to tiny** | p196, p197, p199 (agy, 3/3) | tiny-gate applied without a restatement | rule 6: tiny requires a *successful restatement*; un-restatable prompts are `others` + decision spots, never tiny. Fail-unsafe direction noted below |
| C5 | dropped labels on combos | p193 (lost web search), p195 (lost test script gen) — agy | rule 1 said when to multi-label, not how | rule 1: list the deliverables first, then label each; dropping a label is as wrong as a passenger label |

## Lessons learned

- L5: **Rules transfer across engines, but not equally.** The strong tier internalized all six rules from one
  reading; the flash tier still mis-fires on the judgment that protects the whole method (vague→tiny). Cheap
  tiers may classify; the *tiny* call specifically needs the script gate plus COO review of the verdict —
  a wrong tiny skips everything downstream and no design-level gate ever sees it.
- L6: **Batch instructions must be extracted from the canonical doc at run time**, not rewritten. Round 2's
  instruction was sliced verbatim out of TASK_TYPES.md; the rules therefore cannot drift from the table.
- L7: boundary bugs cluster where two categories share a verb ("write tests", "review"). Every such pair needs
  its own discrimination sentence, with the confusing example named.

## Principle changes

None. Round 2 changed definitions under existing principles. One architectural confirmation: the
classify-cheap/gate-script/review-blind stack caught every C-class error at the script layer *in the corpus
test*; in live runs the tiny-call remains the one decision the script cannot fully gate (L5) — COO verdict
review is its compensating control, as designed.
