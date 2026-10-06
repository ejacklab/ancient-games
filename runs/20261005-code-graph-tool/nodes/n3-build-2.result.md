Found three spec deviations. Fixing them.
---
node: n3-build
attempt: 2
engine: opencode
model: minimax-coding-plan/MiniMax-M3.1-Flash-Preview
status: ok
started: 2026-10-06T09:02:38.320Z
ended: 2026-10-06T09:09:57.635Z
evidence: none
---
## What I built
`.claude/skills/workflow-design/scripts/code_graph.py` — the stdlib-only tool from the n2 spec (module + function nodes, `contains`/`import`/`call`/`fixture` edges, `unresolved_calls` with `dynamic`/`attribute`/`name`, transitive coverage over call+fixture, `errors`, `stats`, `--exclude`/`--test-glob`).

## How to run it
python3 code_graph.py <dir>

## What the smoke test showed
Fixture: `/tmp/opencode/fx` (`pkg/gate.py`, `pkg/sub/helper.py`, `tests/conftest.py`, `tests/test_gate.py`). Exit 0, 24 nodes, 41 edges, first lines:
```json
{
  "coverage": {"follows": ["call", "fixture"], "ratio": 0.5833, "rule": "transitive",
               "tested": 7, "total": 12,
               "untested": ["pkg/gate.py::dup", "pkg/gate.py::dup@44", "pkg/gate.py::outer",
                            "pkg/gate.py::outer::inner", "pkg/gate.py::unused_helper"]},
  "edges": [
    {"from": "pkg/gate.py", "kind": "contains", "line": 52, "to": "pkg/gate.py::outer"},
    {"from": "pkg/gate.py", "kind": "import",   "line": 2,  "to": "pkg/sub/helper.py"},
    {"from": "pkg/gate.py::Gate::decide", "kind": "call", "line": 27, "to": "pkg/gate.py::Base::shared"},
    {"from": "tests/test_gate.py::TestGate::test_gate", "kind": "call", "line": 19, "to": "pkg/gate.py::check"},
    {"from": "tests/test_gate.py::TestGate::test_gate", "kind": "fixture", "line": 5, "to": "tests/conftest.py::env"},
    {"from": "tests/test_gate.py::TestGate::test_gate", "kind": "fixture", "line": 10, "to": "tests/conftest.py::seeded"}
  ],
  "nodes": [{"decorators": [], "end_line": 37, "file": "pkg/gate.py", "id": "pkg/gate.py::check",
 "is_test_file": false, "kind": "function", "line": 35, "module": "pkg/gate.py",
             "name": "check", "qualname": "check", "role": "code", "tested": true,
             "tested_by": ["tests/test_gate.py::TestGate::test_gate"]}]
}
```
Also checked: JSON parses and has `nodes`+`edges` (the node's check), no dangling edge endpoint, two runs byte-identical, exit 2 with empty stdout for a missing directory, exit 1 with one `errors` entry while the scan carries on, `--exclude`, `--test-glob` (first use replaces the defaults; `conftest.py` stays a test file), `.venv`/`node_modules` skipped while other dot-dirs are scanned, `getattr(o, n)` counted in `external_calls` and only `getattr(o, n)()` listed as `dynamic` (the rule, not the spec's example), text cut at 80 chars, `ratio: null` on an empty tree, inheritance across modules, nested defs, `lambda`, class-body and module-level calls, default-value and decorator calls, `x = C()` then `x.m()`, `from ..base import Mid`, duplicate defs (`dup@44` + `dup`), recursive cycles, and pytest accepting a produced test id verbatim. On this repo: 110 files, 1211 nodes, 3371 edges, 0 errors, 0.6 s, no errors; baseline `env -u NO_COLOR python3 -m pytest -q` still 518 passed. Only `code_graph.py` was added.

Fixed from attempt 1: ids now use `::` between enclosing names (`m.py::outer::inner`, so test ids are pytest node ids) instead of dots; calls in default values and in method/class decorators were being dropped by the walker; `from x.y import f` no longer binds `f` to the sibling file `x/y/f.py` when `x/y/f.py` is a plain module (submodule precedence now applies to packages only, as Python does); fixture edges now start only from `test` and `fixture` roles, not `test_support`.

UNCLEAR: a package directory with no `__init__.py` (`from pkg.sub import helper`, `pkg/sub/helper.py` only) is counted in `stats.external_imports` and makes no edge / `dynamic` calls, because the spec's module resolution only accepts files (`a/b.py`, `a/b/__init__.py`) / best guess: keep it spec-literal; n6 can add namespace-package lookup if the coverage numbers call for it.
UNCLEAR: for a `fixture` edge the spec says `line` is "the line of the ... def in the `from` file", but `contains` edges use the child's `def` line, so the two readings disagree / best guess: fixture edges carry the fixture's own `def` line, consistent with `contains`.
UNCLEAR: `evidence` — the node contract lists `runs/20261005-code-graph-tool/nodes/n3.build.md`, but the brief forbids touching anything outside `code_graph.py`, so no evidence file was written and the smoke output is pasted here.
