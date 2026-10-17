# Insight — run 20261017-round17-crossed

## Review finding 1 — Round 17 made a real test failure disappear

Found by: Codex's read-only review (`nodes/review.last.txt`, finding 1); reproduced by `probe.ts` on head
(`nodes/probe.head.txt`: "nothing recorded") and on the base (`nodes/probe.base.txt`: a failure).

Whys:
1. Why was a failure missed? `pytest -q && bun …/src/cli.ts insight` exiting 1 with no summary left no record.
2. Why? Round 17 sent it from D1 to D2's command-error path, and D2 skips a call whose last segment is a guard query
   exiting 1 (`guardQueryAnswered`, F1) — but after `&&` the query may never have run.
3. Why did my change not handle that? I tested what the new branch records, not what the existing path it now feeds
   does with the cases it newly receives; F1's exemption was written for calls with no test runner.
4. Why did my own tests miss it? T1–T4 cover the shapes in the insight and the option text; none puts an exempted
   command last.
Source: instruction — when a change sends new cases into an existing path, I do not list that path's early returns
and exemptions and test each against the new cases.
Root cause: a change routed calls into a path whose exemption assumed they could not reach it.
Fixed (the instance, as EJ's option 1 already requires a warning there): `src/hooks.ts` skips F1's exemption when the
call holds a test run; T5 in `test/round17-runner-exit.test.ts`, red on the old code (`nodes/t5.red.txt`).
Options for the source:
1. [rule] When a change routes cases into an existing path, list that path's early returns and exemptions and add one
   test per exemption with a new case. evidence: F1's exemption was the one early return the new cases reach.
2. [tool] crossed-build-check's review brief always asks "which existing exemptions do the newly routed cases reach".
   evidence: Codex found it when the brief named the interaction areas.
