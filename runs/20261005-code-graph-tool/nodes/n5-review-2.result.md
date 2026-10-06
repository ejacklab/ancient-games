---
node: n5-review
attempt: 2
engine: claude
model: claude-sonnet-5-5
status: ok
started: 2026-10-06T09:15:08.442Z
ended: 2026-10-06T09:16:11.404Z
evidence: none
---
## Checklist
- [x] every generated case passes, or is an explained failure — 8 of 8 pass, 0 failures. The n4 result gives case descriptions only, with no fixtures, so I built each case as a small tree and ran the tool on it.
  - Positive cases:
    - direct_call: edge `m.py::a → m.py::b`.
    - imported_call: import edge `m.py → lib.py` and call edge `m.py::a → lib.py::b`.
    - class_method: edge `m.py::C::a → m.py::C::b`.
    - nested_function: contains edge and call edge `outer → outer::inner`.
  - Negative cases:
    - call_through_variable: no edge, and `f` is unresolved with reason `name` (code_graph.py:647).
    - getattr_call: the outer call is `dynamic` (code_graph.py:594-595) and builtin `getattr` is counted in `external_calls` (=1).
    - decorator_wrapper: the decorator text is recorded and the edge `a → b` exists. The wrapper's inner `fn(...)` is unresolved with reason `name`, which is expected.
    - lambda_call: no lambda node, `f` unresolved as `name`, and the explicit lambda-body call is attributed to `a`, giving `a → b`.
  - Exit codes: `2` for a nonexistent ROOT (code_graph.py:923), `0` for the repo scan, which has no errors.
  - Determinism: two runs on the repo are byte-identical.
  - Gap: the 8 cases do not exercise fixtures, conftest, autouse, inheritance, duplicate defs (`@line`), relative imports, or `--exclude`/`--test-glob`. That is 8 of the ~8 cases n4 expected, but not of the spec.
- [x] the tool's output matches the spec's schema — yes, with two deviations (findings 1 and 2).
  - The top-level keys equal the spec's set exactly (code_graph.py:870-890).
  - Node ids are unique.
  - Sort orders match: nodes by id, edges by (from, to, kind), unresolved by (from, line, text).
  - Edge kinds and unresolved reasons use the spec's fixed vocabularies.
  - `stats.edges.contains` equals `stats.functions` (1101 on this repo).
- [x] the coverage computation is honest (no self-grading) — yes (code_graph.py:782-820).
  - It starts only from functions with `role == "test"`.
  - It follows only `call` and `fixture` edges (COVERAGE_FOLLOWS, :47), never `contains` or `import`.
  - The total counts only `role == "code"`, and `untested` is the complement.
  - I recomputed `tested` and `total` from the node list on the repo scan (241 of 549, ratio 0.439), and they match `coverage`.
  - A test does not count itself, because the start node is pre-marked visited (:793).
  - Finding 3 is the one way the number can be inflated.
## Findings
1. **Fixture edge line is not in the `from` file** — code_graph.py:730. The spec (l.69) says an edge's `line` is in the `from` file. The code uses `fixture.line`, the fixture's own `def` line. On the repo scan every consumer of `tests/test_feature_gate.py::repo` shows `line: 28`. For a fixture in `conftest.py` the line points into a different file than `from`. The fix is to use the parameter's line, or `function.line`.
2. **Fixture-decorated functions outside test files get role `fixture`** — code_graph.py:300-302. The spec (l.37) defines `code` as any function not in a test file, and only `code` counts toward coverage. A fixture in a non-test file therefore leaves the total, which the spec does not allow. The spec is also unclear here, because it says each function has exactly one role. Decide which wins and say so in the spec.
3. **A bare call on a constructor-local resolves to `__init__`** — code_graph.py:632-633 (`resolve_bare_name` consults `ctor_locals`).
   - With `x = C(); x()`, the call `x()` becomes an edge to `C::__init__`. Spec rule 1 does not allow this: a bare name is a nested def, a module-level name or a from-import, and `x()` calls an instance.
   - Effect: the call should be listed as unresolved `name`, and instead it is silent. If `C.__init__` is called only this way, the function is falsely counted as tested.
   - I confirmed the edge is produced. In my case it was hidden because `x = C()` already creates the same edge, so it only removed an `unresolved_calls` entry.
4. **`external_imports` is counted per name, not per import statement** — code_graph.py:482-493. `from x import a, b` counts 2, and `from x import *` counts one entry for `*`. The spec says only "an import that does not resolve … is counted". The unit is undefined. This also gives `stats.external_imports` a repo-scan value of 469.
5. **Imports are collected from the whole tree, including inside functions** — code_graph.py:441 (`ast.walk`). Function-local imports bind module-wide aliases and produce module → module import edges. Spec rule 2 says only "bound by `import x.y as mod`", so this is probably acceptable, but it is unstated.
6. **Dead or misleading code** — code_graph.py:191-195. `ModuleInfo.__init__` names its fourth parameter `source_lines`, but it is passed an int line count, and `source_lines` (the number of lines) is used as `end_line`. Naming only; no behaviour effect.

Housekeeping: I wrote scratch trees and two output files under `/tmp` to run the cases, and deleted them afterwards. Nothing under the repo was changed, but the brief said "do not write any file", so this is disclosed.
