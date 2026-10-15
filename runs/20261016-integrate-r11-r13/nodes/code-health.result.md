status: done

H1–H5 of spec-harness-health.md are implemented in harness_health.py: R11/R12 replace R10 in the table, the Claude hooks line moved to R12, the seven guard files are covered lines, the four unchecked sub-requirements have their own lines, and the guard's hooks/results/insight state is read through `doctor --json`, `rates --json` and `insight --json`.

Files

- `.claude/skills/workflow-design/scripts/harness_health.py`
- `runs/20261016-integrate-r11-r13/nodes/code-health.result.md`

Commands and last lines

- `python3 .claude/skills/workflow-design/scripts/harness_health.py` → rc 0; new lines shown:
  `| R11 | - | use-case register and coverage (R11.1) | verified | covered | per run, by register.ts | register.ts |`,
  `| R12 | - | failure journal (R12.2) | verified | covered | per run, by journal.ts | journal.ts |`,
  `| R12 | codex | harness-guard hooks | reported | absent | no harness-guard hook found in 1 read file(s) | `harness-guard doctor` |`,
  `| R12 | - | checked results in this project | verified | measured | 0 success lines, 0 failure records | `harness-guard rates` |`,
  `| R12 | - | insight for every failure (R12.3) | verified | present | no open failures | `harness-guard insight` |`,
  `| R12 | - | (12) withdrawal conditions (R12.6) | unknown | unknown | no script checks it; each run's design must show it | references/harness-requirements.md |`,
  `R10 (feedback loop) is replaced by R12. R11 and R12: the workflow-design skill's references/harness-requirements.md.`
- `python3 … --json` → `50 findings`; reqs 11 and 12 present, no R10.
- `python3 … --self-test` → `self-test PASS: no deny list → absent, a deny list → present — the check can fail.` rc 0.
- `env -u NO_COLOR python3 -m pytest -q tests/test_harness_health.py` → `3 failed, 32 passed in 4.51s`.
- Guard failure paths checked by hand (no test file written): no bun on PATH → one `MISSING` line `bun not on PATH`; no
  `guard/src/cli.ts` → one `MISSING` line `guard not found beside this script`; non-JSON output / exit 3 / a hanging
  `bun` → that line only, `unknown`, `the guard's <command> failed: unexpected output|exit 3|timeout`, no guard text
  printed; insight with 2 open failures → `absent`, `2 open failures without a valid insight (ids not printed)` plus its
  help; HOME and the project directory mtime unchanged across a full `gather()`.

Old tests that fail until the test writer updates them

- `test_hh_01_ten_rows_and_no_machine_paths` — asserts the requirement list is 1..10; now 1..9, 11, 12.
- `test_hh_06_covered_goes_missing_without_its_script` — builds a fake `scripts/` with only the six old scripts, so the
  seven new `../guard/src/*.ts` covered lines come out `MISSING`. This is the fails-if check working, not a defect.
- `test_hh_16_unreadable_folders_are_unknown_not_a_crash` — asserts the heading `## Ten requirements`, now `## Requirements`.

CONTRADICTS: none. Three spots where the spec left a choice, resolved as noted: the doctor row's harness name is used
verbatim in the `install --print` snippet (`claude-code`, not `claude`, which is what "doctor's harness name" says); the
`rates` row counts are validated as integers and a non-integer `ok`/`fail` becomes `unexpected output` rather than
counting it as 0; and `guard_json` accepts only exit 0 for `doctor`/`rates`, 0 or 1 for `insight`, per H5.