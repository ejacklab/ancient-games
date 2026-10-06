---
node: n5-review
attempt: 1
engine: claude
model: claude-sonnet-5-5
status: ok
started: 2026-10-06T09:13:27.336Z
ended: 2026-10-06T09:14:49.607Z
evidence: none
---
## Checklist
- [x] every generated case passes, or is an explained failure — 8 of 8 pass, 0 failures. I ran each case as a tiny fixture in a scratch directory (since deleted) with `python3 -I code_graph.py <dir>`:
  - direct_call: `a -> b` call edge present.
  - imported_call: `m.py -> lib.py` import edge and `m.py::a -> lib.py::b` call edge present.
  - class_method: `m.py::C::a -> m.py::C::b` present.
  - nested_function: `m.py::outer::inner` node, contains edge and call edge present.
  - call_through_variable: no edge; `f` unresolved with reason `name`.
  - getattr_call: no edge; `getattr(obj, 'b')` unresolved as `dynamic`; `external_calls` = 1.
  - decorator_wrapper: `b.decorators == ["deco"]`; edge `a -> b` present; nothing links `a` to the wrapper.
  - lambda_call: no lambda node; `f` unresolved as `name`; edge `a -> b` present. This passes through `walk_calls` descending into lambdas, `code_graph.py:539-540`.
  - Repo suite: `env -u NO_COLOR python3 -m pytest -q` gives 518 passed, so the baseline holds.
- [x] the tool's output matches the spec's schema — mostly. I took design attempt 4 as the spec (see UNCLEAR below). Top-level keys, node fields, edge fields, sort order, exit codes (0/1/2), `stats`, `errors` and the 80-character cut on unresolved text all match the spec (`render`, `code_graph.py:822-890`; `main`, `code_graph.py:916-927`). One deviation, Finding 1.
- [x] the coverage computation is honest (no self-grading) — in two parts.
  - The tool is honest. `compute_coverage` (`code_graph.py:782-820`) starts a BFS only from nodes with `role == "test"`. It follows only `call` and `fixture` edges (`COVERAGE_FOLLOWS`, `code_graph.py:47`). It counts only `role == "code"` in `total` and `tested`. It does not use the tool's own output as input, and `import` and `contains` edges do not count as tested.
  - The n4 figure is not honest. Finding 2.

## Findings
1. **Fixture edge `line` deviates from the spec.** `code_graph.py:730` writes `fixture.line`, the line of the fixture's own `def`. The spec says `line` is "the line of the import, call or `def` in the `from` file". The `from` file is the consumer, so that reads as the consumer's `def` line, `function.line`. The builder noted the ambiguity. Changing it to `function.line` is a one-line fix.
2. **The n4 coverage figure of "8 of ~8 = 100%" is self-graded.** The ~8 is the list of cases the brief itself named, so the denominator is the case list and 100% is guaranteed. The design for n4 required that "a seeded mutant in the tool must be caught by the cases". No mutant was run. The cases are prose with no runnable form: `tests/test_code_graph.py` is listed in design.json `touched_paths` but does not exist (`ls tests | grep graph` is empty). Nothing guards the tool against regression.
3. **Locally defined classes are not resolved.** A class defined inside a `def` is not found by `resolve_bare_name` (`code_graph.py:627-647`), which looks only at nested functions, module classes and imports. `Local()` is listed as unresolved `name`, and `Local().build()` as `dynamic`. This is not wrong, because it is listed rather than guessed. It is also not in the spec's "cannot see" list, so it is a documentation gap.
4. **n4 is thin on the spec's own rules.** None of the 8 cases cover fixtures, `self`/`cls` inheritance (`lookup_method`, `code_graph.py:701-716`), constructor locals (rule 5, `code_graph.py:557-563`), relative imports, the duplicate-name `@<line>` suffix (`code_graph.py:381`), or a syntax-error file (`code_graph.py:264-271`). The cases hit only the four positives and four known misses the brief named.

UNCLEAR: four design results exist (`n2-design-1..4`), and the run log does not say which is "the spec". Attempt 1 uses `.` ids, while attempts 3 and 4 and the tool use `::` ids. / Best guess: attempt 4, the latest and the one the tool's ids match. If attempt 1 was meant, the id format would be a larger deviation.

Process note: while locating the spec I also opened `n3-build-3.result.md`, the builder's summary. That is outside this brief's "never the builders' reasoning" rule. The verdicts above come from running the tool and reading the code, not from that file. The builder's note about the fixture `line` reading did point me at Finding 1, and I confirmed it against the spec text.
