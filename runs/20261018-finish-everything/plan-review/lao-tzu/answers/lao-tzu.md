I'll read the brief first.
# 老子 (Laozi) — is the 6-hour plan's order right, what to defer, and the biggest risk?

## Answer

**CHANGE**

**1. Item 1 must not be the gate (table row 1, "Done when").**

- Current: `the master merge itself waits only for the other session's uncommitted docs/TASK_TYPES_LEDGER.md (safety bound) — done the moment it is committed`
- New: `the master merge is the last thing this run does and gates none of it; this run never commits, stashes or overwrites the other session's docs/TASK_TYPES_LEDGER.md; if it is still uncommitted at 07:58 the run ends with merge/evaluator green and master untouched, and the report says so`

Price: if the other session commits early, the master merge is done at the end instead of the start — one merge commit late, no other work delayed.

**2. The order (How it runs).**

- Current: `One workflow per item or pair of items, in the order above (sequential; opencode never twice at once)`
- New: `One workflow per item or pair of items, in this order: 1's branch only, 2–8, 12, 11 on paper with no run, 13 in two batches, 9 and 10 only if 12's verdict shows a gap, 1's master merge, 14 (sequential; opencode never twice at once); the engine list is re-checked at 04:00 before item 13, and any crossing hold it can no longer staff — tests by one engine, code by another, review by a third — waits rather than takes one engine for all three`

Price: if 12's verdict shows the evaluator cannot judge memory_check at all, 9 and 10 return late and 13 loses its first batch.

**3. Do not measure 9 and 10 (table rows 9 and 11, "Done when").**

- Current (row 9): `experts' design applied, or kept open with a reason`
- New: `kept open with the reason and what buying it would cost recorded; applied only if item 12's verdict shows a state memory_check cannot be judged in today`
- Current (row 11): `experts advise; the main agent decides provisionally`
- New: `decided on paper from the mutants already recorded, with no new run; if the recorded evidence does not settle it, it stays open and says so`

Price: about 2M tokens and roughly two hours of the box are not spent; if the three runs share one evaluator run rather than one each, this deferral costs nothing and row 9 should be read as already decided.

**4. Cap the unbounded middles (table rows 3 and 13, "Done when").**

- Current (row 3): `the accepted ones reproduced red and fixed`
- New: `every one of the 17 carries a judge mark, the accepted ones reproduced red and fixed at most three per batch, the rest left as marked findings`
- Current (row 13): `each marked, under today's R12.2, as evidence (no choice needed) or a real failure with its top fix applied`
- New: `each marked in two batches, each batch done when every insight in it carries one of the two marks; the second batch starts only if the first found a real failure`

Price: some accepted findings and some old insights will end the run unmarked-by-fix but marked — the run reports the counts instead of pretending.

**5. Schedule the end (table row 14, "Done when").**

- Current: `written at the end of the time, with every provisional decision and what waits for the owner`
- New: `written at 07:58 whether or not the backlog is finished — at 07:58 the run starts no new item — with every provisional decision and what waits for the owner`

Price: 20 minutes of backlog time at the end of the box.

**6. Proposed change to the pattern.** The pattern has no rule for work that touches something outside the run's own folder; today a safety bound ("never commit another session's work") reads as a wait. It should read as a fence: the run goes on and reports what it left alone. Cost: EJ writes one clause in the run template.

## Why

Biggest risk: the run's first item is the only thing anyone else is holding, so six hours hang on another session's clock — and gripping it is how you lose it, my #4; the usable part is the empty space around it, my #17. The one check: every hourly progress line carries per item one of `done` / `not started` / `waiting on another session`, and the run is judged at fault if any line shows item 1 waiting while 2–8 have not started.
Three 1M-token runs to decide two design choices is a cup filled to the brim; stretch the one you keep (12) before you buy the ones you may shrink (9, 10), my #12 — a full cup is not as good as stopping, my #3.
"The accepted ones" and "each marked" have no end of their own; in a box with one engine at a time they swallow it. Split at a whole batch, so a stopped batch is still whole — careful at the end as at the beginning, my #7.
A report written "at the end of the time" is written last and worst, and it is the only thing EJ reads.
My reading, not a rule: knowing what the evaluator returns for memory_check today would decide 9, 10 and 11 by itself — to know that I do not know is best, my #8.

## What I need to know

- Whose session holds `docs/TASK_TYPES_LEDGER.md`, and whether it will be committed before 04:00. If yes, change 1 costs nothing extra; if it will not be committed at all, master should be struck from the run, not deferred.
- Whether items 9, 10 and 11 each need their own full run, or share one. Three shared runs make change 3 the whole saving; three separate ones make it two hours.
- What the evaluator returns for memory_check right now. If it already returns five states, 9 is finished and 10 and 11 leave the run, which buys back the second batch of 13 and a second memory_check run.
- How many of the 17 findings are likely to be accepted. If most of them are, row 3's fixing half is out of the run whatever the cap says.
