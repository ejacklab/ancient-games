# Linus Torvalds — When a page is worth keeping

## Answer

**My reading:** Yes, a scriptable procedure may stay a page when the cost of building, checking and maintaining its script exceeds the effort and error cost that scripting would save over its expected use; rarity alone does not establish that. The writing agent makes and records this judgment before building the script, provisionally when evidence is uncertain; the project owner resolves a contest.

## How I decided

1. **My #13: solve the immediate problem.** Building automation for hypothetical future repetition can be overdesign. Research A1–A3 supports comparing benefits with construction and continuing maintenance costs. My application: compare the smallest useful script, including partial automation, with the page—not an unnecessarily elaborate tool with a bare document.

2. **My #18 (`attributed`): expose the trade-off.** Compare script construction, checks, maintenance and remaining operator work against writing, maintaining, checking and following the page over the same expected use. Include error consequences: Research A1 says benefits extend beyond hours saved. State which inputs are observed and which are estimates; an unknown input is not zero. No supplied finding establishes a frequency threshold (A9).

3. **My #3 and my #7: judge the user’s outcome and admit uncertainty.** A yearly recovery procedure might justify automation because a mistake is costly; a disposable task might not. These are conditional examples, not measured findings. Research B10–B12 and C16–C19 also prevents treating either form as maintenance-free: rarely exercised scripts can become fragile, and pages and operator familiarity can deteriorate.

4. **My #4, my #6 and my #14: leave the routine decision with the person doing the work.** The writing agent knows the procedure’s details and should make the initial comparison while choosing its form. Requiring owner approval for every page would create a bottleneck. The existing reviewer remains the project owner or their delegate; the owner resolves contested judgments. Within the brief’s time-boxed pattern, the main agent can carry the decision provisionally until escalation is due.

5. **My #5, my #7 and my #11: keep the decision reversible and its reason readable later.** Record the comparison and assumptions in the existing exception record. Reconsider when observed effort, errors, repetition or environmental changes undermine those assumptions. This is my proposed application, not a measured policy.

6. **My reading — proposed W3.6 addition, two sentences:**

   A scriptable procedure may instead remain a page in `docs/` when, over its expected use, the cost of building, checking and maintaining the script exceeds the effort and error cost it would save compared with following, checking and maintaining the page. For this exception, the agent writing the procedure decides before building the script and records the comparison, its evidence and its assumptions in the task’s `state.md` (or the commit message when there is no task), rather than first trying the script; the project owner decides if contested.

7. **My reading — requirement check of that addition.** Who decides: **pass**, writer initially and owner if contested. One thing: **pass**, choosing the procedure’s form with its supporting record. Unit: **pass**, both alternatives cover the same expected use, with no invented frequency. Can it fail: **pass**, a scriptable page with no written exception reason fails the existing SHOULD rule. Weak words: **pass**, the comparison replaces “rare” or “not worth it.” Level: **pass**, it inherits SHOULD. Basis: **pass as a labelled proposal**, supported by the supplied findings but **n=0 for this policy**, to be revisited on its first application. Links: **pass**, no new relationship to another requirement is asserted.

## What I need to know

None to recommend this policy. For a particular procedure, the deciding agent needs its expected use, both forms’ construction and upkeep effort, and the consequences of mistakes. Without those, the cost conclusion remains provisional.

## Costs and risks

- **My #18 (`attributed`):** making the comparison takes effort; speculative precision could cost more than a small script.
- **My #7:** optimistic estimates can excuse recurring manual work or justify unused automation. Recording assumptions makes either judgment challengeable.
- **My #3 and my #5:** switching from a page to a script later is possible, but earlier manual mistakes may be irreversible.
- **My #14:** delegated decisions reduce owner workload but can produce inconsistent judgments; review still costs attention.

## How we would know I was right

**My reading:** On subsequent uses, compare observed operator effort, upkeep and errors with the recorded assumptions. A page decision is supported when scripting still would not repay its additional cost; evidence that a small script would have prevented costly repeated work or mistakes overturns it.

The requirement check above is mine. It checks whether the proposal is explicit and reviewable; it does not independently establish savings, reliability or the owner’s acceptance.