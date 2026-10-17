# Brief — r1-code (opencode), attempt {ATTEMPT}

## Task

Implement repair R1 in the modules you built: `tools/evaluator/probe_matrix.py` and `tools/evaluator/spec_parse.py`.
The rules are in `docs/evaluator/DATA.md`, section **"Repair R1"**:
- F1 (the `spec_parse` part);
- F3;
- F4 (the `probe_matrix` part);
- F5 (the `probe_matrix` part);
- F14.

Make the frozen tests pass.

## Context

- **Your frozen tests:** `tests/test_evaluator_r1_matrix_spec.py` (new, by Codex), **plus every existing evaluator
  test**.
- For F3, import the id grammar from `spec_parse` (`ID`). Do not copy it.
- `runs` and `product_changed` are **new optional keys**. Every existing key in `matrix.json` keeps its exact shape,
  because frozen tests compare it.

## Standard (the COO runs it)

- `env -u NO_COLOR python3 -m pytest -q`: 0 failed, **except** the tests in `tests/test_evaluator_r1.py`, which
  cover the other engine's modules and may still fail.
- `feature_gate.py check`.

If a frozen test contradicts DATA.md, add the line `CONTRADICTS …` and do not work around it.

## Limits

- **May change:** those two files.
- **Must not change:** anything else. Do not commit.
- **Timer:** outer 1500 s.
- **Attempts left:** {LEFT}.

{FEEDBACK}

## Write the result to

Print it as your final answer:
1. the header (`node: r1-code-opencode`);
2. one line per finding with its file:line;
3. "Choices not in the spec";
4. CONTRADICTS, if any;
5. the pytest summary.
