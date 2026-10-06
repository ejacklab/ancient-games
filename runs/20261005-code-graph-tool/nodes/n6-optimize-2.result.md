I'll start by finding the tool, spec, and review findings in this repo.
Now I have the tool, spec, and findings. Let me back up the original and start fixing.
Now the fixes. Finding 6 (naming) and finding 1 (fixture edge line):
Now finding 3 — the bare call on a constructor-local:
Now finding 4 — `external_imports` counted per statement, not per name:
Now finding 2 — the role rule for fixture-decorated functions outside test files:
Now the module docstring, recording the two rule decisions so findings 2 and 5 are no longer unstated:
Tool runs clean. Now let me verify each fix on scratch trees.
All four behavioural fixes verified old-vs-new. Now regression: determinism, exit codes, and n5's cases.
Now the final run, then a hand spot-check.
All six findings fixed, tool runs clean, coverage independently reproduced.

```
---
node: n6-optimize
attempt: 2
engine: opencode
model: minimax-coding-plan/MiniMax-M3.1-Flash-Preview
status: ok
started: 2026-10-06T09:58:35.703Z
ended: 2026-10-06T10:04:27.572Z
evidence: /tmp/opencode/n6-graph.json
---
## Findings fixed

All six findings from `runs/20261005-code-graph-tool/nodes/n5-review-2.result.md`, verified
old-vs-new on scratch trees. Only `code_graph.py` changed.

1. **Fixture edge line was not in the `from` file** (was code_graph.py:730, `fixture.line`).
   `parameters()` now returns `(name, line)` pairs from each `ast.arg`, `fixtures_for` returns
   `(fixture, line)`, and the edge takes the consumer's parameter line; an `autouse` fixture has no
   parameter, so the consumer's own `def` line stands in. All 115 fixture edges on this repo moved
   from the fixture's `def` line to the consumer's line — e.g. `test_clean_change_passes_and_flaky_is_not_judged
   -> tests/test_feature_gate.py::repo` went `28` (the fixture's line) to `60` (the parameter's line).
   On a scratch tree with the fixture in `conftest.py`, the `from` file is `test_x.py` and the edge now
   reports `20`, not `conftest.py`'s `5`.

2. **Fixture-decorated functions outside test files got role `fixture`** (was code_graph.py:300-302).
   Role now follows location first: anything outside a test file is `code`, so it stays in
   `coverage.total`. The decorator still registers it in `local_fixtures`/`autouse_fixtures`, so it is
   still injectable and a `fixture` edge still points at it — the far end of that edge is now decided
   by the decorator, not the role. **Decision the review asked for, and it contradicts the spec's edge
   table, which names role `fixture` as the edge target:** location wins for the role, the decorator
   wins for the edge. Recorded in the module docstring. On a scratch tree with a `@pytest.fixture` in
   `pkg/helpers.py`, the role went `fixture` -> `code` and `coverage.total` `1` -> `2`.

3. **A bare call on a constructor-local resolved to `__init__`** (was code_graph.py:632-633).
   The `ctor_locals` branch is gone from `resolve_bare_name`; rule 1 admits only a nested def, a
   module-level name or a from-import. `resolve_class`/`lookup_class_by_name` keep `ctor_locals`, which is
   rule 5's `x.name(...)` attribute path. On a scratch tree, `x = C(); x()` now yields
   `unresolved_calls: {"text": "x", "reason": "name"}` where the old tool produced nothing and routed the
   call to `C::__init__`. Note for the record: the review found the bad edge is usually masked because
   `x = C()` already makes the same edge key, and it is masked here too — an AST sweep of all 110 files
   found **no** bare call on a constructor-local in this repo, so this fix changes no number on this run.

4. **`external_imports` counted per name, not per statement** (was code_graph.py:482-493).
   `handle_import` and `resolve_missing_package` now set a flag and call `count_external_import()` once per
   statement, so `from x import a, b` and `from x import *` each count 1. Alias binding is unchanged, so
   rule 6's external-call detection still works per name. On a scratch tree, 4 external statements went
   `9` -> `5`; on this repo `469` -> `434`.

5. **Imports collected from the whole tree via `ast.walk`, including inside functions** — "probably
   acceptable, but it is unstated". Kept the behaviour (rule 2 binds by `import x.y as mod` and does not
   restrict the statement to module level) and made it stated, in the module docstring and in
   `collect_imports`' own docstring: one alias table per module, so a function-local import binds
   module-wide, and only the binding is recorded, never the executing module. I could not amend the
   spec file, since the brief limits me to `code_graph.py`.

6. **Dead or misleading code** (was code_graph.py:191-195) — `ModuleInfo`'s parameter and attribute
   `source_lines` renamed to `line_count`; it holds an int count and is read as `end_line`, and the old
   name promised lines of text.

Regressions re-checked, all clean: determinism (two runs byte-identical), exit `0` on this repo,
`1` with `errors` non-empty, `2` on a nonexistent ROOT, and n5's 8 cases — positive (direct, imported,
class-method, nested) and negative (`call_through_variable` -> `name`, `getattr`/`fs[0]()`/`g()()` ->
`dynamic` with `getattr` in `external_calls`, decorator wrapper's `fn` -> `name`, lambda body attributed
to the enclosing def with no lambda node). Nothing else in the repo imports `code_graph`.

## Run on this repo

`python3 .claude/skills/workflow-design/scripts/code_graph.py .` at the repo root, exit 0, `errors: []`:

```
{"nodes": 1212, "edges": 3374, "coverage": {"tested": 241, "total": 550}}
```

`ratio` 0.4382, 309 untested. Edges: call 1816, contains 1102, fixture 115, import 341.
Unresolved: attribute 2120, dynamic 745, name 61. External: calls 2941, imports 434.
110 files, 422 tests, 13 fixtures.

Two notes on the numbers. `total` is 550, not the 549 n5 saw, and `tested` is unchanged at 241: my own
edits added `parameters` and `count_external_import` to `code_graph.py`, which is under ROOT, and both
are role `code`. Diffing the node and edge sets against n5's run, **every** difference is inside
`code_graph.py` — no other file's graph, and no coverage verdict anywhere, changed.

## Spot-check

`owner_row_ids` in `ancient_games/hybrid/tools/gate.py`.

By hand: the file's line 15 is `def owner_row_ids(registry=reg.REGISTRY) -> list[str]:` and the body ends
at line 16 — the node reports `line: 15, end_line: 16`. Its only call site in the whole tree is
`gate.py:24` inside `run` (line 26 calls it again, and the spec keeps the first occurrence, so the single
edge is at `24`) — the graph lists exactly one `call` edge in, from `gate.py::run`.

Its two `tested_by` entries are `tests/test_ablation_fixes.py::test_h2_uc1_failing_arg_shapes_are_refused_by_field_and_the_valid_shape_runs`
and `::test_h7_failing_gate_leaves_ctx_unchanged`. By hand: `test_ablation_fixes.py:81` and `:205` are the
only two `gate_tool.run(...)` calls in the test tree, and `gate.py::run` reports the same two. The path is
transitive (test -> `gate.run` -> `owner_row_ids`), which is why the two functions share a `tested_by`.

The summary itself: I recomputed `total`, `tested` and `ratio` from the emitted node and edge lists with an
independent BFS over `call` and `fixture` edges only, starting at `role == "test"` — 550 / 241 / 0.4382,
identical to what the tool reports, and `untested` is 309. I also re-derived reachability for all 2721
`tested_by` claims in the graph: 0 name a test that cannot reach the node it is attached to.
```
