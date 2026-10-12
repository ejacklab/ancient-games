# Workflow design — 20261012-caches-routing

## Challenge (verbatim)

> now we already have the first draft docs/memory-system/CACHES.md , design and execute a workflow to enhance this
> using all the availabel tools you have, with the respect towards vision-statements/caches-memory-vision-statements.md
> , and why I don't see the sqllite, and because it is caches, we need to know when to use sqllite , when to use
> vector, and when to use the code-graph stores , so our development and testing will be more effective in speed ,and
> token cost, create a new folder your own as workspace

## Restatement (method 3.0)

**Objective.** `CACHES.md` gains a routing rule, based on measurements: for each kind of question an agent asks
during development and testing, which store to use (SQLite full-text, vector, code graph, or plain grep/git), judged on
**speed** (seconds) and **token cost** (tokens the agent reads or spends).

**Why the first draft missed it.** Its research brief asked only whether each cache was needed to search
memory *entries*, and for entries grep wins at small sizes. So it built nothing and measured nothing on real
questions. EJ's aim is wider: development and testing, which means code and tests as well as memory.

**In scope.**
- Measure all three stores, plus grep as the baseline, on this repo. Its 124 `.py` and 374 `.md` files are real code,
  tests and memory-like docs.
- Prototype each store in the workspace only.
- Write a routing table and an enhanced `CACHES.md`.
- Propose vision changes as a separate file for EJ.

**Out of scope.**
- Building the caches into the product.
- Editing the vision file: it is EJ's, so changes are proposals only.
- Removing the R1–R8 requirements another session added to `CACHES.md`.
- Committing.

**Respecting the vision.** Every prototype keeps the vision's never-rules:
- never the source of truth;
- full rebuild, never patched;
- never read at session start;
- delete the folder and memory is unaffected.

The vision's "none needed today" and "who it is for: an agent retrieving an entry" are tested, not assumed. If the
measurements disagree, that goes to EJ as a proposed vision change.

**Category.** research → code generation (benchmark harness) → document and explain, with review.

## Readiness (verified 2026-10-12)

| Tool | Status |
|---|---|
| codex `gpt-6.1-sol` | canary returned `CANARY-OK`, exit 0 |
| opencode `minimax-coding-plan/MiniMax-M3.1-Flash-Preview` | ran a node today (run 20261012-memory-caches) |
| Claude subagents, `claude -p` | in use this session |
| SQLite 3.45.1 + FTS5 | verified |
| model2vec 0.10.0 (`potion-base-8M`, 256 dims), sqlite-vec 0.1.9, numpy | installed in a scratch venv (`uv`), embedding verified |
| `code_graph/code_graph.py`, `rg` | present |
| GPU RTX 4070 Ti SUPER 16 GB | present; not needed by model2vec |

## Nodes (sequential, state file `state.md`)

| # | Node | Engine | Why this engine | Output |
|---|---|---|---|---|
| 1a | Question set: 40 real dev/test questions about this repo, each with what the asker knows (question, grep terms, symbol or file) kept apart from the **gold** answer (file paths or test ids), every gold answer checked by a command | codex `gpt-6.1-sol`, high, read-only sandbox | A different kind from the builder and the writer, so the questions are not shaped to the tools | `nodes/queries.codex.stdout.md` → `queries.json` |
| 1b | Benchmark harness: chunk the repo, full-rebuild FTS / vector / graph stores, query routes, runner | opencode M3.1-Flash, build agent, workspace only | Build work gives opencode priority | `bench/` |
| 2 | Verify: gold spot-check by `rg`; harness audit (no gold leakage, rebuild determinism, R1.1 delete-and-rebuild); repair loop of at most 2 attempts | Claude subagents (Workflow) | A different kind from both makers | `nodes/verify.md` |
| 3 | Run the benchmark (script, no model): per question and route, hit@1/5/10, characters read to the first gold hit (a token proxy), seconds; rebuild time and size | script | Objective numbers | `results.json`, `results.md` |
| 4 | Agent trial: 6 questions × 2 arms (grep tools only, against grep plus the cache CLI), `claude -p --output-format json`, real token usage and correctness | script calling `claude-sonnet-5-5` | The real token cost, not a proxy | `trial/` |
| 5 | Routing table and enhanced `CACHES.md` draft; vision proposals | Claude subagent (Workflow) | Writes from the numbers | `CACHES.enhanced.md`, `vision-proposals.md` |
| 6 | Blind review against `results.json`, the nodes and the vision, with one planted defect whose location is kept out of every file the reviewer reads | codex `gpt-6.1-sol`, high, read-only | A different kind from the writer | `nodes/review.codex.stdout.md` |
| 7 | Repair confirmed findings; merge into `docs/memory-system/CACHES.md`, keeping R1–R8. **Waits for EJ:** session `ancient-games-05` is running the same challenge (`runs/20261012-caches-enhance/`) and plans to edit the doc too | main session, or the other session (EJ decides) | — | the doc |

Nodes 1a and 1b run in parallel. They are independent, write different files, and the harness reads `queries.json`
only at run time.

## Stop conditions

- **Verify:** the harness passes the audit, or the repair loop has used both attempts and the failure is reported.
- **Done:** every route in the routing table cites a measured row; numbers not measured here are labelled; the
  review's planted defect is caught; every finding is fixed or answered.

## Predictability, debuggability, quality control

- **Predictability:** fixed nodes and engines, bounded loops, the state file as the only shared progress.
- **Debuggability:** every node's raw output is under `nodes/`, every external command line is in a launch script,
  and every measurement is reproducible from `bench/`.
- **Quality control:** gold answers are written by a different kind and checked by `rg`; the harness is audited for
  leakage; the review is blind and planted. Every check names who wrote it.
