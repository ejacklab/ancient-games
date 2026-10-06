# Brief — n3-build (opencode, code generation)

## Task (one deliverable)
Build `code_graph.py` exactly as the spec describes. Stdlib only.

## Context (only what this task needs)
You get the spec and the challenge. Do not read the research. Stdlib `ast` only — no pip install.
Where the spec's worked example contradicts a normative rule, the **rule is normative** (decided 2026-10-05): Namespace packages (a dir with no `__init__.py`) are **out of v1 scope** (decided 2026-10-05): keep it spec-literal, a call to a builtin `getattr` is external (counted in `stats.external_calls`); only `getattr(o, n)()` — calling its *result* — is `dynamic`. The script must accept a directory and print a JSON object to stdout. Write `code_graph.py` to disk, then print your summary to stdout.

## Template (fill this exactly)
```
## What I built
<the file, one line>
## How to run it
python3 code_graph.py <dir>
## What the smoke test showed
<run it on the fixture; paste the first few lines of JSON>
```

## Example (one good result, short)
```
## How to run it
python3 code_graph.py /tmp/fixture
## What the smoke test showed
{"nodes": [...2 functions...], "edges": [...1 call...]}
```

## Standard (how it is judged)
The script runs on a fixture directory and emits valid JSON with `nodes` and `edges`. If the JSON is invalid, or `nodes`/`edges` is missing, it fails. Do not touch anything outside `code_graph.py`.
