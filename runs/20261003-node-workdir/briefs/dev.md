# Brief — dev, build a feature: per-node working folder in dispatch.py

## Task (one deliverable)
Add an optional per-node `workdir` field to `.claude/skills/workflow-design/scripts/dispatch.py` that satisfies
R1–R7 below, with unit tests for it in `tests/test_dispatch.py`. Change nothing else.

## Context
- Read `runs/20261003-node-workdir/explore.md` first: it names every line involved (X1–X7) and what must not change.
- Read `.claude/skills/workflow-design/scripts/dispatch.py` and `tests/test_dispatch.py` (existing fake-engine style:
  `node()`, `setup()`, `run()`, `fake_bin()`).
- Do not read `tests/test_dispatch_workdir.py` if it appears: it is the independent verifier's, written blind.

## Acceptance criteria (each with an example)
- R1 A node with `"workdir"` runs its engine with that folder as its working folder. Example: a script node whose
  command prints `os.getcwd()`, with `"workdir": "w/q"`, records a result containing `<root>/w/q`.
- R2 A relative `workdir` resolves against `--root`, and a missing folder is created. Example: `w/new` absent before
  the run exists after it.
- R3 A node without `workdir` runs in the repo root, as before. Example: the printed folder equals `<root>`.
- R4 The Codex adapter's `-C` names the node's working folder. Example: `--dry-run` on a codex node with
  `"workdir": "w"` prints `-C <root>/w`.
- R5 The brief, the result file and check commands still resolve against the repo root. Example: a node with
  `"workdir": "w"`, brief `brief.md` at the root and a check `python3 check.py {result}` with `check.py` at the root
  runs and passes; its result file is under `runs/<run_id>/nodes/`.
- R6 A fallback without its own `workdir` keeps the node's; a fallback with one uses it. Example: node `"a"`,
  fallback `"b"` → the fallback call runs in `<root>/b`.
- R7 `dispatch.py check` refuses a `workdir` that exists as a file. Example: `"workdir": "x.txt"` with `x.txt` a file →
  a refusal naming the node and saying it is not a folder.

## Template
Your final answer is the result file (the dispatcher's pass-back header, below), with this body:
```
<one sentence: what changed>
Files changed: <list>
Tests: <the exact command you ran and its last line>
Criteria: R1 <test name> · R2 <test name> · … · R7 <test name>
```

## Example
```
Added an optional per-node workdir; engines run there, briefs and checks stay on the root.
Files changed: .claude/skills/workflow-design/scripts/dispatch.py, tests/test_dispatch.py
Tests: env -u NO_COLOR python3 -m pytest -q tests/test_dispatch.py → 24 passed in 3.1s
Criteria: R1 test_workdir_is_the_engine_cwd · R2 test_workdir_created · …
```

## Standard
- `env -u NO_COLOR python3 -m pytest -q tests/test_dispatch.py` passes, and so does the full suite
  `env -u NO_COLOR python3 -m pytest -q`.
- Each of R1–R7 has at least one test of yours named in the body.
- Only `dispatch.py` and `tests/test_dispatch.py` change; a script gate checks this with `git diff`.
- A node without `workdir` behaves exactly as before (all existing tests unchanged and passing).

## Limits
May change: the two files above. Must not change: anything else, including `ancient_games/`, other scripts, docs,
`tests/test_dispatch_workdir.py`. No network, no real engines in tests. If something is unclear, do not guess:
answer with `UNCLEAR: <question> / <best guess>` in the body.
