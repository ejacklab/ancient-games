# 孫子 (Sun Tzu) — a 6-hour plan, reviewed before it runs

## Answer

CHANGE

- **Defer the measurement of 9–11; keep only their written design.**
  Current:
      | 9 | Evaluator: the five result states (pass, fail, needs a reviewer, not applicable, could not run) | evaluator design | experts' design applied, or kept open with a reason |
      | 10 | Evaluator: use cases as an input (trace each use case to requirement ids) | evaluator design | as 9 |
      | 11 | Evaluator: proof rule O8 (every probe red on its mutant, or one) | evaluator decision | experts advise; the main agent decides provisionally |
  New:
      | 9–11 | Evaluator: the five result states, use cases as an input, proof rule O8 | evaluator design, deferred | a written recommendation per item in `runs/20261018-finish-everything/`, and the choice kept open with a reason — no 1M-token measurement inside the six hours |
  Price: three design questions stay unmeasured, and 12 will show only today's behaviour — a second session is owed.

- **Split row 1: the branch is unblocked, the master merge is not.**
  Current:
      | 1 | Merge `build/evaluator` + the parser fix into master | merge | merged in a clean worktree branch `merge/evaluator` with every suite passing; the master merge itself waits only for the other session's uncommitted `docs/TASK_TYPES_LEDGER.md` (safety bound) — done the moment it is committed |
  New:
      | 1a | Merge `build/evaluator` + the parser fix into a clean worktree branch `merge/evaluator` | merge | `merge/evaluator` carries both, every suite passing; time-boxed to one hour, then left as it is |
      | 1b | The master merge | owner-wait | the other session's uncommitted `docs/TASK_TYPES_LEDGER.md` is committed and the merge applies clean; recorded in the report, no gate on any other row |
  Price: the run ends with the work on a branch, not on master; everything after must build on `merge/evaluator`.

- **Run 12 as soon as 1a and 8 close, ahead of 3–7.**
  Current:
      | 12 | The evaluator at a milestone, end to end: evaluate memory_check, ingest the verdict | integration | a verdict on memory_check exists and `evaluation ingest` turned it into failures and notes (cost recorded) |
  New:
      | 12 | The evaluator at a milestone, end to end: evaluate memory_check, ingest the verdict | integration (starts when 1a and 8 close, before 3–7) | a verdict on memory_check exists and `evaluation ingest` turned it into failures and notes (cost recorded) |
  Price: if 12 finds a real defect, its ~1M tokens are spent before the cheap fixes and 3–7 run on a shorter clock.

- **Run 13 first, split across Claude subagents.**
  Current:
      | 13 | The 42 older insights with no recorded choice | triage | each marked, under today's R12.2, as evidence (no choice needed) or a real failure with its top fix applied |
  New:
      | 13 | The 42 older insights with no recorded choice — run first, split across Claude subagents | triage | each marked under today's R12.2 as evidence (no choice needed) or a real failure; a fix applied only where its check is known, the rest listed as new backlog |
  Price: judgement drifts when 42 sections are split, so a second pass over the marks is owed; I have no measurement that the split is faster than one reader.

- **Put the clock check in "How it runs" — the biggest risk is the clock, not any one engine.**
  Current:
      One workflow per item or pair of items, in the order above (sequential; opencode never twice at once), using the saved
  New:
      One workflow per item or pair of items, in the order above (sequential; opencode never twice at once), with 13 running first and split across Claude subagents, using the saved

      The biggest risk is the clock against these rows on one shared engine. At 05:18 count the rows closed: if 1a, 8 and 12 are not closed, start nothing new, close what is open, and write the report from that.
  Price: the count shows the clock, not whether the rows left can fit it — the cut is still my reading — and the rows cut at 05:18 are not recovered.

- ***proposed change to the pattern* — every piece names, at the start, the clock time by which it is abandoned, as well as its check.** This plan has a check for every row and an abandonment time for none, so the clock first speaks at the deadline. Price: a time set in advance can cut a piece that was one step from landing.

## Why

- my #13 and #14: the force is one shared engine and about six hours, and the rows include a merge another session owns; a general does not take every road, and when outmatched avoids the full battle — the 9–11 measurements and 1b are the roads left.
- my #2 and #9: make the unowned branch unbeatable (1a) and be first on the field with 13 while Codex is down; starting at 04:00 with nothing run is coming late to battle.
- my #8: victory, not duration — 1a green, 8 in, and 12 proved on memory_check is the win; many rows half-closed at 08:18 is not.
- my #15: the plan's title is the first fault, the general set on dying — holding every row risks all of them for the last one.
- my #17: the 05:18 count is the probe — reckoning the plan against the clock while rows can still be shed, instead of learning it at 08:18.

## What I need to know

- Is opencode this run's alone, or shared turn-by-turn with the other session? If shared, 3–8 are Claude-subagent work and 12 is the only call worth queuing for 04:00.
- Is the other session's `docs/TASK_TYPES_LEDGER.md` expected to be committed inside the six hours, and by whom? If not, 1b leaves the run entirely and every test runs on `merge/evaluator`, not master.
- Is row 2's change the same parser fix row 1 carries? If so, row 2 is not a separate row and 1a covers it.
- Is there a token ceiling for the six hours? If roughly 4M is affordable, 9–11 are resequenced after 12 rather than deferred; if not, the deferral is forced.
