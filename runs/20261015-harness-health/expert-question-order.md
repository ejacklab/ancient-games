EJ says three things are now a must before work is designed: **visions, requirements and use cases**. EJ's own view is that use cases should come first. Which comes first — and in what order should the three be written, checked and revised?

Each of you: answer through your own rules. Give (a) the order you recommend, with the reason, and whether it is a strict sequence or a loop (and if a loop, what closes it), (b) where EJ's "use cases first" holds and where it breaks, each with a concrete case, (c) who writes each of the three, and what check each must pass before the next is built on it. Do not decide for EJ.

## Facts

**EJ's words** (quoted, 2026-10-15): "so, 3 things are the must now, visions, requirements and use cases. actually to me use cases should come first. which one come first?"

**How EJ works today** (quoted, same day): "I get requirement, I will gen use cases, and also see old use cases cover this requirement or not. and use AI to gen out all possibily, but actually not all require to be covered. so we get the 80% of all the possibility will do."

**What exists in this project now** (a workflow-design method in which AI engines do the work):
- **Vision.** A product blueprint template (`docs/workflow-templates/blueprint.md`) puts the product vision first: "who it is for; the problem it solves; what it will not do; how we know it works". It is EJ's: "an agent may only write down what EJ has said". Two products have a settled vision (a project-memory system and its caches); one is drafted.
- **Requirements.** Second in the template: one block per requirement, with a level (MUST / SHOULD), a "fails if", the check, and who decides each open choice. The memory system has 64 such records in a YAML file.
- **Use cases.** No section in the blueprint template. EJ writes them per requirement, then uses AI to generate "all possibilities".
- **Rules agreed today for coverage (R11.1):** before any case is generated, the requirement's behaviours are written as fixed units from its text and its "fails if"; AI-generated cases and old use cases attach to a unit as evidence and never add to the count; 80% of units covered is the target; a unit is skipped by consequence, not frequency; old use cases count only after failing on a planted violation.
- **A trial today, n=1** (main agent's mapping): for one requirement, the same engine generated 28 cases from "list the test cases" and 200 from "brainstorm every scenario, be exhaustive". Raw coverage by the existing tests was 46% and 20%; coverage over the fixed units was 80% both times. Both lists surfaced the same gap in the requirement's text (a clause with no "fails if"), and one real gap in its checks (a "fails if" with no test and no code). One list also contained cases that contradicted a decision already settled in the tests.
- **Also agreed today (proposed):** failures are worth more than successes; evaluation rules state what makes a result wrong, not how to be right, so an AI is free to find a better method than a human would.

**House rules that bind the answer:**
- Never fill a missing threshold with an invented number; a trigger is a comparison.
- MUST only for a safety bound; a method rule is SHOULD at most.
- Every artifact has one maker; a form two people fill at two times is two forms.
- Every check must be able to fail, and is shown failing once on a planted wrong input.
- The method is used in other projects; nothing project-specific may be hardcoded.
