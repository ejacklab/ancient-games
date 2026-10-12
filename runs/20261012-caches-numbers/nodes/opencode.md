I'll start by reading the existing research in the repo so I cite by id instead of redoing work.
Now the web research. Starting with slice 2 (code-graph tools):
# Caches-numbers slice: search vs grep by size, code-graph pay-off, rebuild cost

Engine: `opencode` (`MiniMax-M3.1-Flash-Preview`), 2026-10-12. Read-only; no file was changed, and I ran no new benchmark (see *Not checked*).

**How sources were read.** WebFetch returns a model-written extract of the page, not raw HTML — the same caveat the earlier nodes recorded for their own quotes. So **CONFIRMED** here means "I opened the source and the extract quoted the page's wording", not byte-checked. **REPORTED** = a secondary source or a vendor's own self-evaluation. **GAP** = looked, not found. Arithmetic I did on a measured figure is marked *arithmetic* and is never presented as a source's claim.

**Already known, cited by id, not redone:** `S-F4` (BM25-vs-grep-agent crossover), `S-F5`, `S-F13`, `V-F3`, `V-F4`, `V-F5`, `V-F6`, `V-F7`, `V-F8`, `V-F11`, `G-F7`, `G-F7a`, `G-F7b`, `G-F12`, `G-F18`, `s3-F16`, `BM-1…BM-9`.

---

## Slice 1 — when does an agent beat grep with full-text, vector or hybrid, by corpus size

### N1 — CONFIRMED (by id). The one size-ordered crossover in the record is 10M tokens, and it is *above* our entry sizes.
`S-F4`, arXiv 2607.26497v3 (v3 2026-07-31), a general RAG corpus, not code and not memory entries:
> "Around 10 million corpus tokens, BM25 overtakes it and leads at every larger shared tier"

and at the smallest tier (1,144 documents / 1.7M corpus tokens) BM25 used **5.8K tokens per question against 226K** for the grep-and-read agent — but the agent **led at the smallest shared tiers**. So the crossover is a *floor below which grep wins*, not a threshold we are near. `S-F5` already converts this to ≈37,000 entries; I add nothing to that arithmetic.

### N2 — CONFIRMED, NEW, and the most useful thing I found: the only file-count threshold in the record was withdrawn by its own vendor 15 days later.
- `V-F6` (cited, cursor.com/blog/semsearch, 2025-11-06): semantic search *"significantly improves agent performance, especially over large codebases"*; *"This effect increases to 2.6% on large codebases with 1,000 files or more"*; *"the combination of these two leads to the best outcomes."*
- **NEW**, cursor changelog **2.1, Nov 21 2025** (opened today): *"Instant Grep (Beta) — All grep commands run by the agent are now instant."*
- **NEW**, cursor.com/docs/context/codebase-indexing (undated page, opened today): *"Cursor ships with **Instant Grep**, a custom search engine that outperforms `ripgrep` on large codebases."* and *"Cursor does not upload file paths or code to build a search index, and it **does not store embeddings of your codebase for search**."*

Read together: the single published corpus-size number favouring semantic search over grep (1,000 files) came from a feature the same vendor has since replaced with an **indexed lexical search**, with no correctness number published for the replacement ("outperforms ripgrep on large codebases" is unquantified). This is an example value for R5.2, and it is a *vendor's reversal*, not a study.

### N3 — CONFIRMED, NEW. Anthropic's own architecture note says the hybrid is index-up-front plus grep-just-in-time, and names the price.
anthropic.com/engineering/effective-context-engineering-for-ai-agents, published **Sep 29 2025**:
> "Claude Code is an agent that employs this hybrid model: [CLAUDE.md] files are naively dropped into context up front, while primitives like glob and grep allow it to navigate its environment and retrieve files just-in-time, **effectively bypassing the issues of stale indexing and complex syntax trees**."

> "Of course, there's a trade-off: **runtime exploration is slower than retrieving pre-computed data.**"

No number. It is a design statement from the vendor of the agent the record's studies measure (Claude Code appears in `V-F3` and `s3-F16`), and it is the closest published statement of the R5.1/R5.2 ordering rule: a small always-loaded index, grep for the rest.

### N4 — CONFIRMED, NEW. The axis BM-6 actually measures ("characters printed") has a vendor number for what printing everything costs.
anthropic.com/engineering/code-execution-with-mcp, published **Nov 04 2025**:
> "This reduces the token usage from 150,000 tokens to 2,000 tokens—a time and cost saving of 98.7%."

Context: this is about tool definitions/results, not search. It matters here because it is the largest published effect size for *not* printing a result set into context — the same lever `BM-6` pulls (grep 4,304 mean output characters vs full-text 1,817, `BM-6`). It is evidence for the proxy, not for a crossover.

### N5 — CONFIRMED, NEW. The only published *size cap on a memory index* anywhere is a line-per-memory file, and over the cap the documented behaviour is read-on-demand with ordinary file tools — not a vector search.
docs.claude.com/en/docs/claude-code/memory (opened today; page undated, describes Claude Code ≥ v2.1.2xx):
> "MEMORY.md           # Index, one line per memory, loaded into every session"

> "The first 200 lines of `MEMORY.md`, or the first 25KB, whichever comes first, are loaded at the start of every conversation. Content beyond that threshold is not loaded at session start."

> "Claude Code doesn't load topic files such as `user_role.md` or `feedback_testing.md` at startup. Claude reads them on demand using its standard file tools when it needs the information."

> "Claude Code measures the file against the 200-line and 25KB read limits. If the file is near a limit, Claude Code reminds Claude to shorten it: **keep one line per entry, move detail into topic files**, and merge or drop stale entries."

and, for the always-loaded project file: *"target under 200 lines per CLAUDE.md file"*; *"Claude Code loads a CLAUDE.md file of up to 4 MiB in full and skips a larger file."*

Why this is the most useful number I found for `INDEX.md`: it is a shipping agent whose memory index has the same shape as ours (one line per entry, detail in separate files), it caps that index at **200 lines / 25KB**, and its documented overflow path is *grep and read*, not semantic retrieval. At one line per active entry, 200 lines is about 200 entries — roughly half of the400–650 entries `V-F12` derives from Anthropic's 200,000-token "just put it in the prompt" bound (`V-F8`).

### N6 — By id, unchanged, and it is why no crossover exists for our size.
`V-F3` (arXiv 2605.15184, LongMemEval-S, 116 questions, four harnesses incl. Claude Code): *"With inline delivery, lexical search is uniformly stronger than dense retrieval: inline grep exceeds inline vector for every harness-model pair."*, with the exception *"programmatic vector exceeds programmatic grep on five of ten harness-model pairs."* `V-F4` (500,000 documents, EnterpriseRAG-Bench): BM25 correctness 68.8 / vector 51.4 / bash agent 60.6. `V-F5`: dense beats BM25 for issue localization in SWE-style repos, and *"Naive GrepRAG achieves performance comparable to sophisticated graph-based baselines."*

**Reading (mine, not a source's):** the record now holds three independent vendor/harness positions pointing the same way — grep or index-and-grep at these sizes, hybrid only as an addition, vectors never alone (`V-F3`, `V-F4`, `N2`) — and one outlier favouring semantic search only above ~1,000 files (`V-F6`), which its own vendor then stopped shipping. The gap that matters for R5.1 is unchanged: **no measurement on short markdown entries** (`S-F5`, `V-F11`).

---

## Slice 2 — when a code graph pays off

### N7 — CONFIRMED (by id). Size does not order the effect; question type does.
`G-F7` / `G-F7a`, codegraph's own benchmark, 7 repos, one architecture question, Claude Code headless, median of 4 runs: VS Code ~11k files **71% cheaper** (2 vs 28 tool calls, 0 vs 12 file reads); Excalidraw ~640 files **78% cheaper**; Gin ~110 files **~even**; Django ~3k files **13% cheaper**. The vendor's own sentence:
> "Cost tracks how much *discovery* a question demands more than raw repo size: 57–78% on questions the file-reading agent needed 28–43 tool calls to answer, near-even where it got there in 7."

`G-F7b` is the offset on the same repos: *"CodeGraph's responses leave about **80% more retrieval context resident** at the end of a session than a file-reading agent's do — on VS Code, 67k tokens against 18k."*

### N8 — CONFIRMED (by id). The class where a graph beats both grep and BM25 is dependencies with no lexical overlap — and it must be adopted.
`s3-F16`, arXiv 2602.20048: *"achieves 99.4% task completion on hidden-dependency tasks, a 23.2 percentage-point improvement over vanilla agents (76.2%) and 21.2 points over BM25 retrieval (78.2%)"*; and *"58% of trials with graph access made zero tool calls."*

### N9 — CONFIRMED (vendor self-evaluation), NEW: the graph/LSP pay-off is already visible at **43 files**, and it is task-shaped, not size-shaped.
oraios.github.io/serena/04-evaluation/030_results/010_cc_on_tianshou.html (opened today; the report is generated by Claude Opus 4.6 in Claude Code, dated 2026-04-13, on *"Tianshou — a Python reinforcement learning library (~26K lines, 43 source files)"*, 20 tasks, both toolchains, edits verified with `git diff`):

| task | Serena (semantic) | built-in grep/read/edit |
|---|---|---|
| cross-file rename (4 files) | 1 call | *"1 Grep + 4 Read + 4 Edit = 9"* |
| move symbol across modules | 1 call | *"(Read source, Edit source to remove, Edit target to add, Grep for imports, Read+Edit each import site)"* ~8–12 |
| type hierarchy | 1 call, transitive | *"2+ (Grep for `class X(BaseCollector` + Grep for `class Collector(` + potential transitive search)"* |
| find referencing symbols | 1 call, *"63 (code files only…)"* | 1 call, *"83 (includes docs, notebooks, changelogs, README)"* |
| 1-line edit inside a 13-line method | ~550 chars (whole body) | ~120 chars — *"Edit (~4.5×)"* |
| 55-line method rewrite | ~2200 chars | ~4400 chars — *"Serena (~2×)"* |

Verbatim scope limit from the same report: *"These tasks constitute roughly 40–60% of a typical coding session (reading docs, running tests, searching for patterns, editing config)"* is outside the tool's scope; and for pure exploration *"Serena's advantage is modest"*. Caveat: the agent evaluates itself, by the vendor's own stated design (*"The agent evaluates itself. This is deliberate"*), with no independent replication and no token counts — payload **characters** only. So: **tool-call and payload-shape savings are documented; token savings are not.**

### N10 — CONFIRMED, NEW, and thin: Aider's repo map publishes a *budget*, not a saving.
aider.chat/docs/repomap.html (opened today):
> "The token budget is influenced by the `--map-tokens` switch, which defaults to 1k tokens."

and the mechanism (aider.chat/2023/10/22/repomap.html, Oct 22 2023): *"analyzing the full repo map using a graph ranking algorithm, computed on a graph where each source file is a node and edges connect files which have dependencies."* So aider pays a **graph index** to be able to send a *fixed 1k-token* map every turn. That is the correct shape for R5.3's cost argument — a bounded, always-cheap prompt-side artifact — but **no measurement of tokens saved exists** (see *Not found*).

### N11 — CONFIRMED, NEW. Sourcegraph's SCIP is a format, and publishes no size, time or accuracy figure.
raw.githubusercontent.com/sourcegraph/scip/main/README.md (opened today): *"SCIP … is a language-agnostic protocol for indexing source code, which can be used to power code navigation functionality such as Go to definition, Find references, and Find implementations."* Nothing else quantitative. Its practical relevance here is negative: the format that large code hosts standardised on is a *definition/reference* index, i.e. the `G-F8` question class, not a free-text store.

### N12 — CONFIRMED, NEW. Cursor's answer to "large codebase search" was to index grep, not to ship a graph or vectors (see N2): *"Instant Grep … outperforms `ripgrep` on large codebases"*, unquantified.

**Reading (mine):** across four tools and five sources, the only ordering variable that predicts a code-structure tool's pay-off is *question type* (multi-file refactor, hidden dependency, transitive hierarchy), never file count. The record's smallest demonstration of a pay-off is 43 files (`N9`); its largest is 11k files at the weakest tool-call ratio (`G-F7`). Repo size is not a trigger for R5.3, and `G-F10` (no measurement on a markdown decisions corpus) is still the load-bearing gap.

---

## Slice 3 — index build/rebuild cost and disk size

### N13 — CONFIRMED (first-party, this machine). All three caches over this repo: sub-second rebuild, index ≈ 2× the corpus.
Source: `runs/20261012-caches-routing/bench/results.md:9-15` — corpus *"490 files (123 `.py`, 367 `.md`), 4021 chunks"*, 4.8 MB (`CACHES.md` §Measured here):

| store | seconds | bytes |
|---|---:|---:|
| fts | 0.169 | 9,457,664 |
| vec | 0.936 | 10,215,424 |
| graph | 0.892 | 4,902,912 |

*Arithmetic on those figures (mine, not a source's claim):* fts ≈ 0.035 s/MB and 1.97× corpus; vec ≈ 0.20 s/MB and 2.13× corpus, with `EMBED_DIMS = 256` and `EMBED_MODEL = "minishlab/potion-base-8M"` (`bench/build.py:50-51`); graph ≈ 0.19 s/MB and 1.02× corpus. Every query answered in ≤15 ms (`BM-9`).

### N14 — CONFIRMED (first-party, other engine) on a corpus shaped like our entries. FTS5 rebuild scales linearly and the index is ~2.1× the markdown.
`S-F13`, `sqlite-fts.claude.md:98-107`, synthetic entries with the design's frontmatter and ~1 KB body, one run each on WSL2 (Python 3.12, SQLite 3.45.1):

| entries | markdown | index file | full rebuild | one-word `grep -rli` | FTS5 top 10 |
|---|---|---|---|---|---|
| 100 | 0.1 MB | 0.3 MB | 0.03 s | 0.002 s | 0.0006 s |
| 1,000 | 1.1 MB | 2.3 MB | 0.08 s | 0.005 s | 0.0002 s |
| 10,000 | 10.6 MB | 21.9 MB | 0.53 s | 0.038 s | 0.0006 s |
| 50,000 | 53.2 MB | 110.3 MB | 2.57 s | invalid (clock) | — |

*Arithmetic:* ≈0.05 s/MB and ≈2.1× corpus at 10k; ≈0.048 s/MB and ≈2.07× at 50k. The node's own verdict: *"At every size the grep route answers in well under half a second, so latency is not a reason for a cache at this scale; the index is about twice the markdown size."*

### N15 — CONFIRMED (first-party). Code graph over this repo.
`G-F12`, `code-graph.opencode.stdout.md:113-130`: *"full rebuild **0.94 s** wall, 0 errors"* over *"126 files, 126 modules, 1240 functions, 433 tests, 13 fixtures"* and *"**3700** (call 2000, contains 1240, import 345, fixture 115)"*; *"Graph size on stdout **2,607,872 bytes** (~2.6 MB)"*; and the scaling observation *"the 0.6 s → 0.94 s growth tracks 110 → 126 files: linear-ish, and still under a second at this size."* *Arithmetic:* ≈7.5 ms and ≈20.7 KB per `.py` file.

### N16 — CONFIRMED, NEW, and the only vendor statement on *incremental* index cost for a code graph.
colbymchenry.github.io/codegraph/guides/indexing/ (opened today): watcher *"event delivery: typically <100ms"* → *"2000ms debounce"* → sync; `CODEGRAPH_WATCH_DEBOUNCE_MS` *"clamped to `[100ms, 60s]`"*; connect-time *"fast filesystem-based reconciliation (a `(size, mtime)` stat pre-filter, then a content hash on the rest)"*; *"files over 1 MB"* are not indexed. The docs promise *"sync is fast"* with **no number**, and no absolute full-index time — the vendor's own position is that the incremental path is the cheap one, which is exactly what `G-F5 drift` shows is also the *drifting* one.

### N17 — CONFIRMED, NEW, and the one hard published rate for a local embedding model.
MinishLab/model2vec `results/README.md` (opened today), inference-speed table, samples/second: **`model2vec full finetune` 81,018 / `setfit` 1,010 / `minilm full finetune` 274**. Verbatim from the project README: *"makes models up to 500 times faster, with a small drop in performance"*; *"Our best model … is just ~30 MB on disk, and our smallest model just ~8 MB"*; and from the card for the model this repo's bench used, *"allowing text embeddings to be computed **orders of magnitude faster** on both GPU and CPU."* Limits: hardware unspecified; the samples are short single sentences from the classification benchmark, not document chunks; `potion-base-8M` scores 51.32 MTEB-average vs `all-MiniLM-L6-v2` 55.80 (*"91.96% of the performance"*) — a static model is a cheaper rebuild *and* a weaker index, which is the trade-off R5.2 has to record, not hide.

**Reading (mine):** the rebuild costs the design already carries (0.17–0.94 s; ≈2× corpus on disk) are one to two orders of magnitude below any plausible per-session reading saving, and the only axis on which the rebuild cost moves by a large factor is *which embedding model* (`N17`: ~300× between a static model and a MiniLM fine-tune). That is an argument for R8.2's shape ("rebuild is cheap"), not a number to set the trigger by.

---

## Example values

| condition | agent or model | value | what it supports | source |
|---|---|---|---|---|
| Corpus 1,144 docs / 1.7M tokens, one RAG question | "BM25 Wins at Scale" File-System Agent (grep/list_dir/read_doc) vs BM25 | 5.8K vs **226K query tokens/question**; agent led at the smallest tiers | R5.1 (crossover sits far above short entries) | `S-F4`, arXiv 2607.26497v3 (2026-07-31) |
| Corpus ≥ ~10M tokens | same | BM25 overtakes the grep agent and leads at every larger tier | R5.1 | `S-F4` |
| Codebase ≥ 1,000 files | Cursor's models, private Context Bench | code retention +2.6%; accuracy +12.5% avg (6.5–23.5%) | R5.2 — the only file-count threshold in the record | `V-F6`, cursor.com/blog/semsearch (2025-11-06) |
| Same vendor, same corpus class, 15 days later | Cursor Agent, all models | ships Instant Grep; docs now say it *"does not store embeddings of your codebase for search"* and *"outperforms `ripgrep` on large codebases"* (no number) | R5.2 — the threshold was withdrawn by its own vendor | cursor.com/changelog/2-1 (2025-11-21); cursor.com/docs/context/codebase-indexing (opened 2026-10-12) |
| Any repo, hybrid strategy | Claude Code (Anthropic) | index file up front + glob/grep just-in-time, *"effectively bypassing the issues of stale indexing and complex syntax trees"*; price: *"runtime exploration is slower than retrieving pre-computed data"* | R5.1 / R5.2 ordering rule | anthropic.com/engineering/effective-context-engineering-for-ai-agents (2025-09-29) |
| Result set too large to read into context | Claude Code code execution | 150,000 → 2,000 tokens (**98.7%** saved) by filtering in code | R5.1 — the "characters printed" proxy is the axis that moves | anthropic.com/engineering/code-execution-with-mcp (2025-11-04) |
| **Memory index, one line per memory** | Claude Code auto memory | *"The first 200 lines of `MEMORY.md`, or the first 25KB, whichever comes first"* loaded per session; beyond it, topic files are *"read on demand using its standard file tools"* | **INDEX.md size** ≈ 200 entries; overflow path is grep+read, not vectors | docs.claude.com/en/docs/claude-code/memory (opened 2026-10-12) |
| Always-loaded project instruction file | Claude Code | *"target under 200 lines per CLAUDE.md file"*; loaded in full up to 4 MiB | INDEX.md size | same |
| Memory corpus ≤ 200,000 tokens (~400–650 entries) | Anthropic | *"you can just include the entire knowledge base in the prompt … with no need for RAG"* | R5.1 bound (cited, not re-opened) | `V-F8`, anthropic.com/news/contextual-retrieval (2024-09-19) |
| Chat memory, inline delivery, 116 questions | Claude Code + Opus 4.6, Codex + GPT-5.4, Chronos + Opus, etc. | inline grep > inline vector for **every** harness-model pair (93.1 vs 83.6; 93.1 vs 75.9); vector wins5/10 pairs under file-based delivery | R5.2 | `V-F3`, arXiv 2605.15184 (2026-05-14) |
| Enterprise corpus 500,000 docs | OpenAI text-embedding-3-large + Qdrant | correctness BM25 68.8 / vector 51.4 / bash agent 60.6; semantic questions vector 32.8 | R5.2 | `V-F4`, arXiv 2605.05253 |
| Repo 110 files (Gin), one architecture question | Claude Code headless + codegraph | 1 vs 7 tool calls, cost **~even** | R5.3 — size does not order it | `G-F7` |
| Repo 640 files (Excalidraw) | same | 2 vs 43 calls, **78% cheaper**, 84% fewer tokens | R5.3 | `G-F7` |
| Repo ~3k files (Django) | same | 3 vs 14 calls, **13% cheaper** | R5.3 | `G-F7` |
| Repo ~11k files (VS Code) | same | 2 vs 28 calls, 71% cheaper, 0 vs 12 file reads — **but 67k vs 18k tokens still resident after the session** | R5.3 + the `G-F7b` offset | `G-F7`, `G-F7b` |
| Hidden-dependency tasks, production FastAPI repo | agent + CodeCompass vs vanilla vs BM25 | 99.4% vs 76.2% vs 78.2%; 58% of graph trials made zero tool calls | R5.3 — task type, not size; adoption is part of the cost | `s3-F16`, arXiv 2602.20048 |
| **43 files / 26K lines,20 tasks** | Claude Code Opus 4.6 + Serena (vendor self-eval) | cross-file rename 9→1 calls; move 8–12→1; references 63 code files vs grep 83; payload ~8× smaller on rename, **4.5× worse** on a 1-line edit; 40–60% of a session out of scope | R5.3 — pay-off visible at 43 files, task-shaped; precision not recall | oraios.github.io/serena/…/010_cc_on_tianshou.html (report dated 2026-04-13) |
| Any repo | aider | repo map confined to `--map-tokens`, **default 1k tokens**, graph-ranked | R5.3 (a bounded prompt-side artifact) — no saving measured | aider.chat/docs/repomap.html; aider.chat/2023/10/22/repomap.html |
| **490 files / 4.8 MB / 4,021 chunks (this repo)** | FTS5 | full rebuild **0.169 s**, **9,457,664 bytes** (≈2× corpus) | **R8.2** | runs/20261012-caches-routing/bench/results.md:13 |
| same | vector, `potion-base-8M`, 256 dims | **0.936 s**, **10,215,424 bytes** (≈2× corpus) | R8.2 | results.md:14 |
| same | code graph | **0.892 s**, **4,902,912 bytes** (≈1× corpus) | R8.2 | results.md:15 |
| 10,000 entries / 10.6 MB | FTS5 rebuild | **0.53 s**, index **21.9 MB**; grep one word 0.038 s | R8.2 | `S-F13`, sqlite-fts.claude.md:104 |
| 50,000 entries / 53.2 MB | FTS5 rebuild | **2.57 s**, index **110.3 MB**; header-chain grep 0.148 s | R8.2 | `S-F13`, sqlite-fts.claude.md:105 |
| 126 `.py` files (this repo) | `code_graph/code_graph.py` | **0.94 s**, 3,700 edges, **2,607,872 bytes** stdout | R8.2 | `G-F12` |
| Local embedding, short samples | model2vec full finetune vs setfit vs MiniLM finetune | **81,018 / 1,010 / 274 samples/s** | R8.2 — the embedding step is the only cost that moves by ~300× | MinishLab/model2vec `results/README.md` |
| Incremental code-graph sync (codegraph) | codegraph MCP watcher | event delivery *"typically <100ms"* → **2000 ms** debounce → sync; files >1 MB not indexed; no absolute build time published | R8.2 — vendor sells incremental, `G-F5 drift` shows it drifts | colbymchenry.github.io/codegraph/guides/indexing/ |

## Not found

- **Any measured crossover for a few hundred to a few thousand short markdown memory entries.** `S-F5` and `V-F11` stand; nothing new found. This is the gap that blocks a numeric R5.1 at our size.
- **Any published FTS5 index size or build rate per MB from SQLite or a vendor benchmark.** `sqlite.org/fts5.html` carries no performance figures (recorded by the earlier engine as `S-F2`/`S-F14`; I did not re-open it). The only FTS5 numbers in the record are first-party (`S-F13`, BM-9).
- **Any published on-disk size per document or per MB for a local vector index** (sqlite-vec, FastEmbed, Model2Vec, HuggingFace). The only published vector figure I found is throughput, not size.
- **Any absolute full-index build time for codegraph.** Its docs give debounce and event delivery only (`N16`).
- **Any SCIP index size or build time from Sourcegraph** (`N11`), and any Sourcegraph-side measurement of a code graph's pay-off.
- **Any measurement of tokens saved by Aider's repo map.** The docs publish a budget (1k tokens), not a saving (`N10`).
- **Any code-graph pay-off number expressed in repo size in symbols** (as opposed to files or questions). All published numbers are per-question tool calls, tokens or accuracy.
- **Any Serena token counts.** The evaluation reports payload *characters* and call counts only; the agent judges itself.
- **Any code-graph or vector-index measurement on a markdown decisions-and-facts corpus.** `G-F10` unchanged.
- **Any absolute accuracy figures behind Cursor's semantic-search claims** (their Context Bench scores are unpublished — the `V-F6` caveat stands, and `N2` adds that the feature is gone).
- **Any `INDEX.md`-shaped size cap other than Claude Code's `MEMORY.md`** (no OpenAI/Cursor/Aider equivalent publishes one).

## Not checked

- **Sources I cited by id but did not re-open:** `sqlite.org/fts5.html` (S-F2, S-F14), cursor.com/blog/semsearch (V-F6), arXiv 2607.26497 (S-F4), arXiv 2605.15184 (V-F3), arXiv 2605.05253 (V-F4), arXiv 2602.20048 (s3-F16), the codegraph README and drift benchmark (G-F7, G-F5), Anthropic contextual-retrieval (V-F7, V-F8). Their quotes above are as recorded in the node files.
- **Tools I did not open because I found no lead to a quantitative page:** Letta/MemGPT, Zep/Graphiti and its arXiv paper, Mem0, CodeRankEmbed, Sourcegraph Cody docs, `ctags`/`global`, Tantivy, Meilisearch, qmd (V-F14 cited only), basic-memory (V-F15), claude-context (V-F16), FastEmbed (V-F19 cited only).
- **I measured nothing.** No new benchmark was run: this engine ran no build, no timing, no index. Every timing above is either a first-party figure already committed to this repo (`results.md`, `S-F13`, `G-F12`) or a vendor/paper figure, each labelled.
- **Not read:** the merge-review copies of `CACHES.md` (`runs/20261012-caches-merge/reviews/*`), `runs/20261012-caches-routing/vision-proposals.md`, and `docs/research/20261011-agent-memory-graph-r2/FINDINGS-*.md` — I worked from the live guide `docs/memory-system/CACHES.md`, the three node files, and the bench results. I therefore cannot say whether any open review finding already covers the Serena, Cursor-2.1 or `MEMORY.md` items above.
- **Not verified:** whether Cursor's current docs page is newer or older than its `MEMORY.md`-equivalent; and whether the "outperforms ripgrep" claim has a benchmark behind it that is not public.
