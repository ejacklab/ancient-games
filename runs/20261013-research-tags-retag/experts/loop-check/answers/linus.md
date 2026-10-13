# Linus Torvalds — Can these checks accept wrong results?

## Answer

R4 — **strengthen the check:** it accepts every row tagged `verified`; add a separate check of rule application with independently settled examples, and enforce the promised 143-line format.

R5 — **strengthen the check:** require exactly one output shape, actual text for parts and reasons, and review whether splits preserve the original claims; a row containing both `tag` and `split` currently passes but is counted as a single tag.

## How I decided

1. **My #2 — inspect the implementation.** The COO, Claude, wrote `check_sheet.py` and `count.py`. I ran my own in-memory probes against those scripts without writing files. Both modes accepted 143 rows all tagged `verified`. R5 also accepted duplicate split claims, a row containing both `tag` and `split`, and a stuck row whose reason was JSON `null`. R4 accepted an extra blank line. These probes establish acceptance behavior, not that any actual tagging pass has made those mistakes.

2. **My #9 — check the relationship between the data shapes.** R5’s validator accepts `tag` plus `split` because its split branch does not exclude other shapes. The counter checks `tag` first. In my probe, the validator passed a two-part split, but the counter returned `moved`, ignoring the parts. **My reading:** require mutually exclusive shapes and test accepted records through the actual counter. Otherwise EJ can receive incorrect split totals despite a passing check.

3. **My #2 and my #7 — challenge what a pass establishes.** A permitted label does not establish correct application of either definition set. Under the new definitions, tagging a bare vendor performance assertion `verified` can be wrong even though the record passes. Two identical split parts can also pass without separating two claims. **My reading:** add fixed cases whose expected answers were settled independently of the tagger, covering these distinctions. Passing those cases would demonstrate rule application on those cases; it would not establish correctness across all 143 rows.

4. **My #3 — follow the result EJ uses.** The relevant workflow ends in same/moved/split/stuck counts and their interpretation. Control drift measures disagreement with historical labels; it does not identify which label is correct. Byte-identical recounting can faithfully reproduce mistaken classifications. **My reading:** use the control for its stated comparison purpose, and check tagging correctness separately if correctness is part of acceptance.

5. **My #5 — keep the repair reversible.** Strengthen validation and preserve both sheets and the historical key. Do not repair the comparison by changing old labels, fetching additional evidence for one pass, or silently changing definitions. Those actions would change what the experiment measures.

6. **My reading — requirement check.** For the declared format gates: **source PASS** (COO named); **one thing PASS** (accepting one sheet); **unit PASS** (143 rows and explicit cardinalities); **can it fail PASS** for malformed records, but insufficient for wrong classifications; **weak words R4 PASS, R5 FAIL** because a “part” or “reason” lacks a substantive acceptance test; **level PASS** (failure stops acceptance); **basis PASS** for the documented structural fixtures, while semantic adequacy remains **not measured**; **links PASS** for the stated R4/R5 relationship. Structural falsifiability alone does not make either classification check sufficient.

## What I need to know

- Is acceptance meant to establish a complete, countable sheet, or correct tagging of every finding? If only the former, repair the structural defects and explicitly limit the conclusion.
- Who settles expected answers for the separate rule-application cases, and what disagreement sends them to EJ?
- What makes a split preserve the original claims, and what makes a stuck reason explain an unresolved choice? Those acceptance criteria are currently open.

## Costs and risks

- **My #9:** exclusive shapes and strict text types add validator work and may reject outputs that currently pass; they prevent the demonstrated validator/counter disagreement.
- **My #2 and my #7:** independently settled cases require preparation and adjudication. They can expose systematic mistakes but leave unchecked rows uncertain.
- **My #3:** reviewing every row would cost more than checking examples. If EJ needs correctness of every tag, a sample cannot establish that result.
- **My #5:** preserving history costs storage and leaves two definition sets to explain, but keeps the comparison recoverable.

## How we would know I was right

The strengthened validator rejects `tag` plus `split`, duplicate split claims, null reasons, and extra blank lines. An accepted split reaches `count.py` as exactly one split outcome.

Separately, a deliberately wrong but structurally valid tag fails the agreed rule-application check. A valid answer passes it without requiring agreement with historical labels. Until that distinction is demonstrated, a schema pass establishes a countable sheet, not correct tagging.