# 孫子 (Sun Tzu) — which of vision, requirements and use cases is written first

## Answer

Within one pass the order is **vision, then requirements, then use cases, strictly**: a requirement is measured from the vision and a case is measured from the requirement (my #2, #1, #3, #4), and the agreed coverage rule itself scores cases against units taken from the requirement's text and its "fails if" (R11.1, facts). Across passes it is a **loop** — a case that exposes a missing behaviour or a missing "fails if" repairs the requirement, and a requirement that changes who the product is for, or what it will not do, repairs the vision — closed when a full pass adds no new fixed unit and no new "fails if", and every existing "fails if" has a check shown failing once on a planted wrong input. EJ's "use cases first" holds as **discovery** before the requirement is frozen and breaks as **definition**, where the case list sets coverage (my #12, #13, #15); if the product already exists with old use cases, the first pass starts from them, and the choice remains EJ's.

## How I decided

1. Order the war before fighting it. My #1 is an algorithm, and its second passage is an ordered chain: 「地生度，度生量，量生數，數生稱，稱生勝」 — ground gives measurement, measurement gives quantity, quantity gives number, number gives the weighing, and the weighing gives victory (my #1, quoted). The vision is the ground made explicit; requirements are 度/量/數; use cases are 稱, the weighing of the sides. The chain runs one way inside a pass. The mapping of the three artifacts onto the chain is **my reading**; the direction is the rule's.

2. Spend first where the leverage is. 「上兵伐謀，其次伐交，其次伐兵，其下攻城」 — the highest use of troops strikes plans, the lowest attacks walled cities (my #3, quoted). A vision is the plans level; a use case is a walled city. (my #3)

3. Make your own side unbeatable before looking for the enemy's weakness: 「先為不可勝，以待敵之可勝」 (my #2, quoted). A requirement with a level, a "fails if", a check and a named decider is the unbeatable half; the unknown user behaviour is the enemy's half. Cases are how the enemy is made to show form (my #2, my #17).

4. Know yourself before the other side: 「知彼知己，百戰不殆」 (my #4, quoted). Requirements are the self-knowledge; cases are the other side. My #4 also prices half-knowledge — knowing your troops can attack but not whether the ground permits battle is 「勝之半也」 (my #4, quoted). Generate cases over a requirement you have not fixed and you are in that half-victory state.

5. **(b) Where "use cases first" holds — as a probe.** My #17 is a probing algorithm: 「故策之而知得失之計，作之而知動靜之理，形之而知死生之地，角之而知有餘不足之處」 — reckon them, stir them, make them take form, test them in contact (my #17, quoted). The trial (facts, n=1) ran cases before the requirement was frozen, and the list surfaced a clause with no "fails if" and a "fails if" with no test and no code. That is 角之 working: the case list is a legitimate instrument for making a requirement's gaps visible.

6. **(b) Where it breaks — as definition.** When the case list is read as the definition of coverage, the count belongs to whoever brainstormed hardest, not to the requirement. Same trial: 28 cases from "list the test cases" gave 46% raw coverage and 200 from "brainstorm every scenario" gave 20%; over the fixed units both gave 80%. The measure moved with the prompt. My #12 gives the rule: 「故善戰者，求之於勢，不責於人，故能擇人而任勢」 — seek it in the disposition, do not demand it of the people (my #12, quoted). The fixed units are the 勢; the engine is the person. My #13 adds why no list can be complete: 「途有所不由，軍有所不擊，城有所不攻，地有所不爭，君命有所不受」 (my #13, quoted). A second concrete break: one of the brainstormed lists contained cases that contradicted a decision already settled in the tests (facts) — a probe legislating over a settled choice.

7. **(b) The limit is a known danger, not an oversight.** Among the general's five dangers is 「愛民，可煩也」 — loving the people, he can be harried (my #15, quoted). An appetite to cover every possibility is that handle. EJ's agreed 80%-of-units target (R11.1, facts) sits under my #13: some roads are deliberately not taken.

8. **(a) The pass, in one line each, and the revision path.** Write: vision → requirement → case. Revise: case → requirement (a missed behaviour or "fails if") → vision (only when the change touches who it is for or what it will not do). Nothing revises from vision straight to cases without the requirement in between, because the requirement is the unit of measure (my #1's chain; my #12).

9. **(c) Vision — maker and check.** The maker is EJ (facts: "an agent may only write down what EJ has said"). Where EJ is not the person the product is for, the maker is that person and EJ is the decider: my #11 says 「先知者，不可取於鬼神，不可象於事，不可驗於度，必取於人，知敵之情者也」 — foreknowledge must be got from people who know the situation, not by likeness to past events (my #11, quoted). Check before a requirement is built on it: it names who it is for, the problem it solves, what it will not do, and how we know it works, and every line traces to the maker's own words. It fails on a line an agent added that the maker did not say.

10. **(c) Requirements — maker and check.** The maker is the person named as decider for that requirement's open choices; where that is EJ, EJ writes the level and the "fails if". Check before a case is built on it: one behaviour per fixed unit; a level (MUST / SHOULD); a "fails if" for every clause; a check that can fail, shown failing once on a planted wrong input; a named decider for each open choice. It fails on a clause with no "fails if" (the trial's exact gap, facts) and on a "fails if" with no test and no code.

11. **(c) Use cases — maker and check.** The maker is the engine chosen for that round (my #12's 擇人而任勢); the units and the target belong to the requirement owner, not the engine. Check before a case counts: it attaches to an existing fixed unit; AI-generated cases and old use cases are evidence and never add to the count (R11.1, facts); the old-case set is failed once on a planted violation before it counts; no case contradicts a settled decision. A case that fits no unit is not added to the list — it is returned as a missing unit in the requirement.

12. Close the loop on advantage, not on exhaustion: 「合於利而動，不合於利而止」 — move when it accords with advantage, stop when it does not (my #5, quoted). Operationally, a pass that no longer changes the requirement's units has stopped according with advantage. My #8 gives the reason not to wait for completeness: 「故兵聞拙速，未睹巧之久也」 — clumsy speed is heard of, skill that is prolonged has not been seen (my #8, quoted).

## What I need to know

- **Whose product, and who it is for.** If the vision's maker is the person the product is for, the vision check is "traces to their words" and EJ is the decider; if EJ is both, it is "traces to EJ's words." If neither is available, the vision cannot pass and the order collapses to requirement-first — the case I cannot answer without this.
- **Is there an existing product with old use cases?** If yes, the first pass starts from the old cases (my #19: name the ground first; my #17: old cases are signs already read), and "vision first" means only that the vision is named before the requirement is changed. If greenfield, the first pass is vision → requirement → case.
- **Who may fail a check?** My checks are real only if someone can fail them. If only EJ can fail the vision check, the loop runs at EJ's availability; if each named decider can fail their own, it runs faster.
- **Is the 80% target per requirement or per product?** Per requirement, the loop can close on one requirement; per product, one requirement's gap can hide under another's coverage.
- **May a requirement's fixed-unit set change during a pass?** If yes, the close condition I gave is checkable. If no, the loop cannot close except by luck.
- **Do the three musts apply to all designed work, or only product work?** If a one-day internal change is in scope, the vision may be a single line and the effective order is requirement-first.
- **What counts as "checked"?** Whether a check needs a written artifact (a test, a script) or a spoken verdict — the house rule says a check must be shown failing once; I need to know where that record lives.

## Costs and risks

- Vision-first delays the first case list; a vague vision can pass its own check and the error is inherited by every requirement and case (my #1: fewer reckonings lose; my #2: 「勝可知，而不可為」, victory can be known but not made).
- The repair loop has a rework price: each new "fails if" makes earlier cases provisional (my #17; my #6, 「雜於害而患可解也」).
- Use-cases-first as definition makes the coverage number an artifact of the prompt — 46% vs 20% on the same requirement (my #12; my #13).
- A percentage over units can hide a "fails if" with no test and no code; the trial found one (my #6 harm column; my #4, 「勝之半也」).
- Making EJ the sole maker of the vision makes EJ the bottleneck, and my #11 prices foreknowledge in people (「必取於人」); the cheaper alternative — an AI-written vision — is what my #11 forbids (「不可象於事」).
- Accepting EJ's 80% deliberately leaves units uncovered; the risk is that the skipped unit carried a real consequence. The opposite risk — requiring every unit — is the prolonged skill my #8 says has not been seen.

## How we would know I was right

- **The order test.** Take one requirement and run both orders with the same engine: (A) freeze the units and "fails if", then generate cases; (B) generate cases from "brainstorm every scenario", then read the units out. If (B) adds or changes a fixed unit or a "fails if" that (A) did not, use-cases-first was doing discovery work and a discovery pass belongs in the order. If (B) changes only the case count and the raw coverage, it was doing definition work and must not set the count. Either result is a verdict: 吾以此知勝負矣 (my #1).
- **The close test.** Across passes on one requirement, count the fixed units and the "fails if" clauses. If the count stops changing before the coverage target is reached, the requirement was a fixed ground and the order held. If it never stops, the requirement was never fixed and vision/requirements-first did not hold for it.
- **The planted failure.** Show both checks failing once: a vision line no one can deny ("easy to use") must be rejected by the vision check, and a case contradicting a settled decision must be rejected by the case check. A check that has not failed once is not yet a check (house rule; my #6).
