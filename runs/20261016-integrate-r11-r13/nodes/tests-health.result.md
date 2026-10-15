status: done
Wrote spec-derived H1–H5 acceptance tests HH-18–HH-28 and the required legacy updates; the final run has 69 passing and 7 failing cases against the current implementation.

files:
- tests/test_harness_health.py
- runs/20261016-integrate-r11-r13/nodes/tests-health.result.md

commands and last lines:
- `env -u NO_COLOR python3 -m pytest -q tests/test_harness_health.py` — exit 1:

```text
=========================== short test summary info ============================
FAILED tests/test_harness_health.py::test_hh_18_requirement_table_and_docstring
FAILED tests/test_harness_health.py::test_hh_25_open_failures_are_absent_with_insight_help[1-1]
FAILED tests/test_harness_health.py::test_hh_25_open_failures_are_absent_with_insight_help[2-1]
FAILED tests/test_harness_health.py::test_hh_25_open_failures_are_absent_with_insight_help[1-0]
FAILED tests/test_harness_health.py::test_hh_26_guard_command_failures_are_isolated_and_redacted[wrong-type-doctor]
FAILED tests/test_harness_health.py::test_hh_28_real_guard_is_read_only_with_empty_and_open_journal[empty-project]
FAILED tests/test_harness_health.py::test_hh_28_real_guard_is_read_only_with_empty_and_open_journal[open-failure]
7 failed, 69 passed in 39.66s
```

- `git diff --check -- tests/test_harness_health.py` — exit 0, no output.

CONTRADICTS (observed implementation versus spec):
- H1: "The module docstring says the same in its first paragraph" — HH-18 finds only the introductory title in the first paragraph, without R11/R12/R10.
- H5: detail "<n> open failures without a valid insight" followed by the instruction "(ids not printed)" — HH-25's three nonempty cases and HH-28's open-failure case find the parenthetical literally appended to the detail. Tests treat the parenthetical as an instruction, outside the specified detail text.
- H5: output "not the JSON shape of Round 7" must become unknown, "never the command's own text"; Fails-if: "a guard command's raw output appears in the report" — HH-26 wrong-type-doctor supplies numeric guard: 7 with SECRET-PLANT-7f3a9c in note; that note reaches the report rather than an unexpected-output finding.
- Fails-if: "a file changes under HOME or the project during a run (the real guard included, when bun is installed)" — HH-28 empty-project detects new HOME/.bun/install/cache entries. The open-failure case runs independently and fails earlier on its detail text.

Coverage: all seven guard coverage files are planted and individually removed; the four design-only lines stay unknown; guard and bun missing cases are planted; doctor harness mapping, absent-hook help, rates aggregation, insight exits 0/1, command exits, non-JSON, missing fields, malformed field types, timeouts, output redaction, and read-only runs are exercised. The fake bun verifies CLI location/arguments, cwd, HOME/PATH, and /dev/null stdin. Both real-guard cases ran; neither was skipped.

These checks were authored by this worker from the supplied spec, using the existing test interfaces and Round 7 types. They are acceptance tests, not independent proof that the implementation is correct. No new implementation bodies were read; harness_health.py was not changed. No other AI engine was used and no commit was made. The failing acceptance cases are retained for the implementation worker.
