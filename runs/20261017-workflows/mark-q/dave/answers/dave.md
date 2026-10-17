# Dave — keep or remove `deadline wait --mark P`

## Answer
Remove `--mark P` (reading A), provisionally. Nothing in any run has ever used it, or `deadline wait` at all. The test suite does not test it. It was added in the same build as the marks that have now been removed. And the accepted time-up line already has the report written once the time is up.

This flips to keep (B), with a suite test added, if the owner wants the report finished **before** the deadline. Then an idle agent needs to be woken early. The only other way to do that is a `sleep` whose length the agent works out by hand, which is the kind of failure `F-a03fa5b3` recorded.

## How I decided
1. **What would settle it (my #1).** My #1 says: "Before answering, name the measurement or observation that would settle the question, and what result would make me change my answer." (`EJ's rule`)
   - The observation that would settle it is a time-boxed run where the agent sat idle past the point where it needed to start the report. Idle here means waiting on a workflow or an engine call, so it makes no Bash or file-write call and gets no clock line.
   - One such run, where the owner counts the late report as a problem, changes my answer to B.
2. **The data we already have (my #5).**
   - **Given in the brief:** `grep -rn "deadline wait --mark" runs/` finds none, and the time-monitor run used a plain background `sleep`.
   - **Measured by me:** I searched `runs/` with Grep. `deadline wait`, with or without `--mark`, appears only in spec text, briefs, review logs and this question's files. No run has ever used it as its timer.
   - **Measured:** the suite tests `deadline wait` once, without `--mark` (`guard/test/round10-deadline.test.ts:190`). No test passes `--mark`.
   - **Measured:** `--mark` has run exactly once, in the time-monitor reviewer's own check (`runs/20261016-time-monitor/nodes/review.log:4432–4444`).
     - It ran `--mark 50` against a 0.02-minute deadline and returned in 0.603 s, against a target of 0.6 s.
     - So it works. But the reviewer wrote that check, it is n=1, and it is not in the suite.
   - **Measured, where it came from:** `--mark P` was added in the same build as `--marks 50,80,100`.
     - The spec's T3 line then said "until mark P" (`review.log:496`). It now says "until P percent of it" (`guard/SPEC.md:552`).
     - But the code never read the deadline's list of marks. Then (`review.log:575–577`) and now (`cli.ts:221–223`) it accepts any percent from 1 to 100.
   - **What this data does not show:** whether any agent ever needs to be woken before the deadline. Nothing measured says yes or no.
3. **Use case first (the brief's rule; which use case it is, is my reading).**
   - The vision line is a clock line after every call, and a time-up line after the deadline.
   - An agent that is working gets the clock on every call and needs no timer. A timer only helps an agent that is idle.
   - For an idle agent, `deadline wait` with no flag already wakes it at the deadline. The time-up line it then sees says "stop trying, finish the report, and put what is open to the owner" (`SPEC.md:559–560`, accepted). So writing the report after the deadline already has a use case, without `--mark`.
   - `--mark` only serves a use case if the report must be done **before** the deadline. The method's line "stops at the last checkpoint that leaves time for the report" (`docs/WORKFLOW_DESIGN_METHOD.md:543`) leans that way.
   - The method line and the time-up line read differently. That difference is the open question below.
4. **Compare against a control (my #4).** My #4 says: "Compare a change against doing nothing or the current way; never judge a change on its own." (`EJ's rule`)
   - The current way is the clock on every call, plus either a plain `sleep` (as in the time-monitor run) or a `deadline wait` that wakes only at the deadline.
   - Keeping `--mark` means keeping a feature that has never been compared with that: it has zero uses, so nothing shows it does better.
   - Removing it takes the code back to the control.
5. **The owner's reason applies to this flag too (my reading).**
   - The owner removed the 50/80/100% marks because a fixed percent "is not able to well predict, specific when exploring solutions".
   - `--mark P` is also a fixed percent, chosen in advance. The agent chooses it, rather than the guard firing it, and that is reading B's point. But the number has the same weakness.
   - If an early wake is ever needed, how early depends on how long the report takes to write, not on a share of the time limit. That is a reason not to keep it as a percent just in case.
6. **How nature solves it (my #6), dropped by my #7.**
   - *Recall:* migratory birds start fattening before the season turns, cued by day length, so slow work is done by the deadline.
   - The same here: the report takes time, so the wake must come before the deadline.
   - The difference: nature tunes how early over many cycles with measured outcomes. We have zero uses to tune a percent from.
   - The key condition differs, so the analogy is not evidence. It only gives a name to the use case in step 3.
7. **Small and reversible (my #8).**
   - Both choices are small. Removing it touches `cli.ts` lines 45, 221–223, 227 and 242, SPEC T3, and the exported `skills/workflow-design/` copy (measured: a directory, not a link). One git revert would restore it.
   - Neither choice is hard to undo. While the data is zero, the one that is cheaper to carry wins.
8. **A small experiment beats argument (my #2).** The test that settles this costs nothing extra: the next time-boxed run that waits on background work. Arguing longer costs more than that.
9. **Insights used.**
   - `runs/20261016-time-monitor/insight.md#F-a03fa5b3`: a time the agent typed from recall was a year off, and only the guard's own check caught it.
     - This changed my answer from a plain "remove" to a conditional one.
     - If an early wake is needed, removing `--mark` leaves the agent to work out `sleep N` by hand, and nothing checks that N. In that case the guard should compute the wake time, so `--mark` stays.
   - `runs/20261016-time-monitor/insight.md#F-173e0190` (option 3: prove a code path with one cheap call before a run depends on it):
     - No run has used `--mark`, and no suite test covers it.
     - This added a cost to B: keeping it means adding a test.
   - No category was named. I chose these two from the time-monitor run, the run that built this code.
10. **The leftover rule: read, not given, so it does not decide.**
    - The main agent's memory notes record the owner's rule: "anything that existed only to serve that mechanism is dead."
    - Step 2 shows `--mark` never read the marks list, so it did not *only* serve them.
    - So that rule does not settle this by itself, which is why it came to the experts.

## What I need to know
- **Is the report due before the deadline or after it?**
  - If after, which is what the accepted time-up line says: remove `--mark`.
  - If before, which is what method 3.8 item 14's "leaves time for the report" suggests: keep it with a suite test, or replace it with a wake a set number of minutes before the deadline. The owner would choose that number, not me.
- **How common are idle waits in time-boxed runs?** That is, how often does the main agent wait on a workflow without making any calls? This has not been measured. If it never happens, neither form of `--mark` has a user.

## Costs and risks
- **Remove (A):**
  - An idle agent whose background work overruns is woken only at the deadline. Its report then lands late by however long the report takes to write, which is not measured (my #5, step 3).
  - If an early wake is wanted later, the agent's fallback is a `sleep` length worked out by hand, the kind of failure in `F-a03fa5b3` (step 9).
  - The CLI only reads the flags it asks for and does not reject others (`cli.ts:70–76`). After removal, an out-of-date instruction such as `deadline wait --mark 90` would quietly wait until 100% instead of failing.
    - Measured: only SPEC T3 and the CLI's usage text name `--mark` today, so the risk is small.
    - Rejecting `--mark` with a usage error would close it, at the price of one line and one test (my reading).
- **Keep (B):**
  - It keeps a flag with zero uses and no suite test. Its only proof is one reviewer check, n=1 (my #10, step 2).
  - As a percent, it has the weakness the owner named for the marks (step 5).
  - It looks like a leftover, so someone will ask about it again (step 10).
  - The price is one suite test (`F-173e0190`, step 9), and keeping the SPEC line up to date.
- **How sure I am:** low either way. My #10 says: "State the evidence behind each claim and its size: n=1 is a hint, not a law." (`EJ's rule`)
  - Uses: n=0. Proof that it works: n=1. Its origin rests on one build's history.
  - The answer rests on the use-case rule and on which choice is cheaper to carry, not on any measured benefit.

## How we would know I was right
- **Prediction, written down first (my #3):**
  - **Metric:** in the time-boxed runs after this one, count the idle waits that pass the point where the report needed to start, and record whether each report finished before or after the deadline.
  - **Expected:** none needs an early wake, because agents work through calls and get the clock line on each one.
  - **Stop:** the first time-boxed run in which the main agent waits on a workflow or an engine call without making calls of its own. Before that, the owner accepts or declines this decision at the end of this run.
- **I was wrong if** either of these happens:
  - such a run shows the agent idle past the point where the report needed to start, woken only at time-up, and the owner calls the late report a problem;
  - an agent works out a `sleep` by hand to wake early.

  Then restore `--mark` from git and add the suite test.
- **No uses is still a result (my #9).** If that run still shows zero uses, that confirms the removal.
- **Checking the removal itself:**
  - `grep -rn -- "--mark" .claude/skills/workflow-design/guard/src .claude/skills/workflow-design/guard/SPEC.md` finds nothing.
  - The existing `deadline wait` test (`round10-deadline.test.ts:190`) still passes.
  - If the reject line is added, `deadline wait --mark 50` exits with code 2.
