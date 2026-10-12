# Caches — product vision statement

> **Status: settled** (accepted by EJ on 2026-10-12, and again after the changes below: *"others can accept and
> apply"*). EJ's first words: *"ok the vision is confirm"*. Drafted 2026-10-12 by the COO from the research in
> `runs/20261012-memory-caches/nodes/` and `runs/20261011-project-memory-engines/RECOMMENDATION.md`; rewritten the same
> day at EJ's direction — more direct, fewer hedges.
>
> **Drawn from:** `docs/memory-system/CACHES.md`, which carries the core requirements (Build / Keep / Read) this
> vision serves. This file holds the vision only, so each has one copy (`docs/workflow-templates/blueprint.md` keeps
> vision and requirements in separate section files).
>
> **Whose it is.** Per the blueprint template, the product vision is EJ's — *"an agent may only write down what EJ
> has said"*. This was drafted from the research at his request and settled by him on 2026-10-12.
>
> **Changed 2026-10-12:** the code graph removed at EJ's direction (*"code graph should have it's own project"*); its
> draft is `docs/code-graph/CODE_GRAPH.md`. The problem now names both ways it shows up, one per cache — the vector
> reason was missing (EJ: *"ok write it into the vision"*). "How we know it works" now tests that the right entry is
> found for less (B1.1, B1.2), not only that a rebuild repeats; and the rebuild's "no model call" now excepts the vector
> embedding step, as B5.1 does (EJ: *"ok write it into the vision"*). "Too many entries" no longer says `INDEX.md` stops
> listing every active entry: the full-text trigger is the B1.1 comparison (EJ: *"the comparison for full-text"*), and
> `SOURCE_OF_TRUTH.md` requires `INDEX.md` to list every active entry and still fit (K6.1, Rd3.1). Then, on acceptance
> (EJ, 2026-10-12: *"others can accept and apply"*): "who decides" replaces "who sets the triggers"; the grep timing is
> one labelled figure; `G-F5` is labelled as a code-graph study; and "never answers from a stale index" is added. The
> tests run on "the project's own questions and noted misses": the full question log was dropped (EJ, 2026-10-12: *"yes
> , made that change"*).

The caches are two optional indexes over the project's markdown memory — full-text search and vector search. Both
live in `project-memory/.cache/`, both are gitignored, and both are rebuilt from the files. Neither is needed today.

**Who it is for.** An agent retrieving an entry on demand. Not the human reviewer, who reads the entries themselves,
and not EJ, who decides whether a cache is built once its comparison passes (B1.0).

**The problem it solves.** The memory is markdown in git, and today `INDEX.md` plus grep finds what an agent needs — in
the researcher's own test, a one-word grep over 10,000 synthetic entries took 0.038 s (`S-F13`). As the memory grows,
that stops being enough in two ways:
- **Too many entries — full-text search.** Reaching the right entry through `INDEX.md` and grep means reading more
  and more: grep returns unranked matches, and every hit an agent opens costs context (`S-F1`).
- **Different words — vector search.** The agent's words differ from the entry's, so `INDEX.md`, grep and
  full-text search all miss an entry that exists (`V-F13`).

The caches exist to keep finding the right entry cheap when that happens — and not before.

**What it will never do.**
- It is never the source of truth. The markdown is, always, and a cache holds nothing the files do not (`M4`, `M6`).
- It is never patched incrementally. It is rebuilt whole or not at all — a live, incrementally synced index drifted
  4.3% of its edges from a clean rebuild with every integrity check passing (`G-F5`: a study of a code-graph tool,
  kept as evidence of how a patched index fails).
- It never answers from a stale index. Before answering, it is checked against the files and rebuilt if they
  differ (K2) — stale state, not search, is what went wrong in SEZA (`CACHES.md` § SEZA today).
- It is never read at session start (`M18`).
- It is never built before its own trigger fires. Every trigger is an observable comparison, and the measurement
  decides it, not a number set in advance (EJ, 2026-10-12: *"this is design guide, how can I give you a number?"*).
- It never becomes a second thing to keep in sync: delete the folder and memory is unaffected.

**How we know it works.** Two tests, on the project's own questions and noted misses.
- **It finds the right entry, for less.** Full-text search reaches the right entry after reading less than
  `INDEX.md` plus grep, with no more misses (B1.1). Vector search, run on the recorded misses, finds entries
  full-text did not, and does no worse on the other questions (B1.2).
- **It holds nothing of its own.** Delete the cache, rebuild it from the files, and the same query returns the
  same entries, with no model call except the vector embedding step (`M6`, B5.1; a 10,000-entry FTS rebuild takes
  0.53 s, `S-F13`).

One caveat travels with every number here: none of it has been measured on a real `project-memory/` corpus,
because that corpus does not exist yet (`S-F5`, `V-F11`).
