# 范蠡 (Fan Li) — Sorting Insights and Engine for Dave

## Answer
Sort the 62 insights by extending the four existing Source categories into six disjoint buckets (`config`, `tool`, `check-guard`, `check-test`, `instruction-spec`, `instruction-workflow`), choosing task insights via (c) both the main agent scoping categories and Dave picking from the indexed lines; run Dave on Claude Opus 5.5 (costing ~$0.02 to $0.05 per question with prompt caching and category filtering) and revisit when the corpus reaches 200k tokens or any single category exceeds 50k tokens.

## How I decided

1. **Examine the existing ground before drawing boundaries (my #18).** I asked whether defensive preparations are inspected: 「審備則可以戰乎？」王曰：「巧。」 (`quoted`). In `runs/20261016-six-experts/research/insight-sections.txt`, all 62 sections are already cleanly partitioned by their recorded `Source` field into four mutually exclusive groups: `instruction` (22), `check` (18), `tool` (14), and `config` (8). However, inspecting the preparations reveals a critical defect: 24 of the 62 entries (lines 8–15, 18–29, 33–35) have no title recorded in `insight-sections.txt`, only a file path, failure ID, and Source. Sorting by "what went wrong" from titles alone fails because those 24 entries have no title to evaluate.

2. **Adapt what already worked for the state to the household (my #16).** As recorded: 「計然之策七，越用其五而得意。既已施於國，吾欲用之家。」 (`quoted`). We should not invent a disconnected taxonomy from recall when a proven four-part structure already exists. Keep `config` (8) and `tool` (14) intact, and split the two largest buckets (`instruction` and `check`) along their natural structural fault lines to reach exactly six categories:
   - `config` (8 sections): Environment variables, PATH precedence, sandbox limits, and cache paths (e.g., F-132f1953, F-90389583).
   - `tool` (14 sections): Subprocess execution, exit codes, pipes, subagent timeouts, and external engine limits (e.g., F-60cad515, F-785afc27).
   - `check-guard` (10 sections): Referee hooks, late criteria enforcement, session boundary tracking, and harness gate failures (e.g., F-f09b058d, F-8392b4ce, F-3e11ce16).
   - `check-test` (8 sections): Automated test assertions, unit test suites, regression tests, and mutant detection (e.g., F-8712e9fc, F-15cf1278, F-969500fa).
   - `instruction-spec` (12 sections): Ambiguities in prompt specifications, contracts, mixing instructions with literal values, and schema definitions (e.g., F-4cbb2f4b, F-05a1b440, F-d8a49e5a).
   - `instruction-workflow` (10 sections): Operational procedures, runner execution order, editing scripts while running, manual typing slips, and missing diagnostic steps before retry (e.g., F-f44538b2, F-a03fa5b3, F-acf5f562).

3. **Test against the 62 titles: identify sections fitting none or two (my reading).** Testing the proposed six categories against `insight-sections.txt` reveals:
   - *Fitting none (24 sections)*: Lines 8–15, 18–29, and 33–35 have empty title strings in `insight-sections.txt`. If classified strictly by title text, all 24 fit none. Under my placement rule, each is placed deterministically by its recorded `Source` and underlying failure section.
   - *Fitting two (ambiguous by title alone)*:
     - Line 53 (`F-2cdebf3b — the reviewer found the guard-JSON checks incomplete; F-d0736dc7 — the new test then caught my own shape check`): bundles two separate failures into one section, spanning both `instruction-spec` and `check-guard`/`check-test`.
     - Line 50 (`F-76013d09 — the guard's pipe tests failed inside the Codex sandbox only`): mentions pipe tests failing (suggesting `check-test` or `tool`), but failed due to sandbox constraints and is tagged `config`.
     - Lines 30, 36, and 37 (`F-76d8d965`, `F-5e6801ed`, `F-7ed1bcd4`): all describe the identical symptom ("codex exit 0 with missing output/error"), yet root causes span `config` (shim shadowing PATH), `instruction` (prompt lacking output check), and `check` (asserting exit status only).
   - *Placement rule*: Every section is placed primarily by its recorded `Source` field, breaking ties within `instruction` and `check` by the root-cause mechanism. Multi-failure sections (line 53) are indexed by their primary failure ID.

4. **Join the orchestrator and the worker through complementary duties (my #14 and my #1).** Inside the four borders, people's affairs belong to 種; outside, decisive action belongs to 蠡: 「四封之內，百姓之事，蠡不如種也。四封之外，敵國之制，立斷之事，種亦不如蠡也。」 (`quoted`). Success requires human affairs joined with Heaven and Earth: 「夫人事必將與天地相參，然後乃可以成功。」 (`quoted`). Therefore, pick related insights using **(c) both**:
   - The main agent (orchestrator) names the 1–2 applicable categories when writing the question prompt, preventing Dave from loading irrelevant categories.
   - Dave reads the filtered one-line-per-section index for those categories and selects the exact insight IDs to cite in his answer (serving U1).

5. **Eliminate disqualified engines and honor quota reality (my #3).** When conditions are unripe, completion cannot be forced: 「時不至，不可彊生；事不究，不可彊成。自若以處，以度天下，待其來者而正之，因時之所宜而定之。」 (`quoted`). Research confirms Codex has 0% quota left today and caps input at 922k tokens (R15), eliminating it immediately. Furthermore, Fan Li is already assigned to `agy` (Gemini 3.8 Flash), Sun Tzu to `dsh` (deepseek-flash), and Laozi to `opencode` (MiniMax-M3.1). Dave was designed as the Claude control seat (`six_experts.py:48`, R1, R2). Replacing Dave's engine collapses engine diversity.

6. **Select model and count costs with prompt caching (my #17).** Sending the one who can part with resources avoids disaster: 「彼非不愛其弟，顧有所不能忍者也。…前日吾所爲欲遣少子，固爲其能棄財故也。而長者不能，故卒以殺其弟，事之理也，無足悲者。」 (`quoted`).
   - *Engine & Model*: Claude Opus 5.5 (`claude-opus-5-5`), with Claude Sonnet 5.5 as the direct cost-reduction alternative.
   - *Cost per question*: Today's total insights are ≈25k tokens (≈93 KB). Claude Opus 5.5 charges $4/MTok input, $20/MTok output, with prompt cache reads at $0.20/MTok (5% of input) (R1, R4). A full cold call costs ~$0.10 input; a cache hit costs ~$0.005 input. Loading only the 1–2 related categories (~4k–9k tokens) via Decision 1 costs ~$0.016–$0.036 cold, and ~$0.001–$0.002 on cache hits. Adding ~1k tokens of output ($0.02) yields **~$0.02 to $0.05 per question** on cached runs. On Sonnet 5.5 ($2/$10, R1), it costs ~$0.01 to $0.03.

7. **Set limits and stop when the count is reached (my #10, my #5, and my #7).** Ancient generals stopped when the count was exhausted: 「臣聞古之善用兵者，贏縮以為常，四時以為紀，無過天極，究數而止。」 (`quoted`). Do not plan early, but do not shift established plans on the field: 「天節固然，唯謀不遷。」 (`quoted`), and 「有奪，有予，有不予，王無蚤圖。夫吳，君王之吳也，王若蚤圖之，其事又將未可知也。」 (`quoted`).
   - *Growth measurement*: Insights grow at ≈40–50 KB/day (≈10k–13k tokens/day).
   - *Revisit Trigger 1 (200k tokens total)*: In ~14–18 working days, total insights will hit 200k tokens. At this threshold, Anthropic's verified context rot warning (R5: "As token count grows, accuracy and recall degrade") becomes measurable if full loads occur, requiring category loading to be strictly enforced.
   - *Revisit Trigger 2 (50k tokens in a single category)*: When any single category exceeds 50k tokens, one-line index scanning alone will strain Dave's prompt budget, requiring sub-indexing or semantic retrieval.
   - *Revisit Trigger 3 (800k tokens capacity horizon)*: At 80–100 working days away (≈4 MB), Claude's 1M window ceiling (R1) will leave insufficient room for output and reasoning (noted in research: a 1M file leaves no room for output). The engine and storage architecture must be fundamentally migrated before reaching 800k.

8. **Proposed change to the pattern (my reading).** *Proposed change to the pattern*: Enforce a strict "one failure, one title, one category" contract on all future insight sections. Currently, line 53 bundles two failures (`F-2cdebf3b` and `F-d0736dc7`), and 24 sections omit titles in the manifest. Enforcing this format at generation time ensures `insight-sections.txt` is always 100% deterministically indexable without manual disambiguation.

## What I need to know
- Whether EJ requires Dave to remain strictly on Claude Opus 5.5 to preserve the established control definition, or permits Claude Sonnet 5.5 to halve prompt costs ($2 vs $4 per MTok input, R1). If Sonnet 5.5 is permitted, run Sonnet 5.5; if Opus 5.5 is required as the baseline control, run Opus 5.5.
- Whether Dario (the plain control) should also be evaluated on the exact same category-filtered context as Dave, or receive zero insights. If Dario receives no insights, Dario directly measures the marginal lift of Dave's rules + insights.

## Costs and risks
- **Context rot risk (my #10, citing R5):** Claude models suffer degraded recall as prompt length scales (R5). Loading all 25k tokens (and eventually 200k+) unpartitioned degrades Dave's attention. Mitigation: strictly enforce category filtering so Dave only loads ~4k–9k tokens per question.
- **Cache miss cost penalty (my #17, citing R1, R4):** A cold Claude Opus call costs 20x more than a cache hit ($4.00 vs $0.20/MTok, R1). If questions arrive intermittently past the 5-minute cache TTL, costs rise from ~$0.02 to ~$0.12 per call.
- **Classification ambiguity on edge cases (my #18):** Sections like F-76013d09 and F-2cdebf3b/F-d0736dc7 touch multiple layers. If the main agent misidentifies the category, Dave will not load the relevant past failure and may repeat it (violating U2).

## How we would know I was right
- **Category partition check:** Run a script verifying that all 62 entries in `insight-sections.txt` map to exactly one of the six categories with zero unassigned and zero duplicates.
- **Use case U1 and U2 validation:** When Dave is given a task involving a known failure mode (such as bun cache writing under HOME, F-90389583, or mixing spec literals with instructions, F-05a1b440), Dave correctly cites the insight ID in his answer and avoids generating the defect.
- **Token and cost telemetry:** Dave's prompt token consumption per question stays between 5,000 and 15,000 tokens (well below the 25k total corpus), and billing logs verify the per-question cost remains under $0.05 on cached calls.
