# Round 3 — prompts p201–p300, and review of the generated designs

Date: 2026-10-02. Corpus: 20 boundary probes (one per rule enhanced in rounds 1–2), 30 InterOp, 20
ancient-games/general, 20 heavy combos (2–4 deliverables), 10 meta/edge. Classifier: COO. Samples with the
updated rules: codex p221–p245, agy p271–p295 (the combo block — the hardest test of rule 1). All 100 designs
generated (`runs/…/designs_r3/`), all gated; 5 reviewed blind by codex `gpt-6.1-sol` (4-item checklist, no COO
reasoning shown).

## Script-gate pass

1 bug on the first pass — **against the corpus author's own label**: p269 ("extract flags into flags.csv")
marked builds=true, but a deliverable CSV is a report in data shape, not product/test surface. G2 fired exactly
as designed. Fixed by refining rule 5; corpus + results corrected; checker then 0 bugs, exit 0.

## Executor agreement (rules v2, fresh prompts)

| | codex (25) | agy (25, all combos) |
|---|---|---|
| strict | **24/25 (96%)** | 19/25 (76%) |
| lenient | 24/25 (96%) | 22/25 (88%) |

Trajectory: codex 12% → 84% → **96%**; agy 24% → 72% → **76%** strict. Residuals:
- p231 (codex): external research labelled `research and reports` — genuine boundary, fixed forward by new
  rule 8 (source locus decides).
- agy: 2 passenger labels on debugging-with-fix prompts (p273, p285 — rule 1 exists; flash-tier adherence
  limit), 1 missed builds implication (p279), 1 dropped combo label (p286 — debatable, waived with note),
  2 document-vs-research/codegen boundary calls (p288, p295 — fixed forward by new rule 9).

## Blind design review (the round-3 headline)

5 designs reviewed: **2 ACCEPT, 3 REJECT** — and every rejection was a real defect the script gate cannot see:

| Design | Verdict | Defect | Fix |
|---|---|---|---|
| p222 (debugging+review) | ACCEPT | — | — |
| p274 (4-label test combo) | REJECT (item 2) | reviewer same kind as the codex writers; a mixed-kind builder blended the constraint away | G6 now takes kinds from **pure (yes) builders** first; new regression test |
| p279 (grade→fix→regrade) | REJECT (item 4) | the prompt's regrade never became a node | new rule "recheck verbs get their own node" + pipeline row + builder expansion |
| p288 (research→doc) | REJECT (item 4) | the document row's embedded "review against source" was not materialized | builder now emits the review node for non-tiny document pieces |
| p298 (research→codegen trap) | ACCEPT | the G2-trap prompt produced a correct two-label design | — |

Repair pass (attempt 2): p274 ACCEPT, p288 ACCEPT, **p279 REJECT again** — the label was set but the builder
still emitted no regrade node. Attempt limit reached; root cause was mechanical and diagnosed (builder ignored
pipeline node lists), so the builder was fixed and the design verified once more: **ACCEPT** (reviewer confirmed
the regrade node, same rubric, EJ escalation). The limit-hit episode is recorded here per the tier-exit rule's
spirit: a diagnosed mechanical defect gets a direct fix, an unclear piece would have gone to EJ.

## Enhancements applied this round

Rules 8 (web search vs research: source locus) and 9 (document and explain: prose for humans, incl. knowledge
files); recheck-verb rule + `grade → fix → regrade` pipeline row; G6 pure-builder kinds; builder materializes
the document review node and the regrade node; p269/p279 corpus corrections; 1 new regression test (dilution).

## Lessons learned

- L8: **the two-layer review is now evidenced (n=5+3, one campaign):** the script gate caught the structural
  lie (p269) and the blind checklist caught the three semantic defects (missing recheck node, unmaterialized
  pattern step, diluted reviewer kind). Neither layer alone would have passed these designs.
- L9: written rules keep closing the gap on the strong tier (96% — near the ceiling of label-set agreement),
  while the flash tier plateaus ~76–88% with residual errors concentrated in passenger labels and implication
  reading. Cheap tiers stay usable for classification **with** the script gate and COO verdict review (L5).
- L10: the gate is most trustworthy when it fires on its own author — p269 was the COO's label, caught by the
  COO's gate, fixed by a rule change. That is the house sabotage principle working at campaign scale.
