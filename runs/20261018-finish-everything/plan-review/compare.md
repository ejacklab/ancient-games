# Six experts — review the 6-hour "finish everything" plan before it runs (APPROVE or CHANGE)

Question: `runs/20261018-finish-everything/plan-question.md`; plan: `runs/20261018-finish-everything/plan.md`.
Labels: *quoted* (from an answer), *my reading*, *not measured*. This file compares; the main agent decides.

**A fact that changed after the brief was written (measured by me, 02:27, with git):** master now holds
`76596fa Merge build/evaluator and fix/evaluator-parser` (02:24:51) and `16d465d memory_check F3: Fails if written
as one case without commas…` (02:26:24); `git merge-base --is-ancestor` says both `build/evaluator` and
`fix/evaluator-parser` are in master, and `docs/TASK_TYPES_LEDGER.md` is still ` M` in the working tree. The experts
were asked at 02:21, so every answer below treats item 1 as not yet merged. *My reading:* their item-1 advice may
already be overtaken; I have not checked whether 16d465d closes item 2.

| | Linus | 范蠡 | 孫子 | 老子 | Dave (rules + insights) | Dario (plain control) |
|---|---|---|---|---|---|---|
| Answer (one line) | CHANGE: preflight item 1, fixes 2–8 in dependency order, defer 9–11 and 13, item 12 once after the fixes | CHANGE: 2–8 first, item 1 prepared beside them, 9–11 decided on paper, defer 12 and 13 | CHANGE: split item 1 into branch/master, 13 first on Claude subagents, 12 right after 1a and 8, 9–11 written only, 05:18 clock count | CHANGE: master merge last and gating nothing, order 1-branch, 2–8, 12, 11 on paper, 13 in two batches, 9–10 only if 12 shows a gap, report at 07:58 | CHANGE: order 1–8, 12, 9–11, 13, 14; one test call per engine path before item 1; 9–11 written with a prediction; a stop time per item | CHANGE: item 3 after 8, 13 marking beside 4–8, no measuring run for 9–11, 12 the only ~1M run after a no-model dry run, 05:18 checkpoint |
| Main items used | #2 #3 #4 #5 #6 #7 #9 #11 #12 #13 #14 #18 #19 | #1 #3 #4 #7 #10 #13 #18 | #2 #8 #9 #13 #14 #15 #17 | #3 #4 #7 #8 #12 #17 | #1 #2 #3 #4 #5 #8 #9 #10 | — |
| Insights cited | — | — | — | — | `runs/20261016-time-monitor/insight.md#F-173e0190`, `runs/20261016-six-experts/insight.md#F-7f938bdf`, `#F-8ac06aae`, `runs/20261015-score/insight.md#F-1e90a8e1`, `runs/20261017-experts-speed-trial/insight.md#F-1ed514ad` | — |

## Where they agree

- **All six answer CHANGE.** *quoted* (each answer's `## Answer` line). Five engines answering one brief share the
  brief, so this is not six independent verdicts. *my reading*
- **No ~1M-token measuring run for items 9–11 inside the six hours — all six.** *quoted*
  - Linus: "Defer items 9–11 beyond the six-hour run."
  - 范蠡: "Items 9–11 decide provisionally without 1M-token benchmark runs."
  - 孫子: "a written recommendation per item … no 1M-token measurement inside the six hours"
  - 老子: row 11 "decided on paper from the mutants already recorded, with no new run"; row 9 "kept open with the reason"
  - Dave: "the design is written down with its prediction … kept open, not applied or measured inside these 6 hours"
  - Dario: "no separate measuring run for 9, 10 or 11"
- **Item 13's "top fix applied" over 42 insights is cut — all six, in different ways (see disagreements).** *quoted*:
  Linus and 范蠡 defer it; 孫子 "a fix applied only where its check is known, the rest listed as new backlog"; 老子
  "two batches … the second batch starts only if the first found a real failure"; Dave "top fixes are applied only in
  the time left before the report"; Dario "fixes are applied only in the time left after item 12".
- **Item 12 runs once, and after the fixes it measures — five of six (not 范蠡, not 孫子's timing).** *quoted*: Linus
  "after the required fixes among items 1–8 pass"; 老子 order "2–8, 12"; Dave "1–8, 12"; Dario 12 after 3 and 8. 孫子
  also runs it once, but earlier (below). 范蠡 defers it.
- **The master merge must not hold the rest of the run — five of six.** *quoted*: 范蠡 "Item 1 prepares in a worktree
  branch without blocking items 2–8"; 孫子 "1b … no gate on any other row"; 老子 "the master merge is the last thing this
  run does and gates none of it"; Dario "if that file is still uncommitted at the end, the report lists item 1 as
  waiting"; Linus agrees the risk is a wait ("item 1 either waits forever") but answers with a preflight before
  merging. Dave does not change item 1's gate; he adds "print the merge's exit code" from an insight.
- **A clock check before the deadline — four of six (孫子, 老子, Dave, Dario).** *quoted*: 孫子 "At 05:18 count the rows
  closed"; Dario "Checkpoint at 05:18"; 老子 "written at 07:58 whether or not the backlog is finished" plus hourly
  progress lines; Dave "before an item starts, the main agent writes its stop time". Linus and 范蠡 propose none.
- **A stop or abandonment time per piece, as a change to the pattern — 孫子 and Dave (Dario's 05:18 rule is per run).**
  *quoted*: 孫子 "every piece names, at the start, the clock time by which it is abandoned"; Dave "each piece gets its
  own stop time, not only the run as a whole".

## Where they disagree (side by side, quoted; never averaged)

**Item 12 — when, or at all**

| Linus | 范蠡 | 孫子 | 老子 | Dave | Dario |
|---|---|---|---|---|---|
| "Run item 12 once, after the required fixes among items 1–8 pass" | "Items 12 and 13 are deferred past the 6-hour window" | "Run 12 as soon as 1a and 8 close, ahead of 3–7" | "2–8, 12, 11 on paper" | "in the order 1–8, 12, 9–11, 13, 14" | "it starts only after the parser and `evaluation ingest` have run once on a stored verdict with no model call" |

**Item 13 — when, and how much**

| Linus | 范蠡 | 孫子 | 老子 | Dave | Dario |
|---|---|---|---|---|---|
| "Defer item 13 unless a named use case requires its marks"; if kept, a read-only worker in parallel | "[DEFERRED past 6h window to protect focus and engine limits]" | "run first, split across Claude subagents" | "13 in two batches", after 12 and 11 | after 9–11; "each marked … top fix named" | "may run beside the item 4–8 builds"; mark all 42 |

**Item 1 — what the run does about the other session's file**

| Linus | 范蠡 | 孫子 | 老子 | Dave | Dario |
|---|---|---|---|---|---|
| "have its owner commit it or move it to a preserved patch or worktree. Do not merge item 1 until one preflight check proves the edit is preserved" | "Items 2–8 run first. Item 1 prepares in a worktree branch without blocking items 2–8" | "1a … time-boxed to one hour, then left as it is"; "1b … owner-wait" | "if it is still uncommitted at 07:58 the run ends with merge/evaluator green and master untouched" | keeps item 1 first; "print the merge's exit code, and keep the branch's evidence in the worktree until the merge lands" | "the report lists item 1 as waiting and items 8–12 as built on merge/evaluator" |

*my reading:* overtaken in part — the merge is already on master (see the top of this file).

**The biggest risk, and the one check**

| | Risk (quoted) | Check (quoted) |
|---|---|---|
| Linus | "item 1 either waits forever or overwrites another session's edit" | "the phase-0 preflight catches both" |
| 范蠡 | no single risk named; "Measuring items 9–11 and running item 12 consumes ~4M tokens while Codex is capped" | none named |
| 孫子 | "the clock against these rows on one shared engine" | "At 05:18 count the rows closed: if 1a, 8 and 12 are not closed, start nothing new" |
| 老子 | "six hours hang on another session's clock" | "every hourly progress line carries per item one of `done` / `not started` / `waiting on another session`" |
| Dave | "an engine path that returns nothing while every build needs three engines" | "each engine path the run will use … gets one cheap test call; a path whose answer is empty … is dropped" |
| Dario | "one stuck engine … pushes item 12 and the report past 08:18" | "Checkpoint at 05:18: items 1–8 are each done or logged as not done" |

**Item 3 (the 17 unjudged findings)**

| Linus | 范蠡 | 孫子 | 老子 | Dave | Dario |
|---|---|---|---|---|---|
| no change named | no change named | no change named | "the accepted ones reproduced red and fixed at most three per batch" | "a judge step over the 17 saved findings, then tests-first → engine → verify" instead of `review-enhance` | "item 3 runs after item 8" |

**Items 9–10 after item 12**

| Linus | 范蠡 | 孫子 | 老子 | Dave | Dario |
|---|---|---|---|---|---|
| "If a named use case requires one, select exactly one … run it once" | decided provisionally on paper | "if roughly 4M is affordable, 9–11 are resequenced after 12" | "applied only if item 12's verdict shows a state memory_check cannot be judged in today" | "experts advise from item 12's verdict … kept open" | "applied after item 12 if time remains" |

## What each added that the others did not

- **Linus** — a pattern change: "verify that required lessons have reached the agent, copy every outside source into
  the run folder and cite that copy, label every fact separately with its file:line"; and engine routing "one
  coordinator workflow with six bounded expert roles, not six simultaneous calls". *quoted*. *my reading:* his
  "Reserve Codex for critical work before about 04:00" runs against the brief's fact that Codex is at 99% until 04:00;
  every "Current words" he quotes comes from the question's Facts, none from `plan.md`, and he asks "Can you paste
  `runs/20261018-finish-everything/plan.md`" — he likely answered without reading the plan (his engine was mcode, the
  fallback from Codex; *not measured*: his log holds only the answer, so I cannot see whether a read was tried).
- **范蠡** — the only one to defer item 12 as well as 13, trading backlog closure for "items 2–8 and provisional
  designs 9–11 finish cleanly". *quoted*
- **孫子** — run item 13 first on Claude subagents while Codex is down; run 12 ahead of 3–7; time-box 1a to one hour;
  asks whether row 2 is the same parser fix row 1 carries. *quoted*. He states the split's cost himself: "I have no
  measurement that the split is faster than one reader." *quoted*
- **老子** — a pattern change: a safety bound on something outside the run's folder "should read as a fence: the run
  goes on and reports what it left alone"; write the report at 07:58 and start nothing after it; re-check the engine
  list at 04:00; a crossing the engines cannot staff "waits rather than takes one engine for all three". *quoted*
- **Dave** — one cheap test call per engine path before item 1, and "An engine step whose output is empty is not
  done: it is rerun once on another engine, then reported"; write 9–11 with "its prediction (metric, expected result)
  for the next evaluator run"; move item 7 first if crossed-build-check has hit 580 s; from insight F-1e90a8e1, print
  the merge's exit code. *quoted*
- **Dario** — a dry run of the parser and `evaluation ingest` on a stored verdict with no model call before item 12;
  9–11 as one question file; checked that `build/evaluator` changes `docs/TASK_TYPES_LEDGER.md` (*quoted*; I did not
  re-check it); asks whether pushing a branch other than master is allowed, against the memory note "push master
  only". *quoted*

## What they need to know (merged; each with its options)

1. **Will the other session commit `docs/TASK_TYPES_LEDGER.md` inside the six hours, and by whom?** (Linus, 范蠡,
   孫子, 老子) — *my reading:* possibly moot, since the merge is already on master.
   - Before 04:00: item 1 lands as soon as it is ready.
   - Later in the window: the master merge goes at the end.
   - Not at all, or unknown: master leaves the run; every later item builds and tests on `merge/evaluator`.
2. **Is there token budget for more than item 12?** (范蠡, 孫子, Dave)
   - No: 9–11 are written only; item 12 is the one ~1M run.
   - One more ~1M run: measure one design (item 9) against item 12's verdict as the control (Dave).
   - About 4M: run 9–11 after 12 instead of deferring them (孫子).
   - Real-run measurements are required: items 3–8 are cut back to free engine quota (范蠡).
3. **Must item 12 run with 9 and 10 applied to count as the milestone check, and do 9–11 need one run each or one
   shared run?** (Dario, 老子, Linus)
   - Yes, applied first: 9 and 10 go before 12 and something else is dropped.
   - No: 12 runs on today's evaluator, and 9–10 are judged from its verdict.
   - One shared run: deferring 9–11 saves little (老子).
4. **What does the evaluator return for memory_check today?** (老子)
   - It already returns five states: item 9 is done; 10 and 11 leave the run.
   - It does not: as planned.
5. **Does O8 (item 11) change code or only rule text?** (Dario)
   - Rule text only: apply it before item 12.
   - Code: decide on paper and defer the change.
6. **Is opencode this run's alone, or shared turn by turn with the other session?** (孫子)
   - Shared: items 3–8 go to Claude subagents; only item 12 is worth queuing for 04:00.
   - This run's alone: as planned.
7. **Item 3: can `review-enhance` start from the 17 saved findings with no new review and no enhance phase, does it
   need Codex, and why were the findings left unjudged?** (Dave, Dario)
   - It can, without Codex: keep `review-enhance` for item 3.
   - It cannot: a judge step over the saved findings, then tests-first → engine → verify (Dave).
   - The judge's engine refused last time: the judge step runs on a different engine.
8. **Do items 4–8 run through crossed-build-check, and has any call hit the fixed 580 s?** (Dave)
   - Yes: item 7 moves to right after item 1.
   - No: item 7 stays where it is.
9. **Is row 2's change the same parser fix that row 1 carries?** (孫子) — *my reading:* commit 16d465d on master may
   bear on this; not checked.
   - The same: row 2 folds into row 1.
   - Different: row 2 stays a separate row.
10. **May a branch other than master be pushed?** (Dario)
    - Yes: push `merge/evaluator` as items land on it.
    - No (master only): items built on the branch stay local until the merge.
11. **How many of the 17 findings are likely to be accepted?** (老子)
    - Most: the fixing half of row 3 is out of the run whatever the cap says.
    - Few: row 3 as planned.
12. **Does a named use case need item 13's marks, or one of 9–11, before the deadline?** (Linus)
    - Yes: keep it, run once, label the result provisional.
    - No: defer it.
13. **For the main agent, not EJ: Linus asked for `plan.md` to be pasted.** *my reading*
    - Rerun Linus with the plan text in his brief.
    - Use his answer as it stands, read as advice on the Facts only.

## Check

- **Results given to this step:** all six usable; check pass for each. *quoted* (the workflow's task text)
- **What the check files say:** every `check.txt` reads `FAIL: 1 answers, 5 failure(s)`, and the five FAIL lines name
  the other five experts ("no answer file"); none names the folder's own expert. Each expert ran in its own subfolder,
  so the other five are absent by design, and the check steps logged them as ignored (`nodes/plan-review.progress.md`,
  02:22–02:26). *quoted* (files); *my reading* that this is a pass for the folder's own expert.
- **Engines (from each `status.json`):** *quoted*
  - Linus: mcode, `minimax/MiniMax-M3.1-Flash-Preview`, 90 s, exit 0 — **fallback from codex**: "codex has 1% left
    (20% or less)".
  - 范蠡: agy, `gemini-3.8-flash-medium`, 90 s, exit 0.
  - 孫子: dsh, `deepseek-flash (dsh headless profile)`, 94 s, exit 0.
  - 老子: opencode, `minimax-coding-plan/MiniMax-M3.1-Flash-Preview`, 46 s, exit 0; started 02:25:11, after the
    others (opencode runs one at a time). His answer file begins with a stray line, "I'll read the brief first."
  - Dave: claude, `claude-opus-5-5`, 220 s, exit 0.
  - Dario: claude, `claude-sonnet-5-5`, 124 s, exit 0.
  - No expert needed a rerun. Linus and 老子 both ran on MiniMax M3.1 Flash, through different harnesses, so they are
    not independent engines. *my reading*
- **What the check does not establish:** the check script (`six_experts.py check`) was written by Claude. It checks
  the sections and that each persona cites item numbers its list has (and Dave's insight ids). It does not establish
  that a rule was applied correctly, that the advice is good, or that an expert read `plan.md`. Linus's answer
  passes the check although it quotes none of the plan's lines. *my reading*
- **Not measured:** whether Dave's cited insight ids say what he reports, beyond the check script's id lookup;
  whether Dario's 02:21 claim about `docs/TASK_TYPES_LEDGER.md` holds.
