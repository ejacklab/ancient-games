I'll read that brief first.
Now let me read all the referenced source material.
Let me verify two things the answer depends on: the old definitions at `HEAD`, and whether the leak count is a floor or a total.
Two surprises. Let me pin both down.
The column order tripped my parse. Re-running, and reading the workflow file's actual state.
Now the important one: whether the old definitions still exist anywhere at all.
One last verification: the exact leak rows and their text, so my counts are checkable.
# 老子 (Laozi) — which spots answer to subtraction

## Answer

**U1 and U8 cannot be resolved at all, only given up**: `.claude/workflows/research-agent-memory.js` was never committed (`git show HEAD:…` → *exists on disk, but not in HEAD*), and its pre-edit text survives nowhere in the repo, so the control's four definitions live on only as a *quotation* in `runs/20261013-four-experts-relay-tags/facts.md:20-21` — give up the step "prove what the control was, from the file" and keep "quote a named source and say that it is a quotation" (my #1). Beyond that, what may go is three claims and two rows, not the pieces — the control pass, the prediction, the stuck-row split and R2's fixture each carry the use, not the excess (my #17); every verdict below is a question for EJ, not a removal.

- **U1 — give up the proof, keep the quotation.** (my #1) Ask EJ: take the four definitions as quoted in `facts.md:20-21` and label them a quotation. Lost: the control's wording is second-hand, so if the run-1 taggers were handed a slightly different sentence, some part of the measured drift is that sentence, and nothing in the repo can now detect it.
- **U2 — give up the in-place rewrite of the sentence naming `verify/sections/`.** (my #3 with my #7) That sentence records what was owed; R6's result block sits in the same file and can carry the true path. Lost: `grep verify/sections docs/RESEARCH_TAGS.md` still returns the wrong path — the correction is one click away instead of zero.
- **U3 — nothing to give up.** The answer is given and no check in the design reads the folder's name.
- **U4 — keep EJ's answer; know which half is load-bearing.** The design's operative rule is "same engine, model and effort in both passes"; the tier name carries none of the use (my #17). If the tier is ever questioned, drop the name, not the sameness.
- **U5 — give up the claim, keep the count, and correct the figure.** (my #8) Ask EJ: accept that the blind was enforced by instruction only, and print a floor, not 13. Lost: the sentence "the taggers saw nothing but blind rows".
- **U6 — keep; no subtraction buys it.** (my #8, my #4) Any step that hid this — dropping the control, dropping the split count — would improve the numbers without improving the rule.
- **U7 — keep.** Already paid for.
- **U8 — give up the ordering constraint.** (my #1, my #4) It existed only to protect a quote taken from that file; the quote now comes from elsewhere, and A has already been applied. Lost: nothing.
- **U9 — keep.** One mapping line is the smallest sufficient fix (my #2).
- **N1 (new) — give up "force every row into one of four outcomes" for two rows.** `s2 F18` and `s4 F27` are `CONTROL — NOT FOUND` gaps, both labelled `verified` inside the 94; `docs/RESEARCH_TAGS.md` says a search that found nothing is gap prose and carries no tag. Ask EJ: count 141 and list the two by id. Lost: the headline denominator is no longer 143, and the two rows keep an old label on disk that the new rule would not give them.
- **N2 (new) — give up the `sha256sum` if the run folder is not committed.** (my #17) A hash of a file inside an uncommitted folder is a hash the same hand can remake; the witness must sit outside the run. If EJ commits the folder, keep the hash — then it is a cheap copy of a witness that already exists.
- **N3 (new) — give up A's "before", and call the "after" a state, not a check.** (my #1, my #7) Once the old wording is gone, `grep -c` → 0 cannot fail. Lost: the before/after pair; `evidence/A.txt` becomes a statement about the present file plus a quotation from another run.
- **N4 (new) — keep R2's fixture.** (my #2) Six rows is the least sheet that touches every branch the counter has, and the COO wrote the counter, the tags and the key; the fixture is the one thing in the run that is not her own account of her own work (my reading, applying my #16).

## How I decided

1. **I looked instead of taking the brief's facts for the whole answer** (my #8 — the sage is not sick because he treats the sickness as a sickness). The brief gave me the old definitions as "quoted from git `HEAD` of the `.js` (U1)". They are not there.
2. **Subtract once, then subtract again** (my #1:損之又損, an algorithm with a repeated step and an end point). For every spot I asked twice: what goes, and then what the removal still leaves that has to be named instead.
3. **The test for excess** (my #17, turned on a workflow — my reading: 三十輻共一轂, 當其無, 有車之用). A step's use is what it leaves out. Where the thing left out *is* the function, the step is not excess: the control's use is the hole it leaves in the claim about movement; the prediction's use is dated, not summed.
4. **Sufficiency, not completeness** (my #2: 知足不辱, 知止不殆). Where a smaller action does the whole job, the larger one is the loss.
5. **Fact 1 — the control's source is gone.** `git status --short` → `?? .claude/workflows/research-agent-memory.js`; `git show HEAD:.claude/workflows/research-agent-memory.js` → *fatal*; `git cat-file -e HEAD:runs/20261013-four-seats-relay-tags/facts.md` fails too, so the run folder is untracked as well. A repo-wide grep for the old wording returns only quotations inside `runs/20261013-four-experts-relay-tags/`. That is the record I have (my reading).
6. **Fact 2 — A is already applied.** Lines 64–65 already read "defined in `docs/RESEARCH_TAGS.md` (the one copy…)" and lines 82–83 already carry the vendor-blog `unproven` example; the old wording is absent; mtime 21:10:02, two minutes after `workflow-design.md` at 21:08:14; `state.md` still says `todo`. So U8's ordering has already been spent, and A's before/after pair cannot be shown (my #7: the value sits at the end, and here the end has passed without the check).
7. **Fact 3 — the leak figure is a floor, and a wrong one.** Over the 143 rows I count **14** whose Finding cell carries a tag word, and **2 more** (s3 F22, s5 F19) that carry it only in the Source cell, which `blind/rows.md` also shows the tagger: **16 rows**, against readiness's 13. Lost or miscounted, I cannot say which; that is EJ's to settle, and it is a number, not a feeling.
8. **Fact 4 — two rows are not rows.** `s2 F18` and `s4 F27` are `CONTROL — NOT FOUND` search records, both labelled `verified`. Under `docs/RESEARCH_TAGS.md` a search that found nothing is gap prose and carries no tag. Forcing them into one of four outcomes is gripping the whole total (my #4: 天下神器, 不可為也).
9. **What I did not do.** I did not judge whether the new definitions are any good — they are EJ's, and my #8's sickness is not mine to cure. I did not re-run the harness or pytest; both would touch the tree.

## What I need to know

1. Does the pre-edit text of `research-agent-memory.js` survive anywhere I did not look — another run folder, a transcript, an editor backup? If yes, U1 can be **resolved** instead of given up, and the control quote becomes first-hand.
2. Does EJ accept a second-hand quotation as the control's definitions? That is EJ's call and it decides whether N1–N3 stay proposals or become the plan.
3. Will the run folder be committed at the end? Decides N2.
4. Are the two `CONTROL` rows to be counted? Decides N1's denominator.

## Costs and risks

- **Quoted instead of read** (my #1, my #2): the control measures a sentence, not the file the 143 rows were labelled under. A reader who trusts the number more than the caveat will over-read the movement figure.
- **Give up the ordering (my #1):** nothing in this run; a later re-run of R1 after A's edit commits would silently get the *new* definitions as the control. The residue is a commit id to name, not a schedule to keep.
- **Give up A's "before" (my #7):** the run loses the ability to prove it changed what it says it changed. The failure it was guarding against — old text left behind in `SHAPES` — becomes a present-state observation only.
- **Correct13 to ≥16 (my #8):** the headline looks worse and is still not a measurement of the leak's effect. Printing a floor invites the reading that the movement number is contaminated, which is true and unquantified.
- **Count 141 (my #4):** two fewer rows of evidence, and a diff against run2 will show two rows carrying labels the new rule refuses. The gain is that neither pass is forced to invent a tag for a gap.
- **Drop the hash (my #17):** if the folder is never committed, nothing outside the run remembers the prediction existed. The Log line remains the only witness, in a file the same hand can edit.
- **Keeping the fixture, the control and the prediction** costs three dsh calls, one script and one file. Under my #10's third treasure — 不敢為天下先 — I am content to be behind on price here.

## How we would know I was right

- **U1/U8:** `git show HEAD:.claude/workflows/research-agent-memory.js` fails, and a repo-wide grep for the old four-label wording hits only quotations inside `runs/20261013-four-experts-relay-tags/`. If a first-hand copy turns up, I am wrong and U1 needs resolving rather than giving up.
- **N3:** before anything runs, `grep -c "the primary document was read"` on the workflow file returns 0 while `state.md` still says `todo`. If someone shows a state in which that grep was 1, the ordering was intact and my reading of the mtimes is wrong.
- **U5:** after R1, `blind/leaks.txt` should show 16 rows if it counts the Source cell and 14 if it does not. Either number is not 13; which one appears says exactly what was counted.
- **N1:** after both passes, the two taggers' sheets each assign one of the four tags to the R-ids for s2 F18 and s4 F27. That tag is the observable — it is the rule forced onto something that is not a row.
- **U2:** after R6, `grep -c "verify/sections" docs/RESEARCH_TAGS.md` — if it is still 1 and the result block names `docs/research/…`, my verdict was applied; if it is 0, EJ chose the rewrite and nothing of mine is lost but the tidiness.
