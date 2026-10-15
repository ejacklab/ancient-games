# Linus Torvalds — Which comes first?

## Answer

**My reading, applying my #13, #3 and #5:** for a new product, start with a concrete user situation, write a minimal vision, derive requirements, then generate and check use cases against those requirements. This is a loop: it closes for the proposed work when the artifacts agree, the checks demonstrably reject wrong results, and EJ has decided the remaining scope choices; an existing settled vision need not be rewritten first.

## How I decided

1. **Start with the immediate problem — my #13 and #3.**

   My #13 favours solving an immediate need; my #3 judges breakage through the user’s workflow. Applied here, that means identifying someone trying to accomplish something before expanding a product description.

   **My reading:** distinguish an observed situation used to discover the problem from generated cases used to test a requirement. The former can precede requirements; the latter depend on requirements defining what counts as wrong.

   This distinction needs EJ’s agreement if R11.1 currently covers every kind of use case.

2. **Use the vision to choose which problems belong — my #13 and #7.**

   After the concrete situation, record who the product serves, the problem, its exclusions and the intended observable result. Keep it open to correction.

   **My reading:** the vision gives a reason to accept or reject candidate requirements. It does not establish that the product works. Conversely, an interesting use case does not establish that it belongs in this product.

3. **Write requirements before expanding acceptance cases — my #9 and #2.**

   My #9 concerns data and relationships in code. **My reading by analogy:** define the relationships among requirement, behaviour unit and supporting case before generating a large collection.

   EJ’s existing approach fits here: receive a requirement, identify its fixed behaviour units, check existing cases, then generate additional cases. A generated case can reveal a missing requirement, but that becomes a proposed revision; it cannot silently enlarge the coverage denominator.

   The supplied trial supports that distinction locally. It does **not** establish that this ordering produces better products.

4. **Give each artifact one maker and a check — my #6 and #11; the following allocation is my reading.**

   These are proposed responsibilities, subject to EJ’s choice of workers:

   | Artifact, in working order | One maker | Check before building on it |
   |---|---|---|
   | Initial use case | EJ writes the concrete situation | Identify the actor, starting conditions, attempted action and observable outcome. Flag invented details. A case lacking an outcome fails. |
   | Vision | One designated agent records only what EJ has supplied | Trace each claim to EJ’s stated intent. An agent-invented audience or a contradiction of an agreed exclusion fails. Unresolved product choices return to EJ separately. |
   | Requirements | One designated requirement worker | Check each requirement against the vision and use case; identify its behaviours, failure condition, check and decider for open choices. A behaviour with no way to detect its violation fails. |
   | Generated use cases | One designated case worker; EJ’s existing cases remain their separate artifact | Attach each case to a fixed behaviour unit. Cases contradicting settled decisions fail review. Existing checks count only after detecting a planted violation. |

   These checks are **proposed by me**, not independently validated. Traceability can establish consistency with recorded intent; it cannot establish that the intent solves a worthwhile problem.

5. **Revise where the contradiction originates — my #5 and #7.**

   A case exposing an unclear outcome sends the requirement back for revision. A requirement outside the product’s purpose sends the scope choice to EJ. Evidence that the purpose itself is wrong sends the vision back to EJ.

   **My reading:** close the loop for the selected work when those contradictions are resolved, the agreed coverage target is met over fixed units, and EJ has decided exclusions by consequence. The supplied 80% target alone does not justify a particular omission. New contrary evidence reopens the relevant artifact.

6. **Use cases first holds in discovery; it breaks as an unconditional rule — my #13, #3 and #1.**

   **Where it holds — hypothetical:** a person resumes a task after an interruption and cannot recover why the previous decision was made. Recording that situation first gives a concrete problem from which to write a vision and requirements. The price is possible overfitting to that person’s workflow.

   **Where it breaks — hypothetical:** an existing product has an agreed requirement that one user cannot retrieve another user’s private records. Generating a convenience case that retrieves those records cannot authorize the behaviour. Start from the settled constraint, then derive cases that exercise it. The price is that legitimate new needs may require reopening the constraint rather than immediately designing a feature.

7. **Evaluate the proposed prerequisite before adopting it — my reading, using requirement-check.**

   For the proposal that all three artifacts precede work design:

   - **Who decides — FAIL:** who determines that each is ready?
   - **One thing — pass:** it describes one readiness event.
   - **Unit — pass:** the artifacts counted are vision, requirements and use cases.
   - **Can it fail — FAIL as an operational gate:** absence is detectable; adequate content is undefined.
   - **Weak words — FAIL:** the boundary of *before work is designed* needs clarification.
   - **Level — FAIL against the supplied house rule:** an unconditional method gate conflicts with SHOULD as the maximum method level.
   - **Basis — pass as a stated preference:** effectiveness remains unmeasured.
   - **Links — pass:** requiring their presence does not itself establish an order.

## What I need to know

- Does *use cases first* mean recording observed user situations, or generating acceptance cases—and does R11.1 cover both?
- Who decides readiness, and does the prerequisite apply before exploratory investigation or before committing to an implementation design?
- Is the prerequisite an overridable SHOULD, consistent with the supplied house rule, or is there a particular safety bound behind an unconditional gate?

## Costs and risks

- **My #13:** beginning with a concrete need limits speculative design, but can overlook other users.
- **My #5 and #7:** revision keeps decisions reversible, but consumes review time and may invalidate completed work.
- **My #6:** named makers reduce EJ’s drafting burden, but their domain competence still needs scrutiny.
- **My #2 and #18 (`attributed`):** meaningful checks and measured comparisons cost effort. Document agreement and coverage percentages can still hide an incorrect understanding of the user.

## How we would know I was right

**My reading from my #2 and #18 (`attributed`), not measured:** compare this order with the current approach on comparable work, recording clarification time, requirement revisions after design begins, and missed user outcomes.

Exercise the proposed checks with planted defects: an invented vision claim, a requirement outside agreed scope, a case contradicting a settled decision, and a check that accepts a violated requirement. Record whether each is caught before dependent work proceeds.

The checks above are mine; passing them would demonstrate their ability to catch those defects. Evidence favouring the ordering would require fewer late corrections or missed outcomes at a cost EJ considers worthwhile.