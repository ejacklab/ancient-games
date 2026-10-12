# Caches — product vision statement

> **Status: settled** (accepted by EJ on 2026-10-12). EJ's words: *"ok the vision is confirm"*. Drafted 2026-10-12
> by the COO from the research in
> `runs/20261012-memory-caches/nodes/` and `runs/20261011-project-memory-engines/RECOMMENDATION.md`; rewritten the
> same day at EJ's direction — more direct, fewer hedges.
>
> **Drawn from:** `docs/memory-system/CACHES.md`, which carries the core requirements (R1–R9) this vision serves.
> This file holds the vision only, so each has one copy (`docs/workflow-templates/blueprint.md` keeps vision and
> requirements in separate section files).
>
> **Whose it is.** Per the blueprint template, the product vision is EJ's — *"an agent may only write down what EJ
> has said"*. This was drafted from the research at his request and settled by him on 2026-10-12.

The caches are three optional indexes over the project's markdown memory — full-text search, vector search, and a
code graph. All three live in `project-memory/.cache/`, all three are gitignored, and all three are rebuilt from the
files. None of them is needed today.

**Who it is for.** An agent retrieving an entry on demand. Not the human reviewer, who reads the entries themselves,
and not EJ, who sets the triggers.

**The problem it solves.** The memory is markdown in git, and today `INDEX.md` plus grep finds what an agent needs —
at 10,000 entries a grep takes 0.038–0.06 s (`S-F13`). It stops being enough as the memory grows, for two reasons:
`INDEX.md` can no longer list every active entry under its size limit, so the one-line scan of everything is gone;
and grep returns unranked matches, where every hit an agent opens costs context (`S-F1`). The caches exist to keep
finding the right entry cheap at that size — and not before.

**What it will never do.**
- It is never the source of truth. The markdown is, always, and a cache holds nothing the files do not (`M4`, `M6`).
- It is never patched incrementally. It is rebuilt whole or not at all — a live index drifted 4.3% of its edges from
  a clean rebuild with every integrity check passing (`G-F5`).
- It is never read at session start (`M18`).
- It is never built before its own trigger fires. Every trigger is an observable comparison, and the measurement
  decides it, not a number set in advance (EJ, 2026-10-12: *"this is design guide, how can I give you a number?"*).
- It never becomes a second thing to keep in sync: delete the folder and memory is unaffected.

**How we know it works.** Delete the cache, rebuild it from the files, and the same query returns the same entries,
with no model call. That is the whole test (`M6`; a 10,000-entry FTS rebuild takes 0.53 s, `S-F13`; this repo's code
graph rebuilds in 0.94 s, `G-F12`). One caveat travels with every number here: none of it has been measured on a
real `project-memory/` corpus, because that corpus does not exist yet (`S-F5`, `V-F11`).
