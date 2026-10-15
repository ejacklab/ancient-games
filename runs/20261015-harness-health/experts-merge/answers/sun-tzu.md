# 孫子 (Sun Tzu) — merge R10 and R12 into one harness-health requirement

## Answer

Merge them, but not by keeping R12 and discarding R10. R10's first sentence is R12's loop restated and drops out as true repetition; R10's second sentence — review the harness as models improve, and remove scaffolding that only compensates for a model weakness — is the one thing R12 does not cover, and it must be kept with the two things it lacks: a comparison that can fail, and a stated condition for a rule's own withdrawal. Four points still need EJ's decision; I have not decided them (see *What I need to know*).

**Merged requirement (final text) — Harness health: failures and model changes both update the harness**

1. **Failure handling (MUST — safety bound).** An evaluator reports fail — never pass — when the result is missing, empty, of the wrong form, or when the evaluator itself errors or times out. Exit 0 is not success.

2. **Failure log (SHOULD).** Every failure is logged when it happens, as one record: what was checked, the input, the expected and the actual result, the engine and harness that produced it, and the path to the evidence in the run folder. A failure is logged whether an evaluator, a retry, the project owner, or another agent found it, and even when a retry later passes.

3. **Insight at the end of a task (SHOULD; the planted-check clause and the config clause are MUST — safety bounds).** When a task ends with one or more failure records, the agent that ran the task writes an insight file in the run folder. For each failure, or each group with one cause: six whys down to a source that can be changed (an instruction, a check, a tool, a config), the root cause, and the proposed fix as a rule, a check or a tool. A fix that is a check is shown failing on a planted repeat of the failure before it is trusted. A fix to a harness's config is advice to the project owner; the agent never edits it.

4. **Judges say what is wrong, not how to be right (SHOULD).** An evaluation rule states the conditions that make a result wrong. It does not prescribe the method, the algorithm or the exact output, so a worker may reach a correct result by a route nobody wrote down. A judge that compares against one expected output is used only where the output has exactly one correct form, with that reason written into the design. When an insight finds a wrong result that broke no stated condition, the missing condition is added to the rule.

5. **Harness review when a model changes (SHOULD).** When a model the harness uses is replaced or its capability is re-measured, the harness is reviewed against it. Each scaffolding item names the model weakness it compensates for and the observable that shows the weakness still occurs. For each item, the review compares a result produced with the scaffolding against the same result produced without it; where the comparison shows the item no longer contributes, the item is put up for withdrawal. The comparison and the value that counts as no contribution are the project owner's to set; the agent does not invent them.

6. **Withdrawal conditions (SHOULD).** A fix added under this requirement as a rule, a check or a tool names the observable that would show it is no longer needed. This requirement is reviewed on the trigger in part 5, and is revised or withdrawn when its checks stop returning failures while the work still passes, under a comparison the project owner sets.

**Fails if:**
- an evaluator crash or an empty result is read as pass;
- a judge rejects a result that breaks no stated condition only because it differs from the expected method or output;
- a wrong result that passed every condition leads to no new condition;
- a failure a retry later passed has no record, or a failure found outside an evaluator has no record;
- a task with failure records ends without an insight file;
- a why stops at the agent forgetting or the model being wrong;
- a check-type fix is trusted without a planted repeat failing it;
- a model the harness uses changes and no harness review follows;
- a scaffolding item states no model weakness it compensates for, or no observable that shows the weakness still occurs;
- a scaffolding item that shows no contribution under the owner-set comparison is not put up for withdrawal;
- the review uses a comparison or a no-contribution value the project owner did not set;
- a fix added under this requirement states no observable that would show it is no longer needed;
- this requirement is neither revised nor withdrawn after its checks stop returning failures while the work still passes.

## How I decided

1. **my #1** — 「地生度，度生量，量生數，數生稱，稱生勝」 (`quoted`). The reckoning comes before the commitment, so before merging I laid both texts out as clause rows and compared clause against clause. EJ's impression that they "seem" the same is the question I tested, not the count.

2. **my #4** — 「知彼知己，百戰不殆；不知彼而知己，一勝一負」 (`quoted`). I kept every clause of each side that the other does not carry; dropping a clause only one side had is the knowing-yourself-only half, which the same passage calls one win and one loss.

3. **my #5** — 「合於利而動，不合於利而止」 (`quoted`). A clause is dropped only where it adds no ground the other has not already covered. The one true repetition is the fix types: R10's "a rule, a check, a better tool" and R12.3's "a rule, a check or a tool" are the same list, so one copy is kept (R12.3's).

4. **my #16** — 「約束不明，申令不熟，將之罪也」 (`quoted`). R10's first sentence names no input that can make it fail; under the brief's rule that every check must be able to fail and be shown failing once, it cannot stand as a requirement. R12.1–R12.3 are its clear, drilled orders. So the unfailable frame drops and the loop it describes is kept.

5. **my #6** — 「智者之慮，必雜於利害」 (`quoted`). R10's second sentence names only the benefit of scaffolding — compensation. Its harm, a scaffold kept past the weakness it was built for, is the harm column. That is why it stays in the merged text rather than being dropped: dropping it would leave the merged requirement knowing the benefit only.

6. **my #10** — 「兵無成勢，無恒形，能因敵變化而取勝者，謂之神」 (`quoted`). A harness has no constant form either: the model changes, so the scaffolding must. This is the ground of part 5.

7. **my #2** — 「能為不可勝，不能使敵之必可勝」 and 「無恃其不來，恃吾有以待之」 (`quoted`). EJ cannot make a model improve; they can own the trigger (a model replaced or re-measured) and the observable (the weakness still occurring). So part 5 says what is owned, not "as models improve".

8. **my reading, under the brief's house rule** — the comparison and the no-contribution value in parts 5 and 6 are EJ's to set. I did not invent a number or a measure, because the brief forbids it.

9. **my #12** — 「善戰者，求之於勢，不責於人」 (`quoted`). The six whys must end at a changeable source (an instruction, a check, a tool, a config), never at the agent forgetting or the model being wrong. The fix is sought in the condition, not blamed on the person.

10. **my #17** — 「形之而知死生之地，角之而知有餘不足之處」 (`quoted`). A check-type fix is not trusted until a planted repeat makes it take form and fail. That is part 3's planted check.

11. **my #13** — 「途有所不由…君命有所不受」 (`quoted`). The config is the owner's ground; the agent does not enter it. The fix is advice to EJ.

12. **my #15** — 「凡此六者，非天之災，將之過也」 (`quoted`). A rule that cannot fail, and a check trusted without a planted failure, are the general's faults. Parts 5 and 6 and the Fails-if list exist so every part has a way to fail.

13. **my reading, under the brief's house rule** — levels: MUST only for a safety bound. Part 1 (never read a crash, timeout or empty result as pass) and the planted-check and config clauses of part 3 are safety bounds; the rest are method, so SHOULD. This re-levels R12.2 and the rest of R12.3 from the draft's unmarked default, and EJ may want them held higher.

**What I dropped, and what only one side had**

- **Dropped from R10, as true repetition.** "A feedback loop that improves the harness" is the subject of the merged requirement, not a rule; as a standalone sentence it names no failing input. Its loop is parts 1–4. "Every agent mistake becomes a permanent fix (a rule, a check, a better tool)" repeats R12.3's "a rule, a check or a tool". The single word R12 lacks is *permanent*; I left the fix as *proposed*, because who applies it is open (question 2).
- **Kept, only in R10.** (i) The failure log takes a failure found outside an evaluator: R10's claim is "every agent mistake", while R12.2's log is only what an evaluator finds. I wrote the finders as an evaluator, a retry, EJ, or another agent, and flagged the finders as theirs to confirm. (ii) The whole second sentence — review the harness as models improve; scaffolding that compensates for a model weakness; withdrawal when the weakness is gone — kept in substance as parts 5 and 6, re-wrapped so it can fail.
- **Kept, only in R12.** Part 1's failure semantics (missing, empty, wrong form, evaluator error or timeout; exit 0 is not success). Part 2's record fields and the rule that a retry-passing failure is still logged. Part 3's six whys to a changeable source, the planted check, and config as advice. Part 4 in full.

## What I need to know

- **The comparison and the no-contribution value for parts 5 and 6.** R10 says "as models improve" and names no measure. Is the compared pair "the model's result on the item's failure case with the scaffolding" against "the same without it", or another pair? And what difference counts as no contribution? Without both, part 5 still cannot fail and R10 is unchanged.
- **Who closes the loop on a fix.** R10 says a mistake "becomes a permanent fix"; R12.3 says the fix is "proposed". Does the task-running agent apply a rule, check or tool fix, or only propose it? Config is settled as advice only; the rest is not. This decides whether part 3 says *proposed* or *applied*.
- **Who may declare a failure.** R12's log is "every failure an evaluator finds"; R10's claim is "every agent mistake". I read R10 as wider and wrote the log to accept a failure found by an evaluator, a retry, EJ, or another agent. Confirm the finders, or narrow it back to evaluators.
- **What fires the review.** Part 5 fires on a model replaced or re-measured. Is there also a periodic trigger — per run, per release, per count of runs? R10 names none, and the house rule leaves the period to EJ.
- **Does part 6 bind this requirement itself, or only the fixes added under it?** I wrote it to bind both, because the earlier gap was that a rule which cannot be withdrawn cannot fail. If EJ wants this requirement exempt, part 6 narrows to added fixes.

## Costs and risks

- Keeping R10's second sentence live costs a re-measurement and a keep-or-withdraw decision for every scaffolding item whenever a model changes — work that ships no feature (my #6, my #8). The price of not doing it is scaffolding that masks a capable model and taxes every run.
- Logging and the insight are now SHOULD, so a run can skip them and not be wrong. That is the price of the house rule that a method is SHOULD at most, and it weakens R12 as drafted unless EJ holds them higher (my #16: the level must match the consequence).
- The with-and-without comparison in part 5 needs two runs per item. Run it only when the model actually changed, or it is a second levy for no new ground (my #8, 「役不再籍」, `quoted`).
- The six whys cost time at the end of an already-late failing task (my #8: value victory, not duration).
- Config is advice only: if EJ does not act on it, a root cause the six whys found stays unfixed and the loop leaks (my #13: the road not taken has a price).
- Part 6 can be misread as permission to delete checks. A check withdrawn on a comparison nobody set is exactly the general's fault the Fails-if list names (my #15).
- The review rests on someone noticing the model changed. If no one measures, "as models improve" is again a claim that cannot fail (my #2: own the ground; do not rely on the other side's move).

## How we would know I was right

- **Clause trace.** Take every clause of R10 and R12; a reader who did not write the merge must find each one either in the merged text or in the dropped list with a reason. A clause in neither is content I lost. Unit = the clause (my #20, 「地生度」, `quoted`).
- **Can-it-fail, once per line.** For each Fails-if line, write one planted wrong input and show it fails. R10's second sentence as worded yields no failing input; the merged part 5 must yield one — a scaffolding item with no stated weakness, or one kept after the owner-set comparison shows no contribution (my #15, my #17).
- **The withdrawal drill.** Remove one scaffolding item; run the model on the failure case it was built for, with and without. The merged text must show the decision was made against EJ's comparison, and must contain no number EJ did not give.
- **The permanence trace.** Take one failure record and follow it to either an applied fix or a proposed fix. The result must match EJ's answer to question 2; if it does not, part 3 is ambiguous.
