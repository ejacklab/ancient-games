# Plan — finish everything open (time-boxed: 6 hours, deadline 08:18)

EJ: "can you get 6 experts help to auto finish everything within 6 hours via a well plan and design workflow
execution?" Method 3.8 item 14: questions go to the experts; the main agent decides provisionally, applies its top
pick (R12.3) and reports; the owner accepts or declines at the end. Safety bounds wait for the owner: another session's
uncommitted work is never committed, stashed or overwritten; a harness's config needs the owner's yes.

## Engines (checked 02:18)
- opencode: free now; one at a time (another session also uses it). mcode: works for small briefs. Claude subagents:
  inside workflows. agy: read-only reviews. Codex: 99% of its 5-hour window used, resets about 04:00. dsh: returned
  nothing on its last review — used last.
- Crossing holds for every build: tests by one engine, code by another, review by a third.

## The backlog, in order (each: done when its check holds)

| # | Item | Kind | Done when |
|---|---|---|---|
| 1 | Merge `build/evaluator` + the parser fix into master | merge | merged in a clean worktree branch `merge/evaluator` with every suite passing; the master merge itself waits only for the other session's uncommitted `docs/TASK_TYPES_LEDGER.md` (safety bound) — done the moment it is committed |
| 2 | memory_check's Fails-if lines separate cases with "; " | spec | the parser's cases for every memory_check group are whole clauses (no fragment like "ignored files included") |
| 3 | The 17 unjudged review findings of memory-check | review-fix | each judged against the tool's docs; the accepted ones reproduced red and fixed; 87+ tests pass |
| 4 | Guard: deadline commands target one deadline (`--id`; status/end by run) | guard fix | `deadline end` never ends another run's deadline (the slip of 2026-10-17) |
| 5 | Guard: the criteria step does not ask while the task's background work runs | guard fix | a stop with a running workflow or background task is not blocked for unmarked criteria |
| 6 | Guard: the C17 tests use an injected process list | test fix | C17 passes with other sessions' engines running |
| 7 | crossed-build-check: a timeout per engine call (not 580 s fixed) | workflow fix | the harness shows the given timeout reaching the command |
| 8 | Evaluator: the judge copy inside the run folder (EV-R3.2) | evaluator fix | no evaluator file is written outside `runs/<runId>/` |
| 9 | Evaluator: the five result states (pass, fail, needs a reviewer, not applicable, could not run) | evaluator design | experts' design applied, or kept open with a reason |
| 10 | Evaluator: use cases as an input (trace each use case to requirement ids) | evaluator design | as 9 |
| 11 | Evaluator: proof rule O8 (every probe red on its mutant, or one) | evaluator decision | experts advise; the main agent decides provisionally |
| 12 | The evaluator at a milestone, end to end: evaluate memory_check, ingest the verdict | integration | a verdict on memory_check exists and `evaluation ingest` turned it into failures and notes (cost recorded) |
| 13 | The 42 older insights with no recorded choice | triage | each marked, under today's R12.2, as evidence (no choice needed) or a real failure with its top fix applied |
| 14 | Report | — | written at the end of the time, with every provisional decision and what waits for the owner |

## Owner-only — provisional answers from the experts, for EJ to accept or decline
- O1/O3 of the "every task teaches" plan (what counts as a change; how main use cases are marked).
- The experts' proposed method change (a question trials cannot answer goes to the owner at once).
- Whether Claude Code's `~/.claude/projects/*/memory/` is agent memory under the guidelines.
- A real project with `project-memory/` for memory-check's calibration (a fact only the owner has: none found).

## How it runs
One workflow per item or pair of items, in the order above (sequential; opencode never twice at once), using the saved
workflows where they fit (`review-enhance` for 3; tests-first → engine → verify for 4–8; `experts-decide` for 9–11 and
the owner-only questions). Each step's evidence goes in `runs/20261018-finish-everything/`. Tested work is committed and
pushed as each item lands. Out of scope: another session's work (`TODO-2.0.md`, the code-map build).

## After the experts' review (plan-review/compare.md, 02:30) — provisional decisions, the main agent's
- **9–11 on paper.** All six: no ~1M-token measuring run for them inside the window. Each is written as a design
  choice with its reasons and kept open for the owner, or decided where the code already answers it.
- **12 once, after the fixes it measures** (Linus, 老子, Dave, Dario): after items 3 and 8.
- **13 marks only.** Sun Tzu, 老子, Dave, Dario: every one of the 42 is marked evidence or failure; a fix is applied
  only where its check is already known and time is left.
- **1 never holds the run** (five of six) — already moot: merged and pushed at 02:24 (`76596fa`); only the ledger row
  waits for the other session.
- **Clock.** A checkpoint at 05:18 (Sun Tzu, Dario): what is done, what is dropped. The report is written from 07:45
  and done by 07:58 (老子).
- **An empty engine output is not done** (Dave): rerun once on another engine.
- Item 3 already runs as a judge step over the 17 saved findings (Dave's change), on Claude, not the reviewers' engines.
- Branches other than master are not pushed (standing rule; Dario's question answered by it).
