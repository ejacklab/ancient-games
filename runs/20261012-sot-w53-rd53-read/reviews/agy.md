# Reading W5.3 and Rd5.3 (agy)

## W5.3

| question | pass / FAIL | why |
|---|---|---|
| Source | pass | Sourced to EJ (2026-10-12) regarding decision start/completion and the judged check. |
| One thing | FAIL | Combines lifecycle definition ("started when written") with update actions ("adds `done:`") and bundles three distinct fields (time, result, test results). |
| Unit | pass | No countable quantities or numerical thresholds; time format and duration units are left open. |
| Can it fail | pass | A finished task whose governing decision lacks a `done:` line fails the check. |
| Weak words | pass | Contains no prohibited vague qualifiers (*appropriate*, *reasonable*, *fast*, etc.). |
| Level | FAIL | Written in declarative indicative prose ("adds `done:`") with no RFC 2119/8174 uppercase keyword (MUST/SHOULD). |
| Basis | pass | Based on EJ's explicit statements on 2026-10-12 (n=1). |
| Links | pass | Links completion of work to recording outcome/test results, directly derived from EJ's definition. |

**Conflicts:**
- **Conflict with [W4.1](file:///home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md#L178-L185) and [Vision](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/source-of-truth-memory-vision-statements.md#L31-L34) ("anyone may change any entry; no owners"):** W5.3 restricts writing `done:` to "the agent or person who did the work". If an agent implements a change but is interrupted or handed off before running verification, a subsequent verifying agent or reviewer is technically barred from recording completion. *Concrete case:* Agent A implements the code changes for Decision `D-12` and hands off; Agent B executes tests, confirms success, and finishes the task, but cannot write `done:` without violating the clause that only the worker who did the work adds it.
- **Conflict with [K1.1](file:///home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md#L206-L211) ("change the decision first, then the code"):** Decisions are requirements set before code. Modifying the decision entry in-place to append post-hoc completion data (`done:`) causes git commits modifying decision entries to appear after code changes. *Concrete case:* An agent commits code and test files, then in a follow-up commit adds `done:` with test metrics to `D-3`; git history shows a decision modification occurring after the code, which triggers K1.1's check failure.
- **Conflict with [W3.1](file:///home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md#L166-L177) ("nothing that can be read directly from code, tests or commit log"):** Embedding test results and run timestamps into the decision entry duplicates data already stored in git commit history and test execution logs. *Concrete case:* An agent records "15 passed in 0.2s" in `done:`; subsequent test runs render this recorded test output stale.
- *One-line fix:* Allow anyone who finishes or verifies the task to append completion metadata (`done:` timestamp, outcome summary, test status) without treating it as an alteration of the requirement claim.

**Wrong case:**
- *Fails when it should pass:* A task delivers an assigned milestone of a large decision that spans multiple tasks. A reviewer checks the completed task, observes that the broader decision lacks a `done:` line (because remaining tasks are ongoing), and incorrectly fails the task.
- *Passes when it should fail:* An agent appends `done: yes` or records failing test results (`done: 2026-10-12, failed 4 tests`). The check passes mechanically because the `done:` line exists, even though complete details are missing or the work failed.

**COO additions for EJ to confirm:**
- Restricting the author of `done:` to "the agent or person who did the work" (EJ stated: *"when done, you put the time and results , test reuslt those into your memory"* without assigning ownership).
- Specifying the exact YAML header key name `done:`.
- Formalizing the check as an explicit evaluation by a "reviewer of a finished task".

---

## Rd5.3

| question | pass / FAIL | why |
|---|---|---|
| Source | pass | Attributed to EJ's instruction ("ok remove both and update the doc") adapting the removed subagent rule to readers. |
| One thing | FAIL | Combines three distinct rules: prohibition against reader editing, mandatory 3-part reporting, and an approval gate requiring EJ to decide. |
| Unit | pass | Contains no numerical quantities or metrics. |
| Can it fail | pass | An agent editing a mismatched entry before EJ decides, or acting on a contradicted entry without reporting, fails the check. |
| Weak words | FAIL | "No longer matches" and "without saying so" are unquantified and lack concrete definitions. |
| Level | FAIL | Imposes a blocking approval gate and absolute prohibition without RFC 2119/8174 uppercase keywords (MUST/MUST NOT). |
| Basis | pass | Based on EJ's agreement to move background drift reporting to the reader (n=1). |
| Links | pass | Replaces the removed drift-check script ([K2](file:///home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md#L212-L215)) and background subagent ([K3](file:///home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md#L212-L215)) as referenced in [K4.2](file:///home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md#L219-L220) and [Rd5.1](file:///home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md#L271-L274). |

**Conflicts:**
- **Conflict with [W4.1](file:///home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md#L178-L185) and [Vision](file:///home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/source-of-truth-memory-vision-statements.md#L31-L34) ("anyone may change any entry; no owners and no approval gate"):** W4.1 explicitly establishes that there is no approval gate and anyone may change any entry. Rd5.3 contradicts this by prohibiting readers from modifying the entry and requiring that work wait until EJ decides. The check even fails if a `changed:` line settles the discrepancy before EJ decides. *Concrete case:* An autonomous batch runner encounters Fact `F-2` stating default timeout is 10s, while the code explicitly sets 30s. Under W4.1, the agent should update `F-2` and log the change in `changed:`; under Rd5.3, the agent is barred from updating `F-2` and must halt execution waiting for human approval.
- **Conflict with [K1.1](file:///home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md#L206-L211) ("change the decision first, then the code"):** When code has drifted ahead of a decision and EJ rules that the code is correct, the reader updates the decision retroactively. Git history then records the code change before the decision update, triggering K1.1's check failure. *Concrete case:* A commit changes an API signature; when an agent later discovers that Decision `D-6` still specifies the old signature and EJ approves updating `D-6`, updating the decision creates a commit sequence violating K1.1.
- **Conflict with [Rd6.1](file:///home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md#L281-L285) ("a fresh session carries on... without asking EJ again"):** Requiring human arbitration whenever code and memory diverge blocks unattended, multi-session autonomous handoffs.
- *One-line fix:* When an entry contradicts code, the reader records the discrepancy in the task journal or handoff state and alerts EJ, without blocking actions on unrelated tasks or precluding bug-fixing assignments.

**Wrong case:**
- *Fails when it should pass:* An agent assigned specifically to fix code that violates Decision `D-8` reads `D-8`, inspects the code, sees the mismatch, and proceeds to implement the code fix. Because it acted on a contradicted entry without first stopping to report the mismatch to EJ, it fails the check.
- *Passes when it should fail:* An agent detects that a critical Decision `D-4` contradicts code, emits a one-line log notice ("Note: D-4 contradicts code"), and then proceeds to build features relying on the invalid decision. Because the agent did not act "without saying so", it passes the literal check despite executing work against a contradicted requirement.

**COO additions for EJ to confirm:**
- The rigid 3-part reporting schema ("which entry, what the entry says, and what the code does instead"), which was copied from the COO's draft for the discarded background subagent.
- The check rule failing any `changed:` line that settles a mismatch before EJ has decided (imposing an approval gate).
- The escape clause "without saying so" in the check text.

---

## Questions for EJ

1. May any agent or person who completes or verifies a task write `done:` on the governing decision, or strictly only the original implementer?
2. When a decision spans multiple tasks or phases, should `done:` record phase progress or only be added once all governed work is completed?
3. When a reader detects a mismatch between code and an entry, does work halt until you decide, or may the reader proceed if its task is explicitly to reconcile them?
4. Where should an agent report a mismatch when you are not present in an interactive session (e.g., in `state.md`, `journal/`, or a dedicated issue log)?
