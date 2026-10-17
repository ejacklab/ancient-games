# Linus Torvalds — where insights belong

## Answer

My reading: EJ’s hypothesis is partly right—many lessons belong to recurring coding or testing tasks, but the data also contains project-specific implementation lessons beyond requirement issues. A program can route explicitly recorded applicability quickly; reliable inference from the current records is **not measured**, and neither `engine` nor `Source:` determines who should learn.

## How I decided

1. **My #9: establish what is being classified.**

   By *task level*, I mean a lesson applicable to a recurring operation—writing tests, changing shared interfaces, invoking commands—regardless of project or agent engine. I do not mean merely the run where it happened.

   My reading: F-0f2fa841 supports this interpretation. A planted failure was used without establishing that the plant actually failed. F-21e1586c adds that the observed failure must come from the intended plant. These are testing lessons; their stated causes do not depend on Claude, Codex, or this repository.

   F-1e90a8e1 similarly supports a command-execution lesson: piping a command concealed the exit status needed by the next step. These examples support EJ’s move beyond run-local storage.

2. **My #9 and my #10: project implementation knowledge still exists.**

   My reading: these entries break the hypothesis’s exclusion of project-level lessons:

   | Insight | Project-specific knowledge |
   |---|---|
   | F-86553997 | Writable journal kinds were declared twice, so adding a kind required two edits. |
   | F-682702da | This exporter copied a skill’s main file without its referenced resources. |
   | F-d8221199 | This export test examined uncommitted state while claiming to test committed output. |

   An agent maintaining those components needs those facts regardless of engine. They concern representation, implementation, and test design.

   Each can also yield a broader coding lesson. F-86553997 supports removing duplicated declarations; F-682702da supports checking a bundle’s dependencies. **The concrete repair and the transferable lesson can have different audiences.**

   If *project requirement issues* includes every implementation defect because correct behaviour could be expressed as a requirement, the hypothesis becomes true by definition. It stops helping decide where agents should learn.

3. **My #9 and my #7: neither existing field supplies applicability.**

   My reading: F-7f938bdf demonstrates why sorting by the failing engine misleads. Opencode encountered the rejected path, but the caller supplied it. Callers preparing opencode inputs need the lesson too.

   `Source:` also cuts across audiences. F-682702da identifies a project exporter as the tool to repair; F-173e0190 identifies a Claude CLI invocation defect in the runner. The latter matters to callers of that CLI, including callers using another engine.

   F-76013d09 and F-0a1f3ca1 support a Codex-sandbox condition. They do **not** establish that every Codex configuration has the problem.

   I therefore cannot give an honest error count for a sorter over the 56 sections: no proposed sorter or accepted reference classifications were supplied. F-8ac06aae also explicitly leaves the exact cause unresolved; classification should preserve that uncertainty.

4. **My #9 and my #13: record applicability before automating delivery.**

   **Proposed change to the pattern:** when the worker writes an insight, they also propose:

   - The actionable lesson.
   - The conditions under which it applies: component, operation, or engine/configuration.
   - Who needs it: workers, callers, reviewers, or maintainers.
   - Supporting insight IDs and any unresolved applicability.

   EJ retains the decision. Multiple applicable audiences remain possible.

   My reading: F-969500fa needs this separation particularly clearly. It contains both a guard limitation and a command-composition habit. One exclusive label would conceal part of the lesson.

   Once applicability is accepted, a program can match it against the current project, task, and engine configuration. Missing applicability produces an unresolved result. This automates routing; it does not establish that the worker’s proposed scope is correct.

5. **My #2 and my #18 (`attributed`): claims of speed and reliability need evidence.**

   Requirement-check of the proposed sorting rule:

   - **Pass:** who decides—EJ; one thing—assign applicability; unit—insight sections; can it fail—misrouting F-7f938bdf is a concrete failure; links—no dependency on another rule is needed.
   - **FAIL:** weak words—speed and reliability have no targets; level—advice versus automatic authority is unspecified; basis—classification performance has not been measured.

   My reading: the counterexamples above justify rejecting simple field-based sorting. They do not prove that a more capable classifier cannot work.

## What I need to know

- What elapsed-time and wrong-routing limits would make sorting acceptable to EJ?
- Should inferred classifications remain advice, or eventually control delivery automatically?

If classifications remain advice, uncertain suggestions can be reviewed. If they control delivery, missed audiences and irrelevant deliveries both need measurement.

## Costs and risks

- **My #9:** recording applicability adds worker effort; F-969500fa shows why compressing it into one label can lose information.
- **My #13:** broad lessons can create noise. F-76013d09 supports retaining its sandbox condition rather than teaching every agent that pipes are unreliable.
- **My #5:** keep original run evidence and make classifications reversible. F-8ac06aae shows the risk of turning an unresolved diagnosis into permanent instruction.
- **My #18 (`attributed`):** broader reuse and lower noise are expected benefits, **not measured results**.

## How we would know I was right

**My #2 and my #18 (`attributed`):** compare a proposed sorter against EJ-reviewed applicability for the 56 sections. Count sections, since some contain multiple failure IDs. Report wrong audiences, missed audiences, unresolved cases, review time, and routing time.

Then check whether future relevant tasks receive the lesson before the risky action, and whether unrelated tasks receive less irrelevant material.

This is my proposed evaluation, not an executed or independent check. The main agent’s extraction supplies the corpus; it does not establish classification accuracy or improved agent quality.