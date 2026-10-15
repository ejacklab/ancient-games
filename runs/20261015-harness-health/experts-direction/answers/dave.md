# Dave — Does EJ's use-case / requirement / vision direction hold?

## Answer
The core of the direction holds: EJ writes the basic use cases, the AI suggests more, and EJ decides. It also matches the round-1 split between observed and generated cases. It breaks in three places:
- Nobody has measured whether the accepted list is a stable denominator.
- "Must follow" has no rule for which side wins when an accepted use case contradicts a requirement.
- "Suggested by AI, accepted by EJ" is two artifacts, not one.

I would not settle any of these by argument. The trial's 28-case and 200-case lists may already exist. If they do, EJ can run one cheap experiment on them, with a written prediction and with R11.1 as the control, before the direction is written down as a rule.

## How I decided
1. **What would change my mind (my #1).** The whole of T2 rests on one claim: once EJ filters an AI list, its size no longer depends on the generator. I would drop that claim if EJ, accepting from the 28-case and 200-case lists without knowing which prompt made which, ended up with lists whose sizes differ about as much as the raw lists did. I would keep it if the two accepted lists come out close in size and mostly overlap. "About as much" and "close" are comparisons for EJ to make. I am not setting a number.
2. **Data already in hand (my #5).** The trial shows the following:
   - A raw AI list drifts with the prompt: 28 cases against 200, and raw coverage of 46% against 20%.
   - Units fixed from a requirement did not drift: 80% both times.
   - The lists still found real gaps: a clause with no "fails if", a "fails if" with no test or code, and cases that contradict a settled decision.

   It does not show:
   - anything about a list a human accepted, because the trial had no acceptance step;
   - anything about work that has use cases and no requirement;
   - anything beyond one requirement on one engine.
3. **Sizing that evidence (my #10).** It is n=1, so it is a hint. The trial supports this part of the direction: the AI's value is discovery, and the count should not come from a raw AI list. It says nothing about step 3 or step 5.
4. **What holds, with cases (my #5 and my reading).**
   - Steps 1–2 hold. EJ's own basic use cases are the observed situations Linus said may come first. The AI's suggestions are generated cases, and EJ's yes or no stops them from setting the count. Case: in the trial, the brainstorm list surfaced the clause with no "fails if" as a suggestion. A human then decides whether it is in scope.
   - Steps 4 and 6 hold. Requirements carry the detail that use cases leave unclear. Case: a "fails if" with no test is a requirement-level gap that no use case would have shown.
5. **Where it breaks: T2, the denominator (my reading, untested).** EJ deciding on each suggestion turns a generator's list into a decided list. But the size of the offer can still drive the size of what is accepted, through anchoring and fatigue. Being asked about 200 items is not the same as being asked about 28. So the accepted list is fixed only if it is frozen before coverage is counted. Additions after the freeze start a new count. This mirrors R11.1's own order: units are fixed before any case is generated.

   There is also a conflict to surface. R11.1 says old use cases "attach to a unit as evidence and never add to the count". This direction makes use cases the units. EJ has to say whether accepted use cases replace R11.1's units or sit beside them.
6. **Where it breaks: T1, must and should (my reading).**
   - Reading the restatement against the quote: EJ wrote "requirements are SHOULD have" and "as requirements are normally details, requirements are must follow". The main agent's step 5 adds "once a requirement exists", which builds one answer to T1 into the restatement. The words do fit that answer: "have" points to existing and "follow" points to obeying. But EJ gave a different reason for the must: requirements are details, not that they exist.
   - The case that breaks it: the trial already produced cases that contradict a settled decision. Suppose EJ accepts such a use case, which is a must, and the requirement it contradicts is "must follow". Two musts now disagree, and the direction says nothing about which wins.
   - On the house rule: if "MUST only for a safety bound" applies to method rules, then use cases and requirements are product content and may not fall under it. If it applies to everything, "use cases are must" conflicts with it. Which scope is meant is EJ's call.
   - The agreed evaluation style ("state what makes a result wrong") avoids the label altogether. For example: "a result that fails an accepted use case is wrong" and "a result that breaks a written requirement is wrong".
7. **T3, one maker or two: how nature does it (my #6).** The immune system separates generation from selection. Receptors are made in great variety by random recombination. A separate step (thymic selection) then deletes the ones that attack the body's own tissue. What survives is the product of the selection step, not of the generator.
8. **Does the analogy fit? (my #7)**
   - Same: one side over-produces and the other filters.
   - Different: the thymus applies a fixed, cheap criterion to billions of cells. EJ applies judgment, with limited attention, and with no written criterion.
   - I keep only the structural part: generator and selector are different makers, so they make different artifacts. That gives two forms each:
     - the AI's suggestion list (made by the AI);
     - EJ's accepted use-case list (made by EJ, by writing or by accepting);
     - the AI's suggested requirements;
     - the written requirements (accepted by EJ, or written by EJ).
   - I drop the scaling part. A human cannot select at immune-system volume, so the length of the offer is a cost, not a free input (see item 5).
9. **Test instead of arguing (my #2, #3, #4, #8).** The experiment costs less than this debate.
   - Use the trial's existing 28-case and 200-case lists, so no new engine call is needed.
   - EJ accepts or rejects from each list without knowing which prompt made it.
   - Before looking, write down the metric (accepted-list size and overlap between the two), the expected direction ("the gap between the accepted lists is smaller than the gap between the raw lists") and a stop date.
   - Control: R11.1's fixed units for the same requirement, which already gave 80%.
   - Run it on this one requirement only, and spread it only if it holds.
10. **Report a negative with the same weight (my #9).** If the accepted lists still differ by about as much as the raw ones, that result goes into the record as a finding against T2's reading, not as a failed run.

## What I need to know
- **Precedence.** When an accepted use case contradicts a written requirement, which one wins? If use cases win, "requirements must follow" really means "must follow unless a use case says otherwise". If requirements win, use cases are not the top must.
- **Scope of "must".** Does EJ's "must" mean the house-rule MUST (a safety bound), or plain "a result that fails this is wrong"? If it is the second, the house-rule conflict in T1 goes away.
- **Replace or sit beside.** Do accepted use cases replace R11.1's units when there is no requirement, or sit beside them? If they replace them, R11.1's line "never add to the count" needs EJ's change. If they sit beside them, T2 only arises for work that has no requirement at all.
- **Is there work with use cases and no requirement?** If every piece of work in practice has at least one requirement, T2 reduces to R11.1 and the experiment matters less.
- **Are the trial's two lists still kept, and where?** If not, the experiment needs a new engine call, which needs EJ's go-ahead.
- **Does EJ accept against a written criterion, or by judgment?** With a written criterion, an independent reviewer can fail EJ's acceptances, as in R11.1. Without one, the accepted list cannot be checked; it can only be trusted.

## Costs and risks
- **EJ's time (my #8).** Asking EJ about each suggestion costs attention in proportion to the list. On the 200-case list it is a real cost and a source of anchoring. A cheaper option is to show EJ the suggestions grouped, but grouping is itself a choice that can hide items.
- **Two forms instead of one (my #6 and #7).** Splitting suggestion lists from accepted lists adds files and one hand-off per piece of work. The risk on the other side is that without the split, an item EJ never saw can end up in the accepted list.
- **The experiment (my #2 and #3).** It needs EJ's time to review both lists blind. Its result is n=1, a hint (my #10). It costs nothing in engines only if the trial lists still exist.
- **Freezing the accepted list (my reading, from my #1).** Later good suggestions wait for the next count, so coverage looks stable while the list of known cases grows behind it.
- **Writing "what makes a result wrong" instead of MUST/SHOULD (my reading).** EJ has to restate their own words. The risk is that the restatement changes what they meant, so EJ writes it.

## How we would know I was right
- **T2.** In the blind acceptance test, the accepted lists from the 28-case and 200-case prompts differ in size much less than 28 does from 200, and overlap mostly. If they do not, I was wrong to call an accepted list a fixed denominator unless it is frozen first, and I report that (my #9).
- **T1.** Plant two results and check that each is failed. The first breaks a written requirement but passes every accepted use case. The second fails an accepted use case but obeys every requirement. Then plant a suggested use case that contradicts a settled decision, as the trial did. The process should flag it before EJ accepts it, and the precedence rule should say which side wins. If no check flags it, the precedence gap is real.
- **T3.** Take one piece of work under the two-form split and plant an AI suggestion in the accepted list that EJ never saw. A check that compares the accepted list with EJ's recorded decisions should fail on it. If no such check can fail, "accepted by EJ" is not yet a maker; it is a label.
