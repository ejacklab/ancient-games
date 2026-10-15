# Optimisation round

**Measure chosen: the wall time of `tests/test_harness_health.py`**, the check every later change to
`harness_health.py` has to pass. Before the round: **41.51 s** (87 tests, `--durations`: three timeout cases at 10.1 s
each, 30 s of the 41). After: **14.51 s** (87 tests; the three cases at 1.05 s each). Lower is better; 65% less.

Change: the three timeout cases of HH-26 run `gather()` in-process with `CMD_TIMEOUT` set to 1 s and a guard that
sleeps 2 s, with PATH and HOME set to the test box; every other case still runs the script as a person would. The
check still fails when the timeout handling breaks: mutants M13 (timeout reported as an exit) and M14 (timeout not
caught) are killed (`mutants.txt`). What it does not establish: that the real 10 s limit is the right value — that
value is readiness's, unchanged.

Measured and not changed:
- `harness_health.py --json` run time: 0.07 s on master, 0.12–0.13 s after the build (five runs); each guard call 0.01–0.02 s
  with bun's cache off. Not worth a change: under a tenth of a second.
- Report size: 123 lines / 7,294 bytes on master, 173 lines / 10,518 bytes after. Every new line answers C1 (a line per
  sub-requirement); folding them would hide which sub-requirement no script checks. Left as is.

Numbers: `baseline-runtime.txt` and the two pytest runs in this session (41.51 s, 14.51 s).
