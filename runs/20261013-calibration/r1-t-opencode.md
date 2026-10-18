# Brief — r1-tests (opencode), attempt 1

## Task (two deliverables)

A blind review found 20 defects in the requirements evaluator. The fixes are specified, rule by rule, in
`docs/evaluator/DATA.md`, section **"Repair R1"** and the table **"The workflow after R1"**. Write the tests for
those rules **before** the code is changed. Another engine (Codex) writes the code next, and may not edit your
tests.

1. **New file `tests/test_evaluator_r1.py`.** Tests for the R1 rules in `tools/evaluator/verdict.py`,
   `tools/evaluator/workspace.py` and `tools/evaluator/model_io.py`:
   - F1, F4 (the verdict part), F5 (the verdict part), F11, F13, F14 (the verdict part), F15, F16, F19 (the
     verdict part), F20;
   - F8, F10, F12 (the workspace part);
   - F2, F6 (the `confirm-check` counts), F7 (`--attempt 2`), F9 (`mutant-view`), F11, F17 (`check-output`), F18
     (`stamp`).

   Each test's docstring **starts with the finding id**, e.g. `"""R1-F5 — a mutant that turns every probe red is not
   proof."""`.
2. **Update your own harness `tests/workflows/evaluate_harness.mjs`** to the new label table. Replace the old
   14-label happy path. Add cases for:
   - F6: the repair round runs only when `unfaithful > 0`, and only once;
   - F7: the judge rerun runs only on `plant_found: false`, and is skipped on `no other plant`;
   - F12: a bad `runId`, such as `../x` or `a/b`, blocks before any agent;
   - F17: `done: false` blocks, and a `check-output` non-zero exit blocks;
   - F19: a `MEETS:` line with the wrong `run=` blocks;
   - F2: the `e9-judge-1` prompt contains `JUDGE_DIR=` and **not** `RUN=`;
   - F9: the `e5-mutants` command has `-C runs/<runId>/mutant-view`;
   - F8: each `exclude` glob becomes `--exclude <glob>`;
   - F18: `e0-start` is first and `e11-end` is last, with the agent count.

   Keep the sabotage case.

## Context

- Read `docs/evaluator/DATA.md`: the whole file, then **Repair R1** and **The workflow after R1** with care. Then
  read `docs/evaluator/REQUIREMENTS.md`.
- House style: `tests/test_evaluator_verdict.py` and `tests/test_evaluator_model_io.py`. You may import their helpers
  (`tests/` is on `sys.path`), as `tests/test_evaluator_k1_regressions.py` does.
- The existing tests and the frozen fixtures **must not change**, except `tests/workflows/evaluate_harness.mjs`,
  which is yours and must follow the new table.

## Standard (the COO runs it)

1. `env -u NO_COLOR python3 -m pytest --collect-only -q tests/test_evaluator_r1.py` collects.
2. Every finding listed in deliverable 1 is cited in at least one docstring.
3. Against today's code, before the fix, **most of the new tests fail**. A new test that already passes today must
   be one that guards something that already holds; say which ones in your result.
4. `node tests/workflows/evaluate_harness.mjs` runs to the end. It may fail cases, since the workflow is not updated
   yet, but it must not crash.

## Limits

- **May change:** `tests/test_evaluator_r1.py` and `tests/workflows/evaluate_harness.mjs`.
- **Must not:** change code, docs or other tests, or commit.
- **Timer:** outer 1500 s.

## Write the result to

Print it as your final answer:
1. the header (`node: r1-tests-opencode`);
2. one line per finding with its test names;
3. which new tests pass today, and why;
4. the collect summary and the harness summary.
