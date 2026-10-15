# Dave — which comes first: vision, requirements or use cases

## Answer
My recommendation is conditional. The vision comes first, and it is a strict gate. After it, requirements and use cases run as a loop. Each round fixes the requirement's units before any case is generated, and the cases may then send changes back into the requirement text. EJ's "use cases first" fits *discovery* on a product that has only a vision. It does not fit *counting coverage*. I would settle the order with one small, controlled trial before anyone writes it into the blueprint template. I do not decide it for EJ.

## How I decided
1. **What would change my mind (my #1).** Run two orders on the same new requirement area: cases-first (vision, then cases, then requirements) and the current way (vision, then requirements, then cases). If cases-first finds requirement gaps the current way misses, and its coverage over fixed units is no worse, then "use cases first" should hold for elicitation. If it finds nothing extra, or finds more cases that are out of scope or contradict settled decisions, the current order stays.
2. **The data we already have (my #5).** EJ's own quoted practice runs requirement first: "I get requirement, I will gen use cases, and also see old use cases cover this requirement or not." So "first" in "use cases should come first" may mean *most important*, not *earliest in time*. I list this under What I need to know. The n=1 trial **shows** three things:
   - Raw coverage depends on how the prompt is worded: 28 cases gave 46%, 200 cases gave 20%.
   - Coverage over fixed units held at 80% both times.
   - Cases found real gaps in an *existing* requirement: one clause with no "fails if", and one "fails if" with no test and no code.

   It **does not show** whether starting from cases finds more than starting from requirements, because the order was never varied. Nothing in the trial measured that.
3. **Why the vision is a strict gate (my reading, from the facts given).** The vision's "what it will not do" is the only thing that marks an AI-generated case as out of scope. Without it, "all possibilities" has no edge. The blueprint rule also makes the vision EJ's alone, so no AI step can produce it.
4. **Why units are fixed before cases (my #4 and #5).** The trial is the control here. When the count was taken over generated cases, it swung from 46% to 20% just because the prompt changed. Over fixed units it held steady. If cases come first, the base of the count is whatever the generator produced, and the coverage figure measures the prompt, not the product. This is why "use cases first" breaks for counting. R11.1 already says this: cases "attach to a unit as evidence and never add to the count".
5. **Why it is still a loop (my #9).** The same trial showed cases improving the requirement: they found a clause with no "fails if". That is a finding against the requirement and should count as fully as a pass. So the order cannot be a strict one-way sequence. Cases must be allowed to send gaps back into the requirement text, and then the units are fixed again.
6. **How nature solves it (my #6).** In an ant colony, scouts first wander widely; that is exploration, like use cases. The paths that succeed are then laid down as pheromone trails; that is consolidation, like requirements. Trails nobody reinforces fade. This supports exploring before fixing.
7. **Checking that analogy (my #7).**
   - **The same:** wide, cheap exploration, then fixing what worked, in a repeating cycle.
   - **The difference:** a scout knows at once whether it found food, so its success signal is objective. A use case has no such signal until a "fails if" exists to judge it.
   - **Conclusion:** the analogy holds only if the vision's "how we know it works" serves as the food signal. That gives the same answer as step 3, vision first. If that line in the vision is too vague to judge a case against, the key condition differs and I drop the analogy for cases-first.

   A second candidate, the immune system's negative selection (wide random generation filtered against a fixed "self"), fits the counting rule but not the loop: "self" is never revised by what is generated. So it explains only half of the answer, and I use it for nothing more.
8. **Where "use cases first" holds.** Example: a new product with a settled vision and no requirements yet. EJ or an engine writes stories like "the user does X, expects Y", and these surface requirements nobody has written. The "fails if" for each comes from the vision's "how we know it works".
9. **Where it breaks.** Three examples:
   - **Coverage counting:** see step 4.
   - **Settled decisions:** one generated list held cases that contradicted a decision already settled in the tests. Without the requirement and its settled decisions in place first, nothing marks such a case as wrong. It would enter as a "use case" and quietly reopen a closed decision.
   - **Old use cases:** they count only after failing on a planted violation (R11.1), and that test needs a requirement to violate.
10. **Who writes what (my reading, using the house rule that every artifact has one maker).**
    - **Vision: EJ.** The template allows an agent only to write down what EJ said.
    - **Requirements:** the record names who decides each open choice. Who writes the text is not given to me (see What I need to know).
    - **Use cases are two artifacts, not one.** EJ's own use cases are written by EJ per requirement. AI-generated cases are written by the engine as evidence. Two makers at two times means two forms, so they should not share one list.
    - **Fixed units:** R11.1 does not name a maker (see What I need to know).
11. **The check each must pass before the next is built on it.** Each check must be able to fail and must be shown failing once.
    - **Vision, before requirements:** every requirement traces to the vision's "who it is for" or "the problem it solves". Plant a requirement that contradicts "what it will not do"; the check must reject it. If "what it will not do" is empty, the check cannot fail and the vision is not ready.
    - **Requirements, before cases:** each requirement has a "fails if" and a check, and its units are fixed from its text. Plant a clause with no "fails if"; the check must catch it. The trial found a real one, so this check has already failed once on real input.
    - **Use cases, before design:** each case attaches to a unit, or is flagged either as a gap that goes back to the requirement or as out of scope by the vision. Plant a case that contradicts a settled decision; it must be flagged. The trial produced a real one.
12. **What closes the loop (my #3; a comparison, not a number).** Stop when a round of case generation surfaces no requirement-text gap that the previous round did not already surface. Also stop at a date fixed in writing before the round starts. I do not pick that date; it is EJ's.
13. **How sure I am (my #10).** Everything above rests on one trial of one requirement, plus EJ's quoted practice. n=1 is a hint, not a law. Steps 3 to 7 are reasoning, not measurement.
14. **What to do next (my #2 and #8).** One two-arm trial on one product with a settled vision costs less than arguing the order in the template. Run it on one requirement area first, and add a use-case section to the blueprint template only after the trial is measured.

## What I need to know
- Does EJ's "first" mean first in time, or first in importance? Their quoted practice starts from a requirement. If they mean importance, there is no conflict and the loop above already puts use cases at the centre.
- Is the target a new product (vision only) or an existing one (requirements already written)? If new, cases-first for discovery is worth testing. If existing, requirements-first holds, and cases come in as the R11.1 evidence they already are.
- Who writes the requirement text, and who writes the fixed units? Both are needed to satisfy the one-maker rule.
- Who are the use cases for: EJ's own understanding, an engine's design input, or a test plan? Each implies a different artifact and a different check.
- Is the vision's "how we know it works" specific enough to judge a single use case against? If not, the ant analogy fails and cases-first has no success signal.

## Costs and risks
- **The trial costs engine runs plus EJ's time** to judge which gaps are real (my #2 and #4). The risk is that the trial is itself n=1 and gets read as a law (my #10).
- **Running it on one area only (my #8)** means the template stays without a use-case section for a while. The risk is that EJ keeps writing use cases in a form nobody has fixed yet.
- **Cases-first:** the coverage base drifts with prompt wording (46% to 20% in the trial; my #5). Cases that contradict settled decisions can get in unflagged (my #9).
- **Requirements-first, strictly:** this misses the gap-finding the trial showed (my #9), and requirements get frozen before cases have tested them.
- **The loop:** each round costs a full generation and comparison, and without a stop date fixed in advance it never closes (my #3).
- **The analogy (my #6 and #7):** if the vision's success line is vague, the analogy argues for exploring with nothing to judge the results against. In that case it should be dropped, not stretched.
- **The rule's level (my reading, from the house rule):** this is a method rule, so it can be SHOULD at most. Writing "use cases MUST come first" or "vision MUST come first" would break the house rule that MUST is only for safety bounds.

## How we would know I was right
Fix the following in writing before running (my #3):
- **Setup:** one product with a settled vision, one requirement area, the same engine.
- **Arms:** arm A, cases-first (vision, then cases, then requirements drafted from the cases). Arm B, the current way (vision, then requirements and fixed units, then cases).
- **Metrics:**
  - requirement-text gaps found, meaning clauses with no "fails if";
  - checks found missing, meaning a "fails if" with no test;
  - cases contradicting settled decisions;
  - cases out of scope by the vision's "what it will not do";
  - coverage over fixed units;
  - engine cost.
- **My prediction:** arm A finds at least the gaps arm B finds, but produces more out-of-scope and contradicting cases. Coverage over fixed units is no different between the arms once units are fixed. If that holds, the answer is "vision first, then a loop that may start with cases for discovery, but always counts over units."
- **What proves me wrong:** arm A finds no extra gaps and no more noise. Then the order does not matter and EJ should pick whichever is cheaper. If arm B finds gaps that arm A misses, "use cases first" breaks even for discovery.
- **Stop date:** EJ's to fix.
- **Reporting:** report the result whichever way it falls, with n stated (my #9 and #10).
