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
- **Token cost** is measured as *characters the agent must read to reach the first right answer*. That is a proxy,
  not a token count. No agent was run end to end.
- One repo, one question set, **n = 6 to 10 per category**. None of this is a project-memory corpus.

**What each route returns, per category** (symbol hit in the top 5 / characters read to the first right answer):

| | grep (`rg`) | SQLite full-text | vector | hybrid | code graph |
|---|---|---|---|---|---|
| **BM-1** exact identifier (8) | 0.75 / 920 | 0.63 / 356 | 0.0 / 837 | 0.5 / 91 | **0.75 / 43** |
| **BM-2** concept in other words (8) | 0 / — | 0 / — | 0 (file 0.25) / 955 | 0 (file 0.13) / 1,427 | n/a |
| **BM-3** structure and test impact (10) | 0.8 / 1,015 | **0.9 / 175** | 0.1 / 1,421 | 0.9 / 362 | 0.7 / **61** |
| **BM-4** decision or reason in the docs (8) | 0.63 / 4,470 | **0.63 / 525** | 0.5 / 810 | 0.63 / 516 | n/a |
| **BM-5** how to run or configure (6) | 0.17 / 6,875 | 0.33 / 1,146 | 0.5 / 569 | 0.5 / 1,120 | n/a |

- **BM-6, all categories.** Characters read to the first right answer: grep 2,688, full-text 451, hybrid 528, vector
  923, graph 53 (graph over the 20 questions that name a symbol or file). Total output per answer: grep 4,304,
  full-text 1,817.
- **BM-7, test impact against runtime coverage** (C01–C04, n=4). The share of the tests that really run the function
  each route found: graph 0.92; grep, full-text and hybrid 0.59; vector 0.04.
- **BM-8, tests that run the code as a separate process** (C05–C07). The graph returns **nothing**, because no
  call edge exists. Full-text search on the file name found 2 of 3; grep found 1 of 3 and printed up to 8.7K
  characters.
- **BM-9, speed.** Every route answers in at most 11 ms per question. Full rebuilds take 0.17 s for full-text (9.5 MB),
  0.94 s for vector (10.2 MB) and 0.89 s for the graph (4.9 MB). The full test suite, 529 tests, takes 31–33 s (3
  runs).

**What the numbers say (my reading).**
1. **Speed is never the reason to use a cache.** Every route takes milliseconds (BM-9). The saving is in **what the
   agent has to read**: full-text reaches the right answer after about a sixth of grep's characters (BM-6). Where
   the question names a symbol or file, the graph gets there in tens of characters (BM-1, BM-3); its BM-6 mean is over
   those 20 questions only, so it is not a like-for-like ratio.
2. **The vector index loses almost everywhere it was tried.** It never found an exact identifier (BM-1), and it found
   4% of the tests that run a function (BM-7). Its only edge is "how do I run or configure X" (BM-5, n=6), which is
   too small to act on. Nothing here contradicts the earlier rule that vectors come last and only as a hybrid.
3. **No route answers a concept asked in other words in one shot** (BM-2). That still takes an agent searching and
   reading. It is exactly the miss the vector trigger is meant to record.
4. **No single store answers "which tests should I run".** The graph finds tests that reach the code indirectly
   (BM-7), but is blind to tests that run it as a separate process (BM-8). Full-text search on the file name finds
   the latter. An empty graph answer means *not seen*, never *no tests*.

**Routing rule for development and testing (proposed).**

| the question | use | then | evidence |
|---|---|---|---|
| Where is function or method X defined? | code graph | read that definition | BM-1 |
| Where is a flag, constant or string defined? | full-text, or grep | read the hit | BM-1 (A05) |
| What calls X? | code graph | read the callers | BM-3 (C08–C10: 33–46 characters) |
| Which tests should I run after changing function X or file F? | code graph (tests reaching X or F) **plus** full-text on the file name (tests that run it as a separate process) | run that subset; run the full suite (31–33 s) before committing | BM-7, BM-8, BM-9 |
| Why did we decide X? Where is X explained in the docs? | full-text | read the section | BM-4 |
| How do I run or configure X? | full-text first; hybrid if that misses | read the hit | BM-5 (n=6) |
| A concept, in my own words | grep and read, as an agent search | record a miss if the answer is found another way | BM-2 |
| Anything the graph answers with nothing | full-text, then grep | — | BM-8 |

This table is for the **code and docs**. The table above it is for **memory entries**, and is unchanged. The two
differ because the corpus differs. Code and docs exist today and are already large enough that full-text and the
graph save reading (BM-6). `project-memory/` does not exist yet.

**What this does not change, and what it proposes.**
- **Unchanged:** the rules for all three caches below (full rebuild, rebuild when stale, fall back when absent) and
  R1–R8 apply as written.
- **Conflict with "The answer first" and the vision:** for code and docs, the measurements say full-text and the graph
  already save reading today. That contradicts "none of the three caches is needed today" and the vision's *who it is
  for: an agent retrieving an entry*. Changing either is EJ's call. The proposed wording is in
  `runs/20261012-caches-routing/vision-proposals.md`, and neither file has been edited.

