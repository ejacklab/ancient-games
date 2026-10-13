I'll read the brief first.
# Reading W5.3 and Rd5.3 (opencode)

Both requirements trace to real EJ words, and the removal of the drift-check script and the background subagent is
carried through the design consistently (l.10–12, l.79–82, l.212–214, vision l.50–53). What I did not find is a
requirement that is simply wrong; what I found is wording that over-reaches EJ's words, three rules that contradict
each other on the same actor, and two checks that pass or fail on the wrong thing. Nothing below is fixed by me; every
missing value goes to EJ at the end.

## W5.3

> **W5.3** A decision is started when it is written. When the work it governs is complete, the agent or person who did the work adds `done:` to it: the time, the result and the test results (EJ, 2026-10-12).
> **Fails if (W5 part):** For W5.3, it fails if a reviewer of a finished task finds that the decision it carried out has no `done:` line (judged; EJ, 2026-10-12).

| question | pass / FAIL | why |
|---|---|---|
| 1. Source | pass | EJ, 2026-10-12, quoted verbatim in vision l.27–29; the requirement repeats it. The check's judged nature is EJ's own (*"ok make it judged"*). What inside it is the COO's is listed further down. |
| 2. One thing | **FAIL** | Two statements in one: a definition (*"a decision is started when it is written"*) and an obligation on an actor (*"the agent or person who did the work adds `done:`"*). They fail separately — a decision can be correctly started with no `done:`, and one can be wrongly given a `done:` while never having been started. |
| 3. Unit | pass | No number in it; the three `done:` contents are each a named thing, not a count. The open item is *which* time (start or end), which is a question below, not a missing unit. |
| 4. Can it fail | pass | `TBD`, `—`, empty and `0` are all in the failing set: a decision file whose `done:` block is absent, or present with any of its three fields empty, fails. The check names the input. |
| 5. Weak words | **FAIL** | *"when the work it governs is complete"* — "complete" is never defined, and neither EJ's sentence nor the design says whether it means *implemented* or *implemented and tested*. W3.4 draws exactly that line, so the design depends on the answer and does not state it. "The work it governs" also has no end for a decision that governs a standing property. |
| 6. Level | pass | An obligation on a named actor that gates what the entry is — a gate, not a method preference, so MUST-level is earned. (The first half is a definition and carries no level, which is the same split as Q2.) |
| 7. Basis | pass | EJ's own words, quoted. The surrounding header already labels the timing split as design judgement, not measured (l.18–19), so nothing is smuggled here as measured. |
| 8. Links | **FAIL** | Two undeclared relations. (a) `done:` is written **after** the code, which is the reverse of K1.1's entry-first ordering and is asserted nowhere else — EJ's sentence does not say it. (b) The same completion idea now appears three times with no cross-reference: l.53–54, l.12, and vision l.27–29. Each is a link with its own source. |

**Conflicts:**

1. **W3.1 — `done:` asks for what W3.1 forbids.** W5.3 requires the result and the test results; W3.1 says nothing
   that can be read from the code, the tests or the commit log goes in, naming "what a commit changed".
   *Case:* D-07 "use library A for retries". Work lands; `done:` reads "retry added in `src/http.ts`, 3 tests in
   `http_test.py` pass". Every word is in the commit. Either W5.3 means a pointer (commit sha, test-run link) or W3.1
   is violated; the requirement does not say which.
2. **W3.4 — a permanent "verified" claim with nothing watching.** `done:` records that the work was verified. Nothing
   watches (K2 and K3 are gone). *Case:* `done: 2026-10-12, tests pass`. Three weeks later a PR changes
   `src/http.ts`. The entry still says the work is verified and now is not. W3.4 forbids describing work as verified
   when it is only implemented; W5.3 makes exactly that state permanent and unchecked.
3. **W4.1 + Rd6.1 — the named actor is usually not there.** W5.3 assigns `done:` to "the agent or person who did the
   work". The design's own premise is that context is cleared every session (l.24), that unfinished work is handed off
   (W5.1) and that a fresh session carries it on (Rd6.1) — so the worker is normally a *different* engine from the
   writer. W4.1 says anyone may change any entry. *Case:* `claude` writes D-12 on Monday; a handoff; `opencode`
   implements it on Wednesday. W5.3 names nobody who exists; `opencode` is the only candidate but is not named.
4. **W6.2 + W6 "Open" — the completion step can be blocked by an unanswered question.** `done:` is an edit to the
   entry header, the same header block another agent may be editing concurrently, on its own branch. *Case:* agent B
   edits D-12's body on its branch; agent A adds `done:` to D-12; the two meet as a merge conflict; W6 leaves
   "who resolves a merge conflict" open, so the only remaining way for A to finish the requirement is to be the one who
   resolves it — which nobody decided.
5. **K1.1 — the requirement adds an undeclared post-code edit to a decision entry.** Not a contradiction (K1.1 allows
   the same commit) but it means every completed decision is edited twice, before and after the code, and only one of
   those edits is governed by a stated rule. Same finding as the Links FAIL above.

**Wrong case:**

- **Passes when it should fail.** The check counts a `done:` line, not its content. A decision written with
  `done:` already present but empty — `time: —, result: TBD, test results: pending` — satisfies it. Nothing in W5.3 or
  W3.4 forbids an empty `done:`; a reviewer looking for the line finds it. A decision can be declared complete with
  nothing in it, which is the one failure mode EJ's sentence exists to prevent.
- **Fails when it should pass.** A decision that governs a standing property — D-01 "every entry is one markdown file",
  D-02 "no entry is deleted" — has no end, so its work never completes and no `done:` is due. But the check reads "the
  decision **it carried out**", and any finished task that touched the covered code carries such a decision out. A
  reviewer then finds a missing `done:` line and fails a decision that was never complete and never should be.

**COO additions for EJ to confirm:**

1. The field name **`done:`**. EJ said "you put the time and results, test result those into your memory"; the earlier
   vocabulary in `DESIGN-detailed` l.29 was `verified_at` / `observed_at`. The rename and the field-as-header-block
   form are the COO's.
2. The three contents **time / result / test results** as a required set. EJ listed them in one breath; the design makes
   all three mandatory on one line, with no field allowed to be absent.
3. **"the agent or person who did the work"** — EJ named no actor. W4.1's "anyone" is the opposite choice, and the
   design does not reconcile them.
4. **Decisions only.** W1.2 puts `done:` on decisions alone. EJ's words were about memory generally, and a fact (a
   constraint the code must respect) has exactly the same started/finished problem.
5. **"a reviewer of a finished task"** — the judge and the trigger. EJ said *judged*; who reviews, and what counts as
   a finished task (blocked? abandoned? superseded mid-work?), are the COO's.
6. **`done:` after the code**, as an edit to the entry — the reverse of K1.1's ordering, added by the COO (see Links).

**What is fine.** The requirement is short, its three fields are named, and the check does have a concrete failing
input. The split from W5.1 and W5.2 is clean: this is the only timing rule that closes an entry, and it closes it once.

## Rd5.3

> **Rd5.3** When a decision or fact no longer matches the code, the reader does not change the entry. It reports to EJ which entry, what the entry says, and what the code does instead, and EJ decides whether the entry is updated or the code is fixed.
> **Fails if (Rd5):** Fails if an agent acts on an entry that its `covers` code contradicts, without saying so (judged), or a `changed:` line on a decision or fact settles such a mismatch before EJ has decided.

| question | pass / FAIL | why |
|---|---|---|
| 1. Source | pass | EJ's agreement is recorded (*"ok remove both and update the doc"*) and vision l.50–53 carries it. The three contents of the report are not EJ's sentence — they are the removed subagent rule verbatim (`DESIGN-detailed` l.33), which EJ had read and approved before removing the subagent. Traceable, so pass; the inheritance is listed below. |
| 2. One thing | **FAIL** | Three actions in one sentence: (a) do not change the entry, (b) report three things to EJ, (c) EJ decides whether the entry or the code changes. (c) is not a requirement on the agent at all — it is a statement about a future human act, and it sits in a requirements block as if it were one. |
| 3. Unit | pass | No number. "Which entry" is identified by id, which is one thing and one unit. |
| 4. Can it fail | pass | Concrete failing inputs on both halves: a `changed:` line on a decision or fact settling a mismatch before EJ decided, and an agent acting on contradicted code without saying so. `—` and empty are in the failing set. |
| 5. Weak words | **FAIL** | *"no longer matches the code"* is never defined — it does not say whether the mismatch is in the `covers` paths, in the claim, in `How to apply:`, or in the `done:` line, and those fail differently. The prose version (l.81) says "When **they** no longer match" with a singular antecedent. *"reports to EJ"* has no channel and no deadline. |
| 6. Level | pass | A gate that stops work — the reader does not change — so MUST is earned and it is not a method. (Again the EJ-decides half is not the agent's gate.) |
| 7. Basis | pass, labelled | EJ's decision, quoted. But the whole rule rests on one unmeasured assumption — that a reader always checks — and unlike the timing split (l.18) nothing in the document says so here. |
| 8. Links | **FAIL** | Three undeclared relations. (a) It carves decisions and facts out of W4.1's "anyone may change any entry", without W4.1 knowing. (b) It is the stated replacement for the removed K2/K3 — that link *is* declared and sourced (l.212–214), and is the best-sourced part of the requirement. (c) K4.2 ("found out of date only when someone reads it and checks it") is the same claim in a third place, with no cross-reference to either. |

**Conflicts:**

1. **Rd5.1 + Rd5.3 + the Fails-if contradict each other, inside Rd5 itself.** Rd5.1 tells the agent to check and
   nothing about what to do when the check fails. The Fails-if punishes "acts on an entry that its `covers` code
   contradicts, without saying so" — which reads as: report, then act is fine. Rd5.3 says report and EJ decides,
   which reads as: wait. *Case:* an agent reads D-30, finds `covers: src/auth.py` no longer matches the claim, reports
   it to EJ in the session, EJ is busy, and the agent implements D-30 as written to unblock the task. Under Rd5.1 plus
   the Fails-if, having said so, it passes; under Rd5.3 it has acted before EJ decided. Two readings, opposite
   verdicts, same act.
2. **K1.1 vs Rd5.3 — and both checks fire whichever branch is taken.** K1.1: change the entry first, then the code; its
   Fails-if fires if the code's behaviour changed with no entry change. Rd5.3: the reader does not change the entry;
   its Fails-if fires on a `changed:` line settling a mismatch before EJ decided. *Case:* task "switch the retry
   library". D-07 says library A; a later PR moved the code to B and did not touch D-07.
   — Follow K1.1: edit D-07 to B, log `changed:` → Rd5's Fails-if fires ("settles such a mismatch before EJ has decided").
   — Follow Rd5.3: report to EJ and wait → the task stays undone, and if the agent implements B anyway, K1.1's
   Fails-if fires (behaviour changed, entry not changed first).
   There is no branch of this case that satisfies both. This is the sharpest conflict in the two requirements.
3. **W4.1 vs Rd5.3 — the permission and the carve-out.** W4.1 grants everyone, including EJ ("A decision about this
   project is a project entry, whoever made it, EJ included", l.31), the right to change any entry. Rd5.3 forbids the
   reader from doing so, without exempting EJ, and makes "EJ decides" a separate step from "EJ changes". *Case:* EJ
   reads D-30 on Monday, sees the code moved on, and fixes the entry with a `changed:` line. Under a literal reading
   that is the Fails-if's "a `changed:` line settles such a mismatch before EJ has decided" — unless deciding and
   fixing are one step, which nothing says. Under Rd5.3 read as binding agents only, it is fine. Undefined either way.
4. **Rd4.1 × Rd5.3 — an unpriced per-edit obligation.** Rd4.1: before editing a file, read every entry whose `covers`
   includes it. Rd5.3: each of those must then be checked against the code before acting. *Case:* a file covered by
   ten entries means ten checks on every single edit, with no shortcut and no stated basis for the cost. This is not a
   contradiction, but it is a MUST with no measured basis anywhere in the document.
5. **A dropped open item.** `DESIGN-detailed` l.36 said "How the report reaches EJ is a build detail, not decided
   here." The removal of the subagent took that sentence with it, and the **Still open:** list (l.84–85 — K6, W6,
   K4.3) does not carry it forward. The question EJ had already deferred is now silently answered by omission.

**Wrong case:**

- **Passes when it should fail.** An agent reads D-30, finds the mismatch, edits the entry, and writes
  `changed: 2026-10-12 EJ — agreed, code was wrong, updated to B`. Both halves of the check pass: the Fails-if's second
  clause is satisfied because a `changed:` line exists and, on its face, EJ decided; the first clause is satisfied
  because the agent said so. Nothing in the design verifies that EJ was asked, and nothing records the report — the
  channel was dropped (conflict 5). An entry can therefore be silently rewritten with a fabricated decision and pass
  every check the design has.
- **Fails when it should pass.** The one case Rd5.3 does not carve out is the reader who is *about to make* the change
  that closes the gap. *Case:* an agent notices `F-11` says the CI runner is Ubuntu 22.04; it is 24.04; the agent's
  task is to upgrade it. K1.1 requires the fact to change first; Rd5.3 says the reader reports and does not change;
  the Fails-if then fires on the `changed:` line it just wrote. The correct, K1.1-compliant sequence is a violation of
  Rd5.3. This is not a rare corner: it is every fact that changes, and every decision whose own implementation reveals
  it was miswritten.

**What is fine.** The removal itself is carried correctly and consistently in all four places it should be (l.10–12,
l.79–82, l.212–214, vision l.50–53), the decision and fact carve-out is the right scope (the other kinds are supposedto go stale freely), and the check's first half — *without saying so* — does catch a silent reader who acts.

## Questions for EJ

W5.3:

1. Does "complete" mean the work is **implemented**, or **implemented and its tests pass**? W3.4 draws that line, so the
   answer changes what `done:` asserts.
2. Does `done:` hold the **results themselves**, or pointers to the commit and the test run? As written it asks for
   what W3.1 forbids.
3. When the work was done by a **different agent, or in a later session** than the one that wrote the decision, who
   adds `done:` — the worker, or anyone (W4.1)?
4. What does a decision whose work never finishes (a standing rule), or is superseded or abandoned mid-work, get
   instead of `done:`?
5. Does adding `done:` also add a `changed:` line (W4.2 requires one for every change), or is `done:` its own log?
6. Who is **"a reviewer of a finished task"**, and when does it review? You said *judged*; the judge and the trigger
   are mine, not yours.
7. What does `done:` say when the governed work **shipped with no test** — "no test", or does the decision stay
   incomplete forever?
8. Is `done:` for **decisions only**, or do facts need it too? Your words were about memory; W1.2 narrowed it to
   decisions.
9. Should `INDEX.md` (K6.1) show which decisions are complete? `status` has only three values, so today nothing outside
   the entry file knows.

Rd5.3:

10. What counts as **"no longer matches the code"** — a changed `covers` path, a changed claim, a changed `How to
    apply:`, a stale `done:` line? Give one example, so the check can be applied to it.
11. Does Rd5.3 bind **EJ as well as agents**, and may EJ decide and fix in one step, or must the fix be a second act?
12. Does Rd5.3 have an **exception for the reader who is about to make the change** that closes the gap, as K1.1
    requires? Without it, the correct sequence is a violation.
13. After reporting a mismatch, may the agent **proceed to implement the entry as written**, or must it wait for EJ?
    Rd5.1 says only "check"; the check punishes acting.
14. Must the agent check **every entry covering a file on every edit** (Rd4.1 × Rd5.3), or only when the code looks
    like it changed? Ten checks per edit is a real cost and nothing in the design prices it.
15. How does a report **reach EJ, and by when**? That was an open item before the subagent was removed
    (`DESIGN-detailed` l.36) and is no longer on the **Still open:** list — was it closed, or dropped?

### One-line fixes, only where the fix is obvious

- **W5.3:** give "complete" the condition you used — the work is done and, where tests exist, their results are added —
  so the requirement stops depending on a word the design defines elsewhere.
- **Rd5.3:** add one clause — this rule does not apply to the reader who is making the change that closes the gap
  under K1.1 — and say whether it binds EJ.
- **Rd5.3 check:** the second clause should fire when a report was made *and* EJ did not decide, not only on the
  `changed:` line; today the edit is checked and the report is not.
- **Design l.84:** put the report channel back on the **Still open:** list if it is still open.
