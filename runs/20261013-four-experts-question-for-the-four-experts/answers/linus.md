# Linus Torvalds — Fixing the evaluator’s 20 findings

## Answer

**My reading:** Fix false proof and unsafe run handling first, then blindness and requirement coverage, then repair behaviour and reporting. Make each fix independently reviewable and reversible; if isolation cannot be enforced within the session, leave affected evaluations UNKNOWN and identify the unfinished work.

## How I decided

1. **Separate demonstrated failures from review findings — my #2 and my #7.**  
   The brief reports F1, F3 and F5 as confirmed by the COO. The other findings came from a read-only review that ran nothing. Reproduce those before accepting a particular diagnosis; the 762 passing tests do not establish coverage of these failures. **Price:** reproduction takes time, but prevents repairing the wrong mechanism.

2. **Choose the order by consequence and dependency — my #9, my #13; exact ordering is my reading.**  
   My proposed order is:

   **F1 → F12 → F10 → F11 → F5 → F4 → F19 → F17 → F9 → F8 → F3 → F14 → F20 → F2 → F6 → F7 → F15 → F13 → F16 → F18.**

   F1 is a small, confirmed false-positive fix. F12 precedes run cleanup so cleanup cannot escape its directory. F11 establishes valid evidence shapes before F5 changes their meaning. F19 and F17 move ahead of several medium findings because stale or relayed results can defeat otherwise correct repairs. **Price:** some visible coverage improvements wait while the evidence path becomes trustworthy.

3. **F1: make empty input explicitly unevaluable — my #9.**  
   Reject a manifest containing zero requirements before aggregation. Also ensure a requirement with no usable cases cannot pass through another empty `all(...)`. Return a clear input error and never produce affirmative MEETS.  
   **Risk:** a legitimate empty-spec workflow would stop working; whether such a workflow exists is unknown. **Notice:** empty input is rejected, while an ordinary nonempty all-PASS manifest still yields MEETS.

4. **F12 and F10: contain the run, then prevent reuse of its evidence — my #5 and my #9.**  
   For **F12**, validate `runId` as a directory name and check its resolved destination remains inside the intended `runs/` directory before any creation, deletion or command execution. Include symlink escapes in that check.

   For **F10**, my preferred small fix is to reject an existing run directory and require a new run id. If same-id reruns are necessary, reset every generated artifact as one deliberate operation while preserving the agreed historical evidence.  
   **Risk:** rejection changes rerun behaviour; cleanup can destroy evidence. **Notice:** traversal and symlink tests leave outside sentinel files untouched, and a previous `mutants.json` cannot satisfy a new run’s output check.

5. **F11 and F17: validate evidence at entry — my #9 and my #17.**  
   For **F11**, validate JSON roots, entries, required keys, types and referenced ids before verdict logic accesses them. Malformed input produces a documented exit-2 diagnostic or an explicit UNKNOWN, according to the command’s contract; it never produces PASS.

   For **F17**, check `done`, the current invocation’s required output file, its validity, and available execution metadata. If the harness cannot establish the actual model used, record that as unverified and treat the engine constraint as unmet.  
   **Risk:** stricter validation rejects previously tolerated output. **Notice:** missing keys, lists in place of objects, null probes, `done: false` and missing files produce controlled outcomes without tracebacks or stale success.

6. **F5: separate test failure from inability to run the test — my #9 and my #10.**  
   Represent execution status separately from each probe’s result. An outer timeout, missing report, collection failure or broken mutant import supplies no mutation proof. PASS needs the same identified probe to pass on the product and complete with a relevant assertion failure on the intended mutant.

   If the requirement concerns a hang, the probe can observe a bounded subprocess and deliberately assert on that behaviour; a timeout of the entire pytest run remains missing evidence.  
   **Risk:** some current PASS results become UNKNOWN, and fewer mutants count as useful. **Notice:** hanging and syntactically broken mutants cannot grant PASS, while a valid behavioural mutant still can.

7. **F4: measure before execution and require affirmative restoration evidence — my #9; implementation details are my reading.**  
   Take the baseline hash before product probes run. Compare after execution, record any mutation, and verify restoration against that original baseline. Require `restored is True`; missing, null and false supply no restoration proof. A detected mutation invalidates affected evidence even if restoration later succeeds.  
   **Risk:** hashing adds work and detects tests that write caches or generated files into the protected copy. **Notice:** a probe that changes a protected file is caught, and absent restoration evidence cannot support PASS.

8. **F19: return the authoritative verdict — my #9.**  
   Have the runner read and validate `verdict.json` and relay a structured result rather than interpret prose. Tie it to the current run.  
   **Risk:** workflow callers may need an interface update. **Notice:** misleading runner text cannot override the JSON verdict, and missing or stale verdict files cannot produce success.

9. **F9: enforce access boundaries outside the briefs — my #5; containment design is my reading.**  
   Give the mutant writer a dedicated view containing its permitted inputs, with probes inaccessible and writes confined to its output area. Execute probes with access restricted to the disposable workspace and necessary runtime resources. Changing the working directory alone does not establish either boundary.

   If the existing harness cannot enforce those restrictions, report F9 unresolved and stop affected execution until an enforceable boundary exists.  
   **Risk:** this may be the largest repair and can break dependencies that assume broad filesystem access. **Notice:** actual denial checks show the mutant writer cannot read probes or write outside its area, and probes cannot alter the original product.

10. **F8: make workspace exclusions additive and observable — my #9.**  
    Exclude nested test directories, test files and `conftest.py`; preserve default exclusions when adding custom ones. Pass product-specific exclusions from the workflow, including identified build notes. Record what was excluded.

    Do not silently classify every Markdown file as a build note.  
    **Risk:** a product may put runtime assets in a directory named `tests`, or need a broadly matched file. **Notice:** fixtures containing nested tests and notes exclude them, while required runtime files remain usable. Exact build-note identification needs the product’s input list.

11. **F3, F14 and F20: account for every requirement and citation — my #9 and my #10.**  
    For **F3**, fix citation extraction to preserve the complete hyphenated id, then validate it against manifest case ids. Ensure `EV-P1-F2` is not interpreted as a shorter suffix.

    For **F14**, report unsupported id-bearing syntax and reconcile candidate ids with the manifest. An unresolved omission makes the input incomplete; it cannot quietly disappear.

    For **F20**, report probes with absent or unknown citations.  
    **Risk:** broader parsing can misidentify prose, while stricter accounting exposes existing malformed documents. **Notice:** supported ids survive unchanged; unsupported forms and uncited probes appear explicitly in diagnostics.

12. **F2: remove the plant answer from the judge’s accessible inputs — my #2 and my #9.**  
    Keep plant identity in coordinator-only state. The judge receives the cases and product evidence needed to judge them, without a field, filename or accessible side file identifying the planted case. Perform the clean comparison independently so the first judgment cannot contaminate it.  
    **Risk:** this changes input contracts and may lower measured plant detection. **Notice:** inspect the judge’s complete accessible input set, then compare planted and clean judgments. Removing the leak makes the check more meaningful; it does not establish general judging accuracy.

13. **F6 and F7: implement the promised retries as explicit state — my #9.**  
    For **F6**, record whether the one repair round has been consumed. Repair the unfaithful probe, rerun it against the product and relevant mutants, and confirm any resulting red product outcome again. Old execution evidence cannot justify the repaired probe.

    For **F7**, void the failed judging attempt, select a different plant, and rerun judging in a fresh session once. Keep attempt evidence separate; a second failure leaves affected judgments UNKNOWN. If no different plant is available, report that limitation.  
    **Risk:** extra model calls and matrix execution consume time and money; accidental reuse can contaminate retries. **Notice:** scripted model responses demonstrate the single retry limit, changed plant, fresh invocation and rejection of stale evidence.

14. **Finish F15, F13, F16 and F18 without expanding the repair — my #13 and my #18 (`attributed`).**  
    Make duplicate classifications human (**F15**); shell-quote repro arguments (**F13**); retain out-of-scope reasons (**F16**); record elapsed time and available cost data, with unavailable cost explicitly marked (**F18**).  
    **Risk:** duplicate handling increases human work, report changes affect consumers, and cost may be unavailable. **Notice:** duplicate cases remain visible, quoted repros execute correctly, reasons survive aggregation, and recorded measurements identify their units.

15. **Ship changes that remain understandable when separated — my #5 and my #19 (`attributed`).**  
    Keep each logical fix together across its affected files. Preserve frozen tests and add regression tests. Use different engines for tests and implementation where possible, as the brief requests.  
    **Price:** smaller changes require more validation steps, but make a failed repair easier to locate and reverse.

## What I need to know

- **What deadline does one working session mean, and is it a hard stop or a target?** Requirement-check: **source, one thing and links pass; unit, can it fail, weak words, level and basis fail or remain unspecified.** If the deadline is hard, unfinished findings stay explicitly open; safety and evidence checks do not become optional.
- **Which existing mechanism can enforce read and write isolation?** If one exists, use it for F9. If none exists, the brief does not establish that all repairs fit the session.
- **Are same-id reruns required, and which product files count as build notes or required runtime inputs?** These answers determine whether rejecting existing runs and applying exclusions would break an intended workflow.

## Costs and risks

- **More UNKNOWN results — my #2 and my #9.** Removing false proof reduces apparent success. Investigate lost valid evidence separately from corrected false positives.
- **Broken legitimate workflows — my #1 and my #3.** Isolation, exclusions and run-directory changes need checks against actual product usage, beyond synthetic fixtures.
- **Additional calls and execution time — my #18 (`attributed`).** Measure retry costs; the brief supplies no basis for promising completion within the session.
- **Evidence-contract migration — my #9 and my #19 (`attributed`).** Producers and consumers need compatible changes together. Older evidence without required fields cannot acquire proof through permissive defaults.

## How we would know I was right

**My proposed checks, not yet run — my #2 and my #3:**

- Each finding has a regression test that passes with the fix and fails when that fix is undone. Record who wrote the test and who implemented the fix.
- The frozen suite still passes. Repeat the live calibration and investigate any loss of the previously observed fault detection or spec-mismatch detection.
- Empty specs, missing reports, broken mutants, stale files and malformed JSON cannot produce affirmative MEETS.
- Requirement ids remain accounted for; isolation checks demonstrate denied access; the original product remains unchanged.
- Retry checks demonstrate the prescribed single repair or rerun and fresh evidence.

Tests written for these repairs establish the tested behaviours. They do not independently prove that the evaluator satisfies every requirement or that its model judgments are faithful.