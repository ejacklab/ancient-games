# State — 20261012-memory-caches

Rules: one writer at a time. Read this file before your step; update it after. It holds progress and results only —
never reasoning; put notes in your own output file. Never delete a log line.

## Challenge (verbatim)

> now next one research and design the sqlite , vector and code-graph stores caches, answring the 5 why and 5W1H
> Framework questions

## Restatement (method 3.0)

**Objective.** For each of the three caches that `docs/memory-system/SOURCE_OF_TRUTH.md` allows under
`project-memory/.cache/` (SQLite full-text search, a vector index, a code graph): decide whether it is needed, and if
so, design it. Each store gets five whys and the 5W1H questions (who, what, when, where, why, how), grounded in
research.
**In scope.** The three stores as derived caches: gitignored, rebuilt from the markdown and the code, never the source
of truth (RECOMMENDATION M4, M6). Includes the condition under which each one is worth building, and "not needed" as
an allowed answer.
**Out of scope.** Building any of them; changing the source-of-truth rule; user and agent memory.
**Six whys (short).** Why the caches: reading every file or grepping costs context, and some questions grep can't
answer well (find an entry by meaning; what an edit touches). Why now: the design names `.cache/` but says nothing
else about it. Why three: each answers a different kind of question (words, meaning, structure). Why research first:
the repo's own record says it builds graphs nobody queries (`docs/KNOWLEDGE_GRAPH_DESIGN.md` §1: `loop/graph_memory.py`,
seza `.ctxgraph/graph.db`), so "is it needed" comes before "how".
**Provisional category.** research and reports → document and explain (pipeline: research → design → review).

## Baseline

```
 M docs/TASK_TYPES_LEDGER.md
?? .claude/workflows/research-agent-memory.js
?? docs/research/20261011-agent-memory-graph-r2/
?? docs/research/20261011-agent-memory-graph/
?? runs/20261011-agent-memory-graph-r2/
?? runs/20261011-agent-memory-graph/
?? runs/20261011-project-memory-engines/
```

## Already known (read 2026-10-12, not re-verified against the URLs)

- RECOMMENDATION M4: a vector index is refused as the store; at most a rebuildable index, "only when the project's own
  queries justify it". M6: SQLite is derived, gitignored, rebuildable; "its absence must not prevent reading memory".
  CP1 (SQLite as the state store) is contested: opencode dissents.
- Research r2: s3-F4 StateTape reads staleness off a code-graph diff with no model call; s3-F20/F34 MOOSEDev beat
  vector top-k on supersession and set questions, but relevance recall and token cost were "largely equivalent";
  s3-F25/F27 a live auto-synced code graph drifted silently (4.3% of edges wrong) and a CLI served stale answers.
- In the repo: `code_graph/code_graph.py` (stdlib Python code graph, 981 lines, run `20261005-code-graph-tool`);
  `docs/KNOWLEDGE_GRAPH_DESIGN.md` (graph as SQL tables, no graph engine). Its cited source
  `store-research/wave2-kg/MERGED.md` is not on disk.
- This machine: SQLite 3.45.1 with FTS5 works (verified 2026-10-12, in-memory test).

## Steps

| # | Node | Engine | Status | Output file |
|---|---|---|---|---|
| 1a | Research: code graph (read-only `--agent plan`, prints to stdout; variant not set, provider default) | opencode `minimax-coding-plan/MiniMax-M3.1-Flash-Preview` | done | nodes/code-graph.opencode.stdout.md |
| 1b | Research: SQLite full-text index | Claude subagent, `sonnet` | done | nodes/sqlite-fts.claude.md |
| 1c | Research: vector index | Claude subagent, `sonnet` | done | nodes/vector.claude.md |
| 2 | Design: five whys + 5W1H per store | main session (claude-opus-5-5) | done | docs/memory-system/CACHES.md |
| 3 | Blind review against the sources, one planted defect | Claude subagent `sonnet` (document-and-explain default) | done | nodes/review.claude.md |
| 4 | EJ accepts or sends back | EJ | todo | — |

## Log (append only)

- 2026-10-12 run folder created; restatement and plan written. Readiness: claude, codex, agy and qwen are installed
  (versions verified); whether agy can run a task is **unknown** until the canary runs. Waiting for EJ's go-ahead.
- 2026-10-12 EJ: "get help from opencode, and your subagents" — agy is replaced. Research split by store, three
  read-only nodes run in parallel (independent questions, each writes only its own output file). Shared brief:
  `brief.md`; opencode command line: `launch-opencode.sh`. Each brief carries one planted question about a tool
  that does not exist (`hollowfern`, `quillvec`, `tarnline`); the right answer is not-found.
- 2026-10-12 node 1a done: exit 0, 38,893 bytes, used WebFetch (stderr), ran `code_graph.py` into `/tmp/opencode/`
  (scratch). **The planted check is void for all three nodes:** the log line above names the planted tools, and the
  brief tells each node to read this file. opencode's stdout line 5: "`tarnline` appears to be a planted trap. Let
  me confirm from the run folder." It still searched (GitHub, PyPI, npm: no hits), but the control no longer shows
  it would refuse unprompted. Cause: the COO wrote the plant into a file the workers read. Fix for next time: keep
  plants out of any file a worker is given.
- 2026-10-12 node 1b done: 22,369 bytes, 37 tool calls. Planted check void here too: its line 27 says it found
  `hollowfern` listed in this file. Ran its own synthetic timing tests (labelled as its own) in scratch; no file
  outside `nodes/` was added (`git status` checked).
- 2026-10-12 node 1c done: 30,803 bytes, 59 tool calls; quotes checked against saved copies (its header).
- 2026-10-12 node 2 done: `docs/memory-system/CACHES.md` (153 lines). Verdict: none of the three caches is needed
  today; each has a trigger, and every trigger number is left to EJ.
- 2026-10-12 node 3 started: blind review of `verify/CACHES-review-copy.md`, which carries one planted defect. Its
  location is kept out of every file the reviewer may read and will be logged here after the verdict.
- 2026-10-12 node 3 done: **REPAIR**, 13 findings (0 high, 5 medium, 8 low). The plant was an invented trigger,
  "or `entries/` passes 500 files", in the SQLite 5W1H When row of `verify/CACHES-review-copy.md` line 68. The
  reviewer caught it as F-1 at line 68, so this review can fail. The other 12 were checked by the main session
  against the cited lines and all hold.
- 2026-10-12 repair by the main session: F-2 to F-13 fixed in `docs/memory-system/CACHES.md` (F-1 was the plant,
  present only in the review copy). Not re-reviewed. Waiting for EJ (step 4).
- 2026-10-12 EJ agreed: the SQLite node's timing script (`S-F13`) was copied from the session scratchpad to
  `nodes/evidence/bench.py`. The synthetic corpora and databases it generated (about 134 MB) were not kept; the
  script regenerates them. Run committed and pushed with `docs/memory-system/CACHES.md`.
- 2026-10-12 the commit is `7757f21` (12 files, 2,213 insertions); `git branch -r --contains 7757f21` lists
  `origin/master`. Step 4 is still open: the header of `docs/memory-system/CACHES.md` says "draft, not yet accepted
  by EJ".
- 2026-10-12 EJ accepted `docs/memory-system/CACHES.md` ("yes I accept"), including R1–R9; its status line now says so.
