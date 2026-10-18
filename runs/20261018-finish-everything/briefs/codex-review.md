# Brief — read-only review of four commits (run 20261018-finish-everything)

You are a reviewer. Read only: change no file, run no command that writes. Use relative paths from the repository root.

## What to review
Four commits on master, each against its own written contract:
1. `7020438` — memory-check, 12 review findings fixed. Contract: `memory_check/VISION.md`, `memory_check/USE_CASES.md`,
   `memory_check/REQUIREMENTS.md`, and the accepted findings in `runs/20261018-finish-everything/mc-findings/accepted.md`.
   C6 is fixed in memory_check on purpose: `docs/index-md/REQUIREMENTS.md` B2.5 keeps an inactive entry's problem a
   warning in `tools/memory_index.py`.
2. `67100bd` — guard Round 20 and 20b. Contract: the sections "Round 20" and "Round 20, after its review" at the end of
   `.claude/skills/workflow-design/guard/SPEC.md`.
3. `519eae8` — the evaluator's judged-merge removes its /tmp judge folder. Contract:
   `runs/20261018-finish-everything/briefs/ev-cleanup-code.md`.
4. `9f191b4` and `16d465d` — memory_check spec text changes so the evaluator's parser reads them (`docs/evaluator/DATA.md`
   § E1 rules 4 and 7).

`git show <commit>` gives each diff.

## Find
Places where the code breaks a line of its contract or a Fails-if, or breaks behaviour its contract calls unchanged;
and tests that would pass with the defect present. For each finding: the contract line quoted, file:line, the problem,
and an input that shows it. Say what you checked and found nothing in. An empty list is a fine answer.

## Lessons
- When a change sends new cases into an existing code path, list that path's early returns and exemptions first, and
  test each with one of the new cases.

## Answer
Your final message is the review: a heading `## Findings`, then numbered findings or "none", then `## Checked`.
