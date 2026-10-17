# Brief — review-runner-exit (read-only)

Review the guard change "a test failure only when the runner made the exit" in this repository (the current folder is
its root). Do not change any file; your final message is the review.

The change: `git diff 5ffe562..0cb4657 -- .claude/skills/workflow-design/guard` (code, tests and `SPEC.md` section
"Round 17"). The owner's decision: the guard records a failed test run only when the test runner made the call's exit,
or the runner's own summary shows failures; otherwise the call is a command-error warning naming the last command word.

Find defects: a command shape where a runner's real failure is now lost (no failure and no warning); a shape where
another command's exit is still recorded as a failed test run; how `segments()` marks `piped`, `&&`, `||`, `;`, `&`,
subshells `( … )` and heredocs, and whether `testRunMadeExit` reads them right; the interaction with a declared red run
(Round 12) and `expect-fail --run` (Round 16); a test that passes against wrong code; SPEC text that says what the code
does not do. Return `status: done`, then a heading `Findings` with one numbered finding per defect — severity,
file:line, what is wrong, the input that shows it, the fix — and "Checked and found nothing" for each area that is
clean.
