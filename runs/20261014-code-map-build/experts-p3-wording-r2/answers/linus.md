# Linus Torvalds — Final A2 and A5 wording

## Answer

**My reading:** retain the source-or-type meaning of “known,” shortest-route depth, truthful call ownership, and explicit tool and agent duties within each whole requirement. Change my round-one A5 wording: keep early-stop obligations in L1, retain required limits in A5, and replace the list of excluded content with one boundary.

| Proposal | Final decision | Changed from round 1? | One-line reason |
|---|---|---|---|
| 1 | **Accept.** Separate tool and agent failure lines within A2. | No substantive change | Understanding logic requires complete candidates and an agent’s explicit selection; checking either actor alone is insufficient. U1, U4. |
| 2 | **Accept with this wording:** Known places and links are those established from repository source or type information. | No | Evidence determines what is known; the tool’s success at resolving it does not. U1, U2, U4. |
| 3 | **Accept with this wording:** Each link names the nearest body holding the call. A body written straight into a call is a place of its own; unresolved links carry limits. | No | A visible body must not disappear because it lacks a holder; lexical ownership does not prove callback invocation. U1, U4. |
| 4 | **Accept with this wording:** Include every known link within the depth through its shortest route; a reference back never hides such a link. | Wording shortened following 范蠡; decision unchanged | Source order must not change the reported relationships when tracking changes. U1, U2. |
| 5 | **Accept with this wording:** Reject content outside the requested result, its evidence, applicable limits and ambiguity candidates, wherever it appears. | Generalized following 范蠡 | Necessary evidence remains allowed; a correct answer followed by a dump fails. U4. |
| 6 | **Accept with this wording:** Applicable limits include those the interface requires for that command. | Yes—narrowed following 范蠡 | L1 already governs early stops; “whole answer” adds no needed protection and can mislead about completeness. U1, U3, U4. |
| 7 | **Accept with this wording:** The tool returns a whole module map only for `map`; the agent runs `map` only when the user asks for a module map. | No | Focused answers legitimately contain links and definitions; “map content” would prohibit necessary results. U1, U3, U4. |
| 8 | **Accept.** Apply A5 to JSON and default text. | No | The default text is the agent’s working interface. U4. |
| 9 | **Accept with this wording:** The answer contains the requested result, supporting evidence, applicable limits and ambiguity candidates, and no other content, in any section or inside the result. | Yes—replace my enumerated exclusions, following 范蠡 | A fixed list can miss the next kind of surplus content. U1, U3, U4. |

**Merged:** 5, 8 and 9 form A5’s content-and-form boundary. The retained part of 6 defines its applicable limits. Proposal 7 names the tool and agent duties without creating separate requirements.

**A2 The call chain through one place.** Given code or a description, the tool locates the place and returns its caller and callee chains, counted in levels from the place. Known places and links are those established from repository source or type information. The user sets the depth each way; when the user does not, it is six. The place is level 0; each call link adds one level. A link is within the selected depth if it can be reached from the place, in that direction, using no more than the selected number of call links. Every known link within that depth is included.

When more than one place matches, the tool flags the match as ambiguous and lists every matching candidate with its location; the agent picks the place that fits the question best, builds its chain, and names every other candidate it did not build. Each link gives its kind and location and names the nearest function, method or arrow body that holds the call. A body written straight into a call is a place of its own; its calls are never shown as calls by the function that surrounds it. Unresolved links into or out of that body carry stated limits. A function reached twice is shown once, with a reference back; the reference never hides a known link within the depth through a shorter route.

**Fails if:** any of these happens:

- a known place is not found;
- the tool does not flag an ambiguous match, or leaves a matching candidate unlisted or without its location;
- the agent treats an ambiguous match as certain, or does not name a candidate it did not build;
- a known link within the depth is missing, including one hidden behind a reference back, or a shown link contradicts the code, including naming the surrounding function as the caller of a call held by another body;
- a link lacks its kind or location;
- a function reached twice is shown twice, or its reference back is missing or does not identify where it is shown.

**A5 One question, one answer.** A specific question gets that answer with its evidence and limits, not a whole-map dump. The answer contains the requested result, its supporting evidence, applicable limits including those the interface requires for that command, and any candidates needed to resolve ambiguity. It contains no other content, whether in another section or inside the requested result. This holds for JSON and the default text the agent reads. A whole map is produced only when the user asks for a module map: the tool returns a whole module map only for `map`, and the agent runs `map` only when the user asks for a module map.

**Fails if:** any of these happens:

- the tool returns an answer inside a dump, includes content outside the requested result, its supporting evidence, applicable limits and ambiguity candidates, or omits required evidence or limits, in JSON or default text;
- a command other than `map` returns a whole module map;
- the agent runs `map` without the user’s request for a module map.

## How I decided

1. **My #3 — judge the agent’s resulting work.** The Vision names understanding logic, tracking changes and preparing sibling implementations. A missing relationship can corrupt that work; surplus content spends the tokens the map is meant to save. These outcomes support A2’s completeness and A5’s content boundary. Passing the evaluator alone does not establish either outcome on opencode.

2. **My #9 — distinguish evidence from the tool’s method.** 范蠡 argues that proposal 2 would make “the tool’s method the judge of the tool.” That objection holds against defining known as whatever this tool resolves. It does not defeat my broader source-or-type wording: an independently prepared answer key can establish a source relationship that the tool misses.

   孫子’s wording, “a link is one the type checker establishes,” is too narrow for the requirement as a whole. The [interface](/home/smoke01/dev/ancient-games/runs/20261014-code-map-build/spec.md:27) also supports finding places through code, comments and strings. R2 already specifies what type-based declarations and implementation lookup establish; A2 must preserve that distinction.

   **My reading:** a `dynamic` limit does not excuse omission of a link established by source or type evidence. Conversely, knowing that a call expression exists does not establish its runtime target. If the target is unresolved, report that limit; do not fabricate an implementation link.

3. **My #9 — preserve ownership without inventing invocation.** I agree with 范蠡’s “no ‘or a stated limit’” for identifying the body itself. The source contains that body. A limit may explain an unresolved connection, but it cannot replace a known body merely because the body has no holder.

   I hold against 老子’s suggestion that `belongsTo` necessarily contradicts the nearest-body rule. The current code uses `belongsTo` to select calls for an answer and `enclosingNode` to identify each link’s caller. Those are different relationships. A surrounding function’s answer may include a nested body’s calls while truthfully naming that body as caller. The [recorded inline-owner case](/home/smoke01/dev/ancient-games/code_map/eval/COVERAGE.md:244) passes. This round need not prohibit that grouping.

   No extra chain level follows merely from lexical nesting. Each level requires a call link; ownership alone does not establish a callback invocation.

4. **My #3 and my #9 — choose shortest-route depth.** The recorded failure loses a depth-three link when a longer route reaches the shared function first. Reversing source order restores it. That would make a source reorder look like a change in logic, undermining U2.

   I accept shortest-route depth as this round’s decision. I do not claim EJ previously stated it explicitly. 范蠡’s shorter formulation expresses the result without prescribing traversal machinery. The price is an implementation repair, not necessarily a rewrite.

5. **My #7 and my #19 — keep both actors accountable within one requirement.** 孫子 says to “reject the tool/agent split in 1 and 7.” I disagree if that means retaining an indistinguishable failure line. Separate actor lines make the missing evidence visible while leaving A2 and A5 whole.

   My #19 is **attributed** kernel process guidance about independently understandable changes; applying it to requirement readability is **my reading**. It does not establish a rule about how many lines a requirement may contain. Tool checks establish tool behavior; agent integration checks establish selection, candidate naming and whether `map` was requested.

6. **My #13 — remove duplication that solves no additional problem.** 范蠡 changed my decision on proposal 6 with: “Stopping short is already L1’s.” That is supported by L1’s explicit coverage of every answer or branch that stops early. I therefore remove my repeated cap/sample/page sentence and “whole answer,” retaining the clarification that interface-required limits belong in A5.

   老子’s concern about `find` dropping lower-scoring matches does not require a second stopping rule. The interface expressly permits ranked matches. Whether that ranking fulfills the requested search is a search-contract question; undisclosed early termination is already governed by L1.

7. **My #10 and my #13 — use one content boundary.** 范蠡 also changed my proposal 9: “A fixed list of excluded kinds goes stale.” I agree. The permitted content gives the boundary; everything outside it fails, whether it is a separate section or hidden among requested items.

   I hold against 孫子’s retained “map content” prohibition. Call links are map content and also necessary focused results. U1 and U4 therefore require “whole module map.” Command/query identification and resolution or empty-result status belong to the requested result; they are not surplus content.

8. **My reading — requirement-quality check.** These judgments apply to the final wording together with the supplied interface.

   | Criterion | A2 | A5 |
   |---|---|---|
   | Who decides | **Pass:** user sets depth; agent selects; source/type evidence establishes relationships | **Pass:** question and command define scope; user requests a module map |
   | One thing | **Pass:** answering a chain request | **Pass:** answering a specific question |
   | Unit | **Pass:** depth counts call links | **Pass:** no unspecified numerical unit |
   | Can it fail | **Pass:** omit a known link or candidate | **Pass:** append surplus content or omit a required limit |
   | Weak words | **Pass:** known, ownership and depth are defined | **Pass:** permitted content replaces an undefined dump boundary |
   | Level | **Pass:** product acceptance conditions | **Pass:** product acceptance conditions |
   | Basis | **Pass:** Vision, interface and recorded route failure | **Pass:** Vision, interface and confirmed surplus-output false pass |
   | Links | **Pass:** preserves R2 and L1 | **Pass:** preserves A2’s candidates and L1’s stopping obligation |

9. **My #2 and my #7 — distinguish inspection from verification.** I read the allowed source and reports; I did not rerun the tool. Codex wrote the strengthened evaluator checks and the [coverage record](/home/smoke01/dev/ancient-games/code_map/eval/COVERAGE.md:214). That record supports the reported fixture failures; it does not independently establish answer-key correctness, opencode behavior or token savings.

## What I need to know

None for these wording decisions. The sources settle ownership and the distinction between unresolved and fabricated links; this round authorizes recommending shortest-route depth. No anonymous-body display name needs to be fixed in A2.

## Costs and risks

- **1 and 7 — my #7:** separate tool and agent evidence is required. Neither whole requirement is established by tool checks alone.
- **2 — my #9:** independent source/type answer keys cost review time. A `dynamic` label cannot become a blanket exemption.
- **3 — my #9:** anonymous bodies require stable locations and truthful ownership. Correct ownership still does not solve callback invocation.
- **4 — my #9:** traversal must retain links available through shorter routes while avoiding duplicate function expansions. Runtime and memory costs are **not measured**.
- **5, 8 and 9 — my #3:** content checks need valid-answer controls so they preserve supporting evidence, candidates and result metadata. A rigid shape check can reject a useful answer.
- **6 — my #13:** keeping stopping semantics in L1 reduces duplication but requires reviewers to apply both requirements.
- **All proposals — my #18, attributed:** wording and case mappings need coordinated updates. Correctness gains and token savings remain **not measured** on the Vision’s real questions.

## How we would know I was right

- Upward and downward shorter-route cases retain every in-depth link in either source order, with one full showing per function and valid references back.
- Inline-body links name the nearest body. Missing callback-invocation evidence produces a limit, never an invented edge.
- A source-established link omitted under a blanket `dynamic` label fails A2; a genuinely unresolved target remains explicitly unresolved.
- JSON and default text reject surplus content both beside the answer and inside it, while accepting necessary evidence, candidates and interface-required limits.
- A silent early stop fails L1. Reporting a stop does not make a missing known in-depth link pass A2.
- Tool checks and agent integration checks separately exercise their stated duties.
- L2’s comparison on the Vision’s questions establishes whether the resulting answers save tokens against reading and grepping. Fixture success alone cannot establish that.