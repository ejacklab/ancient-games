I'll read the brief first.
Brief read. Let me verify the repo facts the copy depends on (read-only) before writing the answer.
One verification of the claim I intend to make about the accepted files' Label column:
# 老子 (Laozi) — one set of tags for research findings

## Answer

I kept the four tags, the split rule and the no-upgrade rule, and took away the rest: the selection rule is now one question with four parallel answers instead of a four-rung ladder, the adoption test now fails only on a row that still stands between two tags, the re-tag set is corrected to the 143 rows of the accepted run, and the stated price is corrected against what those rows actually contain. If EJ would rather keep the ladder's order as the deciding rule, say so — that is the one thing I changed that is not a subtraction.

### The copy

**Status:** Proposal for EJ's decision; not measured (`n=0`). These are proposed SHOULD defaults, with any departure explained by the researcher. The definitions themselves are EJ's; a default may bend in a hard case with a written reason, but a definition may not. Track operational friction during initial use, but do not alter canonical definitions on an `n=1` basis; evaluate adjustments only after the same friction recurs across separate tasks. **Adoption waits on one reckoning:** re-tag the 143 rows of the five findings files in `runs/20261011-agent-memory-graph-r2/verify/sections/` (run 2 is the accepted run; run 1 was blocked at Sections and its five section findings files are not in the repo), writing each row's tag down before looking at its old one. A row that splits into two claims is the rule working, not the rule failing. The rule is not ready only if a row, after splitting, still stands between two tags — `reported` and `unproven` above all. Report the result as a number: how many of the 143 rows moved, and in which direction. This is a first tagging under the new rule, not an upgrade of old labels, so rows may move either way. Do not argue the number.

**Scope:** The researcher assigns one tag to each research finding. The tag describes the evidence available to the researcher for the finding's exact wording; it is neither a confidence score nor a declaration of universal truth. **Primary and secondary are relative to that exact wording, not to the source's reputation:** one document is primary evidence for the claim that it says what it says, and secondary for a claim about the world that it only reports. That is why the same blog can carry `verified` for one row and no support at all for the next.

**The four tags.** Each names one measure: the evidence in hand for the exact claim. The four are parallel answers to one question, not rungs of a ladder; their order is not their strength, and a fifth tag — source rank, say — is not added.

| Tag | Definition |
|---|---|
| `verified` | The supporting evidence itself — the primary document's own measurements, data, or wording — was inspected, and directly supports the exact claim within its stated scope, and the row shows what was inspected. Merely reading an assertion does not qualify. |
| `reported` | An account describes supporting evidence for the exact claim and points at it — a named benchmark, a citation, a method, figures — but that evidence has not been inspected. An account that only repeats the assertion, however it is attributed, is `unproven`. |
| `unproven` | The claim is asserted, and nothing beyond the assertion is present or described; the cited material offers no supporting evidence. |
| `unknown` | Supporting evidence exists but cannot be obtained or brought to bear on the claim, or the evidence conflicts and is unresolved. One tag serves both; the reason goes in the row, not in the vocabulary. |

**When two tags seem to fit:** First check whether the row contains two claims. Split a statement about what a source says from a statement about whether that assertion holds, then tag each claim separately, each with its own citation of the same passage.

For one claim, ask one question: what evidence is in hand for that exact wording? Source rank does not substitute for evidence, whether the asserting document is primary or secondary. What is in hand is one of four things:

- nothing beyond the assertion → `unproven`
- an account that points at evidence you have not inspected → `reported`
- the evidence itself, inspected and directly supporting the claim → `verified`
- evidence you cannot obtain or bring to bear, or that conflicts and is unresolved → `unknown`, and state the unresolved point

Write the finding so that one row fits; if you cannot, it is two findings. **Never upgrade a label in place.** A finding's label is fixed once assigned; when later investigation inspects primary evidence, record a new finding referencing the original rather than editing the earlier record.

**The row must show what was inspected.** A `verified` row carries in the row — not in a footnote — the wording, figure, or file:line that was inspected. If a reader cannot see from the claim and its row what was looked at, the row is two findings, or it is not `verified`.

For example, reading a vendor announcement supports a `verified` finding that the vendor made a performance claim — the announcement's wording is the evidence for what it says. The performance claim itself is `unproven` if the announcement supplies no measurements.

`verified` does not imply independent replication. State whose evidence was inspected and the conditions it covers. A vendor's benchmark cannot establish performance outside its tested conditions.

**Other finding types:** `INFERRED` and `GAP` stop being alternatives in the trust-label field. Write researcher deductions as inference prose identifying their premise finding IDs and reasoning. Write unsuccessful searches as gap prose identifying the question, query, and places searched. A search that found nothing is a gap, not a tag: do not record absence as though it were evidence. An inference does not inherit `verified` from its premises; failure to find evidence does not establish that something does not exist. An inference or a gap is not a row in the findings table; it is prose, and it carries no trust tag.

When sources disagree, retain separate findings with their citations and tags. Describe the disagreement explicitly; do not average it away. An unresolved overall conclusion is `unknown`.

**One definition:** [RESEARCH_TAGS.md](file:///home/smoke01/dev/ancient-games/docs/RESEARCH_TAGS.md) is to be created as the single copy; it will hold these definitions, the selection rule, the examples, the historical-reading guidance, and two dates: the date it takes effect, and the date before which files carry the older meanings. That is the only new file. Other active documents link to it rather than restating the definitions. Only EJ changes the definitions.

**Files to change if EJ adopts the proposal:**

- `docs/RESEARCH_TAGS.md`: create it with the contents above.
- [research-file.md](file:///home/smoke01/dev/ancient-games/docs/workflow-templates/research-file.md): replace its local definitions with the canonical link; retain the findings table and clarify that bare primary assertions do not qualify for `verified`. Also change the digest's **Confidence** line, which currently counts by the old three labels — and the local list there already omits `unproven`, which is itself an argument for one copy.
- [TASK_TYPES.md](file:///home/smoke01/dev/ancient-games/docs/TASK_TYPES.md): replace `CONFIRMED/INFERRED/GAP/UNPROVEN` in the research check with the canonical link; preserve its citation requirements.
- [FEEDBACK_TEMPLATES.md](file:///home/smoke01/dev/ancient-games/docs/FEEDBACK_TEMPLATES.md): make both research and web-search summaries carry the finding's original ID and canonical tag. Keep inference, gap, and disagreement explanations as prose.
- [.claude/agents/researcher.md](file:///home/smoke01/dev/ancient-games/.claude/agents/researcher.md): update the draft to reference the canonical definition before adoption.

Only these change in the first pass; no historical run folder is edited, and the re-tag produces a count, not an edit. Any future findings check must accept the canonical four tags, must not demand a tag where inference or gap prose is written, and must fail a row that is neither tagged nor written as named prose — that blank middle is the failure that matters. Explorer's `read`/`ran` and the main agent's `quoted`/`my reading`/`not measured` stay separate: they measure what was done to the repo, and how a conclusion is handed to EJ, not the evidence in hand for a claim. There is nothing there to merge.

**Old files:** Preserve completed findings and their original labels. In particular, leave `runs/20261011-agent-memory-graph/check-findings.py` where it is, in the run-1 folder, and do not edit it; its `LABELS` tuple is a spelling check, and the canonical file, not the script, holds the meaning. Preserve run 2's five findings files unchanged, with their 2026-10-11 tags.

Do not automatically translate historical `FACT`, `CONFIRMED`, or even `verified` into the new meanings; read them under their original definitions. When reusing a historical finding, assess its evidence against the new definition and create a current finding referencing the original. Pass-back summaries retain existing tags; new evidence follows the no-upgrade rule above. The re-tag's numbers live in the canonical file's historical section, not in the run folders.

**Price:** Keeping the names requires readers to unlearn the older loose definition of `verified` (where reading any primary document sufficed). One measure means source reliability is not recorded separately; if it matters, it belongs in prose. Centralization requires working links, and preserving history means old and current meanings coexist across repository runs. The regex cost is close to already paid: across the 143 accepted rows the Label column carries only the four tags — 94 `verified`, 44 `reported`, 3 `unproven`, 2 `unknown` — and the gap and inference material is already prose under a `## Gaps` heading. What is genuinely new is the cost of the split: rows will lengthen, and the re-tag will show how many `verified` rows cannot show what was inspected.

## How I decided

1. **Kept** the four tags, one measure each. my #14: 少則得，多則惑 — "little is gained, much is confused." A fifth tag for source rank is the confusion the review's own objection invited; my #12 is why I do not add one, since the words say nothing about who does the stretching or what follows, so rank stays in prose (my application).
2. **Changed** the selection rule from a four-rung ladder to one question with four parallel answers. my #16 is a mindset of parallel statements, not a ladder (知人者智，自知者明); applied to four labels, it says the order carries no meaning — and "the first answer that applies" is an order a reader can reverse.
3. **Changed** `reported` to carry its own test: the account must point at the evidence. my #1: 損之又損，以至於無為 — the sentence already existed in the examples paragraph ("a blog post that only repeats a claim … is `unproven`"). A rule silent where its own example speaks is the sentence written twice, once decorative.
4. **Added** "the row must show what was inspected." my #16, applied: judge the row by its own evidence, not the source's name. my #17 (當其無，有車之用 — the use is in what is not there; the words do not say to remove anything, and this is my application of them) is why an empty cell can be allowed to do work.
5. **Changed** the split rule from an instruction into a check: a reader must see from the claim and its row what was looked at.
6. **Changed** the adoption test. The old pass bar — no row landing on one tag "without argument" — fails on ordinary care and would be waived. my #8: 知不知上，不知知病 — the sickness is the pretended knowledge, and a rule that must be argued around every time is that sickness. New bar: a split is the rule working; only a genuine two-tag standoff says it is not ready.
7. **Changed** by refusal: `unknown` stays one tag. my #2 — 知足不辱，知止不殆, knowing what is enough, knowing to stop — and my #19: 以深為根，以約為紀, restraint as the rule (`attributed`). Conflicting evidence and unobtainable evidence stay one word; the reason goes in the row.
8. **Changed** the re-tag set. my #7: 慎終如始，則無敗事 — "people in their undertakings often fail when they are nearly done," and the copy's last step was its file list. My reading of both run folders and `TASK_TYPES_LEDGER.md`: run 2 is the accepted run, five files, 143 rows; run 1 was blocked at Sections and its five section findings files are not in the repo, only a two-row `findings.md` about defects in `TASK_TYPES.md`.
9. **Changed** the price, against the files. My reading of the Label column across the 143 rows: only the four tags, and no `GAP` or `INFERRED` value anywhere. The regex cost the copy named is already paid; the cost that is real is row length.
10. **Removed** the second copy of the no-upgrade rule inside the `reported` bullet, and the two example sentences that repeated rules now stated in the rule and in the `verified` definition. my #18: 吾所以告子，若是而已 — "what I have to tell you is this, and only this" (`attributed`). Stated twice, it reads as a routine step rather than the rule it is.
11. **Added** the two dates to the canonical file. my #7 again, at the end: a reader must be able to tell which meaning a given file's tags are under, without opening the run folder.
12. **Added** the digest **Confidence** line to the file list. My reading of `research-file.md:30`, which the incoming copy missed.
13. **Kept** the other two label sets separate. my #4: 為者敗之，執者失之 — the world is a sacred vessel and cannot be acted on. They measure other things; merging them would be gripping what is not yours.
14. **Kept** "no historical run folder is edited." my #18: a gentleman rides out when his time comes, and drifts when it does not. That run is finished; rewriting it is not its time.

## What I need to know

- Is the re-tag set only run 2's five files, or are the older 2026-10-02 folders in scope too? If they are, the pass bar changes from 143 rows to several hundred, under an even looser old definition, and I would re-estimate.
- Does EJ accept that a claim about what a source *says* can carry `verified` while a claim about the world cannot, with the difference carried entirely by the row's wording? If EJ wants `verified` to mean only about the world, a claim about wording cannot be `verified` at all and needs either a fifth tag or a separate column — that is the fork this copy resolves by splitting the row, and EJ should confirm it rather than inherit it.
- May a findings-table row have an empty Label cell, or must inference and gap prose stay strictly outside the table? I have answered it as strictly outside; if EJ wants the empty cell inside, the row-must-show rule needs a second sentence.
- Does the historical-reading paragraph belong in `RESEARCH_TAGS.md` or in a separate history note? I have put it in `RESEARCH_TAGS.md` so that one file answers "what did this tag mean in that file".

## Costs and risks

1. Losing the ladder's order removes a mechanical "first that applies" rule; a researcher can now read the four in any order and choose the flattering one. The split rule and the row-must-show rule are the only brakes, and without the second discipline `verified` becomes the default. (my #16, my #14)
2. The softer adoption test will let messy rows pass, so the 143-row re-tag can come back clean while the rule is still vague. EJ gets a number, not a defence. (my #8)
3. `unknown` staying one tag means conflicting evidence and unobtainable evidence look identical in the column; a scanner cannot tell them apart. (my #2, my #14)
4. The row-must-show rule will lengthen rows and will move many `verified` rows down to `reported` or `unproven`. I have said so in advance so the number is not read as a verdict against the change. (my #13: 善有果而已 — a result and that is all, 果而勿矜 — and no vaunting.)
5. Keeping the older meanings alive in the repository means a reader can still meet `verified` in two senses. The only defence is the date line and the historical paragraph; if either is skipped in implementation, the two senses will merge by accident. (my #7, my #18)
6. The 143-row figure, "run 1 was blocked", and the Label-column counts are my own reading of the run folders, not something the brief gave me. If EJ's record of that run differs, the re-tag set is wrong and the pass bar moves with it. (my reading)

## How we would know I was right

- The 143-row re-tag finishes with zero rows standing between two tags after splitting, and the count of rows that moved is on paper.
- A second reader, given any `verified` row from those files, can say from the row alone what was inspected.
- Across the next three research tasks, no findings check fails on a missing tag for inference or gap prose, and nobody asks for a fifth tag.
- And the falsifier: if re-tagged rows repeatedly split into more than two claims, or if `verified` and `reported` keep trading the same row, then my #16 was wrong — the four tags are rungs after all, and the ladder I removed was doing real work.
