# Dave — How much of a requirement to test (the 80% rule)

## Answer
EJ's process works as a habit: reuse old use cases first, write cases down, and skip the rare ones on purpose. As a count, it breaks, because "80% of an AI-generated list" depends on how the generator ran as much as on how much was tested. My proposal is to count the 80% over **distinct behaviours** tied to the requirement's acceptance criteria, not over raw AI cases. Check how stable the list is by generating it twice independently and comparing the two lists. On who marks basic or rare: if a blind trial shows the plan writer and an independent marker agree, the main agent's proposal (writer marks, EJ reviews the rare list) is enough. If they disagree, the disagreements go to EJ. That choice is EJ's to make after the trial, not mine.

## How I decided
1. **What would change my mind (my #1).** Generate the case list for the same requirement twice, independently. If both runs give about the same cases and the same basic/rare split, the list is a stable denominator, the main agent's weak spot is not real, and EJ's process can stand as written. If the counts or the splits move a lot between runs, the percentage is measuring the generator.
2. **Data we already have (my #5).** None on this. No requirement in this project has had an eval plan counted against tests. `docs/TASK_TYPES_LEDGER.md` is at n=0. The weak spot is the main agent's reading and has not been measured. EJ's 80% is n=0. Prior agreement among the five of us (experts-r11 `compare.md`) says a judge counts only if it can return fail. That is a rule, not a measurement on this question.
3. **Where EJ's process holds (my reading, checked against my #4 and #9).**
   - Step 3, reusing old use cases, is "use what you have first" (my #5). It is the cheapest coverage there is.
   - Making 80% a target rather than a gate means a shortfall gets reported instead of hidden (my #9).
   - Naming the rare cases that go untested is honest: the gap is written down, not silent.
4. **Where it breaks, each with a case that breaks it (my reading).**
   - **Denominator drift (step 4).** One run gives 15 cases and another gives 60 for the same requirement. The same test suite then scores, say, 12/15 = 80% on one list and 12/60 = 20% on the other. Nothing about the testing changed.
   - **Padding.** Suppose the list holds 20 small variants of "valid input accepted" and 5 different failure modes. Testing the 20 variants reaches 80%, yet all 5 failure modes are untested. R11.1's clause "every uncovered case is rare" catches this only if those 5 are labelled basic.
   - **Relabelling.** That clause moves the gaming from the count into the label. A writer who wants fewer tests marks a basic case "rare", and the check passes. The clause can fail only if someone other than the beneficiary sets the label.
   - **Old use case "covers" in name only (step 3).** An old test mentions the same feature but asserts nothing the new requirement changes. It counts as coverage, but it would still pass if the new requirement were broken. Under the house rule it should not count until it has been shown failing on a planted violation of the *new* requirement.
   - **The generator's blind spots.** "All possibilities" from an AI misses what the AI does not think of. The 80% is measured over the list, so a missing case is invisible to the count, and 100% of the list is not 100% of the requirement.
5. **How nature solves it (my #6).** The adaptive immune system cannot hold a receptor for every possible antigen. It covers **shape classes**: one receptor cross-reacts with a neighbourhood of similar antigens. It also keeps **memory cells** only for antigens it has actually met. The mechanisms worth borrowing:
   - (a) Count coverage over classes of behaviour. One test covers a class, and variants inside a class do not add to the denominator. This fixes padding and most of the drift.
   - (b) Treat old use cases like memory cells. Reuse them, but re-check that each one still "binds", meaning it fails when the new requirement is violated.
6. **Does the analogy fit (my #7)?**
   - Same: a finite budget against an unbounded space, and coverage by neighbourhoods rather than by single instances.
   - Different: the immune system's coverage is weighted by **what actually arrives** (exposure), and it can tolerate losses at the population level. We decide "rare" *before* any exposure.
   - So I keep (a) class coverage and (b) memory re-checking, and I **drop** any claim that nature tells us which cases are rare. That part fits only if EJ has a record of escaped bugs to stand in for exposure (see What I need to know).
7. **Estimating the size of the list: borrowed from ecology field method, not a living system's mechanism, so my #6 does not strictly apply (my reading).** Ecologists estimate population size with capture–recapture. Run A finds n1 classes, run B finds n2, and m are found by both; the estimated total is about n1·n2/m. Comparing that estimate with the size of the union is a check on whether the list is complete. It is a comparison, not an invented threshold, so it obeys the house rule on thresholds. Its fit is weak: it assumes the two "catches" are independent, and two LLMs share blind spots (house memory: "known answers need a different method"). So it can only underestimate the true total. It is a lower bound, never proof of completeness.
8. **Who marks basic or rare (my #4, my #2).** Don't argue it, test it. The control is the main agent's proposal (the writer marks, EJ reviews the rare list). The change is an independent marker labelling the same classes blind. Compare the two sets of labels on one requirement.
   - If they agree, the cheaper option (the control) is enough.
   - If they disagree, the disagreements are exactly the cases EJ should see. That is a short list, not every case.
   - Either way, EJ decides which arrangement to keep.
9. **Small and reversible first (my #8), prediction written first (my #3).** Run this on one requirement before it becomes method text. Fix in writing beforehand:
   - the metric: raw case count, class count, the 80% figure on each, and writer/marker agreement;
   - the expected result (my prediction): the 80% figure computed over raw cases varies between the two runs more than the same figure computed over classes;
   - the stop date: one session.
10. **How sure I am (my #10).** Everything above is n=0. The breaking cases are constructed examples, not observed failures. The immune-system and capture–recapture borrowings are proposals that have not been tried here.

## What I need to know
- **What does "very basic" mean in EJ's sentence?** "why 80% those very basic things and 1 in a million edge cases those doesn't required to test" can be read two ways: (i) basic cases make up the 80% and must be tested, or (ii) very basic things are too trivial to need a test, like rare cases. The brief assumes (i). If EJ meant (ii), R11.1's clause is backwards, and the 80% sits over the *middle* band.
- **Is there a record of escaped bugs** (defects found after release, per requirement)? If so, step 6's exposure weighting fits. "Rare" can then be checked against history, and the best first trial is a past requirement whose bug escaped: did the case list contain it, and was it marked rare? If not, rare stays a judgment and the blind two-marker comparison is the only check.
- **Is a second generator run a paid engine call?** If so, the trial in step 9 needs EJ's go-ahead before it runs.
- **Who merges cases into classes?** The merging is itself a judgment that can be wrong. If EJ wants it done by the plan writer, the independent check moves to the merge.

## Costs and risks
- **Two independent generations per requirement** roughly double the cost of producing the list (my #1, my #4). The risk is that the generators share blind spots, so their agreement looks like completeness when it is not (my #7).
- **Class merging** adds a step and a new place to game: merge too aggressively and the denominator shrinks, so 80% gets easy again (my #6, my reading). It needs its own failing check: plant two genuinely different behaviours and confirm they are not merged.
- **An independent marker** costs one more pass per plan. Skip it if the trial shows agreement (my #2, my #4).
- **Capture–recapture gives only a lower bound** because the samples are not independent. Reporting it as "total possibilities" would mislead (my #7, my #10).
- **Re-proving old use cases** (planting a violation of the new requirement and confirming the old test fails) costs a run per reused test. Skipping it lets name-only coverage count (my #5, house rule).
- **Running the trial before writing the rule** delays R11.1 by one session (my #8).

## How we would know I was right
- **On one requirement** (preferably a past one with an escaped bug, if there is one), generate the case list twice independently, with EJ's go-ahead if that is paid. Before running, write down the metric, the prediction (the 80% figure moves more between runs over raw cases than over classes) and the stop date (my #3).
- **I am wrong about the weak spot if** the raw-case 80% figure is about as stable between runs as the class-based one. In that case, keep R11.1 as drafted and report that result with full weight (my #9).
- **Checks that must fail once before they are trusted:**
  - Plant a basic case left untested and labelled "rare". The independent marker's blind label should flag it; the writer-only control should miss it.
  - Plant an old use case that names the feature but cannot fail on the new requirement. Re-proving it should reject it.
- **If an escaped-bug record exists:** the better method is the one whose case list contained the escaped bug *and* labelled it basic. The current process is the control (my #4).
