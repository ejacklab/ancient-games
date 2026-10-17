# Report — check the evaluator, wire it, test, improve (time-boxed: 1 hour or 3 rounds)

**The evaluator is not ready to judge every build (five experts, unanimous). Its verdict now reaches the guard: each
failing requirement group the evaluator finds — and not already failing before the change — becomes one failure found
by the evaluator; everything else is a note. Measured on its six real calibration verdicts: 39 failures per id became
6 failures for 6 planted faults, surfacing 5 of them — every fault the evaluator itself found.**

## Round 1 — the experts' check (`check-q/compare.md`)
Five usable answers (Dave timed out twice). Agreed: not ready for every build; it reads no use cases; about 1M tokens
and 20+ minutes per evaluation; three result states are not enough; nothing connected `verdict.json` to the guard; a
crash never becomes PASS. Measured by the compare step: its parser exits 2 ("no requirement ids found") on
`memory_check/REQUIREMENTS.md` and `docs/HARNESS_REQUIREMENTS.md`.

## Round 2 — the bridge (guard SPEC Round 19)
`guard/src/cli.ts evaluation ingest <verdict.json> --run DIR [--baseline <verdict.json>]` (`src/evaluation.ts`):
FAIL → a failure `found_by: evaluator` (it then needs its insight, R12.2); UNKNOWN → a line in
`DIR/evaluator-notes.md`; a blocked or missing verdict → a could-not-run note, exit 1, never a failure; once per
verdict. Tests by the main agent (Claude), each red first (`nodes/round19*.red.txt`); code by mcode (another session's
opencode was running; Codex had 99% of its window used).

## Round 3 — effectiveness, measured (`measure.sh`, `nodes/measure*.txt`)
On the evaluator's six K2 calibration verdicts (one planted fault each; the evaluator found 5 of 6 in its own
calibration):

| Bridge rule | Failures recorded | Runs with a new failure |
|---|---|---|
| one per requirement id | 39 | 6 of 6 (noise) |
| one per failing group | 12 | 6 of 6 |
| per group, baseline by group (k1d) | 5 | 4 of 6 — hid k2-4's fault inside an already-failing group |
| **per group, baseline by case (k1d)** | **6** | **5 of 6** — the miss, k2-2, is the fault the evaluator itself missed |

## Provisional decisions (yours to accept or decline) — `state.md`
- P1 Run the evaluator on milestone builds or a build you name, never per task.
- P2 A blocked or crashed evaluator run is a note to you, never a failure.
- P3 The bridge as built; its baseline is the last accepted evaluation of the same product.
- P4 Open: use cases as an input; the proof rule O8; the parser's grammar; five result states; merging
  `build/evaluator`; EV-R3.2's /tmp judge copy.

## Not done in the hour
- An independent review of the bridge (Codex out of quota, opencode busy, dsh returned nothing earlier).
- Calling the evaluator at the end of a real build: the bridge is ready, but the evaluator still lives on an unmerged
  branch and cannot parse this repo's requirement files.
