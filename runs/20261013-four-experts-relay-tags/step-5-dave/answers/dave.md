# Dave — one official set of research trust tags

## Answer
I kept the four tags, the split-first rule and the old-files policy. I made the re-tag a proper experiment: the prediction is written first, a control pass runs under the old definitions, the taggers work blind, and the count is defined for rows that split. I took the "cannot be obtained" case out of `unknown`, because it overlaps with `reported`. I added the missing case of evidence that contradicts a claim. I also corrected the file list: TASK_TYPES must still state its check, the researcher draft's worked example flips under the new rule, and EJ's operator prompts in `tests/` are left alone.

### The copy

**Status:** Proposal for EJ's decision; not measured (`n=0`). These are proposed SHOULD defaults, and the researcher explains any departure. The definitions themselves are EJ's: a default may bend in a hard case with a written reason, but a definition may not. Track operational friction during first use, but do not change the canonical definitions on an `n=1` basis. Evaluate adjustments only after the same friction recurs across separate tasks.

**Adoption waits on one reckoning: a blind re-tag with a control.** Run 2 is the accepted run. Its five findings files in `runs/20261011-agent-memory-graph-r2/verify/sections/` hold 143 rows. Run 1 was blocked at Sections, and its section findings files are not in the repo.

1. **Prediction first.** Before either tagger starts, the main agent writes three things in the re-tag's run folder: the metric (the four counts in step 4, for both passes), the expected result, and a stop date.
2. **Blind copy.** Make a copy of the five tables with the Label column removed. Each tagger reads only that copy and one set of definitions, and writes each row's tag before seeing any old label.
3. **Two passes by two fresh taggers.**
   - The *new-rule pass* tags under this file.
   - The *control pass* tags under the old definitions, which are quoted from `docs/workflow-templates/research-file.md`: "`verified` = the primary file or document was read; `reported` = a secondary source; `unknown` = not settled".
   - The control pass measures how far a fresh tagger drifts from the old labels with no rule change. Without it, "rows moved" mixes the rule's effect with tagger noise.
4. **Count each original row once, as one of four outcomes:**
   - *same*;
   - *moved* (old → new);
   - *split* (old → the tag of each part);
   - *stuck*: after splitting, it still stands between two tags, above all between `reported` and `unproven`.

   A split is the rule working, not the rule failing.
5. **Report the counts for both passes side by side.** List every stuck row by id, with the same weight as the totals. Name who or what tagged each pass.
6. **Read the result:**
   - Any stuck row in the new-rule pass means the rule is not ready. The definitions go back to EJ, not to the researcher.
   - If the new-rule pass moves no more rows than the control pass, the new rule made no measurable difference. That is a result, and it is reported as one.
   - This is a first tagging under the new rule, not an upgrade of old labels, so rows may move either way. Do not argue the number.

The tag sheets and the prediction live in a new run folder for the re-tag (proposed: `runs/<date>-research-tags-retag/`, subject to EJ's agreement). No historical run folder is edited.

**Scope:** The researcher gives each research finding one tag. The tag describes the evidence the researcher has for the finding's exact wording. It is neither a confidence score nor a declaration of universal truth.

**Primary and secondary are relative to that exact wording, not to the source's reputation.** One document is primary evidence for the claim that it says what it says. It is secondary for a claim about the world that it only reports. That is why the same blog can carry `verified` for one row and `unproven` for the next.

**The four tags.** Each tag names one measure: the evidence in hand for the exact claim. The four are parallel answers to one question, not rungs of a ladder. Their order is not their strength, and no fifth tag (such as source rank) is added.

| Tag | Definition |
|---|---|
| `verified` | The supporting evidence itself was inspected: the primary document's own measurements, data or wording. It directly supports the exact claim within its stated scope, and the row shows what was inspected. Merely reading an assertion does not qualify. |
| `reported` | An account describes supporting evidence for the exact claim and points at it (a named benchmark, a citation, a method, figures), but that evidence has not been inspected. This holds whether the evidence could not be obtained or simply was not fetched. An account that only repeats the assertion, however it is attributed, is `unproven`. |
| `unproven` | The claim is asserted, and nothing beyond the assertion is present or described. The cited material offers no supporting evidence. |
| `unknown` | Evidence bearing on the claim is in hand but does not settle it, in one of two ways: it conflicts and the conflict is unresolved, or it was inspected and neither supports nor contradicts the exact wording. One tag serves both; the reason goes in the row, not in the vocabulary. |

**When two tags seem to fit:** First check whether the row contains two claims. Split a statement about what a source says from a statement about whether that assertion holds. Then tag each claim separately, each citing the same passage.

For one claim, ask one question: what evidence is in hand for that exact wording? Source rank does not substitute for evidence, whether the asserting document is primary or secondary. What is in hand is one of these:

- nothing beyond the assertion → `unproven`
- an account that points at evidence you have not inspected, whether or not you could get it → `reported`
- the evidence itself, inspected and directly supporting the claim → `verified`
- evidence in hand that conflicts unresolved, or that does not settle the exact wording → `unknown`, and state the unresolved point
- evidence in hand that contradicts the claim → this is not a fifth tag. Write the finding as what the evidence shows, which is then `verified`. Keep the contradicted assertion as its own row with its own tag.

Write each finding so that one row fits. If you cannot, it is two findings.

**Never upgrade a label in place.** A finding's label is fixed once assigned. When later investigation inspects primary evidence, record a new finding that references the original; do not edit the earlier record.

**The row must show what was inspected.** A `verified` row carries, in the row itself and not in a footnote, the wording, figure or file:line that was inspected. If a reader cannot see from the claim and its row what was looked at, the row is either two findings or not `verified`.

For example, reading a vendor announcement supports a `verified` finding that the vendor made a performance claim, because the announcement's wording is the evidence for what it says. The performance claim itself is `unproven` if the announcement supplies no measurements, and `reported` if it names a benchmark that was not inspected.

`verified` does not imply independent replication. State whose evidence was inspected and the conditions it covers. A vendor's benchmark cannot establish performance outside its tested conditions.

**Other finding types:** `INFERRED` and `GAP` are no longer choices in the trust-label field.

- Write a researcher's deduction as inference prose that names its premise finding IDs and the reasoning.
- Write an unsuccessful search as gap prose that names the question, the query and the places searched.
- A search that found nothing is a gap, not a tag. Do not record absence as though it were evidence.
- An inference does not inherit `verified` from its premises, and failing to find evidence does not show that something does not exist.
- An inference or a gap is not a row in the findings table. It is prose, and it carries no trust tag.

When sources disagree, keep separate findings with their own citations and tags. Describe the disagreement explicitly; do not average it away. An unresolved overall conclusion is `unknown`.

**One definition:** `docs/RESEARCH_TAGS.md` is to be created as the single copy. It will hold:

- these definitions;
- the selection rule;
- the examples;
- the guidance for reading historical files;
- the re-tag's counts for both passes, with a link to the re-tag's run folder;
- two dates: the date it takes effect, and the date before which files carry the older meanings.

It is the only new document. Other active documents link to it rather than restating the definitions. Only EJ changes the definitions.

**Files to change if EJ adopts the proposal:**

- `docs/RESEARCH_TAGS.md`: create it with the contents above.
- `docs/workflow-templates/research-file.md`:
  - replace its local definitions with the canonical link;
  - keep the findings table, and widen its Label column's placeholder to the four tags;
  - make clear that bare primary assertions do not qualify for `verified`;
  - change the digest's **Confidence** line, which counts by the old three labels. Its local list already omits `unproven`, which is itself an argument for one copy.
- `docs/TASK_TYPES.md`: in the `research and reports` check, replace `CONFIRMED/INFERRED/GAP/UNPROVEN` with a check that still says what is checked. Every finding carries both-side citations and one of the four tags in `docs/RESEARCH_TAGS.md`, or is written as inference or gap prose; missing proof never reads as PASS. Keep the citation requirement and the sabotage cell. Write the tags with "/" or commas, never "|": `design_gate.py` splits this table on "|", and a check that only points at a document is the defect its G3 rule flags.
- `docs/FEEDBACK_TEMPLATES.md`: make both the research and the web-search summaries carry the finding's original ID and canonical tag. Keep inference, gap and disagreement explanations as prose.
- `.claude/agents/researcher.md` (draft, not adopted):
  - replace its label list with the canonical link;
  - rewrite its worked example. Its F7 tags a vendor blog's "reduces memory tokens by 60%" as `reported`. Under this rule, "the vendor says 60%" is `verified`, and the 60% itself is `unproven` unless the blog points at a benchmark.
  - replace "If you cannot quote it, the row is `unknown`". Under this rule, nothing to quote beyond the assertion is `unproven`.

Only these change in the first pass. The re-tag produces counts, not edits.

Any future findings check must:

- accept the canonical four tags;
- not demand a tag where inference or gap prose is written;
- fail a row that is neither tagged nor written as named prose. That blank middle is the failure that matters.

**Tag sets that stay separate.** Explorer's `read`/`ran` and the main agent's `quoted`/`my reading`/`not measured` stay as they are. They measure what was done to the repo and how a conclusion is handed to EJ, not the evidence in hand for a claim, so there is nothing there to merge.

**Operator prompts stay as written.** EJ's prompts in `tests/operator-prompt-list.md` and the `tests/fixtures/operator_prompts_*.jsonl` files ask for `CONFIRMED`/`INFERRED`/`GAP`/`UNPROVEN` and `UNKNOWN`. They are EJ's own words and classifier test inputs, and they are not edited. Proposed default, for EJ to decide: a prompt that names its own labels is answered in those labels, and this file governs findings files.

**Old files:** Keep completed findings and their original labels.

- Leave `runs/20261011-agent-memory-graph/check-findings.py` where it is, in the run-1 folder, and do not edit it. Its `LABELS` tuple is a spelling check; the canonical file, not the script, holds the meaning.
- Keep run 2's five findings files unchanged, with their 2026-10-11 tags.
- Do not translate historical `FACT`, `CONFIRMED` or even `verified` into the new meanings. Read them under their original definitions.
- To reuse a historical finding, assess its evidence against the new definition and create a current finding that references the original.
- Pass-back summaries keep their existing tags. New evidence follows the no-upgrade rule above.

**Price:**

- Keeping the names means readers must unlearn the older, looser `verified`, where reading any primary document was enough.
- One measure means source reliability is not recorded separately. If it matters, it belongs in prose.
- Narrowing `unknown` moves the "could not get the evidence" rows into `reported` or `unproven`.
- Centralizing needs working links. Keeping history means old and current meanings exist side by side across the repo's runs.
- The re-tag costs two tagging passes, not one. The control pass is the price of telling the rule's effect apart from tagger noise.
- The regex cost is mostly paid already. Across the 143 accepted rows the Label column carries only the four tags (94 `verified`, 44 `reported`, 3 `unproven`, 2 `unknown`), and the gap and inference material is already prose under a `## Gaps` heading.
- What is genuinely new is the cost of the split: rows get longer, and the re-tag will show how many `verified` rows cannot show what was inspected.

## How I decided
1. **Checked the copy's numbers before building on them.** My #5. I counted run 2's five files: 29 + 18 + 38 + 27 + 31 = 143 rows. The Label column holds 94 `verified`, 44 `reported`, 3 `unproven` and 2 `unknown`, and all five files have `## Gaps`. Run 1 has no `verify/sections/` folder. **Kept** the numbers and the run-1 note.
2. **Kept the re-tag as the adoption gate** rather than arguing the definitions further. My #2 and #1: the re-tag is the observation that settles whether the rule decides.
3. **Added the prediction written first** (metric, expected result, stop date, before either tagger starts). My #3. I did not fill in the expected value. The main agent writes it, because a number I chose would be a gap filled with my own value.
4. **Added the control pass** under the old definitions. My #4: "moved 30 rows" means nothing until it is set against how many rows a fresh tagger moves with no rule change.
5. **Changed "how many rows moved" into four per-row outcomes**, and made stuck rows listed by id. "Moved" is undefined once rows split (my reading). Listing stuck rows and reporting "no more movement than control" as a result come from my #9.
6. **Added how the blind is done** (a copy with the Label column removed) and naming who tagged each pass. "Before looking at its old one" cannot hold while the label sits in the same row (my reading). Naming the tagger is my #10 and the house rule to name who wrote a check.
7. **Changed `unknown`.** I removed "cannot be obtained", because a paywalled benchmark that a blog points at fit both `reported` and `unknown`: an overlap in the definitions themselves (my reading). The re-tag will show whether I am wrong, if rows still want `unknown` for evidence they could not obtain (my #1).
8. **Added the contradiction case** to the selection list. The copy said "one of four things", but inspected evidence that contradicts the claim had no line (my reading). I added it without a fifth tag, which keeps the copy's "no fifth tag" rule.
9. **Changed "no support at all" to `unproven`** in Scope. "No support at all" is not a tag (my reading).
10. **Changed the TASK_TYPES edit** from "replace with the canonical link" to stating the check plus the link, and added the "|" warning. My #5: I read `design_gate.py`. `parse_types` splits rows on "|" and keeps cell 4 as the check, and G3 flags a check that points at a document instead of saying what is checked.
11. **Added the researcher.md specifics** (the F7 example and the "cannot quote → unknown" line). My #5: I read the draft, and both lines contradict the new rule (my reading).
12. **Added that the operator prompts in `tests/` stay unchanged.** My #5: grep found EJ's real prompts using the old upper-case set. Which labels a prompt like that should be answered in is left to EJ.
13. **Added the control pass and the narrowed `unknown` to Price.** Brief point 4: every recommendation names its price.
14. **Kept unchanged:** the four definitions apart from `unknown`, split-first, no upgrade in place, the row showing what was inspected, the vendor example (extended by one clause), inference and gap as prose, keeping disagreements separate, one canonical file, keeping explorer and conclusion tags separate, and the old-files policy. Nothing in my list argues against them.
15. **Kept the no-upgrade rule; no nature borrowing.** My #6: honeybee nest-site scouts only advertise a site they have inspected themselves, not one they were told about (my reading, general knowledge, not from the given facts). My #7: the mechanism matches no-upgrade and the inspection requirement, but bees keep no history, so it adds nothing the copy does not already say.
16. **Removed:** nothing substantive. My reading: each paragraph carries a rule or a fact the taggers or EJ need.

## What I need to know
- **Will EJ pay for the control pass?** If not, the re-tag count cannot separate the rule's effect from tagger noise, and step 6's second bullet should be dropped.
- **Which labels answer a prompt that names its own?** EJ's operator prompts name `CONFIRMED`/`INFERRED`/`GAP`/`UNPROVEN`. If such prompts should get the four tags, the "Operator prompts stay as written" paragraph changes. If they keep their own labels, it stands.
- **Does EJ agree to a new run folder for the re-tag's sheets?** If not, the evidence needs another home that EJ agrees to.
- **Does the narrowed `unknown` match EJ's intent?** If EJ meant `unknown` to include "exists but unobtainable", the overlap with `reported` comes back. A tie-break line would then be needed, and that line is EJ's to write.

## Costs and risks
- **Two tagging passes instead of one** (from my #4).
- **The blind leaks.** Some Finding texts carry their own label in prose; s1 F2 says "This is a secondary account of the workshop". The blind is partial, so the two passes are compared with each other, not taken as absolute (my reading, from my #5).
- **The re-tag has a target.** In a spot read of s2, I saw at least one `verified` row whose shown quote does not contain the figures its claim states. The new rule should move such rows. That observation must stay out of the taggers' brief, or it becomes a planted hint (my #3 and my #5, n=1).
- **TASK_TYPES parse risk.** A "|" in the new check text breaks `design_gate.py`'s table parse (my #5).
- **Rows shift between tags.** Narrowing `unknown` will move rows into `reported` or `unproven` (from step 7, my reading).
- **The contradiction case lengthens rows.** It turns one row into two (from step 8, my reading).
- **The stuck-row test is strict.** Any one stuck row sends the definitions back to EJ, which may hold up adoption (my #9: that is still the result to report).
- **Everything above is `n=0`** (my #10).

## How we would know I was right
- The prediction exists in the re-tag folder with a timestamp earlier than both tag sheets (my #3).
- The new-rule pass shows zero stuck rows. Its *moved + split* count, set against the control pass's *moved* count, shows whether the rule changed tagging beyond tagger noise (my #4). Either outcome is reported.
- No row in the new-rule pass is tagged `unknown` only because evidence could not be obtained. If any is, my `unknown` change was wrong (my #1).
- After the TASK_TYPES edit, `env -u NO_COLOR python3 -m pytest -q` still passes, and `parse_types` still returns six cells for `research and reports` (my #5).
- In the first new research run under `docs/RESEARCH_TAGS.md`, every `verified` row carries the inspected wording, figure or file:line in the row itself.
