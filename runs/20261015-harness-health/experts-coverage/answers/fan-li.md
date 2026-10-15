# 范蠡 (Fan Li) — Requirement Test Coverage and the 80% Target

## Answer
EJ's principle of reusing old cases and bounding test effort holds, but counting 80% over an unanchored AI-generated list of "all possibilities" breaks because an unstable denominator cannot measure true readiness; the 80% target should be counted over fixed acceptance criteria and their deltas, with all basic criteria strictly covered, while an independent reviewer rather than the author marks which edge cases may be left untested.

## How I decided

1. **What holds in EJ's process (reuse and bounded effort):**
   Reusing existing use cases first holds under my #16: 「計然之策七，越用其五而得意。既已施於國，吾欲用之家」 (`quoted`). Applying proven methods to new ground preserves accumulated strength. Examining existing defensive preparations before initiating new action also holds under my #18: 「審備則可以戰乎？」王曰：「巧。」 (`quoted`). Furthermore, setting a target and stopping rather than chasing every one-in-a-million edge case holds under my #10: 「無過天極，究數而止」 (`quoted`), and my #3: 「時不至，不可彊生；事不究，不可彊成」 (`quoted`). Forcing exhaustive coverage where returns vanish goes against natural limits (*my reading*).

2. **Where EJ's process breaks — Unbounded AI generation:**
   Generating "all possibilities" with AI breaks under my #3: 「必有以知天地之恆制」 (`quoted`). A check must rest on a constant measure. Attempting to force a complete list out of an engine breaks under my #7: 「彊索者不祥」 (`quoted`) and makes the outcome unknowable: 「其事又將未可知也」 (`quoted`).
   *Concrete breaking case:* On a requirement like "validate email address," an AI prompt produces 15 cases in one run (basic formatting) and 60 in another (obscure RFC 5322 comment-nesting variants). Testing 12 cases in the first run achieves 80% coverage while testing almost nothing challenging; in the second run, testing 12 cases yields 20% and falsely flags failure, whereas reaching 80% (48 cases) forces testing the very one-in-a-million edge cases EJ intended to skip (*my reading*). The percentage moves with generator noise rather than the requirement's real boundaries.

3. **Where EJ's process breaks — The unweighted denominator:**
   Counting 80% over an undifferentiated list of generated cases breaks because the volume of trivial variants can swamp core failure modes (*my reading*).
   *Concrete breaking case:* For a financial balance transfer requirement, an AI generates 20 trivial UI formatting variations and 2 concurrency race condition cases. An agent covers 18 trivial cases and reaches 18/22 = 81.8% coverage, satisfying EJ's 80% target while leaving the critical concurrency failure completely untested (*my reading*).

4. **Better approach — Grounding the denominator in constant measures and deltas:**
   Under my #3 (constant measures) and my #18 (examining defensive preparations):
   - First, check existing use cases against the requirement to determine what is already covered (the established base, my #16).
   - Second, define the denominator not as raw AI-generated scenarios, but as the explicit acceptance criteria or contract boundaries of the requirement (the constant measure, my #3).
   - Third, all basic criteria SHOULD have 100% coverage (the solid defense, my #18). The 80% target stays, but it should be measured over the permutations or interaction paths across those criteria (*my reading*).

5. **A check that would show this approach is better:**
   Plant a missing basic requirement (an unhandled error state) alongside 30 trivial passing variants (*my reading*). Under an unanchored 80% rule, 30/31 = 96.8% passes despite the missing basic check. Under the anchored approach requiring 100% coverage of basic criteria, the planted defect causes the check to fail, proving it cannot be spoofed by variant padding (*my reading*).

6. **Answer to the open question (who marks basic vs rare):**
   The main agent's proposal that the author marks cases while EJ only reviews rare cases breaks under my #17: 「固爲其能棄財故也。而長者不能，故卒以殺其弟，事之理也」 (`quoted`). A worker who must implement and test the cases has an inherent conflict of interest; like the eldest son who could not let money go, an author cannot be expected to judge impartially what they are excused from testing. They will naturally label difficult cases "rare" to satisfy the 80% target with minimal toil (*my reading*).
   Having EJ mark every case also breaks under my #14: 「四封之內，百姓之事，蠡不如種也。四封之外，敵國之制，立斷之事，種亦不如蠡也」 (`quoted`). The leader does not manage internal line items.
   Therefore, an independent reviewer agent SHOULD mark or audit the basic versus rare classification, and EJ reviews only the resulting list of untested rare cases to give business consent (*my reading*, combining my #14 and my #17).

## What I need to know

1. If the requirement arrives with formal acceptance criteria or only informal text: if formal criteria exist, the constant measure is derived directly from them; if only free-form text exists, an extraction step must establish the criteria before counting can occur (*my reading*).
2. If the execution environment has strict token or compute budget limits: if budget is severely constrained, the definition of "rare" must account for the cost of running canary tests versus the cost of an uncaught failure (*my reading*).

## Costs and risks

- **Cost of upfront criterion grounding:** Defining explicit criteria and delta-mapping against old use cases takes initial structuring time before running tests, rather than immediately prompting an AI for scenarios (from my #5: 「夫十年謀之，一朝而棄之，其可乎？」 (`quoted`) — disciplined planning takes patience; and my #3: 「事不究，不可彊成」 (`quoted`)).
- **Cost of independent review:** Introducing an independent reviewer to mark basic versus rare cases adds an extra agent pass and token cost (from my #14: dividing labor between 種 and 蠡 requires two distinct roles rather than one).
- **Risk of skipping rare cases:** Leaving 20% of edge variations untested means that rare anomalies will occasionally reach production, which must be accepted as the operational trade-off of stopping when the limit is reached (from my #10: 「無過天極，究數而止」 (`quoted`)).

## How we would know I was right

Run an eval where an implementation intentionally omits a basic boundary condition while an AI generator floods the suite with 40 trivial variations. If the evaluation pipeline rejects the test plan because a basic criterion is uncovered—despite the overall test count exceeding 80%—the grounded measure is proven right. If an author-marked plan misclassifies the omitted case as "rare" but the independent reviewer catches and flags it, the division of labor is proven right (*my reading*).
