The method is not lean. Its core steps hold up. The extra weight is the history of rules that were deleted or changed, kept inline, and the same rule restated in every section it touches. I counted the line ranges by hand; together these ten changes would remove about 150 of the doc's 579 lines (roughly a quarter) without dropping a rule. I wrote the list to `runs/20261008-optimize/claude.md` and edited nothing else. I didn't read the other engines' files.

**The 10 cuts, highest value first**

1. **3.7, lines 395–423 (optional):** the story of the deleted caps rule and the concurrency table. That's about 29 lines about a rule that no longer exists, and the point about naming the unit already lives in `EXECUTOR_KINDS.md:327`. Keep one line pointing there.
2. **3.6, lines 353–370 (optional):** how the decision to compare the design with the plan was made and then revisited. Keep 3 lines: they are two artifacts, `dispatch.py validate --design` compares them, and the plan may add but may not lose. The history belongs in `DECISIONS.md`.
3. **The blueprint "not answered by silence" rule (duplicate):** it appears four times, each worded a little differently, so a reader has to check they agree. Keep it in 3.1 (lines 177–183) and replace the copies in 3.3, 3.4 and 3.6 with "(3.1)".
4. **Splitting and hand-off cost (duplicate):** "every hand-off costs something" and "a segmented run is healthier" are each stated about three times, across §1, 3.2, 3.4 and 3.8. Merge them into one paragraph in 3.4 on how big a piece should be.
5. **Copies of sibling docs (duplicate, about 45 lines):**
   - 3.8 items 9–12 are about how to run the reading roles, not how to design; they belong in `EXECUTOR_KINDS.md`.
   - The bundled-runtime warning is already at `EXECUTOR_KINDS.md:90`.
   - The 20% rule in 3.4 is already at `TASK_TYPES.md:31`.
6. **The 19 inline "(Added … at EJ's request; n=0)" tags:** collapse them into one table at the end. The header on lines 4–7 is also out of date: it lists only 3.0 and 3.5 as n=0, but about ten sections are.
7. **3.0, lines 73–75 (duplicate):** the tiny test is already stated in §2.
8. **3.5 (duplicate):** moving to a stronger model tier is described twice in the same section (item 4 and lines 297–301). Merge them.
9. **Low priority:**
   - The git paragraph that opens 3.1 (lines 85–91) can become one line.
   - The "anchors for 3" in 3.4 (lines 272–274) can move to an appendix; there's also a "the the" typo there.
10. **To an appendix:**
    - The "One word, one job" glossary at the top: it lists function names before the reader knows what a node is.
    - The memory-kinds table in §4.
    - The graph caution in §4.

**Your candidates that are not duplicates:**
- **"Who fills it":** it isn't in the method at all; it's only in `CLAUDE.md`.
- **"One word, one job":** there's one copy; it's just in the wrong place.
- **The loop's five conditions:** not the same list as the five for going parallel in 3.7. They share the "all five" wording, which invites confusion.
- **The three-part stop:** stated once, in 3.6.
- **The check that can fail:** stated once in 3.5; the other mentions are short references.

The **baseline** is the one real duplicate (3.1 and 3.6), and the 3.1 copy goes with cut 9.

**Keep:** the nine steps, the five things a node carries, the state file, the three qualities and the acceptance criteria. One loose end: §5 line 577 still asks for "fixed bounds on … concurrency", but the caps rule was deleted. That word should be re-worded or dropped.
