# Linus Torvalds — Eight code-map decisions

## Answer

**My reading:** choose **1b, 2a, 3b, 4a, 5b, 6a, 7c, and 8b with a supplied by the opencode run**. These are provisional recommendations; decision 6 requires correcting the spec’s test-path classification before its results can support A3.

| Decision | My pick | One-line reason |
|---|---|---|
| 1 | **b — Yes, it is missing.** | An independently established link remains required for understanding logic; a `dynamic` label explains a limitation but does not restore the link. |
| 2 | **a — Entering the inline body adds no level.** | Lexical containment alone is not a call step; retain the body’s identity without spending depth on its placement. |
| 3 | **b — Established from repository source or type information.** | Evidence outside this tool’s successful lookup must be able to expose a missing relationship. |
| 4 | **a — Include interface-required limits explicitly.** | A focused answer needs required qualifications even when no branch stops early. |
| 5 | **b — Separate tool and agent failure lines.** | Each actor needs a checkable duty, while A2 and A5 each remain one requirement. |
| 6 | **a — `exclude`, for an established fake substitution.** | A test whose path substitutes a fake does not establish a path to the real function. |
| 7 | **c — Explicit sibling-group globs.** | Declared groups support the next-implementation template without making interface identity or matching export names universal definitions of siblings. |
| 8 | **b in the tool; a supplied by the run.** | Explicit patterns preserve user control while giving the opencode run a concrete, repeatable test-file rule. |

## How I decided

1. **My #5 and my #7 — decide provisionally and preserve reversibility.** The brief authorizes choosing now, subject to EJ’s later decision. Keep opencode’s fake, sibling and test-file selections in the run’s inputs. These recommendations do not establish measured improvements.

2. **My #3 and my #9 — decisions 1 and 3 follow the user’s work and the evidence.** Understanding logic and tracking changes require relationships that can be checked independently. Defining known links solely through the type checker would exclude source-established relationships from A2’s completeness obligation.

   If source or type evidence establishes the target, omitting that link fails A2 even with a `dynamic` limit. If the source establishes only a call expression, the target remains unresolved: show the site and its limitation without inventing a target. This preserves both A2 and L1. See [A2 and L1](/home/smoke01/dev/ancient-games/runs/20261014-code-map-vision-relay/result-trimmed.md:56).

3. **My #9 — decision 2 separates ownership from invocation.** An inline body owns its calls. Merely entering that body in the representation adds no level; an independently established call relationship adds a level. This does not authorize inventing callback invocation. The claim that the alternative halves useful reach remains **not measured**.

4. **My #13 — decision 4 addresses a concrete interface obligation.** Missing test-file patterns can require a limit even when traversal completes. Therefore L1’s early-stop obligation does not fully explain which limits A5 must carry. The explicit clause clarifies A5’s existing duty without adding another requirement.

5. **My #7; my reading — decision 5 makes incomplete verification visible.** Separate actor-labelled lines let a report distinguish tool behavior from agent behavior. Both remain inside the original requirement. A passing tool check cannot establish that an agent named rejected candidates or obtained the user’s module-map request.

6. **My #9 and my #2 — decision 6 needs evidence about the path.** The spec currently sets `throughFake` when **any candidate** is a test fake, while also retaining those candidates alongside real implementations and specifying no Effect wiring rule. See [candidate resolution](/home/smoke01/dev/ancient-games/runs/20261014-code-map-build/spec.md:94) and [test-path classification](/home/smoke01/dev/ancient-games/runs/20261014-code-map-build/spec.md:115).

   **My reading:** candidate membership does not establish substitution. With that predicate, `exclude` can discard a test that reaches the real implementation merely because another candidate is a fake. Keep the semantic choice `exclude`; where substitution cannot be established, report uncertainty and its limit rather than asserting either path.

7. **My #13 and my #5 — decisions 7 and 8 keep repository choices explicit.** Use shared interface or service-tag evidence to propose sibling groups, then pass their actual globs. Supply the stated test-folder and filename patterns explicitly. Neither selection becomes a universal tool default.

8. **My reading — requirement-quality check of these recommendations:**

   | Criterion | Assessment |
   |---|---|
   | Who decides | **Pass:** provisional choices here; run inputs record selections; EJ may overrule. |
   | One thing | **Pass:** each decision addresses one behavior; actor lines preserve whole requirements. |
   | Unit | **Pass:** depth counts call steps; A3 counts test cases. |
   | Can it fail | **Pass:** missing links, omitted limits and wrongly excluded tests provide counterexamples. |
   | Weak words | **FAIL pending evidence:** actual sibling membership and fake substitution are not established here. |
   | Level | **Pass:** provisional advice, not a claim of newly accepted requirements. |
   | Basis | **Pass for advice:** supplied requirements and spec; effectiveness remains unmeasured. |
   | Links | **Pass:** A2 completeness, L1 disclosure and A5 answer content retain distinct obligations. |

## What I need to know

- **Which concrete sibling groups and globs serve the three module maps?** If shared-interface evidence identifies the intended implementations, use it to propose the groups; otherwise the run needs explicit membership decisions.
- **What source evidence distinguishes actual fake substitution from candidate membership?** If available, apply `exclude` to that path. If unavailable, A3’s real-function reach remains undecided.

Neither question prevents making the provisional selections above.

## Costs and risks

- **1 and 3 — my #9:** independent source/type answer keys cost review time; more A2 results may remain NOT MET.
- **2 — my #9:** body identity must survive without fabricated invocation; traversal costs are **not measured**.
- **4 — my #13:** interface changes require corresponding review of applicable limits.
- **5 — my #7:** separate agent checks remain necessary; tool success cannot complete the verdict.
- **6 — my #2 and my #9:** substitution analysis needs additional evidence; the present predicate risks false exclusions.
- **7 — my #5:** explicit groups need maintenance as modules change.
- **8 — my #7:** naming patterns can miss unconventional tests; this run’s classification remains a stated assumption.

## How we would know I was right

**Proposed checks, authored by me; not run:**

- An independently established link omitted under `dynamic` fails A2; an unresolved target retains its site and limit without a fabricated link.
- Inline bodies retain their ownership, and lexical entry alone consumes no depth.
- Both output forms carry interface-required limits; agent duties receive separate observations.
- A real-service test remains included when unrelated fake candidates exist; an established substitution is excluded; uncertain wiring is disclosed.
- Sibling tables match the declared groups and support preparing the next implementation’s template and questions.
- L2 reports correctness, total tokens including map construction, and elapsed time against reading.

These checks would test the proposed behavior. Their passage alone would not establish answer-key independence or token savings on opencode.