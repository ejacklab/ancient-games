## Example numbers by case

The triggers in R5 and R8.2 are comparisons. The measurement decides them, so no number is fixed in advance. This
section shows **what those comparisons have come out at elsewhere**, by agent type and condition, so a reader knows
roughly where a project stands before measuring. These are examples with sources, not thresholds.

Run: `runs/20261012-caches-numbers/`. Its source ids are:
- `W-*`: web research (`nodes/web.md`);
- `OC`: opencode's research (`nodes/opencode.md`);
- `SZ`: the SEZA measurement (`nodes/seza.md`; every number with its command);
- `CX`: codex's independent second look at SEZA, by agent type (`nodes/codex.md`);
- `BM-*`, `S-F*`, `V-F*`, `G-F*`, `s3-F*`: as above.

Web quotes are model-made extracts, not byte-checked, except W-1. Numbers marked *my arithmetic* are computed from a
sourced figure.

### The index read at session start (`INDEX.md`, `MEMORY.md`), by agent type

| Agent | Window | Limit on files loaded at start | Measured effective context | Example |
|---|---|---|---|---|
| Claude Code (Claude 5.x) | 1M (W-8) | `MEMORY.md`: "first 200 lines … or the first 25KB, whichever comes first"; `CLAUDE.md`: target under 200 lines (W-1) | Opus 4.6, MRCR v2: 93% at 256K, 76% at 1M (W-14, W-15) | 25 KB binds first: about 150 lines at 167 B per line (W-1), about 107 lines at SEZA's 233 B per line (*my arithmetic*, SZ) |
| Codex (GPT-6.x) | 1.05M per the API (W-9), but this machine's Codex model cache says `context_window: 500000`, 95% effective, so about 475K (CX) | `AGENTS.md` combined up to 32 KiB (`project_doc_max_bytes`) (W-2) | GPT-5.4: 79.3% at 128K–256K, 36.6% at 512K–1M (W-15, reported) | instructions plus index under 32 KiB |
| agy (Gemini 3.1 Pro / 3.8 Flash) | 1,048,576 (W-9, CX) | 24,000 bytes per rule file, **and** a 20,000-token budget across all rules (CX, official page); 12,000 characters in other reports (W-4, conflict) | 84.9% at 128K, 26.3% at 1M (W-15, reported) | under 12,000 characters if both readings must hold (*my reading*) |
| opencode (MiniMax M3 / M2.7) | 1M / 204,800 (W-9) | no limit stated (W-6) | GAP | follow the strictest agent sharing the repo |
| dsh (DeepSeek flash / V4 pro) | 1,048,576 (CX) | a 65,536-byte budget for the instruction files it loads (CX, from its loader docs) | GAP | instructions plus index under 64 KiB |
| Qwen Code | — | warns when always-loaded context passes 15% of the window (`MEMORY_CONTEXT_WARNING_RATIO = 0.15`, CX) | — | always-loaded memory under 15% of the window |
| Cursor | — | rules "under 500 lines" (W-3) | — | — |

**Why the start load should stay small, whatever the window:**
- Half of 17 models kept satisfactory performance only up to 32K (RULER, W-10).
- 11 models fell below 50% of their baseline at 32K when the question and the answer share few words (NoLiMa, W-11).
- Focused prompts of about 300 tokens beat full ones of about 113K (W-13).
- Context files raised inference cost by over 20%, with no general success gain (W-17).
- At 500 simultaneous instructions, the best model was 68% accurate (W-16).

**Use case, SEZA (SZ, CX):**
- The start load by agent, as estimates: Claude Code 61,993 B (about 15.4K tokens, including the global `CLAUDE.md`;
  SZ measured 58,427 B without it); dsh 46,319 B (about 11.5K); Codex and agy 29,166 B each (about 7.2K) (CX). All are
  well under 15% of every window above.
- `MEMORY.md` is 52 lines and 12,108 B, within Claude's limit.
- The 52 topic files (167,257 B) would not fit in 25 KB. That is why they are an index plus files read on demand.

**When several agents share a project, the binding limit is the smallest one among them** (*my reading*).

### R5.1: full-text against `INDEX.md` plus grep

| Case | What was measured | Source |
|---|---|---|
| 1,144 docs, 1.7M tokens | the grep agent is more accurate (77.4 vs 74.7) but reads 226K tokens per question against BM25's 5.8K | W-22 |
| 3,980 docs, 8.5M tokens | accuracy crossover: BM25 70.1 vs 69.9; BM25 ahead at every larger tier | W-22, S-F4 |
| 511,959 docs, 600.8M tokens | BM25 50.5 vs the grep agent 30.7 | W-22 |
| This repo's code and docs, 490 files, 4.8 MB | full-text prints about a sixth of grep's characters before naming a right file | BM-6 |
| SEZA's memory stores, 152 md files, 1.66 MB | grep takes 4–7 ms but prints from 361 B (a narrow term) to 109,519 B, about 27K tokens (a broad term). A full-text proxy ranked the right file first on 3 of 5 questions and missed on 2 (n=5, one reader) | SZ |
| A tool result too large to read | filtering in code instead of reading: 150,000 tokens down to 2,000 | OC (Anthropic, 2025-11-04) |

**My reading:** on accuracy, grep stays competitive until millions of tokens. On **tokens read**, full-text wins much
earlier: on SEZA-sized memory, a single broad term already floods grep's output. The R5.1 comparison measures exactly
that.

### R5.2: the vector index

| Case | What was measured | Source |
|---|---|---|
| Loading about 115K tokens of history instead of retrieving | 30%–55% lower accuracy (GPT-4o, Llama 3.1) | W-18 |
| Long context against retrieval, 100K–1M tokens | retrieval better for 3 of 4 models at 100K, and for all 4 from 500K | W-19 |
| Vendor guidance | under about 200,000 tokens, the whole base can go in the prompt | V-F8 (2024) |
| Dense against BM25, 1,144–511,959 docs | dense lowest at all 9 tiers | W-22 |
| Enterprise corpus, 500K docs | vector 51.4 vs BM25 68.8 correctness | V-F4 |
| Code, 1,000 or more files | +12.5% accuracy with vector search (Cursor), but 15 days later Cursor shipped Instant Grep and says it "does not store embeddings of your codebase for search" | V-F6, OC |
| A memory growing 10× (1M to 10M tokens) | Mem0 64.1 to 48.6 (vendor's figures) | W-20 |
| SEZA | no recorded misses, so the comparison has nothing to run on | SZ |

**My reading:** retrieval beats loading everything somewhere around 100K–500K tokens, but it is keyword retrieval
that wins. Vectors earn a place only on recorded meaning-misses, which is what R5.2 tests.

### R5.3: the code graph

| Case | What was measured | Source |
|---|---|---|
| Gin, about 110 files | cost about even with or without the graph | G-F7, W-25 |
| Alamofire, about 110 files | 57% cheaper | W-25 |
| Excalidraw, about 640 files | 78% cheaper, 84% fewer tokens | G-F7 |
| Django, about 3k files | 13% cheaper | G-F7 |
| VS Code, about 11k files | 71% cheaper, but 67k vs 18k tokens left resident after the session | G-F7, G-F7b |
| Hidden-dependency tasks | 99.4% vs 76.2% task completion | s3-F16 |
| 43 files (Serena, vendor self-evaluation) | cross-file rename 9 calls down to 1, but 4.5× worse on a one-line edit | OC |
| This repo | the graph names a caller in 33–46 characters | BM-3 |
| SEZA | `.ctxgraph` (1.1 MB) built 2026-07-28, `usage_count` 0, queried by no code: the case R5.3 exists to prevent | SZ |

**My reading:** the payoff follows how far a question reaches across files, not the file count. Two repos of 110
files went from no saving to 57%.

### R8.2: rebuild cost

| Store | Measured | Source |
|---|---|---|
| Full-text | 0.169 s for 490 files (index 9.5 MB, about 2× the source); 0.53 s for 10,000 entries; 2.57 s for 50,000; SEZA 0.004 s for 55 files, 0.54 s for 2,013 md files (34 MB) | BM-9, S-F13, SZ |
| Vector | 0.936 s for 490 files with model2vec; embedding speed 81,018 samples/s for model2vec against 274 for a MiniLM fine-tune; sqlite-vec builds 1M × 128 dims in about 4 s, embedding excluded | BM-9, OC, W-27 |
| Code graph | 0.94 s for 126 `.py` files; codegraph about 100 s for about 27k files | G-F12, W-25 |

**My reading:** at every size measured here, a rebuild takes under a second, except for embedding with a heavy model.
R8.2 bites only when the embedding model is slow.

### SEZA today, trigger by trigger (SZ, the researcher's reading)
- **R5.1:** no verdict at n=5.
- **R5.2:** not met.
- **R5.3:** cannot be evaluated; the graph that exists is unused.
- **R8.2:** cheap.

SEZA's own `project_memory search` was used 42 times in 15 sessions, with none after 2026-09-24.

**What actually went wrong in SEZA was not search** (CX):
- Its start index carried outdated state: the cleanup audit records *"Memory index stale"*
  (`seza/runs/20261010-project-cleanup/STATUS-GRAPH.md:268`).
- Its derived graph was missing when it was asked for: *"graph is missing; run sync or rebuild"*.

**My reading:** a faster cache would have returned the same stale entries. R3 (stale never answers) and the drift
check matter more here than any of the three stores.

