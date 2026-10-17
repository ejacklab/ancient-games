# Dave — May a scriptable procedure stay a page, and who decides

## Answer
Yes, but running rarely is not the test. A rarely-run script and a rarely-run page both decay (B10, B11 against C16, C18, C19). A procedure that could be a script may stay a page when the agent writing it, after trying the script, writes the comparison on the page: what the script costs to build (the try shows this) and to keep working between runs, against what it saves over the runs expected. The savings include effort, and also the steps a person following a page can miss or find out of date. The agent decides at the time of writing. Whoever follows the page next makes the comparison again, by trying the script first. The owner decides only if it is contested.

Proposed addition to W3.6, after "…the project owner decides if it is contested.":

> A procedure a script could do may stay a page when the agent writing it, after trying the script, writes on the page why: what the script would cost to build and keep working, against what it would save over the runs expected, counting the steps a reader of a page can miss or find out of date — that it runs rarely is not by itself a reason. Whoever follows that page next makes the comparison again, trying the script first.

One more change, in `fails_if`: "with no written reason" becomes "with no written comparison". Without it, a bare "runs rarely" would count as a written reason and pass.

## How I decided

1. **What would settle it (my #1).** Two observations would settle it. First: does a page followed a second time have more missed or out-of-date steps than a script run a second time has breaks? Second: did the agent who chose the page predict that second run? If pages followed again turn out as sound as scripts run again, I would accept "runs rarely" as a reason. Nothing I was given measures either, so this answer is a default, not a finding.

2. **Use the data first (my #5).**
   - No source gives a measured break-even frequency (A9).
   - The sources that weigh scripting all do it as a comparison: cost against benefit (A1), and build time against runs × time saved (A5). That matches the owner's rule of comparisons, not numbers. So the test is a comparison, and I give no number.
   - The vision side points the same way. procedure-to-skill (line 15) treats a prose page as a summary of the procedure that drifts, and W3.6 bans copies of procedures. So the script stays the default, and a page is the exception that needs a reason.

3. **Always run a control (my #4).** The page is not a free "do nothing" option. Rarity raises the costs on both sides:
   - **The page's costs.** It needs keeping: runbooks go out of date unless time is scheduled to update them (C16). It also has an error cost per run, which grows when runs are rare. Skills fade when unused (C18, secondary notes), people fall out of practice (C19), and skipping a step is a common maintenance failure (C20; C21 reported).
   - **The script's costs.** Rarely-run automation is fragile because feedback comes late (B10), and it dies when the code it covers changes and nobody keeps it in sync (B11).

   So rarity does not pick a side. What the sources tie scripting to is repetition:
   - Toil is defined partly by repetition (A4).
   - Limoncelli adds scripts as the process is run again and again (A7, secondary).
   - procedure-to-skill excludes a throwaway procedure (its line 3).

   That is why the reason must be the comparison, with 孫子's test — will it run again on ground that stays still — as its main input.
   - Insight used: `runs/20261016-integrate-r11-r13/insight.md#F-2cdebf3b` (same cause as `#F-b7c8635f`). A contract written as prose was checked as a different subset by each reader; one written as a table was implemented right. This changed my answer: the page's cost side now names the steps a reader can miss. It is n=2 in one run, about specs, not procedures, so a hint only (my #10).

4. **A small experiment beats an argument (my #2).** W3.6 already makes the agent try the script first. That try is the experiment: it measures the build cost instead of guessing it. Only the keep cost and the expected runs remain predictions.

5. **Write the prediction down first (my #3).** The expected runs and the keep cost are predictions. They are proved right or wrong when someone follows the page again. That person reads the page, not the old task's `state.md`, which is where the `levels` key puts a SHOULD reason. So the reason belongs on the page. This is a *proposed change* to where this one SHOULD's reason lives. Its price is listed under costs.

6. **Small and reversible, then scale (my #8).** Both directions can be undone: a page can become a script, and a script can be deleted. So the agent can decide without the owner, and the next run is the natural point to reverse. That is why the second sentence gives the re-decision to the next follower rather than to the owner or a schedule.
   - 孫子 makes the "should not" an owner's value. I agree the owner owns the rule, but one page's case is reversible and gets checked at its next run (my reading).
   - Linus called this a cost judgement, not a technical impossibility (`linus.md:19`). The first sentence writes that judgement down.
   - Insight used: `runs/20261016-four-experts-what-counts-as-change/insight.md#F-8243a18f, F-96578c5b`. Criteria text typed by hand twice within an hour repeated the same mistake. Option 2 made a tool write the line, which now exists (*read*: `.claude/skills/workflow-design/guard/src/criteria.ts:188`, `TESTS_CRITERION`). This changed my answer: in this project, the second manual repeat is where the cost of doing it by hand showed and the tool got built. So the next run is the moment to re-decide. n=1 pair.

7. **Ask how nature solves it, and check the analogy (my #6, #7).** Adaptive immune memory is built during the first encounter, before the body knows whether the pathogen will return, and it fades without re-exposure. This is *recall*, not a source of this run, and it does not decide anything.
   - **Same:** recurrence is unknown, keeping the memory costs something, and it decays without exercise.
   - **Different:** the body cannot know a pathogen will not return. An agent sometimes can, for example with a one-off migration — and that is exactly the case where a page wins.

   The key condition differs exactly where the page decision is made, so I drop the analogy there. It only agrees with W3.6's existing "try the script first" when recurrence is unknown, and with "exercise it", which the research already gives (B13, B14, C16).

8. **Report what failed (my #9).** Suppose a page was kept because it "will not run again", and then it is followed again. That is a failed prediction. It gets recorded as one in that run's `state.md`, not just used as a reason to script it now.

9. **How sure I am (my #10).** Not very. Most of A–C was opened and checked. But the contrast that a page drifts with no warning while a run script fails at a known step is *reported*, not measured (D). No source measured a break-even point (A9). The repo insights are n=1–2 and used by analogy. A SHOULD default is the right strength for evidence of this size.

## What I need to know
- **Are any of these procedures irreversible** (a delete, a failover, a data migration)? If yes, a page instead of a script for one of those goes to the owner before it stays. A missed step there cannot be undone, so finding out at the next run comes too late (my reading). If no, the answer stands.
- **Has any page procedure in these projects already been followed a second time,** with a record of missed or out-of-date steps? If yes, that is the data step 1 asks for, and it should be read before this text is fixed (my #5). It was not given.
- **Does putting the reason on the page break the owner's "product docs, no history" rule** (*recall*, house memory)? I read it as a current reason, not history. If the owner reads it as history, the reason goes back to `state.md`. The second sentence then loses its trigger, because the next follower would not see it.

## Costs and risks
- **The reason on the page** (my #3, step 5) costs a line of reasoning on a `docs/` page. It also departs from the `levels` key, which puts SHOULD reasons in `state.md`, so reasons would live in two places in one design.
- **Re-deciding at the next run** (my #8) costs the next follower one try of the script. The cost is limited: a try that works ends the question, and one that fails costs the try and a line.
- **A self-serving comparison** (my #1). The reviewer can check that the reason is a comparison, not that it is right. A wrong "will not run again" is caught only if the page is run again — and if it never is, the mistake cost nothing.
- **Choosing the script does not end the cost** (my #4). A rarely-run script that nothing runs on a schedule breaks unseen until the day it is needed (B10, B11; B15 reported). W3.6's "external check" protects it only if something runs that check. This is outside the question; I flag it.
- **Weak evidence** (my #10). There is no measured break-even, the decay contrast is reported, and the insights are about specs and criteria text, used by analogy.

## How we would know I was right
- **Recorded now, before results (my #3).** For each page kept under this clause that is followed again, the follower records three things at that run:
  - that the "will not run again" prediction failed;
  - whether any steps were missed or out of date;
  - whether the script try succeeded.
- **The control (my #4).** Compare against the scripts written under W3.6 in the same period: did they break at their next run?
- **What would prove me wrong (my #1, #9).** If pages followed again show no more missed or out-of-date steps than the control scripts show breaks, I was wrong to charge the page that cost, and "runs rarely" can become a valid reason.
- **What would narrow the clause.** If, by the review date, pages followed again outnumber pages never followed again, the agents' predictions are poor. The clause should then shrink to known one-offs only.
- **Stop date.** The owner's next review of W3. The owner sets that date; I do not invent one.
- **A check the reviewer can make immediately.** Every page kept under this clause carries a comparison, and none gives only "runs rarely".
