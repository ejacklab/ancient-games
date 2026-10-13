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

Run the suite. After this attempt, the only failures left should be:
- those tests;
- `tests/test_evaluator_r1_matrix_spec.py`, which covers opencode's modules.
