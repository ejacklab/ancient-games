# Linus Torvalds — what harness health can prove

## Answer

My reading, applying my #2, #3 and #13: keep the useful intentions, but change the list so every verdict states exactly what was tested; readiness can establish local prerequisites, while successful dispatch and acceptable results need later evidence. Recommend counting acceptance criteria for R11.1 and requiring a judge capable of rejecting a result, with both choices left for EJ to approve.

## How I decided

1. **Start with the failure users actually experience — my #1, #2 and #3.**

   A configured harness can still hang, refuse the work or return nothing. A file-existence check cannot establish that those failures are absent.

   The main agent’s paper backtest predicts **0 of 7** recorded failures caught. That is supplied analysis, not an executed backtest I independently verified. My reading: it demonstrates a mismatch between the proposed check’s scope and the failures described, rather than a measured detection rate.

   All checks proposed below are **my designs, not measured here**. No harness calls, config changes or checker implementations were performed.

2. **Check the requirements before treating them as a contract — my #7; the eight-question assessment is my reading.**

   | Criterion | Pass / FAIL in the supplied wording |
   |---|---|
   | **Who decides** | **FAIL:** R1–R10 generally leave the owner of interpretation unnamed. R11.1 leaves its counting unit and qualifying judges unresolved. R11.2 leaves exception approval unnamed. |
   | **One thing** | **PASS:** R3, R4, R8 and R11.1 have an identifiable central event. **FAIL:** R1 combines context delivery and context budgeting; R5 combines evaluator arrangements and acceptance; R6 bundles several security controls; R7 bundles retry and recovery; R10 combines incident correction and periodic review. R2 and R9 need their scope narrowed around a defined interface or record. |
   | **Unit** | **PASS:** R11.1 explicitly says prompts; R11.2 compares durations. **FAIL:** Q1 leaves the intended counting unit unresolved. The comparison in R11.2 needs a declared source for expected durations. Other requirements supply no numeric thresholds to validate. |
   | **Can it fail** | **PASS:** concrete failures can be named for missing task criteria, lost progress, absent verification and missing records. **FAIL:** broad claims about tool quality, injection defense and harness improvement lack acceptance tests. R11.1 remains uncomputable until Q1/Q2 are settled. |
   | **Weak words** | **FAIL:** short, clear, well-designed, clean, sensible, risky and need judgment leave material choices open. R11.2 improves on fast by using a comparison, but its measurement basis remains open. |
   | **Level** | **PASS:** R11.2 is SHOULD. **FAIL:** the other lines lack explicit levels. Method preferences warrant SHOULD or guidance; a specific safety boundary may warrant MUST. |
   | **Basis** | **PASS:** the brief discloses the unknown source of R1–R10 and the unmeasured basis of 80%. **FAIL:** neither establishes effectiveness, and no reconsideration point for 80% is supplied. |
   | **Links** | **PASS:** the readiness/prompt-writing conflict is explicitly identified. **FAIL:** a separate evaluator does not automatically establish independent judgment; hooks do not establish improvement; a faster preliminary check does not automatically justify suppressing the full judge. |

   The questions that change the resulting contract are collected under **What I need to know**.

3. **Give each requirement a verdict and a bounded check — my #2, #3, #5, #9 and #13.**

   These are recommendations for EJ, not adopted requirements. **Partial readiness** means the stated prerequisite can be checked before dispatch; the intended behavior remains unproved.

   | Requirement | Recommended verdict and rule | Readiness check that can fail; limit |
   |---|---|---|
   | **R1 — Context** | **Split:** instruction delivery; context budgeting. My #9, #11. | **Partial.** Resolve the instruction files and referenced resources for the intended working directory. Fail a missing, unreadable or broken reference. Compare assembled context against the selected engine’s documented capacity when known. This proves availability and fit, not that the agent receives or follows it. Leave short undefined until EJ supplies its meaning. |
   | **R2 — Tools** | **Change:** assess declared tool contracts through valid and invalid calls. My #2, #10. | **Partial.** Test an exposed local interface without a model call. Fail invalid arguments accepted silently, errors without a usable cause, or behavior outside the declared boundary. Interfaces only exposed inside a live agent remain unknown. A schema file alone proves no behavior. |
   | **R3 — Task structure** | **Keep**, with the author and acceptance evidence named. My #11; my #19, **attributed**. | **Not fully at readiness:** the task list does not exist yet. Readiness can exercise the design validator against a planted task lacking done-criteria. After design, fail an actual task without an acceptance condition. Template existence is insufficient. |
   | **R4 — State** | **Change:** define successful handoff as reconstructing the next action from saved state. My #9, #11. | **Partial.** Use a local fixture containing completed, pending and blocked work. Fail if the resume procedure loses status or needs unavailable conversational context. A memory directory does not prove resumability; a fresh model context remains untested without an authorized call. |
   | **R5 — Verification** | **Split:** acceptance evidence; independence of judgment. Change the universal separate-agent prescription. My #2, #7; my #18, **attributed**. | **Partial.** Run applicable local judges on known passing and planted failing artifacts. Fail a judge that accepts the failing case, cannot run, or lacks a defined verdict. Actual result acceptance happens later. Deterministic tests can provide useful evidence without another model; another agent alone does not establish independence. |
   | **R6 — Guardrails** | **Split:** permission boundaries, sandbox enforcement and handling of untrusted instructions. My #5, #7. | **Partial.** Inspect effective settings and their overrides where supported. Test a prohibited operation only through a harmless local enforcement probe. Fail if it succeeds. Without that probe, report configuration only. An unset setting is not proof that access is unrestricted; injection resistance needs separate behavioral evidence. |
   | **R7 — Recovery** | **Split:** retry behavior; recovery from partial effects. My #5. | **Partial.** Inject a local interruption after a partial operation, then resume. Fail duplicated effects, corrupted state, continued retries beyond the declared policy, or an unusable recovery point. Retry limits and eligible errors need an owner and basis; they are not supplied here. |
   | **R8 — Human gates** | **Keep**, with named triggers, decision owner and waiting behavior. My #4, #5, #14. | **Partial.** Exercise the gate with a local action fixture that requires approval. Fail if execution proceeds without the required decision. Effective harness enforcement may still require an authorized live test. A bypass prompt setting alone cannot establish the whole approval policy. |
   | **R9 — Observability** | **Change:** record what explains dispatch, result and acceptance; declare unavailable measurements. My #9, #11. | **Partial.** Send a synthetic local event through the recorder and retrieve it. Fail missing linkage between invocation, outcome and acceptance decision. Report unavailable token or cost data as unavailable, never as zero. A session folder proves neither completeness nor useful diagnostics. |
   | **R10 — Improvement** | **Split:** correcting a demonstrated failure; reassessing scaffolding. **Drop the automatic permanent-fix clause**, subject to EJ. My #1, #7, #13. | **Partial.** Replay a known failure against a proposed fix and rerun the previous successful case. Fail recurrence or newly broken behavior. Readiness can exercise this mechanism, but cannot establish future improvement. Hook presence proves no learning. |
   | **R11.1 — Judge coverage** | **Change:** settle the counting unit and qualifying judge, then calculate after step 2. My #3, #9. | **Readiness: inventory only.** Record available judges and what each can establish. After design, calculate coverage against the agreed unit. Fail an unsupported numerator entry, a missing denominator or coverage below the agreed threshold. An empty design is not evidence of coverage. |
   | **R11.2 — First signal** | **Change**, retaining SHOULD: use an earlier rejection check where it has a valid rejection reason. My #2, #13; my #18, **attributed**. | **Partial.** Readiness can validate available checks on fixtures and measure their local duration. After design, compare their expected duration with the expected prompt duration and record the full judge’s expected duration. Fail missing timing evidence, an unjustified rejection or a missing exception reason. Actual timing remains unproved until execution. |

   **My reading on R11.2:** passing the first check permits the full judge to run; it does not establish acceptance. If the first check suppresses the full judge, its rejection needs to demonstrate a real acceptance failure. Otherwise a cheap but unreliable filter can discard good work.

4. **Answer the open questions through the result being judged — my #3 and #9.**

   **Q1 — Recommend acceptance criteria.** Counting prompts lets packaging change the percentage without changing the work: several criteria can be bundled into one nominally covered prompt. Criteria give a closer account of which intended outcomes are judgeable.

   That changes the draft’s unit. **EJ must decide whether to make that change and retain 80% for the new denominator.** Until then, keep prompt coverage and criterion coverage distinct; do not present either as the settled interpretation. Counting criteria also requires stable, agreed criteria, or splitting them can manipulate the percentage.

   **Q2 — Recommend only a judge capable of pass or fail.** A design-standard document qualifies when identified provisions can be applied to the result, a named evaluator applies them, and a violation can reject it. A human can perform that judgment; automation is not required. Merely linking a document does not qualify.

   Both recommendations are **my reading**, not words attributed to Torvalds.

5. **Ask EJ about the missing failure conditions — my #1, #2, #3, #5 and #13.**

   **N1 — Should dispatch have an explicit result contract?**  
   Proposed addition under R2/R5: record the required output and fail a return that does not satisfy it, irrespective of exit code. This catches empty success, a plan returned instead of an answer, and a refusal presented as completion. It needs task-specific acceptance evidence; nonempty output alone is insufficient. **Readiness:** validator fixtures only; actual engine behavior needs authorized dispatch evidence.

   **N2 — Should execution lifecycle checks explicitly cover stdin, concurrency, cancellation and partial failure?**  
   Proposed expansion of R7. It would catch the described stdin hang, database contention, worktree-write refusal and login failure if the relevant failure is reproduced. **Readiness:** local adapter fixtures can prove handling of these conditions; they cannot prove the installed engine will behave identically. Retry eligibility must distinguish transient failure from permission refusal.

   **N3 — Should evidence identify the exact setup it tested and become stale when relevant inputs change?**  
   Proposed addition to R9/readiness: associate evidence with the engine version, working directory, invocation mode and effective permissions it actually exercised. Fail reuse when those dependencies differ or are unknown. This catches a successful test being applied to another mode, directory or configuration. It does not guarantee success when external conditions change.

   **N4 — Should safety boundaries remain outside the 80% allowance?**  
   Proposed clarification to R6/R11.1: a coverage percentage should not excuse an unverified safety-critical action. Fail a design that treats an unmet safety boundary as part of its permitted uncovered fraction. EJ needs to identify those boundaries; I would not invent a severity threshold.

## What I need to know

- **Q1:** Does EJ choose prompts or acceptance criteria, and does 80% remain their threshold if the unit changes?
- **Q2:** Does EJ agree that a standard counts only when a named evaluator can use it to reject a result?
- Who owns the effective safety boundaries, approval decisions, retry policy and acceptance of documented exceptions?
- Does EJ accept dropping the automatic permanent-fix clause in R10, and adding N1–N4? When should the unmeasured 80% rule be reconsidered?

## Costs and risks

- **R1–R4 — my #9, #11, #13:** resolving context and exercising tools, design validators and handoffs adds maintenance. These checks establish narrow prerequisites and can create false confidence if their limits disappear from the report.
- **R5 and R11.1 — my #2, #7; my #18, attributed:** meaningful judges and criterion mappings take work. Judge authors can share the builder’s assumptions; a separate agent adds quota cost without automatically removing that dependence.
- **R6–R8, N2 and N4 — my #5:** enforcement and recovery probes need containment. Stricter boundaries can prevent useful work, while retries can duplicate effects. They need explicit ownership.
- **R9 and N3 — my #9, #11:** evidence collection, redaction and invalidation cost storage and implementation effort. Capturing everything can expose secrets and obscure the useful record.
- **R10 — my #1, #13:** failure-specific fixes require reproduction. Permanent rules added after every mistake can accumulate contradictory scaffolding.
- **R11.2 — my #7; my #18, attributed:** a preliminary check adds latency to passing work and can reject good results. No speed benefit is measured here.
- **N1 — my #3:** stronger output contracts reduce false success, but overly rigid contracts can reject valid alternative results.

## How we would know I was right

Apply each proposed checker to a known passing case and a planted failing case before trusting it. The checker author supplies those cases; a reviewer should also challenge whether they represent the intended failure. Passing an author’s fixtures is limited evidence, not independent validation.

Replay the seven recorded failures where reproducible. For each, show what the readiness check detects, what requires dispatch evidence, and whether the output judge prevents false acceptance. Any reproduction requiring a paid engine call waits for EJ’s go-ahead.

Then compare the revised check with the current check on the same cases: failures detected, successful work wrongly rejected, added checking time and quota spent. My recommendation would be supported by detecting relevant failures without breaking previously successful workflows; fixture results alone would not establish reliability across all six live harnesses.