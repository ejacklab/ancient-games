# Brief — r1-code (codex), attempt 2

## Task

Implement repair R1 in the modules you built:
- `tools/evaluator/verdict.py`;
- `tools/evaluator/workspace.py`;
- `tools/evaluator/model_io.py`;
- `.claude/workflows/evaluate-requirements.js`.

The rules are in `docs/evaluator/DATA.md`, section **"Repair R1"** and the table **"The workflow after R1"**. Your
attempt-1 changes are still in the worktree: continue from them.

## Context

- `docs/evaluator/DATA.md`: re-read Repair R1. **Two rules were corrected after your attempt 1** (see the feedback).
- **Frozen tests:** `tests/test_evaluator_r1.py`, `tests/workflows/evaluate_harness.mjs`, and every existing
  evaluator test.
- The workflow is plain JavaScript with no filesystem access. Never compute a verdict in the workflow.

## Feedback from attempt 1 (the COO's rulings on your CONTRADICTS lines)

Thank you: several of your CONTRADICTS lines were right.

**The COO's own contract errors, now corrected in DATA.md. Change your code to the corrected wording:**
- **F5(c)** is Dave's **guarded** rule: **when** a mutant run has 2 or more probe results, not every one may be
  `fail`. A single-probe run is **not** judged by (c). Your attempt used the strict reading, so the single-probe PASS
  fixtures broke.
- **The F4 reason** is now `"product copy not restored or changed"`. It contains "restored", so the old frozen test
  stands.

**Tests that are wrong, and that their author (opencode) will repair next. Do not work around them; leave your code
to the contract:**
- the R1-F1 test's `out_of_scope == 2` assertion, which sits after its loop;
- the harness `repairRound` and `judgeRerun` fixtures, which are missing answers for the retry calls;
- the harness `excludeGlobs` case: shell-quoting a glob is right;
- the old tests that pin the pre-R1 contract:
  - the two-number `confirm-check` output;
  - the plant data in `judge-input.json`;
  - out-of-scope as plain strings;
  - `--exclude` replacing the defaults;
  - the judge call 1 file location.

## Standard

Run the full suite and the harness. After this attempt, the only failures left should be:
- the tests listed above;
- `tests/test_evaluator_r1_matrix_spec.py`, which covers opencode's modules.

## Limits

- **May change:** those four files.
- **Must not change:** tests, harness, docs, `probe_matrix.py`, `spec_parse.py`. Do not commit.
- **Timer:** outer 1800 s.
- **Attempts left:** 2.

## Write the result to

Print it as your final answer:
1. the header (`node: r1-code-codex`, `attempt: 2`);
2. what changed;
3. the remaining failures, by name;
4. CONTRADICTS, if any;
5. the command summaries.
