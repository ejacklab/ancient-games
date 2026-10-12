I'll start by reading the local context files that the brief points to.
Now the code-graph specific local files and the cited prior findings.
Let me read the code graph implementation details and delegate local research in parallel.
Now web research. Let me check network access and hunt for `tarnline`.
`tarnline` appears to be a planted trap. Let me confirm from the run folder.
Confirmed planted trap. Now the substantive research — opening primary sources.
Primary sources for other tools and for the git-vs-graph question.
One read-only local measurement of the git-based check on this repo, to have a real number.
All research done. Here is the report.

---

# Research — the code graph as a `project-memory/.cache/` storeRun `20261012-memory-caches`, store 2 of 3. Research only; nothing built, nothing written.

**Scope note.** Everything below is about a *derived, gitignored* cache rebuilt from files that stay the source of truth (`SOURCE_OF_TRUTH.md:104`, RECOMMENDATION M4/M6). I treat "is it needed at all" as the first question, per the brief.

---

## 0. The planted question first: `tarnline`

**F1 — GAP — `tarnline` does not exist. No language list can be given.**

Searched, all on 2026-10-12:

| Where | Query | Result |
|---|---|---|
| GitHub repo search | `tarnline`, `tarnline in:name`, `tarnline+code+graph`, `tarnline+cli` | `total_count: 0` on every variant |
| PyPI | `https://pypi.org/pypi/tarnline/json` | HTTP 404 |
| npm | `https://registry.npmjs.org/tarnline` | HTTP 404 |
| GitHub REST | `api.github.com/repos/colbymchenry/tarnline` | HTTP 404 |
| Web (DuckDuckGo) | `tarnline code graph cli`, `"tarnline"` (exact phrase) | 10 results returned, **zero** naming `tarnline`; the space is occupied by `colbymchenry/codegraph`, `al1-nasir/codegraph-cli`, `lib.rs/crates/code-graph-cli` |
| Local disk | `grep -rin tarnline` over the repo and `~/.claude`, `~/.agents` | only `runs/20261012-memory-caches/` itself (`launch-opencode.sh:6`, the brief) |

**Answer to "Which languages does the `tarnline` code-graph CLI support, according to its README?":** it has no README, because there is no such CLI at any registry or index I can reach. Any language list would be invented. The nearest real tools, in case the name was garbled, are **codegraph** (F2) and **Serena** (F11).

Corroboration *about the brief, not about the world*: `runs/20261012-memory-caches/state.md:71` states that each brief carries "one planted question about a tool that does not exist (`hollowfern`, `quillvec`, `tarnline`); the right answer is not-found."

---

## 1. The questions it answers — better than grep over `entries/` + `INDEX.md`

The honest answer: **almost none, for the memory corpus.** The code-graph evidence base is about *source code*, and `project-memory/` is *markdown*.

**F2 — CONFIRMED — codegraph indexes 24 language rows by file extension; Markdown is not one of them.**
<https://colbymchenry.github.io/codegraph/reference/languages/> (retrieved 2026-10-12; the page carries no visible date — a GAP on its revision date, see §Not found).

> "Language support is automatic from the file extension — there's nothing to configure."

Rows: TypeScript, JavaScript, Python, Go, Rust, Java, C#, PHP, Ruby, C, C++, Objective-C (*Partial support*), Swift, Kotlin, Scala, Dart, Svelte, Vue, Astro, Liquid, Pascal/Delphi, Lua, R, Luau. The README's language assets additionally include ArkTS, so the true count is ≥24 and the two pages disagree.

**F3 — CONFIRMED — what gets into the index is code, by definition.**
<https://colbymchenry.github.io/codegraph/guides/indexing/> (retrieved 2026-10-12)

> "Every file whose extension maps to a supported language, minus dependency/build directories excluded by default (node_modules, vendor, dist, …), anything your .gitignore excludes, and files over 1 MB."

**F14 — INFERRED — the benchmark evidence does not transfer to this store.** Derived from F2, F3, F7, s3-F29, s3-F31. Every measured graph-vs-grep win below is on source code. `project-memory/entries/*.md`, `INDEX.md` and `covers:` lists are markdown. So for the questions an agent actually asks this cache — *"what do we already know about `journal.py`?"*, *"which decision covers the paths I am about to edit?"*, *"what did we decide about X and why?"* — a code graph either does not apply or adds nothing over `grep -rl` plus `INDEX.md`, because `covers:` is **already an explicit, hand-maintained index** of entry→path (`SOURCE_OF_TRUTH.md:50`). You built the graph by hand, in the entries.

**F15 — CONFIRMED (cited) — where the graph demonstrably loses to plain reading.** s3-F29 (arXiv 2603.27277), already verified in r2:

> "The Explorer retains an advantage for full source context (16/31 languages) and exhaustive call-site grep (10/31)—queries requiring line-level code that the graph intentionally does not store. The weakest MCP result is macro-heavy C (0.58 vs. 1.00), where macros are not represented in the AST."

s3-F31 (reported) gives the small-repo threshold and the churn hazard:

> "codebases that generate classes or functions at runtime … produce AST symbols that do not reflect runtime structure; PageRank over those symbols misleads rather than orients."
> "In a monorepo with thousands of commits per day, the parsed AST can be stale within minutes; Claude Code's on-demand agentic search is a better fit because it queries the live filesystem."

**F17 — INFERRED — the one graph-shaped question that memory actually asks is a *change* question, not a *lookup* question.** "What does this edit touch?", "what else did we decide about these paths?", "is this entry's code still what the entry says?" That is the code graph's home turf — and it is exactly the question the design already assigns to the background subagent (`SOURCE_OF_TRUTH.md:70-73`), not to the model-free script on line 75. §6 works this through.

**Verdict on Q1.** Grep + `INDEX.md` + `covers:` already answers the lookup questions; the graph's unique capability sits on the model-assigned side of the line, not on the cache's side. See §6.

---

## 2. When it pays off — measured evidence only

**F7 — CONFIRMED — codegraph's own benchmark.** <https://github.com/colbymchenry/codegraph> README (last commit to `README.md` 2026-09-30; measured 2026-08-05).

> "**The universal win — every repo, every size: 88% fewer tool calls · 53% faster · 62% fewer tokens · 44% cheaper · file reads cut to zero on all seven repos.**"

> "Tested across **7 real-world open-source codebases** spanning 7 languages, comparing an agent (Claude Code, headless) answering **one architecture question** **with** and **without** CodeGraph, at the **median of 4 runs per arm**."

| Codebase | Language | Tool calls | Time | File reads | Tokens | Cost |
|---|---|---|---|---|---|---|
| VS Code | TypeScript · ~11k files | 2 vs 28 | 2.2× faster (58s vs 2m 10s) | 0 vs 12 | 77% fewer | 71% cheaper |
| Excalidraw | TypeScript · ~640 | 2 vs 43 | 3.6× faster (45s vs 2m 42s) | 0 vs 18 | 84% fewer | 78% cheaper |
| Django | Python · ~3k | 3 vs 14 | 35% faster (54s vs 1m 23s) | 0 vs 8.5 | 41% fewer | **13% cheaper** |
| Tokio | Rust · ~790 | 3 vs 29 | 2.6× faster (1m 3s vs 2m 43s) | 0 vs 19 | 65% fewer | 64% cheaper |
| OkHttp | Java · ~645 | 1 vs 6 | 43% faster (33s vs 58s) | 0 vs 2 | 54% fewer | 21% cheaper |
| Gin | Go · ~110 | 1 vs 7 | 39% faster (28s vs 46s) | 0 vs 4 | 52% fewer | **~even** |
| Alamofire | Swift · ~110 | 4 vs 33 | 2.6× faster (54s vs 2m 22s) | 0 vs 16.5 | 59% fewer | 57% cheaper |

**F7a — CONFIRMED — the vendor's own table refutes a corpus-size threshold, in the vendor's own words.** This is the single most useful row for Q2:

> "Cost tracks how much *discovery* a question demands more than raw repo size: 57–78% on questions the file-reading agent needed 28–43 tool calls to answer, near-even where it got there in 7."

Read off the table: Django at ~3k files bought **13%**, while Excalidraw at ~640 files bought **78%** and Gin at ~110 files bought **~even**. Repo size does not order the effect; *how much structure the question requires you to re-derive* does.

**F7b — CONFIRMED — the vendor's own context-cost caveat (this is s3-F24, re-verified at source).**

> "the numbers above measure *throughput* — tokens processed, tools called, dollars spent to reach one answer. They don't measure what is still sitting in your context window afterward, and on that axis CodeGraph costs **more**, not less. Across the same seven repos in multi-turn sessions, CodeGraph's responses leave about **80% more retrieval context resident** at the end of a session than a file-reading agent's do — on VS Code, 67k tokens against 18k."

**F8 — CONFIRMED — a task-shaped, not size-shaped, win.** s3-F16, <https://arxiv.org/abs/2602.20048> (2026-02-23), abstract read 2026-10-12:

> "Through258 automated trials across 30 benchmark tasks on a production FastAPI repository, we demonstrate that graph-based structural navigation via CodeCompass … achieves 99.4% task completion on **hidden-dependency tasks**, a 23.2 percentage-point improvement over vanilla agents (76.2%) and 21.2 points over BM25 retrieval (78.2%)."

So the class where the graph beats grep is **dependencies with no lexical overlap**. And the same paper's cost:

> "we uncover a critical adoption gap: **58% of trials with graph access made zero tool calls**, and agents required explicit prompt engineering to adopt the tool consistently."

**F9 — CONFIRMED — the graph must be *adopted*, not merely present.** Same as F8, and reinforced by s3-F32 (Blueprint: ~63K provider-billed tokens with the structural graph against ~41K without, "because the structural map enabled more confident and thorough exploration").

**F10 — CONFIRMED — no measurement exists for the case that matters here.** A code graph indexed over a *markdown decisions-and-facts corpus*, queried for "which entry covers this path", has no published measurement anywhere I looked. **GAP, and the most load-bearing gap in this store's case.**

**F12 — MEASURED (first-party, this machine, 2026-10-12)** — the in-repo graph and the git alternative, on this repo:

| Measurement | Value | How |
|---|---|---|
| `code_graph.py .` full rebuild | **0.94 s** wall, 0 errors | `python3 code_graph/code_graph.py .` |
| Graph content | 126 files, 126 modules, 1240 functions, 433 tests, 13 fixtures | `stats` block |
| Edges | **3700** (call 2000, contains 1240, import 345, fixture 115) | `stats` block |
| Unresolved calls | attribute 2863, dynamic 927, name 84 | `stats` block |
| Graph size on stdout | **2,607,872 bytes** (~2.6 MB) | `ls -l` |
| Prior recorded build | 110 files, 1211 nodes, 3371 edges, 0 errors, **0.6 s** | `runs/20261005-code-graph-tool/nodes/n3-build-3.result.md:33` |
| Repo commits | 246 | `git rev-list --count HEAD` |
| `git log -1 --format=%at -- <path>` | **0.00 s** | timed |
| Full-history `git log --name-only -- ancient_games/` | **0.01 s**, 40 distinct paths ever touched | timed |
| `.git` size | **19 MB** | `du -sh .git` |

Note the 0.6 s → 0.94 s growth tracks110 → 126 files: linear-ish, and still under a second at this size.

**Verdict on Q2.** There is no measured corpus size at which a code graph starts beating grep. The one measured axis that orders the effect is **question type** (hidden-dependency / structural questions — F8), and the second is **how much discovery the question demands** (F7a), which is a property of the question, not the repo. For the memory system, entry→path lookup is neither: `covers:` is already the index, and it is exact.

---

## 3. Current tools (2025–2026) that index files that stay the source of truth

**F4 — CONFIRMED — codegraph.** <https://github.com/colbymchenry/codegraph> (MIT, 73,760★, pushed 2026-10-11; README last commit 2026-09-30).

*How built:* tree-sitter AST extraction, native parse workers, a multi-worker resolver pool; resolution binds a reference to one of the same-named definitions **project-wide**.
*Storage:* `.codegraph/codegraph.db`, SQLite with FTS5.

> "2. **Storage** — Everything goes into a local SQLite database (`.codegraph/codegraph.db`) with FTS5 full-text search."
> "| **100% Local** | No data leaves your machine. No API keys. No external services. SQLite database only |"

*How rebuilt:* incremental, by default and by design.

> "Auto-sync is enabled by default. CodeGraph watches the project and updates the graph on every file change — while your agent edits code, or you add, modify, or delete files. **The index is never stale, and there is nothing to re-run.**"

Rebuild time and size:

> "The Swift compiler repository (27k files of Swift and C++) fresh-indexes in about100 seconds; a one-file edit re-syncs in ~4."
> "the Linux kernel (70k files, 2M symbols, 6.4M relationships) indexes to completion in under 12 minutes"
> "saving a file updates the graph in well under a second — the watcher fires 300ms after a lone save and syncs exactly what changed (**~0.3s of work on a 4,400-file project, ~0.4s on the 27,000-file Swift compiler repo**), never re-scanning the tree."

From the drift benchmark doc (last commit 2026-10-07): **"392-file repo: index 1.88–2.02s in both arms, single-file sync 0.183s in both."**
Local: **yes**,100% local, single binary, "No Node.js required" (bundles its own runtime and grammars, so tree-sitter need not be installed).
Size on disk: **GAP** — see §Not found.

**F5 — CONFIRMED — Serena: the no-index alternative.** <https://github.com/oraios/serena> (30,193★, pushed 2026-10-09).

> "**Language servers** implementing the language server protocol (LSP) — the free/open-source alternative"
> "When using Serena's language server backend, we provide **support for over 40 programming languages**, including Ada / SPARK, … **Markdown**, … TOML, TypeScript, Vue, … YAML, and Zig."

*F11 — INFERRED (from F5 + absence of any index/refresh command in its README):* Serena builds no persistent index to go stale; it asks the live language server. That is the drift-free-by-construction shape. It is also the only one of these tools whose language list **includes Markdown**, which matters for a memory corpus — but it is symbol-level over language constructs, which markdown largely does not have. Local: yes. Cost: language servers must be installed per language (README: "some additional dependencies may need to be installed to support certain languages"). Build/rebuild time: not applicable — no index.

**F13 — CONFIRMED — SCIP: the interchange format, not a tool.** <https://github.com/sourcegraph/scip> (Apache-2.0, 827★, pushed 2026-10-10).

> "SCIP (pronunciation: \"skip\") is a language-agnostic protocol for indexing source code, which can be used to power code navigation functionality such as Go to definition, Find references, and Find implementations."

Files stay the truth; the index is a per-commit build artifact produced by a per-language indexer. Rebuild time and size: **GAP** (not found; the repo is a protobuf schema + bindings + a CLI).

**F16 — CONFIRMED — codegraph's own CI recipe uses git as the change oracle.** <https://colbymchenry.github.io/codegraph/reference/cli/> (retrieved 2026-10-12)

> `codegraph index [path]  # Full re-index from scratch (--force, --quiet, --verbose)`
> `codegraph sync [path]  # Incremental update (--quiet)`
> `codegraph affected [files...]`
> `codegraph affected --stdin # pipe from git diff`
> `AFFECTED = $( git diff --name-only HEAD …`

Relevant to §6: **the vendor's graph consumes git's answer to "what changed"; it does not try to out-perform git at it.**

**F18 — the in-repo tool.** `code_graph/code_graph.py`, 981 lines, stdlib only (`argparse, ast, builtins, fnmatch, json, sys, collections, pathlib`). Emits JSON to **stdout only** — no DB, no file, no cache, no lockfile, no incremental path; `GraphBuilder.run()` re-walks, re-reads and re-`ast.parse`s everything every invocation. `*.py` only (`self.root.rglob("*.py")`, `code_graph.py:262`). Node kinds `module`/`function`; edge kinds `contains`/`import`/`call`/`fixture` (`code_graph.py:55`). Its own stated design rule — "Files are walked in sorted path order. Two runs on the same tree give byte-identical output" — means it **cannot drift** (confirmed independently by F5's determinism control, below).

---

## 4. How it fails

**F5 — CONFIRMED — this is the best-documented drift study I could find, and it is a vendor measuring itself against its own tool.** <https://github.com/colbymchenry/codegraph/blob/main/docs/benchmarks/index-drift-cg33.md> (last commit 2026-10-07; "Measured 2026-08-06"). Confirms and extends s3-F25/F26/F28.

*Silent, and the README says the opposite.*

> "A live, auto-sync-maintained index **does not converge** to a clean full rebuild of the identical working tree. On codegraph's own repo, **4.3% of distinct edges were wrong**, in both directions, overwhelmingly `calls` edges."
> "This matters because it is silent: nothing warns, nothing surfaces it, and the README tells users the index is never stale and there is nothing to re-run."

| | count |
|---|---|
| distinct edge triples (rebuild) | 28,809 |
| in rebuild but **missing** from live | **751** |
| in live but **absent** from rebuild (stale) | **476** |
| **total divergent** | **1,227 — 4.3%** |

*Failure mode 1 — a count-based check lies.* (New; not in r2.)

> "Raw edge **rows** were 39,845 live vs 40,122 rebuilt — a benign-looking +0.7%. The divergence is bidirectional, so a net-count check nets it out and reports almost nothing wrong. **Any drift detector must compare edge sets, not totals.**"

*Failure mode 2 — every conventional integrity check passes.* (New.)

> "Node sets are identical — `files` 501 = 501, `nodes` 10,110 = 10,110, heuristic edges 36 = 36 — and every integrity check is 0 on *both* indexes: no duplicate nodes, no orphan edges, no nodes referencing a missing file row. **Nothing accumulates. Cross-file resolution goes stale.**"

*Failure mode 3 — it is not noise.*

> "Control, rebuild vs rebuild on the same tree and build: **0 differing edges** (28,809 both runs). So the live-vs-rebuild delta is not run-to-run noise."

*Failure mode 4 — the fix is partial, by design.*

> "| 80 commits | 1,634 (963 / 671) | 890 | **361 (359 / 2)** |"
> "**The full rebuild is the wrong one here** — converging would mean teaching sync to manufacture thousands of wrong edges. Left as is, deliberately."

*Failure mode 5 — a mistyped cache path is indistinguishable from staleness.* (New; directly relevant to M6.)

> "`sqlite3` against a mistyped path **creates an empty database** rather than failing, and every subsequent query then answers from an empty schema — which reads exactly like a stale pre-migration index."

*Failure mode 6 — retrieval quality decays invisibly (s3-F26, re-verified).*

> "a generated ambient-types file carried graph mass **0.24750** on the drifted index vs **0.13119** on a clean rebuild (~1.9×), and score **49.0** vs **27.0**. On the drifted index it took **60.7%** of an explore envelope and starved the file the agent had actually named by symbol, which rendered **251 chars of a 10,970 reservation**."

**F5b — CONFIRMED — the detection mechanisms exist, and none of them can see this failure class.** <https://colbymchenry.github.io/codegraph/guides/indexing/>

The three layers are named, on the page, as covering exactly two windows: the debounce window and the server-not-running gap.

> "1. **File watcher with debounced auto-sync (always on)**" — "A debounce timer collapses bursts of edits into a single sync." (default 2000 ms, `CODEGRAPH_WATCH_DEBOUNCE_MS`, clamped `[100ms, 60s]`)
> "2. **Per-file staleness banner** — covers the debounce window"
> "3. **Connect-time catch-up** — covers gaps when the MCP server wasn't running" — "a (size, mtime) stat pre-filter, then a content hash on the rest"

The banner:

> "⚠️ Some files referenced below were edited since the last index sync —their codegraph entries may be stale: - src/Widget.ts (edited 800ms ago, pending sync)For accurate content of those specific files, Read them directly.The rest of this response is fresh."

**F6 — INFERRED — these layers cannot detect the F5 class.** Derived from F5 + F5b. All three are keyed to *mtime/content* of files on disk. The F5 failure is not a file that changed and was missed; it is a file that was correctly re-extracted, after which **cross-file resolution elsewhere in the repo became wrong** and nothing was left behind to revisit. A per-file "is this file pending sync" signal is structurally incapable of seeing it.

**F5c — CONFIRMED — and the vendor says so, explicitly.**

> "### `codegraph status` — decided: no drift metric
> The issue asked whether `status` should surface divergence. Decision: **no**.
> A drift number cannot be computed without the full rebuild it would be recommending, so anything cheap enough to run on `status` would be an estimate — and an honest estimate is not available."

This sharpens the s3 gap ("`status` deliberately declines to report a drift metric") into the load-bearing sentence: **you cannot cheaply detect drift, and detecting it costs exactly the thing you were avoiding.**

**F19 — CONFIRMED (cited) — the CLI-vs-daemon variant.** s3-F27: after adding a symbol, `codegraph query "metodoNuevo"` returned "No results found" and the database had 0 rows for it; issue created 2026-09-20, closed 2026-10-07. Because only the MCP daemon auto-syncs, a user-facing CLI over the same index is stale by construction — i.e. **"the cache" and "the index the reader sees" can be different objects**, which is the sharpest possible violation of "its absence must not stop anyone reading memory" (M6).

**F20 — CONFIRMED (cited) — adoption failure is a failure mode too.** s3-F33: "58% of trials with graph access made zero tool calls" (arXiv 2602.20048). A correct graph that agents route around produces the same outcome as no graph, plus the maintenance and drift cost.

**F21 — INFERRED — the repo has already paid this bill once.** `docs/KNOWLEDGE_GRAPH_DESIGN.md:31-34`: *"Non-goals, stated up front because this repo has a track record of building graphs nobody queries (`loop/graph_memory.py`, 631 lines, no query code, `~/dev/seza/.ctxgraph/graph.db`, wired once, never touched again…)"*, and `:489-499`: *"Building it now would mean testing it exclusively against synthetic data … which is exactly the failure mode wave2 flags … : correct and unused."* That is F20 and F19 in this repo's own history.

---

## 5. What fits here — options, not a choice

Machine as given: Python 3.12, SQLite 3.45.1 + FTS5, numpy, RTX 4070 Ti SUPER 16 GB. **Not installed: sqlite-vec, sentence-transformers, fastembed, tree-sitter.** The repo is 246 commits, 1446 tracked files, 123 `.py` files, `.git` 19 MB. `project-memory/` **does not exist yet**, so there are no real `covers:` values to size this against.

The GPT is bad and most of these numbers are small enough that I would not build anything before the corpus exists. Options as required:

**Option A — no code graph. Git on `covers:`.**
*Needs installed:* nothing. *Rebuild:* n/a. *Size:* 0 (uses `.git`, already 19 MB). *Drift class:* none — `git log` reads the truth, not a projection of it.
*Answers:* the line-75 check exactly, and "which entries cover the files I am about to edit". *Does not answer:* "what does this change transitively affect", "is this entry still true".
*Measured here:* 0.00 s per path, 0.01 s for a full-history path scan of one directory (F12).

**Option B — reuse `code_graph/code_graph.py` as-is, full rebuild, never incremental.**
*Needs installed:* nothing (stdlib). *Rebuild:* **0.94 s** measured now (was 0.6 s at 110 files). *Size:* **2.6 MB** to stdout; no file written. *Drift class:* none by construction — deterministic, byte-identical, no incremental path, no DB.
*Answers:* symbol-level and call-level change within `*.py`. *Does not answer:* anything about markdown; nothing about non-Python paths in `covers:`.
*The trap:* `covers:` names *paths*, not symbols, so a rebuild is mostly wasted — and partial language coverage is a **silent partial answer**, which is F19's failure mode wearing a different hat. A graph that answers for Python entries and silently not for the rest is worse than no graph, because the miss is invisible.

**Option C — adopt an external indexer (codegraph).**
*Needs installed:* the codegraph binary (self-contained; bundles its own runtime and grammars, so the absent tree-sitter is not a blocker). *Rebuild:* ~100 s for 27k files; ~0.3–0.4 s incremental sync; 1.88–2.02 s full index on a 392-file repo. *Size:* GAP. *Runs locally:* yes, 100% local.
*Answers:* F7's measured win — but on **source-code architecture questions**, not on markdown memory (F2, F14). *Costs:* the entire drift apparatus of §4, plus a background daemon and a writer lock, plus `--stdin | git diff` plumbing (F16).

**Option D — adopt Serena (LSP, no index).**
*Needs installed:* a language server per language. *Rebuild:* n/a. *Size:* no index. *Drift class:* none — queries the live filesystem.
*Answers:* live symbol navigation. *Does not answer:* markdown semantics (F5 lists Markdown as supported, but a markdown file has few language-level symbols), call-graph edges it never promised, or anything offline. *Also the only option above that can read `.md` at all.*

**Option E — git for the check, stdlib `ast` for the refinement.**
*Needs installed:* nothing. *Rebuild:* bounded by the diff, not the repo — parse only the changed file(s) to map each diff hunk to its enclosing symbol. *Size:* n/a. *Drift class:* none.
*Answers:* the line-75 check **and** symbol-level precision on `*.py`, because the work is proportional to what changed. *Does not answer:* transitive call impact, non-Python.

Trade-off axis worth naming: **A and E cost nothing and answer the check; C buys a measured win on a question this store has not been shown to ask; D is drift-free but changes tool surface and dependency footprint; B is free and correct but answers a narrower question than the design's entries are phrased in.** I am not choosing, per the brief.

---

## 6. The specific question: does the line-75 drift check need a code graph, or is git on `covers:` enough?

> `SOURCE_OF_TRUTH.md:75` — "A script with no model call also marks a decision or fact in `INDEX.md` when its code changed with no earlier change to the entry."

> `SOURCE_OF_TRUTH.md:79` — "**Not decided yet (EJ decides):** … how the script tells that the entry changed earlier than the code …"

### The check, decomposed

Two primitives, both pure git, given what the design says `covers:` is:

`SOURCE_OF_TRUTH.md:50` — the entry header holds "`covers` (the code paths it is about)". **Paths, not symbols.** That single word decides most of this.

1. *When did the entry last change?* → `git log -1 --format=%at -- project-memory/entries/<id>.md`. **0.00 s here** (F12).
2. *Has a covered path changed since?* → `git log --since=@<t> --name-only -- <each covers path>`. **0.01 s** for a full-history scan of `ancient_games/` (F12).

Compare the two timestamps. No parse, no resolver, no index, no model. Ordering a commit against an entry commit is a field comparison on data git already stores as the record of what happened — the one artifact in this system with no drift class at all, because it is not a projection.

### The case **for** a code graph

1. **Precision.** A one-line comment edit in a 400-line covered file is a change to that file; a symbol-level check would not flag the decision the file encodes. This is real, and it is the strongest argument. *But:* git gives the diff hunk; mapping a hunk to its enclosing symbol is a ~30-line stdlib `ast` walk over the **changed file only**. That is Option E — it buys the precision without a repo-wide graph.
2. **Call edges — transitive meaning change.** If `journal.py` calls into `stages.py` and `stages.py` changes, an entry covering only `journal.py` is not flagged. A graph would flag it. **This is genuinely more capability than git on paths has.** *But it lands on the wrong side of the design's own line:* "does this entry still match the code" is the background subagent's job (`SOURCE_OF_TRUTH.md:70-73`, "it reports to EJ which entry, what the entry says, and what the code does instead"), not the model-free script's. A transitive check is the more expensive question, and the design already pays a model to answer it. Line 75 is the cheap ordering check.
3. **s3-F4 — StateTape reads staleness off a code-graph diff with no model call.** Verified at source (F8, <https://arxiv.org/abs/2609.36319>, 2026-09-28):

> "The key idea of StateTape is to model the repository as a symbol-level code graph, whose dependencies and language rules expose which symbols a write can affect. Upon this graph, a tape marks the symbols each write changed, which turns staleness from an inference about text into an observation of the agent's writes."

Two caveats that survive the citation. First, the abstract concedes a model in the loop for the residue: *"a small manager model settles what the write log cannot."* The model-free claim covers **nomination**, not adjudication — the design's line 75 is nomination-shaped, but so is the model half of StateTape. Second, and decisive for our case: **a write is the agent's own edit, in the current session, on files it just touched.** StateTape marks what the write log logs. The line-75 check is "the code changed at some point in the last four days and nobody updated the entry" — a historical scan over commits the agent did not make. Different problem. And StateTape's records cover **symbols by construction** ("Its unit is the symbol (a function, method or class), the smallest unit whose change alters meaning, not position", s3-F3) — which means s3-F4's applicability is a consequence of *how StateTape chose to scope its records*, not a general property of drift checks. If `covers:` named symbols, s3-F4 would apply. It names paths.
4. **s3-F26's production incident** — a drifted index degraded retrieval. True, and it is evidence *against* the graph for this check, not for it: it is what you get when you introduce a stale projection to answer a question git answers exactly.

### The case **against** — for git on `covers:`

1. **The graph introduces a staleness class into a check that had none.** F5 is the best available measurement of exactly that class: 4.3% of distinct edges wrong, bidirectionally, silently, with a README promising the opposite — and, per F5c, **no cheap way to detect it, because detection costs the full rebuild you were avoiding.** For a check whose entire value is "is this entry still trustworthy", a 4.3%-and-silent oracle is a downgrade from git's exactness, not an upgrade.
2. **The same vendor already ruled on this.** F5: *"The full rebuild is the wrong one here — converging would mean teaching sync to manufacture thousands of wrong edges. Left as is, deliberately."* So the incremental graph — the only form that makes the check cheap — is the form its own maintainers declined to converge, and the full-rebuild form is the form you do not need because git is already the rebuild.
3. **The repo's own rule forbids the edge.** `docs/KNOWLEDGE_GRAPH_DESIGN.md:45-50`: *"No node or edge type without a listed query."* The design lists exactly one query for this store, and it is an ordering check over covered **paths**. No listed query needs a symbol or call edge. `KNOWLEDGE_GRAPH_DESIGN.md:524-528` names the follow-on and its trigger in the same breath: *"The code import/call graph is deliberately not built. If Guard is ever asked 'does this edit reach a hub transitively through imports,' the follow-on is a `kind='imports'` addition to `edge` … This is not built now because no listed query needs it."*
4. **The repo's own doctrine points the other way.** `KNOWLEDGE_GRAPH_DESIGN.md:355-366`, citing the evidence-KG skill's rule 9: *"Build a new graph from the whole corpus. Never incrementally patch a production graph unless the importer proves exact update and provenance-merge semantics … a full rebuild from an append-only log at K3's scale … is cheap enough that incrementality buys nothing."* The in-repo graph honours this and cannot drift (F18: deterministic, byte-identical, 0.94 s). So the repo already has the drift-free shape — and it still does not need it, because git is cheaper and exact.
5. **The git-bound memory literature reaches the same ledger from the other direction.** s3-F13, <https://arxiv.org/abs/2607.14390> (2026-07-15), abstract read 2026-10-12 — *"Why Git Is the Memory Solution for the Agentic Development Lifecycle"*:

> "We argue memory should instead be git-bound -- built into the repository's version control, inheriting the guarantees the machinery struggles to construct: **ground truth from commits, freshness from rebuild**, verification from the merge, containment from review."

Note two things. It is a *memory* paper, and it lands on git — and when it does want structure, it wants a **git-anchored** one: *"A router dispatches breadth to a git-anchored structural map, pointed lookups to confidence-gated episodes, and rationale to decision synthesis."* Same split as `SOURCE_OF_TRUTH.md:70-75`: git decides the ordering, something more expensive decides the meaning.
6. **When it did use structure anyway, it still fell back to git plus a parser.** s3-F22 (relore, Hugging Face): the tool *"had to finish with grep plus a Python AST scan."* The empirical shape of "git, then parse" is what real systems converged on.

### Conclusion, and the flip condition

**Git on the `covers:` paths is enough for the line-75 check as the design states it** — because `covers:` names paths, because git is the authoritative record rather than a projection of it, and because a code graph's two unique capabilities (symbol precision, call edges) either reduce to a parse of the changed file or belong to the model-assigned job on lines 70-73. The check's own open question at line 79 ("how the script tells that the entry changed earlier than the code") is answerable with two `git log` calls and 0.00 s, and does not need to become an index question.

**Three named conditions would flip this** — stated as tests, in the idiom of `KNOWLEDGE_GRAPH_DESIGN.md` §5:

1. `covers:` starts naming **symbols** rather than paths (`SOURCE_OF_TRUTH.md:50`). Then s3-F4's mechanism applies and a parser is needed. Test: does any entry's `covers:` field stop being a path?
2. The check changes from *"did the covered code change"* to *"what does this change affect"* — the `codegraph impact` / transitive question. Test: does the script need an answer about a file not on any `covers:` list? That is the `kind='imports'` trigger already written down at `KNOWLEDGE_GRAPH_DESIGN.md:524-528`.
3. Call sites drift at a rate that makes path-level flags useless noise. Test: if >X% of flags are false positives from unrelated edits in large covered files, precision has become the binding constraint — at which point Option E buys it for free, from the diff.

Per the brief: options reported, not chosen.

---

## Not found- **`tarnline`** — in GitHub repo search (4 query variants, `total_count: 0`), PyPI (404), npm (404), the GitHub REST API (404), and the open web (exact-phrase search: zero hits). No README, no language list, no error page quoting a project of that name.
- **Index size on disk for any external code-graph tool.** codegraph publishes WAL thresholds ("soft threshold = the larger of 256 MB and a quarter of the index size, up to 2 GB"; "at rest it is trimmed to 64 MB") and states "the index itself has no size limit", but **never states the index size for any repo**. Checked: README, `guides/indexing/`, `reference/cli/`, `reference/languages/`.
- **A measured corpus-size threshold at which a code graph beats grep.** None exists. The closest is s3-F31's qualitative "~20 files" claim, and the vendor's own table contradicts size as the ordering variable (F7a).
- **Any measurement of a code graph over a markdown decisions-and-facts corpus.** The whole benchmark base (F7, s3-F16, s3-F29, s3-F38) is source code. This is the load-bearing gap for this store.
- **A drift *detection* metric in codegraph.** Deliberately declined, with reasons (F5c). Matches the r2 gap, now with the reason quoted.
- **A published rebuild-time or index-size figure for Serena or SCIP.** Serena has no index; SCIP is a format (F13). Neither publishes one.
- **Any tool found that detects doc-vs-code staleness from git commit timestamps** — searched for stalint/"checkdocs"-class tooling and for `git diff`-based staleness CI. The search endpoint returned nothing on repeated attempts. **Unproven/GAP** — I am not claiming none exists, only that I did not find one. This would have been the strongest third-party precedent for §6.
- **The unit of "~4" in codegraph's re-sync claim** ("a one-file edit re-syncs in ~4"). The README fragment does not state the unit. Quoted verbatim, not interpreted.
- **The date of codegraph's languages doc page.** No visible date; README last-commit 2026-09-30 recorded instead.
- **`store-research/wave2-kg/MERGED.md`** — already known absent from disk before this run; `KNOWLEDGE_GRAPH_DESIGN.md` numbers citing it are second-hand.

## Not checked

- Building, installing or running any tool in §3 on this machine. Everything about codegraph and Serena is from their primary documents; nothing was executed.
- `codegraph`'s Windows/WSL behaviour, telemetry, the hosted platform, or the `codegraph ui` viewer ("not released yet").
- The README's "2–7× faster than the fastest competing indexer's re-index-on-change … across a 31-repo, 30-language benchmark" — the competitor was not identified or benchmarked.
- s3-F27 (the gentle-ai stale-CLI issue) at first hand; cited from the r2 run, which labelled it `verified`.
- The 2,863 `attribute`-unresolved and 927 `dynamic` unresolved calls in the F12 measurement — recorded, not analysed. Resolution quality of `code_graph.py` is unassessed.
- Any non-Python language in this repo, so `code_graph.py`'s coverage of real `covers:` values is untested.
- Whether `covers:` in practice tends to name one file or many — `project-memory/` does not exist yet, so there is no data.
- s2 and s4 findings beyond what the explore pass surfaced; `FINDINGS-s4-retrieval-consolidation.md` contains no code-graph rows at all.
- The other two stores. Cross-store comparison (does an agent need a graph *because* it also needs FTS?) is out of scope here.
