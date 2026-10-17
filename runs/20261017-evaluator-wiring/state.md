# State — run 20261017-evaluator-wiring

Request: "using a workflow and 6 experts to check the evaluator first then design the wiring, implement, test, review
and improve the effectiveness". Limit: "1 hour and 3 rounds" — deadline D-c578cc89, 23:38 → 00:38, or 3 rounds,
whichever first (method 3.8 item 14: decisions provisional from the experts, the owner accepts at the end).

## Rounds
| Round | What | State |
|---|---|---|
| 1 | six experts check the evaluator (check-question.md); design the wiring | done 00:07 |
| 2 | the bridge: spec, tests red first (Claude), code (mcode) | done 00:10 |
| 3 | measured on 6 real verdicts; per group + case baseline (39 → 6 failures, 5 of 6 faults) | done 00:20 |

## Provisional decisions (item 14: the owner accepts or declines each at the end)
- P1 The evaluator is not ready to judge every build (all five usable experts, check-q/compare.md); it runs on
  milestone builds or a build the owner names, never per task.
- P2 A blocked or crashed evaluator run is a note to the owner, never a failure: under R12.2 a failure is the
  evaluator's judgment, and a crash is none (Linus; Laozi wanted a failure, Sun Tzu an R12.1 record).
- P3 This hour builds only the bridge, verdict.json → guard (guard SPEC Round 19): FAIL → a failure found_by
  evaluator, UNKNOWN → a note, once per verdict.
- P4 Left open, for after this run (each needs more than the hour): use cases as an input (trace each use case to
  requirement ids — Sun Tzu's middle option), the proof rule O8 (every probe red — the literal EV-C3.2, since a wrong
  PASS is the dangerous direction), the parser's grammar (it exits 2 on memory_check's and the harness's
  requirements, measured by the compare step), the five result states, merging build/evaluator, EV-R3.2's /tmp
  judge copy.
- The bridge went to mcode: another session's opencode was running (code-map build, 35-minute limit) and Codex had
  99% of its 5-hour window used.

## Log
- 23:38 deadline started. Snapshot of build/evaluator in snapshot/ (27 files); its tests 177 passed (nodes/evaluator-tests.txt). Waiting for the memory-check review's opencode to finish before the experts start.
- 23:48 my slip: deadline end --session (meant for the memory review's D-3ae31886) ended this run's D-c578cc89, the newest open one; ended the review's, restarted this run's clock for the minutes left (to 00:38) — the guard's per-session deadline defect, again.
- 00:07 check-q done (25 min, 777k tokens): 5 of 6 usable (Dave timed out twice); verdict not ready. Round 19 spec + 7 tests red first (nodes/round19.red.txt); bridge to mcode.
- 00:20 round 3: per group then baseline by case, measured on the six K2 verdicts: 39 → 12 → 5 (group baseline hid k2-4) → 6 (case baseline, 5 of 6 faults, the evaluator's own rate); guard 1527/1527, tsgo clean. Report written.
- 01:52 P1, P2, P3 accepted by EJ ("use a workflow to run your three provisional decisions"); written into method 3.6, the skill and the changelog.
