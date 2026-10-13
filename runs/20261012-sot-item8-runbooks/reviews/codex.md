# Item 8, runbooks (codex)

## Recommendation

[proposed] Choose **(b): remove runbooks as a memory kind, keep reusable procedures with the project as scripts or skills, and link to them from existing memory entries when they help apply a recorded claim.**

## Three reasons

1. [EJ’s] The vision names “the **decisions and facts** the code must follow, written **before** the code” and “what was **learned** after: lessons, observations and hypotheses.” [proposed] My reading: removing the extra kind brings the design into line with the settled vision without expanding what EJ said memory holds.

2. [design] W3.1 says, “Nothing that can be read directly from the code, the tests or the commit log”; W3.6 says, “an entry links to them.” [proposed] My reading: a procedure and a memory entry should have different jobs. The procedure holds the steps; the entry holds a decision, constraint or learning, with a link when useful. A separate runbook entry adds another place for the steps to drift.

3. [proposed] The supplied `procedure-to-skill` skill states, “The procedure is the memory. A prose description of a procedure is a summary of the memory, and summaries drift.” It also requires a “real, **external** check.” [proposed] My reading: making reusable steps executable, with verification of their result, gives the next worker something stronger than instructions to reinterpret. The skill’s exclusion of “a procedure specific to one throwaway task” also prevents turning every task’s instructions into a permanent skill.

## Text changes

[proposed] All replacement text below is a proposal for EJ to decide. The labels identify attribution and are not part of the replacement text.

### Vision

[proposed] **No text change.** Keep the existing list of decisions, facts, lessons, observations and hypotheses. A link to a procedure supports one of those entries; it introduces no additional memory kind.

### Design — “What it is for”

[design] Delete this bullet: “A **runbook** says how to run or fix something; where possible it points at a script.”

[proposed] After the remaining two bullets, insert:

[proposed] “Reusable procedures SHOULD be kept with the project as scripts or skills. Any manual steps stay with the procedure. An entry may link to it from **How to apply:** when the link helps apply that entry’s claim; the entry does not repeat the procedure.”

[proposed] “A reusable procedure shared by the project belongs to **project scope** and is readable from the repo. Instructions specific to an unfinished task belong to **task scope**, in its existing `work/<task-id>/state.md`. Neither belongs solely to agent or user memory when project workers need it.”

[proposed] “SHOULD marks a default; a departure is explained where the procedure is kept.”

### Design — “When to write” table

[design] The current end-of-task row includes “merging duplicates; runbooks.”

[proposed] Replace that row with exactly:

[proposed] `| At the end of a task | Other lessons, observations and hypotheses; merging duplicates. |`

[proposed] Procedure maintenance follows the work that changes the procedure. It is no longer an end-of-task memory-entry obligation.

### Design — layout

[proposed] Replace the `entries/` line with exactly:

[proposed] `  entries/           one file per entry: D- decision, F- fact, L- lesson`

[design] Keep the following sentence about observation and hypothesis prefixes unchanged: “File prefixes for observations and hypotheses: `O-` and `H-`, proposed in W1.1.”

[proposed] This review does not settle those existing prefix proposals.

### Design — W1.1 and W1’s check

[proposed] Replace W1.1 with:

[proposed] “**W1.1** Each entry is one file: `project-memory/entries/<prefix>-<id>-<slug>.md`. The prefixes are `D-` decision, `F-` fact and `L-` lesson, plus `O-` observation and `H-` hypothesis (*proposed*; the design leaves these two open).”

[proposed] Replace W1’s **Fails if** with:

[proposed] “**Fails if** a lint over `entries/` finds a missing field or section, or a reviewer finds two claims in one entry or a prefix outside W1.1.”

### Design — W2.2 and W2’s check

[proposed] Replace W2.2 with:

[proposed] “**W2.2** A **lesson** comes from a failure or a human correction. An **observation** records what was seen. A **hypothesis** is a guess, labelled as one.”

[proposed] Replace W2’s **Fails if** with:

[proposed] “**Fails if** `kind` holds a value other than decision, fact, lesson, observation or hypothesis, or a guess is recorded under any kind but hypothesis.”

[proposed] This removes the unsupported runbook definition from the requirement attributed to the vision.

### Design — W3.6 and W3’s check

[proposed] Replace W3.6 with:

[proposed] “**W3.6** No copy of the project’s existing documents or reusable procedures: an entry links to them.”

[proposed] Keep W3’s **Fails if** unchanged:

[proposed] “**Fails if** a secret scanner finds a credential (W3.2). For W3.1 and W3.3–W3.6, a reviewer finds such content. Those are judged checks.”

[proposed] The revised W3.6 makes copied procedure steps part of that existing judged check.

### Design — W5.2 and W5’s check

[proposed] Replace W5.2 with:

[proposed] “**W5.2** Written at the end of a task: other lessons, observations and hypotheses.”

[proposed] Keep W5’s existing **Fails if** paragraph, including its decision, correction and completion checks. Append:

[proposed] “For W5.2, it fails if a reviewer finds a lesson, observation or hypothesis selected for retention in the task’s closing journal read that was not written as an entry by task completion (judged).”

### Boundaries and requirement check

[proposed] These edits cover all six runbook references: **What it is for**, the timing table, the layout, W1.1, W2.2 and W5.2. They add no memory folders, files or header fields. **How to apply:** already supplies the place for a link.

[design] K4.1 says, “An entry is never deleted.” [proposed] Keep that rule. The inspected checkout has no `project-memory/` directory, so this proposal needs no existing `R-` entry migration here.

[proposed] I applied `requirement-check` to the proposed procedure-placement default:

| Label | Criterion | Assessment |
|---|---|---|
| proposed | Source | **Pass:** codex’s proposal, grounded in the supplied skill and W3. |
| proposed | One thing | **Pass:** placement, links and scope are stated separately. |
| proposed | Unit | **Pass:** no numerical threshold is introduced. |
| proposed | Can it fail | **Pass:** an entry that copies a reusable deployment procedure fails revised W3.6. |
| proposed | Weak words | **Pass:** the replacement identifies the artifact, scope and link location. |
| proposed | Level | **Pass:** procedure placement is SHOULD, with a stated reason for departure. |
| proposed | Basis | **Pass:** design judgement, **n=0**; revisit on the first fresh-session reuse of a procedure. |
| proposed | Links | **Pass:** the claimed relationship to W3 is quoted above and identified as my reading. |

[proposed] The proposed check additions are written by codex. This was a read-only document review; their usefulness in real work is **not measured**, and no lint, procedure or independent verification was run.

## What could go wrong

[proposed] A database recovery procedure includes a manual step: identify the correct backup before running the restore script. A worker moves only the commands into a script and discards that instruction with the runbook. The script finishes successfully but restores the wrong backup.

[proposed] The proposed wording keeps manual steps with the procedure. The supplied skill’s verification rule checks the actual recovery result rather than merely the script’s exit code. Whether a particular recovery check catches this failure remains **not measured**.

## Questions for EJ

[proposed] None. The proposal is complete for your decision; it leaves the existing observation/hypothesis prefix question untouched.
