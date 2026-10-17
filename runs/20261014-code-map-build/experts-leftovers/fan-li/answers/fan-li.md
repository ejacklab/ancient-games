# 范蠡 (Fan Li) — eight code-map decisions for the opencode run

## Answer

I agree with the COO on 2, 3, 4, 5, 7 and 8, and I differ on 1 and 6. Under 3c, a known link that the tool marks `dynamic` counts as a miss, so A2 needs no new clause. On opencode, count only the sure tests and list the fake-path tests separately, provided `throughFake` means what the spec says. Every pick is provisional, and the owner may overrule any of them.

| # | Pick | One-line reason |
|---|---|---|
| 1 | **b, read through 3c.** A2's line stays "a known link within the depth is missing…", with no clause added | Under c a known link is one the type checker establishes, so marking it `dynamic` is false. A target the checker does not establish is not known, and L1 already makes the tool say why it stops. The COO's pair (3c + 1a) would excuse only false limits. |
| 2 | **a.** Add to A2: "Going into a body written straight into a call adds no level." | A2's unit is "each link adds one level", and entering a body is not a call link. Use case 1 needs a body's calls one step from the function that holds the body. |
| 3 | **c** | It puts "known" on the same ground as the vision (typed services "a syntax-only reader cannot follow") and R2 ("the type checker establishes"). Its place half covers `find` by description. Option b's "source" rules out nothing in a TypeScript repository. |
| 4 | **b** | A5's Fails-if "an answer lacks its evidence or limits" already fails an answer missing a limit the interface requires. The clause would tie the requirement's meaning to the spec's text. |
| 5 | **b** | The evaluator gives one verdict per Fails-if line, and the agent's part is NOT CHECKED → P6. One line naming both actors cannot be MET and NOT CHECKED at once. |
| 6 | **c** (conditional) | The tool cannot see which layer a test provides. `exclude` hides tests that may reach the function, and `count` claims tests that may not. Listing them without counting them serves use cases 1 and 2. |
| 7 | **c, with a's rule used to choose the globs** | A1 wants a fixed rule the user sets, and a glob is fixed and checkable. Files that implement the same interface or service tag are what use case 3 needs for a template of the next one. |
| 8 | **b in the tool, a on opencode** | The repository's owner knows what a test is there, and the tool must not guess. Option a covers opencode's `test/` folders (the spec's case files) and test-named files elsewhere. |

The A2 text that follows from these picks:
- Add 老子's round-2 sentence: "In this requirement a place is known when the given code or description points to it, and a link is known when the type checker establishes it."
- Add: "Going into a body written straight into a call adds no level."
- The missing-link line stays as written.

## How I decided

1. **The time has come to decide** (my #4: 「得時無怠，時不再來，天予不取，反為之災。」, `quoted`). In round 2 I left 1 and 3 to the owner (my #7: 「王無蚤圖」, `quoted`). The owner has now set a time box and asked for decisions, so I decide. I change two of my round-2 positions, on 3 and 5, and give the reason each time.

2. **Decision 3: c** (my #11: 「人自生之，天地形之，聖人因而成之」, `quoted`). My reading of it: the tool completes what the type checker has given form to, and does not invent what it has not.
   - The vision says the tool is TypeScript because opencode's calls "go through typed, injected services … which a syntax-only reader cannot follow". R2 links "to the declaration that the type checker establishes". c puts A2's "known" on that same ground.
   - In round 2 I had three objections to defining "known". 老子's round-2 wording removes two of them:
     - His place half ("a place is known when the given code or description points to it") answers my objection that it said nothing for a place found from a description.
     - He dropped the clause that contradicted his own cost line.
   - My third objection was that "the tool's method judges the tool". I now count that as a cost, not a reason to reject (my reading). c fixes what is in scope. L2's keys are still written by another agent using another method, with the type checker as the shared reference.
   - Against b: "established from repository source" rules out nothing in a TypeScript repository (my round-2 reason). Under b, A2 would fail on every dynamic call that a reader can trace, unless 1a's clause is added.

3. **Decision 1: b, read through c** (my #9: 「天地未形，而先為之征，其事是以不成」, `quoted`; my #10: 「無過天極，究數而止」, `quoted`).
   - **Targets the checker does not establish.** For a static reader, such a target has not taken form. Demanding it as a link is campaigning before the form shows (#9). Under c it is not "known", so its absence is not a miss.
   - **L1 already covers them.** L1 lists "dynamic behaviour" as a reason to stop, and it fails a branch that stops without a reason. That is stopping where the measure already stands (#10), and it is why I rejected proposal 6 in round 2.
   - **Links the checker does establish.** Their target is settled, so a `dynamic` mark on one is false and the link counts as missing. That is option b's own reason: "The link is known, so marking it dynamic is a miss."
   - **The COO's pair, 3c with 1a.** Together the line would read "a known [checker-established] link within the depth is missing with no limit at its site naming why".
     - I find no true reason for such a link to be missing within the depth. Depth is excluded by "within the depth". Round 2 agreed that a "seen" stop never hides a link.
     - So the clause would admit only false limits (my reading).
     - R2 would still catch a false mark on a service or interface call ("an implementation the lookup finds has no link"). Nothing would catch one on a direct call.
   - **If the owner picks 3b or 3a instead,** my round-2 conditional clause is needed, and I pick 1a.

4. **Decision 2: a** (my #10, as above, `quoted`).
   - Three of the four of us kept A2's unit sentence in round 2: "the place is level 0 and each link adds one level". A link is a call, a `new` or a service call (the spec's `Link.kind`). Entering a body written into a call is none of these.
   - The framework runs that body; the surrounding function does not call it (my reading). Counting the entry would add a second kind of step to the unit.
   - The brief's facts say most opencode function bodies are written straight into a call, and the spec reports that E1 found 17 of 18 calls in anonymous bodies. Under b, an agent working on use case 1 would find a function's own calls one level further away than it expects.
   - I do not rest this on the COO's "about half as far", which was not measured.
   - The new sentence goes into A2 because, without it, "a place of its own" invites the reading that entering it is a step.

5. **Decision 4: b** (my #5: 「天節固然，唯謀不遷。」, `quoted`).
   - The owner's words stand unless a found fault forces a change.
   - A5 already fails "an answer [that] lacks its evidence or limits". The spec's required limits ("no test-file pattern given", "fake rule not set (A3)", "no sibling rule given (A1)") are that answer's limits.
   - No case has found a required limit that A5 misses.
   - "A limit the interface requires" would make the requirement mean whatever the spec says next (my reading).

6. **Decision 5: b** (my #14: 「四封之內，百姓之事，蠡不如種也。四封之外，敵國之制，立斷之事，種亦不如蠡也。」, `quoted`). Each party is charged with what it does.
   - In round 2 I moved to one line and said two lines moved the requirement toward pieces. The spec settles it the other way. The evaluator "Reports MET, NOT MET or NOT CHECKED per requirement and per Fails-if line", and marks "the agent's part NOT CHECKED, pointing to P6". A line holding both duties would need two verdicts.
   - Linus, 孫子 and 老子 said in round 2 that two actor lines inside one requirement do not split it. I now agree: the body and the title stay one. This returns me to my round-1 choice.

7. **Decision 6: c** (my #9, as above; my #12: 「又觀其民之饑飽勞逸以參之」, `quoted`).
   - **What `throughFake` marks.** The spec says "`throughFake` is true when the path passes a `service-call` link whose candidates include a test fake". Fakes stay in `candidates`, and the link's `to` is the real implementation. So every test whose static path crosses such a service call is marked, including a test that provides the real service.
   - **Why the tool cannot tell.** It "has no rule for Effect service wiring", so it cannot see which layer a test provides. This is my reading of the spec; I did not check it in the code.
   - **What `exclude` does.** With 19 fakes at one call site, `exclude` drops every test through that site from *both* lists. That trips A3's own line "a test with a known path is missing", and it can turn a well-tested function into "none found".
   - **What `count` does.** It claims tests that swap in a fake. Linus and 老子 are right that such a test reaches the fake, not the real function.
   - **Why c.** Deciding either way before the form shows goes against #9. A count of the sure tests plus a separate list of the fake-path tests gives the agent a second signal to cross-check with (#12).
   - If `throughFake` in fact marks only tests whose path goes into the fake's code, those tests reach the fake and not the real function, and I pick a.

8. **Decision 7: c, with a's rule** (my #14, as above; applying it to the tool and the user is my reading).
   - A1 asks for "a fixed rule the user sets". A glob is fixed, and the evaluator can check it.
   - Each does what it is better at. The user, who knows the module, is better at choosing the group. The type checker is better at saying which files implement one interface or service tag. The tool is better at applying a glob exactly.
   - a's meaning is what use case 3 needs: a template for the next implementation of the same thing.
   - b gives a list of candidates, not a fixed rule. A shared export name is a weak sign that two files are the same kind (my reading, not measured).

9. **Decision 8: b in the tool, a on opencode** (my #14, `quoted`; my reading).
   - Whoever owns the repository decides what a test is there. A default in the tool would be the tool guessing.
   - For the run, a covers the folders the spec's case files already use (`packages/core/test/**`) and test-named files outside them.
   - The spec leaves this rule open for the owner (line 189), so this pick is provisional.

10. ***Proposed change to the pattern*** (my #12, `quoted`; the application is my reading).
    - **The problem.** Picks judged one at a time can each look right and still be wrong together. 3c plus 1a is that case.
    - **The change.** When two decisions in one question are linked, as 1 and 3 are here, the brief shows the requirement text the COO's picks produce together. The experts judge that combined text as well as each pick.
    - **What it changes.** One step: the COO writes the combined text before sending the question.

## What I need to know

1. **Does `throughFake` mark every test whose path crosses a service call with a fake among its candidates (my reading of the spec), or only tests whose path enters the fake?** If the first, 6 is c. If the second, 6 is a.
2. **When a call leaves the repository, does the tool show the link to the declaration the checker establishes and stop after it, or leave only a limit?**
   - My answer to 1 rests on the first. I read the spec's `ChainStep`, where a step holds its link and its `stop`, as showing the link.
   - If the tool leaves only a limit, then under c A2 fails on every library call. The missing-link line would then need an exception for a link that leaves the repository, never one for `dynamic`.
3. **Which interface or service tag do the siblings in each of the three A6 modules implement?** That is the COO's probe data, which I do not have. A module with no such group gets no table and carries the "no sibling rule given" limit.

The brief's facts (63 of 71, the 20-implementation site, the Effect body forms) carry no file:line. I took them as given by the COO. Only decision 6 leans on one of them, the 19 fakes.

## Costs and risks

- **3 → c** (my #11).
  - Some links can be seen only by reading the source, such as Effect service wiring the lookup misses ("The tool has no rule for Effect service wiring"). They can never fail A2. Only L1 guards them, by failing a call site that is dropped without a reason.
  - "Known" in A2 also differs from A1's "a known item". One word with two senses across the requirements can mislead a reader.
- **1 → b** (my #9). Any checker-established call that the tool marks `dynamic` fails A2. If the tool has a real reason I have not found, A2 goes NOT MET on it. The only such case I can see is question 2 above.
- **2 → a** (my #10). A body the framework runs later, elsewhere or never is shown at the same level as the calls of the function around it. The `from` field naming the body is the agent's only sign of this (Linus: ownership "does not establish that a framework invokes a callback").
- **4 → b** (my #5). If the evaluator reads "its limits" as stop limits only, a missing interface-required limit goes uncharged.
- **5 → b** (my #14).
  - The Fails-if strings change, so every case's `line` field must be re-mapped before a round can be read. 老子 counted ten cases for his own wording.
  - A2 and A5 stay "tool MET, agent NOT CHECKED" until P6 runs.
- **6 → c** (my #12).
  - Each `tests` answer gets longer by the fake-path list, which works against use case 4 on heavily used services.
  - The count becomes a floor (sure tests only), and the answer must say so.
  - The spec has no rule value for "list separately". Without one, the run must pass no rule and carry "fake rule not set (A3)", so on paper A3's "a fixed rule the user sets" is not met.
- **7 → c** (my #14). A glob does not follow the code. A new non-sibling file in the folder joins the table, and a new sibling outside the glob is missed. Each glob needs its interface or tag written beside it so the choice can be rechecked.
- **8 → a on opencode** (my #14). A real implementation in a `test/` folder, or named `*.spec.ts`, would be labelled a test fake. It would drop out of R2's resolution and turn its target unresolved.

## How we would know I was right

1. **Decisions 1 and 3: three fixture cases** (my #18: 「審備則可以戰乎？」, `quoted`, applied as examining the preparations first).
   - (i) A planted copy of the tool marks a direct call `dynamic` although the checker resolves it. A2's missing-link line must fail. Under the COO's 3c + 1a it would pass, and that pass is the hole.
   - (ii) A computed-member call `obj[k]()` with a `dynamic` limit at its site must pass both A2 and L1.
   - (iii) The same call with no limit must fail L1.
2. **Decision 2.**
   - On opencode, run `chain --down 6` from an entry whose calls sit in `Effect.gen` bodies. Compare the functions reached when entering a body counts as a level and when it does not. This measures the COO's "about half".
   - Every link's `from` names the body, never the surrounding function.
3. **Decision 6.**
   - Run `tests` on the real function behind the 20-implementation site three times: with `exclude`, with `count`, and with c's rule.
   - For each fake-path test the agent can read within the time box, check whether its file provides the real service or a fake.
   - Any test that provides the real service is one `exclude` would have hidden, and c was worth its tokens. If every one provides a fake, `exclude` was safe and c cost tokens for nothing.
4. **Decision 4.** A planted copy of the tool drops the "no test-file pattern given" limit. A5 must fail through "lacks its … limits". If it passes, I was wrong and the clause is needed.
5. **Decision 5.** The evaluator's report shows A2's tool line as MET or NOT MET and its agent line as NOT CHECKED → P6, separately. No case is charged to a line that no longer exists.
6. **Decision 7.** For each glob chosen on opencode, the type checker confirms that every matched file implements the named interface or tag. No file in that folder that implements it is left outside the glob.
7. **Decision 8.**
   - List the files that a's patterns match outside `test/` and `__tests__` folders, and read each one.
   - Compare R2's resolutions on opencode under `packages/core/test/**` and under a. Every resolution that changes must trace to a file that really is test code.
