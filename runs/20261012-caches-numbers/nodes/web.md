# Node 1b — Web: published numbers per agent type and condition

Run: `20261012-caches-numbers`. Written 2026-10-12. Engine: Claude subagent (web). Read-only except this file.

## How to read this

- **CONFIRMED** = I opened the primary source (the paper's arXiv page or HTML, the vendor's own doc or blog, the vendor's repo README). **REPORTED** = a secondary source or a search snippet only. **GAP** = not found.
- **Quote reliability.** Pages were read through the WebFetch tool, which returns a model-made extract. Quotes marked (raw) were copied from the saved raw page text and are exact (W-1 only). All other quotes are as the extract returned them inside quotation marks; the numbers were cross-checked against the search snippets where both existed, but treat the wording as "as extracted", not as a byte-exact copy.
- Dates are the source's own date where the page showed one. "Undated" means the page showed none; I give the fetch date, 2026-10-12.
- "My arithmetic" marks a number I computed from a sourced number. It is not a finding of the source.
- Earlier research ids (S-F*, V-F*, G-F*) are cited, not redone. Where this node upgrades one, it says so.

---

## 1. Size limits each tool puts on its memory and instruction files

### W-1 Claude Code — CONFIRMED
- URL: https://code.claude.com/docs/en/memory — undated (fetched 2026-10-12).
- Quote (raw): "The first 200 lines of `MEMORY.md`, or the first 25KB, whichever comes first, are loaded at the start of every conversation. Content beyond that threshold is not loaded at session start."
- Quote (raw): "Files over 200 lines consume more context and may reduce adherence. Claude Code skips a file over 4 MiB."
- Quote (raw), about CLAUDE.md: "target under 200 lines per CLAUDE.md file."
- Quote (raw): "If the file is over a limit, the write still succeeds, but Claude Code returns an error telling Claude to rewrite the index" (the page continues: everything past the limit is dropped on load).
- Re-verified: the repo's "200 lines or 25KB" is correct. It is a two-part limit; the first one reached applies.
- My arithmetic: 25 KB / 200 lines = 125 bytes per line. Lines longer than that make the byte limit bind first. Measured here: `wc -lc` on this project's `MEMORY.md` = 19 lines, 3,182 bytes; median line 159 bytes, max 218. At about 167 bytes per line (3,182 / 19), 25 KB is reached at about 150 lines, before the 200-line limit.

### W-2 Codex CLI — CONFIRMED
- URL: https://learn.chatgpt.com/docs/agent-configuration/agents-md (redirect target of https://developers.openai.com/codex/guides/agents-md) — undated.
- Quote: "Codex skips empty files and stops adding files once the combined size reaches the limit defined by `project_doc_max_bytes` (32 KiB by default)."
- The extract also gave: raise the limit or split instructions across nested directories "when you hit the cap"; example config sets 65536. The cap applies to the combined guidance, not per file. Codex concatenates files from the root down; at the global level it uses only the first non-empty file of `AGENTS.override.md` / `AGENTS.md`.
- Config key default 32768 bytes: REPORTED by a search snippet of OpenAI's config sample (https://developers.openai.com/zh-Hans/docs/config-file/config-sample, "Default: 32768"); I did not open it.
- Not established: whether truncation is silent. A third-party post says so; the official page does not say (UNPROVEN).

### W-3 Cursor — CONFIRMED
- URL: https://cursor.com/docs/context/rules — undated.
- Quote: "Keep rules under 500 lines." Also "Split large rules into multiple, composable rules."
- Always-apply rules: "Always included. Globs and description are ignored." No token or character limit is stated.
- This is a recommendation, not an enforced limit.

### W-4 Google Antigravity — CONFIRMED, with a conflict
- URL: https://www.antigravity.google/docs/rules?tab=ide — undated.
- Quote: "Antigravity truncates any single rule file that exceeds 24,000 bytes" (after `@[label](path)` includes are expanded). Limit is in bytes, so multi-byte text costs more.
- Conflict (REPORTED): a search snippet says the same docs' Rules page and a third-party guide give "12,000 characters" per Rules file, and a Flutter docs table lists "12,000 characters" as a hard limit (https://flutter.googlesource.com/mirrors/flutter.git/+/HEAD/docs/rules/, not opened). The page I opened says 24,000 bytes. Likely a doc revision, but unproven. A design guide should say "between 12,000 characters and 24,000 bytes depending on version" or re-check at use time.
- Whether the same limit applies to a root `AGENTS.md` / `GEMINI.md`: GAP.

### W-5 Gemini CLI — GAP for a limit
- URL: https://geminicli.com/docs/cli/gemini-md/ — "last updated Jun 18, 2026" (per the extract). CONFIRMED that no limit is stated.
- Quote: the CLI "concatenates the contents of all found files, and sends them to the model with every prompt."
- So the cost of `GEMINI.md` is paid on every prompt and no cap protects the user. `Auto Memory` appears only as a nav link marked experimental; no details.

### W-6 opencode — GAP for a limit
- URL: https://opencode.ai/docs/rules/ — "Last updated: Oct 12, 2026". CONFIRMED that no size limit is stated; the only number is "Remote instructions are fetched with a 5 second timeout." Files from `opencode.json` instructions are "combined with your `AGENTS.md` files."

### W-7 Letta / MemGPT core memory blocks — partial
- URL: https://docs.letta.com/guides/core-concepts/memory/memory-blocks — undated. CONFIRMED: "A `limit`, which is the size limit (in characters) of the block." Examples set 5000, 4000 and 6000 characters. Default value and over-limit behaviour: GAP (the docs page does not state them; the source file `letta/constants.py` returned 404 on both the raw URL and `gh api`, so I could not check it).
- A different package (pi-memory-blocks) shows a 2000-character default in a search snippet; that is not Letta (do not use).
- MemGPT paper: https://arxiv.org/abs/2310.08560 (2023). CONFIRMED the idea only: it "manages different memory tiers in order to effectively provide extended context within the LLM's limited context window." No block size there.

### W-17 Do instruction files help at all? — CONFIRMED (abstract)
- URL: https://arxiv.org/abs/2602.11988 — submitted 2026-02-12 (v3 revised 2026-09-29). ETH Zurich + LogicStar.
- Quote: "providing context files does not generally improve task success rates"; "increasing inference cost by over 20% on average." Setup (from a search snippet, REPORTED): SWE-bench tasks with LLM-generated files plus AgentBench, 138 tasks from repositories with developer-written context files; conclusion that files should describe "only minimal requirements."
- Supports: an index read at session start must earn its tokens; it is not free.

### W-16 How many instructions can be followed — CONFIRMED (abstract)
- URL: https://arxiv.org/abs/2507.11538 — submitted 2025-07-15. 20 models, instruction count 10 to 500 (keyword-inclusion, report writing).
- Quote: "even the best frontier models only achieve 68% accuracy at the max density of 500 instructions." Three decay shapes (threshold, linear, exponential) by model; bias toward earlier instructions (decay shapes: REPORTED from a search snippet).
- Caveat: synthetic keyword task, 2025-era models. It bears on a start-of-session index only as "rules in a list are not all obeyed as the list grows".

---

## 2. Context window of each current model, and effective context

### W-8 Claude — CONFIRMED
- URLs: https://platform.claude.com/docs/en/models/overview and https://platform.claude.com/docs/en/build-with-claude/context-windows — undated.
- Quote: Fable 5.1, Opus 5.5, Sonnet 5.5 and Haiku 5.5 all show "1M tokens" context window, 128K max output. The context-windows page lists Opus 4.6 through 5.5, Sonnet 4.6/5/5.5 and others as 1M; "Other Claude models, including Claude Sonnet 4.5 (deprecated), have a 200k-token context window."
- Quote: "1M tokens is roughly 555k words or 2.5M Unicode characters on the current tokenizer."
- Quote: "more context isn't automatically better. As token count grows, accuracy and recall degrade, a phenomenon known as *context rot*."
- Note: Anthropic's own doc states context rot as a fact but gives no number on that page.

### W-9 Other vendors' windows
| Model | Window | Status | Source (date) |
|---|---|---|---|
| GPT-6 Astra, GPT-6.1 Sol, GPT-6 Luna (OpenAI API) | 1.05M | CONFIRMED | https://developers.openai.com/api/docs/models (undated) |
| Codex CLI models | not stated on the Codex models page | GAP | https://learn.chatgpt.com/docs/models (recommends "GPT-6.1 Sol"; no window) |
| Gemini 3.1 Pro (Preview) | input 1,048,576; output 65,536 | CONFIRMED | https://ai.google.dev/gemini-api/docs/models/gemini-3.1-pro-preview (undated) |
| DeepSeek V4 (Pro, Flash) | 1M; max output 384K | CONFIRMED | https://api-docs.deepseek.com/quick_start/pricing (footer 2026; model "DeepSeek-V4-Pro-0813") |
| MiniMax-M3 / M3.1-Flash-Preview | 1,000,000 | CONFIRMED | https://platform.minimax.io/docs/guides/text-generation (undated) |
| MiniMax-M2.7, M2.5, M2.1, M2 | 204,800 | CONFIRMED | same page |
| Qwen3.5-397B-A17B | 262,144 natively, extensible to 1,010,000 | CONFIRMED | https://huggingface.co/Qwen/Qwen3.5-397B-A17B (undated). Quote: "Context Length: 262,144 natively and extensible up to 1,010,000 tokens." Hosted Qwen3.5-Plus: "1M context length by default". YaRN extension is static and "potentially impacting performance on shorter texts." |

Cursor and opencode have no window of their own; they use whichever model is selected. Antigravity/Gemini CLI: the model's window above.

### Effective context: the research

- **W-10 RULER** — CONFIRMED. https://arxiv.org/abs/2404.06654, 2024-04-09 (v3 2024-08-06). Quote: "While these models all claim context sizes of 32K tokens or greater"; "only half of them can maintain satisfactory performance at the length of 32K." 17 models. Old models.
- **W-11 NoLiMa** — CONFIRMED. https://arxiv.org/abs/2502.05167, 2025-02-07 (v3 2025-07-09). Quote: "At 32K, for instance, 11 models drop below 50% of their strong short-length baselines." GPT-4o "from an almost-perfect baseline of 99.3% to 69.7%." Needles with little word overlap with the question (the case for memory entries phrased differently from the question).
- **W-12 Lost in the middle** — CONFIRMED. https://arxiv.org/abs/2307.03172, 2023-07-06 (v3 2023-11-20, TACL). Quote: performance "significantly degrades when models must access relevant information in the middle of long contexts." Supports putting the key lines of an index first and last, not in the middle.
- **W-13 Chroma context rot** — CONFIRMED. https://www.trychroma.com/research/context-rot, 2025-07-14. 18 models (Claude Opus 4/Sonnet 4/3.7/3.5/Haiku 3.5, o3, GPT-4.1 family, GPT-4o, Gemini 2.5/2.0, Qwen3 235B/32B/8B). Quote: "model performance consistently degrades with increasing input length." Quote: "performance degrades more quickly in input length with lower similarity needle-question pairs." LongMemEval subset (306 prompts): focused prompts about 300 tokens against full prompts about 113k tokens, "Performance was consistently higher on focused prompts"; exact accuracy only in charts (GAP for the numbers).
- **W-14 Anthropic, Opus 4.6** — CONFIRMED. https://www.anthropic.com/news/claude-opus-4-6, 2026-02-05. Quote: Opus 4.6 "scores 76%, whereas Sonnet 4.5 scores just 18.5%" on MRCR v2 8-needle at 1M. Calls it "a qualitative shift in how much context a model can actually use." This is the best vendor number for "window is not effective context" for a Claude model, but Opus 4.6 is not the current generation (Opus 5.5 is).
- **W-15 MRCR v2 across vendors** — REPORTED. https://yage.ai/share/long-context-benchmark-en-20260315.html, 2026-03-15, compiling vendor system cards and model cards. Its table: Opus 4.6 93.0% at 256K and 76.0% at 1M; Sonnet 4.6 90.3% / 65.8%; GPT-5.4 79.3% (128K–256K bin) and 36.6% (512K–1M bin); Gemini 3.1 Pro 84.9% at 128K and 26.3% at 1M; Gemini 3 Pro 45.4% at 256K and 24.5% at 1M. The post itself warns scores from different sources "cannot be directly compared." I did not open the vendor reports behind the GPT and Gemini cells.
- **GAP:** no published long-context score found for the current generation (Claude Opus 5.5 / Sonnet 5.5 / Fable 5.1, GPT-6.x, Gemini 3.6/3.8, DeepSeek V4, MiniMax M3). All the effective-context numbers above are for older models. An example value for a 1M-window model today would have to say "Opus 4.6-era: 76% at 1M, 93% at 256K".
- **W-31 Gemini** — CONFIRMED. https://ai.google.dev/gemini-api/docs/long-context (undated). Quote: "You can get ~99% on a single query, but you have to pay the input token cost every time you send that query." And with multiple needles, "the model does not perform with the same accuracy." No number given for multi-needle.

What this gives the guide for "how big an index read at session start": the cited limits (W-1, W-2, W-3, W-4) are all 25 to 32 KB or 500 lines; the research says accuracy loss shows up from tens of thousands of tokens on older models and from a few hundred thousand on newer ones (W-10, W-11, W-14), and that a rule list loses adherence as it grows (W-16, W-17). All of that is far above a few KB. So an index of a few KB is not near any effective-context problem; the limits matter for cost and adherence, not for recall.

---

## 3. When retrieval beats loading everything

- **V-F8 (cited, not redone):** Anthropic 2024: under 200,000 tokens, include the whole knowledge base. Still the only vendor threshold found.
- **W-18 LongMemEval** — CONFIRMED. https://arxiv.org/abs/2410.10813 (abstract) and https://arxiv.org/html/2410.10813. Submitted 2024-10 (ICLR 2025). Quote: "commercial chat assistants and long-context LLMs showing a 30% accuracy drop". LongMemEval_S is "approximately 115k tokens per problem, with histories of about 50 sessions"; LongMemEval_M is 500 sessions, "around 1.5 million tokens." Long-context reading, oracle (only the right sessions) against S (everything): GPT-4o 0.870 vs 0.606 (30.3% drop); Llama 3.1 70B 0.744 vs 0.334 (55.1%); Llama 3.1 8B 0.710 vs 0.454 (36.1%); Phi-3 128k 14B 0.702 vs 0.380 (45.9%). So reading about 115K tokens of history, which fits in every window above, cost 30% to 55% of accuracy for those 2024 models.
- **W-19 BEAM** — CONFIRMED. https://arxiv.org/html/2510.27246v1 (Tavakoli et al., ICLR 2026; v1 2025-10). 100 conversations up to 10M tokens, 2,000 questions. Table 1 average score, "Vanilla" (long context) / RAG:

| Model | 100K | 500K | 1M | 10M |
|---|---|---|---|---|
| Llama-4-Maverick | 0.240 / 0.323 | 0.283 / 0.330 | 0.259 / 0.307 | 0.104 / 0.249 |
| GPT-4.1-nano | 0.239 / 0.309 | 0.194 / 0.314 | 0.191 / 0.302 | 0.109 / 0.218 |
| Gemini-2.0-flash | 0.242 / 0.280 | 0.257 / 0.267 | 0.199 / 0.271 | 0.122 / 0.216 |
| Qwen2.5-32B-AWQ | 0.280 / 0.269 | 0.200 / 0.291 | 0.193 / 0.285 | 0.133 / 0.211 |

  Quote: "even LLMs with long context windows perform substantially worse as conversation length increases." Read: retrieval already matched or beat loading at 100K in 3 of 4 models and beat it in all 4 from 500K (my reading of the table). Caveats from the paper: vanilla at 10M uses "the largest recent segment that fits" each window; the Qwen vanilla baseline used 128K while RAG used 32K. Models are 2025-era. The unit is conversation tokens, not entries.
- **W-20 Mem0, vendor** — REPORTED (vendor's own page). https://mem0.ai/blog/state-of-ai-agent-memory-2026 — page shows "Published Oct 12, 2026; first posted Apr 1, 2026". Mem0 retrieves "approximately 6,900 tokens per query" on LoCoMo (92.5), LongMemEval (94.4), BEAM 1M (64.1) and BEAM 10M (48.6); the 2025 paper's full-context baseline was "~26,000" tokens per conversation. The page says the figures are not independently reproduced and one is flagged "confirm sourcing before publishing".
- **W-13 (above)**: focused ~300 tokens against full ~113k, same questions: focused better.
- **W-21 Anthropic, context engineering** — CONFIRMED. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents, 2025-09-29. Quote: "CLAUDE.md files are naively dropped into context up front" while "primitives like glob and grep allow it to navigate its environment." Subagents return summaries of "1,000-2,000 tokens" after exploring with "tens of thousands of tokens or more." No threshold.
- **GAP:** no newer vendor threshold than 200K tokens, and no threshold stated in entries. S-F5 (my arithmetic in the repo: 200K tokens is about 400 to 650 entries at 300 to 500 tokens each, V-F12) stays an estimate.

---

## 4. When search beats grep for an agent, by corpus size

- **W-22 BM25 Wins at Scale** — CONFIRMED (upgrades S-F4, which had only the abstract and the smallest tier). https://arxiv.org/html/2607.26497v3 (v3 2026-07-31). Combined score, by tier (docs, corpus tokens: BM25 / File-System Agent with grep, up to 30 matching paths / DenseRAG):

| Docs | Corpus tokens | BM25 | Grep agent | Dense |
|---|---|---|---|---|
| 1,144 | 1.7M | 74.7 | 77.4 | 58.1 |
| 2,254 | 3.0M | 71.4 | 75.4 | 55.7 |
| 6,980 | 8.5M | 70.1 | 69.9 | 51.0 |
| 21,614 | 25.6M | 64.9 | 62.6 | 44.2 |
| 66,932 | 78.6M | 59.5 | 56.7 | 38.1 |
| 131,876 | 154.7M | 55.2 | 50.9 | 36.0 |
| 511,959 | 600.8M | 50.5 | 30.7 | 29.9 |

  Tokens per query: BM25 5.8K (nearly constant), dense 4.9K, grep agent 226K at the smallest tier and 343K at 21,614 docs. Quote (from S-F4): "Around 10 million corpus tokens, BM25 overtakes it". Reading from the table: the grep agent leads by 2.7 and 4.0 points at 1,144 and 2,254 docs, BM25 leads by 0.2 at 6,980 docs. Dense was the lowest at every size. General RAG corpus, not code or notes; one reader model; preprint. Entry equivalents are the repo's arithmetic (S-F5): 8.5M tokens is about 30,000 entries at 0.27M tokens per 1,000.
  The accuracy gap is small in the first tiers; the token cost gap is large (226K vs 5.8K per question at 1,144 docs). So at small sizes the case for an index is cost, not accuracy.
- **W-23 Direct corpus interaction (grep agents) at large scale** — CONFIRMED abstracts.
  - https://arxiv.org/abs/2605.05242 (Li et al., 2026-05-03): grep-and-shell agents "without any embedding model, vector index, or retrieval API"; outperform sparse, dense and reranking baselines on several BRIGHT and BEIR sets. No numbers on the abstract page.
  - https://arxiv.org/abs/2606.06880 (Zhuang et al., 2026): "latency degrades sharply as the corpus grows"; at 1M documents RISE-BM25 reaches 81% (gpt-5.4-mini) while pure-shell DCI on gpt-5.4-nano "degrades to 60%, with 33 of 100 queries failing on wall-clock time."
  - https://arxiv.org/abs/2606.14885 (DR-DCI, 2026): raw DCI "becomes unstable" as the corpus grows from 100K to 10M documents.
  - https://arxiv.org/abs/2608.20317 (2026-08-20): moving BrowseComp-Plus (about 100K documents) into a 553M-document corpus, the strongest agent "loses five points of answer accuracy" but evidence recall falls "from 84.3% to 21.4%", with 63% more search calls.
  - Reading: grep-agent trouble shows at 100K to 1M documents (web-size documents), well above any memory store.
- **V-F6 (cited):** Cursor, 2025-11-06: 12.5% average accuracy gain from semantic search; the effect on code retention grows to 2.6% "on large codebases with 1,000 files or more". Cursor's own model and benchmark. Best result is grep plus semantic.
- **V-F4 (cited):** EnterpriseRAG-Bench, 500K documents: BM25 68.8 / vector 51.4 / bash agent 60.6 correctness.
- **S-F6 (cited):** LongMemEval QA, grep beat vector in a harness study (Claude Opus 4.6 in Claude Code: inline grep 76.7, inline vector 75.0).
- **W-28 ripgrep, the floor for grep** — CONFIRMED but old. https://burntsushi.net/ripgrep/ (2016; hardware: EC2 c3.2xlarge, Ubuntu 16.04). Linux kernel source, pattern `PM_RESUME`: "rg 0.349 +/- 0.104", "git grep 0.342 +/- 0.005". One 1 GB file: "rg 0.268", "grep 0.516". So a text search over a source tree the size of the Linux kernel took about a third of a second on 2016 hardware. This sets the latency baseline: a memory store of a few thousand short files is far smaller.
- **GAP:** no controlled study of full-text or vector against grep on a corpus of a few hundred to a few thousand short notes or memory entries (S-F5 gap holds). The smallest controlled tier found is 1,144 documents (W-22).

---

## 5. When a code graph pays off

- **W-25 CodeGraph, vendor benchmark** — CONFIRMED, vendor on own tool (the repo has G-F7 for the same page; the table below is new). https://github.com/colbymchenry/codegraph, "measured 2026-08-05" per G-F7 (README last changed 2026-09-30). Claude Code (Opus 4.8), one architecture question per repo, median of 4 runs, with against without the graph:

| Repo (files) | Tool calls | Tokens | Cost |
|---|---|---|---|
| VS Code (~11k) | 2 vs 28 | 155k vs 670k | $0.53 vs $1.80 |
| Excalidraw (~640) | 2 vs 43 | 156k vs 991k | $0.54 vs $2.43 |
| Tokio (~790) | 3 vs 29 | 201k vs 573k | $0.66 vs $1.83 |
| Alamofire (~110) | 4 vs 33 | 209k vs 505k | $0.54 vs $1.27 |
| Django (~3k) | 3 vs 14 | 183k vs 309k | $0.55 vs $0.63 |
| OkHttp (~645) | 1 vs 6 | 107k vs 230k | $0.39 vs $0.50 |
| Gin (~110) | 1 vs 7 | 87k vs 180k | $0.31 vs $0.31 |

  Headline on the page: 88% fewer tool calls, 62% fewer tokens, 44% lower cost on average; zero file reads with the graph. Question type in all seven: an architecture or "how does X flow" question. My arithmetic and reading: the cost saving is not ordered by file count. Gin (110 files) and Django (3,000) save nothing or 13%; Alamofire (110) saves 57%; Excalidraw (640) saves 78%. The saving follows the question's reach across files more than the file count. The tokens with the graph are 87K to 209K across repos, so there is a floor of roughly 90K to 200K tokens per such question. Vendor's own benchmark, one question per repo.
- **G-F8 (cited):** arXiv 2602.20048: a graph win is task-shaped, not size-shaped. **G-F9 (cited):** the agent must adopt the graph. **G-F10 (cited):** no measurement of a code graph on a markdown memory corpus: GAP, still.
- **W-26 Aider repo map** — CONFIRMED. https://aider.chat/docs/repomap.html (undated). Quote: `--map-tokens` "defaults to 1k tokens"; it "does expand the repo map significantly at times, especially when no files have been added to the chat." Ranking: "a graph ranking algorithm, computed on a graph where each source file is a node." A real default for "how much structure map to show an agent": 1,000 tokens.
- **GAP:** published number of symbols or files at which a code graph starts to win with a fixed threshold, and any number for question types other than architecture flow (rename, call-site count, who-covers-this-file).

---

## 6. Rebuild and index times, and sizes

- **W-24 Cursor codebase indexing** — CONFIRMED (vendor). https://cursor.com/blog/secure-codebase-indexing, 2026-01-27. Quote: large repos "can take hours to process if indexed naively", and semantic search stays unavailable until at least 80% is done. Time to first query before and after index reuse: median repo 7.87 s to 525 ms; 90th percentile 2.82 min to 1.87 s; 99th percentile 4.03 hours to 21 s. Clones within an organisation are "92% similarity". A 50,000-file workspace's filenames and SHA-256 hashes total "roughly 3.2 MB." Vendor hosted embeddings, not a local rebuild.
- **W-25 CodeGraph build times** — CONFIRMED (vendor). Swift compiler repo (about 27k files) "fresh-indexes in about 100 seconds"; Linux kernel (about 70k files, about 2M symbols) indexes "in under 12 minutes" on a 2-core, 6 GB VPS; a one-file edit re-syncs in "~4" seconds. My arithmetic: about 3.7 seconds per 1,000 files (Swift) and at most about 10 seconds per 1,000 files (Linux, upper bound). Compare with G-F12 (cited): the in-repo graph, 0.94 s on this repo.
- **W-27 sqlite-vec** — CONFIRMED. https://alexgarcia.xyz/blog/2024/sqlite-vec-stable-release/index.html, 2024-08-01, 8 GB Mac mini. Brute-force KNN, k=20: 1M × 128-dim 17 to 81 ms depending on variant; "for small dimensions (1024/768/384/192), all response are below 75ms" at 100k vectors; 100k float vectors 1536-dim 105 ms, 3072-dim 214 ms; 1M float vectors: "none passed the 100ms target", 192-dim 192 ms, 3072-dim "8.52s". Build (vec0, 1M × 128-dim) 4.0 to 4.6 s; 500k × 960-dim 13.6 to 15.5 s. Quote: "Build times are slow, as every insert tracks with SQLite transactions". Query time does not include embedding the text (the model step).
- **W-29 qmd** — CONFIRMED (README, https://github.com/tobi/qmd, undated). Models: embedding about 300 MB, reranker about 640 MB, query expansion about 1.1 GB. Chunks of "900 tokens/chunk, 15% overlap". Exact vector scan when the eligible set is "at most 20,000 chunk vectors". Fusion "Reciprocal Rank Fusion with k=60". Idle context disposed "after 5 min idle", "~1s penalty" on next request. No index time or corpus size stated (GAP).
- **FTS5 build time:** GAP from a primary source. A SQLite forum search found no timing. Only the local S-F13 (0.53 s for 10,000 entries) exists. REPORTED by a search snippet (W-30, https://sqlite.org/forum/info/ccf1ea60a33705a2, not opened): one user's FTS5 index of about 80k emails (detail=none, porter, external content) was about 1.98 GB against 4.6 GB of bodies, about 43%; the maintainer suggested `optimize`. The repo's S-F13 has the index at about twice the markdown size for the default setup.
- **W-32 Embedding speed:** REPORTED only. A search snippet of arXiv 2603.24246 says all-MiniLM-L6-v2 "encodes around 14,000 sentences per second on a standard CPU as stated by the developers"; another result measured 42.32 sentences/s on 24 sentences. The two disagree by more than 300 times; do not use either as an example.
- **Not an index:** a git or ripgrep path scan is the zero-build case: 0.00 to 0.01 s (G-F12), 0.35 s on the Linux tree (W-28).

---

## 7. Recall or precision as a memory grows

- **W-19 BEAM (above)**: all methods fall as the dialogue grows from 1M to 10M tokens. RAG: Llama-4 0.307 to 0.249; GPT-4.1-nano 0.302 to 0.218; Gemini-2.0-flash 0.271 to 0.216; Qwen2.5-32B 0.285 to 0.211. The paper's own method LIGHT also falls: Gemini 0.284 to 0.192.
- **W-20 Mem0, vendor**: BEAM 1M 64.1 to BEAM 10M 48.6 "is a ~25% performance loss as context scales 10x" (the page's own wording; the raw drop is 24%), with tokens per query flat at about 6,700 to 6,900. Vendor's own score, REPORTED.
- **W-18 LongMemEval**: the M setting (about 1.5M tokens, 500 sessions) with Stella V5, sessions as values: Recall@5 0.706, Recall@10 0.783 (key = value); 0.732 and 0.862 with extracted facts added to the key; GPT-4o QA top-5 0.670 → 0.714. Quote: expanding keys with user facts gave "an average 9.4% higher recall@k and 5.4% higher final accuracy." No S-versus-M retrieval comparison with the same retriever is on the HTML page I read (GAP; I read the first 100,000 of 133,126 characters).
- **Vendor LoCoMo/LongMemEval scores (REPORTED, W-20):** Zep LoCoMo 80.32% at 189 ms (up to 83%); Zep LongMemEval 71.2 (GPT-4o); Letta LoCoMo 74.0 (gpt-4o-mini), no standard LongMemEval result; OpenAI Memory LoCoMo 52.9, "not independently confirmed". The page itself says independent results "can differ widely".
- **GAP:** no curve of precision or recall against the *number of stored items* for a memory of a few hundred to a few thousand entries. BEAM varies conversation length, not item count; nothing found varies the count of entries while keeping the questions fixed.

---

## Example values by agent type and condition

"Supports" names the CACHES.md part. Values marked (my arithmetic) are computed from the sourced figure. Rows with GAP give no number on purpose.

| Condition | Agent or model | Value | Supports | Source id |
|---|---|---|---|---|
| Auto-memory index loaded at session start | Claude Code | first 200 lines or first 25 KB of `MEMORY.md`, whichever is reached first; at about 167 bytes per line (this project, measured) 25 KB is about 150 lines | INDEX.md size | W-1 |
| Hand-written instruction file | Claude Code | target under 200 lines; skipped above 4 MiB | INDEX.md size | W-1 |
| Instruction file(s) combined | Codex CLI | 32 KiB (`project_doc_max_bytes` = 32768) by default, combined across files, adjustable | INDEX.md size | W-2 |
| Rules file | Cursor | keep under 500 lines (recommendation); always-apply rules go into every chat | INDEX.md size | W-3 |
| Rules file | Antigravity / `agy` | 24,000 bytes per file on the official page; 12,000 characters in other reports (conflict) | INDEX.md size | W-4 |
| Context file loaded with every prompt | Gemini CLI | no limit stated; all found files are sent with every prompt | INDEX.md size (GAP for a number) | W-5 |
| Instruction files | opencode | no limit stated | INDEX.md size (GAP for a number) | W-6 |
| Always-in-context memory block | Letta | per-block `limit` in characters, examples 4,000 to 6,000; default not found | INDEX.md size | W-7 |
| Does a context file pay for itself | Several coding agents on SWE-bench-style tasks | no general success gain; inference cost up over 20% on average | INDEX.md size, R5.1 (cost axis) | W-17 |
| Many rules in one list | 20 models, best frontier | 68% accuracy at 500 simultaneous instructions | INDEX.md size | W-16 |
| Window versus effective context, Claude | Opus 4.6 (1M window) | MRCR v2 8-needle: 76% at 1M, 93% at 256K; Sonnet 4.5 18.5% at 1M | INDEX.md size, R5.2 | W-14, W-15 |
| Window versus effective context, others | GPT-5.4 / Gemini 3.1 Pro (1M-class) | MRCR v2: 36.6% (512K to 1M bin) / 26.3% (1M), secondary table | INDEX.md size, R5.2 | W-15 |
| Window versus effective context, older models | 17 models (RULER); 11 models (NoLiMa) | half keep satisfactory performance at 32K; 11 models below 50% of baseline at 32K | INDEX.md size | W-10, W-11 |
| Window versus effective context, current generation | Claude 5.x, GPT-6.x, Gemini 3.6/3.8, DeepSeek V4, MiniMax M3 | GAP: window sizes known (1M, 1.05M, 1,048,576, 1M, 1M), no effective-context score found | INDEX.md size, R5.2 | W-8, W-9 |
| Window sizes | Claude 5.x 1M; GPT-6.x 1.05M; Gemini 3.1 Pro 1,048,576; DeepSeek V4 1M; MiniMax M3 1M, M2.7 204,800; Qwen3.5 262,144 (to 1,010,000 with YaRN) | per row | INDEX.md size | W-8, W-9 |
| Load everything versus retrieve: history of about 115K tokens | GPT-4o, Llama 3.1 70B, Llama 3.1 8B | accuracy 30.3%, 55.1%, 36.1% lower than when given only the right sessions | R5.2 | W-18 |
| Load everything versus retrieve: 100K to 1M tokens of dialogue | Llama-4-Maverick, GPT-4.1-nano, Gemini-2.0-flash, Qwen2.5-32B | RAG ahead of long-context reading for 3 of 4 models at 100K and for all 4 from 500K; e.g. Llama-4 at 100K 0.323 vs 0.240 | R5.2 | W-19 |
| Focused versus full prompt | 18 models (Claude, GPT, Gemini, Qwen) | about 300 tokens against about 113k tokens: focused prompts did better | R5.2, INDEX.md size | W-13 |
| Under the "read it all" threshold | Claude (vendor guidance, 2024) | 200,000 tokens (about 500 pages) | R5.2 (V-F8) | V-F8 |
| Tokens spent per question with retrieval | Mem0 (vendor) | about 6,900 per query against about 26,000 for full context | R5.2 | W-20 |
| BM25 against a grep agent, small corpus | agent with grep (File-System Agent) | 1,144 docs / 1.7M tokens: agent 77.4 vs BM25 74.7 (accuracy), but 226K vs 5.8K tokens per question | R5.1 | W-22 |
| BM25 against a grep agent, crossover | same | 6,980 docs / 8.5M tokens: BM25 70.1 vs 69.9; BM25 ahead at every larger tier; paper's round figure: about 10M tokens | R5.1 | W-22, S-F4 |
| BM25 against a grep agent, large corpus | same | 511,959 docs / 600.8M tokens: BM25 50.5 vs agent 30.7 vs dense 29.9 | R5.1 | W-22 |
| Grep-style shell agent over very many documents | gpt-5.4-nano with shell tools | 1M documents: 60% with 33 of 100 queries failing on wall-clock time, against 81% for BM25-narrowed | R5.1 | W-23 |
| Grep over a source tree | ripgrep, git grep (2016 hardware) | Linux kernel tree about 0.35 s; a 1 GB file 0.27 s | R5.1, R8.2 | W-28 |
| Vector search added to grep for code | Cursor agent | 12.5% average accuracy gain (6.5% to 23.5% by model); code retention gain 2.6% at 1,000+ files | R5.2 | V-F6 |
| Vector alone versus keyword, enterprise corpus | bash agent / BM25 / vector | 500K docs: correctness 60.6 / 68.8 / 51.4 | R5.2 | V-F4 |
| Dense against BM25, documents | DenseRAG pipeline in the same study (embedding model not extracted) | dense lowest at every one of 9 tiers (1,144 docs to 511,959 docs) | R5.2 | W-22 |
| Code graph, architecture question | Claude Code (Opus 4.8) | tool calls 88% lower, tokens 62% lower, cost 44% lower on average over 7 repos; floor of 87K to 209K tokens per question with the graph | R5.3 | W-25 |
| Code graph, small repo | Claude Code (Opus 4.8) | Gin (about 110 files): cost $0.31 with and without; Django (about 3k): $0.55 vs $0.63; no file-count rule visible (Alamofire, also about 110, saves 57%) | R5.3 | W-25 (my arithmetic) |
| Code graph, large repo | Claude Code (Opus 4.8) | VS Code (about 11k files): 155k vs 670k tokens, $0.53 vs $1.80 | R5.3 | W-25 |
| Structure map shown at the start | Aider | 1,000 tokens default, graph-ranked over files | R5.3, INDEX.md size | W-26 |
| Code-graph rebuild | CodeGraph | about 27k files in about 100 s (about 3.7 s per 1,000 files, my arithmetic); about 70k files under 12 minutes; one-file re-sync about 4 s | R8.2 | W-25 |
| Code-graph rebuild, this repo | in-repo graph | 0.94 s | R8.2 | G-F12 |
| FTS rebuild, synthetic | stdlib SQLite FTS5 | 0.53 s for 10,000 entries (not independent) | R8.2 | S-F13 |
| Vector rebuild, query | sqlite-vec | 100k vectors of 1536 dimensions: 105 ms per query; 1M of 192 dimensions: 192 ms; build of 1M × 128 dimensions about 4 s (excludes embedding) | R8.2 | W-27 |
| Hosted vector index first query | Cursor | median 7.87 s to 525 ms after index reuse; p99 4.03 h to 21 s | R8.2 | W-24 |
| Index size | SQLite FTS5 | about 43% of body text (one 80k-email report); about 2× markdown (S-F13, default settings) | R8.2 | W-30 (REPORTED), S-F13 |
| Retrieval quality as memory grows 10× | Mem0 (vendor); RAG on Llama-4, GPT-4.1-nano, Gemini-2.0-flash, Qwen2.5-32B | BEAM 1M to 10M: Mem0 64.1 to 48.6 (24% lower); RAG 0.271–0.307 to 0.211–0.249 | R5.2 | W-20, W-19 |
| Retrieval quality with richer keys | Stella V5 + GPT-4o (LongMemEval_M) | Recall@5 0.706 → 0.732, Recall@10 0.783 → 0.862 with facts added to keys | R5.2 | W-18 |

## Not found (GAP)

1. Letta's default core-memory block limit and its over-limit behaviour (docs silent; source file not reachable).
2. Any size limit for `GEMINI.md` or opencode `AGENTS.md`.
3. Whether Antigravity's 24,000-byte (official page) or 12,000-character (other reports) limit is current, and whether it applies to a root `AGENTS.md`.
4. Context window of Codex CLI's own models (the Codex models page gives none; only the API page gives 1.05M for GPT-6.x).
5. Effective-context scores for the current generation of models (Claude 5.x, GPT-6.x, Gemini 3.6/3.8, DeepSeek V4, MiniMax M3); only 2024 to early 2026 models have numbers.
6. A controlled comparison of full-text, vector and grep on a corpus of a few hundred to a few thousand short notes (smallest tier found: 1,144 documents of general text).
7. Precision or recall against the number of stored items, with the questions held fixed.
8. Any measurement of a code graph over a markdown memory corpus (G-F10 still stands).
9. A file-count or symbol-count threshold for a code graph; question types other than architecture flow.
10. A published FTS5 index build time per MB or per 1,000 files from a primary source.
11. A verified local embedding throughput (one claim of 14,000 sentences/s and one measurement of 42/s disagree).
12. Exact LongMemEval accuracy numbers in Chroma's report (charts only).

## Not checked

- Anthropic's, OpenAI's and Google's own system cards for the MRCR cells in W-15 (I opened only Anthropic's Opus 4.6 announcement).
- The Flutter docs table behind the 12,000-character Antigravity report.
- The OpenAI config sample for the 32768-byte default (the guide's "32 KiB" is confirmed).
- Cursor's own blog for the "1,000 files" quote (taken from V-F6 as cited).
- arXiv 2603.24246 (the embedding-speed claim) and the SQLite forum thread (W-30).
- Cursor, Codex and Gemini CLI source code for how limits are enforced (silent truncation or error).
- The remaining 33 KB of the LongMemEval HTML and 88 KB of the BEAM HTML (per-ability tables, other retrievers).
- DeepSeek, Qwen and MiniMax effective-context claims in their own technical reports.
- Zep, Letta and mem0 papers or repos directly (LoCoMo disputes between vendors were not examined).
- SEZA project measurements (node 1a).
