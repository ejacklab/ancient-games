---
node: n3-build
attempt: 3
engine: opencode
model: minimax-coding-plan/MiniMax-M3.1-Flash-Preview
status: ok
started: 2026-10-06T09:10:09.863Z
ended: 2026-10-06T09:12:52.445Z
evidence: none
---
## What I built
`.claude/skills/workflow-design/scripts/code_graph.py` — the stdlib-`ast` tool from the n2 spec: module + function nodes (id = `<module id>::<class>::<def>`, so a test id is a pytest node id), `contains`/`import`/`call`/`fixture` edges, `unresolved_calls` in `dynamic`/`attribute`/`name`, transitive coverage over call+fixture only, plus `errors`, `stats`, `--exclude`, `--test-glob`. Attempt 3 re-verified it line by line against the spec and left the file byte-identical: no deviation was found, so nothing was changed. One place the spec admits two readings: a `fixture` edge's `line` — "the def in the `from` file" versus the child's-def reading that `contains` uses. It carries the **fixture's own** def line, consistent with `contains`; if n5 wants the other reading it is a one-line change in `resolve_fixtures`.
## How to run it
python3 code_graph.py <dir>
## What the smoke test showed
Fixture `/tmp/opencode/fx9` (`pkg/gate.py`, `pkg/sub/helper.py`, `tests/test_gate.py`): exit 0, 28 nodes, 47 edges, `errors: []`, first lines of stdout:
```json
{
  "coverage": {
    "follows": [
      "call",
      "fixture"
    ],
    "ratio": 0.4667,
    "rule": "transitive",
    "tested": 7,
    "total": 15,
    "untested": [
      "pkg/gate.py::Gate::run",
```
The rest of the run agrees with the spec's own worked example: `tests/test_gate.py::TestGate::test_gate -> pkg/gate.py::Gate::decide` (call, line 33) is the edge the example shows; `test_gate -> tests/test_gate.py::seeded` (fixture); `g = Gate(3); g.decide(...)` resolves through rule 5; `self.shared()` reaches `Base::shared` across files and `Base::shared -> pkg/sub/helper.py::twice` closes the transitive chain, which is why `twice` is tested and `Gate::run` is not. Deliberately unresolved rather than silently wrong: `handler = self.handle; handler(...)` -> `name`, `table[0](...)` and `getattr(self, name)()` -> `dynamic`, `other.call_shared()` -> `attribute`, while a bare `getattr(self, name)` (not called) is counted in `stats.external_calls` — the 2026-10-05 ruling, not the example.

Also checked this attempt, each in `/tmp/opencode`: two runs byte-identical; nodes/edges/unresolved in the spec's sort order and no dangling edge endpoint; relative imports (`from . import helper`, `from ..top import TOP`, `from ..sub.inner import deep`) each make the right edge; a class-body call comes from the module node; a class nested in a def hangs off the nearest enclosing def; a class not named `Test*` makes its method `test_support`, not `test`; a conftest `autouse` fixture reaches every test under it; `tmp_path` makes no edge; `exit 2` with empty stdout for a bad ROOT, `exit 1` with one `errors` entry while the scan carries on, `ratio: null` on an empty tree; `--exclude runs/*` and `--test-glob '*_test.py'` (first use replaces the defaults) behave as written. On this repo: 110 files, 1211 nodes, 3371 edges, 0 errors, 0.6 s, coverage 241/549. A class defined inside a def is not in the spec's rule-1 lookup list, so `Local()` there is listed as `name` and `Local().build()` as `dynamic` — a real gap, reported rather than hidden. Nothing outside `code_graph.py` was touched.
