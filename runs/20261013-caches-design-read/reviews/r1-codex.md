### Verdict

REPAIR — my reading, codex: the main changes follow EJ’s decisions, but dependent wording, evidence claims and unresolved-status statements still mislead.

### Findings

1. **Location: K2.3, `CACHES.md:402`. Severity: high.**

   **Quoted text:** “The full-text and vector indexes are rebuilt by one command, in one step. If either fails, neither replaces the old ones”.

   **Why it misleads — my reading:** This unconditionally requires both indexes even when only full-text has been approved. It can make a full-text rebuild depend on a vector index or embedding model that must not yet exist.

   **Source line — quoted:** B1.2, `CACHES.md:344`: “it is built only after B1.1 has fired”; B5.1, `CACHES.md:381`: “the full-text path still works.”

   **Fix:** Apply the joint rebuild and joint publication rule when both indexes are built. State that a full-text-only installation rebuilds full-text alone.

2. **Location: Rd4.1, `CACHES.md:454`. Severity: medium.**

   **Quoted text:** “Every other question goes unrecorded”.

   **Why it misleads — my reading:** B1.1 also uses a journal note about a successful search that required reading many hits. That question is not necessarily a miss, so the blanket prohibition conflicts with the new full-text comparison event.

   **Source line — quoted:** B1.1, `CACHES.md:327`: “when an agent notes in its journal that `INDEX.md` plus grep made it read through many hits to reach an entry”.

   **Fix:** Say ordinary searches need no log, while preserving the specific B1.1 reading-friction notes alongside Rd4.1 miss notes.

3. **Location: `CACHES.md:149`, Rules for every cache. Severity: medium.**

   **Quoted text:** “the same for a missing embedding model”.

   **Why it misleads — my reading:** The preceding sentence sends the query to grep. The accepted Rd3.3 now sends it to available full-text first.

   **Source line — quoted:** Rd3.3, `CACHES.md:442`: “A missing embedding model falls back to full-text if it is there, and to grep if not; the answer says so.”

   **Fix:** Copy that fallback order into the summary rule, including disclosure of the route used.

4. **Location: K3.1 and Rd4.1, `CACHES.md:411`. Severity: medium.**

   **Quoted text:** “for the vector index, on the noted misses”.

   **Why it misleads — my reading:** Journal notes persist, but their target entries can subsequently become superseded or retired. The design does not say how those historical targets participate in a comparison against today’s active-only index. A formerly valid target can become deliberately unsearchable, then appear to demonstrate that the cache stopped paying.

   **Source line — quoted:** B4.1, `CACHES.md:371`: “every file in `entries/` whose own header says `status: active`, and nothing else”. Rd4.2, `CACHES.md:457`: questions are written “from the entries that exist then”.

   **Fix:** State how journal misses are reconciled with the comparison’s current active corpus. Preserve the historical notes, but distinguish an ineligible old target from a retrieval failure.

5. **Location: `CACHES.md:549`, Example numbers by case. Severity: medium.**

   **Quoted text:** “K2 (stale never answers) matters more here than any of the three stores.”

   **Why it misleads — my reading:** This connects stale memory content to cache freshness. K2 detects disagreement between an index and its entry files; it cannot detect an outdated statement faithfully indexed from an unchanged file. The missing projection is instead relevant to Rd3.

   **Source lines — quoted:** K2.1, `CACHES.md:395`: “compares the recorded content hash with the entry files”. CX, `runs/20261012-caches-numbers/nodes/codex.md:341`: outdated information remains “unless memory maintenance and source checking addressed it.”

   **Fix:** Explain that stale statements require checking the source content, while an unavailable projection motivates fallback. Keep K2’s claim limited to agreement with the files.

6. **Location: `CACHES.md:518`, Example numbers by case. Severity: medium.**

   **Quoted text:** “On **tokens read**, full-text wins much earlier: on SEZA-sized memory, a single broad term already floods grep’s output. The B1.1 comparison measures exactly that.”

   **Why it misleads — my reading:** Large grep output establishes a reason to compare routes, not a full-text win. The SEZA measurement did not measure the paired reading path and found full-text misses. B1.1 also requires no more misses.

   **Source lines — quoted:** SZ, `runs/20261012-caches-numbers/nodes/seza.md:337`: “n=5, no verdict.” Its `:349` says it recorded “bytes printed and rank, not the full reading path of an agent”.

   **Fix:** Describe broad output as possible reading friction. Leave the winner unmeasured until the paired B1.1 comparison establishes both reading savings and misses.

7. **Location: `CACHES.md:526` and `:535`, Example numbers by case. Severity: medium.**

   **Quoted text:** “Loading about 115K tokens of history instead of retrieving”; “it is keyword retrieval that wins.”

   **Why it misleads — my reading:** W-18 compares full history with oracle-selected relevant sessions, not with an implemented retrieval route. W-19 reports RAG against vanilla long context; the opened report does not establish that its result is specifically a keyword-retrieval win. The conclusion combines different experiments into a stronger claim.

   **Source lines — quoted:** W-18, `runs/20261012-caches-numbers/nodes/web.md:110`: “oracle (only the right sessions) against S (everything)”. W-19, `:111`: “‘Vanilla’ (long context) / RAG”.

   **Fix:** Label W-18 as oracle context selection and W-19 as RAG versus long context. Keep the BM25-versus-dense findings separate.

8. **Location: `CACHES.md:531`, Example numbers by case. Severity: medium.**

   **Quoted text:** “Code, 1,000 or more files | +12.5% accuracy with vector search”.

   **Why it misleads — my reading:** The file-count condition belongs to Cursor’s code-retention result, not its average question-answering accuracy result.

   **Source line — quoted:** V-F6, `runs/20261012-memory-caches/nodes/vector.claude.md:93`: “agent code retention increases by 0.3% … This effect increases to 2.6% on large codebases with 1,000 files or more”.

   **Fix:** Present the average accuracy gain separately from the retention gain and its file-count condition.

9. **Location: `CACHES.md:212`, Vector index, fifth why. Severity: medium.**

   **Quoted text:** “On memory-style text, the positive results found combine vectors with keyword search (`V-F6`, `V-F7`”.

   **Why it misleads — my reading:** Those findings support hybrid retrieval in other settings. They do not establish the stated result on memory-style text.

   **Source lines — quoted:** V-F6, `vector.claude.md:95`: “code (not decisions/lessons)”. V-F7, `:102`: “a 2024 chunk-RAG test with API embeddings”.

   **Fix:** Name the actual corpora and describe hybrid-only as this design’s proposed policy, supported by evidence from other settings.

10. **Location: `CACHES.md:484` and `:487`, startup examples. Severity: medium.**

    **Quoted text:** “instructions plus index under 32 KiB”; “instructions plus index under 64 KiB”.

    **Why it misleads — my reading:** These examples make instruction-loader budgets appear to govern every subsequent index read. Their applicability depends on whether the index is included in the instruction chain.

    **Source line — quoted:** CX, `runs/20261012-caches-numbers/nodes/codex.md:444`: “An ordinary subsequent file read consumes model context but is not thereby governed by the same loader cap.”

    **Fix:** State that the combined caps apply when the index is loaded through those instruction loaders. Distinguish a later file read from instruction discovery.

11. **Location: `CACHES.md:111` and `:117`, When to use which store. Severity: medium.**

    **Quoted text:** “Still unresolved”; “For memory entries all six stay open.”

    **Why it misleads — my reading:** The run record’s historical disagreements are preserved correctly, but this sentence presents every disagreement as a current design question. EJ has now selected observable comparisons, full-text before hybrid under the stated policy, and decision recording. Actual benefits and costs remain unmeasured.

    **Source lines — quoted:** B1.1, `CACHES.md:323`: “The comparison decides; no fixed size is set in advance”. B1.2, `:344`: “it is built only after B1.1 has fired”.

    **Fix:** Separate historical engine disagreements from current open evidence gaps. Mark the trigger-policy disagreement as settled by B1 and identify the remaining measurement questions individually.

12. **Location: `CACHES.md:240`, Measured here. Severity: medium.**

    **Quoted text:** “Rebuilding from scratch gave the same answers on all 180 question-route pairs.”

    **Why it misleads — my reading:** This correctly reports determinism, but the section omits the unresolved corpus-stability warning. Equal rebuild answers do not establish that the benchmark’s routes and gold answers were evaluated against one stable snapshot. The warning appears only much later in the unresolved table.

    **Source lines — quoted:** The builder, `runs/20261012-caches-routing/nodes/build.opencode.stdout.md:68`: “these numbers are a snapshot of a corpus in motion. Re-run before the tables are used.” The run recorder, `state.md:59`, records a later run “on the repaired harness”.

    **Fix:** Carry the unclosed snapshot warning beside the benchmark’s other limitations. Acknowledge the later rerun without claiming it proved snapshot stability.

13. **Location: `CACHES.md:104`, Costs. Severity: medium.**

    **Quoted text:** “an `INDEX.md` scan, under 0.01 s and minimal tokens (`SOURCE_OF_TRUTH.md`)”.

    **Why it misleads — my reading:** This sits under a “Measured” introduction, but the cited design supplies no scan timing. The number is an engine’s unsupported figure, and the original run explicitly preserved that disagreement.

    **Source line — quoted:** `runs/20261012-caches-enhance/DECISION-RULES.md:150`: “opencode: **<0.01 s** scan … codex: **time GAP and tokens GAP**”.

    **Fix:** Remove the timing or attribute it as an unmeasured estimate. Do not cite the source-of-truth design as a measurement.

14. **Location: `CACHES.md:152`, Rules for every cache. Severity: low.**

    **Quoted text:** “the same set as `INDEX.md`”.

    **Why it misleads — my reading:** As an implementation rule, this still suggests using the generated index to select cache membership. B4 was changed specifically to make entry headers authoritative. A stale generated index must not determine the cache’s membership.

    **Source line — quoted:** B4.1, `CACHES.md:373`: “The headers are the reference, not `INDEX.md`, which is generated from them”.

    **Fix:** Say membership is selected from active entry headers. Equality with a correctly generated `INDEX.md` is a consequence.

15. **Location: `CACHES.md:145`, Rules for every cache. Severity: low.**

    **Quoted text:** “compare the recorded content hash of the sources with the index … (`S-F9`”.

    **Why it misleads — my reading:** The core requirements now distinguish the hash source from the rebuild-before-answering source, but this summary still cites only S-F9 beside the hash procedure.

    **Source lines — quoted:** S-F9, `sqlite-fts.claude.md:80`: “compares the index build time with the newest source mtime”. S-F11, `:89`: “Change detection: SHA-256 on files and chunks.”

    **Fix:** Cite S-F11 for hashing and S-F9 for rebuilding before answering and temporary-file publication, as K1/K2 already do.

16. **Location: `CACHES.md:45`, `:54` and `:550`. Severity: low.**

    **Quoted text:** “Its conflict with the vision for code and docs is left to EJ”; “None of the three caches”; “any of the three stores”.

    **Why it misleads — my reading:** The scope conflict has been decided, and the live caches design contains two caches. Historical three-store benchmark descriptions remain appropriate; these current summary statements do not.

    **Source lines — quoted:** `CACHES.md:61`: proposals to widen the vision “were not adopted”. The snapshot vision, `caches-vision.md:27`: “two optional indexes”.

    **Fix:** Update the summary counts to two and mark the code-and-docs scope decision settled. Retain three-store wording only when describing historical research or benchmark evidence.

17. **Location: `CACHES.md:561`, Not known. Severity: low.**

    **Quoted text:** “All evidence is on other corpora: source code, chat memory, enterprise documents.”

    **Why it misleads — my reading:** The listed evidence now includes SEZA markdown memory and decision records. The genuine remaining gap is measurement on the active-entry corpus specified by this design.

    **Source line — quoted:** SZ, `runs/20261012-caches-numbers/nodes/seza.md:245`: “five questions taken from SEZA memory entries or docs”.

    **Fix:** Include SEZA memory among the example corpora. State the narrower gap: neither accepted comparison has been established on this design’s active `entries/` corpus.

### Unresolved table

- **BM-9 speed bound and `git ls-files` overhead — settled for the recorded bound:** removing overhead cannot increase the recorded maximum; the comparative timing bias remains a disclosed caveat, not evidence that the 15 ms observation is false.
- **Corpus snapshot stability — still open:** a repaired-harness rerun is recorded, but the opened evidence does not close the builder’s stable-snapshot warning.
- **Audit’s lower-severity findings — still open in part:** the repair was not re-audited; some items affect character output or presentation, while the “No problem found” item is already settled and must not be counted as a defect.
- **Discovery versus exhaustive memory routes — still open:** the completeness and absence rows correctly require exhaustive routes, but the structured-header and “why” rows still say “none” without distinguishing finding a candidate from reading or exhaustively enumerating authoritative entries.

### What holds

- **Vision:** two optional, derived memory indexes; EJ decides whether to build after a comparison passes.
- **Changes since review:** replacing the full question log with miss notes and comparison-time question sets is sound in principle; the dependent wording exceptions are identified above.
- **The answer first:** memory-only scope and absence of a demonstrated present need hold; the code-and-docs proposals were not adopted.
- **When to use which store, Part 1:** the B1.1 comparison replaces the size trigger; literal lookup, completeness and proof of absence retain appropriate file routes.
- **Part 2 and code-graph removal:** the operational sections moved out; historical graph evidence need not be removed merely because its subject is outside the caches scope.
- **Rules for every cache:** full rebuild, read-only opening, source freshness and active-only membership hold, subject to the summary corrections above.
- **SQLite full-text index:** the revised trigger, EJ’s build decision, one row per entry, default tokenizer and removal of stored `status` are consistent.
- **Vector index:** meaning-miss comparison, full-text non-regression, model identity and the explicitly proposed hybrid policy hold.
- **Measured here:** BM-1–BM-6 agree with the supplied results; BM-7 agrees with the runtime-recall artifact; proxy limitations and lack of an end-to-end agent trial are disclosed.
- **Core requirements:** B4 consistently removes stored `status` from both schemas while retaining header filtering and `covers`; decision records and trial-index placement hold.
- **K3:** dropping rebuild cost is consistently reflected in its operative clauses and removal of its example table; benchmark rebuild timings can remain as historical measurements.
- **Example numbers:** the scaling table, synthetic timings and SEZA’s “no verdict” preserve useful evidence when kept separate from adoption conclusions.
- **What this changes elsewhere:** retaining the existing optional `.cache/` placement is consistent; no change to `SOURCE_OF_TRUTH.md` is proposed.
- **Not known:** quote-verification limits, missing measurements on the designed corpus and the void planted-tool check remain appropriate caveats.
- **Unresolved after review:** keeping attributed historical positions is sound, provided their current dispositions are made clear.

### Not checked

- Original external papers, vendor pages and saved raw web copies were not independently reopened; citation checks here compare the design with its local research reports.
- Additional number-research reports were inspected at relevant passages, not all read in full.
- The benchmark implementation, repair correctness, actual SEZA files and current installed-tool behavior were not independently verified.
- No benchmark, rebuild or test suite was run. The named checks were written by the recorded researchers and auditors; this review checks documentary consistency, not cache performance.
- No other reader’s work from this round was opened. No files were changed.
