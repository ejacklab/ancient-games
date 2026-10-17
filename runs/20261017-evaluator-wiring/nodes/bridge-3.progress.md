# bridge-3 · progress

- 2026-10-18T00:16:49+08:00 · bycase · planned · V7, by case: hold a group back only when every one of its FAIL cases was FAIL in the baseline; a FAIL case the baseline did not fail keeps the group a failure (case → group by the id prefix, `B1-F1` → `B1`)
- 2026-10-18T00:16:49+08:00 · usage · planned · the `--baseline` usage line names the rule as it now reads
- 2026-10-18T00:16:49+08:00 · verify · planned · `bun test` all pass, `tsgo --noEmit -p .` clean
- 2026-10-18T00:16:49+08:00 · report · planned · result file written
- 2026-10-18T00:16:49+08:00 · bycase · start · the path's early returns listed first: baseline unreadable → blocked note (unchanged), group not failing before → not held back, group failing before with no FAIL cases → held back (V7's own test), with an unknown FAIL case → a failure, and the V3 same-bytes return before any record
- 2026-10-18T00:17:36+08:00 · bycase · done · `failingCaseIds()` + `heldBackGroups()` in evaluation.ts, replacing `failingGroupNames()` alone in the baseline branch; the new FAIL-case test passes
- 2026-10-18T00:16:49+08:00 · usage · start · one line of cli.ts usage text
- 2026-10-18T00:17:36+08:00 · usage · done · "`--baseline F` holds back the groups F already failed, case by case"
- 2026-10-18T00:16:49+08:00 · verify · start · `bun test`, `tsgo --noEmit -p .`, then the four uncovered baseline shapes by hand in a scratch root (no cases array, a case the baseline judged PASS, every case known, unreadable baseline, `--baseline` with no value)
- 2026-10-18T00:17:36+08:00 · verify · done · 1527 pass / 0 fail, tsgo exit 0; the hand checks behaved as the rule reads (written in the result file)
- 2026-10-18T00:16:49+08:00 · report · start · result file
- 2026-10-18T00:17:36+08:00 · report · done · runs/20261017-evaluator-wiring/nodes/bridge-3.result.md