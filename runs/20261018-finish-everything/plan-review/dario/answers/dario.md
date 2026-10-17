# Answer — review of the 6-hour finish-everything plan

## Answer
CHANGE

1. **Order: item 3 after item 8 (answers question 1).** The edits below also put item 13's marking beside the 4–8 builds.
   - Current: `One workflow per item or pair of items, in the order above (sequential; opencode never twice at once)`
   - New: `One workflow per item or pair of items, in the order above, except that item 3 runs after item 8 (sequential; opencode never twice at once; item 13's marking, which uses only Claude subagents and writes only under runs/20261018-finish-everything/, may run beside the item 4–8 builds)`

2. **Defer applying 9 and 10, and run no separate measurement for 9–11 (question 2).**
   - Current, item 9: `experts' design applied, or kept open with a reason`
   - New, item 9: `experts' design written down; applied after item 12 if time remains, otherwise kept open with a reason; no separate measuring run for 9, 10 or 11`
   - Current: ``` `experts-decide` for 9–11 and the owner-only questions```
   - New: ``` `experts-decide` for 9–11 as one question file, and for the owner-only questions as a second```
   - Current, item 12: `(cost recorded)`
   - New, item 12: `(cost recorded; the only ~1M-token run in the plan; it starts only after the parser and `evaluation ingest` have run once on a stored verdict with no model call)`

3. **Item 13 marks all 42, and fixes wait (question 2).**
   - Current: `or a real failure with its top fix applied`
   - New: `or a real failure with its top fix written down; fixes are applied only in the time left after item 12`

4. **Item 1 does not depend on another session's commit.**
   - Current: `— done the moment it is committed`
   - New: `— if that file is still uncommitted at the end, the report lists item 1 as waiting and items 8–12 as built on merge/evaluator, not on master`

5. **Biggest risk and the one check (question 3).**
   - Risk: the one-lane chain has no stop per item, so one stuck engine (opencode busy, Codex until 04:00, dsh empty) pushes item 12 and the report past 08:18.
   - Check: add this sentence at the end of "How it runs".
   - New: `Each item's start and end time goes in runs/20261018-finish-everything/progress.md. Checkpoint at 05:18: items 1–8 are each done or logged as not done; if not all done, items 9–11 get only the experts' answer, item 13 is marking only, and item 12 runs as soon as items 1 and 8 are done.`

## Why
- Time is the biggest risk, and the estimate is mine, not measured. Items 1–8, three expert rounds and 42 readings in one lane likely run past six hours, so the tail (item 12 and the report) gets cut.
- Four ~1M-token runs (9, 10, 11, 12) are too many for six hours. One run at 12 loses the ability to credit a result to one design choice, and that is the cheaper loss.
- Items 4–8 have known checks and need no Codex, so they bank wins while Codex is down until about 04:00. Item 3 still comes before 12, so the evaluator sees the fixed tool.
- I checked at 02:21: `build/evaluator` changes `docs/TASK_TYPES_LEDGER.md`, which is modified in the working tree, so the master merge depends on another session. The plan doesn't say where items 8–12 land meanwhile. I did not check whether `fix/evaluator-parser` or any of items 2–8 touch the other uncommitted files.
- Item 13's "top fix applied" over 42 items is unbounded, since each fix is a build with a three-engine crossing. Marking is cheap and read-only.

## What I need to know
- Does item 3's `review-enhance` need Codex for its judging or crossing? If it works without Codex, change 1 is optional; I would still keep it.
- Is pushing a branch other than master allowed? My memory notes say "push master only", but the plan says "pushed as each item lands" while items 8–12 can't reach master until item 1 does.
- Must item 12 run with the five states and use cases (items 9 and 10) applied to count as the milestone check? If yes, apply 9 and 10 before 12 and drop something else.
- Does the O8 decision (item 11) change code or only rule text? If it is only text, apply it before item 12.
