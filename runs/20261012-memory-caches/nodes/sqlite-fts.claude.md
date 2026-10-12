# SQLite full-text index as a derived cache — research findings

Run `20261012-memory-caches`, store: SQLite FTS5 index over `project-memory/entries/` and related markdown.
Researcher: claude (`claude-sonnet-5-5`), 2026-10-12. Research only; nothing built, nothing chosen.

**How the sources were read.** Pages were opened with WebFetch, which returns a model-written extract of the page, not
raw HTML. A quote below is the text that tool returned as the page's wording. I did not diff it against the raw page.
`CONFIRMED` therefore means "opened, and the extract quoted the page"; it does not mean byte-checked. Dates are the
page's own publication or merge date; sqlite.org and the qmd and sqlite-memory READMEs show none. The "Dated" column
for those says so.

**Already known, used by id:** s3-F16 (graph beat BM25 on hidden-dependency tasks), s3-F19 (BM25 inside a structural
slice), s3-F20/F34 (MOOSEDev: structured question types only), s3-F25/F27 (silent drift of a live index), from
`docs/research/20261011-agent-memory-graph-r2/INDEX.md`. RECOMMENDATION M6 (SQLite derived, absence must not block
reading), CP1 out of scope.

## Answer to the planted question

**Question:** "What default FTS5 tokenizer does the `hollowfern` markdown indexer use, according to its docs?"

**Answer: GAP. I found no `hollowfern` markdown indexer, so there are no docs to answer from.**

What I checked (all on 2026-10-12):
- Two web searches: `hollowfern markdown indexer FTS5 tokenizer` and `"hollowfern" github markdown index`; neither returned any project of that name. The bare search `hollowfern` returned only holly-fern plant pages.
- PyPI `pypi.org/pypi/hollowfern/json` -> HTTP 404; npm `registry.npmjs.org/hollowfern` -> 404; crates.io `api/v1/crates/hollowfern` -> 404.
- `gh api users/hollowfern`: a GitHub account exists (created 2026-01-08) with two repos, `Astra-Grid` ("Fork of grid modeler with new features and fixes.") and `CMBE` ("A library with ready-made functions combo,repeat,hold,sequence."). Neither is a markdown indexer. `gh search repos hollowfern` also lists `lansingalong/hollowfern-game` (no description). `gh search code hollowfern` found only hostnames (`*.hollowfern.sbs`) in a Telegram proxy list.
- The name appears in this repo only in `runs/20261012-memory-caches/state.md` line 71, where it is listed as a name that does not exist.

I did not read the code of `Hollowfern/Astra-Grid`, `Hollowfern/CMBE` or `lansingalong/hollowfern-game`; their one-line descriptions say they are not markdown indexers.

What I can say that is true, and is not an answer about hollowfern: **SQLite's own FTS5 default tokenizer is `unicode61`** (F2). Any tool that creates an FTS5 table without a `tokenize=` option gets it. That says nothing about a tool I could not find.

## Findings

### 1. Questions the store answers (brief item 1)

**F1 — CONFIRMED (stated rationale, not a measurement).** The `monorepo-agents-harness` maintainers list what grep cannot do for their knowledge folder, which is the closest thing found to an argued case for FTS5 over grep for agent memory.
URL: https://github.com/atayahmet/monorepo-agents-harness/issues/25 (opened 2026-10-07, closed 2026-10-08).
Quotes: `"grep returns unranked matches."`; the FTS5 table is described as `"FTS5 virtual table over title + body (BM25 ranking, `snippet()`)."`; the corpus was `"already ~1.4k files in one adopter repo."` The same extract paraphrases the other complaints: agents open whole files to judge relevance, the fallback scans every artifact tree and grows with each task, and backlink and orphan-page queries need ad-hoc shell pipelines.
Limit: it is a feature proposal. It reports no accuracy or token number for FTS5 against grep.

**F2 — CONFIRMED.** FTS5's documented behaviour that matters for this project.
URL: https://sqlite.org/fts5.html (read 2026-10-12, no page date).
Quotes: `"The unicode61 tokenizer, based on the Unicode 6.1 standard. This is the default."`; `"The better the match, the numerically smaller the value returned."` (bm25); `"The contents of columns qualified with the UNINDEXED column option are not added to the FTS index."`
So header fields such as `kind`, `status`, `covers` can ride along as `UNINDEXED` columns or sit in a plain table next to the FTS table.

**F3 — INFERRED from F1, F2 and my measurement F13.** Which questions an agent asks, split by what the store adds over `grep` plus `INDEX.md`:
- *Ranked free-text recall* ("which entries talk about retry budget"): FTS5 adds an order (BM25) and snippets. grep returns an unranked list. `INDEX.md` (one line per active entry) already covers a title-level scan.
- *Header-field queries* ("every active decision whose `covers` includes path X", "what supersedes Y"): a SQL `WHERE` over a table of header fields answers these. grep over `entries/` answers them with a pipeline of greps or a short script (F13 shows both returning the same hits). No source found measures an agent doing either.
- *Backlinks, orphans, broken `supersedes` links*: needs a link table or a script; FTS5 itself does not provide it (the harness in F5 builds a separate `links` table).
- *Semantic ("by meaning") questions*: FTS5 does not answer these; that is the vector cache's question, not this one.

### 2. When it pays off (brief item 2)

**F4 — CONFIRMED.** The one controlled scaling measurement found for BM25 against an agent using grep over files. The "File-System Agent" had `list_dir`, `grep` (fixed string, up to 30 matching paths) and `read_doc` (first 8,000 characters), 80 LLM calls per question; the benchmark is a general RAG corpus, not code or memory entries.
URL: https://arxiv.org/abs/2607.26497 and https://arxiv.org/html/2607.26497v3 ("BM25 Wins at Scale", submitted 2026-07-29, v3 2026-07-31).
Quotes: `"Around 10 million corpus tokens, BM25 overtakes it and leads at every larger shared tier"`; `"its sequential exploration costs 39 times more query tokens at the bedrock."` Numbers from the extract of the HTML: smallest tier 1,144 documents and 1.7M corpus tokens; tokens per question at that tier BM25 5.8K against File-System Agent 226K; at full corpus 5.8K against 895K (agent figure includes retries); BM25 leads "with a margin near 20 points at full scale." Also: the agent leads "at the smallest shared tiers."
Limits: the extract gave the abstract's "roughly 10 million" and the smallest tier, not a per-tier table. The File-System Agent's grep returns paths only, not lines, which is weaker than `rg` with context. This is one paper, preprint.

**F5 — INFERRED from F4 and F13.** Where this project sits against that crossover. The design says an entry is "the claim in one or two sentences, then Why:, then How to apply:", so about 1 KB each. My synthetic entries of that shape came to 1.06 MB per 1,000 entries (F13). At an assumed 4 characters per token (my assumption, not measured) that is about 0.27M tokens per 1,000 entries, so the 10M-token crossover in F4 would be near 37,000 entries, and even the 1.7M-token smallest tier in F4 would be near 6,000 entries. `project-memory/` does not exist yet in this repo (checked), so the real corpus size is unknown. The only count available: `docs/` and `runs/` hold 364 markdown files today. **No measurement exists of when FTS5 or BM25 beats grep for an agent on a corpus of a few hundred to a few thousand short entries.** That is a GAP, not a finding.

**F6 — CONFIRMED, and it cuts the other way.** Grep matched or beat vector retrieval in a controlled agent study.
URL: https://arxiv.org/abs/2605.15184 (submitted 2026-05-14), HTML https://arxiv.org/html/2605.15184v1.
Quotes: `"inline grep exceeds inline vector for every harness–model pair"` (Sec. 4.1.3); `"We do not claim that grep “beats” vector in general."`; `"Lexical tools may be disproportionately helpful here because answers often license on verbatim spans."` Example cells from its Table 1: Claude Opus 4.6 in Claude Code, inline grep 76.7 against inline vector 75.0; GPT-5.4 in Codex CLI 93.1 against 75.9.
Limits: LongMemEval conversational QA (116 questions), not code memory. It compares grep with vector, not with BM25. The extract reported no token or cost figures. Relevant here mainly to the vector cache; for the FTS store it shows grep is a strong baseline.

**F7 — CONFIRMED (vendor's own small benchmark).** A grep baseline recalled almost everything but was less precise than a hybrid index.
URL: https://github.com/rohitg00/agentmemory/blob/main/docs/benchmarks/2026-05-20-coding-agent-life-v1.md (2026-05-20).
Quotes: `"grep baseline: R@5 = 0.967, P@5 = 0.227 — missed one gold session in one multi-gold question."`; `"The benchmark is small (15 questions) and gold-sparse."` Hybrid got R@5 1.000 and P@5 0.240; the author says P@5 "is at the math ceiling for this dataset."
Limits: 15 fictional sessions, 15 queries, author's own project. A web-search summary of this page gave P@5 as 0.267; the page says 0.227, and I use the page. The page's own caveat says precision cannot separate the adapters.

**F8 — UNPROVEN.** Claude Code's own default is grep-style search, not an index (commonly reported). I did not open a primary source for it, so it is not used above.

### 3. Current tools that keep markdown as the source and build a SQLite index (brief item 3)

All of these are 2026; none is measured on a corpus like ours. Rebuild time and size are listed only where a source gave them; the local numbers are in F13.

**F9 — CONFIRMED. `monorepo-agents-harness` `kb-index.sh`.** Closest match to the brief: full rebuild, gitignored, grep fallback.
URLs: https://github.com/atayahmet/monorepo-agents-harness/issues/25 (2026-10-07) and https://github.com/atayahmet/monorepo-agents-harness/pull/26 (merged 2026-10-08, commit `6a22b7e`, VERSION 0.4.0-rc.13).
Quotes: `"Rebuild in full every time."`; `"`query` compares the index build time with the newest source mtime and rebuilds first if the index is stale."`; `"A stale index is worse than no index."`; if `sqlite3` is missing or lacks FTS5 it should `"print one warning and fall back to the current grep path."`; rebuild `"finishes in under a second"` at about 1.4k files. PR: `"a deterministic, self-healing SQLite FTS5 index over `knowledge/**/*.md`"`, built into a temp file then renamed over `knowledge/.index.sqlite`; derived columns `kind`, `workspace`, `task_slug`, `date` come from page shapes, not frontmatter. Tests: 38/38; removing self-heal caused 2 failures and removing atomic publish caused 4.
Local: yes, `sqlite3` CLI and shell. Tokenizer: not named (so FTS5 default). Size on disk: not stated.

**F10 — CONFIRMED. Scott Spence's `node:sqlite` + FTS5 markdown tool** (and its "wiki0" successor).
URL: https://scottspence.com/posts/give-coding-agents-your-project-docs-with-node-sqlite-and-fts5 (2026-09-17).
Quotes: `"One chunk per heading, so results point at a section, not a whole file."`; the index command starts with `db.exec('DELETE FROM chunks')` and reinserts everything; `"with a SQLite index that can be rebuilt any time for search, backlinks and facts."`; facts are `"decisions, requirements, risks and assumptions so they could be queried on their own."` Numbers: about 260 posts as 2,647 chunks in under half a second including Node startup; search about 50 ms; in a real project docs grew from 65 to 291 and agents called the CLI 1,122 times across 327 sessions. FTS5 table made with no tokenizer option (default). Staleness: not discussed; full rebuild each run. Index size: not given. No comparison with grep is made in the post.

**F11 — CONFIRMED. memweave** (Python; hybrid BM25 + optional vectors).
URL: https://towardsdatascience.com/memweave-zero-infra-ai-agent-memory-with-markdown-and-sqlite-no-vector-database-required/ (2026-04-16, by its author).
Quotes: `"The database is always a derived cache — if you delete it, memweave rebuilds it from the files."`; `"losing the database is not data loss. Losing the files is."`; `"BM25 catches exact matches — error codes, config values, proper names"`. Change detection: SHA-256 on files and chunks. Default merge weight 0.7 vector, 0.3 BM25. No size, rebuild time, latency or benchmark number is given.

**F12 — CONFIRMED (partly). Other tools, one line each.**
- `ai-memory` (Rust): `"Plain markdown on disk as source of truth. SQLite is just a derived index."`; `"Persistent index in SQLite + FTS5. Native. No reindex on every restart."`; author calls it beta, a few weeks in personal use. Its comparison target `agentmemory` reportedly pays `"~5 minutes rebuilding from scratch"` on restart and slowed at about 10K observations. https://akitaonrails.com/en/2026/05/23/i-built-memory-system-for-coding-agents-ai-memory/ (2026-05-23). The 5-minute figure is the author's report about another tool.
- `sqliteai/sqlite-memory`: `"Computes a hash of the content. If the same content was already indexed, it is skipped entirely."`; changed file: `"the old entry (chunks, embeddings, FTS) is atomically replaced."` Search needs embeddings (a local GGUF model or a remote key), so it is not FTS-only. No size, time or benchmark number; no page date. https://github.com/sqliteai/sqlite-memory
- `qmd` (Node): FTS5 index `documents_fts`, vectors in sqlite-vec, default index at `~/.cache/qmd/index.sqlite`, `qmd update` re-indexes, `qmd search` is `"BM25 full-text search only"`; vector, rerank and query-expansion models are about 300 MB, 640 MB and 1.1 GB. Rebuild time and size not stated; BM25-only offline use not confirmed from the page. Its fixture "typically shows" bm25 about 0.50, vector about 0.70, hybrid about 1.00, on the repo's own example fixture. https://github.com/tobi/qmd (no date shown).
- Basic Memory: `"all knowledge is represented in standard Markdown files and the database serves as a secondary index."`; the page names neither SQLite nor FTS5 and does not cover rebuild. https://docs.basicmemory.com/reference/technical-information (sample timestamps only, no page date). Search results elsewhere call the database SQLite (UNPROVEN, not opened).
- `metafunctor` "MCP pattern" post (files as ground truth, read-only FTS5 cache): **UNPROVEN**; the page returned HTTP 503 twice, so I only have a search-engine summary of it. https://metafunctor.com/post/2026-03-20-the-mcp-pattern/ (URL dated 2026-03-20 by its path).

**F13 — MEASURED HERE (my own script; not independent evidence).** A synthetic corpus (random words, entries shaped like the design: frontmatter with `id`, `kind`, `status`, `covers`, `superseded_by`, then about 1 KB body), one run each, on this machine (Python 3.12, SQLite 3.45.1, WSL2). Script: `/tmp/claude-1000/-home-smoke01-dev-ancient-games/343bf18f-e2d9-4dcf-8db5-0ed3524f59db/scratchpad/bench/bench.py`. Full rebuild = read every file, parse frontmatter, insert into one FTS5 table plus one header table.

| entries | markdown | index file | full rebuild | "active decision covering path X": python script / grep chain / SQL | one-word search: grep -rli / FTS5 top 10 |
|---|---|---|---|---|---|
| 100 | 0.1 MB | 0.3 MB | 0.03 s | 0.001 / 0.005 / 0.0002 s | 0.002 / 0.0006 s |
| 1,000 | 1.1 MB | 2.3 MB | 0.08 s | 0.011 / 0.009 / 0.0002 s | 0.005 / 0.0002 s |
| 10,000 | 10.6 MB | 21.9 MB | 0.53 s | 0.104 / 0.060 / 0.0008 s | 0.038 / 0.0006 s |
| 50,000 | 53.2 MB | 110.3 MB | 2.57 s | 0.405 / 0.148 / 0.0031 s | invalid (see below) |

What it does and does not show. At every size the grep route answers in well under half a second, so **latency is not a reason for a cache at this scale**; the index is about twice the markdown size. The 50,000-entry grep timing printed a negative number (the WSL clock moved), so I discard it. For the first three rows the structured query matched zero entries (the random path did not occur), so those timings are a full scan with no hits. The python script and the SQL returned the same count only where hits existed (4 and 4 at 50,000). Token cost to the agent is the real axis and this test does not measure it: it does not run an agent. The gain F4 reports is on tokens and accuracy, not wall-clock.

### 4. How it fails (brief item 4)

**F14 — CONFIRMED.** SQLite itself warns about an FTS5 index drifting from its source, and gives a repair.
URL: https://sqlite.org/fts5.html (no page date). Quote: the `rebuild` command `"first deletes the entire full-text index, then rebuilds it based on the contents of the table"`; `integrity-check` fails with `SQLITE_CORRUPT_VTAB` on discrepancies. The extract also says keeping an external-content table in step with its source table is the user's job.
Limit, INFERRED: `integrity-check` compares the index with the table it indexes. It does not compare that table with the markdown files on disk. I found no SQLite feature that does, so file drift must be caught by the tool (F15). Not tested here.

**F15 — CONFIRMED (the mechanisms in use).** How the tools above detect or prevent drift from the files:
- mtime comparison on every query, rebuild first if stale, atomic temp-file-then-rename publish (F9, quotes above).
- Full delete-and-reinsert on every index run, so drift lasts only until the next run (F10).
- SHA-256 per file and chunk, unchanged ones skipped (F11; and sqlite-memory in F12).
- A grep fallback if the index or FTS5 is missing (F9). This is the same property as M6, "its absence must not prevent reading memory."
Not found: any of these tools reporting a measured stale-answer rate. The only measured silent index drift in the record is the code graph, not FTS (s3-F25, s3-F27). The failure class is the same (a derived index that is not rebuilt when files change). Nothing shows FTS5 over markdown is prone to it.

**F16 — MEASURED HERE (small test, `python3` stdlib `sqlite3`, SQLite 3.45.1).** Two query-time traps with the default tokenizer, on a row containing `D-0012 covers src/auth/token_store.py and the retry_budget setting`:
- Unquoted `D-0012` raises `no such column: 0012` (a loud error; the `-` is read as a column filter). Quoted `"D-0012"` matches. The same under `porter` and `trigram`.
- With the tokenizer changed to `unicode61 tokenchars '-_/.'` (a plausible attempt to keep ids and paths whole), the queries `token_store`, `retry`, `budget` and `auth` returned **0 rows, silently**; the quoted full path still matched. `trigram` matched every query tried. The default matched `token_store`, `retry`, `budget`, `auth` and `"auth/token"`.
So a wrong tokenizer choice yields a wrong zero rather than an error. I tried only these 8 queries and 4 tokenizers on one row.

**F17 — INFERRED from F1 and F10.** Result granularity. Chunking by heading (F10) returns a section; one-file-per-entry (the design) could index one row per file. Which is right is not settled by any source found.

**F18 — INFERRED from s3-F20/F34 and F6.** Where the evidence says a richer store helps and where it does not: MOOSEDev's advantage is on supersession and set questions, with relevance recall and token cost "largely equivalent" (s3-F34); a lexical store is not shown to win on relevance either. So for this project the case, if any, rests on the header-field questions in F3, not on search quality.

### 5. What fits here (brief item 5) — options, no choice

The machine has Python 3.12 and SQLite 3.45.1 with FTS5 (verified 2026-10-12), `rg` and `grep`. Nothing to install.

- **Option A — no cache.** `INDEX.md` plus `rg` over `entries/`, and a short stdlib Python script that reads frontmatter for the structured questions (F13 shows 0.1 s at 10,000 entries). Cost: no ranking, no snippets.
- **Option B — smallest FTS cache.** One stdlib `sqlite3` script: full rebuild into a temp file, `os.replace` over `project-memory/.cache/index.sqlite`; one FTS5 table (default tokenizer, one row per entry file, header fields as `UNINDEXED` columns) and optionally a header-fields table; rebuild when the newest file mtime is newer than the index, as in F9; fall back to `rg` if the file or FTS5 is missing. Measured rebuild 0.53 s and 22 MB at 10,000 synthetic entries (F13); the design's M6 holds because absence changes nothing for readers.
- **Option C — B plus link table.** Adds `depends_on` / `supersedes` / `superseded_by` rows for backlink, orphan and broken-link queries (as the harness `links` command in F9). This is the structured-query use; the drift-check script named in the design as "not decided" could read it, but that is a design matter, not found here.
- **Choices a design must still make** (listed, not decided): tokenizer (F16), row grain (F17), staleness test (mtime as in F9, or hash as in F11), who triggers a rebuild, whether query and rebuild share one command (F9 does).

## Not found

- Any docs, repo or package for a `hollowfern` markdown indexer, and therefore its default tokenizer (planted question: GAP).
- Any measurement of FTS5 or BM25 against grep for an agent working on a small (hundreds to a few thousand) corpus of short memory entries, on accuracy or tokens.
- Any measurement of an agent answering header-field or supersession questions with SQL against with grep or a script over frontmatter.
- A measured stale-answer or drift rate for any FTS5-over-markdown tool.
- Index size and rebuild time in the published sources, apart from F9 ("under a second" at about 1.4k files) and F10 (under half a second at 2,647 chunks); no source gave an on-disk size.
- A primary source for the claim that Claude Code's default search is grep without an index (F8).

## Not checked

- The raw page text of any cited page (all reads went through WebFetch extracts); the full text of "BM25 Wins at Scale" beyond the extracts, and its per-tier table.
- The last 71,799 characters of the FTS5 reference page (read to character 100,000 of 171,799), which would hold the details of `trigram`, `porter`, contentless tables and `detail=`.
- `metafunctor` post (HTTP 503), sqlite-memory's code, qmd's source, Basic Memory's code and its FTS usage.
- SQLite FTS5 tools outside the markdown-agent-memory space (for example Obsidian or static-site search), and tools older than 2025.
- Actual `grep` or `rg` token cost to an agent (output size returned into context) against an FTS5 `snippet()` result; not measured.
- Whether Windows or macOS builds of SQLite ship FTS5 (irrelevant on this machine).
- The vector index and the code graph (other nodes' stores).
