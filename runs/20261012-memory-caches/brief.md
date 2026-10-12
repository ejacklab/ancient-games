# Research brief — memory caches (run 20261012-memory-caches)

You are researching **one** of three caches for a project's memory. Your store is named at the end of this brief.
You research only. You do not design or build anything.

## The setting

The project memory is plain markdown kept in the git repo: `AGENTS.md` and `project-memory/` with `INDEX.md`
(generated, one line per entry), `entries/` (one file per decision, fact, lesson, observation, hypothesis or runbook;
each has `covers:` naming the code paths it is about), `work/<task-id>/` and `journal/`. The design is
`/home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md`. Read it first.

The design allows `project-memory/.cache/`: optional, gitignored, rebuilt from the files, **never the source of
truth**. Its absence must not stop anyone reading memory (recommendation M4, M6). There are three candidate caches:
a SQLite full-text index, a vector index and a code graph. The question for each is **whether it is needed at all**,
and only then what it should be. "Not needed, grep and `INDEX.md` are enough" is a valid finding if the evidence says
so.

Already known, so do not redo it: the "Already known" section of
`/home/smoke01/dev/ancient-games/runs/20261012-memory-caches/state.md`, and the findings it cites in
`/home/smoke01/dev/ancient-games/docs/research/20261011-agent-memory-graph-r2/` (s3-F4, F20, F25, F27, F34). Build on
them and cite them by id.

This machine: Python 3.12, SQLite 3.45.1 with FTS5 working, numpy installed, an NVIDIA RTX 4070 Ti SUPER with 16 GB.
Not installed: sqlite-vec, sentence-transformers, fastembed, tree-sitter.

## What to find, for your store

1. **The questions it answers.** Which questions does an agent working on the code ask that this store answers
   better than grep over `entries/` plus reading `INDEX.md`? Give evidence, not intuition.
2. **When it pays off.** Measured evidence on when it starts beating grep: corpus size, query type, token cost,
   accuracy. Numbers only with their source. If no measurement exists, say so.
3. **Current tools.** Tools from 2025–2026 that build this kind of index from files that stay the source of truth:
   how each is built, how it is rebuilt, rebuild time, size on disk, and whether it runs locally.
4. **How it fails.** Drift from the files, stale answers, silent wrong results, and how the tools detect or prevent
   them.
5. **What fits here.** Given the machine above, what would be the smallest working version? Report options; do not
   choose.

## Rules

- Use the web for current sources. Open the primary source (paper, repo, docs) before you cite it.
- Every finding gets an id (F1, F2, …), a label, a URL with its date, and a verbatim quote from the source:
  - **CONFIRMED**: you read the primary source and the quote is from it.
  - **INFERRED**: your reasoning from confirmed findings. Say which ones.
  - **UNPROVEN**: a secondary source, or a claim you could not open.
  - **GAP**: you looked and found nothing.
- Never invent a number. A missing number is a GAP.
- End with two lists: **Not found** (what you looked for and could not find) and **Not checked** (what you did not
  look at).
- Also answer this question: {{PLANT}}
