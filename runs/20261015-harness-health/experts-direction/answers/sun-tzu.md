# 孫子 (Sun Tzu) — does EJ's use-case/requirement direction hold

## Answer

The direction holds as a loop anchored on the vision, and it breaks in one place: the word "must" is doing two jobs — whether a use case has to *exist* (a coverage target) and whether a result has to be *valid for an accepted use case* (an acceptance bound) — and "requirements must follow" is the second job at detail grain, not a third rule. If EJ freezes a written "fails if" per accepted use case before any generation and names that bound, it stands; if not, the coverage number has no denominator and a two-maker form cannot be repaired. I do not decide whether the house rule admits a validity bound as a MUST.

## How I decided

1. **The ground is the vision, and it is EJ's alone — my #1.** The first of the five matters is the Way, and the first of the seven comparisons is "Which ruler has the Way?" (my #1, `quoted`). Since the earlier round already holds the vision to be EJ's alone, the vision is the ground; use cases and requirements are measured from it. If the vision is not fixed, every count below is a precise measurement of the wrong ground.

2. **Holds — "AI suggests, the user decides" — my #1 and #10.** The trial is the case: the same engine, two prompts, gave raw coverage of 46% and 20% against existing tests (28 cases vs 200), and 80% both times over fixed units. My #1 gives the chain — "the ground gives measurement, measurement gives quantity, quantity gives number, number gives the weighing of the sides, and the weighing gives victory" — so the number comes from the ground, not the generator. My #10 says the same from the other side: an army "has no fixed 勢 and no constant form", and neither has a case generator. The direction holds because it puts the freeze in the user's hands, where #1's ground is.

3. **Holds — requirements cover what the use cases leave unclear — my #6 and #1.** The trial surfaced a clause with no "fails if" and a "fails if" with no test or code. My #6 says "the wise always mix benefit and harm together when they deliberate" and "whoever does not fully know the harm of using troops cannot fully know its benefit": a missing "fails if" is a missing harm column, and a requirement is the artifact that can carry it. EJ's sentence holds.

4. **Holds — "the results are valid for use cases" is the right top bound — my #6 and #2.** My #2 says make yourself unbeatable first and "do not rely on the enemy not coming or not attacking; rely on having the means to meet them". The acceptance criterion is your own ground; the suggested case list is not. EJ puts the top emphasis in the right place.

5. **Breaks — "use cases are must" names no order — my #16, `quoted`.** "If orders are not clear and not drilled in, it is the general's fault; if they are clear and still not followed, it is the officers' fault." "Use cases are must" names no who, no test, and no consequence. Concrete case: a stated use case that the built result does not satisfy cannot be called a violation under the direction as written, because the validity sentence is separate. Under the house rule (MUST only for a safety bound), the sentence also fails as a method rule. My reading: the must belongs on validity, not on existence.

6. **Breaks — T1 is not a contradiction, it is two orders under one word — my #16 and #6.** "Requirements are SHOULD have" orders *existence*; "requirements are must follow" orders *obedience*. Both can stand. But the direction never says which failure each answers: a requirement never written (whose fault?) versus a requirement ignored (whose fault?). My #16 gives the test: an order is clear only when its failure has a named owner. Concrete case: under the direction, a result that ignores a requirement is wrong; a requirement that was never written is not.

7. **Breaks — T2: with no requirement, the 80% has no unit — my #1 and #6.** R11.1's unit is written "from its text and its 'fails if'". A use case that is a name and a paragraph yields zero such units, and 80% of zero is not a measure. The trial's stability came from the frozen unit list, which came from the requirement, not from a list of names. So **the main agent's reading is half right**: the accepted list is stable only if each accepted item carries a written validity condition before generation; otherwise the freeze is on names, and names do not count. Concrete case: a project with use cases and no requirements can honestly report no coverage number — not 0% and not 80%.

8. **Breaks — T3: two makers mean no one is at fault — my #15 and #16.** My #15: the six defeats "are not disasters from heaven but the general's faults, and the text names the cause of each". My #16 divides fault between the issuer of unclear orders and the officers who ignore clear ones. A form filled by the AI (suggestion) and the user (acceptance) at two different times has no one named when it is wrong, so the defeat cannot be repaired. Concrete case: an accepted AI-suggested use case is later found invalid; under the direction the AI "suggested" and EJ "accepted", no fault lands, and nothing in the process changes. My reading: one maker (the user) plus one lever (the AI) keeps the naming.

9. **Breaks — suggestions built from vision and use cases alone have no foreknowledge — my #11, `quoted`.** "Foreknowledge cannot be had from spirits, from likeness to past events, or from measurement; it must be got from people who know the enemy's situation." Concrete case: the trial's list held cases contradicting a decision already settled. An AI reading only the vision and the use cases cannot know the settled decision; only EJ or the record holds it. So AI-suggested requirements are admissible as suggestions, not as foreknowledge.

10. **Change — split "must" into three named bounds — my #16 and #6.** (i) validity of a result against an accepted use case: MUST; (ii) existence of a use case: SHOULD, a target like the 80%; (iii) following an existing requirement: MUST, derived from (i), because a violated requirement invalidates the use case it details. Check that shows it is better: plant a result that violates an accepted use case and show the split calls it wrong, then omit a use case entirely and show the split does not call the work wrong. The direction as written cannot pass that pair, because both cases read "must".

11. **Change — freeze each accepted use case's "fails if" before any generation, and count over those — my #1, #6, #10.** A use case with no written "fails if" is not a unit and does not enter the denominator; report "no denominator". Check: run the trial's two prompts again over use-case-derived units; if the percentage moves with the prompt, the freeze is not doing #1's work. The trial's 28/200 → 80%/80% is the positive half.

12. **Change — a requirement is required when the use case's validity cannot be written as a checkable "fails if" from the use case's own text — my #19 and #1.** My #19 is a condition→response table: "identify the ground by the conditions the chapter defines, then act as prescribed". Here the conditions are whether a checkable "fails if" exists. Check: take the trial's clause with no "fails if", show no unit exists from the use case text alone, then show one exists after the requirement is written. No number is needed, and none should be invented.

13. **Change — AI output is evidence and a lever, never the denominator or the maker — my #10 and #12.** My #12: the skilled fighter "seeks victory in 勢 and does not demand it of his people". The 勢 here is the frozen list and the written criterion; the generator is the people. Check: two prompts, one denominator — the trial already shows it.

14. **Change — one maker, one fault, one record per artifact — my #16 and #15.** The accepted use case and the requirement record the user as maker and label the AI's part "suggested"; the acceptance is the making act. Check: for an accepted-but-invalid artifact, name the fault from the artifact alone; if the answer is "the AI suggested it", the form has two makers and must be split into a suggestion form and an accepted form.

15. **Change — the acceptance criterion is EJ's and states what makes a result wrong, before any right-path work — my #6 and #2.** Check, in R11.1's own shape: plant a violation and show the criterion fails it; the plan writer marks units against the written criterion, and an independent reviewer can fail the marks, because by my #4 knowing your own side is not enough. If the reviewer cannot fail the marks, the check cannot fail, and by the house rule it is not a check.

16. **Change — no second levy of the generator for coverage; its job is to expose unclear detail — my #8, `quoted`.** "In war, value victory and not duration"; the skilled user of troops "does not levy twice nor haul grain three times". The trial is the case: 200 cases did not beat 28. Stop condition: the first pass that surfaces a requirement clause with no "fails if". Check: compare a second pass to the first; if it adds no new named defect and coverage is unchanged, it was a second levy.

17. **T1, answered — my #16 and #6.** No contradiction, one unclear word. Existence is SHOULD; obedience to an existing requirement is MUST; validity of a result against an accepted use case is the bound that makes the obedience a must. As written, "use cases are must" fails the house rule's MUST test and my #16; name the bound or drop it to SHOULD.

18. **T2, answered — my #1, #6, #10.** The 80% counts over fixed written "fails if" units: from the requirement if one exists, else from the accepted use case's own validity text. The user's acceptance freezes the list, and that freeze is what stops generator drift — but only when each accepted item carries a written condition. Without one there is no denominator, and the honest output is "no measurement", not a percentage.

19. **T3, answered — my #15, #16; house rule.** "Suggested by AI, accepted by the user" is one maker (the user) and one lever (the AI), provided the artifact records the suggestion as input and the acceptance as the making act. If the artifact cannot name who is at fault when it is wrong, it is two forms, not one.

20. **Where it breaks first, unamended — my reading of my #20.** My #20 judges houses by the land unit, the tax, and what they breed. Here: the unit (no "fails if" per use case), the tax (the second generator levy), and what they breed (two makers, no fault) all point at T2 and T3 breaking before T1. T1 is a wording fix; T2 and T3 are missing fields. This is my reading from structure, not something I measured; its test is below.

## What I need to know

- Does an accepted use case carry a written "fails if" in EJ's own words at acceptance? If yes, the count can sit on use cases alone; if no, a requirement must exist to supply it. This changes the answer.
- Is a use case's validity observable, or is only the requirement's detail observable? If a use case's validity cannot be checked, the top-level bound cannot be enforced and the direction's main claim has no test.
- Who owns the accepted-use-case list — EJ alone, or the AI with EJ's yes? This decides the T3 maker.
- Does "cover" mean "a result exists and is valid", or "the case is in the list"? The direction uses "cover" for existence and "valid" for results.
- Where is the record of a "settled decision" that AI suggestions must be checked against? Needed for my #11.
- Does the house rule count a validity or acceptance bound as a "safety bound"? If not, even the validity must is SHOULD at most, and that is EJ's call, not mine.

## Costs and risks

- Freezing each use case's "fails if" before generation costs writing time before any value is visible. My #8's own answer is that the second levy cost more and bought nothing (28 vs 200 cases, 80% both), so the upfront cost is the cheaper one.
- Counting on the vision as ground means a wrong or shifting vision yields precise, wrong numbers — my #1: measurement is only as good as the ground, so the vision must be fixed first.
- Naming the user as the one maker means EJ carries the fault for accepted AI suggestions. That is the price of a repairable form (my #16).
- A MUST on validity constrains the builder. My #13 gives the general discretion to refuse a command, but refusing is safe only with the written record, not on private judgement.
- The independent reviewer costs a second agent or person. If the same agent marks and reviews, the marks are self-checked, and my #4 warns that self-knowledge is not enough; a check that cannot fail is not a check.
- Keeping foreknowledge with people (my #11) means EJ must stay in the acceptance loop and cannot automate it away. That is EJ's time, and it is also the point.

## How we would know I was right

- Run the trial's two prompts over units written from accepted use cases with no requirement. If the direction holds, the coverage percentage must not move with the prompt. The trial moved 46% vs 20% raw and held 80% vs 80% over fixed units; the use-case-only case is the untested half.
- Take one accepted use case with no written "fails if". If the process reports a percentage for it, my T2 answer is wrong; if it reports "no denominator", it is right.
- Take one accepted-but-invalid use case. If someone can be named at fault from the artifact alone, T3's one-maker claim holds; if the answer is "the AI suggested it", it fails.
- Plant a violation against the written criterion and let the independent reviewer re-mark. If the reviewer cannot make the marks fail, the check is not a check.
- Run a second generator pass. If it adds no new named defect and coverage is unchanged, my #8 "no second levy" is confirmed and the second pass was the waste.
- Make T1's split. If a result violating an accepted use case is called wrong while a missing use case is not, the split is doing what I said; if both still read "must", it is not.
