# Harness requirements R11–R13 — draft

Status: R11.1 complete. R11.2 proposed. R12 (R10 and R12 merged) proposed. R13 written from the project owner's answers.
History and who proposed what: `state.md`, `experts-r11/compare.md`, `experts-coverage/compare.md`,
`experts-order/compare.md`, `experts-direction/compare.md`.

## R11 — results can be judged

**R11.1 Coverage of a requirement (SHOULD; a target, not a gate).**

1. Before any case is generated, a fixed list of **units** is written: each accepted use case's fails-if and minimum
   acceptance criteria (R13.2), and each accepted requirement's text and fails-if. The list is frozen before coverage
   is counted; a change to it starts a new count.
2. Cases from AI generation and old use cases attach to a unit as evidence. They do not add to the count. A generated
   case that fits no unit is added as a new unit by the plan writer with a written reason, or recorded as out of scope.
3. The plan writer marks each unit **basic** or **skippable** against the written skip criterion (below). An
   independent reviewer checks the marks and returns fail on any mark that breaks the criterion. The project owner
   owns the criterion and reviews the list of skippable units.
4. The target is that at least 80% of the units are covered by tests that can fail, and every uncovered unit is marked
   skippable.
5. An old use case counts for a unit only after it has been shown failing on a planted violation of this requirement.
6. A unit that is a safety bound is never skippable (MUST).

Fails if: the units are written after the cases; a variant of a covered unit raises the percentage; an uncovered unit
is marked basic; a skippable mark breaks the criterion and the reviewer passes it; an old use case counts without
having been shown failing; a safety unit is marked skippable.

**Skip criterion.** A unit is skippable when the damage if it breaks is smaller than the cost of covering it, and the
damage can be undone. Frequency alone never makes a unit skippable.

**R11.2 First signal (SHOULD).** Each judge gives a first signal before its full verdict: a check that runs first, can
fail the result on its own, and takes less time than the prompt it judges. The full verdict runs only after that check
passes, and its expected duration is written in the design. A judge with no such first check is allowed only with a
reason written into the design.

## R12 — failures, great successes and model changes all update the harness (replaces R10 and the earlier R12; proposed)

**R12.1 Failure handling (MUST — a safety bound).** An evaluator reports fail — never pass — when the result is
missing, empty, of the wrong form, or when the evaluator itself errors or times out. Exit 0 is not success.

**R12.2 Failure log (MUST).** A failure is anything that went wrong while the work was done, whoever caused it: a
check that returned fail (a test run, a linter, a gate), a tool call that errored, an engine result that fails R12.1,
work that had to be undone or redone, and a correction from the project owner. Every failure is logged when it happens,
as one record: what was checked, the input,
the expected and the actual result, the engine and harness that produced it, the reason it is a failure, and the path
to the evidence (the data) in the run folder. Anyone may declare a failure — an evaluator, a retry, the project owner
or another agent — but a record without a reason and evidence is not accepted. A failure is logged even when a retry
later passes.

**R12.3 Insight at the end of a task (MUST).** When a task ends with one or more failure records, the agent that ran
the task writes an insight file in the run folder and raises it to the project owner in its final report. For each
failure, or each group with one cause: six whys down to a source that can be changed (an instruction, a check, a tool,
a config), the root cause, and two or three fix options — each a rule, a check or a tool — that the agent has
researched, ranked by expected effect, with the evidence for each. The agent proposes; it does not apply a fix without
the project owner's choice. A fix that is a check is shown failing on a planted repeat of the failure before it is
trusted. A fix to a harness's config is advice to the project owner; the agent never edits it.

**R12.4 Judges say what is wrong, not how to be right (SHOULD).** An evaluation rule states the conditions that make
a result wrong. It does not prescribe the method, the algorithm or the exact output, so a worker may reach a correct
result by a route nobody wrote down. A judge that compares against one expected output is used only where the output
has exactly one correct form, with that reason written into the design. When an insight finds a wrong result that
broke no stated condition, the missing condition is added to the rule.

**R12.5 Review when a model changes (SHOULD).** When a model the harness uses is replaced or its capability is
re-measured, the harness is reviewed against it. Each scaffolding item names the model weakness it compensates for
and the observable that shows the weakness still occurs. For each item, the review compares a result produced with
the scaffolding against the same result produced without it; where the comparison shows the item no longer
contributes, the item is put up for withdrawal. The comparison and what counts as no contribution are the project
owner's to set.

**R12.6 Withdrawal conditions (SHOULD).** A fix added under this requirement names the observable that would show it
is no longer needed. This requirement is reviewed on R12.5's trigger, and revised or withdrawn when its checks stop
returning failures while the work still passes, under a comparison the project owner sets.

Fails if: an evaluator crash or an empty result is read as pass; a judge rejects a result that breaks no stated
condition only because it differs from the expected method or output; a wrong result that passed every condition
leads to no new condition; a failure a retry later passed, or one found outside an evaluator, has no record; the agent's own failing test run,
errored tool call or redone step has no record; a task
with failure records ends without an insight file, or with one not raised to the project owner; a failure record has
no reason or no evidence; an insight offers fewer than two fix options, or applies a fix the owner did not choose; a why stops at the agent forgetting or the model being wrong; a
check-type fix is trusted without a planted repeat failing it; a model the harness uses changes and no review
follows; a scaffolding item names no weakness it compensates for, or no observable that shows it still occurs; an
item that shows no contribution under the owner's comparison is not put up for withdrawal; the review uses a
comparison the owner did not set; a fix names no observable that would show it is no longer needed.

**R12.7 Learn from success (MUST; proposed).** A failure matters more than a success, but a great success matters too.
Every checked result is recorded — a success as one line (the time, the session, what was checked, the engine or
runner, `ok`), a failure as its full record (R12.2) — so a check's failures can be read against how often it ran. A
task's result is **scored** as the share of its criteria met — each accepted use case's fails-if and minimum acceptance,
and each accepted requirement's fails-if; for a task with no accepted use cases, the agent writes the criteria from the
request before it starts, and the project owner may correct them. Every criterion not met is a failure (R12.2), even
when the task looks done; a total failure is a score of 0 and needs no other rule. When
a task succeeds, the agent records its **path**: the category and objective, the steps in order with the engine, model
and check of each, the decisions that mattered and why, and the measures of the result (time, failures, retries,
checks passed). A **great success** — one that beats the comparison it was measured against (its prediction, the
previous run of the same work, a first pass where the check failed before, or the project owner calls it great) — also
gets an insight in the same file as the failure insights: the cause that made it work, and one to three options to
make it repeatable, each with evidence. For a similar task — the agent proposes the match by category and objective,
and the project owner may overrule — the design **borrows that path, does not copy it**: it starts from the path as its
parent, changes at least one thing (a step, its order, an engine, a check, a brief), and writes before the run what it
changed, the measure it aims to improve — the score, unless it names another — and the parent's value on it. Every
child tries to avoid the failures recorded
in its parent's insights and to be 2% better than its parent — an aim to keep trying for, reported after the run, never a
reason to block or discard the work. A child that improves on its parent's value without repeating those failures
becomes a parent for the next similar task; every path stays recorded, so the paths grow like a population and are
selected by results.

Fails if: a check's successes are not recorded; a task with criteria has no score, or its criteria are written after
the work; a criterion not met has no failure record; a successful task leaves no path, or a path lacks its steps, engines,
checks or measures; a great success has no insight, names no comparison or evidence, or its insight gives no cause or
nothing to repeat; a design for a similar task neither names a parent path nor says why none applies; a design copies
its parent unchanged; the change, the measure or the parent's value is not written before the run; a child that repeats
a recorded failure is counted as better; the report does not say how far the child got against the 2% aim; a child's
result overwrites its parent's path.

Open — the project owner decides (R12.7): where success paths are kept (proposed: the run folder, with one line per path in
`docs/TASK_TYPES_LEDGER.md`); how much a child may change at once (proposed: one change per run, so its effect can be
read); how R12.7 relates to the method's 20% challenger rule (`docs/TASK_TYPES.md`). Also: whether R12.5's review also runs on a schedule; whether R12.6 binds this
requirement itself or only the fixes added under it.

## R13 — use cases and requirements

**R13.1 Two lists, merged into one.** The user writes the basic use cases in one list. The AI agent writes the use
cases it suggests in a separate list. The user accepts or declines each suggestion, and the accepted list — the user's
own cases plus the suggestions the user accepted — is the one list the work is built and judged against. Its maker is
the user. A suggestion enters it only with the user's recorded decision.

**R13.2 What an accepted use case holds.** Its purpose (why it is needed), its fails-if (what makes a result wrong) and
its minimum acceptance criteria (the least that must be observed for a result to pass), each stated as an observable
outcome, never as a method. A use case missing any of the three is not accepted. This applies to the user's own cases
as well as to suggestions.

**R13.3** A result that fails an accepted use case is wrong.

**R13.4 Requirements (SHOULD exist).** A requirement is written where an accepted use case leaves a detail unclear,
and where qualities pull against each other — for example how secure and how fast — in which case it states the
target for each side, as a value or a comparison the user gives. Requirements that cut across use cases (security,
privacy, speed) SHOULD be written.

**R13.5 Who writes a requirement.** The user, or the AI agent from the vision and the accepted use cases. A suggested
requirement binds only after the user accepts it, and an edited requirement needs a new acceptance. Each requirement
states its purpose: the use case or vision line it serves. A requirement whose purpose cannot be named is not
accepted, including one the user asked for.

**R13.6** A result that breaks an accepted requirement is wrong, except where R13.7 applies.

**R13.7 Conflict.** When an accepted use case and an accepted requirement conflict, the use case wins. The conflict is
recorded and shown to the user, naming the use case, the requirement and the result affected; the user decides
whether the requirement is revised or the trade-off is stated in it.

Fails if: an AI suggestion is in the accepted list with no recorded decision by the user; an accepted use case lacks
its purpose, fails-if or minimum acceptance criteria; a result that fails an accepted use case is passed; a suggested
requirement binds before acceptance, or an edited one keeps its old acceptance; a requirement has no named purpose; two
qualities that pull against each other have no target for either side; a conflict between a use case and a
requirement is resolved without being recorded and shown to the user.
