# Caches — product vision statement

> **Status: settled** (accepted by EJ on 2026-10-12). EJ's words: *"ok the vision is confirm"*. Drafted 2026-10-12
> by the COO from the research in
> `runs/20261012-memory-caches/nodes/` and `runs/20261011-project-memory-engines/RECOMMENDATION.md`; rewritten the
> same day at EJ's direction — more direct, fewer hedges.
>
> **Drawn from:** `docs/memory-system/CACHES.md`, which carries the core requirements (Build / Keep / Read) this
> vision serves. This file holds the vision only, so each has one copy (`docs/workflow-templates/blueprint.md` keeps
> vision and requirements in separate section files).
>
> **Whose it is.** Per the blueprint template, the product vision is EJ's — *"an agent may only write down what EJ
> has said"*. This was drafted from the research at his request and settled by him on 2026-10-12.
>
> **Changed 2026-10-12:** the code graph removed at EJ's direction (*"code graph should have it's own project"*);
> its draft is `docs/code-graph/CODE_GRAPH.md`. The problem now names both ways it shows up, one per cache — the
> vector reason was missing (EJ: *"ok write it into the vision"*). "How we know it works" now tests that the right
> entry is found for less (B1.1, B1.2), not only that a rebuild repeats; and the rebuild's "no model call" now
> excepts the vector embedding step, as B5.1 does (EJ: *"ok write it into the vision"*).

The caches are two optional indexes over the project's markdown memory — full-text search and vector search. Both
live in `project-memory/.cache/`, both are gitignored, and both are rebuilt from the files. Neither is needed today.

**Who it is for.** An agent retrieving an entry on demand. Not the human reviewer, who reads the entries themselves,
and not EJ, who sets the triggers.

**The problem it solves.** The memory is markdown in git, and today `INDEX.md` plus grep finds what an agent needs —
at 10,000 entries a grep takes 0.038–0.06 s (`S-F13`). As the memory grows, that stops being enough in two ways:
- **Too many entries — full-text search.** `INDEX.md` can no longer list every active entry under its size limit,
  so the one-line scan of everything is gone; and grep returns unranked matches, where every hit an agent opens
  costs context (`S-F1`).
- **Different words — vector search.** The agent's words differ from the entry's, so `INDEX.md`, grep and
  full-text search all miss an entry that exists (`V-F13`).

The caches exist to keep finding the right entry cheap when that happens — and not before.

**What it will never do.**
- It is never the source of truth. The markdown is, always, and a cache holds nothing the files do not (`M4`, `M6`).
- It is never patched incrementally. It is rebuilt whole or not at all — a live index drifted 4.3% of its edges from
  a clean rebuild with every integrity check passing (`G-F5`).
- It is never read at session start (`M18`).
- It is never built before its own trigger fires. Every trigger is an observable comparison, and the measurement
  decides it, not a number set in advance (EJ, 2026-10-12: *"this is design guide, how can I give you a number?"*).
- It never becomes a second thing to keep in sync: delete the folder and memory is unaffected.

**How we know it works.** Two tests, both on the project's own recorded questions.
- **It finds the right entry, for less.** Full-text search reaches the right entry after reading less than
  `INDEX.md` plus grep, with no more misses (B1.1). Vector search, run on the recorded misses, finds entries
  full-text did not, and does no worse on the other questions (B1.2).
- **It holds nothing of its own.** Delete the cache, rebuild it from the files, and the same query returns the
  same entries, with no model call except the vector embedding step (`M6`, B5.1; a 10,000-entry FTS rebuild takes
  0.53 s, `S-F13`).

One caveat travels with every number here: none of it has been measured on a real `project-memory/` corpus,
because that corpus does not exist yet (`S-F5`, `V-F11`).
