> **Status: beta copy, not accepted by EJ.** Copied 2026-10-12 by the COO (Claude `claude-opus-5-5`) at EJ's
> request (*"copy like a beta copy from here in to the code-graph"*), after EJ's decision that the code graph is its
> own project (*"code graph should have it's own project"*). Every block below is copied **verbatim** from
> `docs/memory-system/CACHES.md` (accepted 2026-10-12); the only new text is this header and the *From* line above
> each block. Paths inside the blocks are as written in `CACHES.md`, so they are relative to `docs/memory-system/`.
>
> **Two copies for now.** The originals are still in `CACHES.md`. Until EJ decides what moves out, the code-graph
> text exists twice; edit `CACHES.md`, not this file.
>
> **The tool** is `code_graph/code_graph.py`, with tests in `code_graph/tests/`; it was built by the run
> `runs/20261005-code-graph-tool/`.

# Code Graph (beta)

*From `CACHES.md` lines 9–15 (Provenance and Labels, which explain the `G-F*` ids and the labels used below).*

> **Provenance.** Written 2026-10-12 by Claude (`claude-opus-5-5`) from three research
> nodes in `runs/20261012-memory-caches/nodes/`: SQLite full-text (`sqlite-fts.claude.md`, ids `S-F*`), vector
> (`vector.claude.md`, `V-F*`) and code graph (`code-graph.opencode.stdout.md`, `G-F*`). The code-graph node uses `F5`
> twice; `G-F5 drift` means the drift study and `G-F5 Serena` means Serena.

> **Labels.** *Quoted* means the line rests on a finding id; *my reading* means it is my inference; *not measured*
> means nobody has measured it.

*From `CACHES.md` § Code graph, as it stood on 2026-10-12 when it was removed from there (it had been revised
since the first copy: the drift check is gone and there are two conditions, not three).*

## Code graph

### Five whys

1. **Why a code graph?** To answer structural questions about the code, such as what an edit touches.
2. **Why would memory need that?** For "which entries cover the files I am editing" (`SOURCE_OF_TRUTH.md` Rd4.1). The
   drift check it once also served was removed by EJ on 2026-10-12.
3. **Why is a text search enough?** `covers:` names **paths**, not symbols, and is already a hand-kept index from entry
   to path (`G-F14`), so finding the entries that cover a file is a search over `covers:` lines.
4. **Why not add a graph anyway?** An incrementally synced graph adds a silent failure that a text search does not have
   (`G-F5 drift`, 4.3% of edges wrong). A full-rebuild graph such as the repo's own does not drift (`G-F18`), but it
   covers Python only, so for other `covers:` paths it gives a silent partial answer (code-graph node §5, option B).
   Whether an entry is still true is answered by reading it against the code (`SOURCE_OF_TRUTH.md` Rd5), not by a
   graph.
5. **Why might it be needed later?** Either of two conditions in the code-graph node's §6, each a test:
   - `covers:` starts naming functions or classes instead of files;
   - an agent must answer about files not on any `covers:` list ("what does this change affect").

### 5W1H

| | |
|---|---|
| **Who** | Any agent, by a text search over `covers:` lines. EJ decides to build a graph if one of the two conditions holds. |
| **What** | Today: no graph for memory. A text search over `covers:` lines. If a condition holds: the repo's own `code_graph/code_graph.py` (Python only, deterministic, full rebuild, no incremental mode, `G-F18`) before any outside tool. |
| **When** | Today: before editing a file (`SOURCE_OF_TRUTH.md` Rd4.1). A graph, if ever built, is rebuilt in full each time it is used. |
| **Where** | Nothing today. Later, `project-memory/.cache/code-graph.json`, gitignored. |
| **Why** | The five whys above. |
| **How** | `rg` for the file's path in the `covers:` lines of `entries/`. External indexers (codegraph) are not adopted: their win is measured on source-code architecture questions, not on memory (`G-F7`, `G-F14`), and they bring the drift in `G-F5 drift`. |

*From `CACHES.md` lines 124–155 (When to use which store → Part 2, code and docs).*

### Part 2 — code and docs (corpus: this repo's code and docs)

**Outside the vision.** The confirmed vision covers memory entries only (EJ, 2026-10-12). This table is measured on
this repo's code and docs and is kept as evidence and as guidance for agents; it is not part of the caches design.
Its evidence is **Measured here: development and testing** below.

**Routing rule for development and testing (proposed).**

| the question | use | then | evidence |
|---|---|---|---|
| Where is function or method X defined? | code graph | read that definition | BM-1 |
| Where is a flag, constant or string defined? | full-text, or grep | read the hit | BM-1 (A05) |
| What calls X? | code graph — lower bound, Python only | read the callers; treat the list as partial | BM-3 (C08–C10: 33–46 characters) |
| What does changing F reach, several hops out? | code graph — Python only, lower bound | grep imports and callers for the rest, then read | G-F8, G-F17, G-F18 (not measured here) |
| Which tests should I run after changing function X or file F? | code graph (tests reaching X or F) **plus** full-text on the file name (tests that run it as a separate process) | run that subset; run the full suite (31–33 s) before committing | BM-7, BM-8, BM-9 |
| Why did we decide X? Where is X explained in the docs? | full-text (ties hybrid on hits; prints less in total) | read the section | BM-4 |
| How do I run or configure X? | not settled: hybrid and vector scored 0.5 and full-text 0.33, on 6 questions | read the hit | BM-5 (n=6, too small to act on) |
| A concept, in my own words | grep and read, as an agent search | record a miss if the answer is found another way | BM-2 |
| Anything the graph answers with nothing or only partly | full-text, then grep | — | BM-8 |

This table is for the **code and docs**. Part 1 above is for **memory entries**; it is reasoned, not measured, and
three of its citations were corrected in this merge. The two
differ because the corpus differs. Code and docs exist today and are already large enough that full-text and the
graph save reading (BM-6). `project-memory/` does not exist yet.

**What this does not change, and what it proposes.**
- **Unchanged:** the rules for all three caches below (full rebuild, rebuild when stale, fall back when absent).
  R1–R9 are the acceptance criteria for the memory caches.
- **The vision stands as confirmed:** for code and docs, the measurements say full-text and the graph already save
  reading today. EJ kept the vision for memory entries only (2026-10-12), so the proposals in
  `runs/20261012-caches-routing/vision-proposals.md` (P1–P3) were not adopted.


*From `CACHES.md` lines 160–163 (Rules for all three caches → Full rebuild, never patched).*

- **Full rebuild, never patched.** A live, incrementally updated index drifted silently from a clean rebuild: 4.3% of
  edges wrong, with every integrity check passing (`G-F5 drift`). Its makers decided drift cannot be measured cheaply
  (`G-F5c`). A full rebuild of this repo's code graph takes 0.94 s (`G-F12`); the benchmark's own code-graph rebuild
  takes 0.89 s (BM-9); an FTS rebuild of 10,000 synthetic entries takes 0.53 s (`S-F13`).

*From `CACHES.md` lines 282–348 (Measured here: development and testing).*

## Measured here: development and testing

EJ's aim is that development and testing get faster and cheaper in tokens. So this section measures all three stores
against grep on **this repo**: 490 files (123 `.py`, 367 `.md`, 4.8 MB), with 40 questions an agent asks while
developing and testing it. Run: `runs/20261012-caches-routing/` (results in `bench/results.md`, ids `BM-*` below).

**Who wrote each check, and what it does not establish.**
- The **questions and answers** were written by codex (`gpt-6.1-sol`), each checked by an `rg` command it ran. Five
  Claude agents re-checked all 40: 37 were correct and 3 were incomplete. Those 3 were completed.
- **"Which tests run this code"** is also scored against per-test runtime coverage (`pytest-cov`, no model). That
  counts in-process Python only, so it misses tests that run the code as a separate process.
- The **harness** was written by opencode. A Claude audit found 5 high-severity biases, and a Claude repair fixed
  them; the repair was **not re-audited**. Rebuilding from scratch gave the same answers on all 180 question-route
  pairs.
- **Token cost** is measured as *characters printed up to the first line that names a right file*. That is a proxy,
  not a token count, and a weak one:
  - it stops at the right *file*, not the right answer;
  - misses are left out, so each route's mean is over a different set of questions;
  - each route prints a different format.

  No agent was run end to end.
- One repo, one question set, **n = 6 to 10 per category**. None of this is a project-memory corpus.

**What each route returns, per category** (symbol hit in the top 5 / characters read to the first line that names a
right file):

| | grep (`rg`) | SQLite full-text | vector | hybrid | code graph |
|---|---|---|---|---|---|
| **BM-1** exact identifier (8) | 0.75 / 920 | 0.63 / 356 | 0.0 / 837 | 0.5 / 91 | **0.75 / 43** |
| **BM-2** concept in other words (8) | 0 / — | 0 / — | 0 (file 0.25) / 955 | 0 (file 0.13) / 1,427 | n/a |
| **BM-3** structure and test impact (10) | 0.8 / 1,015 | **0.9 / 175** | 0.1 / 1,421 | 0.9 / 362 | 0.7 / **61** |
| **BM-4** decision or reason in the docs (8) | 0.63 / 4,470 | **0.63 / 525** | 0.5 / 810 | 0.63 / 516 | 0.0 (over 2 questions) |
| **BM-5** how to run or configure (6) | 0.17 / 6,875 | 0.33 / 1,146 | 0.5 / 569 | 0.5 / 1,120 | n/a |

- **BM-6, all categories.** Characters printed up to the first right file (each mean over that route's hits only:
  grep 26, full-text 25, vector 19, hybrid 26, graph 13): grep 2,688, full-text 451, hybrid 528, vector
  923, graph 53 (graph over the 20 questions that name a symbol or file). Total output per answer: grep 4,304,
  full-text 1,817.
- **BM-7, test impact against runtime coverage** (C01–C04, n=4). The macro-average test-file recall of the tests that
  really run the function each route found: graph 0.78; grep, full-text and hybrid 0.59; vector 0.04.
- **BM-8, tests that run the code as a separate process** (C05–C07). The graph returns **nothing**, because no
  call edge exists. Full-text search on the file name found 2 of 3; grep named a gold file on 2 of 3 and the
  complete set on 1 of 3, printing up to 8.7K
  characters.
- **BM-9, speed.** Every route answers in at most 15 ms per question; the slowest was grep on E04, at 14.7 ms. Full
  rebuilds take 0.17 s for full-text (9.5 MB), 0.94 s for vector (10.2 MB) and 0.89 s for the graph (4.9 MB); the
  graph's own rebuild for `G-F12` was measured separately at 0.94 s. The full test suite, 529 tests, takes 31–33 s (3
  runs).

**What the numbers say (my reading).**
1. **On this repo, speed is not the reason to use a cache.** Every route takes milliseconds (BM-9). The difference is
   in **what the route prints**: full-text prints about a sixth of grep's characters before naming a right file
   (BM-6). Whether that becomes a sixth of an agent's tokens is not measured. Where
   the question names a symbol or file, the graph gets there in tens of characters (BM-1, BM-3); its BM-6 mean is over
   those 20 questions only, so it is not a like-for-like ratio.
2. **The vector index loses almost everywhere it was tried.** It never found an exact identifier (BM-1), and its
   test-file recall against runtime coverage was 0.04 (BM-7). Its only edge is "how do I run or configure X" (BM-5,
   n=6), which is
   too small to act on. Nothing here contradicts the earlier rule that vectors come last and only as a hybrid.
3. **No route answers a concept asked in other words in one shot** (BM-2). That still takes an agent searching and
   reading. It is exactly the miss the vector trigger is meant to record.
4. **No single store answers "which tests should I run".** The graph finds tests that reach the code indirectly
   (BM-7), but is blind to tests that run it as a separate process (BM-8). Full-text search on the file name finds
   the latter. An empty graph answer means *not seen*, never *no tests*. Even combined, the two routes
   can miss affected tests: both missed C05 entirely, and the graph found only 0.33 and 0.8 of the runtime tests for
   C01 and C02 (BM-7). That is why the full suite runs before committing.


*From `CACHES.md` lines 398–400 (Core requirements → R5.3).*

- **R5.3 Code graph** — built only when one of three conditions holds: `covers:` starts naming functions or classes
  rather than files; the check must answer about files on no `covers:` list; or, on a review of past path-level
  flags, the false alarms outnumber the true ones. (code-graph §6, G-F14, G-F18)

*From `CACHES.md` lines 499–515 (Example numbers by case → R5.3).*

### R5.3: the code graph

| Case | What was measured | Source |
|---|---|---|
| Gin, about 110 files | cost about even with or without the graph (vendor's own benchmark, like the rows below) | G-F7, W-25 |
| Alamofire, about 110 files | 57% cheaper (vendor's own benchmark) | W-25 |
| Excalidraw, about 640 files | 78% cheaper, 84% fewer tokens | G-F7 |
| Django, about 3k files | 13% cheaper | G-F7 |
| VS Code, about 11k files | 71% cheaper, but 67k vs 18k tokens left resident after the session | G-F7, G-F7b |
| Hidden-dependency tasks | 99.4% vs 76.2% task completion | s3-F16 |
| 43 files (Serena, vendor self-evaluation) | cross-file rename 9 calls down to 1, but 4.5× worse on a one-line edit | OC |
| This repo | the graph names a caller in 33–46 characters | BM-3 |
| SEZA | `.ctxgraph` (1.1 MB) imported once on 2026-07-28, every `usage_count` 0, no production code queries it (SZ); a query script exists and a staging copy was queried on 2026-08-02 (CX). How often it was used is a GAP. A built graph with almost no use: the case R5.3 exists to prevent | SZ, CX |

**My reading:** the payoff follows how far a question reaches across files, not the file count. Two repos of 110
files went from no saving to 57%.


*From `CACHES.md` lines 516–519 (Example numbers by case → R8.2, header).*

### R8.2: rebuild cost

| Store | Measured | Source |
|---|---|---|
| Code graph | 0.94 s for 126 `.py` files; codegraph about 100 s for about 27k files | G-F12, W-25 |

*(line 522, the code-graph row)*

*From `CACHES.md` lines 533–533 (SEZA today → R5.3).*

- **R5.3:** cannot be evaluated; the graph that exists is barely used (production queries: GAP).
