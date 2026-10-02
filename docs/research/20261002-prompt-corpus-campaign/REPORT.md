# Campaign report — 300 operator prompts through the workflow-design pipeline

2026-10-02. Requested by EJ: take `tests/operator-prompt-list.md` as testing material, create 300 test
prompts, run three rounds of 100 with enhancement at each round's end, review the generated designs in round
3, and report what was fixed/enhanced and whether any principle changed. Executor use (codex, agy) approved
by EJ for this campaign.

## What ran

| Asset | Size |
|---|---|
| Corpus | 300 prompts (`tests/fixtures/operator_prompts_r{1,2,3}.jsonl`): 90 real operator prompts + 210 synthetic in EJ's voice — InterOp, ancient-games, general dev, combos, boundary probes, vague/trap/meta cases |
| Classifications | COO 300; independent samples: codex `gpt-6.1-sol` 75, agy `gemini-3.8-flash-medium` 75 |
| Generated designs | 300 (round 3's 100 emitted to `runs/…/designs_r3/`; all 300 gated through `design_gate.py`) |
| Blind design reviews | codex, 4-item checklist, 5 designs + 3 repair passes |
| Canaries | codex pass first try + sabotage (can-fail proven); agy pass on 3rd try, two failure modes documented |
| Harness | `tests/workflows/corpus_check.py` (compare/gate/emit/lenient), pytest 395 → **397 green** |

## Agreement trajectory (the campaign's experiment)

Strict = exact label set + tiny + builds, versus corpus expectations:

| Round | codex | agy |
|---|---|---|
| 1 (no labelling rules) | 12% (lenient 32%) | 24% (lenient 72%) |
| 2 (rules v1 embedded) | 84% (lenient 88%) | 72% (lenient 72%) |
| 3 (rules v2 embedded) | **96%** | **76% (lenient 88%)** |

The system under test was the *taxonomy*, not the models: every disagreement class across 150 samples traced
to a missing definition, and each definition written closed its class.

## What was fixed / enhanced (cumulative)

1. **Two new categories** evidenced by real prompts: `document and explain`, `grade a run` (round 1, 10 prompts
   had no home).
2. **Tri-state `Touches product`** (yes/mixed/no): diagnostic debugging and validation-only test-data runs are
   read-only runs of write-capable categories; the binary column produced 12 false accusations (round 1).
3. **Nine labelling rules** in TASK_TYPES.md: deliverable-first labelling, passenger-label ban, review-vs-
   research, grade-vs-debug, builds definition (fixtures yes, deliverable data outputs no), vague-never-tiny,
   cases-vs-script, source-locus for web search, prose-for-humans for documents (rounds 1–3).
4. **G6 hardened**: reviewer-kind constraint computed from pure builders; mixed-kind blends can no longer
   dilute it (blind-review catch, p274).
5. **Recheck-verb rule + `grade → fix → regrade` pipeline row**: "then regrade/rerun/verify after" must appear
   as its own node (blind-review catch, p279 — rejected twice, fixed in the builder, verified ACCEPT).
6. **Builder materializes embedded pattern steps**: the document row's review-against-source is now a node
   (blind-review catch, p288).
7. **Rule 5 refined by the gate firing on its own author**: p269's CSV deliverable is a report in data shape
   (builds=false) — the corpus author's mislabel, caught by G2.
8. **Research row check strengthened** to the corpus's native epistemics: both-side citations +
   CONFIRMED/INFERRED/GAP/UNPROVEN; missing proof never reads as PASS.
9. **agy wrapper requirements proven live**: "Do not use any tools." prefix, `--print-timeout` needs a
   duration suffix, exit 0 + stderr denial notice = FAIL (candidate rows for EXECUTOR_KINDS).
10. **Harness + tests**: corpus_check (strict/lenient/compare/emit-designs), 17 task-type tests including the
    dilution regression; all rounds end checker-green.

## Principle changes: **none**

No principle was weakened, reversed, or added. What changed are definitions and gate mechanics *under* the
existing principles, and the campaign produced their first evidence:

- schema-gates-everything: held — 300/300 designs passed through the same gate;
- category-vs-facts is a stop: held — fired on the trap prompts and on the author's own label;
- cheap classifier + script gate + blind review: held, now n=5+3 — the two layers caught disjoint defect classes;
- coverage is a gate, never an axis: untested (no challenger design was fielded — the 20% rule stays n=0);
- sequential rounds with bounded repair: held — one repair attempt per design, limit-hit episode documented
  and handled per the tier-exit rule.

## Known limits (honest ledger)

- COO wrote both expectations and classifications for the 300 — independence came only from the 150 executor
  samples and the blind reviews. A future campaign should have a second human or a blind agent label a sample.
- The ledger (`TASK_TYPES_LEDGER.md`) is still empty: nothing here ran a real workflow, so all defaults remain
  n=0 for *execution*; they are now n=300 for *routing*.
- agy (flash tier) plateaus ~76–88%: usable with the gate, not trustworthy alone for the tiny-call (L5).
- p286's expectation is debatable (waived with a note, not silently dropped).

## Addendum — two post-report regressions, both caught by re-running all three rounds

Enhancing one round can break another; every enhancement was therefore re-checked against **all 300**, and
that discipline caught two:

1. **p073** (round 1): the new document-review node used the writer's own engine kind while the document piece
   was a builder — G6 fired correctly; the builder now gives an embedded review a different kind when the
   document builds. Regression test added.
2. **p195/p273** (rounds 2/3): designs whose builders span engine kinds cannot have one different-kind
   reviewer. G6 gained reviewer→worker **pairing** (`reviews` field, documented in the design JSON), and the
   rule's honest consequence was written down: a multi-kind build group **splits its review**, one reviewer
   per kind group.

Final state: three round checkers exit 0, pytest **398 passed**, gate and readiness self-tests PASS, intake
harness all passed, shipped ledger validates.

## Files

Round reports: `round1.md`, `round2.md`, `round3.md` (this folder). Raw evidence:
`runs/20261002-prompt-corpus-campaign/` (state, canary logs, batches, executor raw outputs, results, designs,
bug lists). System changes: `docs/TASK_TYPES.md`, `design_gate.py`, `corpus_check.py`, `test_task_types.py`,
corpus fixtures.
