# Linus Torvalds — A2 and A5 wording

## Answer

**My reading:** accept the clarifications below, keeping A2 and A5 whole and retaining the agent’s duties. Merge proposals **5, 6, 8 and 9** into one A5 boundary; revise proposal **7** so it does not prohibit focused answers from containing definitions or links.

| Proposal | Decision | Use case | One-line reason |
|---|---|---|---|
| 1 | **Accept** | 1, 4 | Explicit tool and agent duties preserve the complete interaction without pretending a tool check verifies both. |
| 2 | **Accept with this wording:** Known places and links are those established from repository source or type information. | 1, 2, 4 | The type checker alone is too narrow for finding written code, comments and strings; its declarations also do not prove runtime implementations. |
| 3 | **Accept with this wording:** A call inside a function, method or arrow belongs to that nearest body. A body written straight into a call is a place of its own; unresolved links carry limits. | 1, 4 | Anonymous ownership must remain truthful; anonymity alone does not justify omitting a known body. |
| 4 | **Accept**, adopting shortest-path reachability for depth | 1, 2, 4 | Reordering source must not change which links are within the requested depth. |
| 5 | **Accept with this wording:** An answer fails if it includes unrelated definitions, links, flows or tables, whether beside the answer or inside its payload. | 4 | Unasked sections is too broad: evidence, limits and ambiguity candidates are necessary parts of some answers. |
| 6 | **Accept** | 1, 3, 4 | An undisclosed cap or sample can mislead the agent about logic or sibling differences. |
| 7 | **Accept with this wording:** The tool returns a whole module map only for `map`; the agent runs `map` only when the user asks for a module map. | 1, 3, 4 | Map content includes things focused commands must legitimately return; whole module map states the actual boundary. |
| 8 | **Accept** | 4 | The default text is the agent’s interface and needs the same protection as JSON. |
| 9 | **Accept** | 1, 3, 4 | Relevant content belongs in the answer; unrelated material fails wherever it is placed. |

**Final A2**

**A2 The call chain through one place.** Given code or a description, the tool locates the place and returns its caller and callee chains, counted in levels from the place. Known places and links are those established from repository source or type information. The user sets the depth each way; when the user does not, it is six. The place is level 0; each call link adds one level. A link is within the selected depth if a path from the place in that direction reaches it in no more than that number of call links. Every known link within the selected depth is included regardless of traversal order.

When more than one place matches, the tool flags the match as ambiguous and lists every matching candidate with its location; the agent picks the place that fits the question best, builds its chain, and names every other candidate it did not build. Each link gives its kind and location. A call inside a function, method or arrow belongs to that nearest body, which the link names as the caller. A body written straight into a call is a place of its own; its calls are never attributed to the function that surrounds it. Any unresolved link into or out of that body carries a stated limit. A function reached twice is shown once, with a reference back, without losing links reachable through a shorter path.

**Fails if:** any of these happens:

- a known place is not found;
- the tool does not flag an ambiguous match, or omits a matching candidate or its location; or the agent treats an ambiguous match as certain or fails to name a candidate it did not build;
- a known link within the depth is missing, or a shown link contradicts the code, including naming the surrounding function as the caller of a call inside another body;
- a link lacks its kind or location;
- a function reached twice is shown twice, or its reference is missing or does not identify where it is shown.

**Final A5**

**A5 One question, one answer.** A specific question gets that whole answer with its evidence and limits, not a whole-map dump. The answer contains the requested result, its supporting evidence, applicable limits and any candidates needed to resolve ambiguity. It excludes unrelated definitions, links, flows and tables, whether they appear in another section or inside the requested payload. Where the answer stops short — a cap, a sample, a first page — it carries the limit that says so. A limit the interface requires for that command is part of the answer. This applies to JSON and default text output. The tool returns a whole module map only for `map`; the agent runs `map` only when the user asks for a module map.

**Fails if:** an answer includes unrelated definitions, links, flows or tables, whether beside the answer or inside its payload; lacks its evidence, applicable limits or interface-required limits; stops short without stating that limit; a command other than `map` returns a whole module map; or the agent runs `map` without the user’s request for a module map.

## How I decided

1. **My #3 — judge the agent’s resulting work.** The relevant outcome is whether the agent can understand logic, track changes and prepare the next sibling implementation. Passing a narrower checker does not establish that outcome. The source for this rule distinguishes user workflow failures from changed test behaviour. Applying it to these requirements is **my reading**. [Regression guidance](https://docs.kernel.org/process/handling-regressions.html)

2. **My #9 — preserve relationships before choosing traversal machinery.** The graph must retain caller, call site, target and reachability together. The [current traversal](/home/smoke01/dev/ancient-games/code_map/src/commands.ts:312) stops expanding a function whenever it has already been seen, without considering the remaining depth. That explains the reported longer-route-first failure. I accept proposal 4’s shortest-path interpretation as this round’s wording decision; I do not claim EJ previously stated that interpretation explicitly. The rule’s source favours designing around data and its relationships; it does not prescribe a particular graph algorithm. [Git mailing-list source](https://marc.info/?l=git&m=115401850825206&w=2)

3. **My #9 and my reading — separate evidence from implementation certainty.** Proposal 2’s original wording would make the type checker the sole boundary of what can be known. But [search](/home/smoke01/dev/ancient-games/code_map/src/commands.ts:73) also uses written source, while R2 explicitly distinguishes declarations, implementations and unresolved targets. Source-or-type evidence fits the Vision without relaxing R2. For proposal 3, lexical ownership identifies the caller; it does not establish that a framework invokes a callback. Missing invocation evidence therefore needs a limit, not an invented edge. The [spec](/home/smoke01/dev/ancient-games/runs/20261014-code-map-build/spec.md) already establishes nearest-body ownership. A2 need not fix the anonymous body’s display name.

4. **My #3 and my #9 — define relevance by the question.** A callee outside the queried file can be necessary evidence. Ambiguity candidates can be necessary before any chain is built. Proposals 5 and 7, taken literally, risk forbidding both. That conflicts with use cases 1 and 4, so those use cases win. Proposal 9 supplies the better boundary: exclude unrelated material, wherever it appears.

5. **My #7 — preserve duties and expose uncertainty.** Proposals 1 and 7 clarify who acts; they do not justify deleting the agent’s obligations. Likewise, proposal 6 requires disclosure of incompleteness without making every disclosed omission acceptable. A known link missing within A2’s depth still fails A2, even if A5 reports the omission. This application is **my reading**; the rule’s source supports acknowledging uncertainty, rather than presenting confidence as evidence. [Management-style source](https://docs.kernel.org/process/management-style.html)

6. **My reading — requirement-quality check.** Evaluating the original wording with the supplied interface, then the proposed text:

   | Criterion | A2 | A5 |
   |---|---|---|
   | Who decides | **FAIL → Pass:** evidence boundary and actor duties explicit | **FAIL → Pass:** content boundary and actor duties explicit |
   | One thing | **Pass:** answering a chain request | **Pass:** answering a specific question |
   | Unit | **Pass:** depth counts call links | **Pass:** no missing numerical unit |
   | Can it fail | **Pass:** omit a known link or candidate | **Pass:** append unrelated material or hide truncation |
   | Weak words | **FAIL → Pass:** known, ownership and depth clarified | **FAIL → Pass:** dump boundary clarified |
   | Level | **Pass:** product acceptance condition | **Pass:** product acceptance condition |
   | Basis | **Pass:** Vision, interface and reported failure | **Pass:** Vision, interface and demonstrated false pass |
   | Links | **Pass:** preserves R2 and L1 | **Pass:** preserves command-required limits and A1’s map |

   These are recommendations for this round, not a claim that EJ has accepted the revised requirements.

7. **My #7 and my #18 — state the evidence’s limits.** Codex wrote the strengthened evaluator checks. Its [coverage report](/home/smoke01/dev/ancient-games/code_map/eval/COVERAGE.md:214) records the actual tool failing both longer-route-first cases and passing their reversed counterparts. I inspected that report and the code; I did not rerun the checks here. Those fixtures do not establish correctness on opencode. My #18 is **attributed** kernel process guidance, not verified personal wording by Linus; it calls for explicit costs and supported improvement claims. [Submission guidance](https://docs.kernel.org/process/submitting-patches.html)

## What I need to know

None for this round’s wording decisions. No new use case, cap, performance target or anonymous-body naming convention is needed.

## Costs and risks

- **Proposals 1 and 7 — my #7:** tool checks and agent integration checks need separate evidence. Keeping both duties means the whole requirement remains unchecked until both are exercised.
- **Proposal 2 — my #9:** expected places and links need source or type evidence independent of the tool’s own answer. Preparing those keys costs review time.
- **Proposal 3 — my #9:** anonymous bodies add places and may change chain levels. Correct ownership alone does not solve callback invocation.
- **Proposal 4 — my #9:** traversal must preserve work available through shorter routes while keeping one full expansion per function. Its runtime and memory costs are **not measured**.
- **Proposals 5, 8 and 9 — my #3:** relevance checks need positive controls for legitimate supporting material. Overly rigid checks could reject useful evidence or harmless formatting.
- **Proposal 6 — my #18, attributed:** completeness and explicit limits may increase output. Token savings remain **not measured** until L2’s comparison; disclosure cannot substitute for required results.

## How we would know I was right

- The upward and downward shorter-route cases include the depth-three tail in either source order, while shared functions appear once with valid references.
- Inline-body cases identify the nearest body as caller, retain established links, and report unresolved invocation without inventing it.
- Ambiguous searches list every candidate and location; an agent check separately verifies selection and naming of the others.
- JSON and default text reject unrelated material both beside the answer and inside its payload. Valid evidence, candidates and required limits remain accepted.
- Silent caps fail; stated limits accurately identify where the answer stops. A missing known A2 link still fails.
- Non-map commands cannot return a whole module map, and an agent check rejects an unasked `map` invocation.

These observations would support the wording on the exercised cases. L2 is still needed to establish whether the tool saves tokens on the Vision’s real questions.