# Review of the merge — COO (Claude, `claude-opus-5-5`), 2026-10-12

**This review is not independent.** I wrote Version B's measured section, and I wrote the merge brief that bound dsh.
Line numbers refer to `merge/CACHES.merged.md` after the two leftover fixes. The dsh original is kept as
`merge/CACHES.merged.dsh-original.md`.

## Verdict

The merge is a clear improvement on both inputs:
- It keeps both routing tables, each scoped to its corpus.
- It fixes every error the reviewers agreed on, where the fix already existed in A or B.
- It leaves the four real disagreements as positions.
- It invents nothing: all ids and numbers trace to A or B.

It is **not ready to accept as is**. Three findings would make a builder or an agent act wrongly (high). Four more
are medium.

## Findings

### High: a reader would act wrongly
1. **Three different staleness rules.**
   - The cache rules (l.154) and R3.1 (l.362) say to compare a recorded commit or content hash, so that a deletion is
     caught.
   - The SQLite 5W1H "How" row (l.198) still says "compare modification times".
   - R2.2 (l.358–359) still says "newest source file's mtime or the commit".

   A builder following l.198 would miss deleted entries, which is exactly the failure codex found (R2 #6). All three
   places should name the commit or content hash.
2. **The drift check contradicts itself.**
   - Part 1, row l.79, gives the command `git log -1 --format=%at` on the entry (its last edit), then says "rebind this
     to the entry's verification, not its last edit".
   - The code-graph "How" row (l.270) does the same.

   The command shown measures the baseline the text rejects. The fix is the entry's recorded verification revision
   (`SOURCE_OF_TRUTH.md`'s entry header holds "the date and git revision it was last verified against"), compared
   against changes to each `covers:` path since that revision. Neither A nor B wrote it that way, so rule 3 of the
   merge brief kept dsh from writing it.
3. **One question, two routes.** "Which tests reach function F" and "what does changing F reach" are code questions,
   but they appear in both tables:
   - **Part 1** (l.72–73): code graph only after its trigger; otherwise grep test names and run the suite.
   - **Part 2** (l.127): code graph plus full-text now.

   An agent cannot tell which to follow. These two rows belong in Part 2 only, or Part 1 should point to it.

### Medium
4. **l.133 says Part 1 "is unchanged".** It is not: three citations were corrected in the merge (merge-notes).
5. **"Why no SQLite is visible" (l.104) misses the fact that answers EJ's question most directly.** Three SQLite caches
   were built today, in `runs/20261012-caches-routing/bench/.cache/` (9.5, 10.2 and 4.9 MB, BM-9). All three
   reviewers agreed this should be said (opencode R2 #1, codex R2 #5). Rule 3 kept it out, because the file names occur
   in neither A nor B.
6. **D1–D6 are presented as wholly unresolved (l.99–102).** For code and docs, B's measurements settle three of them:
   - **D1:** full-text before vector (BM-4, BM-5);
   - **D2:** the full-text benefit is measured on docs (BM-4, BM-6);
   - **D3:** grep's printed cost is about 4,470 characters to the right file, not ~226K tokens (BM-4).

   For memory entries they stay open. The merge does not say this, so one of B's main strengths is lost at this point.
7. **R5.2 (l.380 and l.382) states the vector trigger two ways.** One line says "the logged misses outweigh the cache's
   cost"; the next says the miss count is EJ's number. The first wording is A's draft phrasing, which the reviewers
   flagged as making a draft rule operative (opencode R2 #2). Keep only "EJ's number".

### Low
8. **The provenance block (l.5–8)** still credits the whole file to `claude-opus-5-5` from the three research nodes.
   The status line above it corrects this, but the block reads as if it describes the merge.
9. **The speed bound:** two of three reviewers (codex, agy) agree that grep's `git ls-files` overhead should be
   *disclosed* next to BM-9. The merge put it in "Unresolved" instead of disclosing it.
10. **Formatting:** l.316, l.318 and l.378 run past the 120-column wrap, and l.329 is a short orphan line.

## The process, briefly
- **The inputs overlapped:** A already held B's measured section (`verify/check.md`). The comparison was "both" against
  "B", not two separate drafts.
- **agy's discussion was one-way:** codex and opencode never answered it.
- **Rule 3 ("invent nothing") was right but cost something.** It stopped invented numbers, and it also blocked three
  corrections the reviewers agreed on (findings 2, 5 and 6), because their wording or values were not in A or B. Next
  time, the rule should also allow values taken verbatim from the cited sources (results files, `SOURCE_OF_TRUTH.md`),
  with the trace check extended to read those sources too.

## Outcome (2026-10-12, after EJ: "yes fix them")
The high findings 1–3 and the medium findings 4–7 are fixed in `merge/CACHES.merged.md`. The state before these fixes
is kept as `merge/CACHES.merged.before-review-fixes.md`.
- **1 (staleness):** the SQLite "How" row and R2.2 now name the recorded commit or content hash. R2.2 says why mtime
  is not enough.
- **2 (drift check):** one command, `git log <verified-rev>..HEAD -- <covers paths>`, used in Part 1, in the
  code-graph section's why 3 and "How", and in "What this changes elsewhere". It is labelled *my reading*, and its
  baseline is cited to `SOURCE_OF_TRUTH.md` l.50.
- **3 (one question, two routes):** the two code rows left Part 1 for a pointer row. "What does changing F reach"
  moved to Part 2, marked *not measured here*.
- **4:** Part 1 is now described as reasoned, not measured, with three citations corrected.
- **5:** the three SQLite caches built today are named, with their location and sizes.
- **6:** D1–D3 are marked settled for code and docs (my reading, with BM ids), and still open for memory.
- **7:** R5.2 now reads "the miss record reaches EJ's number".
- **Also:**
  - long lines were rewrapped (low finding 10);
  - the status block now records this correction (low finding 8, partly).

  Low finding 9 (disclosing grep's overhead) is not done.

**Trace check after the fixes:** all 113 numbers trace to A or B. One id, `D2`, is not in A or B as a token; it is
the run record's D2 (`runs/20261012-caches-enhance/DECISION-RULES.md`). The never-rules are present, and no shared
file changed. **Not re-reviewed by anyone independent.**
