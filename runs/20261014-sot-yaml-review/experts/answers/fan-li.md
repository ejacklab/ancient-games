# 范蠡 (Fan Li) — Review of the memory requirements YAML draft

## Answer
Another AI agent will not follow this YAML draft reliably because gates and defaults are entangled in shared text blocks, dependencies are buried in prose, and critical checks depend on an unassigned reviewer (*my reading*). To serve an agent reliably, split compound requirements into single-clause items with dedicated levels, attach `fails_if` and `who_decides` directly to each requirement, extract references into a structured `links` list, and assign every judged check to a concrete role before enforcement.

## How I decided

1. **The draft cannot be relied upon because its defensive preparations are unexamined and incomplete (my #18).**
   When Goujian asked what would make it possible to fight, Fan Li answered: 「審備則可以戰乎？」王曰：「巧。」 — "If the preparations are examined, can we then fight?" The king: "Skilful." (韋昭: 備，守禦之備; 巧，審密不可攻入也 — defensive preparations, so close-knit they cannot be broken into — `quoted`, my #18). The round-trip check written by the COO (Claude) established only that words were carried over from Markdown without loss; it did not establish that an agent can execute or verify them (*my reading*). Today, `tools/memory_index.py` automates only file naming, id structure, and index formatting; all other checks, including critical MUST gates, rely on an unassigned "reviewer" (*my reading*). Handing an agent requirements whose verification mechanisms are incomplete leaves the defenses open to failure.

2. **Layout Choice A: Level per clause — Split the text into clauses with separate levels (my #18, my #5).**
   The draft preserves the original prose block under `text:` while placing a summarized split in `level:` (for example, W1.1 lists `MUST: one file per entry...` and `SHOULD: the folder...`). This forces an agent to parse and map two diverging representations of the same rule (*my reading*). Fan Li taught: 「天節固然，唯謀不遷。」 — "Heaven's rhythm is like that; only the plan does not move" (`quoted`, my #5). When a plan's text and its enforcement levels do not map one-to-one, an agent cannot discern whether violating a SHOULD clause in a shared paragraph trips the MUST gate (*my reading*). To make preparations close-knit (my #18), split each clause into its own requirement item with a single scalar level (`MUST` or `SHOULD`) and its own explicit text.

3. **Layout Choice B: Where `fails_if` sits — Place `fails_if` on each requirement, not once per group (my #2, my #18).**
   Fan Li identified three affairs of state: 「持盈者與天，定傾者與人，節事者與地。」 — "Keeping the full goes with Heaven; steadying the tilting goes with people; regulating affairs goes with Earth" (`quoted`, my #2). Regulating affairs on the ground requires exact boundaries. A single `fails_if` per group conflates multiple requirements and bundles MUST gates with SHOULD defaults (for example, W1 bundles W1.1 MUST id formats with W1.2 SHOULD header lines). If a group check fails, an agent cannot tell which requirement broke or whether it must halt work immediately or record a justified exception (*my reading*). Each requirement must carry its own distinct `fails_if` condition (my #18).

4. **Layout Choice C: Links — Extract inline references into a structured `links:` list (my #16, my #18).**
   Inline references such as `(K4.1)` or `(W3.6)` buried in English prose force downstream agents or scripts to use regex or NLP heuristics to resolve dependencies (*my reading*). Fan Li stated: 「計然之策七，越用其五而得意。既已施於國，吾欲用之家。」 — "Ji Ran's policies were seven; Yue used five of them and got what it wanted. Since they have been applied to the state, I want to use them for the household" (`quoted`, my #16). The memory system already specifies explicit frontmatter fields (`depends_on`, `supersedes`) for entry files; the requirements document should apply that same proven method to itself. A machine-readable `links:` list allows agents and automated evaluators to traverse dependency graphs without misinterpreting explanatory prose (my #18).

5. **Layout Choice D: Who decides — Add an explicit `who_decides` field per requirement (my #14).**
   When assigning duties, Fan Li stated boundaries plainly: 「四封之內，百姓之事，蠡不如種也。四封之外，敵國之制，立斷之事，種亦不如蠡也。」 — "Inside the four borders, the people's affairs: I am not as good as 種. Outside the four borders, dealing with enemy states, matters decided on the spot: 種 is not as good as I" (`quoted`, my #14). An AI agent cannot reliably execute open-ended requirements without knowing who holds authority over each choice. In Rd5.3, EJ decides mismatches; in W6.3, the merging agent resolves file collisions; in W4.1, any writer may change an entry. Omitting `who_decides` leaves open choices unowned, causing agents either to overreach or to freeze when exceptions occur (*my reading*).

6. **What to keep in the draft (my #2, my #3).**
   Keep the three-category lifecycle (Write, Keep, Read), which maps cleanly to regulating affairs, preserving stability, and maintaining limits (my #2). Keep the definitions of MUST, SHOULD, and guidance at the top of the file, as they establish constant rules of engagement (my #3).

7. **Other hazards that will cause agents to misread or skip requirements (my #14, my #18, my #3).**
   - **The unassigned reviewer:** Requirements W1.3, W3.1, W3.3–W3.6, W5.3, K1.1, Rd2.3, Rd4.5, Rd5.1, and Rd5.3 depend on a "reviewer" finding violations. Because no reviewer role or agent is defined or dispatched, an agent reading this file will treat these checks as unenforced and skip them (*my reading*, my #14).
   - **Substantive rules hidden inside `guidance`:** Several items labelled `guidance` contain operative constraints and exceptions rather than advice (for example, Rd5.4 carves out explicit exemptions to the Rd5.3 MUST rule). Agents instructed that guidance has "nothing to pass or fail" will skip these clauses and misidentify valid states as violations (*my reading*).
   - **Unmeasured adoption of YAML:** Moving requirements from Markdown into YAML was decided on intuition rather than empirical testing (*not measured*). Fan Li warned: 「時不至，不可彊生；事不究，不可彊成。」 — "When the time has not come, growth cannot be forced; when the matter has not run its course, completion cannot be forced" (`quoted`, my #3). Token consumption and multi-engine parsing reliability for this YAML schema have not been measured against Markdown in this repository (*not measured*).

## What I need to know

1. **Who acts as the "reviewer" for judged checks?** If EJ is the reviewer, the schema must specify `who_decides: EJ` and accept that execution will block on human input; if an automated harness or secondary agent is the reviewer, the evaluation criteria must be specified in executable form before enforcing them as MUST gates.
2. **How will downstream agents consume this file?** If agents ingest the raw YAML file into context prompts, the verbose schema will increase token overhead; if an automated tool parses it into a validation report, strict syntactic keys and clause splitting are strictly necessary.

## Costs and risks

1. **Increased token footprint and context overhead (my #3).** Splitting text into single clauses and adding `links` and `who_decides` fields across all 46 requirements will substantially increase token count compared to the concise Markdown document, raising per-task context costs for every agent that reads it.
2. **Human bottleneck on judged checks (my #14).** Explicitly naming EJ under `who_decides` for all unautomated judged checks will increase interruptions and halt autonomous agent workflows whenever a subjective boundary is reached.
3. **Synchronization drift between prose and requirements (my #5).** Separating prose in `SOURCE_OF_TRUTH.md` from requirements in a separate YAML file introduces dual-maintenance risk; if either file is modified without the other, the constancy of the design is broken (「唯謀不遷」, my #5).

## How we would know I was right

Run an evaluation across the target engines (Claude, Codex, Gemini, DeepSeek, MiniMax) providing identical test repositories with three intentional defects: an unassigned judged violation, a breached SHOULD default, and a broken MUST gate. Compare error detection, false stop rates, and hallucinated passes between the COO's draft layout and the clause-split, fully attributed layout. If the clause-split layout with explicit `who_decides` and single-level clauses achieves lower defect miss rates and eliminates unhandled blockages without human referee intervention, the recommendation is verified.
