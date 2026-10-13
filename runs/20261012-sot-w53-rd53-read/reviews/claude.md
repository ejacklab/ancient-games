# Reading W5.3 and Rd5.3 (claude)

Read: `docs/memory-system/SOURCE_OF_TRUTH.md` (whole file, working-tree version with the 2026-10-12 revision),
the vision statement, and `~/.agents/skills/requirement-check/SKILL.md`. Every verdict and case below is **my
reading** of the text. None of it is measured. The cases are constructed examples, not observed runs.

## W5.3

> W5.3 A decision is started when it is written. When the work it governs is complete, the agent or person who did
> the work adds `done:` to it: the time, the result and the test results (EJ, 2026-10-12).
> Fails if … a reviewer of a finished task finds that the decision it carried out has no `done:` line (judged; EJ,
> 2026-10-12).

| question | pass / FAIL | why |
|---|---|---|
| source | FAIL (partial) | One label "(EJ, 2026-10-12)" covers the whole line. EJ's words cover "started when written" and "time, results, test results". "The work it governs", "the agent or person who did the work" and the check's wording are the COO's, and nothing marks them. |
| one thing | FAIL | Three statements: a definition ("started when written"), a duty (who adds `done:` and when), and a content rule (time, result, test results). The content rule also repeats W1.2. |
| unit | FAIL | "The time" is undefined. It could be when the work finished or when the line was written, and it has no format. It also duplicates the `changed:` time that W4.2 already requires for the same edit. |
| can it fail | FAIL | The check only tests whether `done:` exists. `done: — / result: done / tests: n/a` passes. The check runs only if "a reviewer of a finished task" exists, and the design names no reviewer role and no time when a review happens. |
| weak words | FAIL | "Complete" and "the work it governs" have no test. Nothing says who decides that the work is complete, or what "the result" must say. |
| level | FAIL | It is not marked MUST, SHOULD or guidance. This is true of the whole requirements section. |
| basis | pass | EJ is quoted for both the rule and the judged check ("ok make it judged"). |
| links | FAIL | The check assumes a link from a task to "the decision it carried out", but no field or file records that link: no `work/<task-id>` field on the decision and no decision id required in `state.md`. W1.2 makes `done:` a header field for a "complete" decision, but a lint cannot tell complete from started (see the wrong case). |

**Conflicts**

- **W2.1 (what a decision is).** W2.1 says a decision is *"a choice the code must follow"*, which is a standing
  constraint. W5.3 treats a decision as a piece of work that finishes, matching EJ's *"we decided to build
  something"*. Case: `D-7 "all timestamps are UTC"` governs every future change. It never becomes "complete". If the
  first task adds `done:`, every later task under D-7 still has to follow it, and the old `done:` describes only the
  first task.
- **W4.1 (anyone may change any entry).** "The agent or person who did the work adds `done:`" can be read as
  exclusive. Case: agent A finishes the work and its session is cut off before it writes `done:`. Agent B, in the
  next session, sees the gap. W4.1 lets B add it. W5.3 says the doer adds it. B would also be writing test results it
  did not see run.
- **W3.1 (nothing readable from the tests).** W3.1 forbids *"which test covers it"*. A natural `done:` line,
  `tests: test_index_gen.py::test_regen passes`, names which test covers the decision. A judge cannot tell whether
  that is a test result (required by W5.3) or test coverage (forbidden by W3.1).
- **W1 Fails if (lint).** W1.2 lists `done:` as a header field on a complete decision. A lint over `entries/`
  cannot tell complete from started. If it requires `done:`, it fails every started decision. If it treats `done:` as
  optional, it never catches a missing one.
- **Rd5.3.** At completion, the doer may find that the result differs from the decision. Case: `D-4 "use SQLite
  FTS"`, but FTS failed and the work shipped with grep. The doer writes `done: result: used grep instead; tests
  pass`. That `done:` edit records, and in effect settles, a decision/code mismatch before EJ has decided. Rd5.3's
  check forbids exactly that.
- **K1.1 (entry first, then the code).** There is no real conflict. `done:` records the outcome; it does not change
  behaviour, so writing it after the code is not "the other way". A side note on K1, not on W5.3 (my reading): K1's
  check accepts any earlier change to the entry, so once `done:` (or the first write) exists, a later commit that
  changes behaviour with no entry change still passes.
- **Vision.** It is consistent: the vision states the same start/complete rule in EJ's words.

**Wrong case**

- *Passes when it should fail:* `done: 2026-10-13, result: done, tests: none` exists, so the reviewer finds a
  `done:` line and the check passes. The time is ambiguous, the result says nothing, and there are no test results.
- *Passes when it should fail:* D-7 is later edited in place under K4.3 to change its behaviour, and the new work is
  finished. The old `done:` line is still there and describes the old version, so the check passes.
- *Fails when it should pass:* D-7 (a standing decision) is carried out in part by task T-1. A reviewer of T-1 finds
  no `done:` and fails it, but D-7's work is not complete and never will be.

**COO additions for EJ to confirm**

- "The work it governs": mapping EJ's "we decided to build something" onto W2.1's standing-choice definition.
- "The agent or person who did the work" as the writer. EJ said "you put", which is close, but whether this is
  exclusive is the COO's choice.
- The field name `done:` and its place in the header (W1.2).
- The timing-table row "When the work a decision governs is complete".
- The check's wording: "a reviewer of a finished task" and "the decision it carried out". EJ said only "make it
  judged".

## Rd5.3

> Rd5.3 When a decision or fact no longer matches the code, the reader does not change the entry. It reports to EJ
> which entry, what the entry says, and what the code does instead, and EJ decides whether the entry is updated or
> the code is fixed.
> Fails if an agent acts on an entry that its `covers` code contradicts, without saying so (judged), or a `changed:`
> line on a decision or fact settles such a mismatch before EJ has decided.

| question | pass / FAIL | why |
|---|---|---|
| source | pass (weak) | It is labelled (d) under Rd5, which is accurate for design text. EJ's agreement (*"ok remove both and update the doc"*) is not cited at Rd5.3, although W5.3 cites EJ the same way. |
| one thing | FAIL | Three statements, filled by two people: the reader's ban on editing, the reader's report (three items), and EJ's decision. By the "who fills it" rule, EJ's decision is a separate artifact. The check is also two clauses. |
| unit | pass | No numbers. The missing piece is where the report goes, which is a links/fail question, not a unit question. |
| can it fail | FAIL | The check does not test that the report was made, that it reached EJ, or that it holds the three items. The removed K3 check did ("reaches EJ without the entry, the claim and the code behaviour"), and that part was dropped. Clause 2 needs to know when "EJ has decided", but nothing records EJ's decision, so a judge cannot tell. |
| weak words | FAIL | "No longer matches" has no test. "No longer" assumes the code once matched, which is not true of a decision whose code is not written yet. "The code" is narrower than Rd5.1's "code, test or commit". The check narrows it again to "its `covers` code". |
| level | FAIL | It is not marked. "Does not change the entry" reads as a MUST, but nothing says so. |
| basis | pass | It is carried over from the removed K3.2, and EJ agreed to the transfer. Whether readers will in fact catch drift is unmeasured (n=0). That is accepted in the vision ("nothing else watches"), so it is not a defect. |
| links | FAIL | Rd5.3 is an exception to W4.1 ("anyone may change any entry") and to "no approval gate", and neither text says so. It has no link to W5.3, although `done:` is the only thing that tells a started decision from a drifted one. |

**Conflicts**

- **K1.1 (entry first, then the code).** K1.1 creates a mismatch on purpose: the entry changes, then the code
  catches up. Case: agent A writes `D-9 "logs are JSON"` and commits it. Agent B, or A in its next session after a
  handoff, reads D-9 before editing `logger.py` (Rd4.1), checks it against the code (Rd5.1) and finds text logs.
  Rd5.3 says: do not change D-9, report to EJ, and EJ decides. The implementer is now blocked by, or must report, the
  very gap it was asked to close.
- **K1.1 again, on a drifted decision.** Agent C is tasked to change behaviour under D-5, which has already drifted.
  K1.1 says edit D-5 first. Rd5.3 says do not edit D-5. A judge cannot tell whether C's `changed:` line is a new
  decision (allowed) or a settled mismatch (forbidden).
- **W4.1 / vision "no approval gate".** Rd5.3 makes EJ the only one who can resolve a decision/code mismatch, which
  is an approval gate on that path. The vision states both lines, so this is not a contradiction with the vision.
  But W4.1 reads as having no exception. Fix (one line): add "except as Rd5.3 says" to W4.1.
- **Rd5.1.** Rd5.1 checks against "the code, test or commit it points to". Rd5.3 reacts only to a mismatch with
  "the code". Case: D-2 says "retry 3 times", the code retries 3 times, and the test asserts 5. Is that a mismatch
  for EJ, or one the reader may fix?
- **Rd6.1 (fresh session follows decisions without asking EJ).** Case: a fresh session finds D-3 contradicted by the
  code and reports to EJ, as Rd5.3 requires. Rd6's check fails a session that "asks a question that a decision entry
  … already answers", and D-3 does answer it. The two checks pull in opposite directions. Fix (one line): Rd6's check
  excludes a Rd5.3 report.
- **Vision "nothing is lost between sessions".** The report has no stated home. Case: an agent reports the mismatch
  in its chat, EJ is away, and the session ends. Nothing on D-3, in `state.md` or in `INDEX.md` shows that D-3 is
  under question, so the next reader acts on D-3 or reports it again.
- **W5.3.** See above: a `done:` line whose result differs from the decision settles a mismatch.
- **Fine:** Rd5.3 covers only decisions and facts. A lesson, observation, hypothesis or runbook that is out of date
  may be fixed by the reader under W4.1. That is consistent and needs nothing added.

**Wrong case**

- *Fails when it should pass:* the D-9 case above. The decision is started but not done, so a mismatch with the code
  is expected. Rd5.3, with no started/complete distinction, requires a report to EJ and forbids touching the entry.
- *Passes when it should fail:* an agent finds D-3 ("retry 3") against code that retries 5. It changes the code to 3
  without asking EJ and writes "fixed retry count to match D-3" in its journal. Clause 1 passes because it said so.
  Clause 2 passes because there is no `changed:` line on D-3. But Rd5.3 gives the choice between "update the entry"
  and "fix the code" to EJ, and the agent made it.
- *Passes when it should fail:* an agent writes "D-3 looks stale" in its own journal and carries on. That counts as
  "saying so", but the report never reaches EJ and has none of the three items.
- *Passes when it should fail (facts):* `F-2 "the vendor limit is 100 req/min"`. The vendor moves to 50. The code
  still matches F-2, so Rd5.3 never fires, although both are wrong. A fact is about the outside world, and checking
  it against the code cannot find this.

**COO additions for EJ to confirm**

- "The reader does not change the entry". EJ's agreed phrase was "checks it against the code, and reports a
  mismatch". The ban on editing was carried over from one special actor (the subagent) to every reader, including the
  agent carrying out the decision, and people.
- The three report items, and "EJ decides whether the entry is updated or the code is fixed". These come from K3.2's
  text; EJ did not restate them.
- Both clauses of the check, including the narrowing to "its `covers` code".

## Questions for EJ

1. W5.3: a decision is "a choice the code must follow" (W2.1). For a standing decision that governs many tasks, when is it complete, and does each task add its own `done:`?
2. W5.3: is "the agent or person who did the work" the only one who may add `done:`, or may anyone (W4.1), for example the next session when the doer was cut off?
3. W5.3: who is "a reviewer of a finished task", and when does that review happen?
4. W5.3: what must `done:` hold when the work has no tests? Does "none" pass?
5. W5.3: may `done:` name the tests that ran, given that W3.1 forbids "which test covers it"?
6. W5.3 / Rd5.3: when the result at completion differs from the decision, does `done:` just record it, or is it a Rd5.3 mismatch reported to EJ first?
7. Rd5.3: does it apply to a decision with no `done:` yet, where K1.1 makes a mismatch with the code expected?
8. Rd5.3: until EJ decides, does the reader stop, follow the entry, or follow the code?
9. Rd5.3: may the reader fix the code to match the entry without EJ? (The check does not catch this today.)
10. Rd5.3: where does the report go so that it outlives the session and the next reader can see the mismatch is already reported?
11. Rd5.3: does the ban on editing bind people, and EJ himself, as well as agents? Should W4.1 name it as an exception?
12. Both: MUST, SHOULD or guidance?
