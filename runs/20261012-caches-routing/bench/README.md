# bench — a benchmark harness for the three caches, against grep

Three stores (SQLite FTS5, sqlite-vec, code graph) built from this repo, four
routes that answer a question from them, `grep` as the baseline, and a runner
that scores every route against a gold answer and writes the tables.

Everything here is a prototype for the measurement in `runs/20261012-caches-routing`.
Nothing outside `bench/` is written or read except the repo itself, read-only.

## Run it — three commands

```
VP=/tmp/claude-1000/-home-smoke01-dev-ancient-games/343bf18f-e2d9-4dcf-8db5-0ed3524f59db/scratchpad/caches-venv/bin/python

$VP bench/build.py --store all                                    # 1. build the three stores
$VP bench/run_bench.py --queries ../queries.json                   # 2. score every route, write results
$VP bench/query.py --route hybrid --query-json '{"question":"where is the review stage implemented?","terms":["review","stage"],"symbol":null,"file":null}'   # 3. ask one question
```

Run from the repo root; `bench/` and `../queries.json` are found relative to the
scripts, so any working directory works. Step 2 builds the stores itself and
then deletes and rebuilds them for the determinism check, so step 1 is only
needed to use step 3 on its own.

Without the real question set, use the 5-question stand-in that ships here:
`$VP bench/run_bench.py --queries bench/sample_queries.json`.

Useful flags: `--no-build` (reuse the stores already in `bench/.cache/`),
`--skip-determinism`, `--keep-output` (keep every full output in `results.json`).

## The files

| file | what it is |
|---|---|
| `chunk.py` | the corpus and its chunks: markdown by heading section, Python by top-level `def`/`class` plus module-level code |
| `build.py` | `--store fts\|vec\|graph\|all`; full rebuild, temp file then `os.replace` |
| `query.py` | `--route rg\|fts\|vec\|hybrid\|graph --query-json '<json>'`; one answer per call |
| `run_bench.py` | every route over a question set, the metrics, the determinism check, `results.json` and `results.md` |
| `sample_queries.json` | 5 questions in the shape of `../queries.json`, each gold checked by a command recorded in `gold_check` |
| `.cache/` | `fts.sqlite`, `vec.sqlite`, `graph.sqlite`. Delete it whenever; nothing is lost |

## The rules every store keeps

* **Derived from the files, never the source.** A store holds nothing a reader
  needs in order to be right. Delete `.cache/` and rebuild and the answers are
  the same — `run_bench.py` checks that on every run and prints the result.
* **Full rebuild only.** Each store is built into a temp file in the same
  directory and `os.replace`d over the old one, so a reader sees the whole old
  store or the whole new one. There is no update mode and no code that could
  become one.
* **It records what it was built from.** Every store carries a `meta` table with
  `git_head` and `newest_source_mtime`.
* **A missing store file is an answer.** Routes open `file:...?mode=ro` with
  `uri=True`, so a missing file raises instead of being created, and the route
  returns `paths: []` with an `error` saying which file is missing. No route ever
  creates a database.

## No leakage

A route may read only `question`, `terms`, `symbol` and `file`. It may never read
`gold`, `gold_check` or `literal_overlap`.

This is enforced by construction, not by convention: `query.pick_route_input()`
is the only code that touches a question, it copies those four keys into a frozen
`RouteInput`, every route takes a `RouteInput`, and an `assert` at import fails
the module if a fifth field is added. `run_bench.py` is the only reader of
`gold`, and it scores in a separate function called after the route has answered.
`results.json` records `route_input_fields` so the rule can be checked without
reading the code.

## What each route does, and what it prints

| route | ranks by | `paths` | `output` |
|---|---|---|---|
| `rg` | distinct terms matched, then match count per file | up to 10 files | `# <file> (N matching lines)` for every ranked file, then `path:line:text`; match lines capped at 40 in total |
| `fts` | `bm25()` | up to 10 chunk `path::name` | `path::name:start-end:` plus `snippet()` |
| `vec` | cosine distance to the embedded question | up to 10 chunk `path::name` | `path::name:line:` plus the first 300 characters |
| `hybrid` | reciprocal rank fusion, `sum(1/(60+rank))` | up to 10, from `fts` and `vec` | the block of whichever route ranked it |
| `graph` | directness (hops), then path | up to 10 `path::name` | one hit per line |

`graph` answers only questions carrying a `symbol` or a `file`, and only three
things: callers of a symbol, tests reaching a symbol, and (for a file) tests
reaching any function in it. Which one is asked for is decided from the words of
the question; a test question wins over a call question.

## Decisions a reader should be able to challenge

These are choices the brief did not fix. Each is in `results.json` under
`config`, so a review can flip one and rerun.

* **`rg` treats terms as fixed strings** (`-F`), case-insensitive. The FTS route
  quotes each term for the same reason, so the two search the same literal text.
  Regex terms would make the baseline something no agent actually types.
* **A printed line is cut at 300 characters.** 1495 corpus lines are longer than
  that, and one long line would otherwise decide the token metric by itself.
* **`rg` ranks files by distinct terms matched, then by matching lines**, so a
  file holding every term outranks one repeating a single common term, as an
  agent grepping for two terms together would find it.
* **`rg` match lines are capped at 40 in total**, but the header of every one of
  the 10 ranked files is always printed, so every path in `paths` is in `output`.
  The other routes already print at most 10 blocks.
* **A chunk reports `path::name` for a named top-level Python symbol, and plain
  `path` for a markdown section or module-level code**, so a document is one
  answer however many sections it has.
* **Scoring reports files and symbols.** File-level `hit@k`: a gold `path::name`
  is hit by a route that returned the path alone, as the brief requires, and
  `recall@10` is the share of distinct gold *files* found. Symbol-level
  `sym_hit@k`: a gold `path::name` needs the symbol (an entry naming it, its
  top-level def/class, or a method of it; a module-code chunk for a module-level
  name; for `rg`, a printed match line inside the symbol's lines, read with
  `ast`). The best route per category is chosen on symbol hit@5.
* **`chars_to_first_gold` counts the first line where the route names a gold
  file as its answer** (`# <path> (` or a line starting `<path>:`, exact path),
  not a line that only mentions it. A miss is left out of the mean, never 0;
  the mean is shown with the number of answers it is over. Print formats differ
  per route (fts 24-token snippets, rg and vec 300-character lines), recorded
  as `config.printed_per_answer`.
* **Route seconds exclude the one-time model load**, reported separately as
  `model_load_seconds`. In a session the model is loaded once and the n-th
  question is what costs.

## The metrics

`hit@1/5/10` against `gold`; `recall@10` for category C, where every answer
matters; `chars_to_first_gold` as the token proxy; `output_chars`; `seconds`.
`results.md` has one table per category with routes as columns, then a row per
route over everything, then a row per question.

## A limit of the graph store, found by running it

Question `S03` asks which tests to run after changing `code_graph/code_graph.py`.
The graph route answers "none", and it is right: `code_graph/tests/test_code_graph.py`
runs the tool as a **subprocess** and never imports it, so no call edge and no
fixture edge exists. A static graph cannot see what is exercised only by running
a process.

The graph has no class nodes, only methods (`Class.method`), so a class name
resolves to its methods. That is a property of the store, not a defect in the harness.