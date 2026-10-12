### Verdict
REPAIR — The changes since review are conceptually sound, but the text contains a direct requirement contradiction on fallback behaviour, leftover references counting three caches/stores instead of two, an inaccurate provenance description of moved text, a mis-cited absence finding, and an unaligned rerun trigger in K3.2.

### Findings

1. **Fallback on missing embedding model contradicts Core Requirement Rd3.3**
   - **Location**: `CACHES.md:148-149`
   - **Quoted text**: `"If the cache file or SQLite's FTS5 is missing, the tool answers with grep and says so in every answer (Rd3.2) (S-F9); the same for a missing embedding model (my reading, extending S-F9)."`
   - **Why it misleads or is wrong**: Stating that a missing embedding model does "the same" specifies that it falls back directly to grep. This directly contradicts requirement Rd3.3, which requires a missing embedding model to fall back to full-text search first if available, and only to grep if full-text is absent.
   - **Source line that shows it (quoted)**: `CACHES.md:442-443`: `"- **Rd3.3** A missing embedding model falls back to full-text if it is there, and to grep if not; the answer says so. *(my reading, extending S-F9; *proposed*: full-text before grep.)* (was R4.2)"`
   - **Severity**: High
   - **Fix**: Update line 148–149 to state that a missing embedding model falls back to full-text search first if present, and to grep if not, citing Rd3.3.

2. **Leftover text counts three caches and three stores for memory entries**
   - **Location**: `CACHES.md:54` and `CACHES.md:549`
   - **Quoted text**: Line 54: `"None of the three caches is needed today **for memory entries**."` and Line 549: `"K2 (stale never answers) matters more here than any of the three stores."`
   - **Why it misleads or is wrong**: The code graph was moved out to its own project (`docs/code-graph/CODE_GRAPH.md`). The document title (`# Memory Caches: SQLite Full-Text and Vector`), the vision statement, and line 298–299 establish that there are only two memory caches (full-text and vector). Counting "three caches" and "three stores" for memory entries are unedited leftovers from before the code graph was separated.
   - **Source line that shows it (quoted)**: `runs/20261013-caches-design-read/inputs/caches-vision.md:27`: `"The caches are two optional indexes over the project's markdown memory — full-text search and vector search."` and `CACHES.md:298-299`: `"They serve the vision... and cover the two memory caches, full-text and vector; the code graph is its own project (docs/code-graph/)."`
   - **Severity**: Medium
   - **Fix**: Change `"None of the three caches"` to `"Neither cache"` at line 54, and change `"any of the three stores"` to `"either store"` at line 549.

3. **Provenance note asserts that "Measured here" adds a routing rule for code and docs**
   - **Location**: `CACHES.md:44-46`
   - **Quoted text**: `"> **Measured enhancement, 2026-10-12** (runs/20261012-caches-routing/): the section **Measured here: development and testing** adds measurements on this repo and a routing rule for code and docs."`
   - **Why it misleads or is wrong**: Section "Measured here: development and testing" contains only local measurements (BM-1 to BM-9). The proposed routing rule for code and docs was Part 2, which was moved out to `docs/code-graph/CODE_GRAPH.md`.
   - **Source line that shows it (quoted)**: `CACHES.md:134-136`: `"### Part 2 — code and docs\n\nMoved to the code-graph project, docs/code-graph/CODE_GRAPH.md (EJ, 2026-10-12: \"others can accept and apply\"). It routed questions about this repo's code and docs, outside the caches vision; its evidence stays below in Measured here: development and testing."`
   - **Severity**: Medium
   - **Fix**: Update line 45 to state that "Measured here" adds measurements on this repo, noting that the routing rule for code and docs moved to `docs/code-graph/CODE_GRAPH.md`.

4. **Proving absence cites linguistic negation finding V-F20 instead of V-F23**
   - **Location**: `CACHES.md:93`
   - **Quoted text**: `"| Proving absence (\"have we never recorded…\") | none — no hit is not proof | exhaustive search, then read | V-F20 |"`
   - **Why it misleads or is wrong**: V-F20 covers bi-encoder failure on linguistic negation (the NevIR benchmark, e.g. "do not use X" vs "use X"). Proving absence ("have we never recorded...") because ranked top-k retrieval cannot establish non-existence is documented under V-F23 (and V-F1), not V-F20.
   - **Source line that shows it (quoted)**: `runs/20261012-memory-caches/nodes/vector.claude.md:233`: `"**F20 (CONFIRMED) Negation is a documented weakness of bi-encoders.** NevIR (arXiv 2305.07614, 2023, EACL 2024)..."` versus line 259: `"**F23 (CONFIRMED) Top-k cannot enumerate or prove absence.** F1 quote: it \"cannot enumerate a complete set, establish an absence, or traverse relationships\". Applies to any ranked top-k, vector or keyword (F1's notes-search column)."`
   - **Severity**: Low
   - **Fix**: Change citation `V-F20` to `V-F23` (or `V-F1, V-F23`) at line 93.

5. **Requirement K3.2 conflates vector miss triggers with full-text rerun conditions**
   - **Location**: `CACHES.md:413-414` (Requirement K3.2)
   - **Quoted text**: `"- **K3.2** The comparison is rerun when an agent notes a miss, and when EJ asks; the agent that runs it writes the result to runs/<run-id>/ (*proposed*, the same as B1.2)."`
   - **Why it misleads or is wrong**: K3 applies to any built cache. However, a "miss" is defined in B1.2 and Rd4.1 as an entry where full-text (along with INDEX.md and grep) missed. While noting a miss triggers the vector evaluation (B1.2), it does not trigger a rerun of full-text's comparison against grep; full-text's comparison trigger in B1.1 is when an agent notes in its journal that INDEX.md plus grep required reading through many hits, or when EJ asks.
   - **Source line that shows it (quoted)**: `CACHES.md:327-328`: `"It runs when EJ asks, or when an agent notes in its journal that INDEX.md plus grep made it read through many hits to reach an entry..."`
   - **Severity**: Low
   - **Fix**: Update K3.2 to specify that the rerun is triggered for full-text when an agent notes excessive grep hits or EJ asks, and for vector when an agent notes a miss or EJ asks.

6. **"Example numbers by case" introduction retains framing of removed INDEX.md size trigger**
   - **Location**: `CACHES.md:465-467`
   - **Quoted text**: `"The triggers in B1 and K3 are comparisons. The measurement decides them, so no number is fixed in advance. This section shows **what those comparisons have come out at elsewhere**, by agent type and condition, so a reader knows roughly where a project stands before measuring."`
   - **Why it misleads or is wrong**: The first subsection immediately following this introduction is `The index read at session start (INDEX.md, MEMORY.md), by agent type` (lines 479–506), which documents agent context limits and start-file sizes. This table was originally the evidence for the removed `INDEX.md` size trigger for full-text. Because the full-text trigger was changed to the B1.1 comparison, this table does not measure a B1 or K3 comparison; it informs the session-start load rule (Rd1 / SOURCE_OF_TRUTH Rd3).
   - **Source line that shows it (quoted)**: `CACHES.md:13-14`: `"EJ chose the B1.1 comparison as the full-text trigger, replacing \"INDEX.md can no longer list every active entry\" in the rule, the routing table, the five whys and the 5W1H (EJ: \"the comparison for full-text\")"`
   - **Severity**: Low
   - **Fix**: Revise lines 465–467 to clarify that the section provides quantitative examples for the B1 comparisons as well as the session-start file load constraints governing Rd1.

---

### Unresolved table

- **The BM-9 speed bound and the audit's `git ls-files` overhead**: Still open as a benchmark dispute (no clean rerun without overhead was executed), but no longer relevant to triggering memory caches because B1.1 triggers on characters read rather than latency.
- **Corpus snapshot stability during the benchmark build**: Still open (the benchmark was not re-executed against a frozen corpus snapshot, and the builder's warning remains unclosed).
- **The audit's lower-severity findings**: Still open (the lower-severity harness audit findings were never re-audited or addressed by code changes).
- **Discovery versus exhaustive routes in the memory "none" rules**: Settled (the Part 1 routing table at lines 86–98 explicitly routes discovery questions to FTS5/vector once triggered, and exhaustive enumeration, absence proofs, and exact lookups to "none"/files).

---

### What holds

- **Status and Provenance (`CACHES.md:1-51`)**: Accurately tracks document lineage, merge history, review corrections, and the three research source nodes.
- **When to use which store — Part 1 (`CACHES.md:67-132`)**: Routing rules and table for memory entries are well-grounded; files remain authoritative while caches are optional.
- **Part 2 pointer (`CACHES.md:132-136`)**: Correctly records the relocation of code and docs routing to `docs/code-graph/CODE_GRAPH.md`.
- **Rules for every cache (`CACHES.md:138-154`)**: Mandatory full rebuilds, atomic replacement via temp files, hash-based staleness checks, and active-only entries hold.
- **SQLite full-text index (`CACHES.md:155-190`)**: Five whys and 5W1H clearly justify FTS5 for ranked discovery with snippets (S-F1, S-F4) using stdlib SQLite and `unicode61`.
- **Vector index (`CACHES.md:191-228`)**: Five whys and 5W1H accurately reflect the empirical weakness of standalone vectors and correctly constrain vectors to a secondary hybrid role on recorded misses.
- **Measured here: development and testing (`CACHES.md:229-295`)**: Benchmark figures (BM-1 to BM-9) are accurately reported from `results.md` with audit biases and formatting limitations clearly disclosed.
- **Core requirements: Build (`CACHES.md:306-383`, B1–B5)**: Empirical trigger comparisons, file derivation, no incremental patching, active-only indexing, and zero model calls on rebuild (except embedding) are sound.
- **Core requirements: Keep (`CACHES.md:384-419`, K1–K3)**: Content hashing, serialization of rebuilds, single-step dual-index updates, and empirical trigger re-evaluations are sound.
- **Core requirements: Read (`CACHES.md:420-462`, Rd1–Rd4)**: Prohibition of startup cache reads, entry provenance attribution, graceful degradation, and journaled miss tracking are sound and consistent.
- **Example numbers by case (`CACHES.md:463-550`)**: Empirically sourced scaling baselines (W-22, S-F4) and historical SEZA operational data are accurate.
- **What this changes elsewhere (`CACHES.md:552-555`)**: Correctly establishes that `SOURCE_OF_TRUTH.md` keeps `.cache/` unchanged.
- **Not known (`CACHES.md:556-567`)**: Accurately details research boundaries, lack of existing `project-memory/` corpus, extract limitations, and voided trap questions.

---

### Not checked

- External web pages, papers, and repository URLs cited in the research nodes (read via saved copies and researcher extracts).
- Benchmark raw execution logs and timing runs in `runs/20261012-caches-routing/bench/` (accepted as reported in `results.md`).
- Primary source documents for SEZA cleanup (`seza/runs/20261010-project-cleanup/STATUS-GRAPH.md`) and web citations W-1 through W-22.
- The external code-graph project document `docs/code-graph/CODE_GRAPH.md` (explicitly out of scope).
