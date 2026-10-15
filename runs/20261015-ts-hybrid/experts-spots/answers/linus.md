# Linus Torvalds — Missing facts and reversible choices

## Answer

My reading: **U1** needs a session/run ownership contract; **U2** conflicts with mandatory insight completion; **U3** needs real tool payloads; **U4** can provisionally keep Python; **U5** needs an isolated hook canary; **U6** can provisionally use YAML; **U7** needs approval and rollback rules; **U8** merits a separate correctness fix; **U9** remains an unmeasured protocol; **U10** needs evidence per adapter and event. I also raise **N1** guard failure behavior, **N2** missing enforcement triggers, and **N3** evidence validity; I recommend proving one complete path before expanding, with any deferral put to EJ.

## How I decided

1. **U1 — Establish ownership before choosing storage. My #9 and my #5.**  
   The missing facts are whether sessions span runs, runs span sessions, and child agents share identifiers. A per-session journal alone does not answer which failures an insight must cover. Test two concurrent sessions, a restart, and a retry before accepting the mapping. Keep stable failure IDs and versioned records so changing the mapping does not discard evidence. **Price:** more explicit bookkeeping; the benefit is avoiding another session’s failure blocking unrelated work.

2. **U2 — A retry escape does not establish mandatory completion. My #2 and my #7; the requirement judgment is my reading.**  
   AC4 explicitly permits stopping without the insight. Recording `insight_skipped` makes the omission visible; it does not satisfy R12.3. We also lack runtime evidence that `stop_hook_active` identifies this guard’s previous block across the proposed harnesses.

   Applying requirement-check to AC4: **pass** one thing, unit, can it fail, and weak words—the event, block count, and flag are explicit. **FAIL** who decides—the authority to waive R12.3 is unresolved; **FAIL** level—the escape weakens a MUST; **FAIL** basis—the flag behavior was not exercised; **FAIL** links—AC4 contradicts the stated insight requirement.

   Keep loop protection separate from whether the task is recorded as complete. **Price:** an incomplete task may need a separate completion status and recovery path; repeated blocking can obstruct useful work. EJ decides the acceptable escape.

3. **U3 — Command patterns are a hypothesis about observability. My #2 and my #9.**  
   Matching an engine name does not yet establish its exit status, output location, completion, or expected result form. The missing cases include wrappers, quoted paths, pipelines, background jobs, and nested engine calls. Native subagent calls also need an explicit scope decision.

   Capture actual payloads and normalize recognized calls into one result record. Where observation is insufficient, report that limit instead of treating the call as successfully checked. Keep recognition separate from evaluation so replacing a parser does not rewrite the journal. **Price:** unsupported forms remain visible gaps; supporting arbitrary shell syntax could become a much larger project.

4. **U4 and U6 — Keep these choices cheap to reverse. My #5 and my #13.**  
   Keeping the existing Python probes avoids a rewrite already outside scope. Missing facts are their invocation cost, output contract, and failure behavior when called by `doctor`. YAML parsing is reported as exercised; register semantics remain undecided. Put validation over parsed data and version the schema, so serialization can change independently. **Price:** Python remains a runtime dependency, and schema changes may require migration. Neither choice presently justifies blocking unrelated research.

5. **U5 and U10 — Prove an adapter by its behavior. My #2, my #3, and my #13.**  
   Shared field names do not prove identical response handling, timeouts, retry behavior, or tool-result shapes. First demonstrate a denied trap, an observed failed result, and a Stop decision through one actual harness using the proposed temporary settings. Verify what inherited configuration remains active.

   Then qualify each additional adapter by the events it demonstrably supports. The proposed opencode adapter implements linting only; it cannot establish journal and insight enforcement. Would EJ defer additional adapters until one complete path works? **Price:** narrower initial coverage, but each adapter remains independently replaceable.

6. **U7 — Catalogue placement is easy; authority is consequential. My #5 and my #9.**  
   A package data file is reversible. Automatically adding an insight’s proposed fix is inconsistent with EJ’s choice being required before application. Separate proposed entries from approved entries, and identify which catalogue version produced each denial. Exercise both a real trap and a similar clean command before trusting an entry. **Price:** review delays new protections; careless patterns can block valid work. Reverting an entry should preserve its failure history.

7. **U8 — Judge the dispatcher fix by correctness, not line count. My #1 and my #19.**  
   My #19 is **attributed** process guidance in the supplied list. The reported `status: fail` becoming `done` is a concrete correctness hole. Recommend a separate patch with a reproducer that fails before the fix and passes afterward, regardless of whether the repair takes one line. Check adjacent result states before choosing the change. **Price:** added scope and a separate review; isolation makes the patch independently revertible. This advice does not authorize applying an R12 insight fix without EJ’s choice.

8. **U9 — Freeze the comparison before claiming effectiveness. My #18 and my #7.**  
   My #18 is **attributed** guidance. Missing facts include the model and effort, number of independent tasks, corpus selection, outcome measure, and EJ’s criterion for a useful improvement. Count missed failures and incorrect blocks on valid work, alongside execution cost.

   Separate historical replay from live agent behavior, and separate initial results from results after enhancement. Reusing examples to tune the guard makes later scores evidence of repair on those examples, with limited evidence of generalization. **Price:** independent evaluation consumes additional tasks and time. Leave sample size and success thresholds open.

9. **N1 — What happens when the guard itself fails? My #1, my #2, and my #5.**  
   Missing technical facts include harness behavior on handler crash, malformed response, timeout, unreadable evidence, or failed journal writes. PostToolUse annotation cannot undo the engine call that already happened. Exercise these paths before claiming failure handling is enforced.

   Also resolve how recording inputs and actual results preserves evidence without printing secrets. Deleting code cannot reverse disclosure. **Price:** failure handling and redaction add complexity; retaining less raw data can reduce diagnostic detail.

10. **N2 — Several checks still lack an unavoidable trigger. My #2 and my #13; the gap assessment is my reading.**  
    M4 has a validator, but the design names no fixed event that requires it to run. A command mentioned in a skill can still be skipped—the original problem. Register validation also does not itself judge whether a result violates an accepted case or requirement.

    The design needs explicit owners, triggers, and limits for the remaining R11–R13 obligations, including final-report escalation and model-change review. Would EJ implement these now or explicitly narrow this iteration’s claim? **Price:** completing them increases scope; deferral leaves named obligations unenforced.

11. **N3 — Valid records are not necessarily valid evidence. My #9 and my #7.**  
    A current hash detects changes relative to a recorded hash; it does not alone establish that units were frozen before case generation. A populated acceptance field does not establish EJ’s decision. An existing evidence file does not establish that a planted repeat failed the check. Three to six populated why fields do not establish a researched root cause—and the draft’s required depth needs reconciliation with M3.

    Recommend references to recorded acceptance, preserved freeze history, and actual check outcomes, while leaving causal judgment with the agent and reviewer. **Price:** stronger provenance costs storage and review time; mechanical checks still cannot certify the judgment.

## What I need to know

- **U1:** Can one session serve several runs, and can several sessions or child agents contribute to one run?
- **U2:** Does EJ permit stopping with unresolved insight obligations, and if so, who authorizes the exception and what completion status remains?
- **U9:** Which model, effort, task count, and improvement comparison does EJ choose?
- **U10 / N2:** Which harnesses and R11–R13 obligations must this iteration enforce, and which may be deferred explicitly?
- **N3:** Is the required why depth exactly six or three to six, and what recorded evidence establishes EJ’s acceptance and fix choice?

## Costs and risks

- **My #3:** Passing fixtures can coexist with broken user workflows; valid everyday commands need coverage.
- **My #5:** Reverting implementation does not recover leaked secrets, lost evidence, or wasted work.
- **My #13:** Building every adapter before proving one complete path risks spending effort on an incorrect shared assumption.
- **My #18, attributed:** A small or repeatedly tuned corpus supports a limited claim; broader effectiveness remains **not measured**.

## How we would know I was right

Run the same valid and deliberately failing tasks through the rules-only control and one real hooked harness, under the protocol EJ chooses. Observe whether failures retain evidence across retries, each failure reaches the correct insight obligation, valid commands remain usable, and each installed adapter performs its claimed events.

Then replace or disable an adapter and revert a catalogue entry while preserving the journal and existing workflows. That demonstrates reversibility.

The proposed checks above are my recommendations; I have not run them. Their eventual authors should be named. Fixture success would establish behavior on those fixtures, not universal observability, sound causal analysis, or effectiveness across all harnesses.