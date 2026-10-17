# Linus Torvalds — What memory-check v1 should improve next

## Answer
Validate v1 on one real `project-memory/` repository before adding machinery, make target-absent results explicit, and prepare the session-start hook only as an owner-approved reversible change. Because `USE_CASES.md` and `VISION.md` were not supplied, every use-case mapping below is conditional and must not be treated as final.

## How I decided

1. **My #13, #2, and #18 — Run one real-repository canary before changing the implementation.**
   - **What:** Choose one EJ-approved repository containing `project-memory/`, run the current command there, archive the command, version, output, runtime, and elapsed time, then trace every reported item to its source.
   - **Use case/vision served:** Conditional on the specific use case among `U1`–`U6` that promises useful operation on a real repository. If none does, this improvement is ineligible.
   - **Case showing it is needed now:** The supplied facts say no real project with `project-memory/` has been checked and only fixtures were used (`memory_check/REQUIREMENTS.md` R2; `design-decisions.md` item 15). The known suite passes 70 tests (`bun test`, run at 18:4x), but that does not establish real-world usefulness.
   - **How to check it is done:** The run artefacts are inside the run repository, every finding is labelled true, false, or unclear with a source, EJ confirms that the result serves the mapped use case, and any required fix has a reproducing acceptance test.

2. **My #13, #16, and #18 — Replace ambiguous silence with an explicit target-absent result.**
   - **What:** Under `--warn`, emit a deterministic result such as `skipped: no project-memory/`, distinct from a repository that was checked successfully and produced no warnings. Keep exit 0 for compatibility unless the mapped use case explicitly requires another contract.
   - **Use case/vision served:** Conditional on the `U1`–`U6` entry, or vision line, requiring an agent or caller to know whether memory was actually checked. If silence is the required outcome, do not add this change without first revising that contract.
   - **Case showing it is needed now:** The repository smoke report has no `project-memory/`; `--warn` prints nothing and exits 0 (`runs/20261017-memory-check/nodes/smoke-report.md`; supplied smoke run).
   - **How to check it is done:** Tests distinguish absent target, clean checked target, warnings found, and execution failure; the absent-target case is no longer indistinguishable from a clean check.

3. **My #5, #7, and #13 — Turn the session hook into a reversible proposal, not an automatic installation.**
   - **What:** Produce an exact settings diff, dry-run procedure, expected session-start outcome, and complete rollback instructions. Do not alter EJ’s settings until they explicitly approve the shown diff.
   - **Use case/vision served:** Conditional on the `U1`–`U6` entry or vision line for session-start memory delivery.
   - **Case showing it is needed now:** The hook remains unbuilt because it requires the owner’s yes to a settings diff (`memory_check/REQUIREMENTS.md` R2; `design-decisions.md` item 15).
   - **How to check it is done:** Before approval, a settings snapshot proves nothing changed. After approval, a simulated session shows that the relevant memory reaches the agent before its first substantive call; uninstalling restores the original settings exactly. The criterion names that outcome rather than requiring a particular hook mechanism.

4. **My #2, #11, #18, and #19 — Proposed change to the pattern: make evaluation briefs source-complete and outcome-based.**
   - **What:** Copy every externally cited source into the run repository. Give every factual statement its own file-and-line or exact-command citation; mark any uncited statement as *recall*. State acceptance criteria as observable outcomes delivered before the relevant call.
   - **Use case/vision served:** Conditional on the same real-project use-case mapping as item 1; if no mapped use case concerns agent briefs, this remains a workflow improvement rather than a v1 feature.
   - **Case showing it is needed now:** The brief’s Lessons section records that headless agents denied outside reads, that criteria naming an unresolved mechanism fail the outcome they should serve, and that one blanket verification label can conceal recall.
   - **How to check it is done:** A headless evaluation brief containing one in-repo source, one source-less remembered fact, and one outcome criterion reaches the agent with both files accessible; the remembered fact remains labelled *recall*, and the test observes whether matching evidence arrives before execution.

5. **My #4, #13, and #17 — Remove or simplify no modules yet.**
   - **What:** Do not treat the count of 12 modules as evidence of over-design: `cli.ts` is explicitly a launcher and `command.ts` owns the command. Delete something only after a code-level check finds duplicated responsibility and its removal is tied to a mapped use case.
   - **Use case/vision served:** None is presently evidenced, so module removal is not proposed as an improvement.
   - **Case showing the need for restraint:** The supplied source fact distinguishes the launcher from the command but supplies no duplication evidence (`memory_check/src/`); the 14 review findings already have fix records and all 70 known tests pass.
   - **How to check it is done:** The real-repository canary produces a specific simplification with a demonstrated maintenance or correctness benefit; otherwise the next patch does not churn module boundaries.

## What I need to know

- What exact outcome belongs to each of `U1`–`U6`, and what are the vision-line texts?
- Is silent success for an absent `project-memory/` directory part of the current contract?
- Which real repository may EJ use, and may its memory contents be inspected by the review agents?
- What is the full in-repository path and line for `design-decisions.md` item 15?
- Will EJ consider a settings diff during this enhancement cycle?

## Costs and risks

- The real-repository canary costs review time and may expose private project information; one repository cannot prove general effectiveness, so treat it as a canary rather than broad validation. **(my #13, #2, #18)**
- Explicit target-absent output can create noise or break output-parsing consumers; use one deterministic status and add compatibility tests before changing it. **(my #13, #16, #18)**
- A session hook can consume startup time, add irrelevant context, or modify settings unintentionally; preview, approval, measurement, and rollback are mandatory. **(my #5, #7, #13)**
- Per-fact provenance and copied sources increase brief-maintenance work and can become stale when lines move; record exact paths and update them with each run. **(my #2, #11, #18)**
- Removing modules without demonstrated duplication risks breaking a working boundary merely to make the file count look smaller. **(my #4, #13, #17)**

## How we would know I was right

- The real-repository run has archived evidence, measured runtime, source-traceable findings, and EJ’s explicit determination that it serves the mapped use case.
- `--warn` produces observably different outcomes for no target, clean target, warnings, and failure.
- The hook does nothing before approval; after approval it delivers the relevant memory before the first substantive call, and rollback restores the original settings.
- The pattern check succeeds in a headless run: all cited files are inside the run repository, each fact has its own source label, and the criterion observes evidence arrival rather than a preselected mechanism.
1. Validate on one real repository with `project-memory/`.
2. Make target-absent output explicit and distinct from clean output.
3. Add the session hook only as an owner-approved, reversible settings diff.