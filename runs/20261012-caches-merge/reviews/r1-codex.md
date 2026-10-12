### Strengths of A

- **My reading:** A is the better starting point for memory-entry routing. Its table covers discovery, exact identifiers, completeness, absence, lifecycle links, rationale, drift, resumption and non-Python paths (A:56–72). B disperses that guidance across its per-store explanations.
- A includes concrete acceptance criteria for disposal, rebuilding, missing caches, source attribution and triggers (A:340–394). These make the design more reviewable, although several criteria need correction below.
- A preserves disagreements and acknowledges that the code-graph contributor coordinated with another agent. The evidence record explicitly distinguishes disagreement from corroboration. [DECISION-RULES.md:21–35, 132–164](/home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md:21)

### Strengths of B

- **My reading:** B foregrounds the development/testing questions the user actually wants answered: definitions, callers, affected tests, rationale, configuration and concepts (B:93–102). A contains the same development table and benchmark section.
- The principal benchmark figures match the saved results: category scores, output means, rebuild times and the 14.68 ms maximum. Both versions disclose unequal output formats, exclusion of misses and the absence of an end-to-end agent trial. [results.md:13–28, 30–102, 276](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md:13)
- B clearly leaves the proposed expansion from memory retrieval to code/docs retrieval to EJ (B:111–114). The proposal file is explicitly for acceptance, amendment or rejection. [vision-proposals.md:3–6](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/vision-proposals.md:3)
- **Evidence strength, shared by both:** Codex authored the questions and initial gold; five Claude agents checked the categories; opencode authored the harness; Claude audited and repaired it. This is one repository and one 40-question set, with 6–10 questions per category, four runtime-recall questions and three subprocess questions—not independent replications. The repaired harness and revised prose were not re-reviewed. [routing/state.md:37–60, 67–76](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/state.md:37)

### Errors and weaknesses

- **A:262 — high.** A replaces EJ’s vector threshold with a measurement-decided comparison; A:276 and R5 repeat that change. The cited comparison method is a **draft proposal**, while the settled vision says all three trigger numbers belong to EJ. A:324 simultaneously retains the old ownership statement. Sources: [enhance/SOURCE_OF_TRUTH.md:3, 165–180](/home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/SOURCE_OF_TRUTH.md:165), [vision:33](/home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md:33). Measurements can inform EJ’s decision; they cannot silently replace it.

- **A:43 — medium.** “A cache is never the answer to a question the files answer” would exclude every legitimate derived cache: its information necessarily comes from files. The vision requires files to remain authoritative and readable without caches; it does not prohibit cheaper retrieval of the same information. Source: [vision:25–29, 34](/home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md:25).

- **A:18 — medium.** The claimed blind verification “on this file’s text” overstates the recorded check. The verifier examined `DECISION-RULES.md`, and found the planted alteration partly by diffing against the clean copy. That does not independently validate the final A document or its later threshold changes. Source: [enhance/run-report.md:15–17, 28–39](/home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/run-report.md:28).

- **A:75 — medium.** The paragraph mixes measured timings with unsupported costs. The 226K-token figure belongs to a 1,144-document enterprise benchmark, not the synthetic 10,000-entry grep test; “opening every hit” is not its established mechanism. The claimed `INDEX.md` scan under 0.01 s also has no measurement. Sources: [S-F4:55–60 and S-F13:98–107](/home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/sqlite-fts.claude.md:55), [DECISION-RULES.md:149–151, 191–193](/home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md:149). The primary paper confirms the token figures but describes accumulated model usage with bounded search/read tools. [BM25 paper, §4.4 and Appendix C.2](https://arxiv.org/html/2607.26497v3)

- **A:90 — low.** Gitignored does not mean absent from disk. Three SQLite files currently exist under `runs/20261012-caches-routing/bench/.cache/`. The benchmark record itself names those persistent files. Source: [bench/README.md:40](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/README.md:40). The inherited recon explanation is wrong.

- **A:197; B:124 — high.** Comparing only the newest source mtime cannot guarantee “stale never answers.” **My counterexample:** delete an indexed entry without making a surviving file newer than the cache; the condition never rebuilds, and the deleted entry remains searchable. Preserved timestamps create another failure. The source records this heuristic, alongside content-hash alternatives, but establishes no stale-answer guarantee. Source: [S-F9:80 and S-F15:115–120](/home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/sqlite-fts.claude.md:115). A:352–357 elevates the incomplete heuristic into acceptance criteria.

- **A:67; B:216 — high.** Last modification of an entry is not its last verification against code. An unrelated entry edit can hide code changes since verification. The cited memory requirement explicitly binds staleness to the **verified revision**, and describes diffing covered paths from that revision. Source: [RECOMMENDATION.md:44, 194–198](/home/smoke01/dev/ancient-games/runs/20261011-project-memory-engines/RECOMMENDATION.md:194). Git is the right substrate; this comparison is the wrong baseline for the stated verification question.

- **A:124; B:51 — medium.** The table calls the character metric “first right answer,” although it stops at the first line naming a gold **file**. Later statements that the caches “save reading” also exceed what was measured. The caveats are good but contradict these summaries. Source: [results.md:26–28](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md:26). This is evidence about printed output, not answer completion, agent tokens or development time saved.

- **A:138; B:65 — medium.** BM-7 has the wrong unit and aggregation description. The coverage reducer produces **test-file sets**; 0.78 is the mean of four question-level recalls, not the overall share of individual tests found. The recorded file counts imply graph recall of 8/13 across question/file instances, versus 4/13 for grep/FTS/hybrid. Sources: [derive_maps.py:1–3, 22–32](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/cov/derive_maps.py:1), [runtime-recall.json:2–109](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/nodes/runtime-recall.json:2). Keep 0.78, but label it macro-average test-file recall, n=4.

- **A:141; B:68 — medium.** “Grep found 1 of 3” needs a completeness qualifier. Grep hits C06 and C07, but retrieves only half C07’s gold files. Thus it finds something relevant for 2/3 questions and a complete gold set for 1/3. Source: [results.md:200–214](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md:200).

- **A:153; B:80 — medium.** The experiment is described as testing “the vector index” without identifying its embedding model. It tests `minishlab/potion-base-8M`, a static Model2Vec model. Those results do not establish the performance of the alternative contextual embeddings discussed later. Sources: [build.py:50–51](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/build.py:50), [V-F18:206–220](/home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/vector.claude.md:206).

- **A:173; B:100 — medium.** Configuration coverage has an undisclosed benchmark defect: E02’s gold answer is `pyproject.toml`, but all search routes are restricted to `.py` and `.md`. Its failure is therefore partly corpus exclusion, not retrieval quality. Sources: [queries.json:681–695](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/queries.json:681), [chunk.py:4, 38](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/chunk.py:38). An actual agent also needs a manifest/config-file route.

- **A:168; B:95 — medium.** The development table omits the graph’s Python-only scope and the warning that a nonempty caller/test result can still be incomplete. Falling back only on an empty answer does not address missing edges in a nonempty answer. Sources: [G-F12:119–120](/home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/code-graph.opencode.stdout.md:119), [runtime-recall.json:90–109](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/nodes/runtime-recall.json:90). Put these limits in the lookup table.

- **A:177; B:109 — medium.** Saying R1–R8 apply unchanged does not resolve their mismatch with code/docs retrieval. A’s R5.1 requires an overflowing memory index; R6 requires active-entry status and `covers`; R7 requires an entry filename. These cannot apply literally to arbitrary code nodes and documentation chunks. Source: [A:370–387](/home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md:370). B additionally references R1–R8 without including or directly linking their definitions.

- **A:265; B:191 — medium.** “The positive results found combine vectors with keyword search” is too broad even for memory-style text. V-F3 reports vector-only outperforming grep in five of ten file-delivery harness/model pairs. Hybrid-only can remain a proposed policy, but the evidence does not compel it. Source: [V-F3:60–68](/home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/vector.claude.md:60).

- **A:66 — low.** The rationale row cites `s3-F4`, which concerns StateTape’s staleness maintenance. The relevant rationale finding is `s3-F21`, also used by A’s underlying decision record. Sources: [research INDEX.md:119, 136](/home/smoke01/dev/ancient-games/docs/research/20261011-agent-memory-graph-r2/INDEX.md:119), [DECISION-RULES.md:52](/home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md:52).

### Conflicts between A and B

- **Who decides thresholds.** A:262–276 substitutes measured cost comparisons; B:189–202 retains EJ’s chosen miss count. **B is better supported:** the settled vision reserves the numbers for EJ, and V-F13 explicitly calls the threshold EJ’s rather than a research finding. A’s comparison method is useful as a proposal. [vision:33](/home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md:33), [V-F13:165–168](/home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/vector.claude.md:165).

- **Graph for exact lookup.** A:53 says the graph is only for multi-hop questions, and A:62 routes exact identifiers to files. B:95–97 proposes graph lookup for definitions and callers. A’s later table repeats B, so this is also an internal conflict in A. **B’s proposal is better supported for finding Python candidates in this experiment:** graph and grep tie at 0.75 on exact identifiers, with smaller graph output. **A’s caution is better supported for exhaustive call sites and absence claims.** These are different question contracts and need separate rows. [results.md:34–40, 215–229](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md:34), [G-F15:58–60](/home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/code-graph.opencode.stdout.md:58).

- **Finding rationale versus supplying rationale.** A:66 says no cache for “why”; B:99 proposes full-text to locate the relevant documentation. **B is better supported for discovery; A for answering:** BM-4 measures retrieval hits, while the memory design requires reading the decision and evidence before relying on it. [results.md:68–78](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md:68), [SOURCE_OF_TRUTH.md:114–117](/home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md:114).

The benchmark sections otherwise agree and derive from the same run. Their agreement provides no additional independent evidence.

### Proposed merged outline

1. **Status, scope and EJ’s pending decisions — combine both.** Link the settled vision; distinguish current memory scope from proposed code/docs expansion. Keep trigger ownership explicit.
2. **One question-to-route table — combine both, with new text.** Use A’s memory coverage and B’s development rows. Include corpus, prerequisite, route, fallback and answer limitation in each row. Add configuration files, function behaviour, exhaustive callers and dead-code questions.
3. **Shared never-rules — take from A, corrected.** Preserve disposal, full rebuild, on-demand reads and authoritative files. Add a checkable session-start prohibition and a freshness contract covering deletion and model changes.
4. **Build triggers — combine both.** Keep B’s EJ-owned thresholds; present A’s measurement comparisons as proposed evidence for EJ. Define code/docs triggers only through an explicit vision proposal.
5. **Three store designs — combine both.** Scope active-entry filters to memory, identify graph language coverage, and specify consistent publication of FTS/vector rebuilds.
6. **Development/testing evidence — take from B, corrected.** Name the embedding model, metric units, corpus exclusions, cold-start costs and exact sample sizes. Retain the full-suite safeguard.
7. **Acceptance criteria — take from A, corrected.** Separate common cache criteria from memory-specific and proposed code/docs criteria.
8. **Evidence provenance and unresolved questions — combine both.** Name each check’s author, distinguish self-checks from independent checks, and preserve unmeasured outcomes and pending EJ decisions.

### Not checked

- I did not rebuild caches, rerun benchmarks or execute tests.
- I checked the saved local evidence and selected primary web sources: the BM25 scaling paper, codegraph drift report and Anthropic guidance. I did not independently verify every external research citation.
- End-to-end token savings, development time saved, graph-ordered testing benefits and real project-memory retrieval remain unmeasured.
- No files were changed, and no other reviewers’ reviews were consulted.
