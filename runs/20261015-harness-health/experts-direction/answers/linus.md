# Linus Torvalds — Use cases, requirements and vision

## Answer

**My reading:** EJ’s direction holds as a way to discover the work: start with their actual situation, let AI suggest additions, and let EJ decide scope. It breaks if merely writing a requirement makes it binding, or if counting accepted use cases replaces R11.1 without fixing what each counted unit means.

## How I decided

1. **Start with the user’s working result — my #3 and my #13.**

   Applying these rules beyond their original software context is **my reading**. Starting with an actual need gives the discussion something concrete to answer.

   **Hypothetical case:** EJ needs to reopen a saved report. A proposed implementation satisfies its new file-format specification but cannot open their existing reports. The specification being satisfied does not repair the broken workflow.

   I would keep the actual situation and expected outcome visible through implementation. The check is to perform that situation with the resulting product, including the previously working path. The price is maintaining representative examples.

   Vision can guide suggestions; it does not establish that a proposed feature is wanted. Evidence may justify asking EJ to revise their vision; it does not authorize the agent to revise it.

2. **Separate a proposal from an obligation — my #9; the authority distinction is my reading.**

   The main agent’s restatement mostly preserves EJ’s direction, but step 5 resolves something EJ has not settled: whether a requirement becomes binding through **existence** or through **acceptance**.

   **Hypothetical case:** an agent proposes alphabetical report ordering. Merely placing that sentence in a requirements file should not silently authorize changing EJ’s existing ordering.

   I recommend treating AI-generated requirements as proposals until the designated decision-maker accepts them. EJ has explicitly retained decisions about additional use cases; authority over proposed requirements remains open.

   The check is to insert an unaccepted proposal and verify that it cannot justify a product change. The price is an explicit acceptance decision.

3. **T1: existence and obedience can be different questions — my #9 and my #16; this interpretation is my reading.**

   EJ’s wording can mean that a separate requirements document is optional, while accepted requirements govern the result. That is coherent **if that is what they intend**.

   But acceptance alone does not establish a requirement’s level. Under the supplied house rule, a method default remains SHOULD, with a stated reason for overriding it; a safety bound may earn MUST. Neither use cases nor requirements acquire a blanket level through their document type.

   **Hypothetical case:** exporting a report succeeds, but includes another user’s private rows. A successful ordinary example does not establish that an access constraint holds. Requirements can express restrictions across many situations; they are not necessarily minor details.

   I would distinguish optional documentation, accepted product behavior, and each rule’s level. Check those distinctions by presenting an unaccepted suggestion, an overridden method default, and a violated accepted safety bound. They should receive different judgments. The cost is recording those distinctions.

4. **T2: a frozen list fixes a snapshot, not the meaning of coverage — my #9 and my #2.**

   The main agent is partly right: once EJ accepts and freezes a list, the generator cannot directly change its denominator. But acceptance does not establish consistent granularity.

   **Constructed counterexample:** one accepted case covers exporting CSV and JSON. CSV works; JSON fails. If a case passes only when its whole outcome works, that is **0/1 cases passed**. Split the same scope into two accepted cases and it becomes **1/2**. The product has not changed.

   R11.1 avoids that problem by fixing behavioral units before generating evidence. The supplied n=1 trial supports that distinction in one instance; it does not establish that accepted-case counts are equivalent.

   I recommend retaining R11.1 as written. With no requirement supplying its units, report the accepted outcomes and their evidence individually; do not silently label a use-case percentage as R11.1 coverage. EJ could instead authorize extending unit extraction to accepted use-case text and its failure conditions.

   The check is whether splitting or paraphrasing cases changes the behavioral denominator without changing scope. The price is defining units—or temporarily having no aggregate percentage. The existing 80% remains a target, not permission to disregard a known failure.

5. **T3: authorship and approval are different acts — my #9 and my #11; the artifact interpretation is my reading.**

   An AI-written suggestion remains AI-written when EJ accepts it. Their acceptance is a separate decision, not joint authorship of the suggestion.

   Their own observed case can remain their artifact; an agent’s proposed case can remain the agent’s artifact; EJ’s acceptance can remain their decision. If a consolidated specification is needed, one designated writer can produce it from those inputs.

   The check is whether a reader can distinguish the proposed content from the decision accepting its exact version. Approval of an earlier version does not approve a later edit.

   The price is preserving that connection. Authorship and approval history can live in the run evidence, without putting conversation into the product requirements.

6. **The central validity rule is not complete yet — my #7; applying the eight-question checklist is my reading.**

   For the proposed rule that results satisfy accepted use cases:

   | Criterion | Assessment |
   |---|---|
   | Who decides | **FAIL:** EJ decides added scope; who judges disputed validity or requirement conflicts remains open. |
   | One thing | **Pass:** it concerns whether a result satisfies an accepted case. |
   | Unit | **Pass for individual judgment:** no percentage is specified here. Aggregate coverage needs its own unit. |
   | Can it fail | **FAIL as written:** a wrong result can be imagined, but the case’s expected result and rejection condition are unspecified. |
   | Weak words | **FAIL:** validity needs an observable meaning for each case. |
   | Level | **FAIL:** a blanket must does not distinguish product commitments from method defaults or safety bounds. |
   | Basis | **Pass as a stated user proposal:** effectiveness remains unmeasured. |
   | Links | **FAIL:** precedence between a case and a conflicting requirement is unresolved. |

   I would complete those meanings with EJ rather than supply them myself. The check is whether two reviewers can judge the same deliberately wrong result using the written criterion. The price is resolving ambiguities before claiming success.

7. **Try the clarification before making it universal — my #5, my #13 and my #18 (`attributed`).**

   I recommend applying the clarified direction to the next actual task while preserving existing decisions and evidence. Compare what it exposes: missed outcomes, conflicting instructions, unapproved additions, review effort, and rework.

   No improvement threshold has been supplied; I would not invent one. This trial costs attention and may reveal that some proposed recordkeeping adds no useful distinction.

## What I need to know

- Does EJ mean that **separate requirements documentation is optional**, while accepted behavior remains binding? Who accepts proposed requirements and decides conflicts with use cases?
- What observable outcome and rejection condition make each basic use case valid, and who settles a disputed judgment?
- When no requirement exists, should R11.1 remain unavailable, or should its fixed-unit method be extended to accepted use-case text?

## Costs and risks

- **My #3 and my #13:** concrete examples keep work grounded, but ordinary examples can miss restrictions across situations.
- **My #9 and my #11:** separating proposals from decisions prevents silent authority changes, but adds recordkeeping and version references.
- **My #2 and my #18 (`attributed`):** stable behavioral units make coverage interpretable, but require effort and do not prove the units are complete.
- **My #5 and my #7:** a reversible trial limits commitment, but passing one trial does not establish a general method.

## How we would know I was right

**My #2; these are checks I devised.** Applied on paper to constructed wrong inputs, they produce these failures:

| Check | Planted wrong input | Result |
|---|---|---|
| Judge the actual outcome | Export reports success but omits a requested row. | **FAIL:** the requested output is wrong. |
| Establish authority | An agent uses its unaccepted sorting proposal to justify changing the product. | **FAIL:** no acceptance supports the change. |
| Preserve coverage meaning | Repackaging CSV/JSON changes 0/1 into 1/2 without changing behavior. | **FAIL:** case count is sensitive to packaging. |
| Match approval to content | A requirement is edited after EJ accepts it; the old acceptance is reused. | **FAIL:** the edited version lacks that decision. |

These demonstrations establish that the proposed checks can reject those particular mistakes. They are **not independent evidence** that the method improves delivery. That remains **not measured** until an actual task shows whether the distinctions catch errors worth their cost.