# Dave — one official set of trust tags for research findings

## Answer
Stop using one label for two questions. Each finding row should get two tags. The first says **how we got it**: `primary` or `secondary`. The second says **what backs the claim**: `confirmed`, `shown`, `claimed` or `unknown`. `INFERRED` and `GAP` stop being tags and become their own lists. The definition should live in one place, `docs/workflow-templates/research-file.md`, because the researcher is the one who fills it in. Adopt it on one research run first and compare it against the current four tags before spreading it (my #8, my #4). If that comparison does not show better agreement, keep the four tags and add a single tie-break line instead (my #1).

**The proposed tags**

| Axis (column) | Tag | One-line definition |
|---|---|---|
| **Read** | `primary` | I read the document that makes the claim or owns the data (the paper, the vendor's own page, the repo file). |
| | `secondary` | I read someone else's account of that document. |
| **Backing** | `confirmed` | An independent primary source, or our own run, reproduces the claim. The row names that source's id. |
| | `shown` | The source presents its own evidence (method, data, harness, quoted text), or the claim is what the document itself defines. |
| | `claimed` | The claim is asserted and no evidence is shown. This replaces `unproven`. |
| | `unknown` | The sources I read do not settle it. |

- **Not tags:** `INFERRED` rows go in an "Inferred" list and name the row ids they follow from. `GAP` rows go in a "Gaps" list and name the query run and where it was run. Disagreement stays as two rows, each with its own tags, never merged.
- **Rule when two tags seem to fit:** each axis answers only one question, so a tag from one axis never competes with a tag from the other. The vendor-blog example is `primary` + `claimed`: the narrow claim "the vendor says X" is first-hand, and the 60% figure has no harness behind it. If two tags on the *same* axis both seem to fit, write the weaker one: `secondary` over `primary`, and the lower of confirmed > shown > claimed > unknown. Say why in the row. This is the house rule "never upgrade" applied per axis.
- **Old files:** leave them as they are. Relabelling them could upgrade a label. Add one dated line in `research-file.md` that maps the old words for readers: verified → `primary` (backing not recorded), reported → `secondary` (backing not recorded), unproven → `claimed`, unknown → `unknown`. I do not invent the missing backing tag.
- **Files that change to point at it** (I found these with grep on 2026-10-13):
  - `docs/workflow-templates/research-file.md` is the single copy.
  - `docs/TASK_TYPES.md`, row "research and reports": "CONFIRMED/INFERRED/GAP/UNPROVEN" becomes a pointer.
  - `docs/FEEDBACK_TEMPLATES.md`: in both pass-backs, the FACT and CONFIRMED/UNPROVEN lines become rows with the two tags, while INFERRED, GAP and Disputed stay as lists.
  - `.claude/agents/researcher.md`: its lines 27, 40 and 49–50 are replaced by a pointer.
  - `.claude/workflows/research-agent-memory.js`: the `LABELS` constant (line 50) and the prompt text (lines 60–64) carry their own copy of the definitions and need changing.
  - `runs/20261011-agent-memory-graph/check-findings.py` stays as it is, as that run's record.
- **Keep separate** (my reading; the basis is the house rule "every artifact has one maker", not my list):
  - The explorer's `read`/`ran` tags cover repo code and are enforced by `quote_check.py`.
  - The main agent's *quoted / my reading / not measured* is a different author writing to EJ.
  - `readiness.py`'s `verified`/`reported` describe whether a tool is installed.

## How I decided
1. **What would change my mind (my #1).** Two labelers each tag the same rows twice, once with the current four tags and once with the two axes. If the two-axis tags give no better agreement, I am wrong and a one-line tie-break is cheaper.
2. **The data we already have (my #5).** The accepted run's index, `docs/research/20261011-agent-memory-graph-r2/INDEX.md` (lines 250–256), already records the collision. Zep's 94.8%/93.4% claim from one paper is `verified` in s2-F2 and `reported` in s5-F18. Mem0's 26%/91% claim is `verified` in s1-F3 and `reported` in s4-F19 and s5-F17. The index says why: "The two sections applied different label conventions." s5 had to write its own local convention (FINDINGS-s5 line 7: "`reported` = the row is a performance claim … (vendor paper…)"). `researcher.md` line 40 adds a third reading: "`reported`, not `verified`: the vendor's blog was read, not the benchmark harness". `unproven` was used on a primary source (s3-F10, a Zenodo record) and on a secondary blog (s5-F28), so it already behaves like a second axis. Label counts in that INDEX, from my awk count: verified 91, reported 44 (16 of them cite arXiv), unknown 2, unproven 3.
   - **What this does not show:** collisions are only visible where two sections wrote up the same claim. I do not know the rate among the other rows.
3. **Established schemes (web, checked 2026-10-13).**
   - The Admiralty / NATO code grades the source A–F and the information 1–6 separately. [Wikipedia](https://en.wikipedia.org/wiki/Admiralty_code), fetched: "Each descriptor is considered in isolation". Its 6 is "Truth cannot be judged" and its 1 is "Confirmed by other sources". In my own tags that is `secondary` + `shown`.
   - UK policing's 3x5x2 pairs a source grade (1 reliable / 2 untested / 3 not reliable) with an information grade. A is "Known directly to source", B "Known indirectly to source but corroborated", C "Known indirectly to source", D "Not known", E "Suspected to be false". This comes from search-result summaries of the [College of Policing APP appendix](https://www.college.police.uk/app/intelligence-management/example-intelligence-report-appendix); the page itself returned 403, so it is `secondary` + `unknown` for wording.
   - **What applies here:** keep the axes separate, and treat first-hand versus second-hand plus corroboration as their own grades. My `primary`/`secondary` matches 3x5x2 A vs C, `confirmed` matches Admiralty 1 and 3x5x2 B, and `unknown` matches Admiralty 6.
   - **What does not apply** (my reading): their source-*reliability* axis is graded on a track record, and this repo has no per-source history, so nearly every row would be F, "cannot be judged". Their 6-point likelihood scale also asks the worker for a probability judgment, which a worker would invent. I left both out.
4. **How nature solves it (my #6).** In honeybee swarms choosing a nest site, a scout advertises a site only after inspecting it herself, and the decision waits for enough independent inspectors. This is from my own knowledge (Seeley's work), not checked this session.
5. **Does the analogy fit (my #7)?** What is the same: first-hand inspection is worth more than hearsay, and corroboration means independent inspection. What differs is the key condition. Bees enforce independence through the mechanism itself, while web sources copy one another, so two pages can be one source. I dropped the quorum idea. I kept one piece: `confirmed` counts only an **independent primary** source, never two secondaries quoting the same paper.
6. **A small experiment beats the argument (my #2).** Five reviewers and five experts have now debated this. Labelling about 30 rows costs less than another round.
7. **Write the prediction first (my #3), with a control (my #4).**
   - Control: the current four tags with the `research-file.md` definitions.
   - Treatment: the two axes.
   - Sample: the 5 colliding rows above plus 25 rows drawn at random with a fixed seed from the r2 INDEX.
   - Labelers: two, on different engines, blind to the existing labels.
   - Prediction:
     - Agreement between the labelers is higher with the two axes than with the control.
     - The same claim from the same paper gets identical tags under the two axes.
     - Under the control it does not.
   - Stop: before the next research run starts.
8. **Small and reversible (my #8).** Change only `research-file.md` and use it on one research run. The other files listed above change only after that run.
9. **How sure I am (my #10).** The collision evidence is n=1 run (5 rows across 2 claim pairs, plus 1 template line). It is a strong hint, not a law. That the two axes *fix* it is not measured.

## What I need to know
- **Columns:** two columns (`Read`, `Backing`) or one cell holding both, like "primary · claimed"? If scripts or greps rely on a single `Label` column, then one cell is cheaper. Otherwise two columns are cleaner.
- **Reproduction:** should `confirmed` require an actual re-run (our own or a third party's), or is an independent primary source repeating the number enough? If a re-run is required, then today almost no row qualifies; the r2 digest says "No number here was independently re-run". The tag would be honest but rare.
- **The referee:** should the referee's Corroborate stage count `confirmed` rows? If so, the meaning of "independent" must match SPEC §4 B, and only EJ changes the SPEC.
- **Old files:** does EJ accept leaving them unrelabelled with the read-map? If EJ wants them relabelled, that is a separate, larger job with a risk of upgrading labels.

## Costs and risks
- **Two judgments per row instead of one** (my #10). More work for the worker, and `shown` versus `claimed` can drift ("does a table in a paper count as shown?"). The experiment in my #3 measures exactly this, and if agreement on that axis is low, the proposal fails.
- **Vocabulary break** (my #5). Ten accepted files and five earlier files stay in the old words, so readers need the read-map. Grep-based counts across dates stop lining up.
- **Code changes** (my #8). The `LABELS` constant in `research-agent-memory.js` and any checker built on `check-findings.py` must change. Trying it on one run first limits the damage.
- **Test cost** (my #2): about 30 rows × 2 schemes × 2 labelers, roughly four engine calls plus my comparison.
  - The comparison script would be one I wrote, so its result is not independent evidence. Agreement percentages are simple enough for EJ to recount by hand.
- **The test may fail** (my #9). If the two axes agree no better than the control, that is reported as a result, and the fallback is the one-line tie-break: "a performance claim is `reported` even from a primary source". That is cheaper, but it keeps two meanings in one label.

## How we would know I was right
- **In the experiment** (written before the result): agreement with the two axes is higher than with the control on the same 30 rows, and all 5 colliding rows get identical two-axis tags from both labelers. Equal or lower agreement means I was wrong (my #1, my #9).
- **In the next research run:**
  - The INDEX's duplicate table has no pair where the same claim from the same paper carries different tags.
  - No section has to write its own "Label convention applied" paragraph, as s5 did.
  - Every `claimed` row names a source, and every `confirmed` row names an independent primary source's id. Both are checkable with grep.
