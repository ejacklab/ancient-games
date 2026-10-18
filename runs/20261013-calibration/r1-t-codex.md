# Brief — r1-tests (codex), attempt 1

## Task (one deliverable)

A blind review found defects in the requirements evaluator. The fixes are specified in `docs/evaluator/DATA.md`,
section **"Repair R1"**. Write **new** tests, in `tests/test_evaluator_r1_matrix_spec.py`, for the rules that change
`tools/evaluator/probe_matrix.py` and `tools/evaluator/spec_parse.py`, **before** the code changes. Another engine
(opencode) writes the code and may not edit your tests.

Cover:
- **F3:** the citations `EV-P1-F2`, `EV-C3.3-F1`, `B1-F1`, `W1.3-F2` and `V5-F1` are all read, and `CITATION` is
  built from `spec_parse.ID`.
- **F4:** the baseline is taken before the product run. A probe that writes into the product copy gives
  `product_changed: true`, and `restored` is measured against the first baseline.
- **F5:** the optional `runs` key records `status`, and the `errors` list (probes that ended in a JUnit error)
  separately from failures. A timeout gives `status: "timeout"`. Every existing key keeps its shape.
- **F1:** `spec_parse.py` exits 2 on a file with no requirement ids.
- **F14:** `unparsed_ids` lists id-shaped bold bullets that are not in the manifest, such as `- **B1.1:**`.

Each docstring **starts with the finding id**, for example `"""R1-F3 — …"""`.

## Context

- `docs/evaluator/DATA.md`: the whole file, then "Repair R1".
- House style: `tests/test_evaluator_probe_matrix.py` and `tests/test_evaluator_spec_parse.py`. You may import their
  helpers.
- Existing tests and fixtures **must not change**.

## Standard

1. `env -u NO_COLOR python3 -m pytest --collect-only -q tests/test_evaluator_r1_matrix_spec.py` collects.
2. Against today's code, most of the new tests fail. List those that pass today, and why.

## Limits

- **May change:** that one new file.
- **Must not:** change code, docs or other tests, or commit.
- **Timer:** outer 1200 s.

## Write the result to

Print it as your final answer:
1. the header (`node: r1-tests-codex`);
2. one line per finding with its test names;
3. which tests pass today;
4. the collect summary.
