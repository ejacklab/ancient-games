# Spec — harness_health.py reports R11 and R12 (run 20261016-integrate-r11-r13)

File: `.claude/skills/workflow-design/scripts/harness_health.py`. Tests: `tests/test_harness_health.py` (new tests
HH-18 onward; update the old ones only where this spec changes what they assert). The guard's `--json` commands are
specified in `.claude/skills/workflow-design/guard/SPEC.md`, Round 7. The requirements themselves:
`docs/HARNESS_REQUIREMENTS.md` (R11, R12).

Everything the docstring promises still holds: no quota, no file written, no config value printed, findings never
change the exit code, no machine path printed (paths shown through `Where.show`).

## H1 The requirement table
- `REQUIREMENTS` holds 1–9, **11** "Results can be judged" and **12** "Failures and successes update the harness".
  10 is gone.
- The markdown heading is `## Requirements` (was `## Ten requirements`). Directly under the table, one line:
  `R10 (feedback loop) is replaced by R12. R11 and R12: the workflow-design skill's references/harness-requirements.md.`
- The module docstring says the same in its first paragraph (the list of requirements names R11 and R12, and that
  R12 replaces R10).

## H2 The Claude hooks line moves to R12
The Claude `hooks` line (today `req 10`) is `req 12`. Its logic and help are unchanged.

## H3 Covered lines for the guard
Add to `COVERED` (same mechanism: `covered` when the file exists, `MISSING`/`unknown` when not), paths relative to
`scripts/`:

| req | item | file |
|---|---|---|
| 11 | use-case register and coverage (R11.1) | `../guard/src/register.ts` |
| 12 | engine result check (R12.1) | `../guard/src/traps.ts` |
| 12 | failure journal (R12.2) | `../guard/src/journal.ts` |
| 12 | insight gate (R12.3) | `../guard/src/insight.ts` |
| 12 | success lines and rates (R12.7) | `../guard/src/rates.ts` |
| 12 | success paths (R12.7) | `../guard/src/paths.ts` |
| 12 | criteria and score (R12.7) | `../guard/src/criteria.ts` |

## H4 The sub-requirements no script checks
One line each, harness `-`, status `unknown`, finding `unknown`, detail `no script checks it; each run's design must
show it`, proof `references/harness-requirements.md`:
- `(11) first signal before the full verdict (R11.2)`
- `(12) judges say what is wrong, not how (R12.4)`
- `(12) review when a model changes (R12.5)`
- `(12) withdrawal conditions (R12.6)`

## H5 The guard's state, through its own commands
The guard CLI is `scripts/../guard/src/cli.ts`; it runs with `bun` found on the `PATH` given to `gather` (the `env`
argument), with the working directory set to `gather`'s `cwd`, the same environment, stdin from `/dev/null`, and a
timeout (readiness's `CMD_TIMEOUT`).

- If `cli.ts` is not there: one line `(12, "-", "harness-guard", MISSING, "unknown", "guard not found beside this
  script", "guard/src/cli.ts")` and none of the lines below.
- If `bun` is not on the PATH: one line `(12, "-", "harness-guard", MISSING, "unknown", "bun not on PATH",
  "`command -v bun`")` and none of the lines below.
- **Hooks per harness** — `doctor --json`. For each row whose harness maps to an installed harness (`claude-code` →
  `claude`; `codex`, `qwen`, `opencode` as named), one line `(12, <harness>, "harness-guard hooks", REPORTED,
  <finding>, <note>, "`harness-guard doctor`")` where finding is `present` for guard `installed`, `absent` for
  `absent`, `unknown` otherwise. An `absent` line carries help: file `-`, changes `installs the guard's hooks: it
  blocks known engine-call traps, logs failures as they happen, and asks for the insight before the agent stops`,
  snippet `bun <cli shown through Where.show> install --print <doctor's harness name>`, lang `sh`, how `prints the
  settings to merge; you apply them`.
- **Checked results** — `rates --json`. One line `(12, "-", "checked results in this project", VERIFIED, "measured",
  "<sum ok> success lines, <sum fail> failure records", "`harness-guard rates`")`.
- **Open failures** — `insight --json` (exit 0 or 1 are both answers). One line `(12, "-", "insight for every failure
  (R12.3)", VERIFIED, …)`: `present` with `no open failures` when `open` is empty; else `absent` with `<n> open
  failures without a valid insight` (ids not printed) and help: file `runs/<run>/insight.md`, changes `answers each
  open failure: six whys, the root cause, two or three fix options (R12.3)`, no snippet.
- A command that times out, exits with a code it should not (anything but 0; for `insight` anything but 0 or 1),
  or prints output that is not the JSON shape of Round 7 → that line is `unknown` with `the guard's <command> failed:
  <exit code | timeout | unexpected output>` — never the command's own text. The other lines still run.

## Fails-if
R10 still a row; R11 or R12 missing from the table; a sub-requirement R11.1–R11.2 or R12.1–R12.7 has no line; a
covered guard line stays `covered` when its file is gone; the run crashes or exits non-zero when bun or the guard is
missing, or when a guard command fails; a guard command's raw output appears in the report; a file changes under
HOME or the project during a run (the real guard included, when bun is installed); an `absent` hooks line has no
help; open failures are counted as `present`.
