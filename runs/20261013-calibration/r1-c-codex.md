# Brief — r1-code (codex), attempt {ATTEMPT}

## Task

Implement repair R1 in the modules you built:
- `tools/evaluator/verdict.py`;
- `tools/evaluator/workspace.py`;
- `tools/evaluator/model_io.py`;
- `.claude/workflows/evaluate-requirements.js`.

The rules are in `docs/evaluator/DATA.md`, section **"Repair R1"** and the table **"The workflow after R1"**. Make
the frozen tests pass.

## Context

- `docs/evaluator/DATA.md`: the whole file, then Repair R1 and the new label table.
- **Your frozen tests:** `tests/test_evaluator_r1.py` (new, by opencode) and `tests/workflows/evaluate_harness.mjs`
  (updated by opencode), **plus every existing evaluator test**. All of them must pass.
- **New `model_io.py` subcommands:**
  - `check-output --step classify|probes|mutants`;
  - `stamp --event start|end [--agents N]`;
  - `mutant-view [--collect]`;
  - `judge-input --attempt 1|2`.
- `confirm-check` prints `<n> checked, <m> voided, <u> unfaithful`. `<u>` counts answers that the **model** marked
  `faithful: false`, with no script note.
- The workflow is plain JavaScript with no filesystem access. Every command runs through the runner; see
  `.claude/workflows/intake.js` for the shape. Never compute a verdict in the workflow.

## Rules

- Standard library only.
- Exit codes as DATA.md says.
- No traceback on any input.

## Standard (the COO runs it)

- `env -u NO_COLOR python3 -m pytest -q`: 0 failed.
- `node tests/workflows/evaluate_harness.mjs`: every case PASS.
- `feature_gate.py check` with tests protected.

If a frozen test contradicts DATA.md, do not work around it. Finish the rest and add the line
`CONTRADICTS <test> <rule>: …`.

## Limits

- **May change:** those four files.
- **Must not change:** tests, harness, docs, `probe_matrix.py`, `spec_parse.py`. Do not commit.
- **Timer:** outer 1800 s.
- **Attempts left:** {LEFT}.

{FEEDBACK}

## Write the result to

Print it as your final answer:
1. the header (`node: r1-code-codex`);
2. one line per finding with its file:line;
3. "Choices not in the spec";
4. CONTRADICTS, if any;
5. the command summaries.
