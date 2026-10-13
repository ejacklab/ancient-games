# Dave — smallest experiment, prediction and stop for each unknown spot

## Answer
Only **U5** is marked *unknown*. Its smallest experiment needs no new engine call. When R6 runs, the leak rows and any off-brief file reads get checked against data the run already keeps. I also raise **N1** (whether a split counts as a move), **N2** (one control pass cannot separate tagger noise from information loss), and **N3** (state.md is behind the run). Each of the three is a question for EJ, not a change I make.

- **U5 (unknown).** Run two read-only checks at R6, both on files the run already saves:
  - (a) Compare the 13 leak rows with the other 130, in both passes.
  - (b) Check each pass for any file the tagger read beyond the two the brief names.

  Prediction, written now: (a) when a leak row's Finding contains one of the four tag words, the tagger's tag matches that word more often than it does elsewhere. (b) No other file is read, and the control pass does not reproduce the old labels row for row.

  Stop: one run of each check at R6, with no repeats. The size of difference that would count as "the leak matters" is EJ's to set and stays open.
- **N1 (new, a decision for EJ, not an unknown).** The control brief allows one tag per row, so the control pass cannot split a row or mark it stuck. `count.py` counts only single-tag changes as *moved*. Step 6's test, "moves no more rows than the control pass", does not say whether splits count. This has to be settled before R3, because the prediction must fix the metric first. No experiment answers it.
- **N2 (new, unknown).** The control pass's drift mixes two things: tagger noise, and what was lost because the old labeller read the sources while the blind tagger sees only the row (U6). The smallest experiment that separates them is a second control pass: same brief, a fresh session, output to `tags/control-2.jsonl`.

  Prediction: the two control passes disagree with each other on fewer rows than either disagrees with the old labels.

  Stop: one extra pass, attempt limit 2 as in R4, and a schema failure is reported, not retried further. It is a third pass beyond what `RESEARCH_TAGS.md` prescribes, so EJ decides whether to run it. How much noise is "too much" stays open.
- **N3 (new, information found; no experiment).** state.md marks every piece `todo` and its Log has only the design line. But `evidence/` already holds R1, A, B and R2 outputs, plus the sheet-check output, timed 21:09 to 21:11. The design also says R1 quotes from `git show HEAD:`, but `research-agent-memory.js` is untracked. `make_blind.py` read the working file instead and recorded its sha256. The COO should bring state.md and the design text up to date before R3.
- **U1–U4, U7–U9** are not unknowns, so I have no experiment for them; EJ's "go" settled them. **U6** stays an accepted limit, but its effect on the reading is what N2 measures.

## How I decided
1. My #1. For U5, the observation that would settle it is whether tags follow the leaked words and whether any off-brief file was read. If the control pass reproduces the old labels 143 of 143, I would read it as copying, not agreement.
2. My #5. Before anything new, I took stock of what is already measured. `blind/leaks.txt` lists the 13 leak R-ids. `key/old-labels.json` holds the old labels. The R4 and R5 sheets and `raw/` outputs will be saved. That is enough for U5(a), and possibly U5(b), with no extra engine call. It does not show whether dsh actually opened other files unless its raw output records file reads (see "What I need to know").
3. My #2. A new engine run on U5 (re-running the passes with the repository out of reach) would cost more than reading the saved outputs. So the U5 experiment is the read-only check.
4. My #4. I looked at what the control pass is compared against. It measures drift from labels made by a researcher who read the sources. The blind tagger sees only the row (U6, `briefs/R4-control.md`: "Judge from the row"). So control drift equals tagger noise plus information loss. A control compared with a control isolates the noise, which gives N2.
5. My reading, from the briefs and `count.py`. R4's output allows only `{"id","tag"}`, while R5's allows `split` and `stuck`. `count.py`'s `outcome()` puts a split row under *split*, not *moved*. Step 6 compares *moves* only, which gives N1.
6. My #3. Each prediction above is written before any tag sheet exists: `tags/` and `raw/` are empty and `prediction.md` does not exist yet. If EJ accepts N2 or U5, these lines belong in `prediction.md` next to the COO's R3 prediction, with R3's stop date. I do not set a date.
7. My #8. Every experiment is reversible. U5 only reads saved files. N2 adds one file, `tags/control-2.jsonl`, which can be deleted, and edits nothing outside the run folder.
8. My #6 and #7. I looked for a living system with the same problem, telling a change's effect apart from the noise of the observer. I found none whose mechanism fits better than a plain replicate, so I borrowed nothing.
9. My #9. A null U5 result (no difference in the leak rows) and an N2 result where the two controls disagree as much as either does with the old labels both get reported at the same weight as the totals.
10. My #10. Every prediction here is n=0. Each pass is n=1 per arm, so any difference between the two passes is a hint, not a law. The 13 leak rows are a small group, and a difference there is a hint at most.
11. My reading, from a check I ran. The text in `blind/control-defs.md` matches word for word the quote in `docs/RESEARCH_TAGS.md`, step 3 (EJ's). So the missing git `HEAD` copy (N3) does not put the control definitions in doubt.

## What I need to know
- Does `dsh headless` write a transcript of its tool calls (file reads) into the raw output or a session log? If yes, U5(b) is a grep of that log. If not, U5(b) can only fall back to the indirect sign: the control pass matching the old labels row for row.
- N1: in step 6's comparison, does a split count as a move? If it does, the new-rule pass will almost certainly "move more", because the control cannot split. If it does not, the comparison leaves out the rule's main new effect. That is EJ's choice, and it must be made before R3.
- N2: does EJ want a third pass (a second control)? `RESEARCH_TAGS.md` prescribes two.
- Thresholds that are EJ's and that I leave open: how large a leak-row difference counts as the blind being broken (U5), and how much control-vs-control disagreement counts as too much noise to read the comparison (N2).

## Costs and risks
- **U5 checks (my #5, #8).** Close to free: two script runs on saved files at R6. The risk is that 13 rows are too few to show anything (my #10). A null result is likely and has to be reported as a null (my #9), not as "the blind held".
- **U5(b) without a transcript (my #1).** The indirect sign is weak. A control pass that copies part of the old labels would not be caught.
- **`key/` sits next to `blind/` (my reading).** It is in the same run folder, one `ls` away, and only the brief keeps the tagger out. Moving it out of the repository during the passes would cut that exposure, but it conflicts with "evidence lives in `runs/<run-id>/`" (CLAUDE.md, SHOULD). That trade is EJ's.
- **N2 second control pass (my #4).** One more engine call at the design's estimate of about 25–40k tokens (unmeasured, n=0), and up to two calls with a retry. It goes beyond the file's prescribed two passes. It also risks inviting the argument over the number that step 6 forbids: "Do not argue the number."
- **N1 (my #3).** If it is not settled before R3, the prediction's metric is ambiguous. Then the R3 time check can pass while the prediction cannot fail.
- **N3 (my #9).** If state.md stays behind, the resume point is wrong: a restart would redo R1, A, B and R2. It also weakens the R3 record, whose order evidence is the state.md Log.

## How we would know I was right
- **U5(a).** At R6, a table of the 13 leak rows against the other 130, per pass: the share of rows whose tag equals a tag word in the Finding text. My prediction holds if that share is higher in the leak rows. It fails if the share is the same or lower.
- **U5(b).** If dsh logs reads, a grep over each pass's log shows no file other than the brief and `blind/rows.md`, and the control pass's agreement with the old labels is below 143 of 143. One read of `key/` or `docs/research/…FINDINGS-s*` voids that pass, and that is reported as a result.
- **N2 (if run).** A `count.py`-style comparison of `control.jsonl` with `control-2.jsonl`. I am right if they disagree with each other on fewer rows than either disagrees with the old labels. I am wrong if the disagreements are about equal, which would mean the control's drift is mostly noise and the information-loss story (U6) adds little.
- **N1 and N3.** Before R3 starts, `prediction.md` names whether splits count as moves, and state.md's Steps table and Log match the files in `evidence/`.
