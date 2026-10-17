# Report — crossed check on guard Round 17

**opencode's 15 tests: 6 failed on the base as designed and all 15 pass now. Codex's review: 7 findings, all
reproduced; one was a regression of mine, now fixed; five were already there before Round 17; one was my SPEC
wording, fixed.**

## Run
`crossed-build-check` (workflow `wf_a9e82ef9-09e`), base `5ffe562`, head `0cb4657`; code by Claude, tests by opencode
(`test/round17-crossed.test.ts`), review by Codex read-only (`nodes/review.last.txt`).

- **Failed on the base (6):** the V2 cases — F-bdea5631's `…; ls <gone>`, `&&`, `||`, `timeout 60 …`,
  `env -u NO_COLOR …`, and the warning's evidence. Each failed with "Expected warning, received failure".
- **Passed on the base (9):** the V1 cases and two controls — runner piped to `tail` or `grep`, last after `cd … &&`,
  two runners, a not-last runner whose summary speaks, and an interrupted run. Round 17 left that behaviour alone, so
  these are controls, not misses.
- **Head:** 15 pass.

## The review's findings, checked (`probe.ts`, `nodes/probe.base.txt`, `nodes/probe.head.txt`)
| # | Input | Base | Head | Verdict |
|---|---|---|---|---|
| 1 | `pytest -q && bun …/cli.ts insight`, exit 1 | failure | nothing | **regression, fixed** (T5) |
| 2 | `pytest -q \| grep missing`, exit 1 | failure | failure | real, was there before |
| 3 | `false && pytest test/a.py`, exit 1 | failure | failure | real, was there before |
| 4 | `pytest -q \| (cat)`, stdout `3 failed` | nothing | nothing | real, was there before |
| 5 | `bun test a; pytest b`, exit 2 | `bun test run` | `bun test run` | real, was there before |
| 6 | SPEC: a chained red run "is then not a red record" | — | — | **wording, fixed** (only with no summary) |
| 7 | `pytest; echo '3 errors' >&2; false` | failure | failure | real, was there before |

## Checks
Guard 1373/1373 (1357 + 15 opencode + T5), tsgo clean.

## For EJ
- Findings 2, 3, 4, 5 and 7 (proposed fixes in the message).
- The insight for finding 1 (`insight.md`): the source options.
