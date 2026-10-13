# 范蠡 (Fan Li): one official set of trust tags for research findings

## Answer
I'd keep the four lower-case tags, `verified`, `reported`, `unproven` and `unknown`, and give them new definitions. Each tag should answer one question: how far along the chain of sources did the researcher get, and what was there? The single definition goes in `docs/workflow-templates/research-file.md`, and every other file points to it. `INFERRED` and `GAP` should stop being trust tags. An inference belongs in the answer and must cite the finding ids it rests on. A gap is an `unknown` row, plus a line in the Gaps section. The other two sets (`read`/`ran` for the explorer, and *quoted* / *my reading* / *not measured* for the main agent) stay separate. This is advice. EJ decides.

**The proposed tags.** A researcher picks a tag by asking two questions in order. First: did I read the primary source? Second: does that source *show* the claim as I worded it, or does it only state it?

| Tag | One-line definition |
|---|---|
| `verified` | I read the primary source, and it shows the claim as worded. For a claim like "V states X", the statement itself is the evidence. For a claim like "X is true", the data, method, code or run must be shown. |
| `unproven` | I read the primary source, and it asserts the claim but shows no evidence for it. |
| `reported` | I saw the claim only in a secondary source that passes it on. I did not read the primary. |
| `unknown` | I looked and could not settle it: nothing was found, or the sources I read do not decide it. The Gaps section records what I searched and where. |

**When two tags seem to fit.** The claim is probably two claims, so split it into rows that each take one tag. For example, "Vendor V states its system is 60% faster" (`verified`) and "V's system is 60% faster" (`unproven`). If a row really cannot be split, it takes the weaker tag, in the order `verified` > `reported` > `unproven` > `unknown`. A tag is never raised later unless the primary source is read again. When sources disagree, write both rows; don't average them (house rule).

**Files that change** (one change, done all at once):
1. `docs/workflow-templates/research-file.md` holds the single copy: the four definitions, the two-question test, the rule for when two tags fit, and where inferences and gaps go. Through its link it is also what the skill reads.
2. `docs/TASK_TYPES.md`, the `research and reports` row. Replace "a CONFIRMED/INFERRED/GAP/UNPROVEN label" with "a label from `docs/workflow-templates/research-file.md`". I grepped `design_gate.py` and it does not parse that wording.
3. `docs/FEEDBACK_TEMPLATES.md`: rows 9 and 14, lines 47–49, 130 and 135.
   - `FACT` becomes one of the four tags.
   - `CONFIRMED` and `UNPROVEN` become the four tags.
   - `INFERRED` and `GAP` stay as kinds of line in the pass-back, not trust tags. `INFERRED` names the rows it follows from and can be no stronger than the weakest of them.
4. `.claude/agents/researcher.md`, lines 27, 38–40 and 49–50. Replace the copied definitions with a pointer. Fix the F7 example: it tags a vendor blog `reported` even though the blog *is* the primary source. Under the new definitions it becomes `verified` ("the vendor claims") or `unproven` (the performance claim itself).
5. `.claude/workflows/research-agent-memory.js`, lines 50 and 60–65. Keep the `LABELS` constant, but point its definition text to the template.
6. `skills/workflow-design/`: regenerate it with `tools/export_skills.py`; don't edit it by hand.
7. Not changed: the old `docs/research/*` findings files, and `runs/20261011-agent-memory-graph/check-findings.py`. Its tag list already matches.

**What the evidence-grading schemes say, and what applies here.**
- **The Admiralty code (NATO 6×6).** It rates the source A–F and the information 1–6 separately, and Wikipedia says *"Each descriptor is considered in isolation"*. Tag: `reported`. I read Wikipedia, not the NATO doctrine itself, which is not public.
  - What applies: reading a good source must not raise the claim's tag. The vendor's own page gives "V states X" as `verified`, but "X is true" stays `unproven`. Splitting rows does that job inside one column.
  - What does not apply yet: the second column for how reliable the source is.
  - Its "1 = confirmed by other sources" is cross-checking, and that is the referee's Corroborate stage, not a tag.
- **ICD 203 (US intelligence analysis standard).** It asks writers to *"Properly distinguish between underlying intelligence information and analysts' assumptions and judgements"*. Tag: `reported`. I read this on the ODNI objectivity page; the ICD 203 PDF downloaded but I could not extract its text. This is the reason `INFERRED` leaves the tag column: an inference is a judgement, not information.
- **GRADE (medical evidence grading).** It keeps how certain the evidence is apart from how strong the recommendation is, and its ratings start from the study design and move up or down from there. Tag: `reported`, from search summaries only. What applies: a tag grades a finding, never a decision. Decisions already go to `decisions.md`.

## How I decided
1. **The four lower-case tags carry the weight of use, so I kept them (my #5, quoted: 「天節固然，唯謀不遷。」, "Heaven's rhythm is like that; only the plan does not move").**
   - The word counts you gave show `verified`, `reported` and `unknown` in the hundreds, against roughly 25 upper-case words in total.
   - The 10 files from run 2, which EJ accepted, use only these four.
   - Switching to the upper-case set would throw that away "in one morning" (#5, 「十年謀之，一朝而棄之」). I keep the names and repair the definitions.
2. **One measure per tag (my #14, quoted: 「四封之內，百姓之事，蠡不如種也。四封之外…種亦不如蠡也。」).** Each part does the job it is best at.
   - Today's `reported` measures *who* the source is, while `unproven` measures *whether evidence was shown*. That is two jobs on one column.
   - The two-question test puts all four tags on one measure: how far along the chain I got, and what I found there.
   - By the same rule, the explorer's tags and the main agent's tags keep their own jobs and their own makers.
3. **Confirmation by other sources is not a tag (my #12, quoted: 「又觀其民之饑飽勞逸以參之」, "and we also look at their people's hunger or fullness, toil or ease to cross-check").** Fan Li treats the cross-check as its own step. Here that step is counting independent rows, which is the referee's Corroborate stage. So the old `CONFIRMED` does not come back as a tag. Tying #12 to the Corroborate stage is *my reading*.
4. **No second column now, unlike the Admiralty code (my #3, quoted: 「時不至，不可彊生；事不究，不可彊成。」, and my #7, 「王無蚤圖」, "Do not plan early").**
   - `unproven` has been used about 8 times in total, and nothing in the counts asks for a grade of how reliable a source is.
   - A 6×6 grid now would be forcing growth before its time.
   - Holding to four tags and no more is *my reading* of my #10 (「無過天極，究數而止」) and my #2 (「天道盈而不溢」, "Heaven's way is full but does not overflow").
5. **Act now and finish in one change (my #1 and my #4, quoted: 「得時無怠，時不再來」, "Having got the time, do not slacken; the time does not come again").**
   - The human affairs have arrived. `.claude/agents/researcher.md` is a draft that has not been adopted yet, and it already repeats the conflict in its F7 example (lines 38–40).
   - Once it is adopted, every future run copies the conflict.
   - Changing some files and not others would leave two sets again, the "time that is got but not carried through" of #4.
6. **The rule has to be checkable before we lean on it (my #18, quoted: 「審備則可以戰乎？」, "If the preparations are examined, can we then fight?").** That is why the definitions are two yes/no questions a second person can apply. It is also why `check-findings.py`'s list of tags is kept.
7. **Splitting rows, and taking the weaker tag when a row cannot be split.** The split comes from the house rules ("give both rows", "never upgrade") and the earlier reviewer's narrow-claim point. The order of tags is *my reading*; nothing on my list gives it.
8. **The definition lives in the researcher's form, because the researcher is the only one who fills in the tag.** That is the "one maker" rule from CLAUDE.md. Applying it here is *my reading*.

## What I need to know
- **Who wrote the `CONFIRMED/INFERRED/GAP/UNPROVEN` wording in `TASK_TYPES.md`?** If EJ wrote it as their own rule, step 1 weighs less and EJ chooses between the sets. My proposal then becomes one option, not the answer.
- **Should the word `verified` be renamed?** It still reads as "true" to someone skimming. If EJ wants it renamed, the old files no longer match the new name, and my #5 argues against that. EJ would pick the new name; I won't invent one.
- **Should `GAP` stay a row tag?** If EJ wants that, `unknown` splits into "not found" and "not settled", making five tags, and the order of tags changes.
- **Should old findings files be relabelled?** If yes, someone has to go through about 450 tag words, and run 2, which EJ already accepted, would be changed after acceptance. I advise against it.

## Costs and risks
- **The old files stay mixed (my #5).** Earlier findings files keep `FACT`, `CONFIRMED` and `GAP`. A script that reads across all runs has to tolerate them, or label them as older-format files.
- **Some old `reported` rows meant `unproven` (my #14).** Under the new definitions, a row like F7 in the draft would be tagged differently. Readers comparing old and new runs may misread the change as a change in the facts.
- **`verified` can still be read as "true" (my #5).** I keep the name to keep the files continuous. The price is that a skim reader may over-trust a row that only says "V states X".
- **No grade for how reliable a source is (my #3, #7).** One vendor with a bad track record and another with a good one get the same tag. If that starts to matter, a second column will be needed later, and the format changes then.
- **One change across 5 files plus a regenerated bundle (my #4).** Doing it partly is worse than not doing it. The price is one coordinated change that EJ has to approve, and `tools/export_skills.py` has to be run afterwards.
- **The two-question test is mine (my #18).** I wrote it, and I have not run it against real rows. Until someone else applies it blind, it is not independent evidence that it works.

## How we would know I was right
- **One copy.** After the change, a grep shows the four definitions in `docs/workflow-templates/research-file.md` only. Every other file points to it.
- **Agreement between labellers, measured as a comparison.** Take about 30 rows from earlier findings files. Have two blind labellers tag them, once with the old definitions and once with the two-question test. Compare how often they agree under each. If I am right, they agree more under the new test. Rows like the 60% vendor claim are where the old definitions should split them.
- **The checker stays clean.** On the next research runs, `check-findings.py` finds no tag outside the four, and no `INFERRED` or `GAP` appears in the Label column.
- **The test case comes out the same for everyone.** The vendor's "60% faster" blog post gives the same two rows (`verified` / `unproven`) from different researchers without anyone asking. Today the draft researcher tags it `reported` and the earlier review said `verified`.
