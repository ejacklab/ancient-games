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
| `reported` | You read an account that gives a locator for where the claim comes from (a URL, a DOI, or the exact title), and you have not inspected that source. You do not yet know what evidence it holds. This holds whether the source could not be obtained or simply was not fetched. |
| `unproven` | You read the claim, and nothing beyond the assertion is in hand: no evidence is shown, and no locator leads further. A primary source that asserts without evidence is `unproven`; so is an account that names no locator ("studies show", "the company says", "per the Smith paper"). |
| `unknown` | Evidence bearing on the claim is in hand but does not settle it, in one of two ways: it conflicts and the conflict is unresolved, or it was inspected and neither supports nor contradicts the exact wording. One tag serves both; the reason goes in the row, not in the vocabulary. |

**When two tags seem to fit:** First check whether the row contains two claims. Split a statement about what a source says from a statement about whether that assertion holds. Then tag each claim separately, each citing the same passage.

For one claim, ask one question: what evidence is in hand for that exact wording? Source rank does not substitute for evidence, whether the asserting document is primary or secondary. What is in hand is one of these:

- nothing beyond the assertion → `unproven`
- an account that gives a locator for a source you have not inspected, whether or not you could get it → `reported`
- the evidence itself, inspected and directly supporting the claim → `verified`
- evidence in hand that conflicts unresolved, or that does not settle the exact wording → `unknown`, and state the unresolved point
- evidence in hand that contradicts the claim → this is not a fifth tag. Write the finding as what the evidence shows, which is then `verified`. Keep the contradicted assertion as its own row with its own tag.

**`reported` or `unproven`, for a secondhand account.** One question: **does the account give a locator** — a URL, a DOI, or the exact title of the source the claim comes from? Yes → `reported`. No → `unproven`. The locator may sit anywhere in the account (a footnote, a bibliography entry). An exact title is a title written out in full; a short name such as "the Smith paper" is not one. Nothing else is a locator, in any combination: an author's name, a venue, a year or a benchmark name, alone or together, is not one. What kind of source the locator leads to (a paper, a whitepaper, a README, a company post, a recording — anything) and the account's verb ("claims", "found", "shows") do not change the tag; what that source holds is learned only by inspecting it, and the inspection is a new finding with its own tag.

Examples: "a 2025 arXiv paper (link) found +12% recall on LoCoMo" → `reported`. "The company says it is 60% faster" with a link to the company's post → `reported`; inspect the post, and if it shows no measurements, a new finding "the 60% claim has no evidence in its source" is `verified` and the claim itself stays `unproven`. "Per the Smith paper, latency drops 40%" → `unproven`. "Studies show it is faster" → `unproven`.

A row saying what the account itself says ("the blog states X") is `verified`, and is written only when what the account said matters to the answer; the row the tag rules are for is the claim itself.

Write each finding so that one row fits. If you cannot, it is two findings.

**Never upgrade a label in place.** A finding's label is fixed once assigned. When later investigation inspects primary evidence, record a new finding that references the original; do not edit the earlier record.

**The row must show what was inspected.** A `verified` row carries, in the row itself and not in a footnote, the wording, figure or file:line that was inspected. If a reader cannot see from the claim and its row what was looked at, the row is either two findings or not `verified`.

For example, reading a vendor announcement supports a `verified` finding that the vendor made a performance claim, because the announcement's wording is the evidence for what it says. The performance claim itself is `unproven` if the announcement supplies no measurements, and `reported` if it gives a locator for a benchmark that was not inspected.

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
