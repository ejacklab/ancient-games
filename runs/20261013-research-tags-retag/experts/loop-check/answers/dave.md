# Dave — are the R4/R5 loop checks real, and what is their control?

## Answer
- **R4 (control pass): strengthen the check.** The schema check does fail when it should, and its control (a plant) is already shown. But it only checks the shape of the sheet, not the tagging: I ran it on a sheet tagging all 143 rows `verified` and it passed. Before the loop counts as done, add three things. (a) Check that the tagger read only its two files. (b) Treat an exact match with the key as a sign it read the key. (c) Give both briefs the same worked-example row, so the control differs from R5 only in the definitions.
- **R5 (new-rule pass): strengthen the check.** It has the same blind spot, plus two degenerate sheets that pass. I ran both: a sheet with all 143 rows `stuck` passes, and so does a sheet of `split`s whose two parts have the same text. R5 also runs after `tags/control.jsonl` exists in the repository, which it can read. Fix this by moving that file out of reach during R5, by requiring split parts to have different text, and by comparing the two sheets for an exact match after R5.

## How I decided
1. **My #1.** What would show this check can fail? A bad sheet it rejects, next to a good sheet it accepts. `evidence/R4-R5-check.txt` has both for each mode. The bad control sheet (fifth label, missing id) fails with 2 lines. The bad new sheet (one-part split, stuck naming the same tag twice) fails with 2 lines. The good sheet passes in both modes. So as a schema check it is real.
2. **My #4.** The schema check's control is the planted fixture, and that exists. But the loop's purpose is a usable tag sheet, and the schema check has no control for content. The only content control is R6: the original labels (94/44/3/2) and the R4-against-R5 comparison. That sits outside the loop. So the loop can exit as a success on a worthless sheet.
3. **My #2.** Asking whether degenerate sheets pass was cheaper to test than to argue. I wrote throwaway sheets to my scratchpad (I did not change any repository files) and ran `check_sheet.py` on them, once each (n=1). Results:
   - all 143 `verified` in control mode: **PASS**
   - all 143 `stuck` in new mode: **PASS**
   - 143 splits whose two parts have the same text, each line with an extra key: **PASS**
   - code fence around the lines: fails ("not JSON")
   - duplicate id: fails
   - extra field on a tag line: fails
   - a JSON list as a line: crashes with a Python traceback. That still fails loud, but the feedback for attempt 2 is a traceback, not a message.

   So the likeliest real LLM mistakes (a fence, a duplicate) are caught. The cheap ways to fake a good sheet are not.
4. **My #4, again (what the control is).** R4 is meant to be "the current way" that R5 is judged against. But the R4 and R5 briefs differ in more than the definitions:
   - R5 also allows `split` and `stuck`.
   - The worked examples differ. R4's is an arXiv paper quoted → `verified`. R5's is a vendor blog → split.

   A difference in movement could come from the example or the allowed output shapes rather than the definitions. Using the same example row in both briefs, each answered under its own definitions, removes one of those two confounds for the price of one brief edit.
5. **My #4 (plant), applied to the blind.** The blind is by instruction only (U5). dsh can read `key/old-labels.json`, and R5 can read `tags/control.jsonl`. Neither schema check can see a peek: a copied key or a copied control sheet passes. It shows up only as an exact match: R4 agreeing with the key on 143 of 143, or R5 identical to R4. My reading: an exact match is a warning sign, not proof of a peek. The direct evidence would be the dsh transcript of which files were read.
6. **My #10.** Each pass runs once. R4-against-R5 is one run against one run. How much deepseek-flash at low effort moves from one run to the next is not measured. Without that, a gap between the passes cannot be told apart from noise. A second control pass in another fresh session would measure it. I list this under costs; it is not a condition for the loop.
7. **My #3.** `prediction.md` (R3) is not yet in the Log. When it is written, it should also say in advance which results void the comparison: evidence of a peek, R5 identical to R4, a sheet that is almost all `stuck`. Then nobody decides this after seeing the counts.
8. **My #9.** If any of the above happens, it is a result for `result.md`, reported with the same weight as the counts, not something to fix quietly.

## What I need to know
- Does `dsh headless` record which files it read or listed, in a form the COO can grep? If yes, then (a) is a short grep. If no, then (a) needs a different check, such as a canary in a file the tagger must not read. A canary costs more: it touches the key, and the COO must then exclude it from R2's counts.
- Who writes `tags/control.jsonl`: the engine directly, or the COO from the raw stdout? If the COO extracts it (for example by stripping fences), the check is checking the COO's extraction and not the tagger's output. The raw output in `raw/` would then need the same check.
- Is attempt 2 a fresh session or the same one? If it is the same session, a retry after a missing-id failure may patch only those ids, which is fine. If it is fresh, all 143 rows are re-tagged and the attempt-1 sheet should be kept in `raw/` as data.
- Can dsh read outside the repository? If it can read anywhere on disk, moving `control.jsonl` aside only works if it goes somewhere dsh cannot reach, or is deleted until R6 and restored from a copy.

## Costs and risks
- **Transcript grep for files read (my #4):** minutes of COO work. Risk: dsh may not record reads, and then a clean grep proves nothing (see above).
- **Exact-match check after each pass (my #4):** one line of script, no real cost. Risk: an honest tagger could in principle match the key exactly. My reading: that is unlikely across 143 rows under changed instructions, but it is not measured.
- **Same worked example in both briefs (my #4):** one edit to a brief that is already written, plus re-checking it. Risk: under the old definitions the vendor-blog row is plainly `verified`, which shows the control a split it is not allowed to make. That is the point, but it makes the R4 brief slightly longer.
- **Moving `control.jsonl` out of reach during R5 (my #4):** one move and one restore. Risk: forgetting to restore it before R6. A check at R6 for byte-identity with a saved hash covers that.
- **Different text in split parts (my #2):** one condition in `check_sheet.py`, and its fixture needs a matching bad row (my #1), roughly 10 minutes. Risk: the COO writes and tests it, so it is not independent evidence.
- **Optional second control pass for the noise floor (my #10, #2):** about 25–40k tokens on the cheap tier (the design's estimate, unmeasured, n=0), plus one engine call. Risk: it adds a sheet to count, and R2's script must take a third sheet or be run twice.
- **Leaving the checks as they are:** the loop can report done on an all-`verified` control sheet, a copied key, or an all-`stuck` new sheet. Each would surface only at R6, after the passes are spent, and the R4-against-R5 reading would rest on n=1 against n=1 with no noise floor.

## How we would know I was right
- **Before the run:** rerun my degenerate sheets (all `verified`, all `stuck`, same-text split) after the change. The same-text split should now fail. The other two still pass the schema by design, and they should be caught by the exact-match and void-condition checks written in `prediction.md`.
- **After the run:** the dsh transcript lists reads of only the brief and `blind/rows.md`. R4's agreement with the key is below 143 of 143. R5 is not byte-identical to R4. If a second control pass is run, the number of rows that moved between the two control sheets is the noise floor, and R5's movement against the original labels is read against it. If R5's movement is inside that floor, the comparison without a floor would have misled us, and that bears out step 6.
