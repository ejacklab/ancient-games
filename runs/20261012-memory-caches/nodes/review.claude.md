VERDICT: REPAIR

Reviewer: claude, blind. Document: `runs/20261012-memory-caches/verify/CACHES-review-copy.md` (cited below as "doc:N"). Sources read: the three research nodes, `SOURCE_OF_TRUTH.md` (SOT), `RECOMMENDATION.md` M4/M6 (and, for context, M18), INDEX.md s3 rows, `KNOWLEDGE_GRAPH_DESIGN.md`. Nothing else in the run folder.

Counts: high 0, medium 5, low 8.

## The five items

1. **Grounding: FAIL (minor).** Most citations hold: S-F1, S-F2, S-F4 (5.8K vs 226K), S-F5 (37,000 = 10M / 0.27M per 1,000), S-F9 quote, S-F13 numbers (0.53 s, 0.104 s), S-F16, V-F3, V-F4, V-F11, V-F12 (400-650), V-F13, V-F18 (speed not measured), G-F5 4.3%, G-F5c, G-F12 (0.94 s, 0.00-0.01 s), G-F14, G-F18, G-F21 (KNOWLEDGE_GRAPH_DESIGN.md §1 is lines 14-54; the "track record" text is line 31), M4, M6, SOT lines 68-73, 75, 104. Failures: F-2 (grep at 50,000), F-6 (RRF cite V-F14), F-7 ("option B in S-F13"), F-8 (embedding-model fallback under S-F9).
2. **No invented values: FAIL.** One unsourced number: "500 files" (doc:68). See F-1. Every other number traces to a source or is marked EJ's.
3. **Labels: FAIL.** Four conclusions stated as fact without a label (F-3, F-4 partly, F-5, F-9). The `my reading` and `not measured` labels that are present are correct (doc:37, 51, 53, 55-56, 84, 89, 101, 135).
4. **Coverage: PASS.** SQLite (doc:43-60 whys, 62-71 table), vector (75-93, 95-104), code graph (108-125, 127-136): five whys each and all six 5W1H rows each. The Why row only points back to the whys above; that is acceptable.
5. **Logic: FAIL (one real gap, F-4).** The objective (optional cache, rebuilt from files, absence never blocks reading) is respected throughout. One argument rests on a practice the design forbids.

## Findings

**F-1 (medium) doc:68.** "Built when the trigger fires: `INDEX.md` can no longer list every active entry, or `entries/` passes 500 files." No source gives 500. The nearest figure is V-F12's "400-650 entries" for 200,000 tokens, which is an estimate from a 300-500 token assumption, not a threshold. The doc's own "Not known" list (doc:146-148) says every trigger number is EJ's and does not list this one. Shows: `vector.claude.md:145-149` (V-F12, "my assumption, not measured"); `SOURCE_OF_TRUTH.md:126` (size limit is EJ's number). Fix: drop the second clause, or mark it EJ's number to set.

**F-2 (medium) doc:50-51.** "grep answered in under half a second at 50,000 synthetic entries (S-F13)". In S-F13 the one-word grep (the free-text case this sentence argues about) at 50,000 entries is "invalid" because the clock went negative. The 0.148 s grep figure at 50,000 is the structured-query chain, not free-text search. The valid free-text grep figure is 0.038 s at 10,000. Shows: `sqlite-fts.claude.md:105` and `:107` ("The 50,000-entry grep timing printed a negative number ... I discard it"). Fix: cite 10,000 entries / 0.038 s, or name the structured query.

**F-3 (medium) doc:91-93.** "Every positive result found combines vectors with keyword search (V-F6, V-F7; V-F10 is unproven); vectors alone were the weakest arm (V-F3, V-F4)." Universal claim, contradicted by the same node. V-F5 reports dense retrieval beating BM25 "by large margins" for code issue localization. V-F3 reports that with file-based delivery "programmatic vector exceeds programmatic grep on five of ten harness-model pairs", so vector alone was not the weakest arm there. V-F7 shows hybrid beating embeddings, which is not a positive result for vectors. Shows: `vector.claude.md:80-87` (F5), `:64-67` (F3 not uniform). The source's own sentence is narrower ("evidenced to help in combination", `:307-309`, citing F7, F10, F13 and qmd, not F6). Fix: say "for memory-style text, the positive results found are hybrid" and label it my reading, or name the exceptions (code; file-based delivery).

**F-4 (medium) doc:82-84.** Why-3 cites "Under about 200,000 tokens, Anthropic's guidance is to read the whole knowledge base rather than retrieve (V-F8)" as a reason not to build vectors. The design forbids reading the whole tree: `SOURCE_OF_TRUTH.md:121-123` ("Never loaded at all: ... the whole `project-memory/` tree at once"); M18 agrees. The research node noted this ("F8 is a bound on the cost of 'read it all', not a rule", `vector.claude.md:148-149`) and the doc dropped the caveat. A builder could read the sentence as permission to load all entries. It also gives no weight to V-F8's own note that the 2024 context figure has since moved (`vector.claude.md:107-109`). Fix: restate as "retrieval is unnecessary only in the sense that reading everything would fit, which the design does not do", or drop V-F8 from the argument and keep V-F11 and the INDEX.md argument.

**F-5 (medium) doc:14-16.** "at the size a project memory reaches, `INDEX.md`, grep and git already answer the questions each cache would answer." Stated as fact. `project-memory/` does not exist and no source measures any of the three caches on a memory corpus (doc:148-149; `sqlite-fts.claude.md:143`, `vector.claude.md:316-317`, `code-graph.opencode.stdout.md:111`). This is an inference from "no evidence of need", which the doc itself says elsewhere. Needs the label "my reading" and a pointer to the "Not known" list. The conclusion (not needed today) is fine; the basis is not labelled.

**F-6 (low) doc:100.** "merged ... by reciprocal rank fusion (V-F14)". V-F14 (qmd) does not mention RRF (`vector.claude.md:172-180`). RRF appears in the Hybrid paragraph (`:307-310`, qmd README and Zep) and in V-F13 (Zep, `:156-157`). It is also a design choice with no "my reading" label.

**F-7 (low) doc:71.** "about the smallest option in `S-F13` (option B)". Option B is in the node's section 5 (`sqlite-fts.claude.md:136`), not in F13. Also, "one row per active entry file" is presented as settled; S-F17 says row grain is not settled by any source (`:127`, `:138`).

**F-8 (low) doc:34-35.** "If the cache file, SQLite's FTS5 or the embedding model is missing, the tool warns once and answers with grep (S-F9)". S-F9 covers a missing `sqlite3` or FTS5 (`sqlite-fts.claude.md:80`). The embedding-model case is not in S-F9; it follows from M4/M6 and `vector.claude.md:310-312` (V-F-list Q5 filters). Cite those for that part. "Opens the cache read-only" is the doc's own design step, not marked.

**F-9 (low) doc:59-61 and doc:67.** "Do not need SQLite" is stated as fact on a latency basis. S-F13 says that at every size the zero-hit structured scan was tested, "latency is not a reason", and that "token cost to the agent is the real axis and this test does not measure it" (`sqlite-fts.claude.md:107`). S-F3 says no source measures an agent on header-field queries (`:49`). Also, S-F13 and S-F16 are the researcher's own tests; the opening labels (doc:9-10) name only S-F13 and G-F12. S-F16 is 8 queries, 4 tokenizers, one row (`:125`).

**F-10 (low) doc:47-48.** The 5.8K vs 226K figure is given without its context: it is the 1.7M-token tier of a general RAG corpus, against a grep tool that returns paths only (`sqlite-fts.claude.md:57-58`). By S-F5 that tier is about 6,000 entries. A reader sees a 39x token gap and then "not needed", with no statement of why the 500-entry trigger is far below it. Not wrong, but half the picture.

**F-11 (low) doc:117.** "It adds a silent failure that git does not have (G-F5 drift, 4.3% of edges wrong)". The 4.3% is codegraph's incrementally synced index. The doc's own rules (doc:27-30) and its chosen later option (the in-repo `code_graph.py`) are full-rebuild and, per G-F18, cannot drift (`code-graph.opencode.stdout.md:181`). The reason applies to the external indexer, not to the in-repo graph. Say which.

**F-12 (low) doc:140-141.** "The research answers it. It is a build detail." `SOURCE_OF_TRUTH.md:78-79` lists this as "Not decided yet (EJ decides)". The doc does mark the section "proposed, not done", but it should say "proposed answer; EJ decides", not "build detail".

**F-13 (low) doc:104.** "Nothing is installed today." V-F19 says no embedding runtime is installed, but numpy 2.4.3 is (`vector.claude.md:228-229`, `:284`). Option A needs numpy plus `model2vec`. Say "no embedding runtime".

## Not checked

- Whether the cited external pages say what the research nodes quote (arXiv, GitHub, sqlite.org). I only checked the doc against the nodes. The S-F extracts are, by their own header, not byte-checked.
- The researchers' local measurements (the S-F13 benchmark script, the G-F12 timings). I did not re-run them.
- Whether the doc's claim "SQLite 3.45.1 with FTS5 works here (verified 2026-10-12)" is true now; it rests on the S node.
- Authorship line (doc:3) and the "planted tool" paragraph (doc:152-153), which depend on `state.md`, which I was not allowed to read. Both nodes mention `state.md:71` consistently.
- RECOMMENDATION.md beyond rows M4, M6, M18 and a grep for related lines. INDEX.md rows other than s3-F4, F20, F25, F27, F34.
- The other `KNOWLEDGE_GRAPH_DESIGN.md` line numbers the G node cites (45-50, 355-366, 524-528); the doc does not cite them directly, only its §1.
- Whether the "400-650 entries" and "37,000 entries" estimates are consistent with each other: they use different entry sizes (about 270 tokens in S-F5, 300-500 in V-F12). Each is labelled as an assumption in its own node, and the doc does not mix them.
