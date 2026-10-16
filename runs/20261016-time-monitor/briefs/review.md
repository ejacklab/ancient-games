# Brief — review (read-only)

Review commits `b716bdf..3033e18` in this repository (`git diff b716bdf~1..3033e18 -- .claude/skills docs`): guard
Round 10 (`.claude/skills/workflow-design/guard/SPEC.md`, Round 10 and its correction; `src/deadline.ts`, `src/hooks.ts`
withTime and handleUserPromptSubmit, `src/cli.ts` deadline), the four-experts runner change, and method 3.8 item 14.

## Pieces and progress (first)
Divide the review into small pieces (e.g. T1–T6, the runner, the docs). Append a `planned` line per piece to
`runs/20261016-time-monitor/nodes/review.progress.md`, then a line as each starts and ends:
`- <ISO time from date -Iseconds> · <piece> · <planned|start|done|fail> · <short note>`

## Find defects
Code that does not do what the SPEC says; a check that cannot fail; a test that passes against wrong code; a crash or
a file written where none should be; a reminder that could repeat, go missing, or reach another session; time
arithmetic errors (rounding, time zones, a deadline that never ends). Run `cd .claude/skills/workflow-design/guard &&
bun test` if useful. Do not change any file except the progress and result files. No other AI engine. Stop by 11:00 +0800.

## Result
`runs/20261016-time-monitor/nodes/review.result.md`: `status: done`; one numbered finding per defect — severity,
file:line, what is wrong, the input that shows it, the fix you suggest; "Checked and found nothing" for each area where
that is true.
