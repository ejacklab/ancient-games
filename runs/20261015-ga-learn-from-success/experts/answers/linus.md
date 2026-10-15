# Linus Torvalds — Learning from imperfect successes

## Answer

**My reading:** use a working path to find specific improvements, but keep learning from complete failures when they contain reproducible evidence. I recommend retaining failure logging, replacing compulsory explanations with evidence-backed diagnosis, and allowing a successful path to be reused unchanged when there is a stated reason.

## How I decided

1. **Start with what the evidence actually distinguishes — my #2 and my #7.**

   The principle holds when a successful result contains an identifiable defect or waste. For example, a task succeeds after `sed` edits the wrong file and the agent repairs it. The working path supplies a baseline; changing how the file is selected gives a concrete improvement to test.

   It also explains why undifferentiated failures are difficult to select between. Hinton and Nowlan construct an extreme problem in which only the exact solution receives increased fitness; the other candidates supply no fitness ordering toward it. That establishes a limitation of that fitness landscape, not a prohibition on learning from failures. [How Learning Can Guide Evolution](https://www.cs.toronto.edu/~hinton/absps/evolution.htm).

   **Where it breaks:** suppose every task attempt aborts before producing an answer because the runner passes an invalid argument. No task succeeded, but the command, error and a corrected invocation can establish a repair. Discarding those failures would discard useful evidence.

2. **Keep the event separate from the eventual outcome — my #9 and my #11.**

   A successful task can contain failed operations. A failed task can contain successful operations. The records need those relationships before another rule can learn from them.

   **Proposed addition to R12.2:**

   > The failure record SHOULD identify the task, the operation or check, and the evidence needed to locate the event in the task’s path. When recovery is observed, the agent SHOULD link the recovery evidence to the original record. A later task success does not remove that record. An intentionally failing diagnostic or regression test SHOULD be identified as such.

   **Failing check:** a task contains the wrong-file edit, then succeeds, but its failure record disappears. The record check rejects it.

   This preserves the data without treating a deliberately reproduced bug as a newly introduced defect. Its price is additional record linkage.

3. **Do not manufacture a root cause to complete a form — my #2, my #7 and my #13.**

   Six answers are not six pieces of evidence. The brief’s measured results establish behaviour in those trials; they do not establish why a particular instruction, hook or workaround caused it.

   **Proposed replacement for the diagnostic portion of R12.3:**

   > For each failure, or group supported by evidence of a shared cause, the task agent SHOULD trace the explanation to a changeable source and distinguish observations from causal hypotheses. The investigation SHOULD stop when the evidence stops; six why questions may guide it but do not establish a cause. An unresolved insight SHOULD name the missing evidence and propose the next diagnostic check.
   >
   > Where supported, the agent SHOULD provide the existing two or three researched fix options and their expected effects. If fewer are supported, it SHOULD state that limitation rather than invent options. Any ranking SHOULD distinguish measured effects from predictions.

   Keep EJ’s existing choice of fixes and prohibition on agent edits to harness configuration.

   **Failing check:** an insight declares a root cause without supporting evidence and supplies neither an evidence gap nor a diagnostic next step. Reject it. Accept an explicitly unresolved diagnosis with those fields.

   The price is that some tasks end with an honest unresolved problem.

4. **Reuse what works; change it for a reason — my #5 and my #13.**

   Compulsory mutation makes an unchanged reproduction impossible. Sometimes repeating the parent is precisely how we discover whether its apparent advantage survives another run.

   **Proposed replacement for R12.7’s compulsory-change clause:**

   > For a similar task, the design SHOULD name the parent path or explain why none applies. Before execution, the agent SHOULD record either the proposed change and its expected effect, or the reason for reusing the parent unchanged. The comparison SHOULD name the measure, its unit, the direction of improvement, and the parent’s value before execution. Parent records remain intact.

   **Failing check:** a design names a parent but records neither a change nor a reason for unchanged reuse. Reject it. An unchanged run expressly intended to measure baseline variation passes.

   My recommendation is to prefer a single identifiable change when investigating causation, while allowing interacting changes to be tested together with that limitation stated. The price is slower exploration.

5. **Select for the user’s result, then assess the claimed gain — my #1, my #3 and my #18.**

   My #18 is **attributed** kernel documentation, not independently established as Torvalds’s own words.

   A faster child that skips a required check has not established a better path. Conversely, a successful child that deliberately reproduces its parent’s bug to verify a fix should not automatically be disqualified.

   **Proposed replacement for R12.7’s promotion clause:**

   > Before comparison, the agent SHOULD identify the user acceptance checks and disclose differences in task, inputs, engine, model or evaluation conditions. A child SHOULD become a preferred parent only when it meets those acceptance checks, improves the named measure in a comparison supported by the recorded conditions, and does not reintroduce the parent’s recorded defects. Unsupported comparisons remain recorded observations rather than established improvements.

   **Failing check:** a faster child fails a required acceptance check but is promoted. Reject the promotion.

   **Proposed replacement for R12.7’s success-insight claim:**

   > A success insight SHOULD identify the observed result, its comparison, and the evidence for the proposed explanation. Without a discriminating comparison or intervention, the explanation SHOULD be labelled a hypothesis. The project owner calling a result great does not by itself establish its cause.

   **Failing check:** an insight calls an engine switch the established cause of improvement solely because the task succeeded. Reject the causal claim; accept it as a hypothesis.

   **Proposed clarification of the existing 2% aim:**

   > The report SHOULD give the observed change against the named measure. The 2% improvement remains an aim, never an acceptance gate. When the parent’s value is zero, percentage improvement is undefined; report the absolute change and that limitation.

   **Failing check:** a report claims a percentage improvement over a zero baseline. Reject that calculation.

6. **Check the requirements before adopting the proposals — my #7; checklist judgments are my reading.**

   | Criterion | Assessment of the current drafts |
   |---|---|
   | Who decides | **FAIL:** acceptance of evidence and comparative promotion needs an identified decision procedure. |
   | One thing | R12.2 logging **passes**; R12.3 and R12.7 **FAIL** as single requirements because they combine several events and obligations. |
   | Unit | R12.3’s counts **pass**; R12.7 **FAILS** to specify percentage handling and measurement direction. |
   | Can it fail | R12.2 and the supplied R12.7 rejection cases **pass**; R12.3’s claimed cause lacks a falsification condition. |
   | Weak words | **FAIL:** great, similar and better do not all resolve to comparable evidence. |
   | Level | **FAIL under the skill’s method guidance:** these are methods, although EJ expressly chose MUST. I have not overridden that choice. |
   | Basis | Logging has an owner-defined policy basis. The priority of failures, compulsory mutation and learning effectiveness remain **unmeasured**. |
   | Links | R12.2’s R12.1 reference is **unverified here**; the claim that retaining paths creates a selected population is not established. |

   My proposed method clauses use SHOULD. Their benefit in this harness is **n=0**; review them after the first comparable application rather than presenting them as proven improvements.

7. **What my research added — my #2 and my #7.**

   - **Verified mechanism:** Hansen’s CMA-ES tutorial includes negative covariance-update weights for lower-ranked candidates. Evolutionary search therefore does not universally ignore unsuccessful candidates. These candidates have comparative fitness information; this does not establish learning from indistinguishable all-zero outcomes. [CMA-ES tutorial, §3.2](https://arxiv.org/html/1604.00772v2#S3.SS2).
   - **Verified debugging mechanism:** delta debugging starts with a failure-inducing input and reduces it while preserving the failure. A completely unsuccessful execution can therefore support a concrete investigation without an already successful task path. This supplies a practical alternative to unsupported why chains. [The Debugging Book](https://www.debuggingbook.org/html/DeltaDebugger.html).
   - **My reading:** the harness resembles parent-and-child evolutionary search, but calling it exactly a `(1+1)` evolution strategy is stronger than the description establishes. Comparable evaluations and a defined variation-and-selection procedure still matter.
   - **Unverified:** which principle EJ originally learned, whether these proposals improve this harness, and the cause of today’s observed workaround. I did not inspect the harness implementation or independently reproduce the reported trials.

## What I need to know

- Does avoiding a parent’s failures mean avoiding recurrence of its defects, while allowing deliberate failing tests?
- Which user acceptance checks and evidence should authorize parent promotion, and who resolves a disputed or noisy comparison?
- Should EJ’s chosen MUST levels remain, including when an investigation can only report an unresolved cause?

These answers change the final rule text; I have left them open.

## Costs and risks

- **My #9 and my #11:** linking events and recovery increases logging work.
- **My #7:** permitting unresolved diagnoses can leave problems open; requiring a next diagnostic check makes the gap visible.
- **My #5 and my #13:** unchanged repetitions and focused comparisons consume time or engine budget.
- **My #1, my #3 and my #18:** acceptance checks may miss user breakage, and an observed speed gain may be noise. Retaining the parent preserves a way back.

## How we would know I was right

I exercised six illustrative predicates on synthetic records: failure retention, diagnostic support, reuse justification, promotion, causal attribution and zero-baseline arithmetic. Each rejected its planted wrong input and accepted its corrected counterpart. **I wrote these checks; they establish only that those examples are distinguishable, not that the harness implements the proposals or benefits from them.**

For an EJ-authorized trial, compare the existing method with the proposed method on comparable tasks. Record user acceptance, recurrence of defects, diagnosis accuracy on planted causes, total time and engine cost. The recommendation loses support if it produces unsupported explanations, promotes broken paths, or adds investigation cost without an observed benefit. The 2% aim remains a reported aim.