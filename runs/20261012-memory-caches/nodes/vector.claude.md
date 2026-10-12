# Research: the vector index as a derived cache (run 20261012-memory-caches)

Researcher: claude (`claude-sonnet-5-5`), 2026-10-12. Research only; nothing designed or built.
Setting read first: `docs/memory-system/SOURCE_OF_TRUTH.md` (line 100: `INDEX.md` is "generated, one line per active entry";
line 104: `.cache/` is "optional search index, gitignored, rebuilt from the files"; lines 112-114: read `INDEX.md` at
session start, then "text search over `entries/`" on demand). `project-memory/` does not exist yet in this repo
(checked: `ls project-memory` fails), so there is no corpus and no query log of the project's own to measure.

How sources were opened: arXiv abstracts and HTML full texts, vendor blog/README pages and the Hugging Face and GitHub
APIs were fetched with `curl` and the quoted text was checked in the saved copy. A search-tool summary was never used as
a quote. Labels as in the brief.

## Answer to the planted question

**What recall@10 does the `quillvec` embedding cache report on its own benchmark? No number can be given: GAP.**

- The only thing named `quillvec` that I found is the GitHub repository `revlery/quillvec`. Its description is
  "Semantic search for your notes, no server required". It was created 2026-08-01T03:48:29Z, pushed 2026-08-01T03:48:30Z,
  has 0 stars, size 0, and GitHub answers "This repository is empty." for both contents and commits (API calls on
  2026-10-12). It has no README, no code and no benchmark.
- No package of that name: PyPI (`/pypi/quillvec/json`) 404, npm registry 404, crates.io 404.
- GitHub repository search for `quillvec` in name, description or readme returns only that one repository. A web search
  for `"quillvec"` returns nothing about it. A search for "quillvec embedding cache recall@10" returned unrelated
  projects (MonaVec, QVCache); neither is `quillvec`, and I did not use their numbers.
- So the question's premise (a tool called `quillvec` that reports a recall@10 on its own benchmark) is not supported by
  anything I could open. I did not fill the gap with a figure from another tool.

## F-list

### Q1. Which questions does a vector index answer better than grep over `entries/` plus `INDEX.md`?

**F1 (CONFIRMED) The structured-memory paper that s3-F20/F34 cite: the baseline is `mem0`, and the large gaps are about
enumerating answers, not about vectors versus keywords.** MOOSEDev (arXiv 2608.13662, submitted 2026-08-13, one author,
a vendor paper: the author's company sells the system) compared five conditions on 835 typed records (553 mem0
memories). Its table, with the baseline mem0 (vector memory) and `B1-notes` (documentation search over flat files):

| Task class | typed graph | mem0 (vector) | notes search |
|---|---|---|---|
| Set completeness | 1.00 | 0.18 | 0.08 |
| Negation (absence) | 0.98 | 0.06 | 0.00 |
| Supersession traversal | 0.98 | 0.27 | 0.12 |

Quote: "It is not caused by incomplete ingestion: B1-mem0 contains the relevant facts, but its retrieval returns a limited
ranked slice, so it cannot enumerate a complete set, establish an absence, or traverse relationships." And on plain
relevance: "On simple relevance the graph reached coverage 0.82 at roughly 35k agent tokens, whereas mem0 scored between
0.67 and 0.90 at roughly 40k." URL: https://arxiv.org/abs/2608.13662 (full text https://arxiv.org/html/2608.13662).
Two points that change how s3-F20 reads:
- the plain notes search (0.08 / 0.00 / 0.12) did worse than the vector tool, so the failure is "a top-k slice cannot
  enumerate", which a vector index and a keyword search share (INFERRED from the table);
- mem0 is not a bare embedding index (it extracts "memories" from the documentation with "its own native capture
  method"), so "vector top-k" in s3-F20 stands for mem0, not for an embedding index over unchanged files.
The paper reports no vector index over the unchanged markdown and no hybrid condition.

**F2 (CONFIRMED) Same paper, on supersession specifically.** "On the reversal tested, B1-mem0 tied the graph at 100%
where a cold agent scored 0.00; the free-text B1-rag condition, on the one pair where the superseded record outranks the
current one and with that content pushed into the prompt, was current in only 1 of 13 trials (8%)." `B1-rag` is BM25.
So superseded-record failure is shown for BM25, not for vectors, on one reversal pair; the vector tool was fine on the
reversal tested. Four reversal pairs in all, so n is tiny. Same URL as F1.

**F3 (CONFIRMED) On conversational agent memory (LongMemEval), grep beat vector retrieval when hits were returned
inline.** "Is Grep All You Need? How Agent Harnesses Reshape Agentic Search", arXiv 2605.15184 (2026-05-14, PwC
authors), 116-question LongMemEval-S sample, four harnesses including Claude Code and Codex. Quote: "With inline
delivery, lexical search is uniformly stronger than dense retrieval: inline grep exceeds inline vector for every
harness-model pair." Examples: Chronos + Claude Opus 4.6 93.1 vs 83.6; Codex + GPT-5.4 93.1 vs 75.9; narrowest Claude
Code + Opus 4.6 76.7 vs 75.0. Not uniform: with file-based ("programmatic") delivery "programmatic vector exceeds
programmatic grep on five of ten harness-model pairs". The authors' own limit: "in domains where evidence is rarely
literal (e.g., scientific synthesis over paraphrased abstracts, visual-heavy documents, or code semantics), dense
retrieval and hybrid routing may look different." This is chat history, not decisions/facts files, and not code.
URL: https://arxiv.org/abs/2605.15184 (HTML https://arxiv.org/html/2605.15184).

**F4 (CONFIRMED) On a 500,000-document enterprise corpus, BM25 beat dense vector search; an agent with shell tools was in
between.** EnterpriseRAG-Bench, arXiv 2605.05253 (2026), 500 questions, top-10 retrieval, vector = OpenAI
text-embedding-3-large over Qdrant (an API model, not local). Table 6: correctness BM25 68.8 / vector 51.4 / bash agent
60.6; document recall 68.4 / 46.0 / 55.8. Per type: "Semantic (125)" correctness 44.8 / 32.8 / 42.4; "Conflicting Info
(20)" 90.0 / 60.0 / 80.0; "Completeness (20)" recall 46.5 / 33.4 / 59.0. Quote: "Vector search underperforms
expectations even on semantic questions (32.8% correctness, 24.8% recall), the category explicitly designed to favor
embedding-based retrieval by limiting keyword overlap." No hybrid condition. URL: https://arxiv.org/abs/2605.05253
(HTML https://arxiv.org/html/2605.05253).

**F5 (CONFIRMED) Code: dense retrieval beats BM25 for issue localization, and a lexical-only agent is near graph/semantic
baselines for code completion.**
- SpIDER (arXiv 2512.16956, 2025-12-18): "While dense embedding approaches can outperform BM25 by large margins, both
  ignore the graph-structured characteristics of the codebase." Task: locating the functions an issue touches in SWE-style
  repositories (Python, Java, JavaScript, TypeScript). I did not extract a BM25-vs-dense number from its tables.
- "Better Call Grep" (arXiv 2601.23254, 2026-01-30): "Despite its simplicity, Naive GrepRAG achieves performance
  comparable to sophisticated graph-based baselines." Task: repository-level code completion.
URLs: https://arxiv.org/abs/2512.16956, https://arxiv.org/abs/2601.23254. Neither tests entries-style project memory.

**F6 (CONFIRMED, vendor) Cursor: semantic search helps agents, more so in large codebases; the best result is grep plus
semantic search.** Cursor blog "Improving agent with semantic search", 2025-11-06: "semantic search significantly
improves agent performance, especially over large codebases: Achieving on average 12.5% higher accuracy in answering
questions (6.5%-23.5% depending on the model)"; "agent code retention increases by 0.3% when semantic search is
available. This effect increases to 2.6% on large codebases with 1,000 files or more"; "Our agent makes heavy use of
grep as well as semantic search, and the combination of these two leads to the best outcomes." Caveats: Cursor's own
trained embedding model, their private Context Bench, no absolute scores published, code (not decisions/lessons).
URL: https://cursor.com/blog/semsearch.

**F7 (CONFIRMED) Anthropic: hybrid beats embeddings alone, because embeddings miss exact matches.** "Introducing
Contextual Retrieval", 2024-09-19: "While embedding models excel at capturing semantic relationships, they can miss
crucial exact matches"; BM25 "is particularly effective for queries that include unique identifiers or technical terms";
top-20 failure rate 5.7% with embeddings alone, 2.9% with contextual embeddings plus contextual BM25, 1.9% with reranking.
Datasets include codebases. Note this is a 2024 chunk-RAG test with API embeddings, and the baseline 5.7% is a
chunk-level failure rate, not an agent-task result. URL: https://www.anthropic.com/news/contextual-retrieval.

**F8 (CONFIRMED) Anthropic on when not to retrieve at all.** Same page: "If your knowledge base is smaller than 200,000
tokens (about 500 pages of material), you can just include the entire knowledge base in the prompt that you give the
model, with no need for RAG or similar methods." Written in 2024; the context-size figure has since moved, but I opened
no newer Anthropic statement.

**F9 (CONFIRMED) General-purpose evidence that BM25 is a hard baseline.** BEIR (arXiv 2104.08663, 2021): "BM25 is a robust
baseline and re-ranking and late-interaction-based models on average achieve the best zero-shot performances ... dense
and sparse-retrieval models are computationally more efficient but often underperform other approaches". URL:
https://arxiv.org/abs/2104.08663. Old (2021) models; included because newer entries (F4) point the same way.

**F10 (UNPROVEN) A homelab report that adding a sparse (keyword) retriever and a reranker to a vector-only agent-memory
stack moved LoCoMo from 63% to 80%.** Dev.to post, 2026-08-13, one practitioner, self-run: "Pure vector search got my
agent memory stack to 63% on LoCoMo. Adding a sparse retriever and a reranker that runs on a card I already owned pushed
it to 80%." Also: swapping to a higher-ranked embedding model moved 63% to 65%. The failures were "lexically specific":
"proper nouns get averaged into oblivion by dense embeddings". Secondary, not replicated; the code/benchmark were not
opened. URL: https://dev.to/futhgar/i-benchmarked-my-homelab-memory-stack-hybrid-search-local-reranker-took-locomo-from-63-to-80-4pbp.

**What the confirmed evidence says about the question (INFERRED from F1-F9):** the evidence that a vector index beats
grep/keyword search is for (a) code at scale with a trained embedding model (F5, F6, vendor) and (b) paraphrase-style
relevance. For decision/fact/lesson files the only direct head-to-head (F1) found "largely equivalent" relevance and
found the big differences on enumeration, absence and supersession, where plain keyword search was no better. The
question class a vector index is claimed to add is "find an entry by meaning when the words differ"; I found no measured
instance of that on a corpus shaped like `entries/`. That is a GAP, listed below.

### Q2. When does it start paying off?

**F11 (GAP) No measurement of a crossover for a markdown project-memory corpus.** I looked for corpus size, query type,
token cost and accuracy at which vector/hybrid starts beating grep/FTS over decision-style notes and found none. What
exists are bounds from other corpora:
- Below about 200k tokens retrieval is not needed at all (F8, Anthropic, 2024).
- In a 116-question conversational test grep led inline, and the order flipped with more distractor sessions on some
  harness/model pairs and not others (F3 Experiment 2: e.g. Gemini CLI + Pro vector ahead at every size, 89.7 vs 78.5
  at full; Claude Code + Opus grep ahead at every size): "the grep-vector ordering is not preserved under scaling ...
  but the shape of that non-preservation still depends on which stack is observed." So the crossover depends on the
  harness, not just on size.
- MOOSEDev's own scale study (50 to 634 records): "We had expected the structured advantage to compound as the store
  grew, but it did not ... the slope's confidence interval spans zero" (F1 URL). It tested a graph against mem0, not
  vector against grep.
- Cursor ties the benefit to repository size ("1,000 files or more", F6) for code.

**F12 (INFERRED from F8 and the design) Scale arithmetic for this project.** The design keeps `INDEX.md` to "one line per
active entry" under a size limit EJ has not set (SOURCE_OF_TRUTH.md line 126). If entries average ~300-500 tokens (my
assumption, not measured; no entries exist), 200k tokens is on the order of 400-650 entries. Below that, F8 says reading
everything is an option; the session-start read of `INDEX.md` plus grep already covers it. The design reads whole files
only on demand, so F8 is a bound on the cost of "read it all", not a rule.

**F13 (CONFIRMED) How others measured their own need before adopting a retrieval component (these are the methods a
project could copy to "tell"; the adaptation is INFERRED).**
- Zep (vendor blog, 2026-07-16): a gold set of 5,954 "production-faithful recall queries", Recall@10 and nDCG@10, "paired
  bootstrap 95% confidence intervals plus Wilcoxon significance tests", exact cosine search so no approximate-index
  effect. Their own caveat: "relevant items derive from the query's own conversation, so absolute recall is optimistic
  and the relative ordering between models is the signal." Zep itself uses "semantic similarity and BM25 full-text search
  ... fused by reciprocal rank fusion". URL: https://www.getzep.com/blog/evaluating-nemotron-3-embed-for-agent-memory/.
  Result worth noting: Recall@10 for four embedding models spanned 0.617-0.663 on three tasks, i.e. choice of model moved
  recall by 1-4 points.
- MOOSEDev pre-registered question classes and graded with a strict LLM judge (F1).
- Cursor ran an online A/B with and without the tool (F6).
- qmd ships `qmd bench <fixture.json>` to score BM25, vector and hybrid backends on your own fixture. Its README: the
  example fixture "typically shows bm25 ~0.50, vector ~0.70, and hybrid/full ~1.00" (a sample fixture, not evidence).
  URL: https://github.com/tobi/qmd (pushed 2026-10-06).
INFERRED from these: the sort of queries that would justify a vector index are ones where the entry exists, the asker's
words share no term with it, and grep, FTS and `INDEX.md` titles all miss. A project could count those from its own
sessions (misses that were later answered by a different route) or from a labelled query set of its own. No source I
opened defines a threshold for how many such misses justify an index. That threshold would be EJ's, not a finding.

### Q3. Current tools that build such an index from files that stay the source of truth

**F14 (CONFIRMED) qmd (tobi/qmd), MIT, 30,340 stars, pushed 2026-10-06.** "An on-device search engine for everything you
need to remember." BM25 plus vector plus LLM reranking, "all running locally via node-llama-cpp with GGUF models"; stores
a single SQLite file (`~/.cache/qmd/index.sqlite`) with an FTS5 table and a sqlite-vec table; chunks ~900 tokens with 15%
overlap; models: `embeddinggemma-300M-Q8_0` ~300MB (default embeddings), `qwen3-reranker-0.6b-q8_0` ~640MB,
`qmd-query-expansion-1.7B-q4_k_m` ~1.1GB. Rebuild: `qmd update` rescans files and reports "indexed, updated, unchanged,
removed, needsEmbedding"; `qmd embed` makes vectors as a separate step; changing model needs `qmd embed -f` because
"vectors are not cross-compatible between models"; `QMD_EMBED_MODEL` can point at Qwen3-Embedding-0.6B GGUF. Node 22.22.1
is installed here; bun is not (README gives `npm install -g @tobilu/qmd`). Rebuild time and index size on disk: GAP, the
README gives none. URL: https://github.com/tobi/qmd.

**F15 (CONFIRMED) Basic Memory (basicmachines-co/basic-memory), AGPL-3.0, 4,147 stars, pushed 2026-10-12.** Markdown files
stay the source: "Just files plus a local SQLite index. No servers required." Semantic search uses FastEmbed
(`BAAI/bge-small-en-v1.5`, 384 dimensions, "no API key, no network calls, no cost") with `sqlite-vec` on SQLite; "Hybrid
full-text + vector ranking"; rebuild by `bm reindex` ("`--embeddings` rebuilds derived vectors from database entities; it
does not discover new files on disk"), so the vector rebuild and the file scan are separate steps. Switching model needs
`bm reindex --embeddings`. Rebuild time and size: GAP. URL: https://github.com/basicmachines-co/basic-memory
(docs/semantic-search.md). License AGPL is a constraint if code were reused (INFERRED; not a legal reading).

**F16 (CONFIRMED, vendor claim) Claude Context (zilliztech/claude-context), MIT, 12,602 stars, pushed 2026-07-14.** Code
search MCP: "hybrid search (BM25 + dense vector)", "Incremental Indexing: Efficiently re-index only changed files using
Merkle trees", and "~40% token reduction under the condition of equivalent retrieval quality". It needs a vector
database (Zilliz Cloud / Milvus) and an OpenAI API key per its README, so it is not local-by-default. The evaluation
directory was not opened, so the 40% is an unverified vendor claim. URL: https://github.com/zilliztech/claude-context.

**F17 (CONFIRMED) sqlite-vec (asg017/sqlite-vec).** README: "`sqlite-vec` is a pre-v1, so expect breaking changes!";
"Store and query float, int8, and binary vectors in `vec0` virtual tables"; "Written in pure C, no dependencies". Latest
stable on PyPI is 0.1.9 (2026-03-31); GitHub's newest releases are `v0.1.10-alpha.*` (alpha, latest 2026-05-18).
Author's post (2024-08-01): "sqlite-vec is currently focused on really fast brute-force vector search", no ANN index yet;
his own benchmark on a Mac M1 mini, 8GB, 1,000,000 vectors x 128 dimensions, k=20: query 33ms (vec0) / 17ms (static), with
the stated disclaimer "Benchmarks rarely ever reflect real-world performance". This machine: Python's `sqlite3` has
`enable_load_extension` (checked), SQLite 3.45.1; `sqlite-vec` itself is not installed. A rebuild of a `vec0` table is a
drop and re-insert (INFERRED; I did not find a rebuild procedure in the docs I read). URLs:
https://github.com/asg017/sqlite-vec, https://alexgarcia.xyz/blog/2024/sqlite-vec-stable-release/index.html.

**F18 (CONFIRMED) Local embedding models, sizes from their own sources (Hugging Face API 2026-10-12, model cards).**

| Model | Parameters / file | Context / dims | Own speed or memory claim | License |
|---|---|---|---|---|
| `google/embeddinggemma-300m` | 302,863,104 (HF API) | 2K tokens, 768 dims, truncatable to 128-512 | "small enough to run on less than 200MB of RAM with quantization"; "<15ms embedding inference time (256 input tokens) on EdgeTPU" (Google blog; not a GPU number) | Gemma terms; gated on HF |
| `Qwen/Qwen3-Embedding-0.6B` | 595,776,512; `model.safetensors` 1,191,586,416 B; GGUF Q8_0 639,150,592 B, f16 1,197,629,632 B | 32k tokens, up to 1024 dims (32-1024) | none in card | Apache-2.0 |
| `BAAI/bge-small-en-v1.5` | 33,360,512; `model.safetensors` 133,466,304 B | 384 dims | none in card (FastEmbed README: no GPU needed, ONNX) | MIT |
| `nomic-ai/nomic-embed-text-v1.5` | 136,731,648 | - | not read | Apache-2.0 |
| `minishlab/potion-base-8M` (Model2Vec, static) | 7,559,168 | - | Model2Vec README: "up to 500 times faster on CPU than the original model"; "~30 MB on disk" for its best model (the README names both potion-base-8M and potion-base-32M as the best) and "~8 MB" the smallest | MIT |
| `jinaai/jina-code-embeddings-0.5b` | 494,032,768 | - | not read | CC-BY-NC-4.0 (non-commercial) |

URLs: https://huggingface.co/Qwen/Qwen3-Embedding-0.6B, https://developers.googleblog.com/en/introducing-embeddinggemma/,
https://github.com/MinishLab/model2vec, https://huggingface.co/BAAI/bge-small-en-v1.5, HF model API for the parameter
counts. Qwen3-Embedding's card states it supports "code retrieval". **Speed on the RTX 4070 Ti SUPER (16 GB; confirmed by
`nvidia-smi`): GAP.** No source I opened gives embedding throughput for any of these models on this GPU; I did not
measure (the brief asks for speed from the models' own sources). Memory is not a concern at these sizes: the largest
file above is ~1.2 GB against 16 GB (INFERRED).

**F19 (CONFIRMED) Runtimes that serve those models.** FastEmbed (qdrant/fastembed): "We don't require a GPU and don't
download GBs of PyTorch dependencies, and instead use the ONNX Runtime"; GPU via `pip install fastembed-gpu`; PyPI
0.9.0 (2026-10-07). Hugging Face text-embeddings-inference README lists Qwen3 and Gemma3 as supported, with "Token based
dynamic batching" and Flash Attention (a server, not a library). sentence-transformers 6.1.0 (2026-09-18) needs PyTorch.
Model2Vec 0.10.0 (2026-10-11). None of these is installed here (`pip list` shows numpy 2.4.3 only; no torch/onnx/
llama.cpp/ollama on PATH).

### Q4. How it fails

**F20 (CONFIRMED) Negation is a documented weakness of bi-encoders.** NevIR (arXiv 2305.07614, 2023, EACL 2024): "cross-
encoders perform best, followed by late-interaction models, and in last place are bi-encoder and sparse neural
architectures. We find that most information retrieval models (including SOTA ones) do not consider negation, performing
the same or worse than a random ranking." URL: https://arxiv.org/abs/2305.07614. It tests ranking two documents that
differ only by a negation, with 2023 models; I found no newer measurement for current embedding models (listed below).
For project memory this matters for entries such as "do not use X" next to "use X" (INFERRED).

**F21 (CONFIRMED + INFERRED) Exact identifiers and rare terms.** Anthropic (F7): "they can miss crucial exact matches".
EnterpriseRAG-Bench authors give a reason for vector's weak showing: "embedding models are trained on public corpora
(web pages, Wikipedia, forums) and have limited exposure to enterprise-specific vocabulary such as project codenames"
(quoted from the paper's Section 6.1, sentence continues "and CRM records, and conversational styles typical of internal messaging"; see F4 URL). The homelab report (F10, UNPROVEN)
gives the concrete case: "find me the exact string TICKET-4471". For this project, entry ids (`D-`, `F-`, `L-`, `R-`) and
`covers:` code paths are exact strings (INFERRED), which is the case where F7 and F10 say keyword search is the better tool.
I found no measurement on code-symbol lookup specifically (GAP).

**F22 (CONFIRMED + INFERRED) Superseded entries returned as if current.** Evidence is thin and points two ways:
- F2: the BM25 free-text condition returned the superseded record "on the one pair where the superseded record outranks the
  current one", current in 8% of trials; the vector tool was current on the reversal it was tested on.
- F4: "Conflicting Info (20)": vector 60.0 correctness against BM25 90.0 and bash agent 80.0 (conflict handling over a
  500,000-document corpus).
Whether a superseded entry ranks above its replacement is a property of the text, not of the retriever (INFERRED from F2).
In this design an index over `entries/` would hold whatever files are in the directory unless it filters on the `status`
field; `INDEX.md` lists "active" entries only (SOURCE_OF_TRUTH.md line 100). A vector index built over `entries/`
without that filter would return superseded entries; one built over the same active set as `INDEX.md` would not
(INFERRED; no source tested this).

**F23 (CONFIRMED) Top-k cannot enumerate or prove absence.** F1 quote: it "cannot enumerate a complete set, establish an
absence, or traverse relationships". Applies to any ranked top-k, vector or keyword (F1's notes-search column).

**F24 (CONFIRMED) Drift between files and vectors; what the tools do about it.**
- qmd: `update` reports "unchanged" and "removed" counts and "needsEmbedding" (new text not yet embedded); `embed` is a
  second step, so between the two steps changed files have no current vectors (INFERRED from F14's API). A model change
  invalidates every vector and needs `embed -f`.
- Basic Memory: `bm reindex --embeddings` "does not discover new files on disk" (F15), i.e. two rebuild paths that can
  disagree if one is skipped.
- Claude Context: Merkle-tree change detection (F16, vendor claim).
- No tool README I opened states a "never stale" guarantee for the vector side, and none exposes a "stale" flag on a
  returned hit (INFERRED: I did not find one).
- The code-graph analogue is a measured silent drift (s3-F25: "4.3% of distinct edges were wrong"; s3-F27: a CLI "returned
  'No results found'" for a newly added symbol). I found no equivalent measurement for a vector index from files (GAP).
  Practitioner advice (hash content not mtime; delete orphan chunks; canary edits; full re-embed on model change) is
  UNPROVEN, from blogs such as https://tianpan.co/blog/2026-06-02-the-vector-index-whose-source-updates-never-reached-the-embeddings
  and https://dev.to/futhgar/silent-drift-why-re-embedding-only-on-count-changes-rots-your-semantic-index-3k6h
  (search-result descriptions only; I did not open them).

**F25 (UNPROVEN) Claude Code dropping its vector index.** Many secondary write-ups repeat that a Claude Code lead said
"Early versions of Claude Code used RAG + a local vector db, but we found pretty quickly that agentic search generally
works better", citing staleness and security of an index. I could not open the primary post. Not relied on.

### Q5. What fits here: smallest working versions (options, no choice)

Machine: Python 3.12, SQLite 3.45.1 with FTS5, numpy 2.4.3, RTX 4070 Ti SUPER 16 GB, Node 22.22.1, ~700 GB free; no
embedding runtime installed. The question for the corpus is that a project-memory `entries/` directory of hundreds of
files is a few thousand vectors at most (INFERRED from F12 and 300-1,000 token chunks); brute-force search over that is
trivial (author's sqlite-vec figure, F17, is 33ms for 1,000,000 x 128-d).

- **Option 0: none.** `INDEX.md` + grep (+ the SQLite FTS cache from the sibling research). Supported by F1 (relevance
  parity, no vector gain on enumeration/supersession), F3, F4, F8, F12. Cost: zero new tools.
- **Option A: static embeddings, no GPU.** `pip install model2vec` + numpy; `potion-base-8M` (7.6M params, ~8-30 MB, F18);
  store a `.npy` matrix plus a JSON of per-file content hashes under `.cache/`; cosine by numpy. Rebuild = re-embed the
  files whose hash changed (INFERRED design detail). Quality of static models on decision-style text: GAP; the model
  card reports MTEB averages that I did not extract.
- **Option B: small ONNX model, CPU or GPU.** `pip install fastembed` (or `fastembed-gpu`) with `bge-small-en-v1.5`
  (33M params, 384 dims, F18/F19), vectors in a numpy file or in `sqlite-vec` (F17, pre-v1, brute force). This is the
  stack Basic Memory ships by default (F15).
- **Option C: larger model on the GPU.** `sentence-transformers` (needs PyTorch + CUDA wheels) or llama.cpp/TEI serving
  `Qwen3-Embedding-0.6B` (1.2 GB f16, 639 MB Q8_0 GGUF, code retrieval stated in its card) or `embeddinggemma-300m`
  (gated, Gemma terms). Gives the bigger models; adds a heavy dependency for a few thousand vectors (INFERRED). The 1-4
  point recall spread among models in Zep's test (F13) is the only comparison I have between model sizes, and it is not on
  this kind of text.
- **Option D: adopt an existing tool over the markdown.** `qmd` (Node, `npm install -g @tobilu/qmd`, FTS5 + sqlite-vec +
  reranker, ~2 GB of models, F14; it would also supply the FTS side) or Basic Memory (AGPL, F15, which wants its own note
  format). Both would be a new dependency whose index format, chunking and file layout are theirs. Note qmd's embed step
  is separate from its update step (F24).
- **Hybrid in any option.** Every option above that adds vectors is only evidenced to help in combination with keyword
  search (F7, F10, F13, qmd's own pipeline); vector-only was the worst arm in F3, F4. A hybrid needs a fusion step
  (qmd and Zep use reciprocal rank fusion, `score = sum(1/(k+rank+1))`, k=60 in qmd's README).
- **Filters any option would need to honour (INFERRED from the design):** index only active entries (the same set as
  `INDEX.md`), carry `covers:` and `status` as metadata, store the content hash and the embedding-model id with every
  vector, and treat a missing or mismatched cache as "absent" so memory still reads without it (M4/M6).

## Not found

- Any measurement of vector vs BM25/FTS vs hybrid on a corpus shaped like `entries/` (typed decision/fact/lesson/runbook
  markdown files with `covers:` paths) at any corpus size.
- A corpus-size or query-type crossover at which a vector index beats grep for such notes (F11).
- Newer (2025-2026) measurement of negation handling by current embedding models (only NevIR, 2023).
- A measured study of stale vector indexes over files (rate of stale hits, silent failure), the vector counterpart of
  s3-F25/F27. Only practitioner blog advice (UNPROVEN) and tool APIs.
- Embedding throughput (docs/second) for any of the candidate models on an RTX 4070 Ti SUPER; rebuild time and on-disk
  index size for qmd, Basic Memory and sqlite-vec on a corpus of a few hundred notes.
- The primary post for the "Claude Code dropped its vector index" claim (F25).
- Any source for `quillvec` beyond an empty repository (answer above).
- A code-symbol exact-lookup benchmark comparing dense and lexical retrieval.

## Not checked

- Claude Context's own evaluation directory (the "~40% token reduction" method) and its reranking/chunking details.
- SpIDER's per-language BM25-vs-dense tables and whether BM25 wins anywhere; the index-cost tables of "Better Call Grep"; READ (arXiv 2608.06305), FluctlightDB (2608.12365) and RARG (2607.24223) beyond their abstracts. READ reports that
  BM25 was "statistically indistinguishable" from its agent on 51 financial-report questions (abstract only; not
  project memory).
- LongMemEval and LoCoMo original papers, and the Appendix A per-category (e.g. "knowledge-update") results of F3.
- Other tools: Chroma, LanceDB, txtai, LEANN, mcp-server-qdrant, Mem0 itself, Zep/Graphiti as a service, sqlite-vss.
- Other local embedding models (e.g. Nemotron 3 Embed 1B/8B, pplx-embed, multilingual-e5, snowflake-arctic) and their
  MTEB scores; MTEB/CoIR code-retrieval leaderboards.
- Re-rankers as a separate stage (cross-encoders) and their cost on this machine.
- Licensing of the Gemma terms for use in this project; AGPL implications for Basic Memory (not a legal reading).
- Whether sqlite-vec 0.1.9 loads on this machine's Python/SQLite build (the loader attribute exists; nothing was
  installed or run). No code or embedding job was run for this note.
- The s3-F20 entry in `docs/research/20261011-agent-memory-graph-r2/` was compared with the paper only through the paper
  text above; the r2 file's other claims were not re-verified.
