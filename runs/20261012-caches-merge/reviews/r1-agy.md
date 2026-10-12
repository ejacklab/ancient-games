### Strengths of A

- **Full two-domain query routing coverage:** [`version-A.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L41-L100) provides the 15-row decision table for markdown memory-entry questions (distinguishing free-text recall, meaning-based matching, multi-hop structural reach, exact identifiers, completeness scans, proving absence, structured headers, rationale, drift, and session startup) alongside the 8-row table for development and testing on code and docs ([`version-A.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L166-L176)).
- **Complete specification of Core Requirements (R1–R8):** Includes the full requirements framework ([`version-A.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L335-L395)) with checkable criteria (disposable/derived R1, full rebuild R2, staleness rejection R3, absence fallback R4, observable triggers R5, active entry filter R6, source naming R7, and rebuild cost bounds R8) required by the vision ([`caches-memory-vision-statements.md`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md#L8)).
- **Transparent ledger of costs, gaps, and disagreements:** Retains the cost evidence summary ([`version-A.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L74-L84)), notes explicit GAPs for real memory corpora, and preserves the six unresolved multi-engine disagreements (D1–D6) from [`DECISION-RULES.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L134-L165) without forcing a false consensus.
- **Answers EJ's architectural precedent question:** Incorporates the repo recon ([`version-A.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L90-L96)) explaining why SQLite is not visible in git (gitignored `.db`, [`ancient_games/index.py`](file:///home/smoke01/dev/ancient-games/ancient_games/index.py) indexing the referee journal rather than memory, and unbuilt `project-memory/`).
- **Complete provenance and review metadata:** Explicitly records the run lineage and caveats ([`version-A.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L16-L27)), including the enhancement runs and the link to the external vision file.

### Strengths of B

- **Strict alignment with the Vision on trigger authority ("EJ's number"):** Correctly attributes trigger thresholds directly to EJ ([`version-B.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L189-L190), [`L202`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L202), [`L228`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L228))—matching [`caches-memory-vision-statements.md`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md#L33) ("all three numbers are EJ's") and [`CLAUDE.md`](file:///home/smoke01/dev/ancient-games/CLAUDE.md#L78-L79) ("Never fill a gap with my own value").
- **Avoids citations to non-existent document sections:** Does not reference the unmerged/reverted phantom section `SOURCE_OF_TRUTH.md § How each threshold is found` that Version A repeatedly cites.
- **Compact focus on repo-measured routing:** Places the empirical development and testing benchmarks ([`version-B.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L28-L115)) immediately after "The answer first", directly answering EJ's speed and token cost objective for this codebase.
- **Sound architectural foundations for individual stores:** Fully preserves the 5 Whys and 5W1H analyses for SQLite FTS5, vector search, and the code graph.

### Errors and weaknesses

- `A:262-264`, `A:302-303`, `A:371`, `A:375`, `A:379`, `A:392`: Version A repeatedly asserts that trigger thresholds are determined by a "measured comparison (`SOURCE_OF_TRUTH.md` § How each threshold is found)". In [`SOURCE_OF_TRUTH.md`](file:///home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md), no such section exists (it was part of 77 unrequested lines added during an earlier run and reverted at EJ's instruction; see [`state.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/state.md#L75-L82)). This also contradicts the vision rule that all trigger thresholds are EJ's policy decisions.
  - *Source line showing error:* [`SOURCE_OF_TRUTH.md:1-127`](file:///home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md#L1-L127) (section absent); [`caches-memory-vision-statements.md:33`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md#L33).
  - *Severity:* High.
- `B:1-257`: Version B completely omits the "When to use which store" section (the query-time decision routing table for memory entries, the cost summary, the unresolved disagreements D1–D6, and the explanation of why SQLite is not visible). An agent querying memory entries has no routing guidance in Version B.
  - *Source line showing error:* [`DECISION-RULES.md:37-65`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L37-L65); [`version-A.md:41-100`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L41-L100).
  - *Severity:* High.
- `B:1-257`: Version B completely omits the Core Requirements section (R1–R8). It lacks the checkable acceptance criteria defining disposable caches, full rebuilds, staleness checks, fallback behavior, and active entry filters required by the vision.
  - *Source line showing error:* [`caches-memory-vision-statements.md:8`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md#L8); [`version-A.md:335-395`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L335-L395).
  - *Severity:* High.
- `A:66`: In the memory decision table, row "Why did we choose this, or why is this line like this?" cites `s3-F4`. `s3-F4` is StateTape (staleness from a code-graph diff), not rationale. The rationale synthesis finding is `s3-F21` / `SOURCE_OF_TRUTH.md`.
  - *Source line showing error:* [`DECISION-RULES.md:52`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L52); [`code-graph.opencode.stdout.md:309`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/code-graph.opencode.stdout.md#L309).
  - *Severity:* Medium.
- `A:141` and `B:68`: Both versions state for BM-8: "Full-text search on the file name found 2 of 3; grep found 1 of 3 and printed up to 8.7K characters." The benchmark results show `rg` (grep) scored `symbol hit@10 = 1` and `file hit@10 = 1` on C06 ([`results.md:205`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L205)) and C07 ([`results.md:210`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L210)), missing only C05 ([`results.md:200`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L200)). Grep found gold files for 2 of 3 questions, not 1 of 3.
  - *Source line showing error:* [`results.md:200`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L200), [`L205`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L205), [`L210`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L210).
  - *Severity:* Medium.
- `B:104-105`: Version B claims: "This table is for the code and docs. Memory entries are covered by the per-store sections below." This statement is inaccurate: the per-store sections below provide store architecture and 5W1H build triggers, not question-routing rules.
  - *Source line showing error:* [`version-B.md:134-240`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L134-L240).
  - *Severity:* Medium.
- `A:76-77`: Version A lists "grep plus opening every hit, about 226K tokens per question" without contextualizing that this figure comes from `S-F4`'s 1.7M-token general RAG corpus benchmark with a paths-only agent, not a memory corpus on this system.
  - *Source line showing error:* [`sqlite-fts.claude.md:57-58`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/sqlite-fts.claude.md#L57-L58); [`DECISION-RULES.md:146-148`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L146-L148).
  - *Severity:* Low.
- `B:1-15`: Version B omits the header provenance blocks detailing the enhance run, the routing benchmark run, and the pointer to [`caches-memory-vision-statements.md`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md).
  - *Source line showing error:* [`version-A.md:16-27`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L16-L27).
  - *Severity:* Low.

### Conflicts between A and B

1. **Trigger threshold determination: "Measured comparison in `SOURCE_OF_TRUTH.md`" vs "EJ's number"**
   - *What A says:* The thresholds for building vector indexes (miss count), code graphs (false-alarm rate), and rebuild budgets are defined by a "measured comparison (`SOURCE_OF_TRUTH.md` § How each threshold is found), not a number to guess" ([`version-A.md:262-263`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L262-L263), [`L302-303`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L302-L303), [`L371-392`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L371-L392)).
   - *What B says:* These thresholds are explicitly "**EJ's number**" ([`version-B.md:189`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L189), [`L202`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L202), [`L228`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L228)).
   - *Which is better supported and why:* **Version B is better supported.** The vision statement ([`caches-memory-vision-statements.md:33`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md#L33)) states: "Every trigger is observable, and all three numbers are EJ's." Furthermore, [`SOURCE_OF_TRUTH.md`](file:///home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md) does not contain a section titled "§ How each threshold is found". Version A cites a non-existent phantom section that was reverted during an earlier run ([`state.md:75-82`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/state.md#L75-L82)).
2. **Routing table scope: Dual tables vs Single table with phantom deferral**
   - *What A says:* Provides two explicit routing tables: a 15-row table for memory entries ([`version-A.md:56-72`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L56-L72)) and an 8-row table for code and docs ([`version-A.md:166-175`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L166-L175)), noting that the two differ because their underlying corpora differ ([`version-A.md:177-179`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L177-L179)).
   - *What B says:* Includes only the 8-row code and docs table, asserting that memory entries are covered by the per-store sections below ([`version-B.md:104-105`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L104-L105)).
   - *Which is better supported and why:* **Version A is better supported.** The per-store sections below do not route memory queries. Without A's table, an agent querying memory entries has no routing guidance for supersession, absence proof, exact identifiers, or drift checks. A's table is grounded in the 21-row table in [`DECISION-RULES.md:42-65`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L42-L65).
3. **Core Requirements (R1–R8): Retained vs Omitted**
   - *What A says:* Retains the 8 Core Requirements R1–R8 ([`version-A.md:335-395`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L335-L395)).
   - *What B says:* Omits Core Requirements entirely, terminating at line 257.
   - *Which is better supported and why:* **Version A is better supported.** The vision statement explicitly identifies [`CACHES.md`](file:///home/smoke01/dev/ancient-games/docs/memory-system/CACHES.md) as the document carrying Core Requirements R1–R8 ([`caches-memory-vision-statements.md:8`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md#L8)). Omitting them removes the architectural contract.
4. **Header and Recon Context: Retained vs Stripped**
   - *What A says:* Retains header notes on the enhance and routing runs, records D1–D6 disagreements, and answers EJ's question on why SQLite is not visible on disk ([`version-A.md:16-27`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L16-L27), [`L85-99`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L85-L99)).
   - *What B says:* Strips these sections out.
   - *Which is better supported and why:* **Version A is better supported.** The recon section directly answers EJ's prompt question ("why I don't see the sqlite"), grounded in [`recon.md:1-26`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/recon.md#L1-L26).

### Proposed merged outline

Version A should serve as the structural base, corrected by Version B's trigger wording and verified benchmark figures.

1. **Title and Frontmatter Notes**
   - *Action:* **Combine both.**
   - *Detail:* Take Version A's header ([`version-A.md:1-28`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L1-L28)), including research provenance, review notes, enhance run notes ([`runs/20261012-caches-enhance/`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/)), routing run notes ([`runs/20261012-caches-routing/`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/)), and the pointer to [`caches-memory-vision-statements.md`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md).
2. **The answer first**
   - *Action:* **Take from A** (identical in B).
   - *Detail:* Re-states that no cache is needed today for memory entries, each requires an observable trigger, and caches are optional and derived ([`version-A.md:29-40`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L29-L40)).
3. **When to use which store: Query routing**
   - *Action:* **Combine both with new routing index.**
   - *Detail:* Present two clearly demarcated sub-sections to allow single-lookup routing:
     - *Part 1: Markdown memory entries (15 questions)*: Take from Version A ([`version-A.md:41-73`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L41-L73)), with the citation fix on line 66 (change `s3-F4` to `s3-F21` / `SOURCE_OF_TRUTH`).
     - *Part 2: Code and docs development & testing (8 questions)*: Take from Version A ([`version-A.md:164-176`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L164-L176)) / Version B ([`version-B.md:91-103`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L91-L103)).
     - *New text needed:* A two-line lookup rule at the start of the section: "For memory entry questions (`project-memory/`), consult Part 1. For development and testing questions on code and docs, consult Part 2."
4. **Measured here: development and testing**
   - *Action:* **Combine both with factual repair.**
   - *Detail:* Take the benchmark section from Version A ([`version-A.md:101-163`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L101-L163)) / Version B ([`version-B.md:28-90`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L28-L90)). Correct BM-8 text to reflect [`results.md:205-210`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L205-L210): state that grep found gold files for 2 of 3 questions (C06 and C07) while printing up to 8.7K characters, rather than "1 of 3". Retain the note acknowledging the conflict with the vision regarding code/docs caches, leaving the decision to EJ ([`vision-proposals.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/vision-proposals.md#L1-L48)).
5. **Costs, gaps, and unresolved disagreements**
   - *Action:* **Take from A.**
   - *Detail:* Absent in B. Retain Version A's cost discussion, GAPs, and the D1–D6 disagreement records ([`version-A.md:74-89`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L74-L89)).
6. **Why no SQLite is visible in this repo**
   - *Action:* **Take from A.**
   - *Detail:* Absent in B. Retain Version A's recon analysis ([`version-A.md:90-100`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L90-L100)) explaining [`ancient_games/index.py`](file:///home/smoke01/dev/ancient-games/ancient_games/index.py), gitignored database files, and unbuilt memory.
7. **Rules for all three caches**
   - *Action:* **Take from A** (identical in B; [`version-A.md:189-206`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L189-L206)).
   - *Detail:* Full rebuild never patched, rebuild before answering when stale, fall back when absent, index active entries only.
8. **SQLite full-text index (5 Whys and 5W1H)**
   - *Action:* **Take from A** (identical in B; [`version-A.md:207-242`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L207-L242)).
   - *Detail:* Preserves BM25 rationale, 10M token crossover context, and stdlib implementation plan.
9. **Vector index (5 Whys and 5W1H)**
   - *Action:* **Take from B for trigger wording; otherwise combine.**
   - *Detail:* In Why-4 and 5W1H When ([`version-B.md:189-190`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L189-L190), [`L202`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L202)), use Version B's wording designating the miss threshold as "**EJ's number**", deleting Version A's citations to `SOURCE_OF_TRUTH.md § How each threshold is found`.
10. **Code graph (5 Whys and 5W1H)**
    - *Action:* **Take from B for trigger wording; otherwise combine.**
    - *Detail:* In Why-5 ([`version-B.md:228`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L228)), use Version B's wording designating the false-alarm tolerance as "**EJ's number**", deleting Version A's citation to `SOURCE_OF_TRUTH.md § How each threshold is found`.
11. **What this changes elsewhere (proposed, not done)**
    - *Action:* **Take from A** (identical in B; [`version-A.md:316-321`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L316-L321)).
    - *Detail:* Preserves proposals regarding git timestamp comparisons for drift checks.
12. **Not known**
    - *Action:* **Take from A** (identical in B; [`version-A.md:322-332`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L322-L332)).
    - *Detail:* Preserves open trigger items, absence of memory corpus data, and extract caveats.
13. **Core requirements (R1–R8)**
    - *Action:* **Take from A with trigger repairs.**
    - *Detail:* Absent in B. Adopt Version A's requirements framework ([`version-A.md:335-395`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L335-L395)). Repair R5.1, R5.2, R5.3, and R8.2 by removing all references to `SOURCE_OF_TRUTH.md § How each threshold is found` and replacing them with `OPEN: EJ's number`, harmonizing R1–R8 with the vision.

### Not checked

- **Other reviewers' Round 1 outputs:** Did not inspect [`reviews/r1-codex.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/reviews/) or [`reviews/r1-opencode.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/reviews/), preserving strict reviewer independence for Round 1.
- **Raw web source verification:** Did not byte-check cited external URLs (arXiv papers, GitHub issues/READMEs, sqlite.org docs); accepted research node citations as recorded in [`sqlite-fts.claude.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/sqlite-fts.claude.md), [`vector.claude.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/vector.claude.md), and [`code-graph.opencode.stdout.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/code-graph.opencode.stdout.md).
- **Execution of benchmarks or test suite:** Did not run local shell commands or execute scripts (`pytest`, `bench.py`, or `code_graph.py`), relying strictly on saved artifacts ([`results.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md) and [`runtime-recall.json`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/nodes/runtime-recall.json)).
