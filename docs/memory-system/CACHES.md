> Status: draft, not accepted by EJ. Merged 2026-10-12 by dsh (`deepseek-flash`) from Version A
> (`runs/20261012-caches-enhance/CACHES.md`) and Version B (`runs/20261012-caches-routing/CACHES.enhanced.md`), after
> reviews by agy, codex and opencode (`runs/20261012-caches-merge/reviews/`).
> Then corrected by the COO (Claude `claude-opus-5-5`) for two leftovers and seven review findings
> (`runs/20261012-caches-merge/verify/review-coo.md`); dsh's original is `merge/CACHES.merged.dsh-original.md`.

# Memory Caches: SQLite Full-Text, Vector, Code Graph

> **Provenance.** Written 2026-10-12 by Claude (`claude-opus-5-5`) from three research
> nodes in `runs/20261012-memory-caches/nodes/`: SQLite full-text (`sqlite-fts.claude.md`, ids `S-F*`), vector
> (`vector.claude.md`, `V-F*`) and code graph (`code-graph.opencode.stdout.md`, `G-F*`). The code-graph node uses `F5`
> twice; `G-F5 drift` means the drift study and `G-F5 Serena` means Serena.

> **Labels.** *Quoted* means the line rests on a finding id; *my reading* means it is my inference; *not measured*
> means nobody has measured it.

> **Review.** A blind review (`claude-sonnet-5-5`, `runs/20261012-memory-caches/nodes/review.claude.md`) returned
> REPAIR with 13 findings. It caught the planted defect (F-1), and the other 12 are fixed here. The fixes have not
> been re-reviewed.

> **When-to-use enhancement, 2026-10-12** (`runs/20261012-caches-enhance/`): three engines, rotated so each store
> got fresh eyes, answered *when to use this store at query time and what it costs*; the merge is the section
> **When to use which store** below. Caveats carried: one engine (claude) disclosed coordinating with another agent on
> the same question, so its answer is not independent; and every cost for a real `project-memory/` is `GAP`. What the
> verifier checked, and what it returned, is in the run record.

> **Measured enhancement, 2026-10-12** (`runs/20261012-caches-routing/`): the section **Measured here: development and
> testing** adds measurements on this repo and a routing rule for code and docs. In this merged version, review
> corrections also touch other sections (see `runs/20261012-caches-merge/merge/merge-notes.md`). Its conflict with
> the vision for code and docs is left to EJ.

> **Vision:** `vision-statements/caches-memory-vision-statements.md` — moved out 2026-10-12 so the vision
> and the requirements each have one copy.

## The answer first

None of the three caches is needed today **for memory entries**. `project-memory/` does not exist yet, so nothing has
been measured on it. My reading of the research is that at the sizes measured elsewhere, `INDEX.md`, grep and git
answer the questions each cache would answer. Each cache below has a
**trigger**: a condition that can be observed and that makes it worth building. None of them is built before its
trigger fires.

The caches are for **memory entries** only: that is the vision EJ confirmed on 2026-10-12. The measured section below
on code and docs is kept as evidence; it is outside the vision, and its proposals to widen the vision were not adopted.

This follows the design's own rule: `.cache/` is optional, gitignored and rebuilt from the files, and its absence
must not stop anyone reading memory (`SOURCE_OF_TRUTH.md`; recommendation M4, M6). It also follows the repo's own
history of building graphs nobody queried (`docs/KNOWLEDGE_GRAPH_DESIGN.md` §1, quoted in `G-F21`).

## When to use which store

The two tables below cover two different corpora and are kept apart. **Part 1 is for memory entries**
(`project-memory/`), reasoned from the research and the run record. **Part 2 is for code and docs**, measured on this
repo. In both parts a cache is derived and optional and is never the source of truth; once its trigger fires it is a
cheaper way to reach the same entry.

### Part 1 — memory entries (corpus: `project-memory/`)

At query time the memory is answered by the files — `INDEX.md`, grep, git, or reading the entry — and the files are
the source of truth, not the cache. The table below merges three engines asked independently, one store
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
| A question about the code itself: what changing F reaches, which tests reach F | see **Part 2** (code and docs) | — | Part 2 |
| An exact identifier, an error string, a known `file:line` | none | literal grep or filename lookup, then read | V-F7, V-F21, s3-F29 |
| Every active entry covering path X — completeness | none — a ranked top-k cannot prove completeness | exhaustive scan of `INDEX.md` and entry headers | V-F1, S-F13, G-F14 |
| Proving absence ("have we never recorded…") | none — no hit is not proof | exhaustive search, then read | V-F20 |
| A structured header question (status, `supersedes`, `depends_on`) | none | `INDEX.md` scan or a script over frontmatter; follow links by grep | V-F22, M13 |
| Why did we choose this, or why is this line like this? | none | the entry's **Why:** and its evidence; `git blame`, `git log -S` | M19, SOURCE_OF_TRUTH |
| Did the covered code change after the entry was verified? | none | `git log <verified-rev>..HEAD -- <each covers: path>`; any commit listed means yes. `<verified-rev>` is the git revision the entry header records it was last verified against (`SOURCE_OF_TRUTH.md` l.50); the command is my reading | G-F14, G-F12, M15 |
| Is this decision still true of the code? | none | read the entry and the code; the design gives this to the background subagent | SOURCE_OF_TRUTH:68–73 |
| What should I load when resuming? | none | `INDEX.md` and the task's `state.md` | M17, M18, M19 |
| A map of the whole repo | none | `PROJECT_OVERVIEW.md`, `INDEX.md` | M18, G-F18 |
| A `covers:` path that is not Python | none | git and grep | G-F18 |
| Is the graph I am about to query current? | none — do not check, rebuild whole | rebuild, or use git | G-F5, G-F18 |

**Costs, and where there are none.** Measured on other corpora or on this machine, never on a real
`project-memory/`: grep over 10,000 synthetic entries, 0.038 s for one word and 0.060 s for a structured chain
(`S-F13`); grep plus opening every hit, about 226K tokens per question (`S-F4`, `S-F13` — opencode's figure, and D3
records that the other two report no such measurement; `S-F4` measures other corpora, not memory entries); an
`INDEX.md` scan, under 0.01 s and minimal tokens
(`SOURCE_OF_TRUTH.md`); reading one entry, roughly 270 tokens by the 4-characters-per-token assumption (`S-F5`, not
measured); a git last-change lookup at the tool's timing resolution (`G-F12`). **`GAP` for everything that matters
most**: no FTS5-vs-grep measurement on short entries (`S-F5`), no vector measurement on a corpus shaped like
`entries/` (`V-F11`), no graph-vs-grep head-to-head on this repo's own questions (`G-F10`, `M21`), and no wrapper
exists to time a filtered graph query (`G-F18`). The graph-vs-grep head-to-head is now measured on this repo's own
code and docs (BM-1–BM-9, below); the vector-on-`entries/` gap and a real `project-memory/` corpus are not. See
**Measured here: development and testing** below.

**Still unresolved.** Six disagreements the three engines did not settle, kept as positions and not averaged (D1–D6
in the run record): whether FTS5 or the vector index comes first, or whether memory needs a store at all; whether the
FTS/vector benefit has been measured at all; the true token cost of grep-plus-open; the cost of `INDEX.md`; whether
`INDEX.md` carries `covers:` and status; and what counts as a *fired* trigger. **For code and docs, the measurements
settle three of them** (my reading): D1, full-text before vector (BM-4, BM-5); D2, the full-text benefit is measured
on docs (BM-4, BM-6); D3, grep printed about 4,470 characters to the right file on decision questions, not ~226K
tokens (BM-4). For memory entries all six stay open.

**Why no SQLite is visible in this repo.** Three reasons, and none is a rejection. (Since 2026-10-12 three SQLite
caches do exist, in the measurement run's workspace: `runs/20261012-caches-routing/bench/.cache/` holds `fts.sqlite`,
`vec.sqlite` and `graph.sqlite`, 9.5, 10.2 and 4.9 MB (BM-9). They are gitignored and rebuilt there, not part of the
product.) The patterns are gitignored and
the indexes are rebuilt on demand. The SQLite this repo does have, `ancient_games/index.py`,
indexes the **referee's journal**, not memory: it is the working precedent for this exact pattern (7 tables, derived,
~8 ms per journal) but it answers a different question. And the memory cache is gated behind a trigger that has not
fired, because `project-memory/` does not exist yet. The same is true of the code graph: `code_graph/code_graph.py`
already exists, deterministic and full-rebuild, and is the option this document names if that trigger fires.

A fourth reason belongs to the first draft. Its research asked only whether each cache is needed to search memory
*entries*, so it measured nothing on the questions asked during development and testing. The section **Measured here:
development and testing** measures those.

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

## Rules for all three caches

These apply to whichever cache is built. They come from how the researched tools fail.

- **Full rebuild, never patched.** A live, incrementally updated index drifted silently from a clean rebuild: 4.3% of
  edges wrong, with every integrity check passing (`G-F5 drift`). Its makers decided drift cannot be measured cheaply
  (`G-F5c`). A full rebuild of this repo's code graph takes 0.94 s (`G-F12`); the benchmark's own code-graph rebuild
  takes 0.89 s (BM-9); an FTS rebuild of 10,000 synthetic entries takes 0.53 s (`S-F13`).
- **Rebuild before answering when stale.** Before each query, compare the recorded commit or content hash of the
  sources with the index and rebuild if they differ. Build into a temporary file and rename it over the old one
  (`S-F9`, quoted: *"A stale index is worse than no index."*).
- **Fall back when absent.** If the cache file or SQLite's FTS5 is missing, the tool warns once and answers with grep
  (`S-F9`); the same for a missing embedding model (my reading, extending `S-F9`). A mistyped database path silently
  creates an empty database, which looks exactly like a stale one (`G-F5 drift`, failure mode 5), so the tool opens the
  cache read-only and treats "no such file" as absent.
- **Index only active entries** — for `project-memory/` — the same set as `INDEX.md`, with `status` and `covers`
  stored beside each row (`V-F22`, my reading). Otherwise superseded entries come back looking current.

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
| **How** | One stdlib `sqlite3` script, the smallest option in the SQLite node (§5, option B): rebuild to a temporary file and rename; compare the recorded commit or content hash for staleness, so a deleted entry is caught (R3.1); fall back to `rg`. Nothing to install: SQLite 3.45.1 with FTS5 works here (verified 2026-10-12). |

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
   it, and it was found another way (`V-F13`, my reading). The vector index is worth building when, on those recorded
   misses, the hybrid index finds entries full-text did not, and it does no worse on the other questions (R5.2).
5. **Why hybrid only?** On memory-style text, the positive results found combine vectors with keyword search (`V-F6`,
   `V-F7`; `V-F10` is unproven), and vectors alone were the weakest arm when results were returned inline (`V-F3`,
   `V-F4`). So the vector index comes after the full-text index, never
   instead of it. This is a **proposed** policy: on half the file-based pairs in `V-F3` vectors won alone (why 2
   above), so the evidence does not compel it.

### 5W1H

| | |
|---|---|
| **Who** | Built and rebuilt by a script with no model call except the embedding model itself. Read by any agent on demand, through the same command as full-text search. EJ decides to build it when the trigger fires. |
| **What** | One vector per active entry file, with the entry's `status`, `covers`, content hash and embedding-model id stored beside it (`V-F24`: a changed model makes every vector useless). Results merged with the full-text results by reciprocal rank fusion (vector node §Q5, from qmd's README). |
| **When** | After the full-text index exists, and when the R5.2 comparison favours hybrid. Rebuilt with the full-text index, in the same step, so the two cannot disagree (`V-F24`, my reading). |
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
   to path (`G-F14`). One `git log` from the entry's verified revision lists the changes to its `covers:` paths, in
   0.00–0.01 s on this repo (`G-F12`; code-graph node §6). Git is the record itself, so it cannot drift.
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
   - on a review of past path-level flags, the false alarms outnumber the true ones (R5.3).

### 5W1H

| | |
|---|---|
| **Who** | The drift-check script, with no model call. EJ decides to build a graph if one of the three conditions holds. |
| **What** | Today: no graph for the memory drift check. Git on `covers:` paths, plus an `ast` parse of changed Python files if precision is needed. If a condition holds: the repo's own `code_graph/code_graph.py` (Python only, deterministic, full rebuild, no incremental mode, `G-F18`) before any outside tool. |
| **When** | Today the check runs whenever `INDEX.md` is generated (my reading of `SOURCE_OF_TRUTH.md` line 75). A graph, if ever built, is rebuilt in full each time it is used. |
| **Where** | Nothing today. Later, `project-memory/.cache/code-graph.json`, gitignored. |
| **Why** | The five whys above. |
| **How** | One `git log` call per entry: `git log <verified-rev>..HEAD -- <each covers: path>`, where `<verified-rev>` is the revision the entry header records it was last verified against (`SOURCE_OF_TRUTH.md` l.50). A listed commit flags the entry. The baseline is the verification, not the entry's last edit, which an unrelated edit can move (code-graph node §6; this command is my reading). External indexers (codegraph) are not adopted: their win is measured on source-code architecture questions, not on memory (`G-F7`, `G-F14`), and they bring the drift in `G-F5 drift`. |

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

## Core requirements

Acceptance criteria are checkable or they are questions for EJ. Where the research gives no number, the criterion
carries `OPEN:` rather than an invented value. They cover the memory caches, the scope
of the confirmed vision (`vision-statements/caches-memory-vision-statements.md`); R9 carries the vision's "never read
at session start".

### R1 — Derived and disposable
The cache is computed from the files (the memory's markdown, and for the code graph the code its entries cover) and
never holds knowledge of its own (M4, M6).

- **R1.1** Deleting the cache and rebuilding from the files restores every answer. *Example:* `rm -rf
  project-memory/.cache/` → run the documented rebuild → the same query returns the same entries. (M6)
- **R1.2** Memory is fully readable with no cache present. *Example:* with `.cache/` absent, session start and an
  on-demand `grep` over `entries/` both work. (M6)
- **R1.3** The cache directory is ignored by git and a rebuild leaves `git status --short` clean. (M6)

### R2 — Full rebuild, never patched
- **R2.1** The documented rebuild regenerates the whole index from the files; no incremental update path exists.
  *Example:* the rebuild command has no "update" mode. (G-F5 drift)
- **R2.2** The index records what it was built from, so a stale one is detectable. *Example:* the index stores the
  commit or a content hash of its sources, and the query tool compares before answering. A newest-mtime check is not
  enough: a deletion leaves no newer file (R3.1). (S-F9)

### R3 — Stale never answers
- **R3.1** Before answering, the tool compares the index's recorded commit or content hash with the sources and
  rebuilds if they differ, building into a temporary file and renaming over the old one — so a deleted entry cannot
  stay searchable. (S-F9)
- **R3.2** A wrong path is never mistaken for an empty index: the cache is opened read-only and "no such file" is
  treated as absent. *Example:* point the tool at a typo'd path → it warns and falls back to grep, it does not
  create an empty database. (G-F5, failure mode 5)

### R4 — Absence degrades, it does not fail
- **R4.1** A missing cache file or a missing FTS5 warns once and answers with grep. (S-F9)
- **R4.2** A missing embedding model does the same. *(my reading, extending S-F9.)*

### R5 — Nothing is built before its trigger fires
Each cache has an observable trigger. This is the requirement that keeps the whole layer honest. The query-time
counterpart — which store to reach for once a trigger has fired — is the section **When to use which store** above.

- **R5.1 Full-text** — built only when, on the project's own recorded questions, full-text reaches the right entry
  after reading less than `INDEX.md` plus grep does, with no more misses. Measured as the code-and-docs benchmark was
  (BM-1 to BM-9): the same questions through both routes, the characters read to the first right entry, and the misses.
  The comparison decides; no fixed size is set in advance (S-F5, S-F13: nothing is measured yet for a corpus of a few
  hundred to a few thousand short entries).
- **R5.2 Vector** — built only after R5.1 has fired *and*, run on the recorded misses, the hybrid index finds entries
  full-text did not, while doing no worse on the other recorded questions. A "miss" is recorded when an entry existed
  and `INDEX.md`, grep and full-text search all missed it (V-F13). How its results are combined with full-text
  (hybrid only) is a design proposal in **Vector index**, not part of this trigger.
- **R5.3 Code graph** — built only when one of three conditions holds: `covers:` starts naming functions or classes
  rather than files; the check must answer about files on no `covers:` list; or, on a review of past path-level
  flags, the false alarms outnumber the true ones. (code-graph §6, G-F14, G-F18)

### R6 — Only active entries, with their status
- **R6.1** The index holds the same set of entries as `INDEX.md`, each row carrying `status` and `covers`.
  *Example:* a superseded entry never appears in a search result as if current. (V-F22)

### R7 — An answer names its entry
- **R7.1** Every result prints the entry file it came from, so a human can open the source before acting.
  *Example:* search output names `entries/D-0012-*.md`. (M19)

### R8 — The rebuild stays cheap
- **R8.1** The documented rebuild completes without a model call, except the embedding step of R5.2.
  *Example:* rebuild with no model credentials available; the FTS and code-graph paths still work. (M4, M6)
- **R8.2** A rebuild costs less than the cache saves between rebuilds: its time is compared with the reading time the
  cache saved on the recorded questions in that period. If the rebuild costs more, the cache is not kept. Measured, for
  orientation only: 0.94 s (code graph,
  this repo, G-F12) and 0.53 s (FTS, 10,000 synthetic entries, S-F13). Nothing is measured on a real
  `project-memory/` corpus, because it does not exist yet.

### R9 — Never read at session start
- **R9.1** No cache file is part of what a session loads at start. *Example:* the session-start reads in
  `SOURCE_OF_TRUTH.md` (§ When it will be used) name no file under `project-memory/.cache/`; a start hook that
  opens `.cache/index.sqlite` fails this. (The vision's never-rule; M18)

## Example numbers by case

The triggers in R5 and R8.2 are comparisons. The measurement decides them, so no number is fixed in advance. This
section shows **what those comparisons have come out at elsewhere**, by agent type and condition, so a reader knows
roughly where a project stands before measuring. These are examples with sources, not thresholds.

Run: `runs/20261012-caches-numbers/`. Its source ids are:
- `W-*`: web research (`nodes/web.md`);
- `OC`: opencode's research (`nodes/opencode.md`);
- `SZ`: the SEZA measurement (`nodes/seza.md`; every number with its command);
- `CX`: codex's independent second look at SEZA, by agent type (`nodes/codex.md`);
- `BM-*`, `S-F*`, `V-F*`, `G-F*`, `s3-F*`: as above.

Web quotes are model-made extracts, not byte-checked, except W-1. Numbers marked *my arithmetic* are computed from a
sourced figure.

### The index read at session start (`INDEX.md`, `MEMORY.md`), by agent type

| Agent | Window | Limit on files loaded at start | Measured effective context | Example |
|---|---|---|---|---|
| Claude Code (Claude 5.x) | 1M (W-8) | `MEMORY.md`: "first 200 lines … or the first 25KB, whichever comes first"; `CLAUDE.md`: target under 200 lines (W-1) | Opus 4.6, MRCR v2: 76% at 1M (W-14); 93% at 256K (W-15, reported) | 25 KB binds first: about 150 lines at 167 B per line (W-1), about 107 lines at SEZA's 233 B per line (*my arithmetic*, SZ) |
| Codex (GPT-6.x) | 1.05M per the API (W-9), but this machine's Codex model cache says `context_window: 500000`, 95% effective, so about 475K (CX) | `AGENTS.md` combined up to 32 KiB (`project_doc_max_bytes`) (W-2) | GPT-5.4: 79.3% at 128K–256K, 36.6% at 512K–1M (W-15, reported) | instructions plus index under 32 KiB |
| agy (Gemini 3.1 Pro / 3.8 Flash) | 1,048,576 (W-9, CX) | 24,000 bytes per rule file, **and** a 20,000-token budget across all rules (CX, official page); 12,000 characters in other reports (W-4, conflict) | 84.9% at 128K, 26.3% at 1M (W-15, reported) | under 12,000 characters if both readings must hold (*my reading*) |
| opencode (MiniMax M3 / M2.7) | 1M / 204,800 (W-9) | no limit stated (W-6) | GAP | follow the strictest agent sharing the repo |
| dsh (DeepSeek flash / V4 pro) | 1,048,576 (CX) | a 65,536-byte budget for the instruction files it loads (CX, from its loader docs) | GAP | instructions plus index under 64 KiB |
| Qwen Code | — | its auto-memory index is capped at 200 lines or 25,000 bytes (`MAX_MANAGED_AUTO_MEMORY_INDEX_LINES` / `_BYTES`, CX); it also warns when always-loaded context passes 15% of the window, an advisory only (CX) | — | the index cap binds first: under 25,000 bytes, as for Claude |
| Cursor | — | rules "under 500 lines" (W-3) | — | — |

**Why the start load should stay small, whatever the window:**
- Half of 17 models kept satisfactory performance only up to 32K (RULER, W-10).
- 11 models fell below 50% of their baseline at 32K when the question and the answer share few words (NoLiMa, W-11).
- Focused prompts of about 300 tokens beat full ones of about 113K (W-13).
- Context files raised inference cost by over 20%, with no general success gain (W-17).
- At 500 simultaneous instructions, the best model was 68% accurate (W-16).

**Use case, SEZA (SZ, CX):**
- The start load by agent, as estimates: Claude Code 61,993 B (about 15.4K tokens, including the global `CLAUDE.md`;
  SZ measured 58,427 B without it); dsh 46,319 B (about 11.5K); Codex and agy 29,166 B each (about 7.2K) (CX). All are
  well under 15% of every window above.
- `MEMORY.md` is 52 lines and 12,108 B, within Claude's limit.
- The 52 topic files (159,524 B) would not fit in 25 KB. That is why they are an index plus files read on demand.

**When several agents share a project, the binding limit is the smallest one among them** (*my reading*).

### R5.1: full-text against `INDEX.md` plus grep

| Case | What was measured | Source |
|---|---|---|
| 1,144 docs, 1.7M tokens | the grep agent is more accurate (77.4 vs 74.7) but reads 226K tokens per question against BM25's 5.8K | W-22 |
| 6,980 docs, 8.5M tokens | accuracy crossover: BM25 70.1 vs 69.9; BM25 ahead at every larger tier | W-22, S-F4 |
| 511,959 docs, 600.8M tokens | BM25 50.5 vs the grep agent 30.7 | W-22 |
| This repo's code and docs, 490 files, 4.8 MB | full-text prints about a sixth of grep's characters before naming a right file | BM-6 |
| SEZA memory: the Claude memory folder (55 files) and a wider set of 257 files (2.5 MB) | grep takes 4–7 ms but prints from 361 B (a narrow term, memory folder) to 109,519 B, about 27K tokens (a broad term, 257-file set). Over the 257 files, a full-text proxy ranked the right file first on 3 of 5 questions and missed on 2 (n=5, one reader) | SZ |
| A tool result too large to read | filtering in code instead of reading: 150,000 tokens down to 2,000 | OC (Anthropic, 2025-11-04) |

**My reading:** on accuracy, grep stays competitive until millions of tokens. On **tokens read**, full-text wins much
earlier: on SEZA-sized memory, a single broad term already floods grep's output. The R5.1 comparison measures exactly
that.

### R5.2: the vector index

| Case | What was measured | Source |
|---|---|---|
| Loading about 115K tokens of history instead of retrieving | 30%–55% lower accuracy (GPT-4o, Llama 3.1) | W-18 |
| Long context against retrieval, 100K–1M tokens | retrieval better for 3 of 4 models at 100K, and for all 4 from 500K | W-19 |
| Vendor guidance | under about 200,000 tokens, the whole base can go in the prompt | V-F8 (2024) |
| Dense against BM25, 1,144–511,959 docs | dense lowest at every tier in the table (7 tiers) | W-22 |
| Enterprise corpus, 500K docs | vector 51.4 vs BM25 68.8 correctness | V-F4 |
| Code, 1,000 or more files | +12.5% accuracy with vector search (Cursor), but 15 days later Cursor shipped Instant Grep and says it "does not store embeddings of your codebase for search" | V-F6, OC |
| A memory growing 10× (1M to 10M tokens) | Mem0 64.1 to 48.6 (vendor's figures) | W-20 |
| SEZA | no recorded misses, so the comparison has nothing to run on | SZ |

**My reading:** retrieval beats loading everything somewhere around 100K–500K tokens, but it is keyword retrieval
that wins. Vectors earn a place only on recorded meaning-misses, which is what R5.2 tests.

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

### R8.2: rebuild cost

| Store | Measured | Source |
|---|---|---|
| Full-text | 0.169 s for 490 files (index 9.5 MB, about 2× the source); 0.53 s for 10,000 entries; 2.57 s for 50,000; SEZA 0.004 s for 55 files, 0.54 s for 2,013 md files (34 MB), both in an in-memory database, so no disk writes (SZ) | BM-9, S-F13, SZ |
| Vector | 0.936 s for 490 files with model2vec; embedding speed 81,018 samples/s for model2vec against 274 for a MiniLM fine-tune (model2vec's own table); sqlite-vec builds 1M × 128 dims in about 4 s, embedding excluded | BM-9, OC, W-27 |
| Code graph | 0.94 s for 126 `.py` files; codegraph about 100 s for about 27k files | G-F12, W-25 |

**My reading:** at the sizes of this repo (490 files) and of SEZA's whole markdown corpus (2,013 files; its memory
stores alone are 152–201 files), a rebuild takes under a second (SEZA's figure is in-memory, not on disk). Larger
corpora take seconds (2.57 s for 50,000 entries; about 4 s for sqlite-vec at 1M vectors, embedding
excluded) to minutes (codegraph, about 100 s for about 27k files). A heavy embedding model adds the most per file.
So R8.2 starts to bite with corpus size and with a slow embedding model.

### SEZA today, trigger by trigger (SZ, the researcher's reading)
- **R5.1:** no verdict at n=5.
- **R5.2:** not met.
- **R5.3:** cannot be evaluated; the graph that exists is barely used (production queries: GAP).
- **R8.2:** cheap.

SEZA's own `project_memory search` was used 42 times in 15 sessions, with none after 2026-09-24.

**What actually went wrong in SEZA was not search** (CX):
- Its start index carried outdated state: the cleanup audit records *"Memory index stale"*
  (`seza/runs/20261010-project-cleanup/STATUS-GRAPH.md:268`).
- Its derived graph was missing when it was asked for: *"graph is missing; run sync or rebuild"*.

**My reading:** a faster cache would have returned the same stale entries. R3 (stale never answers) and the drift
check matter more here than any of the three stores.

## What this changes elsewhere (proposed, not done)

- `SOURCE_OF_TRUTH.md` lists as undecided "how the script tells that the entry changed earlier than the code". The
  research suggests an answer for EJ to decide: list the commits to its `covers:` paths since the
  revision the entry was last verified against, not since the entry's last edit.
- `SOURCE_OF_TRUTH.md` line 104 can keep `.cache/` as written. This document says when each part of it is built.

## Not known

- No trigger has a fixed number. Each is a comparison (R5, R8.2) that is measured once `project-memory/` has entries
  and recorded questions; the measurement decides (EJ, 2026-10-12: *"this is design guide, how can I give you a
  number?"*).
- No measurement exists of any of the three on a project-memory corpus. All evidence is on other corpora: source code,
  chat memory, enterprise documents.
- The researchers' web reads went through extracts. `S-F*` quotes are not byte-checked (`sqlite-fts.claude.md`,
  header). `V-F*` quotes were checked against saved copies.
- The planted "tool that does not exist" check in the research was void: the names were readable in the run's
  `state.md` (see that file's log).

## Unresolved after review

The round-2 reviews agreed on most points; these are the points they did not settle. Each position is kept as its
reviewer stated it and is not averaged.

| point | agy | codex | opencode |
|---|---|---|---|
| The BM-9 speed bound and the audit's `git ls-files` overhead | Holds codex's position: the bound holds. | The overhead biases grep's comparative timing, but removing it lowers grep's time and does not break the 15 ms bound; it should be disclosed. | The overhead makes the speed comparison unsafe and the finding undercuts BM-9. |
| Corpus snapshot stability during the benchmark build | Holds codex's position: carry the warning; do not say no rerun happened. | A later run on the repaired harness is recorded, so "no rerun" is too strong; the builder's snapshot-stability warning is unclosed and should be carried. | The builder's note that the numbers must be re-run on a stable snapshot is unclosed; a rerun is needed. |
| The audit's lower-severity findings | Sides with codex. | Not every remaining finding is a defect (one reports no problem), and the vector-deduplication finding does not change the hit rate. | The lower-severity findings remain open, and some of them bear on the text. |
| Discovery versus exhaustive routes in the memory "none" rules | Adopts codex's position. | Discovery may use a derived cache; only exhaustive enumeration and proof of absence need a files-only route. | Keeps A's rows with citation fixes. |
