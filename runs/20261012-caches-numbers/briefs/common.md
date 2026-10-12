## Context and evidence rules (shared by every engine in run 20261012-caches-numbers)

The design guide is `/home/smoke01/dev/ancient-games/docs/memory-system/CACHES.md`. It describes memory caches
(SQLite full-text, vector, code graph) over a project's markdown memory. Its triggers (R5.1, R5.2, R5.3, R8.2) are
**comparisons, not fixed numbers**. The owner wants **example values**: "in this case, with this agent, the number
tends to be about X, because of this source".

Earlier research already in the repo: `docs/research/20261011-agent-memory-graph-r2/INDEX.md` and
`runs/20261012-memory-caches/nodes/*.md` (ids S-F*, V-F*, G-F*). Cite them by id instead of redoing them.

**Rules for evidence:**
- Every number comes with its source (a URL and its date, or a command and its output) and a verbatim quote.
- Label each number:
  - **CONFIRMED**: you opened the primary source;
  - **REPORTED**: a secondary source;
  - **GAP**: not found.
- Never present an estimate of your own as a finding.

Change no files. Print your whole answer to stdout.

End with a table, **"Example values"**, with the columns: condition, agent or model, value, what it supports
(R5.1 / R5.2 / R5.3 / R8.2 / INDEX.md size), and the source. Then add "Not found" and "Not checked" lists.
