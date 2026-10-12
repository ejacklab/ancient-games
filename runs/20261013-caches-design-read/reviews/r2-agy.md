### Points I now support

1. **B1.1 agent-side trigger event conflicts with Rd4.1 prohibition on recording non-misses**
   - **Raised by**: claude (Finding 2), codex (Finding 2), opencode (Finding 3). Location: `CACHES.md:327-329` and `CACHES.md:452-455`.
   - **Why it holds**: I missed this in round 1. B1.1 states that the full-text comparison runs *"when an agent notes in its journal that `INDEX.md` plus grep made it read through many hits to reach an entry"* (`CACHES.md:327-328`). However, Rd4.1 explicitly restricts journal notes to misses and mandates: *"Every other question goes unrecorded: a log of every search costs every search, and the comparisons do not need it"* (`CACHES.md:454-455`). An agent adhering to Rd4.1 will never record reading through many hits, rendering B1.1's agent-side trigger dead in practice. Rd4.1 must provide a home for this second journal note.

2. **K2.3 joint rebuild unconditionally requires both indexes, contradicting B1.2 and B5.1**
   - **Raised by**: codex (Finding 1). Location: `CACHES.md:402-404` (Requirement K2.3).
   - **Why it holds**: I missed this in round 1. K2.3 states: *"The full-text and vector indexes are rebuilt by one command, in one step. If either fails, neither replaces the old ones, and the query falls back (Rd3.5)"*. Under B1.2 (`CACHES.md:344`), the vector index *"is built only after B1.1 has fired"*; under B5.1 (`CACHES.md:380-381`), *"If embedding fails mid-rebuild or the model is missing, the full-text path still works."* Requiring both indexes to rebuild jointly and failing both if either fails makes full-text rebuild impossible in a full-text-only installation or when embeddings are unavailable. K2.3 must state that joint atomic rebuilding applies when both indexes are built.

3. **Part 1 "Still unresolved" asserts "For memory entries all six stay open", which is no longer true**
   - **Raised by**: claude (Finding 4), codex (Finding 11), opencode (Finding 12). Location: `CACHES.md:111-117`.
   - **Why it holds**: I missed this in round 1. Line 117 states: *"For memory entries all six stay open."* This misleads: D6 (what counts as a fired trigger) was settled by EJ selecting empirical comparisons (B1.1 and B1.2; `CACHES.md:12-14`); D5 (`INDEX.md` contents) is settled by `SOURCE_OF_TRUTH.md` K6.1 and `CACHES.md` B4.1; D1 (order of stores) is settled as proposed policy by B1.2 (`CACHES.md:344`, full-text before vector). Only D2, D3, and D4 remain open measurement questions.

4. **`INDEX.md` scan and grep-plus-open costs cite sources that do not contain them**
   - **Raised by**: claude (Finding 5), codex (Finding 13), opencode (Finding 5). Location: `CACHES.md:101-105`.
   - **Why it holds**: I missed this in round 1. Line 104 cites `SOURCE_OF_TRUTH.md` for *"an `INDEX.md` scan, under 0.01 s and minimal tokens"*, but `SOURCE_OF_TRUTH.md` contains no scan timing or token counts; the figure is opencode's unsourced estimate from D4 (`runs/20261012-caches-enhance/DECISION-RULES.md:150`). Additionally, line 102 cites `S-F13` for 226K tokens, but S-F13 explicitly states: *"Token cost to the agent is the real axis and this test does not measure it"* (`sqlite-fts.claude.md:107`), while S-F4 measured an 80-call File-System Agent across 1,144 documents rather than grep-plus-open (`sqlite-fts.claude.md:55`).

5. **"Rules for every cache" designates `INDEX.md` as the membership reference, contradicting B4.1**
   - **Raised by**: claude (Finding 12 item 1), codex (Finding 14), opencode (Finding 6). Location: `CACHES.md:152-153`.
   - **Why it holds**: Line 152 states: *"Index only active entries … the same set as `INDEX.md`"*. B4.1 was explicitly modified to establish that *"The headers are the reference, not `INDEX.md`, which is generated from them (`SOURCE_OF_TRUTH.md` K6.1)"* (`CACHES.md:373-375`). Citing `INDEX.md` as the reference suggests that a stale generated file determines cache contents.

6. **Cursor 12.5% accuracy gain is conflated with the 1,000+ files condition**
   - **Raised by**: claude (Finding 10), codex (Finding 8). Location: `CACHES.md:531`.
   - **Why it holds**: Line 531 states: *"Code, 1,000 or more files | +12.5% accuracy with vector search (Cursor)"*. In `runs/20261012-memory-caches/nodes/vector.claude.md:90-93` (V-F6), Cursor's 12.5% average higher accuracy was reported across the entire benchmark; the condition *"on large codebases with 1,000 files or more"* applied strictly to code retention increasing from 0.3% to 2.6%.

7. **Vector why 5 cites code and chunk-RAG studies as evidence on memory-style text**
   - **Raised by**: claude (Finding 11), codex (Finding 9). Location: `CACHES.md:212-213`.
   - **Why it holds**: Line 212 asserts: *"On memory-style text, the positive results found combine vectors with keyword search (`V-F6`, `V-F7`; `V-F10` is unproven)"*. In `vector.claude.md:95`, V-F6 is Cursor on code (*"code (not decisions/lessons)"*); in `:102`, V-F7 is chunk-RAG on general documentation and codebases. Neither evaluated memory-style text; only V-F10 touched agent memory, and it is unproven.

8. **"Rules for every cache" cites S-F9 alone for SHA-256 content hashing**
   - **Raised by**: codex (Finding 15). Location: `CACHES.md:144-146`.
   - **Why it holds**: Line 145 cites `S-F9` beside content hashing. In `sqlite-fts.claude.md:80`, S-F9 evaluated build time versus source mtime; S-F11 (`sqlite-fts.claude.md:89`) is the source that introduced SHA-256 content hashes. S-F11 should be cited alongside S-F9, matching K1.1 and K2.1.

9. **B1.2 references "the B1.1 question set", but Rd4.2 builds fresh question sets per comparison**
   - **Raised by**: claude (Finding 8). Location: `CACHES.md:337-339`.
   - **Why it holds**: B1.2 requires that *"every question in the B1.1 question set that full-text answers is still answered"*. Because B1.2 runs only after B1.1 has fired, referencing "the B1.1 question set" implies reusing a historical question set that may reference retired or superseded entries, whereas Rd4.2 explicitly mandates that question sets are constructed fresh when a comparison runs (`CACHES.md:456-457`).

10. **Vector 5W1H How row cites Option A, which specifies forbidden incremental re-embedding**
    - **Raised by**: claude (Finding 14). Location: `CACHES.md:227`.
    - **Why it holds**: Line 227 cites Option A from V-F18/V-F19. In `vector.claude.md:292-293`, Option A specifies: *"Rebuild = re-embed the files whose hash changed"*. This directly violates Core Requirement B3.1 (`CACHES.md:368`), which explicitly forbids incremental reuse of rows or vectors and mandates full rebuilds.

11. **Part 1 routing table relies on `INDEX.md` for metadata fields it does not carry**
    - **Raised by**: claude (Finding 15). Location: `CACHES.md:92` and `CACHES.md:94`.
    - **Why it holds**: Lines 92 and 94 specify scanning `INDEX.md` for path coverage (`covers`) and structured headers (`status`, `supersedes`, `depends_on`). Under `SOURCE_OF_TRUTH.md` K6.1 (`:276`), `INDEX.md` contains only entry id, kind, and one-line claim. Exhaustive searches for coverage, supersession, or dependencies must scan entry headers directly.

12. **Vector fallback in Part 1 routing table omits full-text search, contradicting Rd3.3**
    - **Raised by**: claude (Finding 12 item 4). Location: `CACHES.md:89`.
    - **Why it holds**: The vector row lists its fallback as `"`INDEX.md`, grep, then read"`. Because vector is built only after full-text is present, the fallback must include full-text search before grep, as accepted in Rd3.3 (`CACHES.md:442-443`).

13. **Rd3.4 cites ambiguous `(G-F5, failure mode 5)` instead of `G-F5 drift`**
    - **Raised by**: opencode (Finding 8). Location: `CACHES.md:446`.
    - **Why it holds**: Line 28 distinguishes `G-F5 drift` (drift study) from `G-F5 Serena` (Serena). Citing bare `G-F5` at line 446 is ambiguous, and failure mode 5 belongs to the drift study (`runs/20261012-memory-caches/nodes/code-graph.opencode.stdout.md:218-220`).

14. **`CACHES.md:98` cites G-F18 for whole-repo map**
    - **Raised by**: opencode (Finding 13). Location: `CACHES.md:98`.
    - **Why it holds**: Line 98 cites `G-F18` for a whole-repo map. In `code-graph.opencode.stdout.md:181`, F18 establishes tool determinism and stdout-only execution; it does not evaluate repository maps. The citation should reflect M18 with the run record's other sources (`runs/20261012-caches-enhance/DECISION-RULES.md:61`).

15. **CONTESTED status of M6 and M17 cited bare without disclosure**
    - **Raised by**: opencode (Finding 11). Location: `CACHES.md:97` and `CACHES.md:438`.
    - **Why it holds**: In `runs/20261011-project-memory-engines/RECOMMENDATION.md:35, 46`, M6 and M17 are recorded as CONTESTED. While B2 discloses M6's contested status, line 97 and Rd3.1 (`:438`) cite them without noting their status.

16. **Tokens-read claim overstates full-text performance on SEZA memory**
    - **Raised by**: codex (Finding 6). Location: `CACHES.md:518-520`.
    - **Why it holds**: Line 518 states: *"On **tokens read**, full-text wins much earlier: on SEZA-sized memory, a single broad term already floods grep's output. The B1.1 comparison measures exactly that."* This claims a full-text win at SEZA size. However, line 515 notes that on the 257-file set, the full-text proxy missed on 2 of 5 questions, resulting in *"no verdict at n=5"* (`CACHES.md:539`; `runs/20261012-caches-numbers/nodes/seza.md:337`). Because B1.1 requires fewer characters read *and no more misses*, large grep output proves reading friction, not that full-text won.

17. **W-18 and W-19 cited to claim keyword retrieval wins over loading at 100K–500K tokens**
    - **Raised by**: codex (Finding 7). Location: `CACHES.md:526` and `CACHES.md:535`.
    - **Why it holds**: Line 535 states: *"retrieval beats loading everything somewhere around 100K–500K tokens, but it is keyword retrieval that wins."* In `runs/20261012-caches-numbers/nodes/web.md:110`, W-18 evaluated oracle session selection against full history; in `:111-120`, W-19 (BEAM) evaluated RAG against long-context LLMs. Neither evaluated BM25 or keyword retrieval against dense vector embeddings. Citing them to claim keyword retrieval specifically wins combines disparate experiments into an unsupported assertion.

---

### Points I reject

1. **Reconciling historical journal misses with the active corpus in K3.1**
   - **Raised by**: codex (Finding 4). Location: `CACHES.md:411`.
   - **Why it does not hold**: Codex argues that journal notes persist while target entries may become superseded, demanding an explicit mechanism to reconcile historical targets with the active-only index. This is rejected. Rd4.2 already specifies: *"The question set for a comparison is built when the comparison runs, by an agent or by EJ, from the entries that exist then (B1.1, B1.2, K3.1)"* (`CACHES.md:456-457`). Furthermore, B1.2 defines a miss as an entry currently in `entries/` with `status: active` (`CACHES.md:333-334, 371`). Questions targeting retired entries are excluded when the set is built. Codex proposes adding unneeded procedural structure, violating the owner's rule to keep requirements intact without inventing complexity (`CLAUDE.md:80`).

2. **Rejecting the K2 freshness claim regarding SEZA stale entries**
   - **Raised by**: codex (Finding 5). Location: `CACHES.md:549`.
   - **Why it does not hold**: Codex asserts that K2 detects only index-to-file discrepancies and cannot address outdated entry text. Line 549 is explicitly labelled *my reading* and draws a direct lesson from SEZA's recorded failure: `"auto-memory index: 'vision v0.4 … RATIFIED 2026-09-26' … Memory index stale"` (`seza/runs/20261010-project-cleanup/STATUS-GRAPH.md:268`). In SEZA, the index file itself was stale relative to current documents (`PRODUCT_VISION.md` was v0.9). The text does not claim K2 edits human markdown files; it correctly emphasizes that freshness validation (K2) takes precedence over index speed.

3. **Demanding a formal ranking / top-5 definition for B1.1's `INDEX.md` arm**
   - **Raised by**: claude (Finding 9). Location: `CACHES.md:320-323`.
   - **Why it does not hold**: Claude objects that grep and `INDEX.md` scans are unranked and lack a defined ranking rule for "top 5". In unranked file scans, "top 5" has consistently denoted the first 5 matching results returned in sequential scan order, exactly as evaluated for `rg` in the benchmark (`runs/20261012-caches-routing/bench/results.md:26-28`). Mandating formal ordering specifications for linear text scans adds artificial complexity to an accepted baseline route.

4. **Importing task versus project journal distinctions from `SOURCE_OF_TRUTH.md` into Rd4.1**
   - **Raised by**: claude (Finding 13). Location: `CACHES.md:453`.
   - **Why it does not hold**: Claude argues that Rd4.1's phrase *"notes the miss in its journal/ file"* ignores task-specific journals in `work/<task-id>/journal/`. The brief explicitly governs: *"`docs/memory-system/SOURCE_OF_TRUTH.md` is a **different design**... Caches only"* (`briefs/r1-read.md:24-27`). In `CACHES.md:453`, "its journal/ file" refers generically to whatever journal file the working agent uses. Introducing the twin-journal taxonomy from a separate design violates scope boundaries.

5. **Requiring BM-9 tables to duplicate historical audit caveats**
   - **Raised by**: opencode (Finding 4). Location: `CACHES.md:263-276`.
   - **Why it does not hold**: Opencode argues that BM-9 states the 15 ms bound flatly without repeating that `git ls-files` added 1.2 ms of overhead or that the corpus moved mid-run. As codex proved and opencode acknowledged, removing `git ls-files` overhead reduces grep's runtime, leaving the <=15 ms upper bound intact. Furthermore, `CACHES.md:280-285` already discloses the repair history and caveats, while the Unresolved table explicitly records the corpus-stability and audit caveats. Duplicating these caveats inside the BM summary tables is unnecessary.

6. **Demanding that every citation of `G-F5 drift` state that it studied a code-graph tool**
   - **Raised by**: opencode (Finding 9). Location: `CACHES.md:143` and `CACHES.md:366`.
   - **Why it does not hold**: Opencode argues that `CACHES.md` must explain at each citation that G-F5 was a code-graph study. The Provenance section at `CACHES.md:28-29` already establishes that all `G-F*` findings originate from `runs/20261012-memory-caches/nodes/code-graph.opencode.stdout.md` and explicitly distinguishes `G-F5 drift`. Repeating this contextual description at every citation is redundant.

7. **Requiring `BM-*` IDs to be mapped or renamed to match `bench/results.md` headings**
   - **Raised by**: opencode (Finding 10). Location: `CACHES.md:233` and `CACHES.md:316`.
   - **Why it does not hold**: Opencode objects that `results.md` uses Category headings rather than `BM-*` labels. `CACHES.md:233` explicitly introduces the mapping: *"results in bench/results.md, ids BM-* below"*. Assigning concise local IDs to synthesized benchmark metrics is standard practice and creates no ambiguity.

8. **Trimming BM-9 Item 4 regarding test-suite execution**
   - **Raised by**: claude (Finding 7, item 4). Location: `CACHES.md:291-294`.
   - **Why it does not hold**: Claude suggests deleting Item 4 (*"No single store answers 'which tests should I run' … That is why the full suite runs before committing"*) or moving it to `docs/code-graph/`. Item 4 provides empirical context explaining why full test suites are executed in this repository during development and testing. It serves developer guidance for the test run and requires no removal.

9. **Restricting startup index size caps to instruction loaders**
   - **Raised by**: codex (Finding 10). Location: `CACHES.md:484` and `CACHES.md:487`.
   - **Why it does not hold**: Codex argues that combined caps (e.g. 32 KiB, 64 KiB) apply only when `INDEX.md` is loaded via instruction loaders. The section heading is explicitly titled *"### The index read at session start (`INDEX.md`, `MEMORY.md`), by agent type"* (`CACHES.md:479-481`) and defines limits on files loaded at session start. It does not claim subsequent file reads are governed by loader caps.

10. **Broadening the corpus gap to explicitly name SEZA memory**
    - **Raised by**: codex (Finding 17). Location: `CACHES.md:561`.
    - **Why it does not hold**: Codex suggests adding SEZA memory to the list of example corpora. The section states: *"No measurement on `project-memory/` entries. All evidence is on other corpora: source code, chat memory, enterprise documents. The short entry text, the five fields, the one-sentence claim, and the tags have not been run against either cache"* (`CACHES.md:560-562`). SEZA's memory was an unstructured legacy folder, not the structured schema specified for `project-memory/`. The gap description is accurate as written.

---

### My own points: held or withdrawn

- **Finding 1 (Fallback on missing embedding model contradicts Core Requirement Rd3.3, `CACHES.md:148-149`)**: **Held** — confirmed independently by claude (Finding 1) and codex (Finding 3); `CACHES.md:148-149` sends queries to grep, directly contradicting Rd3.3 (`CACHES.md:442-443`).
- **Finding 2 (Leftover text counts three caches and three stores for memory entries, `CACHES.md:54` and `:549`)**: **Held** — confirmed independently by claude (Finding 7), codex (Finding 16), and opencode (Finding 1); memory caches comprise two indexes (`caches-vision.md:27`).
- **Finding 3 (Provenance note asserts that "Measured here" adds a routing rule for code and docs, `CACHES.md:44-46`)**: **Held** — confirmed independently by claude (Finding 7), codex (Finding 16), and opencode (Finding 7); Part 2 moved to `docs/code-graph/CODE_GRAPH.md` and scope widening was rejected (`CACHES.md:60-61`).
- **Finding 4 (Proving absence cites linguistic negation finding V-F20 instead of V-F23, `CACHES.md:93`)**: **Held** — verified against source; `vector.claude.md:233` (V-F20) addresses bi-encoder negation failure, whereas `vector.claude.md:259` (V-F23) establishes that top-k cannot prove absence.
- **Finding 5 (Requirement K3.2 conflates vector miss triggers with full-text rerun conditions, `CACHES.md:413-414`)**: **Held** — confirmed independently by claude (Finding 3) and opencode (Finding 2); K3.2 must provide distinct rerun events for full-text (B1.1) and vector (B1.2).
- **Finding 6 ("Example numbers by case" introduction retains framing of removed INDEX.md size trigger, `CACHES.md:465-467`)**: **Held** — confirmed independently by claude (Finding 6); the startup index sizing table (`:479-506`) informs `SOURCE_OF_TRUTH.md` Rd3.1 rather than B1/K3 cache comparisons.

---

### Unresolved table

| Row | Position after reading others | Reason |
|---|---|---|
| **The BM-9 speed bound (15 ms) and the audit's `git ls-files` overhead** | **Settled for the speed bound; open as a caveat in the text; no longer relevant to cache triggers.** | Removing the ~1.2 ms subprocess overhead decreases `rg`'s mean latency from ~7.4 ms to ~6.2 ms, so the <=15 ms upper bound mathematically holds (as codex demonstrated and opencode conceded). However, disclosing that `rg` paid subprocess overhead an agent would not pay remains an unclosed benchmark caveat in BM-9 (`CACHES.md:273-276`). As claude noted, latency is no longer an operative requirement in B1.1 or K3, so the timing dispute does not affect cache triggers. |
| **Corpus snapshot stability during the benchmark build** | **Still open.** | All four readers agree that the builder's warning (`runs/20261012-caches-routing/nodes/build.opencode.stdout.md:68`: *"these numbers are a snapshot of a corpus in motion. Re-run before the tables are used"*) remains unclosed. While a later repair run was executed, the benchmark was never re-run against a verified frozen corpus snapshot. |
| **The audit's lower-severity findings** | **Still open.** | All four readers agree that the repair was never re-audited (`CACHES.md:285`). While some items are informational ("No problem found"), others (such as vector chunk deduplication returning fewer than 10 chunks) remain unaddressed in the text. |
| **Discovery versus exhaustive routes in the memory "none" rules** | **Settled in the design.** | The Part 1 routing table (`CACHES.md:86-98`) and rule (`:81-85`) explicitly route free-text and semantic discovery to FTS5/vector once triggered, while routing exact lookups, completeness, absence proofs, and metadata/why inspections to "none" (file-based). Codex's desire to distinguish candidate discovery from reading within the "Why" and structured-header rows is an unadopted refinement that does not change the settled routing. |
