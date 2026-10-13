# Result — blind re-tag with a control (2026-10-13)

Run by the COO (Claude Opus 5.5). Design: `workflow-design.md`; prediction (written first, sent to EJ before R4):
`prediction.md`; counts: `counts-140.md` (main) and `counts.md` (all 143), both from `count.py`, a script the COO
wrote and proved on a fixture before any sheet existed (`evidence/R2.txt`) — not independent evidence; every sheet
and the key are saved for a hand recount.

## Who tagged

| Pass | Engine | Checks | Audit |
|---|---|---|---|
| control (old meanings) | dsh headless, DeepSeek deepseek-flash, fresh session | schema PASS, 2 of 2 scored plants right | read only brief.md and rows.md |
| new (RESEARCH_TAGS.md) | same engine, fresh session | schema PASS, 3 of 3 plants right | read only its two files; wrote and checked its own output file in its work dir |
| control2 | same | attempt 1: a plant wrong; attempt 2: a prose line before the JSON; **attempt 3** (beyond the limit, EJ's decision): schema PASS, plants right | clean in all three |

## Counts, 140 rows (quoted from `counts-140.md`)

| outcome | control | new |
|---|---|---|
| same | 109 | 92 |
| moved | 31 | 47 |
| split | 0 | 1 |
| stuck | 0 | 0 |

Moves — control: reported → verified 27, reported → unknown 2, verified → reported 2. New: reported → verified 31,
verified → unknown 7, reported → unknown 6, unproven → verified 3; one split (R080, s5-F29: verified + unproven).
The three MagmaMem control rows: `unknown` in both passes. On 143 rows: control 109 same / 34 moved; new 92 / 50 / 1 / 0.

## Prediction, scored

| # | Predicted | Got | |
|---|---|---|---|
| 1 | control same 105–125, moved 15–35 | 109, 31 | held |
| 1 | control keeps different tags in at least one pair | both pairs unified (all `verified`) | **failed** |
| 2 | new moved + split 30–60, stuck 0–3 | 48, 0 | held |
| 2 | mostly reported → verified and verified → split | reported → verified 31; but verified → split only 1, and verified → unknown 7 | **half** |
| 3 | new gives each pair one tag | Zep pair one tag; Mem0 trio not — R014 (s4-F19) `reported`, the others `verified` | **failed** |
| 4 | the two control passes disagree less than either with the old labels | control vs control2: 11 rows; vs old labels: 31 and 36 | held |

## Void conditions — none triggered

Audits clean; control equals the old labels on 109 of 143, not 143; new differs from control on 26 rows; both
counted sheets passed their plants.

## Reading (by `docs/RESEARCH_TAGS.md` step 6)

- **No stuck row** in the new-rule pass: the definitions decided every row. By the file's own test, they are not sent
  back to EJ on that ground.
- **New-rule movement (47, or 48 with the split) is larger than control movement (31; control2: 36).** By the file's
  test that is a measurable difference. **Noise floor** (control2 attempt 3, run at EJ's word after two failures): the
  two control runs disagree on **11** of 140 rows. The new pass disagrees with them on **26** and **21**. On the 129
  rows where both control runs agree, the new pass gives a different tag on **16**. *My reading:* the new rules change
  about twice as many rows as running the same tagger again does — a real but modest effect, n=1 per pass. (An earlier
  draft of this file read the noise as 20 rows from control2 attempt 1, a sheet that had failed a plant; the valid
  sheet gives 11, so that reading was too pessimistic.)
- *My reading:* most of the control's movement (27 of 31) is old `reported` → `verified`: a blind tagger reading a
  primary quote calls it `verified`, which is what s5's local convention ("performance claims stay `reported`") had
  overridden. Both passes undo that convention, so **both** unify the Zep pair; the new pass alone splits the Mem0
  trio, and R014's own Finding text says "vendor-run benchmark, so reported, not verified" — a row whose label leaked
  into its text (`blind/leaks.txt` lists R014). The sharp test was decided by a leak, not by the rule. control2 also unified both pairs (all `verified`).
- *My reading:* the new pass's 7 verified → unknown rows are mostly rows that record a disagreement (R003, R045) or
  whose quote does not contain the claim (R115) — the new `unknown` and "the row must show what was inspected" at work.
  Not checked row by row.
- **Plant PB** (a blog citing an arXiv paper with a link → `reported` under both meanings) was missed once, by
  control2 attempt 1 (`unproven`). *My reading:* under the old meanings "claimed without evidence" can also be read
  onto that row, so the plant was less clean for the control than I judged when writing it.

## What this does not establish

- That the new rules are *better* than the old: they change about twice as many rows as one re-run of the same tagger,
  but changing a tag is not the same as getting it right — no row was checked against its source.
- Anything about researchers who read the sources: both taggers saw only the row text (U6).
- That the blind held beyond what the audit shows: dsh could read the repository by absolute path; the audit saw no
  such read.

## After the run

EJ, 2026-10-13: replace plant PB. `run_pass.py` now carries a survey paper that reports another paper's measured result
with its table — a secondary source with a locator. The results above used the first PB; they are not re-run.
