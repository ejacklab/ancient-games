# 范蠡 (Fan Li) — final wording of A2 and A5 (round 2)

## Answer

I accept 1, 3, 4, 5, 7, 8 and 9, and I still reject 2 and 6. I made three changes from round 1, each taken from another expert:
- Each actor's duty now goes in one Fails-if line, not two (from 孫子 and Linus).
- A call credited to the wrong body is now caught inside the "contradicts the code" line (from 孫子 and Linus).
- A5 now lists what an answer holds, and an agent breaks A5 by *running `map`* without being asked (from Linus).

Two questions are still for EJ: does a known link marked `dynamic` count as missing, and does going into a body written straight into a call count as a level?

| # | Final decision | Changed from round 1? | One-line reason |
|---|---|---|---|
| 1 | accept with this wording: **one** Fails-if line that names the tool's duty and the agent's duty | **Yes**: one line, not two (孫子, Linus) | Each actor is named, so each is charged with its own duty. Splitting the line was only a matter of layout, and it moved the requirement toward pieces. |
| 2 | reject | No | No defect has been found in "known". Each of the three definitions offered decides the dynamic-call case differently, and 老子's definition and his own cost line contradict each other on it. That case is EJ's call (question 1). |
| 3 | accept with this wording (no "or a stated limit"; no extra sentence that "unresolved links carry limits") | Partly: the wrong-holder clause moves into the "contradicts the code" line (孫子, Linus) | A body can always be placed from the source. L1 already covers any unresolved link. |
| 4 | accept with this wording (shortest route; the level unit kept; a reference never hides a link) | No | The fault is real. Use case 2 needs the same answer whatever the source order. |
| 5 | accept, merged with 8 and 9 | No | "Only inside a dump" let a right answer followed by a dump pass. That happened. |
| 6 | reject | No | A5's "lacks its limits" and L1 already fail a silent cap. 老子's `find` finding is real, but the fix belongs in the spec and the code, not in this sentence. |
| 7 | accept the agent half with Linus's wording ("runs `map`"). The tool half is covered by 5/9 | **Yes**, wording only (Linus) | It names the act the agent controls. A command other than `map` that returns a map is already "content the question did not ask for". |
| 8 | accept, merged into 5 | No | The false pass happened in the default text. |
| 9 | accept the idea, merged into 5. The list of excluded kinds is rejected, and Linus's list of what an answer holds is taken | **Partly** (Linus) | Saying what an answer holds makes "not asked for" checkable. A list of excluded kinds goes stale, and "unrelated" is a weak word. |

**A2 The call chain through one place.** Given code or a description, the tool locates the place and returns its caller and callee chains, counted in levels from the place. The place is level 0 and each link adds one level. A link is within the depth when its shortest route from the place is. The user sets the depth each way; when the user does not, it is six. When more than one place matches, the tool flags the match as ambiguous and lists every candidate with its location; the agent picks the place that fits the question best, builds its chain, and names every other candidate it did not build. Each link gives its kind and location, and names the body that holds the call. A body written straight into a call is a place of its own; its calls are never shown as calls by the function that surrounds it. A function reached twice is shown once, with a reference back; the reference never hides a link that is within the depth through another route.
**Fails if:** any of these happens:
- a known place is not found;
- the tool does not flag an ambiguous match, or leaves a matching candidate unlisted or without its location; or the agent treats an ambiguous match as certain, or does not name a candidate it did not build;
- a known link within the depth is missing, including one hidden behind a reference back, or a shown link contradicts the code, including a call credited to a function that surrounds the body holding it;
- a link lacks its kind or location;
- a function reached twice is shown twice.

*Conditional, waiting on question 2.* If EJ answers **no level**, add after "each link adds one level": "Going into a body written straight into a call adds no level." If EJ answers **a level**, add: "Going into a body written straight into a call adds one level."

**A5 One question, one answer.** A specific question gets that answer with its evidence and limits, not a whole-map dump. The answer holds the requested result, its evidence and its limits, and, when more than one place matches, the candidates; it holds nothing the question did not ask for. This holds for JSON and for the default text the agent reads. A whole map is produced only when the user asks for a module map; the agent runs `map` only then.
**Fails if:** any of these happens:
- an answer comes inside a dump, or carries content the question did not ask for, beside the answer or inside it, in JSON or in the default text;
- an answer lacks its evidence or limits;
- the agent runs `map` when the user did not ask for a module map.

*Conditional, waiting on question 1.* If EJ says a known link marked with a `dynamic` limit at its site is **not** missing, change A2's third line to: "a known link within the depth is missing with no limit at its site naming why, including one hidden behind a reference back, or …" (the rest as above).

## How I decided

1. **I read the other three answers as a cross-check, not a vote** (my #12: 「又觀其民之饑飽勞逸以參之」, `quoted`; using it to check the COO's summary is my reading). The COO's summary is right except on 1 and 7:
   - It says Linus writes "a tool line and an agent line". His final A2 has one line: *"the tool does not flag an ambiguous match, or omits a matching candidate or its location; or the agent treats an ambiguous match as certain or fails to name a candidate it did not build"*. His A5 also has a single Fails-if line.
   - 孫子's single line names the agent too (*"or the agent treats an ambiguous match as certain"*).
   - So all four of us name both actors. The only real difference was layout, plus 老子's A5, which has two bullets.
2. **Proposal 1: I changed from two lines to one** (my #14: 「四封之內，百姓之事，蠡不如種也。四封之外，敵國之制，立斷之事，種亦不如蠡也。」, `quoted`). The rule is that each party is charged with what it does. Naming the actor inside one line already does that. 孫子's argument changed my mind: *"The evaluator/P6 division is a checking matter, not a wording matter."* Two lines bought nothing that the naming did not, and they pushed the requirement toward pieces, which the brief forbids (my reading).
3. **Proposal 2: I still reject it** (my #5: 「天節固然，唯謀不遷。」, `quoted`). The owner's word stays unless a defect forces a change. No check has found one in "known": the dynamic-call false pass was a *shown* link contradicting the code. Here is why each counter-argument fails:
   - **Linus**, *"Known places and links are those established from repository source or type information."* Every link in a TypeScript repository is in its source, so this rules out nothing a key writer could claim. It also leaves the one hard case (a dynamic call whose target is known) undecided. And it would define, in A2 alone, a word that A1 also uses.
   - **孫子**, *"a link is one the type checker establishes."* His own cost line concedes my round-1 objection: *"if the tool is the checker's only interpreter, the check and the tool still share one reading."* That conflicts with L2's keys, which must come *"by a method other than the tool's"*.
   - **老子** defines known to include the case where *"the source makes a call the tool cannot resolve"*. His cost line then says such a call *"is no longer 'known', so its absence no longer fails that line"*. The same case is read in two opposite ways in one answer. That is the clearest sign this is EJ's call (question 1), not a wording fix.
4. **Proposal 6: I still reject it** (my #10: 「無過天極，究數而止」, `quoted`, which I read as: stop where the measure already stands).
   - **Linus**, *"An undisclosed cap or sample can mislead the agent."* True, but A5's "lacks its evidence or limits" and L1's *"Every answer or branch that stops early names why"* already fail it.
   - **老子**, *"`find` drops every match below the best score with no limit at all."* I checked `code_map/src/commands.ts` (`matchesByDescription`, lines 137–138): it keeps only the best score tier. The finding is real. But proposal 6 does not settle it either; 老子's own question 4 asks whether a ranked search is a stop at all.
   - The spec's interface row promises *"ranked matches for a description"*, and A2 already requires every matching candidate to be listed. So if the lower tiers are matches, A2 already fails the tool. If they are not, nothing in A5 changes. Either way it is a disagreement between the spec and the code, for the COO, and it does not change A5's wording (my reading).
   - Keeping 6 would also use "whole" in two senses in one sentence ("whole answer", "whole-map dump").
5. **Proposal 3: no "or a stated limit"** (my #11: 「用力甚少而名聲章明」, `quoted`, applied as the fewest words that hold).
   - Linus backs dropping the limit: *"anonymity alone does not justify omitting a known body."* 孫子 and 老子 keep "or a stated limit" but give no case where a body cannot be placed. Without one, an escape clause only invites losing links. The spec says *"E1 found 17 of 18 calls in anonymous bodies"* on the first target.
   - I reject Linus's *"Any unresolved link into or out of that body carries a stated limit"* for the reason I gave on 6: L1 already says it.
   - I did move my separate wrong-holder line into the "contradicts the code" line, using 孫子's and Linus's wording. It is the same failure, and the evaluator case `A2-inline-generator-owner` is already charged to that line in `fixtures.json`, so no case has to move.
6. **Proposal 4: I keep the unit sentence** (my #4: 「得時無怠」, `quoted`, since the fault is live now).
   - All four accept shortest route. The reasoning is that a reorder of calls must not read as a change of logic (use case 2), and "counted in levels from the place" means distance. I no longer count this as an owner question (my reading; EJ can still overturn it).
   - Against **老子**, *"Level 0 is already the interface's (`spec.md:32,104`)"*: the evaluator charges the requirement, not the spec. Without the unit, A2's "six" has no unit inside A2 (requirement-check's "unit"; my reading).
   - I leave out Linus's and 孫子's *"regardless of traversal order"*. The shortest route already makes the set of links independent of order, so the phrase would say the same thing twice.
7. **A5: full without overflowing** (my #2: 「天道盈而不溢，盛而不驕，勞而不矜其功。」, `quoted`).
   - I took Linus's list of what an answer holds (*"the requested result, its supporting evidence, applicable limits and any candidates needed to resolve ambiguity"*). Everything outside it is "not asked for". That answers 孫子's risk, *"A strict reading can punish a legitimate answer … a loose reading lets a dump pass"*, better than the weak word "unrelated".
   - Against **老子**'s *"a section or content the command does not answer"*: an extra link from another function inside a `callees` answer is content the command *does* answer by type, so his wording misses the inside-the-payload case that `A5-exact-callees` checks.
8. **Proposal 7: Linus's "runs `map`"** (my #14 as in step 2, `quoted`). "Produces a whole map" does not say who acts. "The agent runs `map`" names the one act the agent controls; the spec says `map` prints a module only because the user asked.
9. **The two open questions wait for EJ** (my #9: 「天地未形，而先為之征，其事是以不成」, `quoted`, applied as: do not decide before the form is visible).
   - The level of a body written straight into a call was raised by 老子 (his question 2). Linus's point is behind it: *"lexical ownership identifies the caller; it does not establish that a framework invokes a callback."*
   - Nobody can settle it from the vision, and it changes how far the default six reaches on opencode. So I give conditional sentences rather than pick one (my #7: 「王無蚤圖」, `quoted`).
10. **Settled this round, so no longer for EJ** (my reading). All four agree on these:
    - The requirement does not fix the name of a body with no holder (老子: cut it; Linus: *"A2 need not fix the anonymous body's display name"*; 孫子: *"fix ownership, not the string"*). The spec's rule-table row owns the name.
    - The agent's duties stay inside A2 and A5.
    - Depth means the shortest route.

## What I need to know

1. **Does a known link that the tool cannot follow, but marks with a `dynamic` limit at that site, count as "missing" under A2?** Round 1 split three ways on this through the definitions of "known", so the four of us cannot settle it.
   - *If yes:* A2 stands as written. It fails on every dynamic call whose target a key writer knows.
   - *If no:* use the conditional third line above. The tool then cannot fail on a link it marked dynamic.
2. **Does going into a body written straight into a call count as a level?** The vision does not say. The answer changes how many real calls the default six reaches on opencode, where the spec reports 17 of 18 calls in such bodies.
   - *If no level:* add "Going into a body written straight into a call adds no level."
   - *If a level:* add "… adds one level". The levels expected in the fixtures may then change, as 老子 noted.

## Costs and risks

- **One line naming both actors** (my #14, `quoted`). The evaluator cannot mark the tool's half MET by the line's text alone. A2 and A5 stay "tool part MET, agent part NOT CHECKED → P6" until the integration test runs.
- **Rejecting 2 leaves "known" undefined until question 1 is answered** (my #5, `quoted`). Until then, a dynamic-call key can fail A2 on a link that no static reader can establish.
- **Rejecting 6 leaves `find`'s top-tier cut to the COO** (my #10, `quoted`). If the spec rules that lower-scoring description matches are neither matches nor a stop, no requirement catches a weaker match the agent never sees. Use case 1 would pay for that.
- **"Nothing the question did not ask for" is strict** (my #2, `quoted`). An answer that echoes the query, or prints a header, could be read as unasked. Exact-shape cases (`A5-exact-*`) are what make the line checkable; without them it is weaker than it reads.
- **Proposal 4 costs a rewrite of the traversal** (my #4: 「得時不成，天有還形」, `quoted`). `chainDown`/`chainUp` keep one `expanded` map and never revisit a function. Until the rewrite, `A2-shorter-route-down` and `-up` stay NOT MET, by design.
- **Dropping "or a stated limit"** (my #11, `quoted`). If opencode turns out to have a body the tool truly cannot place, the requirement leaves no way out other than L1 on that branch.
- **New wording means new line strings** (my #18: 「審備則可以戰乎？」, `quoted`). Every case's `line` field must be re-mapped before a round can be read. 老子 reports the strings live in `eval/requirements.ts` and that 70 cases name them; I did not read that file. Merging the wrong-holder clause into an existing line keeps that re-mapping smaller.

## How we would know I was right

1. **Negative control, after the line strings are re-mapped** (老子's test, which I adopt). Run the bundled cases against the current tool. Exactly the two `A2-shorter-route` long-first cases should be NOT MET, and nothing else. A line that no case names, or a case charged to a line that no longer exists, means the re-mapping is wrong.
2. **After the traversal fix**, `chain --down 3` on `route-depth/down.ts` and on its reversed copy gives the same set of links, with `routeTail` present in both. That is the same answer in any source order (use case 2).
3. **A planted copy of the tool** that adds one true but unasked link inside a `callees` answer fails A5's first line, in both `--json` and the default text. The same answer with only its required limits passes.
4. **On opencode**, a `callees` answer on a function whose calls sit in `Effect.gen(function* …)` bodies shows each link with the body's own location as `from`. A key written by another agent finds no call credited to the surrounding function. The levels match whatever EJ answers to question 2.
5. **For question 1**, whichever way EJ decides, a fixture with a dynamic call and a known target gives the same verdict in the evaluator report as the wording does.

*What I verified this round:* I read the four round-1 answers, the requirements in `result-trimmed.md`, the spec's lines on `find`, candidates and the enclosing function, `matchesByDescription` in `commands.ts`, the `A2-inline-generator-owner` case and `COVERAGE.md`. I did not run the tool this round. The tool output I cite comes from my round-1 run.
