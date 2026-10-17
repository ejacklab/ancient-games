# Result — tests-clock

status: done — the guard's clock behaves as SPEC.md Round 10 T5 and the notes after it describe, and the acceptance tests now say so.

## Test file

`.claude/skills/workflow-design/guard/test/round10-clock-only.test.ts` — 17 checDone — only the three allowed files touched, nothing committed.

- Test: `.claude/skills/workflow-design/guard/test/round10-clock-only.test.ts` — 17 checks (one clock line at 10/49/50/51/80/99%, no mark reminder, no `deadline:<id>:<mark>` raised record, 100% clean, time-up twice in a row, other session silent), injected clock only.
- `bun test test/round10-clock-only.test.ts` → 17 pass, 0 fail, 189 expects.
- Result written to `runs/20261017-workflows/nodes/tests-clock.result.md`: status done, CONTRADICTS none.
 calls in a row after the deadline; another session's deadline adds nothing.

## Command

`cd .claude/skills/workflow-design/guard && bun test test/round10-clock-only.test.ts`

```
bun test v1.4.3 (c6da4a4d3)

 17 pass
 0 fail
 189 expect() calls
Ran 17 tests across 1 file. [120.00ms]
```

## CONTRADICTS

none. SPEC T5 ("before the deadline one line, `harness-guard clock: <m>/<N> min (<p>%), <left> left`; after it
`harness-guard time is up (<m> min over): …`. There are no reminders at 50, 80 or 100%: no marks, no mark block, no
`raised` mark record") and `src/hooks.ts` `withTime` agree on every point checked.

One boundary the tests leave open, on purpose: the SPEC says "after it" for time-up, so at exactly the deadline the
line is only required to be a single line with no mark text, not pinned to either form.