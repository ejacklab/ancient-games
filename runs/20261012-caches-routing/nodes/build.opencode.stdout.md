I'll start by reading the project instructions and the code graph tool, since both govern how I work here.
Now let me check the environment, the run folder, and the venv.
Environment verified. Now I'll write the harness. Starting with `chunk.py`:
Chunking is correct. Now let me verify the sqlite-vec `vec0` schema before writing `build.py`:
Now `build.py`:
Now let's build all three stores:
Let me refactor the vec section so `hybrid` reuses structured chunks instead of re-parsing output text:
All routes work. Now `run_bench.py`:
Now let me verify the 5 sample questions' gold answers with commands before writing them:
Found it — `category_table` was not filtering by route, so every route reported the whole category. Fixing:
The report is readable. Let me check the S03 graph miss — it looks like a real finding, not a bug:
Now the README:
Now let me verify the four rules hold — especially that a missing store creates nothing:
Two cleanups: a no-op line in `excerpt`, and making `hybrid` fuse the two routes' *answers* symmetrically rather than a 200-row internal scan:
Let me stress-test the FTS query building with the adversarial terms the brief hints at:
One real crash: `vec` with an empty question. Fixing:
Let me do a final review pass over the two most important files:
Let me verify the README's three commands work verbatim from the repo root:
Built and ran end to end. Here is the report.

## What I built

Everything is under `runs/20261012-caches-routing/bench/`; nothing else in the repo changed (verified against `baseline-git-status.txt` — identical).

| file | lines | what |
|---|---|---|
| `chunk.py` | 228 | corpus = `git ls-files '*.py' '*.md'` minus the two run dirs (490 files: 123 `.py`, 367 `.md`); markdown by heading section, Python by top-level `def`/`class` + module-level code → 4017 chunks |
| `build.py` | 424 | `--store fts\|vec\|graph\|all`; each store built into a temp file then `os.replace`d; `meta` table with `git_head` + `newest_source_mtime` |
| `query.py` | 668 | `--route rg\|fts\|vec\|hybrid\|graph --query-json '<json>'` |
| `run_bench.py` | 511 | metrics, determinism check, `results.json` + `results.md` |
| `README.md`, `sample_queries.json` | — | three commands; 5 questions, every gold checked by a command I ran (`rg -n 'def count_sources'`, `rg -n 'def guard'`, `ls code_graph/tests/`, `rg -n 'Store — SQLite read index'`, `rg -n 'Tests:'`) |

Graph indexes as asked: functions, call edges, fixture edges, test→function reachability (direct table + transitive with `hops`), module→file. My BFS over call+fixture edges agrees with `code_graph.py`'s own coverage count (241 = 241), which the build asserts and reports.

**No leakage is enforced by construction:** `pick_route_input()` is the only code that touches a question; it copies four keys into a frozen `RouteInput`, and an `assert` fails the module if a fifth field appears. `run_bench.py` reads `gold` in a separate function after the route answered. Probed with a poisoned gold (`CANARY/...`) — no route's answer contains it.

## Build times and sizes

| store | seconds | bytes |
|---|---:|---:|
| fts | 0.16 | 9,449,472 |
| vec | 0.96 | 10,207,232 |
| graph | 0.91 | 4,898,816 |

## Determinism check

**True** — deleted `bench/.cache/`, rebuilt in 1.89 s, answered all 22 applicable route/question pairs again, compared `paths`: 0 mismatches.

## Sample results (`bench/results.md`, 5 questions)

hit@5 / mean chars to first gold:

| category | rg | fts | vec | hybrid | graph |
|---|---|---|---|---|---|
| A exact identifier | 0 / 5997 | 0 / 1229 | **1 / 481** | **1 / 1598** | **1 / 38** |
| B concept | 0 / 4400 | 0 / 2371 | 0 / 3223 | 0 / 2820 | n/a |
| C structure | 0 / 7098 | 0 / 1817 | 0 / 181 | 0 / 181 | 0 / 0 |
| D decision | **1 / 677** | **1 / 934** | 0 / 1777 | 0 / 316 | n/a |
| E how-to | 0 / 7747 | 0 / 2500 | 0 / 3407 | 0 / 3225 | n/a |

Over all questions: rg 8.0 ms, fts 3.3 ms, vec 1.7 ms, hybrid 4.9 ms, graph 0.4 ms; graph answers only the 2 questions carrying a symbol/file, so its row has n=2 — the report says so rather than comparing it head-on with n=5.

## What did not work, and what I chose

- **S03 is a real miss, and the graph is right.** "Which tests should I run after changing `code_graph/code_graph.py`" → the graph answers *none*. `code_graph/tests/test_code_graph.py` runs the tool as a **subprocess** and never imports it, so no call edge exists. A static graph cannot see process-exercised code.
- **Crashes I found and fixed while testing:** `vec` raised `TypeError` on an empty question (model2vec returns no embedding, not a zero one). FTS term quoting survives `D-0012`, `c++`, `a AND b`, `"`, `*` — no raises.
- **Choices the brief left open**, all in `results.json` under `config` so a review can flip one: `rg` uses `-F` (fixed strings) so it searches the same literal text FTS quotes; printed lines cut at 300 chars (1495 corpus lines are longer); `rg` output capped at 40 lines; scoring compares files, so a gold `path::name` is hit by a bare path; route seconds exclude the one-time model load (0.31 s, reported separately).
- **`newest_source_mtime` moved mid-run** (4016 → 4017 chunks): `docs/memory-system/CACHES.md` was edited at 13:59:43 by the parallel session `20261012-caches-enhance`. The stores picked it up — which is rule 1 working, but it means these numbers are a snapshot of a corpus in motion. Re-run before the tables are used.
- `../queries.json` did not exist (node 1a still running), so the run used `bench/sample_queries.json`; `--queries ../queries.json` will work as soon as it lands.

One caveat on evidence: these numbers come from a harness I wrote, and the determinism check is my own check of my own code — node 2's audit is what should make them evidence.
