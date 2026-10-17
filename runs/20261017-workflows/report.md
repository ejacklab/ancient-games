# Report — run 20261017-workflows (time-boxed: 4 hours or 6 rounds, whichever first)

**6 rounds in about 42 minutes. Your decisions are integrated, and the plan-B pattern is now two saved workflows,
each of which has run once for real.**

## Your decisions, integrated
- **Clock only.** One line after every Bash or file-write call; no reminders at 50%, 80% or 100%. The marks, `--marks`
  and `deadline wait --mark` are gone, and asking for either is a usage error. Workers' progress is read with
  `deadline status`.
- **The guard watches Bash and file writes only** (D2 of the time-monitor run declined). The install snippet and its
  test are back to those matchers, and the parked TODO is closed: your installed settings already match.
- **Four insight categories** (the Source kinds): done in the code yesterday; docs and tests now match.
- **Workflows, not hand-run rounds** (D3 declined). Two saved workflows exist; see below.
- **"Whichever comes first"** (P0 accepted): now in method 3.8 item 14, for when both a time and a number of rounds are
  given.

All of it went through the workflow `integrate-decisions`:
- four builders worked on disjoint files;
- a verifier ran every suite and grepped for leftovers;
- an adversarial reviewer found 13 issues, all fixed.

## The two saved workflows (`.claude/workflows/`)
- **`experts-decide`** asks the experts one question. Each expert works in its own subfolder; each answer is checked;
  a missing answer gets one rerun; then it writes the comparison. It decides nothing.
  - **Live run:** "keep `deadline wait --mark`?" Four experts answered and all passed the check.
  - Three advised remove, 孫子 advised keep. Provisional decision: removed, and a usage error.
- **`crossed-build-check`** has engines other than the code's write tests, shows each fails on the base commit, runs
  them on the current code, then has a read-only review.
  - **Live run:** today's clock-only change. opencode wrote 17 tests: 10 failed on the base as designed, and all 17
    pass now.
  - The 7 that also passed on the base test behaviour the change didn't touch.
  - The dsh review found 6 issues, all fixed with tests: the clock after file writes, old deadline files, minutes
    rounded down, `--marks` refused, and a deadline claimed only by the guard command itself.
- Each workflow has an offline harness (stubbed agents, no tokens) whose every check is shown failing on a planted
  input.

## Checks
Guard 1351/1351, tsgo clean, Python 1133, three workflow harnesses all passed. Pushed.

## Yours to decide
- **D-mark** (provisional): `--mark` removed. 孫子's dissent: "the defect is the fixed percentage".
- **From the experts:**
  - Dave's wake a set number of minutes before the deadline (you'd pick the number);
  - whether the report is due before the deadline or after the time-up line.
- **The fix for F-bdea5631** (below).

## Failures and insights (`insight.md`)
- **F-3caba088:** I parsed a workflow's output file by an assumed structure. Your pick: print the keys first, now a
  working rule.
- **F-bdea5631:** a trailing `ls` in a test command line made the guard record a failed test run.
  - My first insight blamed the planned red run; the workflow's own report corrected me.
  - Options: the guard records a test failure only when the test runner made the exit; planned red runs as their
    own call; the workflow runs them through `expect-fail --run`.
