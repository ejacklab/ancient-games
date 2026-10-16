# Dave — Can a procedure always be a script, and who decides

## Answer
No. A procedure cannot be a script when one of its steps cannot be written as a command whose result an outside check can confirm. That happens in two cases: a step a person has to do, and a step where the next move depends on judging what was just seen. The agent writing the procedure decides at the moment it writes the procedure down, and it decides by trying to write the script. If the attempt fails, the procedure becomes a `docs/` page that names the step that could not be scripted and calls scripts for every other step. The project owner decides only when the decision is contested or comes up at review.

## How I decided
1. **What would change my mind (my #1).** One kind of procedure would change my answer: one where every step has a checkable command, yet a script is still the wrong home for it. I cannot name such a procedure. I can name procedures that have a step with no checkable command, so "always a script" is wrong.
2. **The test is an experiment, not an argument (my #2).** The question "can this be a script?" costs about as much to argue as it costs to try. So the test an agent applies is to try. Write `procedure.sh` plus an external `verify.sh`, the shape the `procedure-to-skill` skill already uses, and run it once.
   - If it runs end to end and the external check passes, the procedure is a script.
   - If some step cannot be written as a command with a checkable result, that step is the reason it is not a script.
   - The kinds that fail the test:
     - **(a) A person's action:** an approval, a login with a second factor, a physical change.
     - **(b) A branch on judgment:** the next step depends on interpreting output. Debugging is the clear case. `procedure-to-skill` says it is "NOT for a fact with no steps … or a procedure specific to one throwaway task", and the `e2e-probe` skill excludes "exploratory debugging where the next step genuinely depends on judgment".
   - A procedure run only once is not a procedure in W3.6's sense. It is task work.
   - A mixed procedure becomes a page that calls the scripted parts. It does not copy their steps.
3. **Borrow from nature (my #6).** People have the same split: procedural memory, which runs without thought (riding a bike), versus deliberate control. A skill becomes automatic through repetition in a stable setting. A new or ambiguous situation is handed back to deliberate thought. The mechanism to borrow: what repeats with the same steps becomes automatic (a script), and the step that meets something new stays deliberate (the page names it).
4. **Check that the analogy fits (my #7).**
   - Same: the deciding conditions are repetition plus a stable setting, and the same conditions decide scriptability.
   - Different: the brain promotes a skill gradually and with no one choosing, while a repo needs someone to decide and write the script.
   - The key condition (a stable setting means automatic, a new situation means deliberate) carries over, so I keep the analogy. It does not tell me who decides; step 6 does that.
5. **Use the data I have (my #5).** Nothing about procedures here is measured. The brief says no lint checks W3.6.
   - What I observed by listing files, not by reading their contents: two procedures already exist as scripts. One is `~/.claude/skills/stage2a-e2e-dev116/scripts/procedure.sh` plus `verify.sh`. The other is the `workflow-design` skill's `scripts/` folder.
   - I saw no file name in `docs/` that marks a page as a procedure or runbook.
   - This shows that scripted procedures already happen in this repo. It does not show how many procedures fail the test.
6. **Compare against the current way (my #4).**
   - Today's control is `unassigned`: nobody decides, and nothing checks.
   - Making the owner decide every time would add a review for every procedure, while W3.6 is only a SHOULD.
   - The agent that tried the script holds the evidence: the failed step. So the agent decides, and the owner reviews. W3.6 already carries `check: reviewer`, so the owner's role is in place and needs no new mechanism.
   - The decision happens when the procedure is first written down. That is the moment an agent would otherwise write prose.
7. **Small and reversible first (my #8).** Apply the test to the next procedure that gets written, one path only, before re-checking any existing ones.
8. **Report the failed attempt (my #9).** The failed script attempt is the record that it could not be a script. The page states the step that failed and why. A page with no named step reads as a skipped attempt, not as a result.
9. **How sure I am (my #10).** I am about as sure as an untested proposal allows. My earlier view (agent decides, owner if contested) was one opinion, not data. This answer adds a test but no measurement.

**What W3.6 should say** (proposed): *"A procedure lives in the repo as a script with an external check; where a step cannot be a command with a checkable result — a person's action, or a choice that depends on judging what was seen — it is a page in `docs/` that names that step and calls scripts for the rest. The agent writing the procedure decides by trying the script first; the project owner decides if it is contested."* `who_decides` becomes *"the agent writing the procedure, by attempting the script; the project owner if contested."*

Linus's "one thing" point (that W3.6 bundles three things) is not something my rules decide. I answer only the placement sentence.

## What I need to know
- **Does a script that pauses for a person count as a script?** One example is a script that stops for a typed confirmation before an irreversible step.
  - If yes, kind (a) shrinks to steps a script cannot even prompt for, such as a physical action or a web login.
  - If no, every procedure with an approval step becomes a page.
- **Should the owner review every procedure that ends up as a page, or only contested ones?**
  - If every one, the owner's cost grows with the number of pages.
  - If only contested ones, the agent's "could not script it" stands unless someone objects.

## Costs and risks
- **Trying first costs agent time (my #2).** Procedures that turn out unscriptable cost a failed attempt before the page is written. That is the price of having evidence instead of an opinion.
- **The agent judges its own case (my #4).** An agent may pick the cheaper path (prose) and call a step "judgment". Two mitigations: the page must name the specific step, and the owner reviews. Nothing automated catches a weak reason.
- **The mixed case can slide into copying (my #9).** A page that "calls scripts for the rest" may start to repeat their steps, which is exactly what W3.6's `fails_if` forbids.
- **A script without an external check still drifts (my #1).** A script that only reports its own exit code is a weaker claim than "it worked", as `procedure-to-skill` says. The test needs the outside check or it proves little.
- **The analogy could mislead (my #7).** The brain promotes skills gradually and without anyone choosing. Repos do not. I used the analogy only for which kinds of step stay deliberate, not for timing or for who decides.
- **No measurement behind any of this (my #10).** This is a proposal at n=0.

## How we would know I was right
- **Prediction, written before any result (my #3).** Apply the test to new procedures. Every procedure that ends up as a `docs/` page names a step of kind (a) or (b), and no page's stated reason is something a command could have done.
- **Metric.** For each page, the step it names. Each page is checked one way: a reviewer other than the writing agent tries to script that step.
- **Control (my #4).** Compare this with the current way, where agents write prose or scripts with no test. Count how many pages from the current way contain steps a reviewer can script.
- **What would prove me wrong (my #1, my #9).** Either of these:
  - a reviewer scripts a step that the page called unscriptable;
  - a procedure that passes the test still needs a page.
- **Stop date.** Not given to me. EJ sets it.
