# Linus Torvalds — One vocabulary for research findings

## Answer

*My reading:* adopt **`observed / reported / inferred / unknown`**, defined once in a new `docs/RESEARCH_FINDING_LABELS.md`, with source provenance recorded separately. These labels describe how the researcher supports the exact claim; they are not a ranking of truth or source reputation.

## How I decided

1. **My #9 — design around the data.** A source’s identity, what it asserts, and what the researcher establishes are different facts. One label cannot safely stand for all three.

   *My reading, requirement-check:* **source** passes—the brief requests consolidation; **one thing** passes—classifying a finding; **unit** passes—one claim per row; **can it fail** passes—contradictory template definitions are observable; **weak words** fails—“one set” leaves provenance’s place unspecified; **level** passes—this is advice for EJ; **basis** passes for the documented inconsistency, while this remedy is explicitly **n=0**; **links** passes—no existing schemes are assumed equivalent.

2. **My #10 — remove the special case by changing the model.** Use this vocabulary:

   | Tag | One-line definition |
   |---|---|
   | `observed` | The researcher directly inspected text, data, or an execution record demonstrating the exact claim within its stated scope. |
   | `reported` | A source asserts the claim, but the researcher has not directly established the underlying claim. |
   | `inferred` | The researcher derives the claim from identified findings and states the reasoning and assumptions. |
   | `unknown` | The question remains unresolved from the material examined; the row states why. |

   The researcher fills every field. Alongside the existing source citation, record whether the source is primary or secondary **for that claim**, and the evidence or limitation behind the label. Neither source role implies reliability.

3. **My #2 and my #7 — require evidence and acknowledge its limits.** A vendor’s performance assertion illustrates the distinction:

   - The vendor published a claim of a 60% improvement: `observed`, if the researcher inspected that statement.
   - The system achieves that improvement: `reported`, if the researcher only inspected the assertion; record that no benchmark evidence was checked.
   - The improvement will transfer to this repo: `inferred`, with dependencies and assumptions, or `unknown` if no inference is supported.

   **When two tags seem to fit:** first fix the exact claim and who is making it. Split documentary facts from underlying assertions. Direct evidence of that exact claim gives `observed`; an external assertion gives `reported`; the researcher’s derivation gives `inferred`; an unanswered question gives `unknown`. An inference resting on reported findings remains conditional.

   `unproven` becomes an explicit limitation on a reported claim. `GAP` becomes an `unknown` question with its search record. Disagreement keeps separate source rows and an explicit unresolved comparison; it is never averaged.

4. **My #9 and my #13 — borrow the useful distinction without importing an entire grading system.** WADA’s Admiralty guidance evaluates source reliability and information accuracy separately and warns against letting one determine the other. That separation applies here, although primary/secondary provenance is **not** itself a reliability grade. [WADA guidance, §5.1](https://www.wada-ama.org/sites/default/files/resources/files/wada_guidelines-information-gathering-intelligence-sharing_final_en.pdf)

   GRADE assesses certainty in a **body of evidence for a particular outcome**, considering bias, inconsistency, indirectness and other domains. Reading a primary paper alone does not perform that assessment. *My reading:* use the distinction between collection and assessment; do not rename primary-source access `CONFIRMED`. [GRADE Working Group requirements](https://www.gradeworkinggroup.org/)

5. **My #11 and my #19 — make the change understandable across every consumer.** The concrete file proposal is:

   | File | Proposed change |
   |---|---|
   | `docs/RESEARCH_FINDING_LABELS.md` | Own definitions, selection rule, examples and historical-policy boundary. |
   | `docs/workflow-templates/research-file.md` | Reference the canonical definitions; update finding and digest examples. |
   | `docs/TASK_TYPES.md` | Replace its research-label enumeration with the canonical reference. |
   | `docs/FEEDBACK_TEMPLATES.md` | Use the same labels in web-search and research pass-backs; retain search and dispute details. |
   | `.claude/agents/researcher.md` | Reference the policy; correct its vendor example and copied definitions. |
   | `docs/WORKFLOW_DESIGN_METHOD.md` | Reference the policy for research findings; explicitly distinguish tool-readiness labels. |

   Explorer’s `read / ran` and the main agent’s `quoted / my reading / not measured` stay separate: they describe different activities.

6. **My #1, my #5 and my #12 — preserve existing users and history.** Leave historical findings and `runs/20261011-agent-memory-graph/check-findings.py` under their original convention. If that validator becomes shared tooling, create a current-policy version referencing the canonical vocabulary. Do not globally replace old tags: their meanings differ, so translation requires rereading each claim and its evidence.

## What I need to know

Does EJ’s “one set” allow source provenance to remain separate metadata alongside one official finding-label field? This proposal assumes yes; forbidding that separation would change its shape.

## Costs and risks

- **My #9:** recording provenance and evidence limitations adds work per finding.
- **My #7:** `observed` can still mislead if a row overstates what the inspected artifact demonstrates.
- **My #1 and my #12:** preserving history leaves legacy vocabularies visible; their policy boundary needs explanation.
- **My #18:** the proposed improvement is **not measured**. Established schemes support the separation, not these particular names.

## How we would know I was right

Have researchers independently label actual rows covering the vendor example, a derivation, a failed search and conflicting sources. Compare both their labels and their claim wording; disagreements should identify a defect in the definitions.

My proposed mechanical check would verify vocabulary, citations, inference dependencies and recorded limitations. It would not establish evidence quality or claim truth. No such check or classification trial was run here.