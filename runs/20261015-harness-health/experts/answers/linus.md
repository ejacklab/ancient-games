# Linus Torvalds — Harness health for workflow readiness

## Answer

Build a read-only health report that compares the selected harness’s effective capabilities with the planned task’s stated needs, and gives specific help for each mismatch. Keep installation evidence, configuration evidence, demonstrated behavior, and EJ’s acceptance decision distinct; the presence of a setting is not enough to declare a harness healthy.

## How I decided

1. **Start with the failure we need to catch — my #2, #3 and #7.**

   A harness can be installed and logged in while being unsuitable for the work assigned to it. Conversely, an absent configuration key may mean a documented default applies. The extension should catch those mismatches without manufacturing failures from missing keys.

   **My reading:** the ten requirements are useful design inputs, but they are not an established standard. The main agent’s existing-coverage mapping is also input evidence, not independently verified coverage.

   Applying `requirement-check` to the proposed inference *a deny list exists, therefore guardrails are good enough*:

   | Criterion | Result |
   |---|---|
   | Who decides | **FAIL:** the acceptance rule and its owner are unspecified. |
   | One thing | **Pass:** one judgment with a stated condition. |
   | Unit | **Pass:** presence is a Boolean observation. |
   | Can it fail | **Pass:** an absent list fails, although the check misses ineffective lists. |
   | Weak words | **FAIL:** “good enough” has no task boundary. |
   | Level | **FAIL:** advice versus a blocking gate is unspecified. |
   | Basis | **FAIL:** presence has not been shown to establish enforcement. |
   | Links | **FAIL:** the claimed relation between this setting and effective protection is unsupported. |

   The replacement I recommend is conditional: **if a task requires a stated boundary, compare evidence of the effective boundary with that requirement.** Missing policy leaves the judgment unresolved; missing evidence leaves it unproven. Price: fewer reassuring verdicts and more explicit unknowns.

2. **Resolve U1–U7 without deciding policy for EJ — my #4, #5, #7, #9 and #13.**

   | Spot | My verdict and recommendation | Price or risk |
   |---|---|---|
   | **U1 — harness selection** | Keep the provisional split: inventory all six; judge suitability for explicitly selected harnesses. During early readiness, report capabilities; refine the verdict once assignments exist. Never silently omit a selected but missing harness. | Two moments of evaluation; unselected engines may retain unknowns. |
   | **U2 — help** | Prefer advice naming the observation, verified setting/file, proposed change, and recheck. Supply a snippet only when its syntax and effect are established for that version. Automatic modification is a separate decision for EJ. | Manual work remains; applying a snippet may affect other projects. |
   | **U3 — good enough** | Change the assumption. Concrete-looking settings do not automatically justify pass/fail. Compare effective behavior with accepted task requirements; report measurements without judgment where the target is missing. | Some findings remain unresolved until EJ supplies policy. |
   | **U4 — location** | Prefer a separate `harness_health.py`, beside `readiness.py`, using its evidence conventions. Keep the existing inventory interface working. Add readiness integration after the standalone report is checked. | Another script and an interface to maintain. |
   | **U5 — design effects** | Keep the proposed findings/effects table, but make effects specific to dependent work. Unproven confinement creates a preparation piece before work requiring confinement; it does not automatically alter an unrelated risk score. A script is a reviewer only for criteria it actually covers. | More explicit dependency records; fewer automatic substitutions. |
   | **U6 — version differences** | Keep version-qualified probes. Establish effective precedence across defaults, configuration, profiles, launch flags, and outer restrictions where applicable. Unsupported interpretation stays `unknown`; never guess a key. | Adapter maintenance and incomplete coverage across versions. |
   | **U7 — run/tool properties** | Keep the scope distinction, but replace “covered by gate” with “gate identified; coverage verified or unverified.” Inspect the actual run’s criteria and evidence when available. | Additional per-run checks; readiness cannot finish every judgment before a plan exists. |

   I recommend changing U3 and U7’s provisional assumptions. That is advice for EJ, not a recorded decision by them.

3. **Design the evidence record before the probes — my #9, #10 and #11.**

   **My reading:** each finding should contain:

   - Requirement and check identity.
   - Scope: harness, version, project, launch configuration, or run.
   - Expected condition and its policy source.
   - Observed condition and safe evidence reference.
   - Existing evidence status: `verified`, `reported`, `unknown`, or `MISSING`.
   - A separate requirement result: satisfied, violated, unresolved, or inapplicable with a reason.
   - Help and the check to repeat after applying it.

   A command can **verify** that a configuration file contains a value while leaving enforcement **unknown**. Those belong in separate findings.

   Offer Markdown for the person and JSON for tooling. Keep generic scripts and adapter knowledge in the workflow-design skill; keep project expectations with the project or run. Put run evidence under the already specified `runs/20261015-harness-health/`, using relative references rather than hardcoded machine paths.

   The checker writes observations and proposed help. EJ’s acceptance remains their decision, recorded separately. Price: a richer record, but it prevents an observation from being mistaken for approval.

4. **Give every requirement a check, a failure, and help — my #2, #3, #5 and #7; implementation details are my reading.**

   The following are proposed checks, not claims that the existing tools already perform them.

   | Requirement | Proposed check and planted failure | Help; price |
   |---|---|---|
   | **1. Context delivery** | Resolve the instruction entry points applicable to this launch and follow required document/skill references. Plant a broken pointer or unreadable required document. Compare token usage with the chosen model’s established capacity and the task’s supplied budget; line counts alone cannot establish suitability. | Identify the broken reference or measured excess and suggest moving material behind an on-demand pointer. Price: actual assembled context may be unavailable and remain unknown. |
   | **2. Tools** | For tools the task uses, check documented input/output contracts and safe invalid-call behavior. Plant an ambiguous argument or an error lacking the required correction information. | Give a corrected call or an adapter defect report. Price: tool-specific tests; discovery alone proves little. |
   | **3. Planning** | Check the run’s task structure and observable completion criteria through the existing gate after its coverage is established. Plant a task with no done criterion. | Name the missing criterion and who supplies it. Price: cannot finish this check before a plan exists. |
   | **4. State and memory** | Check that the next worker can recover the completed step and next action from the handoff. In a fixture, interrupt after a checkpoint or remove a required handoff reference. | Repair the handoff or checkpoint mechanism, then repeat the resume exercise. Price: file presence does not prove recovery. |
   | **5. Independent verification** | Check criterion coverage, checker authorship, evaluator assignment, and information boundaries. Plant an uncovered criterion or give the reviewer the builder’s reasoning. | Identify the missing test or independent review. Price: separate evaluation costs time or quota; different engines alone do not prove independence. |
   | **6. Guardrails** | Compare effective permissions with stated allowed and forbidden actions. Where a quota-free isolated behavioral check exists, exercise both a forbidden action and an allowed control. Plant a configuration that looks protective but permits the forbidden action. Report prompt-injection mechanisms and test coverage separately. | Explain the specific boundary gap and a version-verified correction, or propose an external boundary. Price: configuration evidence cannot prove comprehensive confinement or injection resistance. |
   | **7. Recovery and retries** | Check the run’s declared attempt limit, exhaustion action, and rollback/resume behavior. Plant a partial failure, then repeat the step; reject duplicate effects or continuation past the supplied limit. | Add a recovery mechanism or ask the owner for the missing limit. Price: realistic failure exercises need isolated fixtures. |
   | **8. Human gates** | Check that each declared gate has an owner and actually holds dependent execution. Plant missing approval and confirm that work behind that gate does not start. | Name the missing owner or unenforced gate. Price: written Guard rules alone cannot establish runtime enforcement. |
   | **9. Observability** | Reconcile an external fixture’s action sequence with recorded actions, decisions, anomalies, and engine usage. Plant a missing event or unavailable usage data. Do not translate unavailable cost into zero. | Identify the capture/parser gap and retain the unknown. Price: internal model actions may not be observable; captured logs require secret-safe handling. |
   | **10. Feedback** | Trace a recorded mistake to its corrective change and a recurrence check. Replay the recorded failure. Treat model/version review as a separate maintenance action. | Propose the smallest source-level fix and show what catches recurrence. Price: indiscriminate permanent rules accumulate contradictions and context cost. |

   No instruction-file length limit, retry count, cost ceiling, or aggregate health score is supplied here. Any needed target comes from an existing accepted requirement or EJ.

5. **Build in a checked sequence — my #13, #1, #3 and #17; my #19 is an attributed rule.**

   This is a proposed build order, not an execution plan with invented models, budgets, or attempt limits. Each piece reads the run state, produces evidence, passes its check, and then updates state through one writer.

   | Order | Deliverable | Check that can fail | Price |
   |---|---|---|---|
   | **First** | Completed acceptance criteria and responses to the policy questions below. | A sample task requiring confinement has no defined expected boundary or unresolved-finding policy. The build target remains incomplete. | EJ’s decision time. |
   | **Then** | Inventory support for `dsh` and `opencode`. | Fake executables demonstrate missing, successful, and unsuccessful probes without launching model work; existing inventory consumers still work. | Small adapter and regression-test cost. |
   | **Then** | Finding format and standalone report, using synthetic input. | Reject a finding that marks an unsupported claim satisfied, loses scope, or exposes a planted secret. Check Markdown/JSON agreement. | Format and renderer maintenance. |
   | **Then** | One complete adapter for a selected harness, including version and effective-setting provenance. | Exercise defaults, overrides, malformed input, unsupported versions, and ineffective protective settings. Add isolated behavior checks where available. | Establishing precedence may be harder than reading files. |
   | **Then** | Remaining selected adapters and the per-run evidence checks. | Every claimed capability has supporting evidence; unsupported capabilities remain unknown. A gate reference without demonstrated coverage cannot satisfy a requirement. | Broader maintenance; no promise that all harnesses expose equivalent evidence. |
   | **Then** | Specific help attached to findings. | In a fixture, applying supported advice changes the failed observation as predicted. Reject wrong-version advice or a snippet that broadens unrelated permissions. | Advice becomes another maintained interface. |
   | **Then** | Readiness integration and method 3.1’s findings/effects table. | An unrelated finding leaves an independent task usable; an unresolved required boundary routes the dependent task according to EJ’s selected policy. Legacy invocation behavior remains usable. | Integration and migration work. |
   | **Finally** | Independent acceptance review and reproducible evidence. | A reviewer given criteria and evidence, without builder reasoning, challenges unsupported passes and reproduces planted failures. Run the recorded baseline and relevant new checks. | Review time and any approved evaluator quota. |

   Keep ordinary readiness quota-free. A behavioral check that requires model execution becomes a separately identified experiment, with its cost and authorization explicit. If repair loops are used, their attempt limits remain open until supplied; this advice does not choose them.

## What I need to know

- **U1, U3 and U5:** Do EJ accept task-specific suitability for selected harnesses, and where should each task’s required capabilities and boundaries be declared?
- **N1 — unresolved required evidence:** Should an unresolved required condition hold dependent work, require EJ’s decision, or permit continuation with a recorded exception? This blocks the integration policy.
- **U2 and N2 — help and experiments:** Is help advice plus verified snippets? May separately identified experiments use model quota or change isolated fixtures, and who authorizes those actions? This blocks active checks, not static reporting.
- **U7:** Should the report retain all ten requirements and explicitly show which need a later run/tool check? If EJ prefer any outside scope, which ones should be excluded?
- **N3 — effective launch and evidence reuse:** What launch configuration should a verdict describe, and should a changed version, configuration, project, or invocation invalidate previously collected evidence? This blocks claims about reused results.

## Costs and risks

- **My #7:** Honest unknowns may feel less helpful than a score. They prevent unsupported assurance.
- **My #5:** Read-only advice keeps mistakes reversible, but applying configuration changes can affect other work. Help needs a stated scope and a recheck.
- **My #9 and #17:** Six harnesses create adapter maintenance. Keep parsing, comparison, and presentation separate so version changes remain local.
- **My #1 and #3:** An overbroad health gate can break existing workflows. Judge requirements the task depends on and preserve the inventory’s established behavior.
- **My #13:** Begin with a complete selected-harness slice. Expanding all ten requirements into universal runtime proofs immediately risks overdesign.
- **My #18 — attributed:** Claimed savings require measured elapsed time, calls, and available usage data. This recommendation has no measured performance or cost benefit yet.

## How we would know I was right

A seeded ineffective protection produces a violation or unresolved result rather than a health pass. A documented effective default can satisfy the corresponding requirement even when no explicit key exists. A supported correction changes the failed observation, while an unrelated task remains usable.

Every implemented check is first shown failing on its planted wrong input. A separate evaluator examines the evidence and coverage, and the recorded baseline still passes.

**Not measured:** these are acceptance checks proposed by this Linus seat. I have not run them or independently verified the main agent’s coverage mapping. Passing synthetic checks would establish the checker’s behavior on those cases; it would not establish complete harness security or protection against every prompt injection.