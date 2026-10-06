Now let me rewrite it cleanly — the first pass had a few structural issues I want to fix (duplicate edge build, a broken ctor-locals walk, dead code).
Found three bugs (module lookup falling back too early, class bodies leaking into the module scope, autouse edges from non-tests). Fixing:
Indentation is correct. Now the class-body scope leak and the autouse edge:
The ctor-locals walker checked children of statements, so `x = C(...)` never fired. Fixing:
All specified rules fire correctly now. Testing the harder cases — inheritance, nested defs, module aliases, relative imports, duplicate defs, determinism:
`enclosing_def` was holding an AST node instead of a FunctionInfo. Fixing the link:
One more gap: implicit namespace packages (no `__init__.py`). Let me make `from pkg import sub` still resolve:
---
node: n3-build
attempt: 1
engine: opencode
model: minimax-coding-plan/MiniMax-M3.1-Flash-Preview
status: ok
started: 2026-10-06T08:50:21.706Z
ended: 2026-10-06T09:02:21.094Z
evidence: none
---
## What I built
`.claude/skills/workflow-design/scripts/code_graph.py` (the spec's location) — the full stdlib-ast tool: module and function nodes with every field, `contains`/`import`/`call`/`fixture` edges, `unresolved_calls` with reasons, transitive coverage over call+fixture, `errors`, `stats`, `--exclude`/`--test-glob`, argparse/json/ast only. `getattr`-style, `alias = f` and unknown-object calls are reported unresolved or external, never silently dropped.

## How to run it
python3 code_graph.py <dir>

## What the smoke test showed
On a fixture of `pkg/gate.py` (class `Gate` with `decide`/`reset`/`__init__`, functions `load`/`check`/`unused_helper`), `tests/conftest.py` (`env` and an `autouse` `seeded` fixture) and `tests/test_gate.py` — exit 0, 15 nodes, 22 edges, first lines of the JSON:
```json
{
  "coverage": {"follows": ["call", "fixture"], "ratio": 0.5, "rule": "transitive",
               "tested": 3, "total": 6,
               "untested": ["pkg/gate.py::Gate.reset", "pkg/gate.py::load", "pkg/gate.py::unused_helper"]},
  "edges": [
    {"from": "pkg/gate.py", "kind": "contains", "line": 9,  "to": "pkg/gate.py::Gate.__init__"},
    {"from": "pkg/gate.py", "kind": "contains", "line": 12, "to": "pkg/gate.py::Gate.decide"},
    {"from": "pkg/gate.py::Gate.decide", "kind": "call", "line": 15, "to": "pkg/gate.py::check"},
    {"from": "tests/test_gate.py::test_gate", "kind": "call", "line": 9, "to": "pkg/gate.py::Gate.__init__"},
    {"from": "tests/test_gate.py::test_gate", "kind": "call", "line": 10, "to": "pkg/gate.py::Gate.decide"},
    {"from": "tests/test_gate.py::test_check", "kind": "fixture", "line": 7, "to": "tests/conftest.py::env"}
  ],
  "nodes": [{"id": "pkg/gate.py", "kind": "module", "file": "pkg/gate.py", "line": 1, "end_line": 29, "is_test_file": false},
            {"id": "pkg/gate.py::Gate.decide", "kind": "function", "file": "pkg/gate.py", "line": 12, "end_line": 15, "is_test_file": false, "name": "decide", "qualname": "Gate.decide", "module": "pkg/gate.py", "role": "code", "decorators": [], "tested": true, "tested_by": ["tests/test_gate.py::test_gate"]}]
}
```
Also checked: JSON parses, both `nodes` and `edges` present, zero edges with a dangling endpoint, two runs byte-identical, exit 2 with nothing on stdout for a non-directory, exit 1 when a file fails to parse (error listed, scan continues), `--exclude`/`--test-glob` honoured, inheritance (`b.shared()` → `Base.shared`), nested defs, duplicate defs (`dup@18` / plain `dup` resolving to the last), relative imports, namespace packages, `x = C(...)` then `x.m()` (rule 5), lambdas attributed to the enclosing def, and dataclass/`property`/`match`/`async with` sources. On this repo: 110 files, 1211 nodes, 3395 edges, 0 errors, 0.6 s. Baseline `python3 -m pytest -q` still 518 passed. Only `code_graph.py` was added.

UNCLEAR: the spec's own worked example lists `getattr(self, name)` as a `dynamic` unresolved call, but its normative rule 6 says a call to a builtin `getattr` is external and must not be listed; I followed the rule (it is counted in `stats.external_calls`, and `getattr(o, n)()` — calling its *result* — is listed as `dynamic`) / Best guess: the example is illustrative, the rule is normative.
UNCLEAR: `evidence` — the node's contract lists `runs/20261005-code-graph-tool/nodes/n3.build.md`, but the brief forbids touching anything outside `code_graph.py`, so I wrote no evidence file and pasted the smoke output here instead.
