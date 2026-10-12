# Brief 1b — build a cache benchmark harness (run 20261012-caches-routing)

Build a small benchmark harness that measures three cache stores against grep on this repo. Write files **only**
under `/home/smoke01/dev/ancient-games/runs/20261012-caches-routing/bench/`. Do not change any other file in the
repo.

## Environment
- Repo: `/home/smoke01/dev/ancient-games`. The corpus is `git ls-files '*.py' '*.md'`, excluding anything under
  `runs/20261012-caches-routing/` and `runs/20261012-memory-caches/`.
- Python with the packages: `/tmp/claude-1000/-home-smoke01-dev-ancient-games/343bf18f-e2d9-4dcf-8db5-0ed3524f59db/scratchpad/caches-venv/bin/python`
  (has `model2vec` 0.10.0, `sqlite_vec` 0.1.9, `numpy`; SQLite 3.45.1 with FTS5). Use only the stdlib and these.
- Embedding model: `model2vec.StaticModel.from_pretrained("minishlab/potion-base-8M")` (already cached locally).
- Code graph: `python3 /home/smoke01/dev/ancient-games/code_graph/code_graph.py <root>` prints JSON to stdout. Read
  its docstring and output for the node and edge shape: modules and functions; `contains`, `import`, `call` and
  `fixture` edges; test reachability.
- `rg` is installed.

## The rules every store must keep (the project's vision)
- It is derived from the files and never the source. Deleting `bench/.cache/` and rebuilding gives the same answers.
- Full rebuild only. Build into a temporary file, then `os.replace` it over the old one. There is no incremental or
  update mode.
- It records what it was built from (git HEAD and the newest source mtime).
- If a store file is missing, the route says so and returns nothing. It must not create an empty database: open it
  with `file:...?mode=ro`, `uri=True`.

## Files to write
1. `bench/chunk.py`: splits the corpus into chunks. Markdown by heading section; Python by top-level `def` or
   `class`, plus module-level code as one chunk. Each chunk has `path`, `start_line`, `end_line` and `text`.
2. `bench/build.py --store fts|vec|graph|all`: full rebuild into `bench/.cache/{fts,vec,graph}.sqlite`. Prints JSON
   with the seconds taken and the bytes on disk for each store.
   - `fts`: an FTS5 table over the chunks, with `path` and the line numbers as UNINDEXED columns, default tokenizer.
   - `vec`: a sqlite-vec `vec0` table of the chunk embeddings, plus a chunk table.
   - `graph`: the `code_graph.py` output loaded into tables, with these indexes:
     - functions;
     - call edges (caller → callee);
     - fixture edges;
     - test → function reachability (direct and transitive over call and fixture edges);
     - module → file.
3. `bench/query.py --route ROUTE --query-json '<json>'`: answers one question. It prints JSON with:
   - `paths`: ranked, unique, at most 10, as repo-relative paths or `path::name`;
   - `output`: the text an agent would read, i.e. what the route prints, such as matching lines or snippets;
   - `seconds`.

   The routes:
   - `rg`: the baseline. `rg -n -i` over the corpus for the `terms`. Rank files by match count. `output` is the
     matching lines, as an agent would see them.
   - `fts`: an FTS5 MATCH on the `terms` joined with OR, quoting each term (ids like `D-0012` break unquoted), ranked
     by bm25, with `snippet()` as the output.
   - `vec`: embed the `question` and take the top 10 chunks by cosine distance. The output is the first 300
     characters of each chunk.
   - `hybrid`: reciprocal rank fusion of `fts` and `vec`, `score = sum(1/(60+rank))`.
   - `graph`: only for questions with a `symbol` or `file`. Use what the question asks:
     - callers of the symbol;
     - tests reaching the symbol;
     - for a file, tests reaching any function in that file.

     The output is the list of hits, one per line.
4. `bench/run_bench.py --queries ../queries.json`: runs every applicable route for each question. For each, it
   records:
   - `hit@1`, `hit@5` and `hit@10` against `gold` (a gold `path::name` also counts as a hit when the route returns its
     path);
   - `chars_to_first_gold`: the characters of `output` up to and including the first line that names a gold path,
     or the whole output if there is no gold hit;
   - `output_chars`;
   - `seconds`;
   - for C questions, `recall@10` as well.

   It also records the build seconds and size of each store, and runs a **determinism check**: delete `bench/.cache/`,
   rebuild, re-run all queries, and compare the `paths`. It writes `bench/results.json` and a readable
   `bench/results.md`: one table per category, with routes as columns and mean hit@5, mean chars to the first gold
   hit, and mean seconds.
5. `bench/README.md`: how to run it, in three commands.

## The one hard rule: no leakage
A route may read only `question`, `terms`, `symbol` and `file`. It must never read `gold`, `gold_check` or
`literal_overlap`. Only `run_bench.py` reads `gold`, after a route has answered.

## Test it
`../queries.json` may not exist yet, because another agent is writing it now. Make your own 5-question
`bench/sample_queries.json` in the same shape (fields: `id`, `category`, `question`, `terms`, `symbol`, `file`,
`gold`, `gold_check`, `literal_overlap`), and run the whole pipeline on it end to end.

## When you are done
Print what you built, the sample results table, the build times and sizes, the determinism-check result, and anything
that did not work.
