# Write the regression test for code_graph.py

## Task (one deliverable)
Write `code_graph/tests/test_code_graph.py` — a pytest suite covering the 8 cases below against the tool at
`code_graph/code_graph.py`. Do not change the tool. Stdlib + pytest only.

## The 8 cases (from `runs/20261005-code-graph-tool/nodes/n4-test-cases-1.result.md`; read it for the exact expected result of each)
- positive: direct_call, imported_call, class_method, nested_function
- negative: call_through_variable, getattr_call, decorator_wrapper, lambda_call

## How to build each test
Use a pytest `tmp_path`: write the tiny `.py` file(s) for the case, run
`python3 code_graph/code_graph.py <dir>`, parse the JSON, and assert the expected nodes/edges/unresolved markers.

## Standard (how it is judged)
- All 8 cases covered — 4 positive, 4 negative.
- `python3 -m pytest code_graph/tests/ -q` passes.
- Each test fails if the tool regresses (e.g. the `a -> b` call edge disappears).
- The test file lives at `code_graph/tests/test_code_graph.py` — in the project, NOT /tmp.

Print a summary of what you wrote and the pytest result to stdout.
