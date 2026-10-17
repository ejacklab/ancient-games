# Linus Torvalds — deliver context or hold once?

## Answer

**My reading: choose B provisionally.** Holding the first matching call gives the agent an opportunity to apply the lesson before execution; the price is an extra turn and retry, with no measured assurance yet that mistakes decrease.

## How I decided

1. **My #3 — judge the result for the user.** EJ wants fewer repeated code and testing mistakes, with less noise. A can deliver the lesson after the first relevant action. The [hooks reference](https://code.claude.com/docs/en/hooks#pretooluse-decision-control) places `additionalContext` alongside the tool result; it does not establish an opportunity to reconsider the pending call. My reading: that uncertainty matters when the first call can repeat the mistake.

2. **My #13 — solve the immediate problem with what exists.** The supplied facts describe an existing deny/read/retry path. I confirmed that mechanism in [hooks.ts](/home/smoke01/dev/ancient-games/.claude/skills/workflow-design/guard/src/hooks.ts:105). B reuses it. Extending it to lesson delivery remains untested.

3. **My #9 — make the state precise.** The decided unit is **one lesson per session**, not one hold per file or tool. My reading: return all newly matching lessons together and record their delivery before returning the denial. A retry with no newly matching lessons proceeds through the existing guards and normal permissions. The delivery state is separate from the execution journal: nothing executed during the hold.

4. **My #5 and my #7 — keep the decision reversible and preliminary.** Recommend B to the main agent for this run, subject to EJ’s acceptance afterward. R12.3 leaves hook configuration changes with EJ. This recommendation does not authorize changing their settings.

5. **My reading — requirement check.** For the delivery event, **who decides, one thing, unit, can it fail, weak words, level, basis, and links pass** when B is stated as a provisional default with explicit session deduplication. Its basis is the existing denial mechanism plus an inference about usefulness—not measured effectiveness. The outcome claim, *fewer mistakes with less noise*, remains incomplete: its comparison unit and acceptable tradeoff are open.

6. **My #2 and my #18 — distinguish implementation evidence from benefit.** A test showing a denial proves neither that the agent understood the lesson nor that its retry improved. The supplied restriction on live testing means those claims remain unmeasured this session.

## What I need to know

- In a planted repeat, does the agent revise the pending action after reading the lesson, or retry it unchanged? If unchanged, B’s interruption buys no demonstrated prevention.
- How much retry delay and lesson noise will EJ accept for the observed reduction in mistakes? That tradeoff remains theirs; I would not invent a threshold.

These are questions for the run’s investigation and end review, not reasons to interrupt EJ now.

## Costs and risks

- **My #18:** B adds a denied call and another agent turn whenever previously undelivered lessons match. Once per lesson still permits several interruptions as different lessons appear.
- **My #3:** A path or command match establishes relevance according to the matcher, not an actual mistake. A correct action can therefore be interrupted.
- **My #7:** Delivery is not understanding. The agent may repeat the same mistake after the hold.
- **My #5:** The existing execution journal omits denied calls. Measuring interruption costs requires observing those holds separately; journal silence cannot establish low noise.

## How we would know I was right

**My #2 and my #18 — proposed validation, not performed here:** replay the plan’s planted mistakes under A and B, with an unrelated control call.

Check that B prevents the first execution, supplies the lesson, and permits reconsideration; that the same lesson causes no second hold in that session; and that the control receives no lesson hold. Then compare actual repeated mistakes, successful task completion, extra turns, elapsed time, and lesson text delivered.

I propose these checks; they are not independent evidence. Offline checks can establish hook output and session state. Only a later authorized live trial can establish agent behavior.

B is the wrong choice if it loops, stalls useful work, or produces unchanged retries without fewer mistakes. If A produces the same useful outcomes with fewer interruptions, prefer A.

**Choice: B — hold once per matching lesson per session, provisionally.**