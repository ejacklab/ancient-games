# Check of the merge (node V) — COO, 2026-10-12

## Script: `verify/trace_check.py`, written by the COO before the merge existed
Output in `trace_check.out.txt`:
- all 82 finding ids in the merge occur in A or B;
- all 112 numbers occur verbatim in A or B;
- all four never-rules are present;
- no file outside this run changed since the baseline.

**What the script does not establish:**
- that a number sits next to the right claim;
- that a copied row still means the same thing;
- that this is the *best* version.

## Read by the COO: the rewritten parts, spot-checked against the reviews and sources
- The **BM-4** graph cell now reads `0.0 (over 2 questions)`. That matches `routing/bench/results.md` category D
  (graph 0.0 over 2).
- **BM-7** is now labelled as the macro-average test-file recall, n=4. That matches `cov/derive_maps.py` and
  `nodes/runtime-recall.json`.
- The **freshness rule** now compares a recorded commit or content hash, not the newest mtime (codex R2 #6: a deletion
  leaves no newer file). This is a design change, raised by codex and accepted by agy and opencode.
- **"The answer first"** is now scoped to memory entries. The code-and-docs expansion is a proposal for EJ.

## Residual defects, not fixed: the merge is dsh's output
1. The header note "Measured enhancement … It does not change the sections above or below it" is now stale: the
   merge did change them.
2. Line 327 still says the vector index found "4% of the tests that run a function". BM-7 was relabelled as
   test-file recall, but that sentence keeps the old unit.

## Input flaw
Version A already held Version B's measured section (88 lines, 4 differing lines: the one sentence fixed in B). So
the reviewers compared "A, which is both" against "B, which is HEAD plus the measured section", not two disjoint
drafts. The COO did not check this before launching.
