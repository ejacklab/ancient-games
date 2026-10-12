# State — 20261012-caches-routing

Rules: one writer at a time. Read this file before your step; update it after. It holds progress and results only —
never reasoning. Never delete a log line. The design is `design.md`.

## Steps

| # | Node | Engine | Status | Output |
|---|---|---|---|---|
| 1a | Question set (40, with checked gold answers) | codex `gpt-6.1-sol` high, read-only | done | `nodes/queries.codex.stdout.md` → `queries.json` |
| 1b | Benchmark harness | opencode `MiniMax-M3.1-Flash-Preview`, build | done | `bench/` |
| 2 | Verify gold answers and harness, at most 2 repairs | Claude subagents (Workflow `wf_48c8f56f-a17`) | stopped after repair 1 | `nodes/gold-verdicts.json`, `nodes/audit-0.json` |
| 3 | Run the benchmark | script | done | `bench/results.json` |
| 4 | Agent token trial, 6 × 2 | `claude -p`, `claude-sonnet-5-5` | **dropped** (EJ: design, not build) | `trial/run_trial.sh` unused |
| 5 | Routing table and enhanced draft; vision proposals | main session | done | `docs/memory-system/CACHES.md` § Measured here; `vision-proposals.md` |
| 6 | Blind review with a plant | codex `gpt-6.1-sol` high, read-only | done | `nodes/review.codex.stdout.md` |
| 7 | Merge into `docs/memory-system/CACHES.md` | **waits for EJ** (see log) | todo | — |

## Log (append only)

- 2026-10-12 readiness: codex canary `CANARY-OK`; model2vec 0.10.0 + sqlite-vec 0.1.9 installed in a scratch venv with
  `uv`, embedding verified (256 dims). Baseline: `baseline-git-status.txt`.
- 2026-10-12 **another session (`ancient-games-05`) is running the same challenge** in `runs/20261012-caches-enhance/`:
  three engines, one store each, answering from the existing research with no measurement, and the doc edit is its
  node 6. To avoid double work, this run does the measurement only and does not touch `CACHES.md`, the vision file or
  that run's folder. A message proposing that split was sent to `ancient-games-05`. Node 7 waits for EJ to say who
  merges.
- 2026-10-12 nodes 1a and 1b launched in parallel (`launch-1a-codex.sh`, `launch-1b-opencode.sh`). They are
  independent: the harness reads `queries.json` only at run time.
- 2026-10-12 reply from `ancient-games-05` (its code-graph engine, a subagent): the split is accepted; it will not
  touch this workspace or `CACHES.md`. It asked for four measurements its own run could not take, because commands
  needing approval were refused there: the cost of a filtered graph query, labelled with who wrote the wrapper; graph
  recall against gold answers, including wrong "no callers" answers; the full test-suite wall time; and a real token
  count for the 2.6 MB graph dump. This run takes only the ones already inside its own design: items 1 and 2 (node
  1b's graph route, scored on recall) and item 3 (the baseline for test selection). It does not take them on the
  peer's behalf. Item 4 has no local tokenizer; the node 4 trial gives real token counts. EJ is told of the request.
- 2026-10-12 node 1a done: exit 0, 40 questions (A 8, B 8, C 10, D 8, E 6), extracted to `queries.json`. **Bias
  found:** all ten C answers were checked by grepping for direct references ("with direct calls"; codex's own note:
  "runtime coverage was not measured"), so grep is scored against answers grep produced, and test-impact answers
  miss indirect tests. Added fix: per-test runtime coverage (`run-suite-and-coverage.sh`, coverage 7.13.5 +
  pytest-cov) as independent gold for the test-impact questions; also gives the full-suite wall time (3 runs).
  Limit: coverage sees in-process Python only, not tests that run code in a subprocess.
- 2026-10-12 node 1b done: exit 0, harness in `bench/` (chunk/build/query/run_bench, 4,017 chunks from 490 files).
  It reports rebuilds of fts 0.16 s, vec 0.96 s and graph 0.91 s, deterministic rebuild (0 mismatches) and a
  poisoned-gold leakage probe that came back clean. These are self-checks by the builder, not evidence until node 2
  audits them. It found the static graph cannot see subprocess-run tests (`code_graph/tests` runs the tool as a
  subprocess). `git status` matches the baseline. It also noticed `CACHES.md` being edited mid-run by the parallel
  session, so the numbers must be re-run on a stable snapshot.
- 2026-10-12 node 2 launched as Workflow `wf_48c8f56f-a17`: five gold checkers (one per category) and an
  independent harness audit (leakage probe, determinism, code review), with at most 2 repair-and-re-audit rounds.
- 2026-10-12 suite timing and coverage done: 529 tests pass in 31.0-33.3 s (3 runs); per-test coverage reduced to
  `cov/coverage-maps.json` (84 files, 918 functions); the 151 MB raw JSON deleted. Runtime coverage shows the direct-call
  gold is far from complete (C01: 1 file direct, 6 at runtime) and is blind to subprocess-run tests (C05-C07).
- 2026-10-12 node 2: gold 37/40 correct, 3 incomplete and completed (`queries.v2.json`, now `queries.json`; v1 kept).
  Audit 0: no leakage, deterministic, 5 high biases (rg ranking and output cap, the chars proxy, file-level scoring,
  class names in graph); repair 1 fixed all 5 (`bench/` only). **Workflow stopped during re-audit 1** after EJ: "I
  am not asking you to build a cache I am asking you to improve and enhance the design". The repair is not
  re-audited.
- 2026-10-12 node 3 run once on the repaired harness: `bench/results.md`, determinism 180/180. Runtime recall for
  C01-C04 in `nodes/runtime-recall.json`. Node 4 (the agent trial) dropped: it is building, not design.
- 2026-10-12 node 5: section "Measured here: development and testing" added to `docs/memory-system/CACHES.md` (main
  session, after the other session's run had finished its edit), plus a header line and one pointer sentence. No
  other text changed. Vision proposals in `vision-proposals.md`; the vision file was not edited. The other session
  is still editing `CACHES.md` R5 and `SOURCE_OF_TRUTH.md`.
- 2026-10-12 node 6 launched: codex blind review of the new section. The plant location is kept outside every file
  the reviewer may read, and will be logged after the verdict.
- 2026-10-12 node 6 done: codex **REPAIR**, 6 findings (2 high, 3 medium, 1 low). The plant was BM-7 "graph 0.92"
  (true 0.78) in `verify/section-review-copy.md`; codex caught it as its first high finding, with the right sources.
  The other 5 were checked by the main session against `bench/results.md` and `results.json`.
- 2026-10-12 repair: findings 2-6 fixed in the CACHES.md section, and the same wording in `vision-proposals.md`:
  - the proxy's limits are stated, and "a sixth" now refers to printed characters, not tokens;
  - the speed bound is now 15 ms (E04 grep 14.7 ms) and limited to this repo;
  - test selection is stated as able to miss tests (C05; C01/C02 recall);
  - BM-4 is shown as a tie;
  - BM-5 is shown as not settled.
  Not re-reviewed. Step 7 (merge) was done in place in node 5, so the doc is the merged copy.
