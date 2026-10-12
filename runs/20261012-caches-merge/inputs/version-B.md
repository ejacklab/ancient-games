# Memory Caches: SQLite Full-Text, Vector, Code Graph

> **Status: draft, not yet accepted by EJ.** Written 2026-10-12 by Claude (`claude-opus-5-5`) from three research
> nodes in `runs/20261012-memory-caches/nodes/`: SQLite full-text (`sqlite-fts.claude.md`, ids `S-F*`), vector
> (`vector.claude.md`, `V-F*`) and code graph (`code-graph.opencode.stdout.md`, `G-F*`). The code-graph node uses `F5`
> twice; `G-F5 drift` means the drift study and `G-F5 Serena` means Serena.
>
> **Labels.** *Quoted* means the line rests on a finding id; *my reading* means it is my inference; *not measured*
> means nobody has measured it. Two numbers come from checks the researchers wrote and ran themselves (`S-F13`,
> `G-F12`). They show timings on this machine and nothing more.
>
> **Review.** A blind review (`claude-sonnet-5-5`, `runs/20261012-memory-caches/nodes/review.claude.md`) returned
> REPAIR with 13 findings. It caught the planted defect (F-1), and the other 12 are fixed here. The fixes have not
> been re-reviewed.

## The answer first

None of the three caches is needed today. `project-memory/` does not exist yet, so nothing has been measured on it.
My reading of the research is that at the sizes measured elsewhere, `INDEX.md`, grep and git answer the questions
each cache would answer. Each cache below has a
**trigger**: a condition that can be observed and that makes it worth building. None of them is built before its
trigger fires.

This follows the design's own rule: `.cache/` is optional, gitignored and rebuilt from the files, and its absence
must not stop anyone reading memory (`SOURCE_OF_TRUTH.md`; recommendation M4, M6). It also follows the repo's own
history of building graphs nobody queried (`docs/KNOWLEDGE_GRAPH_DESIGN.md` §1, quoted in `G-F21`).

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

**What each route returns, per category** (symbol hit in the top 5 / characters read to the first right answer):

| | grep (`rg`) | SQLite full-text | vector | hybrid | code graph |
|---|---|---|---|---|---|
| **BM-1** exact identifier (8) | 0.75 / 920 | 0.63 / 356 | 0.0 / 837 | 0.5 / 91 | **0.75 / 43** |
| **BM-2** concept in other words (8) | 0 / — | 0 / — | 0 (file 0.25) / 955 | 0 (file 0.13) / 1,427 | n/a |
| **BM-3** structure and test impact (10) | 0.8 / 1,015 | **0.9 / 175** | 0.1 / 1,421 | 0.9 / 362 | 0.7 / **61** |
| **BM-4** decision or reason in the docs (8) | 0.63 / 4,470 | **0.63 / 525** | 0.5 / 810 | 0.63 / 516 | n/a |
| **BM-5** how to run or configure (6) | 0.17 / 6,875 | 0.33 / 1,146 | 0.5 / 569 | 0.5 / 1,120 | n/a |

- **BM-6, all categories.** Characters printed up to the first right file (each mean over that route's hits only:
  grep 26, full-text 25, vector 19, hybrid 26, graph 13): grep 2,688, full-text 451, hybrid 528, vector
  923, graph 53 (graph over the 20 questions that name a symbol or file). Total output per answer: grep 4,304,
  full-text 1,817.
- **BM-7, test impact against runtime coverage** (C01–C04, n=4). The share of the tests that really run the function
  each route found: graph 0.78; grep, full-text and hybrid 0.59; vector 0.04.
- **BM-8, tests that run the code as a separate process** (C05–C07). The graph returns **nothing**, because no
  call edge exists. Full-text search on the file name found 2 of 3; grep found 1 of 3 and printed up to 8.7K
  characters.
- **BM-9, speed.** Every route answers in at most 15 ms per question; the slowest was grep on E04, at 14.7 ms. Full rebuilds take 0.17 s for full-text (9.5 MB),
  0.94 s for vector (10.2 MB) and 0.89 s for the graph (4.9 MB). The full test suite, 529 tests, takes 31–33 s (3
  runs).

**What the numbers say (my reading).**
1. **On this repo, speed is not the reason to use a cache.** Every route takes milliseconds (BM-9). The difference is
   in **what the route prints**: full-text prints about a sixth of grep's characters before naming a right file
   (BM-6). Whether that becomes a sixth of an agent's tokens is not measured. Where
   the question names a symbol or file, the graph gets there in tens of characters (BM-1, BM-3); its BM-6 mean is over
   those 20 questions only, so it is not a like-for-like ratio.
2. **The vector index loses almost everywhere it was tried.** It never found an exact identifier (BM-1), and it found
   4% of the tests that run a function (BM-7). Its only edge is "how do I run or configure X" (BM-5, n=6), which is
   too small to act on. Nothing here contradicts the earlier rule that vectors come last and only as a hybrid.
3. **No route answers a concept asked in other words in one shot** (BM-2). That still takes an agent searching and
   reading. It is exactly the miss the vector trigger is meant to record.
4. **No single store answers "which tests should I run".** The graph finds tests that reach the code indirectly
   (BM-7), but is blind to tests that run it as a separate process (BM-8). Full-text search on the file name finds
   the latter. An empty graph answer means *not seen*, never *no tests*. Even combined, the two routes
   can miss affected tests: both missed C05 entirely, and the graph found only 0.33 and 0.8 of the runtime tests for
   C01 and C02 (BM-7). That is why the full suite runs before committing.

**Routing rule for development and testing (proposed).**

| the question | use | then | evidence |
|---|---|---|---|
| Where is function or method X defined? | code graph | read that definition | BM-1 |
| Where is a flag, constant or string defined? | full-text, or grep | read the hit | BM-1 (A05) |
| What calls X? | code graph | read the callers | BM-3 (C08–C10: 33–46 characters) |
| Which tests should I run after changing function X or file F? | code graph (tests reaching X or F) **plus** full-text on the file name (tests that run it as a separate process) | run that subset; run the full suite (31–33 s) before committing | BM-7, BM-8, BM-9 |
| Why did we decide X? Where is X explained in the docs? | full-text (ties hybrid on hits; prints less in total) | read the section | BM-4 |
| How do I run or configure X? | not settled: hybrid and vector scored 0.5 and full-text 0.33, on 6 questions | read the hit | BM-5 (n=6, too small to act on) |
| A concept, in my own words | grep and read, as an agent search | record a miss if the answer is found another way | BM-2 |
| Anything the graph answers with nothing | full-text, then grep | — | BM-8 |

This table is for the **code and docs**. Memory entries are covered by the per-store sections below. The two
differ because the corpus differs. Code and docs exist today and are already large enough that full-text and the
graph save reading (BM-6). `project-memory/` does not exist yet.

**What this does not change, and what it proposes.**
- **Unchanged:** the rules for all three caches below (full rebuild, rebuild when stale, fall back when absent) and
  R1–R8 apply as written.
- **Conflict with "The answer first" and the vision:** for code and docs, the measurements say full-text and the graph
  already save reading today. That contradicts "none of the three caches is needed today" and the vision's *who it is
  for: an agent retrieving an entry*. Changing either is EJ's call. The proposed wording is in
  `runs/20261012-caches-routing/vision-proposals.md`, and neither file has been edited.

## Rules for all three caches

These apply to whichever cache is built. They come from how the researched tools fail.

- **Full rebuild, never patched.** A live, incrementally updated index drifted silently from a clean rebuild: 4.3% of
  edges wrong, with every integrity check passing (`G-F5 drift`). Its makers decided drift cannot be measured cheaply
  (`G-F5c`). A full rebuild of this repo's code graph takes 0.94 s (`G-F12`); an FTS rebuild of 10,000 synthetic
  entries takes 0.53 s (`S-F13`).
- **Rebuild before answering when stale.** Before each query, compare the newest source file with the index and
  rebuild first if the source is newer. Build into a temporary file and rename it over the old one (`S-F9`, quoted:
  *"A stale index is worse than no index."*).
- **Fall back when absent.** If the cache file or SQLite's FTS5 is missing, the tool warns once and answers with grep
  (`S-F9`); the same for a missing embedding model (my reading, extending `S-F9`). A mistyped database path silently
  creates an empty database, which looks exactly like a stale one (`G-F5 drift`, failure mode 5), so the tool opens the
  cache read-only and treats "no such file" as absent.
- **Index only active entries**, the same set as `INDEX.md`, with `status` and `covers` stored beside each row
  (`V-F22`, my reading). Otherwise superseded entries come back looking current.

## SQLite full-text index

### Five whys

1. **Why a full-text index?** To find entries by their words, ranked, with a snippet, instead of grep's unranked list
   (`S-F1`, quoted: *"grep returns unranked matches."*).
2. **Why does ranking matter?** Every hit the agent opens costs context. In the one controlled study, BM25 used 5.8K
   tokens per question against 226K for an agent using grep over files, on its smallest corpus: 1,144 documents,
   1.7M tokens (`S-F4`).
3. **Why not build it now?** That study puts the point where BM25 overtakes the grep agent at around 10 million tokens
   of text, and the grep agent led at the smallest sizes (`S-F4`). At our entry size that is about 37,000 entries
   (`S-F5`, my reading via its 4-characters-per-token assumption). `INDEX.md` already lists every active entry. In the
   researcher's own test, at 10,000 synthetic entries a one-word grep took 0.038 s and a grep chain for a header
   question 0.06 s; at 50,000 the header chain took 0.15 s, and the one-word timing was invalid (`S-F13`). No study
   covers a corpus of a few hundred to a few thousand short entries (`S-F5`: not measured).
4. **Why might it be needed later?** `INDEX.md` stops being enough once it can no longer list every active entry under
   its size limit. The agent then loses the one-line scan of every entry, and ranked search is what replaces it (my
   reading).
5. **Why only as a cache?** The markdown is the source of truth, and the cache must be rebuildable and skippable (M6).

Structured questions such as "every active decision covering path X" or "what supersedes Y" do not need SQLite. A
short script reading the entry headers answers them in 0.1 s at 10,000 entries (`S-F13`). That measures time, not
tokens; my reading is that the script and an SQL query return the same list of entries, so the agent reads the same
amount either way (not measured).

### 5W1H

| | |
|---|---|
| **Who** | Built and rebuilt by a script with no model call. Read by any agent on demand. EJ decides to build it when the trigger fires. |
| **What** | One FTS5 table with `kind`, `status` and `covers` as `UNINDEXED` columns (`S-F2`). One row per active entry file: the research leaves the row grain open (`S-F17`); my reading is that an entry of one or two sentences is already one section. The default `unicode61` tokenizer: in the researcher's own one-row test, a plausible change to keep paths whole made ordinary queries return zero rows silently, and ids such as `D-0012` had to be quoted (`S-F16`). |
| **When** | Built when the trigger fires: `INDEX.md` can no longer list every active entry. Rebuilt before any query that finds it stale. Never read at session start. |
| **Where** | `project-memory/.cache/index.sqlite`, gitignored. |
| **Why** | The five whys above. |
| **How** | One stdlib `sqlite3` script, the smallest option in the SQLite node (§5, option B): rebuild to a temporary file and rename; compare modification times for staleness; fall back to `rg`. Nothing to install: SQLite 3.45.1 with FTS5 works here (verified 2026-10-12). |

## Vector index

### Five whys

1. **Why a vector index?** To find an entry by meaning when the question shares no words with it.
2. **Why can't grep or full-text search do that?** They match words. But the evidence does not show vectors winning on
   memory text. (They do win on some code tasks, `V-F5`, and on half the file-based pairs in `V-F3`.) On conversational
   memory, grep returned inline beat vector search for every harness and model pair (`V-F3`). On a 500,000-document
   corpus, BM25 beat vectors even on the questions built to favour them (`V-F4`). On decision-style records, a
   structured graph and a vector memory tool were "largely equivalent" on relevance, and plain notes search did no
   better on listing or supersession questions (s3-F34; `V-F1`).
3. **Why not build it now?** No measurement exists on a corpus shaped like `entries/` (`V-F11`: not measured).
   Anthropic's 2024 guidance is that under about 200,000 tokens a knowledge base can simply be put in the prompt
   (`V-F8`), roughly 400–650 entries (`V-F12`, my reading). This design does not do that (it never loads the whole
   tree), so this is only a bound: below it, retrieval quality is not what limits an agent (my reading). Vectors also
   add failures of their own: negation (`V-F20`), exact ids and paths (`V-F21`), and a second rebuild step that can lag
   the first (`V-F24`).
4. **Why might it be needed later?** If agents keep missing entries that exist because their words differ from the
   entry's. The trigger is a record of such misses: the entry existed, `INDEX.md`, grep and full-text search all missed
   it, and it was found another way (`V-F13`, my reading). How many misses justify building it is **EJ's number**. No
   source gives one.
5. **Why hybrid only?** On memory-style text, the positive results found combine vectors with keyword search (`V-F6`,
   `V-F7`; `V-F10` is unproven), and vectors alone were the weakest arm when results were returned inline (`V-F3`,
   `V-F4`). So the vector index comes after the full-text index, never
   instead of it.

### 5W1H

| | |
|---|---|
| **Who** | Built and rebuilt by a script with no model call except the embedding model itself. Read by any agent on demand, through the same command as full-text search. EJ decides to build it when the trigger fires. |
| **What** | One vector per active entry file, with the entry's `status`, `covers`, content hash and embedding-model id stored beside it (`V-F24`: a changed model makes every vector useless). Results merged with the full-text results by reciprocal rank fusion (vector node §Q5, from qmd's README). |
| **When** | After the full-text index exists, and after the miss record shows EJ's number. Rebuilt with the full-text index, in the same step, so the two cannot disagree (`V-F24`, my reading). |
| **Where** | `project-memory/.cache/`, beside `index.sqlite`, gitignored. |
| **Why** | The five whys above. |
| **How** | The smallest options in `V-F18`/`V-F19`: a static Model2Vec model with numpy (option A, no GPU) or `bge-small-en-v1.5` through FastEmbed (option B). Both are small next to the 16 GB GPU here. Embedding speed on this GPU is **not measured** (`V-F18`). No embedding runtime is installed today; numpy is (`V-F19`). |

## Code graph

### Five whys

1. **Why a code graph?** To answer structural questions about the code: what an edit touches, and whether the code an
   entry covers has changed.
2. **Why would memory need that?** For the drift check (`SOURCE_OF_TRUTH.md` line 75: mark a decision or fact whose
   code changed with no earlier change to the entry) and for "which entries cover the files I am editing".
3. **Why is git enough for both?** `covers:` names **paths**, not symbols, and is already a hand-kept index from entry
   to path (`G-F14`). Two `git log` calls compare the entry's last change with its paths' last change, in 0.00–0.01 s
   on this repo (`G-F12`; code-graph node §6). Git is the record itself, so it cannot drift.
4. **Why not add a graph for precision anyway?** An incrementally synced graph adds a silent failure that git does not
   have (`G-F5 drift`, 4.3% of edges wrong). A full-rebuild graph such as the repo's own does not drift (`G-F18`), but
   it covers Python only, so for other `covers:` paths it gives a silent partial answer (code-graph node §5, option B).
   The precision it buys, a one-line comment flagging a whole file, can be had by parsing only the changed file with
   Python's `ast` (code-graph node §5, option E). The deeper question, "is this entry still true", belongs to the
   background subagent that compares entries with the code (`SOURCE_OF_TRUTH.md` lines 68–73), not to a model-free
   script.
5. **Why might it be needed later?** Any one of the three conditions in the code-graph node's §6, each a test:
   - `covers:` starts naming functions or classes instead of files;
   - the check must answer about files not on any `covers:` list ("what does this change affect");
   - path-level flags raise too many false alarms. How many is **EJ's number**.

### 5W1H

| | |
|---|---|
| **Who** | The drift-check script, with no model call. EJ decides to build a graph if one of the three conditions holds. |
| **What** | Today: no graph. Git on `covers:` paths, plus an `ast` parse of changed Python files if precision is needed. If a condition holds: the repo's own `code_graph/code_graph.py` (Python only, deterministic, full rebuild, no incremental mode, `G-F18`) before any outside tool. |
| **When** | Today the check runs whenever `INDEX.md` is generated (my reading of `SOURCE_OF_TRUTH.md` line 75). A graph, if ever built, is rebuilt in full each time it is used. |
| **Where** | Nothing today. Later, `project-memory/.cache/code-graph.json`, gitignored. |
| **Why** | The five whys above. |
| **How** | Two `git log` calls per entry: `git log -1 --format=%at -- <entry file>` and the same for each `covers:` path (code-graph node §6). External indexers (codegraph) are not adopted: their win is measured on source-code architecture questions, not on memory (`G-F7`, `G-F14`), and they bring the drift in `G-F5 drift`. |

## What this changes elsewhere (proposed, not done)

- `SOURCE_OF_TRUTH.md` lists as undecided "how the script tells that the entry changed earlier than the code". The
  research suggests an answer for EJ to decide: compare `git log` times of the entry file and its `covers:` paths.
- `SOURCE_OF_TRUTH.md` line 104 can keep `.cache/` as written. This document says when each part of it is built.

## Not known

- Every trigger number is EJ's: the `INDEX.md` size limit (already open in `SOURCE_OF_TRUTH.md`), the number of
  recorded misses for vectors, and the false-alarm rate for the code graph.
- No measurement exists of any of the three on a project-memory corpus. All evidence is on other corpora: source code,
  chat memory, enterprise documents.
- The researchers' web reads went through extracts. `S-F*` quotes are not byte-checked (`sqlite-fts.claude.md`,
  header). `V-F*` quotes were checked against saved copies.
- The planted "tool that does not exist" check in the research was void: the names were readable in the run's
  `state.md` (see that file's log).
