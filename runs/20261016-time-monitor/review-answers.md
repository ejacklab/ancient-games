# Answers to the review (`nodes/review.result.md`, Codex gpt-6.1-sol, effort high; it wrote none of the code)

| # | Finding | Answer | Test (failed on 3033e18, passes now) |
|---|---|---|---|
| 1 | `--progress` to a missing folder crashed the runner after an expert started | fixed: the folder is made before any expert starts; a failed progress write warns, never stops supervision | — (runner has no test suite; py_compile only) |
| 2 | a command that mentions "deadline start", or a failed one, claimed another session's deadline | fixed: only a succeeded PostToolUse running this guard's `cli.ts deadline start` claims | review 2 |
| 3 | installed matchers kept the clock off Read, Grep and web calls | fixed in `install --print`: PostToolUse and PostToolUseFailure watch every tool (hook run measured at 0.02 s); **your installed settings still have the old matchers** — config advice for you | install test |
| 4 | the 100% block with workers was recorded but never said | fixed: said once at the first call past the deadline, then time-up alone | review 4 |
| 5 | a crafted id could write outside the deadlines folder | fixed: id must be `D-xxxxxxxx` and match its file name; marks and the end validated on load | review 5 |
| 6 | `--minutes 1e308` made a deadline that never ends | fixed: an end that is not a representable time is a usage error | review 6 |
| 7 | fractional budgets overstated the overrun | fixed: computed from the exact end, rounded once | review 7 |
| 8 | caller-run experts left no progress lines | fixed in part: the runner writes the hand-off line and tells the caller to append the end line; it cannot see a subagent finish | — |
| 9 | the minutes instruction did not cover a limit in rounds | fixed: a rounds limit has no clock; the state file holds the last round and the agent checks it before each round | — (docs) |
| 10 | the default-wait test accepted a live status | fixed: it must say time is up | the T3 test |

Its 47 suite failures were empty child stdout inside its sandbox; here the suite is 1263/1263 (same cause as F-76013d09).
