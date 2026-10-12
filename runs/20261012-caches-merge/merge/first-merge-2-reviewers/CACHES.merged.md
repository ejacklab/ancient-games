# Memory Caches: SQLite Full-Text, Vector, Code Graph

> **Status: draft, not accepted by EJ. Merged 2026-10-12 by dsh (`deepseek-flash`) from Version A (`runs/20261012-caches-enhance/CACHES.md`) and Version B (`runs/20261012-caches-routing/CACHES.enhanced.md`), after reviews by agy, codex and opencode (`runs/20261012-caches-merge/reviews/`).**

> **Source research (Version A).** Written 2026-10-12 by Claude (`claude-opus-5-5`) from three research nodes in `runs/20261012-memory-caches/nodes/`: SQLite full-text (`sqlite-fts.claude.md`, ids `S-F*`), vector (`vector.claude.md`, `V-F*`) and code graph (`code-graph.opencode.stdout.md`, `G-F*`). The code-graph node uses `F5` twice; `G-F5 drift` means the drift study and `G-F5 Serena` means Serena.

> **Labels.** *Quoted* means the line rests on a finding id; *my reading* means it is my inference; *not measured* means nobody has measured it. The section **Measured here: development and testing** adds numbers measured on this repo, ids `BM-*`.

> **Review.** A blind review (`claude-sonnet-5-5`, `runs/20261012-memory-caches/nodes/review.claude.md`) returned REPAIR with 13 findings. It caught the planted defect (F-1), and the other 12 are fixed here. The fixes have not been re-reviewed.

> **When-to-use enhancement, 2026-10-12** (`runs/20261012-caches-enhance/`): three engines, rotated so each store got fresh eyes, answered *when to use this store at query time and what it costs*; the merge is the section **When to use which store** below. Caveats carried: one engine (claude) disclosed coordinating with another agent on the same question, so its answer is not independent; and every cost for a real `project-memory/` is `GAP`.

> **Measured enhancement, 2026-10-12** (`runs/20261012-caches-routing/`): the section **Measured here: development and testing** adds measurements on this repo and a routing rule for code and docs. It does not change the sections above or below it. It conflicts with "The answer first" and the vision for code and docs; that is left to EJ.

> **Vision:** `vision-statements/caches-memory-vision-statements.md` — moved out 2026-10-12 so the vision and the requirements each have one copy.

## The answer first

None of the three caches is needed today. `project-memory/` does not exist yet, so nothing has been measured on it.
My reading of the research is that at the sizes measured elsewhere, `INDEX.md`, grep and git answer the questions
each cache would answer. Each cache below has a
**trigger**: a condition that can be observed and that makes it worth building. None of them is built before its
trigger fires.

This follows the design's own rule: `.cache/` is optional, gitignored and rebuilt from the files, and its absence
must not stop anyone reading memory (`SOURCE_OF_TRUTH.md`; recommendation M4, M6). It also follows the repo's own
history of building graphs nobody queried (`docs/KNOWLEDGE_GRAPH_DESIGN.md` §1, quoted in `G-F21`).

This section is about the **memory entries**. The measured routing rule for **code and docs** is added below, in
**When to use which store**; for that corpus the answer differs, and changing the vision or this section is EJ's call.

## When to use which store

At query time the memory is answered by the files — `INDEX.md`, grep, git, or reading the entry — and a cache is
never the answer to a question the files answer. The table below merges three engines asked independently, one store
each: `claude` on the code graph, `codex` on the vector index, `opencode` on SQLite FTS5. The full 21-row table and
the 30-row cost table, with every disagreement kept, are in `runs/20261012-caches-enhance/DECISION-RULES.md` — the
run record. **This file is the live copy.**

**The rule.** **SQLite FTS5** is for a free-text question whose words are likely in the entry text, once `INDEX.md`
can no longer list every active entry under its size limit and ranked results with snippets save opened files
(`S-F1`, `S-F4`). **The vector index** is for the same discovery when the question's wording differs from the
entry's, once the documented miss trigger has fired (`V-F11`, `V-F13`, `M4`). **The code graph** is only for a
multi-hop structural question about Python code, after its trigger, and only as a lower bound (`G-F8`, `G-F17`,
`G-F18`, `M5`). Everything else is the files.

**Table 1 — memory entries (reasoned).**

| the question | store | if not, this | evidence |
|---|---|---|---|
| What do we already know about X? (free text, words likely in the entry) | **FTS5** — conditional on the size trigger | `INDEX.md`, grep, then read | S-F1, S-F4 |
| Which prior entry matches when my words differ from its? (find by meaning) | **vector** — conditional on the miss trigger | `INDEX.md`, grep, then read | V-F11, V-F13, M4 |
| What does changing F reach, several hops out, including files on no `covers:` list? | **code graph** — after its trigger; Python only; lower bound | grep imports and callers, then read | G-F8, G-F17, G-F18 |
| Which tests reach function F, so I know what to run first? | **code graph** — conditional, lower bound | grep test names, then run the suite | G-F12, R5.3 |
| An exact identifier, an error string, a known `file:line` | none | literal grep or filename lookup, then read | V-F7, V-F21, s3-F29 |
| Every active entry covering path X — completeness | none — a ranked top-k cannot prove completeness | exhaustive scan of `INDEX.md` and entry headers | V-F21 |
| Proving absence ("have we never recorded…") | none — no hit is not proof | exhaustive search, then read | V-F20 |
| A structured header question (status, `supersedes`, `depends_on`) | none | `INDEX.md` scan or a script over frontmatter; follow links by grep | V-F22, M13 |
| Why did we choose this, or why is this line like this? | none | the entry's **Why:** and its evidence; `git blame`, `git log -S` | s3-F4 |
| Did the covered code change after the entry was verified? | none | `git log -1 --format=%at` on the entry, then on each `covers:` path | G-F14, G-F12, M15 |
| Is this decision still true of the code? | none | read the entry and the code; the design gives this to the background subagent | SOURCE_OF_TRUTH:68–73 |
| What should I load when resuming? | none | `INDEX.md` and the task's `state.md` | M17, M18, M19 |
| A map of the whole repo | none | `PROJECT_OVERVIEW.md`, `INDEX.md` | M18, G-F18 |
| A `covers:` path that is not Python | none | git and grep | G-F18 |
| Is the graph I am about to query current? | none — do not check, rebuild whole | rebuild, or use git | G-F5, G-F18 |

**Costs, and where there are none.** Measured on other corpora or on this machine, never on a real
`project-memory/`: grep over 10,000 synthetic entries, 0.038 s for one word and 0.060 s for a structured chain
(`S-F13`); grep plus opening every hit, about 226K tokens per question (`S-F4`, `S-F13` — opencode's figure, and D3
records that the other two report no such measurement); an `INDEX.md` scan, under 0.01 s and minimal tokens
(`SOURCE_OF_TRUTH.md`); reading one entry, roughly 270 tokens by the 4-characters-per-token assumption (`S-F5`, not
measured); a git last-change lookup at the tool's timing resolution (`G-F12`). **`GAP` for everything that matters
most**: no FTS5-vs-grep measurement on short entries (`S-F5`), no vector measurement on a corpus shaped like
`entries/` (`V-F11`), no graph-vs-grep head-to-head on this repo's own questions (`G-F10`, `M21`), and no wrapper
exists to time a filtered graph query (`G-F18`).

**Still unresolved.** Six disagreements the three engines did not settle, kept as positions and not averaged (D1–D6
in the run record): whether FTS5 or the vector index comes first, or whether memory needs a store at all; whether the
FTS/vector benefit has been measured at all; the true token cost of grep-plus-open; the cost of `INDEX.md`; whether
`INDEX.md` carries `covers:` and status; and what counts as a *fired* trigger.

**Why no SQLite is visible in this repo.** Two reasons, and none is a rejection. The SQLite this repo does have,
`ancient_games/index.py`, indexes the **referee's journal**, not memory: it is the working precedent for this exact
pattern (7 tables, derived, ~8 ms per journal) but it answers a different question. And the memory cache is gated
behind a trigger that has not fired, because `project-memory/` does not exist yet. The same is true of the code
graph: `code_graph/code_graph.py` already exists, deterministic and full-rebuild, and is the option this document
names if that trigger fires.

A fourth reason belongs to the first draft. Its research asked only whether each cache is needed to search memory
*entries*, so it measured nothing on the questions asked during development and testing. The next section measures
those.

**Table 2 — code and docs (measured here).** The table below is for the **code and docs**; Table 1 is for memory
entries. The two differ because the corpus differs. Code and docs exist today and are already large enough that
full-text and the graph save reading (BM-6). `project-memory/` does not exist yet. Run:
`runs/20261012-caches-routing/`.

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

## Measured here: development and testing

EJ's aim is that development and testing get faster and cheaper in tokens. So this section measures all three stores
against grep on **this repo**: 490 files (123 `.py`, 367 `.md`), with 40 questions an agent asks while
developing and testing it. Run: `runs/20261012-caches-routing/` (results in `bench/results.md`, ids `BM-*` below).

The routing rule this measurement supports is **Table 2** in **When to use which store** above.

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

**What this does not change, and what it proposes.**
- **Unchanged:** the rules for all three caches below (full rebuild, rebuild when stale, fall back when absent) and
  R1–R8 apply as written.
- **Conflict with "The answer first" and the vision:** for code and docs, the measurements say full-text and the graph
  already save reading today. That contradicts "none of the three caches is needed today" and the vision's *who it is
  for: an agent retrieving an entry*. Changing either is EJ's call. The proposed wording is in
  `runs/20261012-caches-routing/vision-proposals.md`, and neither file has been edited.

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

---

## Core requirements

Acceptance criteria are checkable or they are questions for EJ. Where the research gives no number, the criterion
carries `OPEN:` rather than an invented value.

### R1 — Derived and disposable
The cache is computed from the markdown and never holds knowledge of its own (M4, M6).

- **R1.1** Deleting the cache and rebuilding from the files restores every answer. *Example:* `rm -rf
  project-memory/.cache/` → run the documented rebuild → the same query returns the same entries. (M6)
- **R1.2** Memory is fully readable with no cache present. *Example:* with `.cache/` absent, session start and an
  on-demand `grep` over `entries/` both work. (M6)
- **R1.3** The cache directory is ignored by git and a rebuild leaves `git status --short` clean. (M6)

### R2 — Full rebuild, never patched
- **R2.1** The documented rebuild regenerates the whole index from the files; no incremental update path exists.
  *Example:* the rebuild command has no "update" mode. (G-F5 drift)
- **R2.2** The index records what it was built from, so a stale one is detectable. *Example:* the index stores the
  newest source file's mtime or the commit, and the query tool compares before answering. (S-F9)

### R3 — Stale never answers
- **R3.1** Before answering, the tool compares the newest source file with the index and rebuilds first if the
  source is newer, building into a temporary file and renaming over the old one. (S-F9)
- **R3.2** A wrong path is never mistaken for an empty index: the cache is opened read-only and "no such file" is
  treated as absent. *Example:* point the tool at a typo'd path → it warns and falls back to grep, it does not
  create an empty database. (G-F5, failure mode 5)

### R4 — Absence degrades, it does not fail
- **R4.1** A missing cache file or a missing FTS5 warns once and answers with grep. (S-F9)
- **R4.2** A missing embedding model does the same. *(my reading, extending S-F9.)*

### R5 — Nothing is built before its trigger fires
Each cache has an observable trigger. This is the requirement that keeps the whole layer honest. The query-time
counterpart — which store to reach for once a trigger has fired — is the section **When to use which store** above.

- **R5.1 Full-text** — built only when `INDEX.md` can no longer list every active entry under its size limit.
  `OPEN: not measured — the limit is EJ's number` (S-F5, S-F13: not measured for a corpus of a few hundred to a few
  thousand short entries).
- **R5.2 Vector** — built only after R5.1 has fired *and* the logged misses outweigh the cache's cost. A "miss" is
  recorded when an entry existed and `INDEX.md`, grep and full-text search all missed it (V-F13).
  `OPEN: not measured — the miss count is EJ's number.` The vector index is hybrid only — appended to
  full-text results by reciprocal rank fusion, never instead of them (V-F3, V-F4, V-F6, V-F7; V-F10 is unproven).
- **R5.3 Code graph** — built only when one of three conditions holds: `covers:` starts naming functions or classes
  rather than files; the check must answer about files on no `covers:` list; or path-level flags raise too many
  false alarms. `OPEN: not measured — the false-alarm number is EJ's.` (code-graph §6, G-F14, G-F18)

### R6 — Only active entries, with their status
- **R6.1** The index holds the same set of entries as `INDEX.md`, each row carrying `status` and `covers`.
  *Example:* a superseded entry never appears in a search result as if current. (V-F22)

### R7 — An answer names its entry
- **R7.1** Every result prints the entry file it came from, so a human can open the source before acting.
  *Example:* search output names `entries/D-0012-*.md`. (M19)

### R8 — The rebuild stays cheap
- **R8.1** The documented rebuild completes without a model call, except the embedding step of R5.2.
  *Example:* rebuild with no model credentials available; the FTS and code-graph paths still work. (M4, M6)
- **R8.2** `OPEN: not measured — the budget is EJ's number.` Measured, for orientation only: 0.94 s (code graph,
  this repo, G-F12) and 0.53 s (FTS, 10,000 synthetic entries, S-F13). Nothing is measured on a real
  `project-memory/` corpus, because it does not exist yet.

## Unresolved after review

agy returned no review text in either round (the agy fields in the run's reviews are empty), so only codex and
opencode have positions. Each row is a point the two reviewers did not settle; nothing below has been averaged or
silently decided.

| point | codex | opencode |
|---|---|---|
| The scope of "The answer first" | Needs explicit scope: "none needed today" is about memory; code and docs results are retrieval-output evidence with unmeasured agent outcomes. | Take A's text; the merged status/scope text carries the memory-vs-code/docs distinction. |
| The rule at the top of **When to use which store**, that "a cache is never the answer to a question the files answer" | Over-broad: it would exclude every derived cache, whose information comes from the files; the vision keeps the files authoritative, it does not ban cheaper retrieval of the same information. Rewrite the rule. | Retain the memory "none" rows and the surrounding rule; the "none" rows are the useful part of the design. |
| The cost paragraph under **When to use which store** | Attribution alone cannot make the costs valid measurements: the 226K figure belongs to a different study, and the `INDEX.md` scan cost is unmeasured. | Retain the paragraph with the attribution and the `GAP` corrections. |
| The evidence id on the rationale row (`s3-F4`) | The error is resolvable from evidence: `s3-F4` concerns staleness, not rationale. | Replace `s3-F4`, or preserve the documentation disagreement for EJ. |
| The severity of the evidence-id substitutions on the completeness, absence and rationale rows | One wrong id in a table cell is low severity. | A pattern of three substitutions on never-rule rows, all traceable to the enhance run's own copy; medium severity. |
| The citation for the graph's Python-only limit | Cite `G-F12`. | Cite the code-graph node's §5 option B. |
| Whether the store-design conclusions need qualification | The vector experiment used a static embedding model, so it cannot establish the contextual embeddings discussed later; and the claim that positive memory results always combine vectors and keywords conflicts with `V-F3`. | Adopt B's threshold phrases and retain the other store text; A's hybrid-only rule is stated on `V-F3`'s inline half while `V-F3` reports vectors ahead on the file-based half. |
