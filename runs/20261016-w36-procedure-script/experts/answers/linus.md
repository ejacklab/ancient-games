# Linus Torvalds — When a procedure should be a script

## Answer

**My reading:** No: a script can carry out executable work, but printing instructions or requesting a judgment does not mean it performs the whole procedure. The author should choose the form when creating or revising it; the project owner or their named reviewer should resolve uncertainty or disagreement before accepting that choice.

## How I decided

1. **Require execution, not a filename — my #2; my reading applied here.** A `.sh` file that prints a checklist has not automated the checklist. Apply this test:
   - Identify the procedure’s intended result, required inputs, actions, and success check.
   - For each action, identify what the script actually executes. Mark physical actions, human decisions, and unavailable interfaces.
   - Determine what the script can verify and where it must stop for a named person.
   - If it performs the work and exposes a checkable result, use a script. If it merely describes what someone else must do, use a page.

   This is my proposed test, not a claim that Linus supplied an automation checklist. Missing tooling establishes a current limitation, not permanent impossibility.

2. **Separate executable work from judgment — my #6 and my #10; my reading applied here.** Physical inspection without a machine interface cannot be performed by a script. Negotiation, resolving conflicting goals, and judging an unfamiliar incident should not be presented as automated merely because a script asks someone—or an LLM—for an answer. A mixed procedure can have a page explaining the human work and linking to scripts that perform the executable parts. Human involvement alone does not disqualify a script: an explicit approval stop can be part of it.

3. **Do not automate merely to satisfy the format — my #13 and my #18.** A procedure can be scriptable yet not worth scripting: for example, a disposable task whose automation would require more construction and maintenance than its intended use warrants. That is a cost judgment, not technical impossibility. The author should state the concrete tradeoff; I propose no universal reuse count or time threshold.

4. **Let the author make ordinary technical choices — my #4, my #5, my #6, and my #14.** The author applies the test while preparing the procedure and supplies the evidence with it. The existing reviewer checks that choice during review. If uncertainty remains or the choice is contested, the project owner resolves it or names someone with the relevant knowledge. Escalate the disputed step or tradeoff, rather than asking the owner to classify every procedure. This is my proposed allocation of responsibility, not an existing delegation.

5. **Repair the requirement’s scope — my #17 and my #19; my reading applied to requirements.** W3.6 combines entry duplication, procedure placement, and script listing. Keep the first and last as separate requirements.

   Requirement-check assessment of the supplied W3.6: **FAIL** who decides, one thing, and weak words—the script/prose boundary is undefined. **Pass** unit, can it fail, level, and links: script lines have a unit, copying without a reason is a concrete failure, SHOULD is stated, and no unsupported relationship between rules is needed. **FAIL basis for the script/prose boundary:** the supplied owner rationale supports keeping procedures in project work, but does not establish that boundary.

   **My proposed placement wording, not a quotation:**

   A project procedure SHOULD live in a repo script when the script performs its executable steps and exposes a checkable result, with explicit stops for named human decisions; otherwise it SHOULD live in `docs/`, linking to any scripts it uses. When creating or revising it, the author records the reason for choosing prose in the task’s `state.md`, and the project owner or their named reviewer resolves any remaining uncertainty or disagreement before acceptance.

## What I need to know

None to make this recommendation. No particular procedure was supplied, so classifying one remains conditional on its actual steps, interfaces, and intended use.

## Costs and risks

- **My #18:** Scripts require maintenance; prose leaves execution and some checking to people. Mixed procedures require maintaining the links between them.
- **My #4 and my #14:** Author discretion permits inconsistent choices; escalating every choice makes the owner a bottleneck.
- **My #5:** A reversible format choice can still produce irreversible effects when executed. Choosing a script does not authorize its actions.
- **My #7:** This policy is **not measured, n=0**. Revisit it when first applied to an actual procedure.

## How we would know I was right

Apply the proposed test to a real procedure. A reviewer should be able to identify what executes, what proves completion, what still needs a person, and why the chosen form fits.

I wrote this test; passing it would establish that those boundaries are explicit, not independently prove correctness or reduced maintenance. The practical evidence would be successful use of the procedure without reconstructing missing steps or mistaking a printed checklist for completed work.