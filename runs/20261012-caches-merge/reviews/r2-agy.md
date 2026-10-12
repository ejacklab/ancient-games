### Where I agree with the others

- **Retain the memory-entry routing table from Version A (`version-A.md:41–73`).** All three reviewers agree this table is indispensable. Version B completely omits memory-entry routing and asserts at [`version-B.md:104–105`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L104-L105) that the per-store descriptions cover it, which is false: the per-store sections describe build triggers and architecture, not question routing. The memory routing table is grounded in [`DECISION-RULES.md:42–65`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L42-L65).
- **Retain Core Requirements R1–R8 from Version A (`version-A.md:335–395`).** All three reviewers agree Version B's omission of R1–R8 leaves a dangling cross-reference at [`version-B.md:109`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L109) and violates the vision contract ([`caches-memory-vision-statements.md:8`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md#L8)), which explicitly designates `CACHES.md` as the home of R1–R8.
- **Adopt Version B's trigger threshold wording ("EJ's number").** All three reviewers agree Version B is better supported at [`version-B.md:189`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L189), [`L202`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L202), and [`L228`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L228). Version A cites a phantom section `SOURCE_OF_TRUTH.md § How each threshold is found` that does not exist in the active document ([`SOURCE_OF_TRUTH.md:1–127`](file:///home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md#L1-L127)), existing only in a draft proposal file ([`runs/20261012-caches-enhance/SOURCE_OF_TRUTH.md:165`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/SOURCE_OF_TRUTH.md#L165)). The vision settles threshold authority: *"all three numbers are EJ's"* ([`caches-memory-vision-statements.md:33`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md#L33)).
- **Correct the rationale citation on row `A:66`.** All three reviewers agree that citing `s3-F4` (StateTape staleness diff off a code graph; [`code-graph.opencode.stdout.md:309`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/code-graph.opencode.stdout.md#L309)) for "Why did we choose this..." is a citation error. The correct rationale findings are `s3-F21` ([`INDEX.md:136`](file:///home/smoke01/dev/ancient-games/docs/research/20261011-agent-memory-graph-r2/INDEX.md#L136)) and `M19` / `SOURCE_OF_TRUTH` ([`DECISION-RULES.md:52`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L52)).
- **Qualify the 226K token cost figure (`version-A.md:76`, `version-B.md:140`).** All three reviewers agree this figure derives from `S-F4`'s 1,144-document enterprise RAG benchmark ([`sqlite-fts.claude.md:55–58`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/sqlite-fts.claude.md#L55-L58)) using a paths-only file-system agent, and was not measured on a memory corpus or code in this repository.
- **Clarify the BM-8 benchmark summary (`version-A.md:141`, `version-B.md:68`).** All three reviewers agree that saying "grep found 1 of 3" is inaccurate without qualification. Grep named a gold file on 2 of 3 questions (C06 and C07) and retrieved a complete gold set on 1 of 3 ([`results.md:200–214`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L200-L214)).
- **Preserve the cost ledger, GAPs, and multi-engine disagreements D1–D6.** All three reviewers agree that the unresolved disagreements D1–D6 ([`DECISION-RULES.md:134–165`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L134-L165)) and empirical GAPs must be preserved rather than averaged into a false consensus.

---

### Where I disagree

1. **SQLite visibility explanation on disk (`version-A.md:90–95`)**
   - *Other reviewer's position:* Codex showed that asserting "No `.db` is ever on disk" is factually false because three SQLite files exist on disk at `runs/20261012-caches-routing/bench/.cache/{fts,vec,graph}.sqlite` ([`bench/README.md:40`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/README.md#L40)). Opencode conceded this point in round 2.
   - *My position in round 1:* Listed A:90 as a strength of A that answers EJ's question by explaining that SQLite is not visible because `.db` files are gitignored and never committed.
   - *Verdict:* **Change.**
   - *Reason and source:* Codex is factually correct. [`version-A.md:90`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L90) explicitly states: *"No `.db` is ever on disk"*. That statement is contradicted by [`bench/README.md:40`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/README.md#L40), which documents persistent `.cache/*.sqlite` files created during the routing run. Gitignore explains why SQLite files are not committed to git, not why they cannot exist on disk. I change my position: the paragraph must be corrected to explain that SQLite files are gitignored and derived (and thus uncommitted), while preserving the valid architectural precedents from [`DECISION-RULES.md:171–182`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L171-L182) (`ancient_games/index.py` indexing the referee journal, `code_graph/code_graph.py` indexing code, and unbuilt `project-memory/`).

2. **"The answer first" opening scope (`version-A.md:29–39` / `version-B.md:16–26`)**
   - *Other reviewer's position:* Opencode maintained keeping A:29–39 verbatim. Codex held that "The answer first" requires an explicit scope restriction: "None of the three caches is needed today" must be scoped specifically to memory entries (`project-memory/`) so it does not contradict the empirical code/docs development benchmark that follows.
   - *My position in round 1:* Proposed taking A:29–39 verbatim, summarizing it as re-stating that no cache is needed today for memory entries.
   - *Verdict:* **Change** (to adopt Codex's explicit scope qualification).
   - *Reason and source:* While my round-1 summary interpolated "for memory entries", the actual text of [`version-A.md:31`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L31) states flatly: *"None of the three caches is needed today."* Without an explicit scope limiter, this flat claim contradicts the 40 benchmark results on code and docs ([`version-A.md:101–163`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L101-L163)) where caches outperform grep. Per [`caches-memory-vision-statements.md:15–17`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md#L15-L17), the settled vision applies to `project-memory/`. I change my position: the opening must explicitly state that no cache is needed today *for memory entries*, framing code and docs retrieval as a proposed expansion governed by [`vision-proposals.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/vision-proposals.md#L1-L6).

3. **Query routing prohibition on derived caches (`version-A.md:43`)**
   - *Other reviewer's position:* Codex identified that *"a cache is never the answer to a question the files answer"* would ban all derived caches, since derived caches inherently retrieve information from files. The vision requires files to remain authoritative and readable, not retrieval banned ([`caches-memory-vision-statements.md:25–29, 34`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md#L25-L29)). Opencode accepted this in round 2.
   - *My position in round 1:* Did not flag `A:43`; accepted the text introducing the memory table.
   - *Verdict:* **Change.**
   - *Reason and source:* Codex is correct. The vision states that markdown is always the source of truth and caches are optional and derived ([`caches-memory-vision-statements.md:29`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md#L29)), but their explicit purpose is to keep retrieval cheap when sequential reading of files becomes too expensive ([`caches-memory-vision-statements.md:25–26`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md#L25-L26)). Banning caches whenever files can answer the question makes derived caches impossible. I change my position: the rule must be reworded to state that markdown files remain the authoritative source of truth, while derived caches provide cheaper retrieval paths once triggered.

4. **Freshness check heuristic and deletion flaw (`version-A.md:197`, `version-B.md:124`, `version-A.md:356`)**
   - *Other reviewer's position:* Codex identified that comparing only the newest source mtime cannot guarantee "stale never answers": deleting an entry does not make surviving files newer, leaving deleted rows searchable indefinitely ([`sqlite-fts.claude.md:115–120`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/sqlite-fts.claude.md#L115-L120)). Opencode accepted this in round 2.
   - *My position in round 1:* Accepted the newest-mtime rule in section 7 and R3.1 without objection.
   - *Verdict:* **Change.**
   - *Reason and source:* Codex's deletion counterexample exposes an architectural flaw. Under [`version-A.md:197`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L197) and `A:356` (R3.1), the check compares `max(source mtime)` against cache mtime. When an entry is deleted, surviving mtimes are unchanged, no rebuild is triggered, and deleted entries remain searchable. Because memory entries live in git ([`caches-memory-vision-statements.md:22`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md#L22)), freshness must be bound to the git commit revision or content/manifest hash ([`sqlite-fts.claude.md:118`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/sqlite-fts.claude.md#L118), F11/F15; [`version-A.md:352–353`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L352-L353)). I change my position: R3.1 and the freshness rule must require commit or manifest hash verification to handle deletions.

5. **Memory drift baseline: Entry mtime vs Verified git revision (`version-A.md:67`, `version-B.md:216`)**
   - *Other reviewer's position:* Codex showed that comparing code changes against entry mtime (`git log --since=<entry-mtime>`) is invalid: editing an entry updates its mtime without re-verifying it against code, concealing intervening code changes. M15 binds staleness to the `verified_at` git revision ([`RECOMMENDATION.md:44, 194–198`](file:///home/smoke01/dev/ancient-games/runs/20261011-project-memory-engines/RECOMMENDATION.md#L44)). Opencode accepted this in round 2.
   - *My position in round 1:* Retained `A:67` as written in the memory decision table.
   - *Verdict:* **Change.**
   - *Reason and source:* Codex's analysis is directly grounded in the memory design specification. [`RECOMMENDATION.md:44`](file:///home/smoke01/dev/ancient-games/runs/20261011-project-memory-engines/RECOMMENDATION.md#L44) (M15) states: *"Staleness is bound to the revision an entry was verified against and to changes in the code, config or dependencies it covers, not to age."* Lines 194–198 describe diffing covered paths from `verified_at` to HEAD. Using entry file mtime masks code changes whenever an entry's markdown is touched for maintenance or metadata edits. I change my position: the drift check route must be bound to git diff from `verified_at` to HEAD.

6. **Definition lookup vs Exhaustive call-site routing (`version-A.md:168`, `A:170` vs `DECISION-RULES.md:58`)**
   - *Other reviewer's position:* Opencode in round 1 called `A:168` a flat contradiction of [`DECISION-RULES.md:58`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L58). Codex countered that `DECISION-RULES.md:58` combined two distinct contracts: definition lookup (where the code graph tied grep at 0.75 hit@5 with 3x smaller output; [`results.md:34–40`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L34-L40)) vs exhaustive call-site discovery (where 3,874 unresolved calls prevent proving completeness; [`code-graph.opencode.stdout.md:119`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/code-graph.opencode.stdout.md#L119)). Opencode accepted Codex's split in round 2.
   - *My position in round 1:* Adopted `A:168` and `A:170` in the development routing table without distinguishing definition candidates from exhaustive caller contracts.
   - *Verdict:* **Change.**
   - *Reason and source:* Codex is better supported by the benchmark and node evidence. For Python definitions, the code graph achieved 0.75 hit@5 with 43 chars vs grep's 129 chars ([`results.md:34–40`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L34-L40)). But for caller enumeration and dead code (`A:170`, [`DECISION-RULES.md:58, 60`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L58)), unresolved calls mean the graph's answer is a non-exhaustive lower bound. Furthermore, `A:175`'s fallback rule ("if the first-choice tool returns an empty answer, fall back to grep") fails on partial caller lists. I change my position: split definition lookup (code graph) from exhaustive callers / dead code (`none` + grep), state the graph's limits, and update the fallback rule to fire on empty *or* partial answers.

7. **Section ordering in the merged document**
   - *Other reviewer's position:* Opencode in round 1 placed the benchmark evidence at section 7 (after recon). Codex placed development/testing evidence *after* the store designs and triggers (section 6), establishing the memory system architecture before presenting code/docs empirical proposals. Opencode accepted Codex's order in round 2.
   - *My position in round 1:* Placed benchmark evidence immediately after the query routing table (section 4), mirroring Version A's flow.
   - *Verdict:* **Change.**
   - *Reason and source:* Codex and Opencode's round-2 consensus is structurally superior. Placing 60+ lines of benchmark results directly after the opening creates narrative dissonance: it forces the reader to jump from "None of the three caches is needed today" (for memory) straight into benchmarks where caches win on code, before the store designs or build triggers have even been defined. Presenting memory architecture first (scope, query routing, never-rules, triggers, store designs), followed by the repository's empirical development evidence, then acceptance criteria and provenance, provides a coherent logical structure. I change my position to adopt Codex's section ordering.

8. **Routing table presentation: Dual separate tables vs Single unified table**
   - *Other reviewer's position:* Codex and Opencode (round 2) propose unifying all routing into a single table with a `Corpus` column (`project-memory/` vs `code & docs`), prerequisites, route, fallback, and answer limitations.
   - *My position in round 1:* Proposed keeping two demarcated sub-sections (Part 1: Memory, Part 2: Code/docs) under section 3.
   - *Verdict:* **Change.**
   - *Reason and source:* In [`version-A.md:56–72`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L56-L72) and [`L166–175`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L166-L175), separating memory questions from development questions by 90 lines was confusing. Unifying them into a single table with an explicit `Corpus` column eliminates fragmentation, enables single-lookup routing for agents, and makes corpus boundaries unambiguous. I change my position to adopt the unified table format.

9. **Blind verifier claim in provenance header (`version-A.md:18–20`)**
   - *Other reviewer's position:* Codex and Opencode showed that A:18 overstates verification. The verifier checked `DECISION-RULES.md`, caught the plant on the planted copy (returning REPAIR), passed the clean copy, and diffed against the clean copy in the same directory ([`runs/20261012-caches-enhance/run-report.md:15–17, 30–39`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/run-report.md#L15-L17)). No verifier ever checked `version-A.md`.
   - *My position in round 1:* Listed A:18–20 as a strength of A ("Complete provenance and review metadata").
   - *Verdict:* **Change.**
   - *Reason and source:* The run report confirms that node 5 evaluated `DECISION-RULES.md`, and node 6 wrote `CACHES.md`. Version A was created after the verification pass. Claiming a blind verifier returned all four PASS "on this file's text" is inaccurate. I change my position: the provenance note must accurately record what was checked and what was not.

10. **BM-4 Graph cell: `n/a` vs `0.0 (over 2 questions)` (`version-A.md:131`, `version-B.md:58`)**
    - *Other reviewer's position:* Opencode showed that marking the BM-4 graph cell `n/a` converts a measured zero into an absence: [`results.md:76`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L76) recorded graph scoring `0.0 | 0.0 | -- (0) | 38.0 | 0.0005` over 2 applicable questions, as flagged in [`audit-0.json:79`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/nodes/audit-0.json#L79). Codex changed in round 2 to agree with Opencode.
    - *My position in round 1:* Did not flag this cell error.
    - *Verdict:* **Change.**
    - *Reason and source:* [`runs/20261012-caches-routing/bench/results.md:76`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L76) and [`audit-0.json:79`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/nodes/audit-0.json#L79) prove the graph was measured on category D and scored 0.0. I change my position: the cell must be reported as `0.0 (over 2 questions) / 38`.

11. **BM-7 Unit and aggregation (`version-A.md:138`, `version-B.md:65`)**
    - *Other reviewer's position:* Codex demonstrated that 0.78 is macro-average test-file recall over n=4 questions, not overall share of individual tests found ([`derive_maps.py:22–32`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/cov/derive_maps.py#L22-L32), [`runtime-recall.json:90–109`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/nodes/runtime-recall.json#L90-L109)). Opencode accepted this in round 2.
    - *My position in round 1:* Accepted the BM-7 text as written.
    - *Verdict:* **Change.**
    - *Reason and source:* [`runtime-recall.json:90–109`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/nodes/runtime-recall.json#L90-L109) confirms the scores for C01–C04 are 0.33, 0.8, 1.0, 1.0 (mean 0.7825). The unit is test-file recall, and C03/C04 have single-test gold sets. I change my position to label it macro-average test-file recall (n=4).

12. **Completeness and absence row citations (`version-A.md:63–64`)**
    - *Other reviewer's position:* Opencode showed that `A:63` cites `V-F21` ("Exact identifiers and rare terms"; [`vector.claude.md:240`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/vector.claude.md#L240)) instead of `V-F23` ("Top-k cannot enumerate or prove absence"; [`vector.claude.md:259`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/vector.claude.md#L259)), dropping the run record citations from [`DECISION-RULES.md:47, 49`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L47). Codex accepted this in round 2.
    - *My position in round 1:* Did not catch the citation substitutions on `A:63` and `A:64`.
    - *Verdict:* **Change.**
    - *Reason and source:* `V-F21` is exact identifiers; `V-F23` is the finding establishing that top-k cannot prove completeness or absence. I change my position to restore the full citation sets from [`DECISION-RULES.md:47, 49`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L47) (`V-F1, V-F23, S-F13, G-F14` for completeness; `V-F20, V-F23` for absence).

13. **Application of Core Requirements R1–R8 to code and docs (`version-A.md:177`, `version-B.md:109`)**
    - *Other reviewer's position:* Codex showed that asserting R1–R8 apply unchanged to code and docs fails because R5.1 (overflowing `INDEX.md`), R6 (active-entry filter / `covers`), and R7 (entry filename attribution) cannot apply literally to code AST nodes or markdown doc chunks. Opencode agreed in round 2.
    - *My position in round 1:* Treated R1–R8 as an undivided unit to take from A.
    - *Verdict:* **Change.**
    - *Reason and source:* Codex is correct. R1–R4 (disposable, full rebuild, freshness, fallback) are general cache invariants. R5.1, R6, and R7 are specific to `project-memory/`. Saying R1–R8 apply unchanged creates an uncheckable requirement for code/docs. I change my position: the requirements section must explicitly separate universal cache invariants from memory-specific criteria and proposed code/docs criteria.

14. **Character metric definition (`version-A.md:124`, `version-B.md:51`)**
    - *Other reviewer's position:* Codex showed that calling the metric "first right answer" exceeds what was measured: [`results.md:26–28`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L26-L28) defines `chars` as characters to the first line naming a gold *file*. Opencode agreed in round 2.
    - *My position in round 1:* Accepted the metric description as written.
    - *Verdict:* **Change.**
    - *Reason and source:* [`runs/20261012-caches-routing/bench/results.md:26–28`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L26-L28) explicitly defines the metric as characters to the first gold file. Claiming it measures answer completion or saved reading time exceeds the measurement. I change my position to use the exact source definition.

15. **Vector-only vs Hybrid evidence (`version-A.md:265`, `version-B.md:191`)**
    - *Other reviewer's position:* Codex showed that claiming positive results always combine vectors with keyword search overstates the source: [`vector.claude.md:60–68`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/vector.claude.md#L60-L68) (V-F3) reports programmatic vector retrieval beating grep in 5 of 10 harness-model pairs. Opencode agreed in round 2.
    - *My position in round 1:* Did not flag this overstatement.
    - *Verdict:* **Change.**
    - *Reason and source:* [`runs/20261012-memory-caches/nodes/vector.claude.md:65–66`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/vector.claude.md#L65-L66) explicitly states that with file-based delivery, vector retrieval exceeded grep on 5 of 10 pairs. Hybrid-only can remain a proposed policy, but the text must not claim empirical unanimity. I change my position to qualify the claim.

16. **Speed bound compliance vs Grep `git ls-files` overhead (`audit-0.json:93–94`)**
   - *Other reviewer's position (Opencode vs Codex):* Opencode argued in round 1 that finding 12 in `audit-0.json` (rg spawns `git ls-files` per query, adding ~1.2 ms / 16%) undercuts BM-9's 15 ms speed bound. Codex argued in round 2 that subtracting overhead reduces rg's time to ~6.2 ms, which does not undercut the 15 ms upper bound.
   - *My position in round 1:* Did not examine the audit findings in detail.
   - *Verdict:* **Hold Codex's position over Opencode's.**
   - *Reason and source:* Codex is better supported. Per [`audit-0.json:93–94`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/nodes/audit-0.json#L93-L94), rg's measured mean was ~7.4 ms with ~1.2 ms overhead. Removing overhead lowers grep's execution time to ~6.2 ms, comfortably beneath BM-9's 15 ms bound ([`results.md:15`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L15); maximum measured across all routes was 14.68 ms). Subtracting overhead strengthens compliance with the upper bound rather than undercutting it. The overhead must be disclosed to contextualize comparative timings between grep and FTS, but the 15 ms bound holds.

17. **Corpus snapshot stability during benchmark build (`state.md:48`)**
   - *Other reviewer's position (Opencode vs Codex):* Opencode noted in round 1 that `state.md:48` warned numbers must be rerun on a stable snapshot due to concurrent editing, and called for a rerun. Codex noted in round 2 that while a rerun on the repaired harness occurred (`state.md:59–64`), whether that rerun occurred on an isolated snapshot remains unconfirmed.
   - *My position in round 1:* Noted benchmark execution was not independently verified.
   - *Verdict:* **Hold Codex's position over Opencode's.**
   - *Reason and source:* Codex is better supported. [`runs/20261012-caches-routing/state.md:59–64`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/state.md#L59-L64) confirms node 3 was run on the repaired harness and determinism was established. However, the initial builder note ([`state.md:48`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/state.md#L48)) regarding concurrent editing during the build was not formally closed. This should be reported as an evidence caveat, not an assertion that no rerun ever occurred.

---

### Revised merged outline

The section order of the best version takes Codex's ordering (as adopted by Opencode in round 2), incorporating the factual corrections, unified routing table, and split acceptance criteria.

1. **Title, status, and provenance notes**
   - *Action:* **Combine both; new text needed.**
   - *Detail:* Take Version A's header pointers ([`version-A.md:16–27`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L16-L27)) to the enhance run, routing run, and vision statement. Replace the stale label block ("Two numbers come from checks the researchers wrote...").
   - *New text needed:* (a) Attribute the development/testing section to the main routing session ([`state.md:61`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/state.md#L61)); (b) record that Version B's "EJ's number" was adopted because `docs/memory-system/SOURCE_OF_TRUTH.md` contains no threshold section; (c) accurately report that the blind verifier evaluated `DECISION-RULES.md`, not `version-A.md` ([`run-report.md:15–17, 30–39`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/run-report.md#L15-L17)).

2. **The answer first: Status and scope**
   - *Action:* **Take from A; new text needed.**
   - *Detail:* Take [`version-A.md:29–39`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L29-L39) (caches optional, derived, rebuildable; unbuilt `project-memory/`; `G-F21` / `KNOWLEDGE_GRAPH_DESIGN.md`).
   - *New text needed:* Explicitly scope "None of the three caches is needed today" to **memory entries** (`project-memory/`). State up front that code and docs retrieval is a proposed expansion awaiting EJ's decision via [`vision-proposals.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/vision-proposals.md#L1-L6), and affirm that all three trigger numbers belong to EJ ([`caches-memory-vision-statements.md:33`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md#L33)).

3. **When to use which store: Unified query routing table**
   - *Action:* **Combine both; new text needed.**
   - *Detail:* Unify memory routing rows ([`version-A.md:56–72`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L56-L72)) and development/testing rows ([`version-A.md:166–175`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L166-L175)) into a single table with an explicit `Corpus` column (`project-memory/` vs `code & docs`), listing prerequisite, route, fallback, and answer limitations for each row.
   - *New text needed:*
     - Replace A:43's prohibition with the principle that markdown files remain the authoritative source of truth, while derived caches provide cheaper retrieval once triggered.
     - Restore correct citations on completeness (`V-F1, V-F23, S-F13, G-F14`) and absence (`V-F20, V-F23`), replacing `V-F21` ([`DECISION-RULES.md:47, 49`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L47)).
     - Correct rationale row to cite `M19, s3-F21, SOURCE_OF_TRUTH` ([`DECISION-RULES.md:52`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L52)), replacing `s3-F4`.
     - Re-bind memory drift check to git diff from `verified_at` to HEAD ([`RECOMMENDATION.md:44, 194–198`](file:///home/smoke01/dev/ancient-games/runs/20261011-project-memory-engines/RECOMMENDATION.md#L44)), eliminating `entry-mtime`.
     - Add config/manifest lookup row routed directly to grep, noting `pyproject.toml` exclusion from AST corpus (E02).
     - Split definition lookup (code graph) from exhaustive caller enumeration and dead code (`none` + grep), citing Python-only coverage ([`code-graph.opencode.stdout.md:269–270`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/code-graph.opencode.stdout.md#L269-L270)) and 3,874 unresolved calls ([`code-graph.opencode.stdout.md:119`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/code-graph.opencode.stdout.md#L119)).
     - Update fallback rule to trigger on empty *or* partial graph answers.

4. **Shared never-rules for all caches**
   - *Action:* **Take from A; new text needed.**
   - *Detail:* Take [`version-A.md:189–205`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L189-L205) (never source of truth, full rebuild only, fall back when absent, read-only open).
   - *New text needed:* Replace newest-mtime freshness rule with git commit revision or content/manifest hash verification to detect deletions ([`sqlite-fts.claude.md:115–120`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/sqlite-fts.claude.md#L115-L120)); add checkable session-start read prohibition (`M18`); scope active-entry filtering to memory corpora.

5. **Build triggers**
   - *Action:* **Combine both; take trigger wording from B.**
   - *Detail:* Adopt Version B's explicit trigger phrasing ("**EJ's number**"; [`version-B.md:189, 202, 228`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L189)), deleting all citations to `SOURCE_OF_TRUTH.md § How each threshold is found`. Retain Version A's cost comparisons as proposals informing EJ's decisions. Retain the three `OPEN:` criteria ([`version-A.md:370–379`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L370-L379)).

6. **Three store designs (5 Whys and 5W1H)**
   - *Action:* **Combine both; take trigger wording from B, rest from A; new text needed.**
   - *Detail:* Take SQLite FTS5, Vector index, and Code graph sections. Use Version B's trigger wording.
   - *New text needed:* Reconcile "Today: no graph" ([`version-A.md:310`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L310)) by distinguishing the unbuilt memory drift graph from the benchmarked code graph (`code_graph/code_graph.py`); reconcile 0.94 s repo build (`G-F12`) with 0.892 s benchmark build ([`results.md:15`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L15)); specify the static `minishlab/potion-base-8M` embedding model; qualify V-F3 to note programmatic vector beat grep on 5 of 10 pairs ([`vector.claude.md:65–66`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/vector.claude.md#L65-L66)).

7. **Empirical evidence: Development and testing benchmarks**
   - *Action:* **Take from B's placement, shared text from A/B; new text needed.**
   - *Detail:* Place the benchmark section here (following store designs and triggers). Take shared text [`version-A.md:101–163`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L101-L163) / [`version-B.md:28–90`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L28-L90).
   - *New text needed:*
     - BM-4: correct graph cell from `n/a` to `0.0 (over 2 questions) / 38` ([`results.md:76`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L76), [`audit-0.json:79`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/nodes/audit-0.json#L79)).
     - BM-7: label as macro-average test-file recall (n=4), noting C03/C04 single-test gold sets and the 10-function cap ([`runtime-recall.json:90–109`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/nodes/runtime-recall.json#L90-L109)).
     - BM-8: state full 3-part qualification (named gold file for 2 of 3; complete gold set for 1 of 3; 8.7K chars came from C05 miss; [`results.md:200–214`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L200-L214)).
     - BM-5: disclose E02 corpus exclusion (`pyproject.toml` outside `.py`/`.md` globs; [`queries.json:681`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/queries.json#L681), [`chunk.py:38`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/chunk.py#L38)).
     - Define `chars` metric as characters to the first line naming a gold *file* ([`results.md:26–28`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L26-L28)).
     - Disclose relevant audit qualifications (rg's ~16% `git ls-files` overhead, vector deduplication; [`audit-0.json:49–53, 91–109`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/nodes/audit-0.json#L49-L53)) and note the unverified snapshot warning ([`state.md:48`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/state.md#L48)).

8. **Costs, gaps, and architectural precedents**
   - *Action:* **Take from A; new text needed.**
   - *Detail:* Take [`version-A.md:74–89`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L74-L89) (cost ledger, GAPs, unresolved disagreements D1–D6) and [`L90–99`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L90-L99) (recon on repo precedents).
   - *New text needed:*
     - Qualify 226K tokens as EnterpriseRAG-Bench / S-F4 with a paths-only agent, not memory or repo code ([`sqlite-fts.claude.md:55–58`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/sqlite-fts.claude.md#L55-L58)).
     - Correct `A:82` over-claim: benchmark closes code/docs graph-vs-grep, not the vector-on-`entries/` gap.
     - Correct `A:90`: state that `.cache/*.sqlite` files exist on disk ([`bench/README.md:40`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/README.md#L40)) and explain that SQLite files are gitignored and uncommitted, preserving the valid precedents of `ancient_games/index.py`, `code_graph/code_graph.py`, and unbuilt memory.

9. **Core requirements and acceptance criteria (R1–R8)**
   - *Action:* **Take from A; new text needed.**
   - *Detail:* Retain the R1–R8 framework from [`version-A.md:335–395`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L335-L395).
   - *New text needed:*
     - Replace phantom citations in R5.1, R5.2, R5.3, R8.2 with `OPEN: EJ's number`.
     - Update R2.2 and R3.1 to require git commit or content hash verification for freshness to handle deletions.
     - Split acceptance criteria into three clear categories: universal cache invariants (R1–R4), memory-specific criteria (R5.1, R6, R7), and proposed code/docs criteria.

10. **Proposed changes elsewhere, evidence limits, and open items**
    - *Action:* **Combine both; new text needed.**
    - *Detail:* Take [`version-A.md:316–321`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L316-L321) (proposed drift git diff, updated to `verified_at`) and [`L322–332`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L322-L332) ("Not known").
    - *New text needed:* Explicitly list the three proposals from [`vision-proposals.md:1–48`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/vision-proposals.md#L1-L48) (P1 code/docs expansion, P2 cache types, P3 empty answer ≠ absence); preserve unreviewed status of harness repair and unmeasured end-to-end agent trial.
