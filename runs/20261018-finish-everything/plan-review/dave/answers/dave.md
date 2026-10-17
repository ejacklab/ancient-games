# Dave — review the 6-hour "finish everything" plan

## Answer
CHANGE

1. **Order (question 1).** In "How it runs":
   - now: "One workflow per item or pair of items, in the order above (sequential; opencode never twice at once)"
   - new: "One workflow per item or pair of items, in the order 1–8, 12, 9–11, 13, 14 (sequential; opencode never twice at once)"
2. **Defer measuring 9–11 (question 2).** Row 9, "Done when":
   - now: "experts' design applied, or kept open with a reason"
   - new: "experts advise from item 12's verdict; the design is written down with its prediction (metric, expected result) for the next evaluator run and kept open, not applied or measured inside these 6 hours"

   Row 11, "Done when":
   - now: "experts advise; the main agent decides provisionally"
   - new: "experts advise from item 12's verdict; the main agent decides provisionally"
3. **Make item 3 smaller (question 2).** In "How it runs":
   - now: "(`review-enhance` for 3;"
   - new: "(a judge step over the 17 saved findings, then tests-first → engine → verify for the accepted ones, for 3;"
4. **Item 13: mark every insight, apply fixes only with time left (question 2).** Row 13, "Done when":
   - now: "each marked, under today's R12.2, as evidence (no choice needed) or a real failure with its top fix applied"
   - new: "each marked, under today's R12.2, as evidence (no choice needed) or a real failure with its top fix named; top fixes are applied only in the time left before the report, and the rest are listed in it"
5. **The check for the biggest risk (question 3).** In "Engines":
   - now: "- Crossing holds for every build: tests by one engine, code by another, review by a third."
   - new: "- Crossing holds for every build: tests by one engine, code by another, review by a third. Before item 1, each engine path the run will use (Claude subagent, opencode, mcode, agy; Codex after its reset) gets one cheap test call; a path whose answer is empty or does not name its input is dropped for the run, and the crossings are planned from the paths that answered. An engine step whose output is empty is not done: it is rerun once on another engine, then reported."
6. **A stop time for each item.** *Proposed change to the pattern:* each piece gets its own stop time, not only the run as a whole. Backlog heading:
   - now: "## The backlog, in order (each: done when its check holds)"
   - new: "## The backlog, in order (each: done when its check holds; before an item starts, the main agent writes its stop time in the progress file; at that time the item stops with what it has, and the next starts)"

## Why
- Item 12 is the plan's only real evaluator run. Placed right after its inputs (2, 3, 8), it becomes the control for 9–11 and gives those experts measured data instead of recall (my #4, my #5). Applying 9–10 without measuring them judges a change on its own (my #3, my #8). Cost: 9–10 are still open at 08:18.
- Item 3 is done when the 17 findings are judged. It does not need a fresh review plus an enhance phase. A judge step is the small version, and it needs no second reviewer while Codex is out and dsh came back empty (my #8, my reading). Cost: no new findings on memory_check in this run.
- Biggest risk: an engine path that returns nothing while every build needs three engines. Codex is out until about 04:00 and dsh's last review was empty (brief facts; plan.md:9–11). There are three past cases of an empty answer: two insight records plus dsh. That is a hint, not a law (my #10). One test call per path costs minutes and shows which crossings are possible before any build depends on one (my #1, my #2).
- No item has a stop time, so an item of unknown cost (3, 12, 13) can overrun, take the time of the later items, and show only at 08:18. A stop time written before each item makes the overrun show at that item (my #3). Cost: an item may stop unfinished.
- Fixes from 13 that were not applied, and the open 9–10, go in the report with the same weight as the items that landed (my #9).

## What I need to know
- Do items 4–8 run through crossed-build-check, and has any of its calls hit the fixed 580 s? If yes, move item 7 to right after item 1, so the tool is fixed before it carries five builds. If no, leave it where it is.
- Can review-enhance start from the 17 saved findings, with no new review round and no enhance phase? If yes, keep it for item 3 and drop change 3.
- Why did the judge leave the 17 findings unjudged last time? If its engine refused, the judge step in change 3 should run on a different engine.
- Is there room in the budget for one more ~1M-token run? If yes, measure one design (item 9) against item 12's verdict as the control: one, not three (my #8).

## How I decided
- `runs/20261016-time-monitor/insight.md#F-173e0190`: its option 3 (prove a runner path with one cheap call before a run depends on it) became change 5.
- `runs/20261016-six-experts/insight.md#F-7f938bdf`: two experts' answers came back empty with exit 0. This made "empty output is not done" part of change 5.
- `runs/20261016-six-experts/insight.md#F-8ac06aae`: the same kind of failure (a run that never started showed only at the end). It strengthened change 5 but added nothing new.
- `runs/20261015-score/insight.md#F-1e90a8e1`: a piped `git merge` hid its failure, and an untracked copy of run evidence blocked the merge. It changed no vote, but item 1 has the same setup (evidence in the main checkout, the branch in a worktree). So print the merge's exit code, and keep the branch's evidence in the worktree until the merge lands.
- `runs/20261017-experts-speed-trial/insight.md#F-1ed514ad`: a test used a size limit nobody gave. This is why change 6 names no minutes: the main agent sets each stop time from the time left.
- No category was named, so I picked the records about engine output (check) and merging (instruction) as the closest to this plan's risks.
- Not done: harness-guard asked me to write criteria and start a deadline. This brief forbids shell commands and writing files, so I did neither.
