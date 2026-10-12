# Merge — write the best version from Versions A and B (run 20261012-caches-merge)

You are the merger. You did not write either version, and you did not review them. Below you have:
- Version A and Version B, both in full;
- three independent round-1 reviews of them, by agy, codex and opencode;
- the same three reviewers' round-2 discussion.

Write the **best version**: one document that keeps the strengths of both.

## Rules
1. **Follow the reviewers' agreement.** Where the round-2 reviews agree on an outline or a point, follow it. Where
   they still disagree, do not pick silently. Add the point as a row in a final section, **Unresolved after review**,
   with each reviewer's position.
2. **Reuse the versions' own text.** Copy whole sections or table rows from A or B wherever possible. Write new text
   only to join them, and keep it short.
3. **Invent nothing.** Every number, finding id (`S-F*`, `V-F*`, `G-F*`, `BM-*`, `M*`, `D*`, `R*`) and claim must
   appear in A or in B exactly as written there. Do not add a number. Do not round a number differently.
4. **Keep the labels** a source attaches to a claim: *my reading*, *not measured*, *proposed*, `GAP`, `OPEN`.
5. **Keep the vision's never-rules.** Any change to the vision stays a proposal for EJ, never a decision.
6. **Header.** Start the document with a short status block: "Status: draft, not accepted by EJ. Merged 2026-10-12
   by dsh (`deepseek-flash`) from Version A (`runs/20261012-caches-enhance/CACHES.md`) and Version B
   (`runs/20261012-caches-routing/CACHES.enhanced.md`), after reviews by agy, codex and opencode
   (`runs/20261012-caches-merge/reviews/`)."
7. **Measured and reasoned rules stay apart.** If both a memory-entry routing table (A) and a measured routing table
   for code and docs (B) survive, keep them as two tables and say which corpus each covers.

## Output, exactly
Print the merged document between the lines `BEGIN_MERGED` and `END_MERGED`. Then print a merge-notes table between
`BEGIN_NOTES` and `END_NOTES`, with the columns `section | taken from (A / B / both / new) | reviewer support | note`.


## Version A

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
>
> **When-to-use enhancement, 2026-10-12** (`runs/20261012-caches-enhance/`): three engines, rotated so each store
> got fresh eyes, answered *when to use this store at query time and what it costs*; the merge is the section
> **When to use which store** below, and a blind verifier with a planted fabricated cost figure returned all four
> items PASS on this file's text. Caveats carried: one engine (claude) disclosed coordinating with another agent on
> the same question, so its answer is not independent; and every cost for a real `project-memory/` is `GAP`.

> **Measured enhancement, 2026-10-12** (`runs/20261012-caches-routing/`): the section **Measured here: development and
> testing** adds measurements on this repo and a routing rule for code and docs. It does not change the sections
> above or below it. It conflicts with "The answer first" and the vision for code and docs; that is left to EJ.

> **Vision:** `vision-statements/caches-memory-vision-statements.md` — moved out 2026-10-12 so the vision
> and the requirements each have one copy.

## The answer first

None of the three caches is needed today. `project-memory/` does not exist yet, so nothing has been measured on it.
My reading of the research is that at the sizes measured elsewhere, `INDEX.md`, grep and git answer the questions
each cache would answer. Each cache below has a
**trigger**: a condition that can be observed and that makes it worth building. None of them is built before its
trigger fires.

This follows the design's own rule: `.cache/` is optional, gitignored and rebuilt from the files, and its absence
must not stop anyone reading memory (`SOURCE_OF_TRUTH.md`; recommendation M4, M6). It also follows the repo's own
history of building graphs nobody queried (`docs/KNOWLEDGE_GRAPH_DESIGN.md` §1, quoted in `G-F21`).

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
exists to time a filtered graph query (`G-F18`). The last three are now measured on this repo's own code and
docs. See **Measured here: development and testing** below.

**Still unresolved.** Six disagreements the three engines did not settle, kept as positions and not averaged (D1–D6
in the run record): whether FTS5 or the vector index comes first, or whether memory needs a store at all; whether the
FTS/vector benefit has been measured at all; the true token cost of grep-plus-open; the cost of `INDEX.md`; whether
`INDEX.md` carries `covers:` and status; and what counts as a *fired* trigger.

**Why no SQLite is visible in this repo.** Three reasons, and none is a rejection. No `.db` is ever on disk — the
patterns are gitignored and the indexes are rebuilt on demand. The SQLite this repo does have, `ancient_games/index.py`,
indexes the **referee's journal**, not memory: it is the working precedent for this exact pattern (7 tables, derived,
~8 ms per journal) but it answers a different question. And the memory cache is gated behind a trigger that has not
fired, because `project-memory/` does not exist yet. The same is true of the code graph: `code_graph/code_graph.py`
already exists, deterministic and full-rebuild, and is the option this document names if that trigger fires.

A fourth reason belongs to the first draft. Its research asked only whether each cache is needed to search memory
*entries*, so it measured nothing on the questions asked during development and testing. The next section measures
those.

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
   it, and it was found another way (`V-F13`, my reading). How many misses justify building it is a **measured comparison** (`SOURCE_OF_TRUTH.md` § How each threshold is
found), not a number to guess. No
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
| **When** | After the full-text index exists, and after the logged misses outweigh the cache's cost. Rebuilt with the full-text index, in the same step, so the two cannot disagree (`V-F24`, my reading). |
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
   - path-level flags raise too many false alarms — the comparison is in `SOURCE_OF_TRUTH.md` § How each threshold
     is found. How many you will tolerate is the one policy value, and it is yours.

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
  `OPEN: not measured — the limit is the comparison in SOURCE_OF_TRUTH.md § How each threshold is found` (S-F5, S-F13: not measured for a corpus of a few hundred to a few thousand
  short entries).
- **R5.2 Vector** — built only after R5.1 has fired *and* the logged misses outweigh the cache's cost. A "miss" is
  recorded when an entry existed and `INDEX.md`, grep and full-text search all missed it (V-F13).
  `OPEN: not measured — the miss count is the comparison in SOURCE_OF_TRUTH.md § How each threshold is found.` The vector index is hybrid only — appended to
  full-text results by reciprocal rank fusion, never instead of them (V-F3, V-F4, V-F6, V-F7; V-F10 is unproven).
- **R5.3 Code graph** — built only when one of three conditions holds: `covers:` starts naming functions or classes
  rather than files; the check must answer about files on no `covers:` list; or path-level flags raise too many
  false alarms. `OPEN: not measured — the false-alarm comparison is in SOURCE_OF_TRUTH.md § How each threshold is found.` (code-graph §6, G-F14, G-F18)

### R6 — Only active entries, with their status
- **R6.1** The index holds the same set of entries as `INDEX.md`, each row carrying `status` and `covers`.
  *Example:* a superseded entry never appears in a search result as if current. (V-F22)

### R7 — An answer names its entry
- **R7.1** Every result prints the entry file it came from, so a human can open the source before acting.
  *Example:* search output names `entries/D-0012-*.md`. (M19)

### R8 — The rebuild stays cheap
- **R8.1** The documented rebuild completes without a model call, except the embedding step of R5.2.
  *Example:* rebuild with no model credentials available; the FTS and code-graph paths still work. (M4, M6)
- **R8.2** `OPEN: not measured — the budget is the comparison in SOURCE_OF_TRUTH.md § How each threshold is found.` Measured, for orientation only: 0.94 s (code graph,
  this repo, G-F12) and 0.53 s (FTS, 10,000 synthetic entries, S-F13). Nothing is measured on a real
  `project-memory/` corpus, because it does not exist yet.


## Version B

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


## r1 review by agy

### Strengths of A

- **Full two-domain query routing coverage:** [`version-A.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L41-L100) provides the 15-row decision table for markdown memory-entry questions (distinguishing free-text recall, meaning-based matching, multi-hop structural reach, exact identifiers, completeness scans, proving absence, structured headers, rationale, drift, and session startup) alongside the 8-row table for development and testing on code and docs ([`version-A.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L166-L176)).
- **Complete specification of Core Requirements (R1–R8):** Includes the full requirements framework ([`version-A.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L335-L395)) with checkable criteria (disposable/derived R1, full rebuild R2, staleness rejection R3, absence fallback R4, observable triggers R5, active entry filter R6, source naming R7, and rebuild cost bounds R8) required by the vision ([`caches-memory-vision-statements.md`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md#L8)).
- **Transparent ledger of costs, gaps, and disagreements:** Retains the cost evidence summary ([`version-A.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L74-L84)), notes explicit GAPs for real memory corpora, and preserves the six unresolved multi-engine disagreements (D1–D6) from [`DECISION-RULES.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L134-L165) without forcing a false consensus.
- **Answers EJ's architectural precedent question:** Incorporates the repo recon ([`version-A.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L90-L96)) explaining why SQLite is not visible in git (gitignored `.db`, [`ancient_games/index.py`](file:///home/smoke01/dev/ancient-games/ancient_games/index.py) indexing the referee journal rather than memory, and unbuilt `project-memory/`).
- **Complete provenance and review metadata:** Explicitly records the run lineage and caveats ([`version-A.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L16-L27)), including the enhancement runs and the link to the external vision file.

### Strengths of B

- **Strict alignment with the Vision on trigger authority ("EJ's number"):** Correctly attributes trigger thresholds directly to EJ ([`version-B.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L189-L190), [`L202`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L202), [`L228`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L228))—matching [`caches-memory-vision-statements.md`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md#L33) ("all three numbers are EJ's") and [`CLAUDE.md`](file:///home/smoke01/dev/ancient-games/CLAUDE.md#L78-L79) ("Never fill a gap with my own value").
- **Avoids citations to non-existent document sections:** Does not reference the unmerged/reverted phantom section `SOURCE_OF_TRUTH.md § How each threshold is found` that Version A repeatedly cites.
- **Compact focus on repo-measured routing:** Places the empirical development and testing benchmarks ([`version-B.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L28-L115)) immediately after "The answer first", directly answering EJ's speed and token cost objective for this codebase.
- **Sound architectural foundations for individual stores:** Fully preserves the 5 Whys and 5W1H analyses for SQLite FTS5, vector search, and the code graph.

### Errors and weaknesses

- `A:262-264`, `A:302-303`, `A:371`, `A:375`, `A:379`, `A:392`: Version A repeatedly asserts that trigger thresholds are determined by a "measured comparison (`SOURCE_OF_TRUTH.md` § How each threshold is found)". In [`SOURCE_OF_TRUTH.md`](file:///home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md), no such section exists (it was part of 77 unrequested lines added during an earlier run and reverted at EJ's instruction; see [`state.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/state.md#L75-L82)). This also contradicts the vision rule that all trigger thresholds are EJ's policy decisions.
  - *Source line showing error:* [`SOURCE_OF_TRUTH.md:1-127`](file:///home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md#L1-L127) (section absent); [`caches-memory-vision-statements.md:33`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md#L33).
  - *Severity:* High.
- `B:1-257`: Version B completely omits the "When to use which store" section (the query-time decision routing table for memory entries, the cost summary, the unresolved disagreements D1–D6, and the explanation of why SQLite is not visible). An agent querying memory entries has no routing guidance in Version B.
  - *Source line showing error:* [`DECISION-RULES.md:37-65`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L37-L65); [`version-A.md:41-100`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L41-L100).
  - *Severity:* High.
- `B:1-257`: Version B completely omits the Core Requirements section (R1–R8). It lacks the checkable acceptance criteria defining disposable caches, full rebuilds, staleness checks, fallback behavior, and active entry filters required by the vision.
  - *Source line showing error:* [`caches-memory-vision-statements.md:8`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md#L8); [`version-A.md:335-395`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L335-L395).
  - *Severity:* High.
- `A:66`: In the memory decision table, row "Why did we choose this, or why is this line like this?" cites `s3-F4`. `s3-F4` is StateTape (staleness from a code-graph diff), not rationale. The rationale synthesis finding is `s3-F21` / `SOURCE_OF_TRUTH.md`.
  - *Source line showing error:* [`DECISION-RULES.md:52`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L52); [`code-graph.opencode.stdout.md:309`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/code-graph.opencode.stdout.md#L309).
  - *Severity:* Medium.
- `A:141` and `B:68`: Both versions state for BM-8: "Full-text search on the file name found 2 of 3; grep found 1 of 3 and printed up to 8.7K characters." The benchmark results show `rg` (grep) scored `symbol hit@10 = 1` and `file hit@10 = 1` on C06 ([`results.md:205`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L205)) and C07 ([`results.md:210`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L210)), missing only C05 ([`results.md:200`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L200)). Grep found gold files for 2 of 3 questions, not 1 of 3.
  - *Source line showing error:* [`results.md:200`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L200), [`L205`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L205), [`L210`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L210).
  - *Severity:* Medium.
- `B:104-105`: Version B claims: "This table is for the code and docs. Memory entries are covered by the per-store sections below." This statement is inaccurate: the per-store sections below provide store architecture and 5W1H build triggers, not question-routing rules.
  - *Source line showing error:* [`version-B.md:134-240`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L134-L240).
  - *Severity:* Medium.
- `A:76-77`: Version A lists "grep plus opening every hit, about 226K tokens per question" without contextualizing that this figure comes from `S-F4`'s 1.7M-token general RAG corpus benchmark with a paths-only agent, not a memory corpus on this system.
  - *Source line showing error:* [`sqlite-fts.claude.md:57-58`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/sqlite-fts.claude.md#L57-L58); [`DECISION-RULES.md:146-148`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L146-L148).
  - *Severity:* Low.
- `B:1-15`: Version B omits the header provenance blocks detailing the enhance run, the routing benchmark run, and the pointer to [`caches-memory-vision-statements.md`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md).
  - *Source line showing error:* [`version-A.md:16-27`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L16-L27).
  - *Severity:* Low.

### Conflicts between A and B

1. **Trigger threshold determination: "Measured comparison in `SOURCE_OF_TRUTH.md`" vs "EJ's number"**
   - *What A says:* The thresholds for building vector indexes (miss count), code graphs (false-alarm rate), and rebuild budgets are defined by a "measured comparison (`SOURCE_OF_TRUTH.md` § How each threshold is found), not a number to guess" ([`version-A.md:262-263`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L262-L263), [`L302-303`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L302-L303), [`L371-392`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L371-L392)).
   - *What B says:* These thresholds are explicitly "**EJ's number**" ([`version-B.md:189`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L189), [`L202`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L202), [`L228`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L228)).
   - *Which is better supported and why:* **Version B is better supported.** The vision statement ([`caches-memory-vision-statements.md:33`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md#L33)) states: "Every trigger is observable, and all three numbers are EJ's." Furthermore, [`SOURCE_OF_TRUTH.md`](file:///home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md) does not contain a section titled "§ How each threshold is found". Version A cites a non-existent phantom section that was reverted during an earlier run ([`state.md:75-82`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/state.md#L75-L82)).
2. **Routing table scope: Dual tables vs Single table with phantom deferral**
   - *What A says:* Provides two explicit routing tables: a 15-row table for memory entries ([`version-A.md:56-72`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L56-L72)) and an 8-row table for code and docs ([`version-A.md:166-175`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L166-L175)), noting that the two differ because their underlying corpora differ ([`version-A.md:177-179`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L177-L179)).
   - *What B says:* Includes only the 8-row code and docs table, asserting that memory entries are covered by the per-store sections below ([`version-B.md:104-105`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L104-L105)).
   - *Which is better supported and why:* **Version A is better supported.** The per-store sections below do not route memory queries. Without A's table, an agent querying memory entries has no routing guidance for supersession, absence proof, exact identifiers, or drift checks. A's table is grounded in the 21-row table in [`DECISION-RULES.md:42-65`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L42-L65).
3. **Core Requirements (R1–R8): Retained vs Omitted**
   - *What A says:* Retains the 8 Core Requirements R1–R8 ([`version-A.md:335-395`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L335-L395)).
   - *What B says:* Omits Core Requirements entirely, terminating at line 257.
   - *Which is better supported and why:* **Version A is better supported.** The vision statement explicitly identifies [`CACHES.md`](file:///home/smoke01/dev/ancient-games/docs/memory-system/CACHES.md) as the document carrying Core Requirements R1–R8 ([`caches-memory-vision-statements.md:8`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md#L8)). Omitting them removes the architectural contract.
4. **Header and Recon Context: Retained vs Stripped**
   - *What A says:* Retains header notes on the enhance and routing runs, records D1–D6 disagreements, and answers EJ's question on why SQLite is not visible on disk ([`version-A.md:16-27`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L16-L27), [`L85-99`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L85-L99)).
   - *What B says:* Strips these sections out.
   - *Which is better supported and why:* **Version A is better supported.** The recon section directly answers EJ's prompt question ("why I don't see the sqlite"), grounded in [`recon.md:1-26`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/recon.md#L1-L26).

### Proposed merged outline

Version A should serve as the structural base, corrected by Version B's trigger wording and verified benchmark figures.

1. **Title and Frontmatter Notes**
   - *Action:* **Combine both.**
   - *Detail:* Take Version A's header ([`version-A.md:1-28`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L1-L28)), including research provenance, review notes, enhance run notes ([`runs/20261012-caches-enhance/`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/)), routing run notes ([`runs/20261012-caches-routing/`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/)), and the pointer to [`caches-memory-vision-statements.md`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md).
2. **The answer first**
   - *Action:* **Take from A** (identical in B).
   - *Detail:* Re-states that no cache is needed today for memory entries, each requires an observable trigger, and caches are optional and derived ([`version-A.md:29-40`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L29-L40)).
3. **When to use which store: Query routing**
   - *Action:* **Combine both with new routing index.**
   - *Detail:* Present two clearly demarcated sub-sections to allow single-lookup routing:
     - *Part 1: Markdown memory entries (15 questions)*: Take from Version A ([`version-A.md:41-73`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L41-L73)), with the citation fix on line 66 (change `s3-F4` to `s3-F21` / `SOURCE_OF_TRUTH`).
     - *Part 2: Code and docs development & testing (8 questions)*: Take from Version A ([`version-A.md:164-176`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L164-L176)) / Version B ([`version-B.md:91-103`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L91-L103)).
     - *New text needed:* A two-line lookup rule at the start of the section: "For memory entry questions (`project-memory/`), consult Part 1. For development and testing questions on code and docs, consult Part 2."
4. **Measured here: development and testing**
   - *Action:* **Combine both with factual repair.**
   - *Detail:* Take the benchmark section from Version A ([`version-A.md:101-163`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L101-L163)) / Version B ([`version-B.md:28-90`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L28-L90)). Correct BM-8 text to reflect [`results.md:205-210`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L205-L210): state that grep found gold files for 2 of 3 questions (C06 and C07) while printing up to 8.7K characters, rather than "1 of 3". Retain the note acknowledging the conflict with the vision regarding code/docs caches, leaving the decision to EJ ([`vision-proposals.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/vision-proposals.md#L1-L48)).
5. **Costs, gaps, and unresolved disagreements**
   - *Action:* **Take from A.**
   - *Detail:* Absent in B. Retain Version A's cost discussion, GAPs, and the D1–D6 disagreement records ([`version-A.md:74-89`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L74-L89)).
6. **Why no SQLite is visible in this repo**
   - *Action:* **Take from A.**
   - *Detail:* Absent in B. Retain Version A's recon analysis ([`version-A.md:90-100`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L90-L100)) explaining [`ancient_games/index.py`](file:///home/smoke01/dev/ancient-games/ancient_games/index.py), gitignored database files, and unbuilt memory.
7. **Rules for all three caches**
   - *Action:* **Take from A** (identical in B; [`version-A.md:189-206`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L189-L206)).
   - *Detail:* Full rebuild never patched, rebuild before answering when stale, fall back when absent, index active entries only.
8. **SQLite full-text index (5 Whys and 5W1H)**
   - *Action:* **Take from A** (identical in B; [`version-A.md:207-242`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L207-L242)).
   - *Detail:* Preserves BM25 rationale, 10M token crossover context, and stdlib implementation plan.
9. **Vector index (5 Whys and 5W1H)**
   - *Action:* **Take from B for trigger wording; otherwise combine.**
   - *Detail:* In Why-4 and 5W1H When ([`version-B.md:189-190`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L189-L190), [`L202`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L202)), use Version B's wording designating the miss threshold as "**EJ's number**", deleting Version A's citations to `SOURCE_OF_TRUTH.md § How each threshold is found`.
10. **Code graph (5 Whys and 5W1H)**
    - *Action:* **Take from B for trigger wording; otherwise combine.**
    - *Detail:* In Why-5 ([`version-B.md:228`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L228)), use Version B's wording designating the false-alarm tolerance as "**EJ's number**", deleting Version A's citation to `SOURCE_OF_TRUTH.md § How each threshold is found`.
11. **What this changes elsewhere (proposed, not done)**
    - *Action:* **Take from A** (identical in B; [`version-A.md:316-321`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L316-L321)).
    - *Detail:* Preserves proposals regarding git timestamp comparisons for drift checks.
12. **Not known**
    - *Action:* **Take from A** (identical in B; [`version-A.md:322-332`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L322-L332)).
    - *Detail:* Preserves open trigger items, absence of memory corpus data, and extract caveats.
13. **Core requirements (R1–R8)**
    - *Action:* **Take from A with trigger repairs.**
    - *Detail:* Absent in B. Adopt Version A's requirements framework ([`version-A.md:335-395`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L335-L395)). Repair R5.1, R5.2, R5.3, and R8.2 by removing all references to `SOURCE_OF_TRUTH.md § How each threshold is found` and replacing them with `OPEN: EJ's number`, harmonizing R1–R8 with the vision.

### Not checked

- **Other reviewers' Round 1 outputs:** Did not inspect [`reviews/r1-codex.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/reviews/) or [`reviews/r1-opencode.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/reviews/), preserving strict reviewer independence for Round 1.
- **Raw web source verification:** Did not byte-check cited external URLs (arXiv papers, GitHub issues/READMEs, sqlite.org docs); accepted research node citations as recorded in [`sqlite-fts.claude.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/sqlite-fts.claude.md), [`vector.claude.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/vector.claude.md), and [`code-graph.opencode.stdout.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/code-graph.opencode.stdout.md).
- **Execution of benchmarks or test suite:** Did not run local shell commands or execute scripts (`pytest`, `bench.py`, or `code_graph.py`), relying strictly on saved artifacts ([`results.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md) and [`runtime-recall.json`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/nodes/runtime-recall.json)).


## r1 review by codex

### Strengths of A

- **My reading:** A is the better starting point for memory-entry routing. Its table covers discovery, exact identifiers, completeness, absence, lifecycle links, rationale, drift, resumption and non-Python paths (A:56–72). B disperses that guidance across its per-store explanations.
- A includes concrete acceptance criteria for disposal, rebuilding, missing caches, source attribution and triggers (A:340–394). These make the design more reviewable, although several criteria need correction below.
- A preserves disagreements and acknowledges that the code-graph contributor coordinated with another agent. The evidence record explicitly distinguishes disagreement from corroboration. [DECISION-RULES.md:21–35, 132–164](/home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md:21)

### Strengths of B

- **My reading:** B foregrounds the development/testing questions the user actually wants answered: definitions, callers, affected tests, rationale, configuration and concepts (B:93–102). A contains the same development table and benchmark section.
- The principal benchmark figures match the saved results: category scores, output means, rebuild times and the 14.68 ms maximum. Both versions disclose unequal output formats, exclusion of misses and the absence of an end-to-end agent trial. [results.md:13–28, 30–102, 276](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md:13)
- B clearly leaves the proposed expansion from memory retrieval to code/docs retrieval to EJ (B:111–114). The proposal file is explicitly for acceptance, amendment or rejection. [vision-proposals.md:3–6](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/vision-proposals.md:3)
- **Evidence strength, shared by both:** Codex authored the questions and initial gold; five Claude agents checked the categories; opencode authored the harness; Claude audited and repaired it. This is one repository and one 40-question set, with 6–10 questions per category, four runtime-recall questions and three subprocess questions—not independent replications. The repaired harness and revised prose were not re-reviewed. [routing/state.md:37–60, 67–76](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/state.md:37)

### Errors and weaknesses

- **A:262 — high.** A replaces EJ’s vector threshold with a measurement-decided comparison; A:276 and R5 repeat that change. The cited comparison method is a **draft proposal**, while the settled vision says all three trigger numbers belong to EJ. A:324 simultaneously retains the old ownership statement. Sources: [enhance/SOURCE_OF_TRUTH.md:3, 165–180](/home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/SOURCE_OF_TRUTH.md:165), [vision:33](/home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md:33). Measurements can inform EJ’s decision; they cannot silently replace it.

- **A:43 — medium.** “A cache is never the answer to a question the files answer” would exclude every legitimate derived cache: its information necessarily comes from files. The vision requires files to remain authoritative and readable without caches; it does not prohibit cheaper retrieval of the same information. Source: [vision:25–29, 34](/home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md:25).

- **A:18 — medium.** The claimed blind verification “on this file’s text” overstates the recorded check. The verifier examined `DECISION-RULES.md`, and found the planted alteration partly by diffing against the clean copy. That does not independently validate the final A document or its later threshold changes. Source: [enhance/run-report.md:15–17, 28–39](/home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/run-report.md:28).

- **A:75 — medium.** The paragraph mixes measured timings with unsupported costs. The 226K-token figure belongs to a 1,144-document enterprise benchmark, not the synthetic 10,000-entry grep test; “opening every hit” is not its established mechanism. The claimed `INDEX.md` scan under 0.01 s also has no measurement. Sources: [S-F4:55–60 and S-F13:98–107](/home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/sqlite-fts.claude.md:55), [DECISION-RULES.md:149–151, 191–193](/home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md:149). The primary paper confirms the token figures but describes accumulated model usage with bounded search/read tools. [BM25 paper, §4.4 and Appendix C.2](https://arxiv.org/html/2607.26497v3)

- **A:90 — low.** Gitignored does not mean absent from disk. Three SQLite files currently exist under `runs/20261012-caches-routing/bench/.cache/`. The benchmark record itself names those persistent files. Source: [bench/README.md:40](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/README.md:40). The inherited recon explanation is wrong.

- **A:197; B:124 — high.** Comparing only the newest source mtime cannot guarantee “stale never answers.” **My counterexample:** delete an indexed entry without making a surviving file newer than the cache; the condition never rebuilds, and the deleted entry remains searchable. Preserved timestamps create another failure. The source records this heuristic, alongside content-hash alternatives, but establishes no stale-answer guarantee. Source: [S-F9:80 and S-F15:115–120](/home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/sqlite-fts.claude.md:115). A:352–357 elevates the incomplete heuristic into acceptance criteria.

- **A:67; B:216 — high.** Last modification of an entry is not its last verification against code. An unrelated entry edit can hide code changes since verification. The cited memory requirement explicitly binds staleness to the **verified revision**, and describes diffing covered paths from that revision. Source: [RECOMMENDATION.md:44, 194–198](/home/smoke01/dev/ancient-games/runs/20261011-project-memory-engines/RECOMMENDATION.md:194). Git is the right substrate; this comparison is the wrong baseline for the stated verification question.

- **A:124; B:51 — medium.** The table calls the character metric “first right answer,” although it stops at the first line naming a gold **file**. Later statements that the caches “save reading” also exceed what was measured. The caveats are good but contradict these summaries. Source: [results.md:26–28](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md:26). This is evidence about printed output, not answer completion, agent tokens or development time saved.

- **A:138; B:65 — medium.** BM-7 has the wrong unit and aggregation description. The coverage reducer produces **test-file sets**; 0.78 is the mean of four question-level recalls, not the overall share of individual tests found. The recorded file counts imply graph recall of 8/13 across question/file instances, versus 4/13 for grep/FTS/hybrid. Sources: [derive_maps.py:1–3, 22–32](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/cov/derive_maps.py:1), [runtime-recall.json:2–109](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/nodes/runtime-recall.json:2). Keep 0.78, but label it macro-average test-file recall, n=4.

- **A:141; B:68 — medium.** “Grep found 1 of 3” needs a completeness qualifier. Grep hits C06 and C07, but retrieves only half C07’s gold files. Thus it finds something relevant for 2/3 questions and a complete gold set for 1/3. Source: [results.md:200–214](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md:200).

- **A:153; B:80 — medium.** The experiment is described as testing “the vector index” without identifying its embedding model. It tests `minishlab/potion-base-8M`, a static Model2Vec model. Those results do not establish the performance of the alternative contextual embeddings discussed later. Sources: [build.py:50–51](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/build.py:50), [V-F18:206–220](/home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/vector.claude.md:206).

- **A:173; B:100 — medium.** Configuration coverage has an undisclosed benchmark defect: E02’s gold answer is `pyproject.toml`, but all search routes are restricted to `.py` and `.md`. Its failure is therefore partly corpus exclusion, not retrieval quality. Sources: [queries.json:681–695](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/queries.json:681), [chunk.py:4, 38](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/chunk.py:38). An actual agent also needs a manifest/config-file route.

- **A:168; B:95 — medium.** The development table omits the graph’s Python-only scope and the warning that a nonempty caller/test result can still be incomplete. Falling back only on an empty answer does not address missing edges in a nonempty answer. Sources: [G-F12:119–120](/home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/code-graph.opencode.stdout.md:119), [runtime-recall.json:90–109](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/nodes/runtime-recall.json:90). Put these limits in the lookup table.

- **A:177; B:109 — medium.** Saying R1–R8 apply unchanged does not resolve their mismatch with code/docs retrieval. A’s R5.1 requires an overflowing memory index; R6 requires active-entry status and `covers`; R7 requires an entry filename. These cannot apply literally to arbitrary code nodes and documentation chunks. Source: [A:370–387](/home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md:370). B additionally references R1–R8 without including or directly linking their definitions.

- **A:265; B:191 — medium.** “The positive results found combine vectors with keyword search” is too broad even for memory-style text. V-F3 reports vector-only outperforming grep in five of ten file-delivery harness/model pairs. Hybrid-only can remain a proposed policy, but the evidence does not compel it. Source: [V-F3:60–68](/home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/vector.claude.md:60).

- **A:66 — low.** The rationale row cites `s3-F4`, which concerns StateTape’s staleness maintenance. The relevant rationale finding is `s3-F21`, also used by A’s underlying decision record. Sources: [research INDEX.md:119, 136](/home/smoke01/dev/ancient-games/docs/research/20261011-agent-memory-graph-r2/INDEX.md:119), [DECISION-RULES.md:52](/home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md:52).

### Conflicts between A and B

- **Who decides thresholds.** A:262–276 substitutes measured cost comparisons; B:189–202 retains EJ’s chosen miss count. **B is better supported:** the settled vision reserves the numbers for EJ, and V-F13 explicitly calls the threshold EJ’s rather than a research finding. A’s comparison method is useful as a proposal. [vision:33](/home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md:33), [V-F13:165–168](/home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/vector.claude.md:165).

- **Graph for exact lookup.** A:53 says the graph is only for multi-hop questions, and A:62 routes exact identifiers to files. B:95–97 proposes graph lookup for definitions and callers. A’s later table repeats B, so this is also an internal conflict in A. **B’s proposal is better supported for finding Python candidates in this experiment:** graph and grep tie at 0.75 on exact identifiers, with smaller graph output. **A’s caution is better supported for exhaustive call sites and absence claims.** These are different question contracts and need separate rows. [results.md:34–40, 215–229](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md:34), [G-F15:58–60](/home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/code-graph.opencode.stdout.md:58).

- **Finding rationale versus supplying rationale.** A:66 says no cache for “why”; B:99 proposes full-text to locate the relevant documentation. **B is better supported for discovery; A for answering:** BM-4 measures retrieval hits, while the memory design requires reading the decision and evidence before relying on it. [results.md:68–78](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md:68), [SOURCE_OF_TRUTH.md:114–117](/home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md:114).

The benchmark sections otherwise agree and derive from the same run. Their agreement provides no additional independent evidence.

### Proposed merged outline

1. **Status, scope and EJ’s pending decisions — combine both.** Link the settled vision; distinguish current memory scope from proposed code/docs expansion. Keep trigger ownership explicit.
2. **One question-to-route table — combine both, with new text.** Use A’s memory coverage and B’s development rows. Include corpus, prerequisite, route, fallback and answer limitation in each row. Add configuration files, function behaviour, exhaustive callers and dead-code questions.
3. **Shared never-rules — take from A, corrected.** Preserve disposal, full rebuild, on-demand reads and authoritative files. Add a checkable session-start prohibition and a freshness contract covering deletion and model changes.
4. **Build triggers — combine both.** Keep B’s EJ-owned thresholds; present A’s measurement comparisons as proposed evidence for EJ. Define code/docs triggers only through an explicit vision proposal.
5. **Three store designs — combine both.** Scope active-entry filters to memory, identify graph language coverage, and specify consistent publication of FTS/vector rebuilds.
6. **Development/testing evidence — take from B, corrected.** Name the embedding model, metric units, corpus exclusions, cold-start costs and exact sample sizes. Retain the full-suite safeguard.
7. **Acceptance criteria — take from A, corrected.** Separate common cache criteria from memory-specific and proposed code/docs criteria.
8. **Evidence provenance and unresolved questions — combine both.** Name each check’s author, distinguish self-checks from independent checks, and preserve unmeasured outcomes and pending EJ decisions.

### Not checked

- I did not rebuild caches, rerun benchmarks or execute tests.
- I checked the saved local evidence and selected primary web sources: the BM25 scaling paper, codegraph drift report and Anthropic guidance. I did not independently verify every external research citation.
- End-to-end token savings, development time saved, graph-ordered testing benefits and real project-memory retrieval remain unmeasured.
- No files were changed, and no other reviewers’ reviews were consulted.


## r1 review by opencode

I'll start by reading the two versions and their supporting evidence.
Now let me read the evidence sources in parallel.
I have enough verified material. Here is the review.

---

# Round 1 review — `20261012-caches-merge`

**Bottom line up front:** B is not a second design. It is A with one section removed — the memory-entry routing table — plus the cost table, the disagreements, the "why no SQLite is visible" answer, and all of R1–R8. B's remaining text is byte-identical to A's except for four threshold wordings and one cross-reference sentence. So the comparison reduces to: is the memory-entry routing layer worth keeping, and are A's threshold wordings or B's better? I find the answer is yes, and B's.

## Verification method

I checked every number in the shared "Measured here" section against `runs/20261012-caches-routing/bench/results.md`, `nodes/bench-run.txt`, `bench/results.json`, `nodes/runtime-recall.json`, `nodes/gold-verdicts.json` and `nodes/audit-0.json`; every research figure against `runs/20261012-memory-caches/nodes/`; A's routing section against `runs/20261012-caches-enhance/DECISION-RULES.md`; and both against the vision.

**All 40 shared BM-1…BM-9 figures trace exactly.** Category hit rates, the `chars` column, the BM-6 means and counts (26/25/19/26/13), BM-7 (graph 0.7825→0.78, rg/fts/hybrid 0.5925→0.59, vec 0.0425→0.04), the rebuild times and byte sizes, 180/180 determinism, 37 correct + 3 incomplete, 529 tests in 31.0–33.3 s, the 15 ms / 14.68 ms bound, and the C01/C02 recalls of 0.33 and 0.8 are all correct. The research side also traces: `S-F4` (1,144 docs, 1.7M tokens, 5.8K vs 226K, ~10M crossover), `S-F5` (~37,000 entries, 4-chars/token), `S-F13` (0.038 s / 0.060 s / 0.53 s / 0.104 s), `S-F16` (0 rows silently, `D-0012` needs quoting — verbatim), `S-F2`, `S-F9` ("A stale index is worse than no index"), `G-F5` (4.3%), `G-F5c`, `G-F12` (0.94 s), `G-F21`, `V-F8`/`V-F12` (200,000 tokens → 400–650 entries), `V-F18`/`V-F19` (RTX 4070 Ti SUPER 16 GB, speed GAP, numpy only), `V-F22`, `V-F24`, and M4/M6/M13/M15/M17/M18/M19/M21. That is a strong result and both versions deserve credit for it.

### Strengths of A

- **It is the only version that answers both question classes.** A has a routing table for memory entries (A:56–72) and one for code and docs (A:166–175), and it says why they differ (A:177–179: "The two differ because the corpus differs. Code and docs exist today… `project-memory/` does not exist yet"). That is the design's actual scope.
- **The memory table's "none" rows are the useful part.** A:62–72 routes exact identifiers, completeness, proof of absence, structured headers, rationale, the drift check, "is this still true", resume-loading, repo map, non-Python `covers:`, and graph freshness — eleven real questions an agent asks, all to `none`, each with a named alternative and an evidence id.
- **It keeps the disagreements as disagreements.** A:85–88 carries all six (D1–D6) as positions, correctly summarised against DECISION-RULES.md:136–160, with no averaged winner.
- **It states the proxy's limits exactly as the audit found them** (A:115–121), including "No agent was run end to end", and it separately flags that the graph's BM-6 mean is over20 questions only (A:151–152).
- **It leaves the vision conflict to EJ and says the files were not edited** (A:184–187), with the right pointer to `vision-proposals.md`.
- **Its provenance header is honest about the merge**: A:16–20 records the enhance run, that the merge is A's "When to use which store" section, and that claude's answer was not independent.
- **"Why no SQLite is visible in this repo"** (A:90–95) is a genuine answer to EJ's question, traceable to `recon.md` via DECISION-RULES.md:166–182.

### Strengths of B

- **B's three threshold rewordings are better than A's.** A:262, A:276 and A:302–303 tell the reader the threshold is "the comparison in `SOURCE_OF_TRUTH.md` § How each threshold is found". That section exists **only** in `runs/20261012-caches-enhance/SOURCE_OF_TRUTH.md:165` — the live `docs/memory-system/SOURCE_OF_TRUTH.md` has no such section and no such string. B:189, B:202 and B:228 say "**EJ's number**", which is what the vision actually says (vision:33, "all three numbers are EJ's") and is findable. A points a reader at a file they will not find; B does not.
- **B has one table, one reading, one conflict paragraph, adjacent** (B:91–114). A puts ninety lines between the memory table and the sentence explaining that it applies to a different corpus (A:177). A reader in a hurry can reach B's routing rule without passing a second table.
- **B:99 states BM-4 correctly as a tie** ("ties hybrid on hits; prints less in total"), which is the codex repair at `state.md:74`.
- **B is shorter for a reason that could be defended**: if EJ decides the caches serve memory entries only, B is the whole document.

### Errors and weaknesses

- **B:104–106 — B has no memory-entry routing at all, and asserts the per-store sections cover it.** They do not. B's SQLite/vector/code-graph sections say *why a store would be built* and *what it would contain*; none says *which store for which question*. So in B an agent asking "which memory entries cover this function", "what supersedes this decision", "has this entry drifted", or "have we ever recorded a restriction against this" finds no row. **Severity: high** — it fails the usability criterion outright, and the sentence that hides it is the whole defence.
- **B:109–110 — dangling cross-reference to requirements B does not contain.** B says "the rules for all three caches below … and R1–R8 apply as written", but B ends at B:256 with "Not known" and has no `## Core requirements`. The vision names this file as the requirements source: vision:8, "**Drawn from:** `docs/memory-system/CACHES.md`, which carries the core requirements (R1–R8) this vision serves." Removing them also removes R1 ("never the source of truth"), R1.1 (the delete-and-rebuild acceptance test) and R5 (the triggers). **Severity: high.**
- **A:82 — "The last three are now measured on this repo's own code and docs" over-claims.** Of the four GAPs listed at A:79–82, the bench closes the graph-vs-grep head-to-head and (arguably) the filtered-query wrapper. It does **not** close "no vector measurement on a corpus shaped like `entries/`" — the corpus was 490 `.py`/`.md` files, and A:122 says so itself two hundred lines earlier ("None of this is a project-memory corpus"). **Severity: medium** (self-contradictory within one file).
- **A:63 — wrong evidence id on the completeness row.** "a ranked top-k cannot prove completeness" is cited to `V-F21`, which is "Exact identifiers and rare terms" (`vector.claude.md:240`). The finding that says top-k cannot enumerate is `V-F23` (`vector.claude.md:259`, "Top-k cannot enumerate or prove absence"), and the run record cites `V-F1, V-F23, S-F13, G-F14` (DECISION-RULES.md:47). **Severity: medium** — it is the evidence behind a never-rule.
- **A:66 — wrong evidence id on the rationale row.** "Why did we choose this" is cited to `s3-F4`, which is StateTape reading staleness off a code-graph diff (`code-graph.opencode.stdout.md:309`) — nothing to do with rationale. The run record cites `M19, s3-F21, SOURCE_OF_TRUTH` (DECISION-RULES.md:52). A picked up the `s3-F4` from the enhance run's own `CACHES.md:66`, which disagrees with its own `DECISION-RULES.md`. **Severity: medium.**
- **A:18–20 — the verifier claim is stated in a way the run record contradicts.** A says "a blind verifier with a planted fabricated cost figure returned all four items PASS on this file's text". Per `runs/20261012-caches-enhance/run-report.md:30–39`, the verifier on the *planted* file returned "item 1 FAIL, items 2–4 PASS, `VERDICT: REPAIR`" — it caught the plant; the all-four-PASS result was on the *unplanted* file; and "blind" is disputed by the run's own caveat, that the verifier "confirmed the alteration by diffing the planted file against the clean `DECISION-RULES.md`" because "both files sit in the same run folder". A reports the flattering half and drops the caveat. **Severity: medium.**
- **A:131 / B:58 — the graph cell for BM-4 is marked `n/a` when it was measured and scored 0.** `results.md:76` gives graph `0.0 | 0.0 | -- (0) | 38.0 | 0.0005` for category D, and `results.md:251` shows D05 with a graph row. The audit already flagged this exact trap: "Graph's category-D row is over 2 questions while the other routes' rows are over 8, and its 0.0 hit@5 with 38 chars sits next to them without saying so" (`audit-0.json`, last low finding). `n/a` is right for BM-5 (`results.md:88`) and wrong for BM-4. **Severity: medium** — it converts a measured zero into an absence.
- **A:141–142 / B:68–69 — "Full-text search on the file name found 2 of 3; grep found 1 of 3" is wrong under the plain reading.** From `results.json`: rg hit a gold file on C06 and C07 (missed C05); fts hit on C06 and C07 (missed C05). Both found **2 of 3**. "1 of 3" is true only under an unstated criterion — questions where the route found *every* gold — which the sentence does not say and which sits beside "The graph returns nothing", inviting the plain reading. (Under a gold-file count it is 3 of 4 and 2 of 4, which is neither.) **Severity: medium** — same number in both versions.
- **A:213–215 / B:140–142 — the strongest token number in the document carries an omitted limit.** `S-F4`'s own limits record: "The File-System Agent's grep returns paths only, not lines, which is weaker than `rg` with context" (`sqlite-fts.claude.md:58`). The 226K baseline is that handicapped agent, on one vendor preprint. The document carries the figure three times (A:76, A:213, DECISION-RULES.md:79) without this caveat. **Severity: medium.**
- **A:104 / B:31 — "4.8 MB" is unsourced.** The corpus is recorded as `{files: 490, files_py: 123, files_md: 367, chunks: 4021}` in `results.json`, with no byte total in `results.md`, `results.json`, `bench-run.txt` or `design.md`. Recomputing `bench/chunk.py`'s own selection (`git ls-files '*.py' '*.md'` minus the two excluded run folders) gives 4,703,239 bytes = **4.70 MB**. So 4.8 MB matches no source and is ~2% off. This is the same defect class as the earlier blind review's F-1 ("500 files"). **Severity: low.**
- **A:112–114 / B:39–41 — only the 5 high audit findings are reported; the 9 low ones are not.** Two of those lows bear directly on claims in the section: "rg's seconds are about 16% high" because each query spawns a `git ls-files` (`audit-0.json`, finding 12) undercuts BM-9's speed bound; and "vec returns 9.28 paths on average… the minimum is 7" (finding 6) undercuts the vec row. **Severity: low** individually, but the disclosure is presented as the full audit outcome and is not.
- **Neither version discloses that the corpus snapshot was unstable during the build.** `runs/20261012-caches-routing/state.md:48`: the builder "noticed `CACHES.md` being edited mid-run by the parallel session, so the numbers must be re-run on a stable snapshot." `state.md:59` records node 3 as "run once", and I find no confirmation it was re-run. **Severity: medium** — a self-identified stability problem, unclosed and undisclosed.
- **A:172 / B:99 (shared) and A:310 / B:235 — "Today: no graph" contradicts the measured graph.** The Code graph 5W1H says "Today: no graph", and A:94 says the graph is "gated behind a trigger that has not fired"; both files then report a real graph rebuild in 0.89 s and per-question graph hits at BM-1/BM-3. The distinction (no graph *for the memory drift check*; `code_graph/code_graph.py` exists and was measured *for code*) is real but is never drawn. **Severity: medium.**
- **A does not flag a cross-run conflict that both versions create.** A:168 routes "Where is function or method X defined?" to the code graph (BM-1:0.75,43 chars). DECISION-RULES.md:58 routes the same question to **`none`** — grep — because "3,874 unresolved calls against 2,000 call edges means 'no callers' would be a silent partial answer". One table is measured, the other is reasoned, and the merged document puts them side by side with no reconciliation and no flag to EJ. **Severity: medium.**
- **A:3–4 / B:3–4 — the header is stale in both.** "Two numbers come from checks the researchers wrote and ran themselves (`S-F13`, `G-F12`)" now sits above a section containing ~30 first-party measured numbers from a different run. A:22–24 fixes this for A by adding the routing-run provenance paragraph; B's header (B:3–14) does not, so B's label block contradicts its own body. **Severity: low** for A, **medium** for B.
- **B:3–4 — B attributes the whole file to `claude-opus-5-5`, including a section B did not write.** The routing section was written by the routing run's main session (`state.md:61`), and the routing run's engines were codex `gpt-6.1-sol`, opencode, Claude subagents and `claude-sonnet-5-5` for review (`state.md:10–16`). B never says so. A does (A:22–24). **Severity: medium** for B.
- **A:195 / A:392 vs A:143 — the graph rebuild is 0.94 s in two places and 0.89 s in a third.** `G-F12` measured `code_graph.py .` at 0.94 s (`code-graph.opencode.stdout.md:117`); the bench's graph build was 0.892 s. Both are correct on their own corpora, but a reader sees two numbers for one thing with no reconciliation. **Severity: low.**
- **Neither version names who wrote the routing tables.** A:107–123 and B:34–49 account for the questions, the gold, the harness and the audit — and not for the deliverable, the routing rule itself, which in both cases was written by the session that also ran the bench (`state.md:61`). **Severity: low.**

### Conflicts between A and B

1. **Memory-entry routing.** A carries a 14-row table (A:56–72); B asserts the per-store sections cover it (B:104). **A is better supported.** The run record holds the 21 rows the live table was cut from (DECISION-RULES.md:42–64), each with engine-by-engine agreement and evidence ids. B's claim is not merely thin, it is false about its own file: none of B's per-store sections routes a question. B's brevity is real, but the cost is a whole question class.
2. **The requirements.** A carries R1–R8 (A:335–394); B references them and lacks them (B:109). **A wins decisively.** The vision points at this file for R1–R8 (vision:8) and R5 is where the three triggers live — the never-rule "never built before its own trigger fires" (vision:33) has no home in B except scattered `When:` rows.
3. **Threshold wording.** A points to a comparison method in a section that exists only in a run-folder copy of `SOURCE_OF_TRUTH.md` (A:262, 276, 302); B says "EJ's number" (B:189, 202, 228). **B wins.** A reader cannot open `docs/memory-system/SOURCE_OF_TRUTH.md` and find § "How each threshold is found" — I checked; it is not there. And the vision itself says "all three numbers are EJ's" (vision:33). B's phrasing is the one that survives contact with the repo.
4. **Section order.** A puts memory routing before the code/docs measurement; B puts the measurement immediately after "The answer first". **A wins on vision fit.** B's order reads as if the measurement supports "None of the three caches is needed today" (B:18) — it does the opposite, and B has to say so 90 lines later (B:111–113). A's order keeps the design's stated subject first and flags the measurement's different corpus at the point of use.
5. **Provenance.** A's header records where the routing section came from and that it conflicts with the answer-first; B's header does not. **A wins**, for the reasons in the stale-label and attribution errors above.

### Proposed merged outline

Take **A** as the base — it is the only version with the full scope — and apply B's wording fixes. Order as listed.

1. **Header / provenance** — *combine both.* Take A:16–27 (both run pointers, the claude-independence caveat, the vision path). Add B's shorter "Labels" wording only if it removes A's now-stale "Two numbers come from checks the researchers wrote and ran themselves", which the routing section invalidates. *New text needed:* one line stating that B's "EJ's number" wording was adopted and why (the cited `SOURCE_OF_TRUTH.md` section exists only in the enhance run's copy) — otherwise a future editor will "restore" A's wording.
2. **The answer first** — *take from A* verbatim. Both are identical (A:29–39 = B:16–26). Keep the `G-F21` / `KNOWLEDGE_GRAPH_DESIGN.md` citation; it traces.
3. **When to use which store (memory entries)** — *take from A* (A:41–72), with two fixes. Replace `V-F21` with `V-F23` on the completeness row. Replace `s3-F4` with `M19, s3-F21` on the rationale row, or cite both files' disagreement and leave it to EJ — this is a documentation conflict in the source run, not something to silently pick.
4. **Costs, and where there are none** — *take from A* (A:74–83), with fixes. Attribute the "under 0.01 s / minimal tokens" `INDEX.md` scan to **opencode's reading of** `SOURCE_OF_TRUTH.md`, per DECISION-RULES.md:76 — A currently attributes it to the file. Cut "The last three are now measured on this repo's own code and docs" to "the graph-vs-grep head-to-head is; the vector-on-`entries/` gap and the memory corpus itself are not."
5. **Still unresolved (D1–D6)** — *take from A* (A:85–88). Unchanged in B; nothing to merge.
6. **Why no SQLite is visible in this repo** — *take from A* (A:90–99).
7. **Measured here: development and testing** — *take from B's placement* (immediately after the answer-first material, before the per-store sections, as both versions have it) and the shared text A:101–187 = B:28–114. Then apply four fixes to the shared text: mark the BM-4 graph cell `0.0 over 2 questions` instead of `n/a`; restate BM-8's "1 of 3" with its criterion or correct it to 2 of 3; disclose the 9 unfixed low audit findings that touch BM-9 (rg seconds ~16% high) and the vec row; and carry `state.md:48`'s unreclosed snapshot warning. *New text needed:* one sentence reconciling "Where is function or method X defined?" with DECISION-RULES.md:58, and one naming the third vision proposal (P3, empty answer ≠ absence) in the "left to EJ" list, which A:184–187 omits.
8. **Rules for all three caches** — *take from A* (A:189–205). Identical in both.
9. **SQLite full-text index / Vector index / Code graph** (five whys + 5W1H each) — *take from B's wording* for the three threshold phrases (B:189, B:202, B:228) and A's wording everywhere else. Identical in both otherwise.
10. **What this changes elsewhere (proposed, not done)** — *take from A* (A:316–320).
11. **Not known** — *take from A* (A:322–331). Add one line: the harness repair was not re-audited and nine low audit findings remain open.
12. **Core requirements R1–R8** — *take from A* (A:333–394). Non-negotiable; the vision points here.

### Not checked

- I did not open the three raw enhance-run node files (`code-graph.claude.stdout.md`, `vector.codex.stdout.md`, `sqlite.opencode.stdout.md`). I checked A's and B's summaries of them against DECISION-RULES.md, not the nodes themselves.
- I did not re-run the bench or reproduce the 180/180 determinism result.
- I did not open `cov/coverage-maps.json` or run `run-suite-and-coverage.sh`; the "529 tests, 31–33 s" figure rests on `state.md:51` alone.
- I confirmed that `V-F20`–`V-F24` exist and say what A claims; I did not verify `V-F3`, `V-F4`, `V-F1`, `V-F5`, `V-F6`, `V-F7`, `V-F10`, `V-F13`, `V-F23`'s underlying paper, nor `s3-F29`/`s3-F34`.
- I confirmed the existence and subject of `G-F5`, `F5c`, `F12`, `F21`; I did not verify `G-F7`/`G-F7a`, `G-F8`, `G-F9`, `G-F10`, `G-F14`, `G-F17`, `G-F18` at source.
- I did not audit whether the three "incomplete" gold answers (E01, E03, B02) were fixed in `queries.json` in a way that could bias a route in the routes' favour.
- I did not check the 12 non-planted findings from `runs/20261012-memory-caches/nodes/review.claude.md` line by line beyond spot checks.
- I did not check that the five non-planted findings from `nodes/review.codex.stdout.md` were all fixed — only the five listed at `state.md:70–75`.
- I did not check that `project-memory/` still does not exist, and I did not open `runs/20261012-caches-enhance/site/`.
- I did not compare either version against the live `docs/memory-system/CACHES.md` working-tree state, which both runs edited concurrently.

---

Two things worth flagging before you act on this. First, both versions carry the same three shared defects (the BM-8 "1 of 3", the unsourced 4.8 MB, the omitted `S-F4` baseline caveat), which means neither is a clean base for those lines — they need fixing wherever they land. Second, the most consequential finding is not in either version: `runs/20261012-caches-routing/state.md:48` says the numbers "must be re-run on a stable snapshot", node 3 is recorded as run once, and no re-run is recorded. That is a re-run to schedule, not a wording fix.


## r2 review by agy

### Where I agree with the others

- **Retain the memory-entry routing table from Version A (`version-A.md:41–73`).** All three reviewers agree this table is indispensable. Version B completely omits memory-entry routing and asserts at [`version-B.md:104–105`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L104-L105) that the per-store descriptions cover it, which is false: the per-store sections describe build triggers and architecture, not question routing. The memory routing table is grounded in [`DECISION-RULES.md:42–65`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L42-L65).
- **Retain Core Requirements R1–R8 from Version A (`version-A.md:335–395`).** All three reviewers agree Version B's omission of R1–R8 leaves a dangling cross-reference at [`version-B.md:109`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L109) and violates the vision contract ([`caches-memory-vision-statements.md:8`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md#L8)), which explicitly designates `CACHES.md` as the home of R1–R8.
- **Adopt Version B's trigger threshold wording ("EJ's number").** All three reviewers agree Version B is better supported at [`version-B.md:189`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L189), [`L202`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L202), and [`L228`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L228). Version A cites a phantom section `SOURCE_OF_TRUTH.md § How each threshold is found` that does not exist in the active document ([`SOURCE_OF_TRUTH.md:1–127`](file:///home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md#L1-L127)), existing only in a draft proposal file ([`runs/20261012-caches-enhance/SOURCE_OF_TRUTH.md:165`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/SOURCE_OF_TRUTH.md#L165)). The vision settles threshold authority: *"all three numbers are EJ's"* ([`caches-memory-vision-statements.md:33`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md#L33)).
- **Correct the rationale citation on row `A:66`.** All three reviewers agree that citing `s3-F4` (StateTape staleness diff off a code graph; [`code-graph.opencode.stdout.md:309`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/code-graph.opencode.stdout.md#L309)) for "Why did we choose this..." is a citation error. The correct rationale findings are `s3-F21` ([`INDEX.md:136`](file:///home/smoke01/dev/ancient-games/docs/research/20261011-agent-memory-graph-r2/INDEX.md#L136)) and `M19` / `SOURCE_OF_TRUTH` ([`DECISION-RULES.md:52`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L52)).
- **Qualify the 226K token cost figure (`version-A.md:76`, `version-B.md:140`).** All three reviewers agree this figure derives from `S-F4`'s 1,144-document enterprise RAG benchmark ([`sqlite-fts.claude.md:55–58`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/sqlite-fts.claude.md#L55-L58)) using a paths-only file-system agent, and was not measured on a memory corpus or code in this repository.
- **Clarify the BM-8 benchmark summary (`version-A.md:141`, `version-B.md:68`).** All three reviewers agree that saying "grep found 1 of 3" is inaccurate without qualification. Grep named a gold file on 2 of 3 questions (C06 and C07) and retrieved a complete gold set on 1 of 3 ([`results.md:200–214`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L200-L214)).
- **Preserve the cost ledger, GAPs, and multi-engine disagreements D1–D6.** All three reviewers agree that the unresolved disagreements D1–D6 ([`DECISION-RULES.md:134–165`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L134-L165)) and empirical GAPs must be preserved rather than averaged into a false consensus.

---

### Where I disagree

1. **SQLite visibility explanation on disk (`version-A.md:90–95`)**
   - *Other reviewer's position:* Codex showed that asserting "No `.db` is ever on disk" is factually false because three SQLite files exist on disk at `runs/20261012-caches-routing/bench/.cache/{fts,vec,graph}.sqlite` ([`bench/README.md:40`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/README.md#L40)). Opencode conceded this point in round 2.
   - *My position in round 1:* Listed A:90 as a strength of A that answers EJ's question by explaining that SQLite is not visible because `.db` files are gitignored and never committed.
   - *Verdict:* **Change.**
   - *Reason and source:* Codex is factually correct. [`version-A.md:90`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L90) explicitly states: *"No `.db` is ever on disk"*. That statement is contradicted by [`bench/README.md:40`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/README.md#L40), which documents persistent `.cache/*.sqlite` files created during the routing run. Gitignore explains why SQLite files are not committed to git, not why they cannot exist on disk. I change my position: the paragraph must be corrected to explain that SQLite files are gitignored and derived (and thus uncommitted), while preserving the valid architectural precedents from [`DECISION-RULES.md:171–182`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L171-L182) (`ancient_games/index.py` indexing the referee journal, `code_graph/code_graph.py` indexing code, and unbuilt `project-memory/`).

2. **"The answer first" opening scope (`version-A.md:29–39` / `version-B.md:16–26`)**
   - *Other reviewer's position:* Opencode maintained keeping A:29–39 verbatim. Codex held that "The answer first" requires an explicit scope restriction: "None of the three caches is needed today" must be scoped specifically to memory entries (`project-memory/`) so it does not contradict the empirical code/docs development benchmark that follows.
   - *My position in round 1:* Proposed taking A:29–39 verbatim, summarizing it as re-stating that no cache is needed today for memory entries.
   - *Verdict:* **Change** (to adopt Codex's explicit scope qualification).
   - *Reason and source:* While my round-1 summary interpolated "for memory entries", the actual text of [`version-A.md:31`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L31) states flatly: *"None of the three caches is needed today."* Without an explicit scope limiter, this flat claim contradicts the 40 benchmark results on code and docs ([`version-A.md:101–163`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L101-L163)) where caches outperform grep. Per [`caches-memory-vision-statements.md:15–17`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md#L15-L17), the settled vision applies to `project-memory/`. I change my position: the opening must explicitly state that no cache is needed today *for memory entries*, framing code and docs retrieval as a proposed expansion governed by [`vision-proposals.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/vision-proposals.md#L1-L6).

3. **Query routing prohibition on derived caches (`version-A.md:43`)**
   - *Other reviewer's position:* Codex identified that *"a cache is never the answer to a question the files answer"* would ban all derived caches, since derived caches inherently retrieve information from files. The vision requires files to remain authoritative and readable, not retrieval banned ([`caches-memory-vision-statements.md:25–29, 34`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md#L25-L29)). Opencode accepted this in round 2.
   - *My position in round 1:* Did not flag `A:43`; accepted the text introducing the memory table.
   - *Verdict:* **Change.**
   - *Reason and source:* Codex is correct. The vision states that markdown is always the source of truth and caches are optional and derived ([`caches-memory-vision-statements.md:29`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md#L29)), but their explicit purpose is to keep retrieval cheap when sequential reading of files becomes too expensive ([`caches-memory-vision-statements.md:25–26`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md#L25-L26)). Banning caches whenever files can answer the question makes derived caches impossible. I change my position: the rule must be reworded to state that markdown files remain the authoritative source of truth, while derived caches provide cheaper retrieval paths once triggered.

4. **Freshness check heuristic and deletion flaw (`version-A.md:197`, `version-B.md:124`, `version-A.md:356`)**
   - *Other reviewer's position:* Codex identified that comparing only the newest source mtime cannot guarantee "stale never answers": deleting an entry does not make surviving files newer, leaving deleted rows searchable indefinitely ([`sqlite-fts.claude.md:115–120`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/sqlite-fts.claude.md#L115-L120)). Opencode accepted this in round 2.
   - *My position in round 1:* Accepted the newest-mtime rule in section 7 and R3.1 without objection.
   - *Verdict:* **Change.**
   - *Reason and source:* Codex's deletion counterexample exposes an architectural flaw. Under [`version-A.md:197`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L197) and `A:356` (R3.1), the check compares `max(source mtime)` against cache mtime. When an entry is deleted, surviving mtimes are unchanged, no rebuild is triggered, and deleted entries remain searchable. Because memory entries live in git ([`caches-memory-vision-statements.md:22`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md#L22)), freshness must be bound to the git commit revision or content/manifest hash ([`sqlite-fts.claude.md:118`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/sqlite-fts.claude.md#L118), F11/F15; [`version-A.md:352–353`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L352-L353)). I change my position: R3.1 and the freshness rule must require commit or manifest hash verification to handle deletions.

5. **Memory drift baseline: Entry mtime vs Verified git revision (`version-A.md:67`, `version-B.md:216`)**
   - *Other reviewer's position:* Codex showed that comparing code changes against entry mtime (`git log --since=<entry-mtime>`) is invalid: editing an entry updates its mtime without re-verifying it against code, concealing intervening code changes. M15 binds staleness to the `verified_at` git revision ([`RECOMMENDATION.md:44, 194–198`](file:///home/smoke01/dev/ancient-games/runs/20261011-project-memory-engines/RECOMMENDATION.md#L44)). Opencode accepted this in round 2.
   - *My position in round 1:* Retained `A:67` as written in the memory decision table.
   - *Verdict:* **Change.**
   - *Reason and source:* Codex's analysis is directly grounded in the memory design specification. [`RECOMMENDATION.md:44`](file:///home/smoke01/dev/ancient-games/runs/20261011-project-memory-engines/RECOMMENDATION.md#L44) (M15) states: *"Staleness is bound to the revision an entry was verified against and to changes in the code, config or dependencies it covers, not to age."* Lines 194–198 describe diffing covered paths from `verified_at` to HEAD. Using entry file mtime masks code changes whenever an entry's markdown is touched for maintenance or metadata edits. I change my position: the drift check route must be bound to git diff from `verified_at` to HEAD.

6. **Definition lookup vs Exhaustive call-site routing (`version-A.md:168`, `A:170` vs `DECISION-RULES.md:58`)**
   - *Other reviewer's position:* Opencode in round 1 called `A:168` a flat contradiction of [`DECISION-RULES.md:58`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L58). Codex countered that `DECISION-RULES.md:58` combined two distinct contracts: definition lookup (where the code graph tied grep at 0.75 hit@5 with 3x smaller output; [`results.md:34–40`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L34-L40)) vs exhaustive call-site discovery (where 3,874 unresolved calls prevent proving completeness; [`code-graph.opencode.stdout.md:119`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/code-graph.opencode.stdout.md#L119)). Opencode accepted Codex's split in round 2.
   - *My position in round 1:* Adopted `A:168` and `A:170` in the development routing table without distinguishing definition candidates from exhaustive caller contracts.
   - *Verdict:* **Change.**
   - *Reason and source:* Codex is better supported by the benchmark and node evidence. For Python definitions, the code graph achieved 0.75 hit@5 with 43 chars vs grep's 129 chars ([`results.md:34–40`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L34-L40)). But for caller enumeration and dead code (`A:170`, [`DECISION-RULES.md:58, 60`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L58)), unresolved calls mean the graph's answer is a non-exhaustive lower bound. Furthermore, `A:175`'s fallback rule ("if the first-choice tool returns an empty answer, fall back to grep") fails on partial caller lists. I change my position: split definition lookup (code graph) from exhaustive callers / dead code (`none` + grep), state the graph's limits, and update the fallback rule to fire on empty *or* partial answers.

7. **Section ordering in the merged document**
   - *Other reviewer's position:* Opencode in round 1 placed the benchmark evidence at section 7 (after recon). Codex placed development/testing evidence *after* the store designs and triggers (section 6), establishing the memory system architecture before presenting code/docs empirical proposals. Opencode accepted Codex's order in round 2.
   - *My position in round 1:* Placed benchmark evidence immediately after the query routing table (section 4), mirroring Version A's flow.
   - *Verdict:* **Change.**
   - *Reason and source:* Codex and Opencode's round-2 consensus is structurally superior. Placing 60+ lines of benchmark results directly after the opening creates narrative dissonance: it forces the reader to jump from "None of the three caches is needed today" (for memory) straight into benchmarks where caches win on code, before the store designs or build triggers have even been defined. Presenting memory architecture first (scope, query routing, never-rules, triggers, store designs), followed by the repository's empirical development evidence, then acceptance criteria and provenance, provides a coherent logical structure. I change my position to adopt Codex's section ordering.

8. **Routing table presentation: Dual separate tables vs Single unified table**
   - *Other reviewer's position:* Codex and Opencode (round 2) propose unifying all routing into a single table with a `Corpus` column (`project-memory/` vs `code & docs`), prerequisites, route, fallback, and answer limitations.
   - *My position in round 1:* Proposed keeping two demarcated sub-sections (Part 1: Memory, Part 2: Code/docs) under section 3.
   - *Verdict:* **Change.**
   - *Reason and source:* In [`version-A.md:56–72`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L56-L72) and [`L166–175`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L166-L175), separating memory questions from development questions by 90 lines was confusing. Unifying them into a single table with an explicit `Corpus` column eliminates fragmentation, enables single-lookup routing for agents, and makes corpus boundaries unambiguous. I change my position to adopt the unified table format.

9. **Blind verifier claim in provenance header (`version-A.md:18–20`)**
   - *Other reviewer's position:* Codex and Opencode showed that A:18 overstates verification. The verifier checked `DECISION-RULES.md`, caught the plant on the planted copy (returning REPAIR), passed the clean copy, and diffed against the clean copy in the same directory ([`runs/20261012-caches-enhance/run-report.md:15–17, 30–39`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/run-report.md#L15-L17)). No verifier ever checked `version-A.md`.
   - *My position in round 1:* Listed A:18–20 as a strength of A ("Complete provenance and review metadata").
   - *Verdict:* **Change.**
   - *Reason and source:* The run report confirms that node 5 evaluated `DECISION-RULES.md`, and node 6 wrote `CACHES.md`. Version A was created after the verification pass. Claiming a blind verifier returned all four PASS "on this file's text" is inaccurate. I change my position: the provenance note must accurately record what was checked and what was not.

10. **BM-4 Graph cell: `n/a` vs `0.0 (over 2 questions)` (`version-A.md:131`, `version-B.md:58`)**
    - *Other reviewer's position:* Opencode showed that marking the BM-4 graph cell `n/a` converts a measured zero into an absence: [`results.md:76`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L76) recorded graph scoring `0.0 | 0.0 | -- (0) | 38.0 | 0.0005` over 2 applicable questions, as flagged in [`audit-0.json:79`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/nodes/audit-0.json#L79). Codex changed in round 2 to agree with Opencode.
    - *My position in round 1:* Did not flag this cell error.
    - *Verdict:* **Change.**
    - *Reason and source:* [`runs/20261012-caches-routing/bench/results.md:76`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L76) and [`audit-0.json:79`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/nodes/audit-0.json#L79) prove the graph was measured on category D and scored 0.0. I change my position: the cell must be reported as `0.0 (over 2 questions) / 38`.

11. **BM-7 Unit and aggregation (`version-A.md:138`, `version-B.md:65`)**
    - *Other reviewer's position:* Codex demonstrated that 0.78 is macro-average test-file recall over n=4 questions, not overall share of individual tests found ([`derive_maps.py:22–32`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/cov/derive_maps.py#L22-L32), [`runtime-recall.json:90–109`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/nodes/runtime-recall.json#L90-L109)). Opencode accepted this in round 2.
    - *My position in round 1:* Accepted the BM-7 text as written.
    - *Verdict:* **Change.**
    - *Reason and source:* [`runtime-recall.json:90–109`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/nodes/runtime-recall.json#L90-L109) confirms the scores for C01–C04 are 0.33, 0.8, 1.0, 1.0 (mean 0.7825). The unit is test-file recall, and C03/C04 have single-test gold sets. I change my position to label it macro-average test-file recall (n=4).

12. **Completeness and absence row citations (`version-A.md:63–64`)**
    - *Other reviewer's position:* Opencode showed that `A:63` cites `V-F21` ("Exact identifiers and rare terms"; [`vector.claude.md:240`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/vector.claude.md#L240)) instead of `V-F23` ("Top-k cannot enumerate or prove absence"; [`vector.claude.md:259`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/vector.claude.md#L259)), dropping the run record citations from [`DECISION-RULES.md:47, 49`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L47). Codex accepted this in round 2.
    - *My position in round 1:* Did not catch the citation substitutions on `A:63` and `A:64`.
    - *Verdict:* **Change.**
    - *Reason and source:* `V-F21` is exact identifiers; `V-F23` is the finding establishing that top-k cannot prove completeness or absence. I change my position to restore the full citation sets from [`DECISION-RULES.md:47, 49`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L47) (`V-F1, V-F23, S-F13, G-F14` for completeness; `V-F20, V-F23` for absence).

13. **Application of Core Requirements R1–R8 to code and docs (`version-A.md:177`, `version-B.md:109`)**
    - *Other reviewer's position:* Codex showed that asserting R1–R8 apply unchanged to code and docs fails because R5.1 (overflowing `INDEX.md`), R6 (active-entry filter / `covers`), and R7 (entry filename attribution) cannot apply literally to code AST nodes or markdown doc chunks. Opencode agreed in round 2.
    - *My position in round 1:* Treated R1–R8 as an undivided unit to take from A.
    - *Verdict:* **Change.**
    - *Reason and source:* Codex is correct. R1–R4 (disposable, full rebuild, freshness, fallback) are general cache invariants. R5.1, R6, and R7 are specific to `project-memory/`. Saying R1–R8 apply unchanged creates an uncheckable requirement for code/docs. I change my position: the requirements section must explicitly separate universal cache invariants from memory-specific criteria and proposed code/docs criteria.

14. **Character metric definition (`version-A.md:124`, `version-B.md:51`)**
    - *Other reviewer's position:* Codex showed that calling the metric "first right answer" exceeds what was measured: [`results.md:26–28`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L26-L28) defines `chars` as characters to the first line naming a gold *file*. Opencode agreed in round 2.
    - *My position in round 1:* Accepted the metric description as written.
    - *Verdict:* **Change.**
    - *Reason and source:* [`runs/20261012-caches-routing/bench/results.md:26–28`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L26-L28) explicitly defines the metric as characters to the first gold file. Claiming it measures answer completion or saved reading time exceeds the measurement. I change my position to use the exact source definition.

15. **Vector-only vs Hybrid evidence (`version-A.md:265`, `version-B.md:191`)**
    - *Other reviewer's position:* Codex showed that claiming positive results always combine vectors with keyword search overstates the source: [`vector.claude.md:60–68`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/vector.claude.md#L60-L68) (V-F3) reports programmatic vector retrieval beating grep in 5 of 10 harness-model pairs. Opencode agreed in round 2.
    - *My position in round 1:* Did not flag this overstatement.
    - *Verdict:* **Change.**
    - *Reason and source:* [`runs/20261012-memory-caches/nodes/vector.claude.md:65–66`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/vector.claude.md#L65-L66) explicitly states that with file-based delivery, vector retrieval exceeded grep on 5 of 10 pairs. Hybrid-only can remain a proposed policy, but the text must not claim empirical unanimity. I change my position to qualify the claim.

16. **Speed bound compliance vs Grep `git ls-files` overhead (`audit-0.json:93–94`)**
   - *Other reviewer's position (Opencode vs Codex):* Opencode argued in round 1 that finding 12 in `audit-0.json` (rg spawns `git ls-files` per query, adding ~1.2 ms / 16%) undercuts BM-9's 15 ms speed bound. Codex argued in round 2 that subtracting overhead reduces rg's time to ~6.2 ms, which does not undercut the 15 ms upper bound.
   - *My position in round 1:* Did not examine the audit findings in detail.
   - *Verdict:* **Hold Codex's position over Opencode's.**
   - *Reason and source:* Codex is better supported. Per [`audit-0.json:93–94`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/nodes/audit-0.json#L93-L94), rg's measured mean was ~7.4 ms with ~1.2 ms overhead. Removing overhead lowers grep's execution time to ~6.2 ms, comfortably beneath BM-9's 15 ms bound ([`results.md:15`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L15); maximum measured across all routes was 14.68 ms). Subtracting overhead strengthens compliance with the upper bound rather than undercutting it. The overhead must be disclosed to contextualize comparative timings between grep and FTS, but the 15 ms bound holds.

17. **Corpus snapshot stability during benchmark build (`state.md:48`)**
   - *Other reviewer's position (Opencode vs Codex):* Opencode noted in round 1 that `state.md:48` warned numbers must be rerun on a stable snapshot due to concurrent editing, and called for a rerun. Codex noted in round 2 that while a rerun on the repaired harness occurred (`state.md:59–64`), whether that rerun occurred on an isolated snapshot remains unconfirmed.
   - *My position in round 1:* Noted benchmark execution was not independently verified.
   - *Verdict:* **Hold Codex's position over Opencode's.**
   - *Reason and source:* Codex is better supported. [`runs/20261012-caches-routing/state.md:59–64`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/state.md#L59-L64) confirms node 3 was run on the repaired harness and determinism was established. However, the initial builder note ([`state.md:48`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/state.md#L48)) regarding concurrent editing during the build was not formally closed. This should be reported as an evidence caveat, not an assertion that no rerun ever occurred.

---

### Revised merged outline

The section order of the best version takes Codex's ordering (as adopted by Opencode in round 2), incorporating the factual corrections, unified routing table, and split acceptance criteria.

1. **Title, status, and provenance notes**
   - *Action:* **Combine both; new text needed.**
   - *Detail:* Take Version A's header pointers ([`version-A.md:16–27`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L16-L27)) to the enhance run, routing run, and vision statement. Replace the stale label block ("Two numbers come from checks the researchers wrote...").
   - *New text needed:* (a) Attribute the development/testing section to the main routing session ([`state.md:61`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/state.md#L61)); (b) record that Version B's "EJ's number" was adopted because `docs/memory-system/SOURCE_OF_TRUTH.md` contains no threshold section; (c) accurately report that the blind verifier evaluated `DECISION-RULES.md`, not `version-A.md` ([`run-report.md:15–17, 30–39`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/run-report.md#L15-L17)).

2. **The answer first: Status and scope**
   - *Action:* **Take from A; new text needed.**
   - *Detail:* Take [`version-A.md:29–39`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L29-L39) (caches optional, derived, rebuildable; unbuilt `project-memory/`; `G-F21` / `KNOWLEDGE_GRAPH_DESIGN.md`).
   - *New text needed:* Explicitly scope "None of the three caches is needed today" to **memory entries** (`project-memory/`). State up front that code and docs retrieval is a proposed expansion awaiting EJ's decision via [`vision-proposals.md`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/vision-proposals.md#L1-L6), and affirm that all three trigger numbers belong to EJ ([`caches-memory-vision-statements.md:33`](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md#L33)).

3. **When to use which store: Unified query routing table**
   - *Action:* **Combine both; new text needed.**
   - *Detail:* Unify memory routing rows ([`version-A.md:56–72`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L56-L72)) and development/testing rows ([`version-A.md:166–175`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L166-L175)) into a single table with an explicit `Corpus` column (`project-memory/` vs `code & docs`), listing prerequisite, route, fallback, and answer limitations for each row.
   - *New text needed:*
     - Replace A:43's prohibition with the principle that markdown files remain the authoritative source of truth, while derived caches provide cheaper retrieval once triggered.
     - Restore correct citations on completeness (`V-F1, V-F23, S-F13, G-F14`) and absence (`V-F20, V-F23`), replacing `V-F21` ([`DECISION-RULES.md:47, 49`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L47)).
     - Correct rationale row to cite `M19, s3-F21, SOURCE_OF_TRUTH` ([`DECISION-RULES.md:52`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md#L52)), replacing `s3-F4`.
     - Re-bind memory drift check to git diff from `verified_at` to HEAD ([`RECOMMENDATION.md:44, 194–198`](file:///home/smoke01/dev/ancient-games/runs/20261011-project-memory-engines/RECOMMENDATION.md#L44)), eliminating `entry-mtime`.
     - Add config/manifest lookup row routed directly to grep, noting `pyproject.toml` exclusion from AST corpus (E02).
     - Split definition lookup (code graph) from exhaustive caller enumeration and dead code (`none` + grep), citing Python-only coverage ([`code-graph.opencode.stdout.md:269–270`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/code-graph.opencode.stdout.md#L269-L270)) and 3,874 unresolved calls ([`code-graph.opencode.stdout.md:119`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/code-graph.opencode.stdout.md#L119)).
     - Update fallback rule to trigger on empty *or* partial graph answers.

4. **Shared never-rules for all caches**
   - *Action:* **Take from A; new text needed.**
   - *Detail:* Take [`version-A.md:189–205`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L189-L205) (never source of truth, full rebuild only, fall back when absent, read-only open).
   - *New text needed:* Replace newest-mtime freshness rule with git commit revision or content/manifest hash verification to detect deletions ([`sqlite-fts.claude.md:115–120`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/sqlite-fts.claude.md#L115-L120)); add checkable session-start read prohibition (`M18`); scope active-entry filtering to memory corpora.

5. **Build triggers**
   - *Action:* **Combine both; take trigger wording from B.**
   - *Detail:* Adopt Version B's explicit trigger phrasing ("**EJ's number**"; [`version-B.md:189, 202, 228`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L189)), deleting all citations to `SOURCE_OF_TRUTH.md § How each threshold is found`. Retain Version A's cost comparisons as proposals informing EJ's decisions. Retain the three `OPEN:` criteria ([`version-A.md:370–379`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L370-L379)).

6. **Three store designs (5 Whys and 5W1H)**
   - *Action:* **Combine both; take trigger wording from B, rest from A; new text needed.**
   - *Detail:* Take SQLite FTS5, Vector index, and Code graph sections. Use Version B's trigger wording.
   - *New text needed:* Reconcile "Today: no graph" ([`version-A.md:310`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L310)) by distinguishing the unbuilt memory drift graph from the benchmarked code graph (`code_graph/code_graph.py`); reconcile 0.94 s repo build (`G-F12`) with 0.892 s benchmark build ([`results.md:15`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L15)); specify the static `minishlab/potion-base-8M` embedding model; qualify V-F3 to note programmatic vector beat grep on 5 of 10 pairs ([`vector.claude.md:65–66`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/vector.claude.md#L65-L66)).

7. **Empirical evidence: Development and testing benchmarks**
   - *Action:* **Take from B's placement, shared text from A/B; new text needed.**
   - *Detail:* Place the benchmark section here (following store designs and triggers). Take shared text [`version-A.md:101–163`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L101-L163) / [`version-B.md:28–90`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-B.md#L28-L90).
   - *New text needed:*
     - BM-4: correct graph cell from `n/a` to `0.0 (over 2 questions) / 38` ([`results.md:76`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L76), [`audit-0.json:79`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/nodes/audit-0.json#L79)).
     - BM-7: label as macro-average test-file recall (n=4), noting C03/C04 single-test gold sets and the 10-function cap ([`runtime-recall.json:90–109`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/nodes/runtime-recall.json#L90-L109)).
     - BM-8: state full 3-part qualification (named gold file for 2 of 3; complete gold set for 1 of 3; 8.7K chars came from C05 miss; [`results.md:200–214`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L200-L214)).
     - BM-5: disclose E02 corpus exclusion (`pyproject.toml` outside `.py`/`.md` globs; [`queries.json:681`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/queries.json#L681), [`chunk.py:38`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/chunk.py#L38)).
     - Define `chars` metric as characters to the first line naming a gold *file* ([`results.md:26–28`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md#L26-L28)).
     - Disclose relevant audit qualifications (rg's ~16% `git ls-files` overhead, vector deduplication; [`audit-0.json:49–53, 91–109`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/nodes/audit-0.json#L49-L53)) and note the unverified snapshot warning ([`state.md:48`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/state.md#L48)).

8. **Costs, gaps, and architectural precedents**
   - *Action:* **Take from A; new text needed.**
   - *Detail:* Take [`version-A.md:74–89`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L74-L89) (cost ledger, GAPs, unresolved disagreements D1–D6) and [`L90–99`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L90-L99) (recon on repo precedents).
   - *New text needed:*
     - Qualify 226K tokens as EnterpriseRAG-Bench / S-F4 with a paths-only agent, not memory or repo code ([`sqlite-fts.claude.md:55–58`](file:///home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/sqlite-fts.claude.md#L55-L58)).
     - Correct `A:82` over-claim: benchmark closes code/docs graph-vs-grep, not the vector-on-`entries/` gap.
     - Correct `A:90`: state that `.cache/*.sqlite` files exist on disk ([`bench/README.md:40`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/README.md#L40)) and explain that SQLite files are gitignored and uncommitted, preserving the valid precedents of `ancient_games/index.py`, `code_graph/code_graph.py`, and unbuilt memory.

9. **Core requirements and acceptance criteria (R1–R8)**
   - *Action:* **Take from A; new text needed.**
   - *Detail:* Retain the R1–R8 framework from [`version-A.md:335–395`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L335-L395).
   - *New text needed:*
     - Replace phantom citations in R5.1, R5.2, R5.3, R8.2 with `OPEN: EJ's number`.
     - Update R2.2 and R3.1 to require git commit or content hash verification for freshness to handle deletions.
     - Split acceptance criteria into three clear categories: universal cache invariants (R1–R4), memory-specific criteria (R5.1, R6, R7), and proposed code/docs criteria.

10. **Proposed changes elsewhere, evidence limits, and open items**
    - *Action:* **Combine both; new text needed.**
    - *Detail:* Take [`version-A.md:316–321`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L316-L321) (proposed drift git diff, updated to `verified_at`) and [`L322–332`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md#L322-L332) ("Not known").
    - *New text needed:* Explicitly list the three proposals from [`vision-proposals.md:1–48`](file:///home/smoke01/dev/ancient-games/runs/20261012-caches-routing/vision-proposals.md#L1-L48) (P1 code/docs expansion, P2 cache types, P3 empty answer ≠ absence); preserve unreviewed status of harness repair and unmeasured end-to-end agent trial.


## r2 review by codex

### Where I agree with the others

The supplied agy review is empty, so it provides no position to compare. All comparisons below are with opencode. These are my readings of the reopened sources; I changed no files and reran no benchmarks.

- **Keep A’s memory-entry routing and R1–R8; use B’s threshold wording. Hold.** B’s per-store descriptions do not replace question routing, and its requirements reference is dangling. The settled vision explicitly names this document as the home of R1–R8 and reserves all three trigger numbers for EJ. [Vision:8, 33](/home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md:8)

- **Correct the verifier account. Hold.** We agree that A overstates verification. The deepseek verifier checked `DECISION-RULES.md`: the planted copy received REPAIR, the clean copy passed, and comparison with the clean copy partly exposed the plant. This does not validate final A. [Enhance run report:15–17, 30–39](/home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/run-report.md:30)

- **Clarify BM-8. Hold.** Both grep and FTS found a relevant gold file for two of three subprocess questions. FTS retrieved the complete gold set for two; grep did so for one. The original sentence mixes these criteria. [Results:200–214](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md:200)

- **Accept opencode’s additional citation and scope corrections. Change my assessment to include them.** Completeness needs `V-F23`, not `V-F21`. A:82 cannot close the vector-on-memory-entries gap using a code/docs benchmark. [Vector findings:240–260](/home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/vector.claude.md:240), [A:79–83, 122](/home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md:79)

- **Accept the additional provenance and measurement qualifications. Change my assessment to include them.** Remove the unsupported “4.8 MB” unless a snapshot-specific measurement is supplied; identify the main session as the routing-section author; distinguish the earlier 0.94 s graph measurement from the benchmark’s 0.892 s build. The saved corpus summary gives file and chunk counts, while the state identifies the section’s author. [Results:4, 13–15](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md:4), [Routing state:61–64](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/state.md:61), [G-F12:117](/home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/code-graph.opencode.stdout.md:117)

### Where I disagree

1. **Keeping “The answer first” verbatim.**  
   **Opencode:** retain A:29–39 unchanged. **My position: hold** that the opening needs explicit scope. The settled vision concerns memory entries; the proposed expansion concerns code/docs. “None … needed today” should retain its memory meaning without making an unqualified claim about both corpora. Smaller benchmark output also does not establish development time or agent-token savings. [Vision:15–20](/home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md:15), [Results:28](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md:28)

2. **Preserving the memory “none” rules with only citation fixes.**  
   **Opencode:** the “none” rows are A’s useful core; retain the surrounding rule. **My position: hold** that their question contracts need correction too. A:43–44 prohibits a cache from answering any question files answer, although the vision expressly permits derived caches holding information from those files. Exhaustive enumeration and absence need exhaustive routes; discovery may use a cache. [A:43–54](/home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md:43), [Vision:25–29](/home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/caches-memory-vision-statements.md:25)

3. **Treating rationale citation repair as an EJ decision.**  
   **Opencode:** replace `s3-F4`, or preserve the documentation disagreement for EJ. **My position: hold** that this citation error can be resolved from evidence. `s3-F4` concerns staleness; `s3-F21` concerns rationale retrieval. No policy choice is required to correct the reference. Separately, FTS can locate documentation, while the agent must read the decision to answer “why.” [Research index:119, 136](/home/smoke01/dev/ancient-games/docs/research/20261011-agent-memory-graph-r2/INDEX.md:119), [Memory design:114–117](/home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md:114)

4. **Retaining the cost paragraph through attribution.**  
   **Opencode:** preserve the paragraph with the proposed attribution and gap corrections. **My position: hold** that attribution alone cannot make its costs valid measurements. The 226K figure belongs to an enterprise-document agent benchmark with bounded path-search/read tools, not the synthetic 10,000-entry test or an established “open every hit” mechanism. The synthetic test explicitly measures no agent token cost. The `INDEX.md` scan cost remains unmeasured. [S-F4:55–58](/home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/sqlite-fts.claude.md:55), [S-F13:98–107](/home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/sqlite-fts.claude.md:98), [Decision record:191–193](/home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md:191)  
   I **change** my assessment to include opencode’s additional paths-only-baseline caveat from S-F4.

5. **Keeping “Why no SQLite is visible” unchanged.**  
   **Opencode:** calls it a traceable answer and retains it. **My position: hold** that its disk-absence claim is false. Gitignore explains why files are uncommitted; it does not prevent their existence. I confirmed `fts.sqlite`, `vec.sqlite` and `graph.sqlite` under the benchmark cache directory, exactly as its README records. Preserve the journal-versus-memory distinction, but rewrite the visibility explanation. [Benchmark README:40](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/README.md:40)

6. **Keeping the shared cache rules and R1–R8 unchanged apart from thresholds.**  
   **Opencode:** retains those sections. **My position: hold** that freshness and corpus scope require substantive repair. The newest-mtime rule misses a deletion that leaves no newer surviving file; it therefore cannot support “stale never answers.” Also, memory-specific `INDEX.md`, active-status, `covers` and entry-filename requirements cannot apply literally to arbitrary code/docs results. [A:352–357, 370–387](/home/smoke01/dev/ancient-games/runs/20261012-caches-merge/inputs/version-A.md:352), [S-F15:115–120](/home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/sqlite-fts.claude.md:115)

7. **Keeping the entry-versus-code timestamp comparison.**  
   **Opencode:** preserves the drift row and graph design except for threshold wording. **My position: hold** that last entry modification is the wrong baseline for “changed since verification.” An unrelated entry edit can conceal intervening code changes. M15 binds staleness to the verified revision, and the recommendation describes diffing covered paths from that baseline. [Recommendation:44, 194–198](/home/smoke01/dev/ancient-games/runs/20261011-project-memory-engines/RECOMMENDATION.md:194)

8. **Calling the definition-lookup conflict the same question.**  
   **Opencode:** says the routing tables give conflicting routes for the same definition question. **My position: hold** that the source combines two contracts: “Where is X defined, **and exactly where is it called?**” Graph lookup is supported for finding Python definition candidates here; exhaustive call-site discovery requires stronger checks. The graph and grep tie at 0.75 for exact identifiers, while unresolved calls prevent completeness claims. Split these rows and state graph limits beside them. [Decision record:58](/home/smoke01/dev/ancient-games/runs/20261012-caches-enhance/DECISION-RULES.md:58), [Results:34–40](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md:34), [G-F12:119–120](/home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/code-graph.opencode.stdout.md:119)

9. **“All shared figures trace exactly.”**  
   **Opencode:** broadly certifies the figures, while later identifying exceptions. **My position: change** my similarly broad statement that category scores match: BM-4’s graph cell is wrongly `n/a`; the saved result is zero over two applicable questions. [Results:76](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/results.md:76), [Claude audit:79](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/nodes/audit-0.json:79)  
   I **hold** my BM-7 correction: 0.78 is the macro-average **test-file recall** over four questions, not the fraction of individual tests found. Numerical agreement does not validate the unit or aggregation wording. [Coverage reducer:1–3, 22–32](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/cov/derive_maps.py:1), [Runtime recall:90–109](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/nodes/runtime-recall.json:90)

10. **Leaving the store-design conclusions unchanged.**  
    **Opencode:** adopts B’s threshold phrases and retains the other store text. **My position: hold** that vector conclusions also need qualification. The experiment used static `minishlab/potion-base-8M`; it cannot establish performance for the alternative embeddings. Hybrid-only may remain a proposed policy, but the claim that positive memory results always combine vectors and keywords conflicts with V-F3’s five vector-only wins among ten file-delivery pairs. [Build:51](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/build.py:51), [V-F3:60–68](/home/smoke01/dev/ancient-games/runs/20261012-memory-caches/nodes/vector.claude.md:60)

11. **Nine low findings remaining open and undermining the speed bound.**  
    **Opencode:** describes nine unfixed low findings and says grep overhead undercuts BM-9’s bound. **My position: change** my assessment to disclose the omitted audit qualifications, but reject that count as nine defects: one low entry explicitly says “No problem found.” The measured grep overhead biases comparative timing; removing overhead would not invalidate the reported 15 ms upper bound. The vector deduplication finding explicitly says hit@5 does not change. [Claude audit:49–53, 91–109](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/nodes/audit-0.json:49)

12. **The snapshot warning and absence of a rerun.**  
    **Opencode:** finds no confirmation of a stable-snapshot rerun and calls for one. **My position: change** my evidence assessment to carry the unresolved warning. However, a later run on the repaired harness is recorded; “no rerun” would be too strong. What remains unconfirmed is whether that later run used a stable corpus. Deterministic returned paths do not establish snapshot stability. [Routing state:43–48, 59–64](/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/state.md:43)

### Revised merged outline

1. **Status, provenance, scope and pending EJ decisions — combine both; new text needed.** Use A’s run attribution, correct verification claims, distinguish settled memory scope from proposed code/docs scope, and name all three vision proposals.

2. **The answer first — take from A; new text needed.** Scope “none needed today” to memory. Describe code/docs results as retrieval-output evidence with unmeasured agent outcomes.

3. **Question-to-route table — combine both; new text needed.** Group memory and development rows within one section. Separate discovery, explanation, exhaustive callers and absence. Include Python scope, incomplete nonempty graph results, verified-revision drift checks and direct configuration-file lookup.

4. **Shared cache rules — take from A; new text needed.** Preserve authoritative files, disposal, full rebuild, on-demand reads and fallback. Replace the insufficient freshness heuristic; scope active-entry filtering to memory.

5. **Build triggers — combine both.** Use B’s EJ-owned numbers. Keep A’s cost comparisons as proposals informing EJ’s decision.

6. **Three store designs — combine both; new text needed.** Correct drift baselines, qualify hybrid policy, and distinguish a memory drift-check graph from the graph already benchmarked for code.

7. **Development/testing evidence and costs — combine both; new text needed.** Correct BM-4, BM-7 and BM-8; name the embedding model; disclose corpus exclusions, audit qualifications and snapshot uncertainty. Separate enterprise, synthetic and repository measurements. Retain the full-suite safeguard.

8. **Core requirements R1–R8 and acceptance criteria — take from A; new text needed.** Retain their home in this document, repair freshness criteria and thresholds, and distinguish common, memory-specific and proposed code/docs requirements.

9. **Repository precedents and proposed changes elsewhere — take from A; new text needed.** Preserve the journal/code/memory distinctions; correct SQLite visibility and the proposed verification baseline.

10. **Unresolved disagreements and evidence limits — combine both.** Preserve D1–D6 as attributed positions, correct unsupported cost transfers, and retain pending EJ decisions, unreviewed repairs and unmeasured end-to-end benefits.


## r2 review by opencode

Read agy's review: it is empty — no text was returned for round 1. This round is therefore a two-reviewer exchange, and I treat codex as the only other review.

---

### Where I agree with the others

**On the thresholds (codex: A:262 high, "who decides thresholds").** We reach the same verdict — B — from different premises. My round-1 ground was that `SOURCE_OF_TRUTH.md § How each threshold is found` is unresolvable: the live file is 126 lines and contains no occurrence of the string "threshold"; the section exists only at `runs/20261012-caches-enhance/SOURCE_OF_TRUTH.md:165`. Codex's ground is stronger and I adopt it (see disagreement 2).

**On BM-8 (codex: "needs a completeness qualifier").** Codex and I independently reached the same two numbers. `results.md:206` gives rg on C06 `1.0`; `results.md:207` gives rg on C07 **`0.5`**; `results.md:201` gives rg on C05 `0`. So rg named a gold file on 2 of 3 and retrieved a complete gold set on 1 of 3, and A:141-142 states only the second. Codex's C07 line is the better source than mine.

**On the s3-F4 / s3-F21 id on the rationale row.** Agreed. `docs/research/20261011-agent-memory-graph-r2/INDEX.md:119` (s3-F4) is StateTape reading staleness off a graph diff; `INDEX.md:136` (s3-F21) is the "why"-question finding. A:66 cites the wrong one. See disagreement 7 for severity.

**On the verifier claim (codex: A:18).** Agreed, and codex's scope point is sharper than mine, so I adopt it. `runs/20261012-caches-enhance/run-report.md:12-19` orders the nodes: node 5 was the blind verify, whose row reads "all 4 PASS **on the clean file**; plant found", and node 6 is "write the enhancement into the doc". No check ever read the text of A.

**On A:75 (codex: mixed costs).** Agreed. `DECISION-RULES.md:75` is the row A:76 copies verbatim, and it pairs "~226K per question" with the citation "`S-F4, S-F13`" — but `sqlite-fts.claude.md:107` says of S-F13: "Token cost to the agent is the real axis and this test does not measure it: it does not run an agent." One correction to codex's wording: S-F4 calls it "a general RAG corpus, not code or memory entries" (`sqlite-fts.claude.md:55`); "EnterpriseRAG-Bench" is the same paper seen from the vector node (`vector.claude.md:242`). The load-bearing half of codex's point — that 226K is the 1,144-document study, not the 10,000-entry synthetic test — stands either way. My separate limit still applies: that agent's grep "returns paths only, not lines" (`sqlite-fts.claude.md:58`), and the figure appears in both versions without it.

**On A:90's first reason (codex: gitignored ≠ absent).** Codex is right on the fact. Three SQLite files exist: `runs/20261012-caches-routing/bench/.cache/{fts,vec,graph}.sqlite`, named as expected artefacts in `bench/README.md:40` ("Delete it whenever; nothing is lost"). The inherited text says the opposite — `DECISION-RULES.md:180-181`: "a `find` for those extensions returns nothing". See disagreement 1 for how far I move.

**On the points only codex raised, all of which I now accept as stated:** A:43 ("a cache is never the answer to a question the files answer" — vision:25-29 requires files authoritative, not retrieval banned); A:197/B:124 (mtime cannot guarantee stale never answers — delete an entry, nothing surviving is newer, the row stays searchable); A:67/B:216 (entry mtime is not the verified revision — `RECOMMENDATION.md:44`, M15, MAJORITY, "not to age"; `:194-198` diffs `covers` from `verified_at` to HEAD); A:124/B:51 (`results.md:26-28` defines `chars` as characters to the first line naming a gold **file**); A:138/B:65 (macro-average, n=4 — I confirm directly: `nodes/runtime-recall.json:90-109` gives C01 0.33, C02 0.8, C03 1.0, C04 1.0, mean 0.783); A:141/B:68 and A:173/B:100 (E02's gold is `pyproject.toml`, `queries.json`, while `bench/chunk.py:38` sets `CORPUS_GLOBS = ("*.py", "*.md")`); A:153/B:80 (`bench/build.py:50-51`: `EMBED_MODEL = "minishlab/potion-base-8M"`, `EMBED_DIMS = 256`); A:168/B:95; A:177/B:109; A:265/B:191 (`vector.claude.md:60-68`).

Two of these I can strengthen with sources neither review used. **A:138**: two of the four BM-7 questions have a one-test gold (C03, C04, both1 test — `runtime-recall.json:104-109`), so 0.78 leans on two trivial cases, and `nodes/audit-0.json` finding 9 records that the graph's answer is ten test *functions*, so one file's 46 tests can spend the cap and depress file-level recall. **A:173/B:100**: on category E, rg scores 0.5 `file hit@5` (`results.md:86`) while fts scores 0.3333 — grep is the only route that *could* have answered E02, and it is the row that makes full-text look worst.

**On evidence strength.** Agreed with codex's tempering of mine. I verified the 40 figures trace; codex's point is that tracing is not replication: one repo, one question set, n=6–10 per category, `state.md:59` "the repair is not re-audited", `state.md:74` "Not re-reviewed".

### Where I disagree

**1. A:90 "Why no SQLite is visible in this repo" — codex says the inherited explanation is wrong; I called it a genuine answer to EJ's question. CHANGE, partly.**

Codex is right that the first reason is false. But the reason is not that recon was wrong — it is that the routing run, later the same day, built the three caches. `DECISION-RULES.md:180-181` was true when written; `bench/.cache/*.sqlite` (14:16) makes it false now. My "traceable to recon.md" claim was about provenance, not truth, and I let it stand as a strength.

What survives: reasons 2–4 (`ancient_games/index.py` as the working precedent, `code_graph/code_graph.py` as the second, and `project-memory/` not existing) are unaffected, and the three on-disk files are now the strongest available evidence that the derived-cache pattern works here — A:93-94 calls the trigger unfired and never mentions that the mechanism was exercised today.

**2. A:262 threshold ownership — codex: a high-severity ownership substitution; me: a broken cross-reference. CHANGE.**

Codex's framing is right, and it is not only about the dead pointer. `enhance/SOURCE_OF_TRUTH.md:165-169` is not a neutral method note: "The design asks EJ to set numbers … Each is a *comparison* … so the design states the comparison and the measurement decides the value", and that file is "Status: draft, not yet accepted by EJ" (`:2`). A:262 makes a draft proposal operative and contradicts `vision-statements/caches-memory-vision-statements.md:33` ("all three numbers are EJ's") — while A:324, in the same file, still says "Every trigger number is EJ's". My round-1 "wording fix" understated it; the outcome is unchanged (B's wording), the severity is codex's.

**3. A:168 vs `DECISION-RULES.md:58` — codex: two question contracts needing separate rows; me: a flat contradiction. CHANGE.**

Codex is better supported and I was wrong about the object. `DECISION-RULES.md:58` is "Where is X defined, **and exactly where is it called?**" — one compound, exhaustive-contract question, routed to `none` because "3,874 unresolved calls against 2,000 call edges means 'no callers' would be a silent partial answer". A:168 asks only for the definition, which is a contract the graph satisfies. The real conflict is at A:170 ("What calls X? → code graph"), which takes the half the run record reserved for grep, and at A:175, whose fallback fires only on an empty answer. That is codex's "different contracts need separate rows", and it is also what `DECISION-RULES.md:60` says for dead code ("a missing edge does not mean no caller"). My round-1 prescription — a one-sentence reconciliation — is replaced by two rows plus the fallback fix.

**4. Section order — codex moves the evidence after the store designs; I said A's order wins on vision fit. CHANGE, and my reason was defective.**

I compared two documents that place the measurement identically: A:101 and B:28, both immediately after the answer-first material. A's only order difference from B is the inserted memory-routing section at A:41-72. So "A's order keeps the design's subject first" was not evidence about placement; it was an artefact of the section I was advocating. Codex's reorder is the real proposal, and I accept it on the reason I originally gave: in both versions "None of the three caches is needed today" (A:31 / B:18) sits ~70 lines above the measurement that contradicts it for code and docs, with the reconciliation deferred to A:184-187 / B:111-113. Moving the evidence after the design closes that window.

One condition: codex's order is only safe because disagreement 2 is resolved. If A's "the measurement decides the value" wording survives into the triggers section (codex item 4), the same contradiction reappears two sections earlier instead of later.

**5. Provenance placement — codex: a closing section; me: the header. CHANGE on the detail, HOLD on the pointer.**

I hold that a corrected Labels block and a "which run wrote this" line stay at the top. A:9-10 and B:9-10 both say "Two numbers come from checks the researchers wrote and ran themselves (`S-F13`, `G-F12`)" directly above a section containing ~30 first-party numbers from a different run; B:3-4 attributes the whole file to `claude-opus-5-5` although `state.md:61` records the routing section as the main session's work. A reader needs both corrections before "The answer first". I change on the detail: the expanded per-check provenance table goes last, per codex's item 8.

**6. BM-8's fix — codex: add a completeness qualifier; me: correct it to 2 of 3. CHANGE, and neither of us fixed the whole sentence.**

Codex's qualifier is better than my correction because the sentence has a third clause neither of us addressed: "printed up to 8.7K characters" is C05's `mean output` of 8,744 (`results.md:201`) — the one question grep found nothing in. So the sentence pairs a complete-set count with a character figure from a different question. The fix needs all three facts: named a gold file on 2 of 3; complete gold set on 1 of 3 (C07, 0.5);8.7K is C05, a miss.

**7. s3-F4 severity — codex: low; me: medium. CHANGE on the id, HOLD on the pattern, and the pattern is now three rows.**

Codex is right that a wrong id in a table cell is low. But A:66 did not mistype: it *replaced* the run record's three correct ids at `DECISION-RULES.md:52` (`M19, s3-F21, SOURCE_OF_TRUTH`) with one wrong one. The same substitution happened twice more, on the same table, on the two other rows that carry never-rules:

| row | run record | A |
|---|---|---|
| completeness | `V-F1, V-F23, S-F13, G-F14` (`DECISION-RULES.md:47`) | `V-F21` (A:63) |
| absence | `V-F20, V-F23` (`DECISION-RULES.md:49`) | `V-F20` (A:64) |
| rationale | `M19, s3-F21, SOURCE_OF_TRUTH` (`DECISION-RULES.md:52`) | `s3-F4` (A:66) |

`vector.claude.md:259` is "Top-k cannot enumerate or prove absence" (V-F23); `:240` is "Exact identifiers and rare terms" (V-F21); `:233` is negation (V-F20). So A:63's "a ranked top-k cannot prove completeness" and A:64's "no hit is not proof" are each carried by an id the run record had and A dropped. One typo is low; three substitutions on the three never-rule rows, all traceable to `runs/20261012-caches-enhance/CACHES.md:63-66`, is a pattern I keep at medium.

**8. The source for the graph's Python-only limit — codex cites `G-F12:119–120`; I hold the substance and correct the line.**

`code-graph.opencode.stdout.md:119` is "Unresolved calls | attribute 2863, dynamic 927, name 84" — that supports codex's *caller* incompleteness point, not language coverage. `:120` is the graph's byte size. The Python-only limit is at `:269-270` (§5 option B: "Does not answer: … nothing about non-Python paths in `covers:`" and "partial language coverage is a **silent partial answer**") and `:361`. Same defect class codex charged against A — a wrong evidence id — so it is worth correcting in the merged citation.

### Revised merged outline

Codex's order, with my four additions (contest-limit row, freshness contract, audit disclosure, provenance detail at the end).

1. **Header, labels, provenance pointer — combine both, plus new text.** A:16-27 (both run pointers, the claude-independence caveat, the vision path). Replace the "Two numbers come from checks the researchers wrote and ran themselves" block (A:9-10 / B:9-10). **New text needed:** one line naming `state.md:61` as the author of the development/testing section, and one recording that B's "EJ's number" wording was adopted and why — `docs/memory-system/SOURCE_OF_TRUTH.md` has no such section — or a future editor restores A's.
2. **Status, scope, and EJ's pending decisions — take from A** (A:29-39 = B:16-26, A:181-187 = B:108-114, A:316-320). **New text needed:** current memory scope vs the proposed code/docs expansion, with `runs/20261012-caches-routing/vision-proposals.md:3-6` named as for acceptance, amendment or rejection; and all three trigger numbers stated as EJ's up front (`vision:33`), so the triggers section cannot re-open them.
3. **One question-to-route table — combine both, with new text.** A's memory rows (A:56-72) and A/B's development rows (A:166-175) in one table with a corpus column; each row carries corpus, prerequisite, route, fallback, answer limitation. **New text needed:** (a) restore the three lost evidence ids (disagreement 7); (b) a config/manifest row routed to grep, because `pyproject.toml` is outside `CORPUS_GLOBS`; (c) the graph rows' limits — Python-only (`code-graph.opencode.stdout.md:269-270`, `:361`) and unresolved calls (`:119`); (d) exhaustive callers and dead code to `none` + grep per `DECISION-RULES.md:58,60`, replacing A:170/A:175, and the fallback becomes "graph answer empty **or** partial", not "empty"; (e) the drift row bound to `verified_at` against HEAD (`RECOMMENDATION.md:44`, `:194-198`), not to entry mtime.
4. **Shared never-rules — take from A** (A:189-205 = B:116-132), corrected. Rebuild-whole, fall back when absent, filter to active entries. **Change:** freshness is commit or content hash, not newest mtime — A:352-353 already offers "mtime **or the commit**", and `S-F15` lists SHA-256 per chunk (F11) and full delete-and-reinsert (F10) as the same node's alternatives. **New text needed:** the session-start prohibition as a checkable criterion, and the deletion case that mtime cannot see.
5. **Build triggers — take from B's wording** (B:189, 202, 228) with A's three `OPEN:` criteria (A:370-379). A's comparison method survives as a **proposal addressed to EJ**, quoted from `runs/20261012-caches-enhance/SOURCE_OF_TRUTH.md:165-180` and labelled draft (`:2`). Code and docs triggers only through an explicit vision proposal.
6. **Three store designs — combine both.** B's threshold phrases, A's wording elsewhere. Fix "Today: no graph" (A:310) to draw the distinction (no graph for the memory drift check; `code_graph/code_graph.py` exists and was measured at 0.892 s, `results.md:15`), reconcile 0.94 s with 0.89 s, scope the active-entry and source-attribution filters to memory (R5.1/R6/R7 cannot apply to a code chunk — A:177's "R1–R8 apply unchanged" is false for exactly the three checkable ones), and note that A:265's hybrid-only rule is stated on V-F3's inline half while `:60-68` reports vectors ahead on five of ten file-based pairs — the mode the bench itself delivers.
7. **Development and testing evidence — take from B's text, corrected, placed per codex.** BM-4 graph cell `0.0 over 2 questions` (`results.md:76`, `:251`; `audit-0.json` finding 10), not `n/a`; BM-7 as macro-average test-file recall n=4 with the one-test-gold caveat and the ten-function cap (findings 9); BM-8 with all three facts (disagreement 6); BM-5 disclosing E02's exclusion; the embedding model named; `chars` labelled as characters to the first gold **file**; **new text:** disclose all 14 audit findings, of which five bear on the text — rg's `git ls-files` overhead inflating the speed bound (finding 12), vec's 10-chunks-then-dedup (6), hybrid always printing vec's block (13), the graph's 3 untracked files (7), the ten-function cap (9) — and carry `state.md:48`'s unclosed stable-snapshot warning, naming who wrote the tables (`state.md:61`).
8. **Acceptance criteria — take from A** (A:335-394), corrected. R2.2 and R3.1 re-based on commit-or-hash; R5 `OPEN:`s name EJ's number; split into common, memory-specific, and proposed code/docs.
9. **Evidence provenance and unresolved questions — combine both.** `run-report.md:12-19` (node 5 verified the record, node 6 wrote the doc, so no check read the merged text), the 5 high and 9 low audit findings with their fixes, `state.md:37-60` and `:67-76`, one repo and one question set with no replication, plus A:322-331 "Not known", plus the 4.8 MB corpus figure replaced by the byte count (`results.json` gives `{files: 490, files_py: 123, files_md: 367, chunks: 4021}`; `chunk.py`'s own selection recomputes to 4,703,239 bytes).
