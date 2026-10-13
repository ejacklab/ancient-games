# Reading W5.3 and Rd5.3 (codex)

This is my reading of the two requirements and their checks, using the requirement-check skill. The brief identifies the COO as their author. EJ’s quoted words support the core intentions; they do not establish every added detail. No implementation behavior was measured.

## W5.3

| question | pass / FAIL | why |
|---|---|---|
| Source | pass | The brief identifies the COO, the date and EJ’s exact words; W5.3 also attributes its lifecycle statement to EJ. |
| One thing | FAIL | It combines when a decision starts, who records completion, when they record it, and what they record. |
| Unit | pass | There is no numerical threshold needing a unit; “the time” identifies a recorded field. |
| Can it fail | FAIL | A missing `done:` line fails, but an empty line or `done: TBD` passes the stated presence check despite supplying no completion evidence. |
| Weak words | FAIL | “The work it governs is complete” and “a finished task” lack a common scope: finishing one task need not finish the work governed by a decision. |
| Level | FAIL | The text does not distinguish a gate that stops work from a default that permits an explained exception. |
| Basis | FAIL | EJ supplies the start/completion intention and asks for a judged check; the worker-specific duty and line-presence test lack a separately stated basis. |
| Links | pass | W5.3 does not assert an unsupported equivalence or relationship to another numbered requirement. |

**Conflicts — my reading:**

- **W4.1:** No direct conflict. Assigning the worker responsibility for recording completion does not expressly forbid someone else from editing the entry. Whether a successor may discharge that responsibility remains unclear.
- **K1.1:** No inherent conflict. Recording results after implementation is different from changing the governing choice after implementation.
- **Rd5.1 and Rd5.3:** Checking before acting is compatible with completion recording, but Rd5.3’s blanket instruction not to change a mismatching entry can block it. Concrete case: a worker implements the recorded 30-second timeout and obtains passing results; another change restores 60 seconds before completion is recorded. W5.3 calls for adding the completion record, while Rd5.3 prohibits changing that entry after the mismatch is found.
- **Vision:** Its completion statement supports W5.3. There is a separate tension with its prohibition on copying information available from tests or the commit log, also expressed in W3.1. Concrete case: a commit already records the completion time and test results; copying those into `done:` satisfies the apparent completion wording but duplicates commit-log information. A reference might satisfy both, but the requirement does not say.

**Wrong case — my reading:**

A finished task’s decision contains only `done: TBD`. The reviewer finds a `done:` line, so W5.3’s stated check passes, although the time, result and test results are absent. W1’s missing-field check does not explicitly establish that these contents are valid either.

Obvious fix: judge the required completion contents, rather than merely the existence of the line.

**COO additions for EJ to confirm:**

- The particular `done:` field and placement in the decision entry.
- Assigning the recording duty specifically to “the agent or person who did the work.”
- Using a reviewer of a finished task as the check’s trigger.
- Treating the absence of a line as the completion failure test. EJ’s “ok make it judged” supports human judgement, but does not specify this test.
- Whether completion results may be recorded through evidence references to avoid duplication.

## Rd5.3

| question | pass / FAIL | why |
|---|---|---|
| Source | pass | The brief identifies the COO’s wording and the reporting/non-editing rule EJ agreed to transfer from the background subagent to readers. |
| One thing | FAIL | It combines an editing prohibition, a reporting duty, report contents and EJ’s authority to choose the remedy. |
| Unit | pass | There is no numerical quantity or threshold needing a unit. |
| Can it fail | FAIL | The check catches some unreported actions and premature edits, but can pass when a reader discovers a mismatch and never reports it. |
| Weak words | FAIL | “No longer matches” does not distinguish unintended drift from the expected difference between a newly written requirement and code awaiting implementation. |
| Level | FAIL | It does not state whether reporting is a default or a gate, or whether implementation must wait for EJ’s decision. |
| Basis | FAIL | Reporting and non-editing have quoted support; making EJ choose the remedy and rejecting resolution before that choice are additional judgements without their own stated basis. |
| Links | pass | No explicit equivalence to another numbered rule is asserted; the operational conflicts below still need resolution. |

**Conflicts — my reading:**

- **W4.1:** Rd5.3 introduces an exception to “Anyone … may create or change any entry” and “There is no owner and no approval.” Concrete case: a reader discovers that a factual constraint was entered incorrectly and has its primary source. W4.1 permits a logged correction; Rd5.3 prohibits that correction and assigns the remedy decision to EJ.
- **K1.1:** Changing the decision first deliberately creates a temporary mismatch. Concrete case: an agent changes the recorded timeout from 30 to 60 seconds before changing the implementation. The next reader sees a 60-second requirement and 30-second code. Rd5.3 does not explain how to distinguish this expected implementation state from drift requiring EJ’s decision.
- **Rd5.1:** Checking before acting is consistent with Rd5.3. However, the check’s phrase “without saying so” is weaker than reporting the specified information to EJ. Concrete case: an agent writes “mismatch noticed” in its journal and proceeds; it has said so, but has not made the required report to EJ.
- **Vision:** The vision explicitly supports readers checking, reporting mismatches and not editing entries. It also says there are no owners or approval gates and that decisions change before code. Those statements preserve the same tensions; the vision does not explicitly assign EJ the final remedy choice.

Obvious fix for the implementation-order conflict: distinguish a recorded change awaiting implementation from unintended drift.

**Wrong case — my reading:**

A reader checks a decision requiring a 30-second timeout against code using 60 seconds, then ends the session without acting, editing or reporting. Neither branch of Rd5’s stated failure check fires. The check passes despite the reader violating Rd5.3’s reporting duty.

Obvious fix: judge whether a discovered mismatch received the required report, including when no subsequent action or edit occurred.

**COO additions for EJ to confirm:**

- The report’s required contents: which entry, what it says and what the code does instead. These are sensible details, but exceed the quoted reporting instruction.
- “EJ decides whether the entry is updated or the code is fixed.”
- The check that rejects an entry change settling the mismatch before EJ decides.
- Whether “does not change the entry” prohibits every edit, including recording completion evidence, or only an edit resolving the mismatch.
- Whether the judged check covers people as well as agents: the requirement says “reader,” but its first failure branch says “an agent.”

## Questions for EJ

1. For W5.3, what makes the work governed by a decision complete when that decision spans multiple tasks or remains an ongoing constraint?
2. Must the original worker record completion, or may another agent or person do it from the evidence after a handoff?
3. Should W5.3’s check reject missing, empty or placeholder time, result and test results, rather than checking only for a `done:` line?
4. May `done:` reference recorded evidence instead of copying results already available from tests or the commit log?
5. Should Rd5.3 distinguish expected differences during implementation from unintended drift?
6. Does EJ choose the remedy before anyone resolves a mismatch, or is the intended obligation only to report it without changing the governing entry?
7. Does Rd5.3 prohibit every edit to a mismatching entry, including completion recording, or only edits that resolve the mismatch?
8. Should Rd5’s check require the specified report to EJ from any reader who discovers a mismatch, even if they take no further action?
9. For each requirement, is failure a gate that stops work or a default that can be overridden with a stated reason?
