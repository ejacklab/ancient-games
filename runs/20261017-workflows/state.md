# State — run 20261017-workflows (time-boxed: 4 hours or 6 rounds, whichever first — EJ confirmed)

Request: build the plan-B pattern as workflows ("better build a workflow"). Start 2026-10-17 09:23 +0800 · deadline
13:23 +0800 (D-a4ab637c) · 6 rounds.

## Rounds
| # | Round | State |
|---|---|---|
| 1 | design both workflows (args, steps, returns, checks) | — |
| 2 | experts-decide.js + offline harness | — |
| 3 | crossed-build-check.js + offline harness | — |
| 4 | live run: experts-decide on a real decision | — |
| 5 | live run: crossed-build-check on a real small build | — |
| 6 | docs pointers, review, report | — |

## Decisions
- EJ 2026-10-17: P0 of run 20261016-six-experts accepted ("4 hours, 6 rounds is whichever come first").
- EJ 2026-10-17: D3 of run 20261016-six-experts declined ("build in into a workflow script will provide more flexible and enhancing") — this run builds the workflows.

## Log
- 09:23 start; deadline D-a4ab637c.
- 09:2x the guard denied a python heredoc holding a backslash (a new trap); files written with the Write tool instead.
- 09:3x EJ mid-run: "I prefer clock more than the 50% 80% and 100%" (D1 of run 20261016-time-monitor accepted as clock only; marks removed, 07b67a9) and "guard watches back to bash and file writes only" (D2 declined); then "Design and execute a workflow to integrate all the above decisions" — workflow integrate-decisions (run wf_ba186582-4eb): Build (guard revert, docs and records, experts-decide, crossed-build-check) → Verify → Review. The owner TODO for the hook matchers closed (memory removed).
- **D-mark (provisional; experts-decide mark-q, live run 1):** `deadline wait --mark` removed; passing it is a usage error (Dario's "fail loud"); `deadline wait` stays, to the deadline. Linus, Dave, Dario: remove; 孫子: keep ("the defect is the fixed percentage"). Open for EJ: Dave's wake a set number of minutes before the deadline; whether the report is due before the deadline or after the time-up line.
- 10:0x round 6: report, criteria 7/7; rounds 1-6 done in ≈42 of 240 min (whichever first: the 6 rounds); deadline ended.
