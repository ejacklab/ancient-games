# Brief — r1 (opencode): repair your tests, then fix your two modules

## Part 1: repair your own tests, following the COO's rulings

Codex implemented repair R1 (`docs/evaluator/DATA.md`, "Repair R1" and "The workflow after R1") in `verdict.py`,
`workspace.py`, `model_io.py` and the workflow. Some of **your** tests contradict the R1 contract. The COO ruled on
each one below. Change **only** these assertions, and keep every test's intent.

1. **`tests/test_evaluator_r1.py::test_meets_is_false_when_there_is_no_in_scope_requirement_at_all`.** The
   `out_of_scope == 2` assertion sits after the loop, so it checks the empty spec, which has 0. Move it into the loop,
   for the all-open case only.
2. **`tests/workflows/evaluate_harness.mjs`:**
   - `repairRound` and `judgeRerun`: give the stub answers for every call the new table makes. That is
     `e8-repair … e8-check-2`, and `e9-input-2 … e9-merge-2`. `e9-input-2` is called even when it prints
     `no other plant`, and is the only one of the four that runs then.
   - `excludeGlobs`: accept a shell-quoted glob. `--exclude '*.md'` is correct; an unquoted glob would be expanded by
     the shell.
3. **Old tests that pin the pre-R1 contract. R1 changed it on purpose; update them to the new contract:**
   - `tests/test_evaluator_model_io.py`, the `confirm_check` tests: stdout is now
     `<n> checked, <m> voided, <u> unfaithful`.
   - `tests/test_evaluator_model_io.py`, the `judge_input` and `judged_merge` tests:
     - `judge-input.json` no longer holds `plant_case`; the plant is in `{RUN}/.coordinator/plant.json`;
     - call 1's folder is `/tmp/evaluator-judge-<run folder name>/`, holding `judge-input.json`, `product/` and
       `judge-1.json`;
     - stdout carries `plant <case>`;
     - `--attempt` exists.

     **Read the current `tools/evaluator/model_io.py` for the exact paths it uses**, and follow DATA.md where they
     differ.
   - `tests/test_evaluator_verdict.py::test_an_open_id_gets_no_verdict_and_is_listed_out_of_scope`: `out_of_scope` is
     now a list of `{"id", "reason"}`.
   - `tests/test_evaluator_workspace.py::test_an_exclude_glob_replaces_the_default_tests_glob`: `--exclude` now
     **adds** to the defaults (R1-F8). Rename the test, and assert the new behaviour.
   - `tests/test_evaluator_r1.py::test_a_judge_answer_whose_root_is_not_an_object_is_dropped_rather_than_crashing`:
     call 1's answer lives in the judge folder.

## Part 2: fix your own two modules

Implement R1 in `tools/evaluator/probe_matrix.py` and `tools/evaluator/spec_parse.py`:
- F1 (`spec_parse` exits 2 on an empty manifest);
- F3 (import `ID` from `spec_parse`; read hyphenated ids);
- F4 (baseline before the product run; `product_changed`);
- F5 (the optional `runs` key with `status` and `errors`);
- F14 (`unparsed_ids`).

The frozen tests for these are `tests/test_evaluator_r1_matrix_spec.py`, written by Codex. Do not change them.
Every existing key in `matrix.json` keeps its exact shape.

## Standard (the COO runs it)

`env -u NO_COLOR python3 -m pytest -q` and `node tests/workflows/evaluate_harness.mjs`. After this, the only failures
left should be in Codex's modules: its attempt 2 was cut short by a usage limit and resumes after you. List every
failure you still see, and say whose module it is in.

## Limits

- **May change:**
  - Part 1: the test files named above;
  - Part 2: `probe_matrix.py` and `spec_parse.py`.
- **Must not change:** `verdict.py`, `workspace.py`, `model_io.py`, the workflow, docs, the
  `tests/test_evaluator_r1_matrix_spec.py` file. Do not commit.
- **Timer:** outer 1800 s.

## Write the result to

Print it as your final answer:
1. the header (`node: r1-opencode`);
2. Part 1: one line per assertion you changed, with old and new;
3. Part 2: finding → file:line;
4. CONTRADICTS, if any;
5. the summaries.
