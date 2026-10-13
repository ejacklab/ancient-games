I'll read the brief first.
# Item 8, runbooks (opencode)

## Recommendation

**Drop the runbook kind entirely — (b), tightened — *proposed*: memory holds no procedures, so remove `R-` and the runbook definition from the design; a procedure lives as a script (or a document in `docs/`) next to the code that runs it, and the reason and the when stay in the kinds that already exist — decision, fact, lesson — linking to it exactly as W3.6 already links to `docs/`; the vision is left as EJ wrote it, and no scope, folder, field or when-to-write row is added.**

## Three reasons

**1. A prose runbook is the one artefact this environment's own procedure rule rejects, and the design already half-rejects it. *design / skill***
The skill is blunt: *"The procedure is the memory. A prose description of a procedure is a summary of the memory, and summaries drift"* (procedure-to-skill SKILL.md, l.15–16), and its only exception is a step-less fact. W2.2 *design* writes exactly the rejected shape, then concedes it — *"says how to run or fix something **and points at a script where one exists**"*. Deleting the kind makes the script mandatory by construction: the script *is* the runbook, and nothing is left behind to drift.

**2. W3.1 already forbids most runbooks, and the design already has the "link, don't copy" rule for the rest. *design***
*"**W3.1** Nothing that can be read directly from the code, the tests or the commit log"*; the vision *EJ* names the same failure: *"A copy goes stale when the code changes"* (vision l.46–48). A runbook saying "run `make test`, then `make deploy`" is a paraphrase of a Makefile. What is left over is a pointer to a procedure — and for that the design already has the pattern: *"**W3.6** No copy of the project's existing documents (requirements, architecture in `docs/`): an entry links to them."* A procedure belongs in that same family: the thing itself lives with the code, memory points at it. No new rule needed, only W3.6 applied once more.

**3. Deleting the kind makes W2's `(v)` citation true for the first time, and nothing unique is lost. *design***
W2 is headed *"(v; d: What it is for)"* — it claims the vision as its source. But the vision *EJ* says only *"what was **learned** after: lessons, observations and hypotheses"* (l.23). W2.2 *design* adds a fourth kind the vision has no word for, so today that `(v)` is a claim the vision does not support; after the deletion, W2.2's three kinds *are* the vision's three. And everything a runbook carried has an existing home: the **steps** → the script; the **reason to run it** → a decision (*"a choice the code must follow, with the reason"*, W2.1); the **environment, order, what to check afterwards** → a fact (*"a truth or outside constraint the code must respect"*, W2.1); the **failure that made the procedure necessary** → a lesson (W2.2). Four existing kinds, zero new mechanism. Worth noting: the runbook is the only kind whose end-of-task write has no **Fails if** clause behind it — W5's group check names only decisions-before-code, human corrections and W5.3. Removing it removes a gap, not a check.

## Text changes

**Scope, before the edits — *proposed*: project, always.** A procedure is for the next agent and the next task, never for one person or one agent. So it lives next to the code it operates (a script, or a document in `docs/`), and the entry that links to it is a project-scope entry in `project-memory/entries/`. *Not task:* a one-off repair inside one task stays in that task's `state.md` and `evidence/` and dies with the task, because nothing after that task needs it. *Not agent or user:* W3.5 *design* — *"No user memory … and no agent memory … Both live in the home folder"*; a procedure only one agent needs is that agent's own notes, not shared memory.

**Vision — `vision-statements/source-of-truth-memory-vision-statements.md`**

*Default: no change.* The vision never mentioned runbooks, so deleting them restores it rather than editing it. The vision is EJ's (*"an agent may only write down what EJ has said"*), and I am not inventing his sentence. One sentence is offered, under **What it will never do**, immediately after the first bullet, as the guard that stops the kind creeping back — **it carries [proposed] until EJ says it, per the file's own header**:

> *proposed:* "It never holds a procedure. A procedure lives as a script next to the code that runs it, and an entry links to the script rather than repeating its steps."

If EJ prefers no change at all, everything below still stands; only that guard is lost.

**Design — `docs/memory-system/SOURCE_OF_TRUTH.md`, six places *design* names runbooks. Every requirement keeps its existing Fails if, quoted unchanged below.**

**1. What it is for, l.63** — delete the bullet in full:
> `- A **runbook** says how to run or fix something; where possible it points at a script.`

No **Fails if** lives on this section (the checks sit on the requirements), so nothing is lost here; W2.2's check is inherited, below.

**2. When to write, table, l.95:**
> Before: `| At the end of a task | Other lessons, observations and hypotheses; merging duplicates; runbooks. |`
> After: `| At the end of a task | Other lessons, observations and hypotheses; merging duplicates. |`

**Fails if** unchanged — W5's group check reads: *"a commit changes code under a new decision with no entry in that commit or an earlier one. For a human correction, it fails if the session ends without one (judged)…"*. It names no runbook clause, so the row loses nothing by losing the word.

**3. Where it is put, layout, l.127:**
> Before: `  entries/           one file per entry: D- decision, F- fact, L- lesson, R- runbook`
> After: `  entries/           one file per entry: D- decision, F- fact, L- lesson`

l.135 *design* — *"File prefixes for observations and hypotheses: `O-` and `H-`, proposed in W1.1"* — needs no edit; it already names only `O-` and `H-`.

**4. W1.1, l.181–183:**
> Before: *"The prefixes are `D-` decision, `F-` fact, `L-` lesson and `R-` runbook, plus `O-` observation and `H-` hypothesis (*proposed*; the design leaves these two open)."*
> After: *"The prefixes are `D-` decision, `F-` fact and `L-` lesson, plus `O-` observation and `H-` hypothesis (*proposed*; the design leaves these two open)."*

**Fails if** W1 keeps, verbatim: *"a lint over `entries/` finds a missing field or section, or a reviewer finds two claims in one entry."*

**5. W2.2, l.195–197:**
> Before: *"A **lesson** comes from a failure or a human correction. An **observation** records what was seen. A **hypothesis** is a guess, labelled as one. A **runbook** says how to run or fix something and points at a script where one exists."*
> After: *"A **lesson** comes from a failure or a human correction. An **observation** records what was seen. A **hypothesis** is a guess, labelled as one."*

**Fails if** W2 keeps, verbatim: *"`kind` holds any other value, or a guess is recorded under any kind but hypothesis."* — and this is the check that now enforces the deletion: `kind: runbook` is "any other value" and fails. No new check is needed.

*Optional, pending Question 1 — *proposed*: one closing sentence, *"A procedure is not a kind: it lives as a script next to the code, and an entry links to it the way it links to a document in `docs/` (W3.6)."*

**6. W5.2, l.224:**
> Before: *"**W5.2** Written at the end of a task: other lessons, observations, hypotheses, and runbooks."*
> After: *"**W5.2** Written at the end of a task: other lessons, observations and hypotheses."*

**Fails if** W5's group check, as quoted at 2 above.

**Two dependent docs, so the change is complete (not named in the brief, but both name the kind)**

**7. `docs/index-md/REQUIREMENTS.md` B2.4, l.39** — *"a `kind` from the six (decision, fact, lesson, runbook, observation, hypothesis)"* → *"a `kind` from the five (decision, fact, lesson, observation, hypothesis)"*. **Fails if** B2 keeps verbatim, and *"a prefix/kind mismatch passes"* now catches an `R-` file twice over — once on `kind`, once on prefix.

**8. `docs/index-md/DESIGN.md` step 5, l.48–49** — *"`kind` not one of the six; file prefix not matching `kind` (D decision, F fact, L lesson, R runbook, O observation, H hypothesis)"* → *"`kind` not one of the five; file prefix not matching `kind` (D decision, F fact, L lesson, O observation, H hypothesis)"*.

No code change is needed: `tools/memory_index.py` is not written yet, and `project-memory/entries/` holds no files, so there is nothing to migrate.

## What could go wrong

**One concrete case: a repair that has judgement in it and will not be run twice.** Say a production incident needs a database repair where the *order* of the steps depends on what you find when you look, and no one will ever run it as a routine. It is not a script (the branch depends on what is observed), it is not a standing instruction (nobody is "always" going to hit it, so `AGENTS.md` is the wrong home and would be read by every session for nothing), and it is not a decision or a fact — nothing about the code must follow it. Under this way it lives in that task's `evidence/` and is gone when the task is. That is exactly the loss the memory exists to prevent: *"The context window is cleared at the start of every session, so anything learned is lost unless it is written down"* (design l.35).

The failure is silent, which is what makes it the real risk: no lint fails, no **Fails if** fires, because nothing is written. K5.2 is the only net — it forces the journal read at task end (*"reads what is worth keeping as entries"*). If that repair is still in the journal then, it gets written as a decision or a fact, or scaffolded into a script by the procedure-to-skill rule; if it is missed, it is lost. The cheap escape hatch, needing no new mechanism: it goes in `docs/` as a project document and a decision entry links to it under W3.6. I would not add a runbook kind to insure against one case; I would name it here so the hole is known.

Second-order, and the reason for the optional vision sentence: with the design silent on procedures, the first person who hits that case is likely to conclude runbooks are wanted after all, and the round starts again. One sentence in the vision closes that.

## Questions for EJ

**1. If a procedure cannot be a script, where does it live — `AGENTS.md` or `docs/`?** This decides whether W2.2 keeps the optional closing sentence above and whether it names `AGENTS.md` or `docs/`, and it decides whether the design's "project documents stay in `docs/`" line needs to name procedures too. If the answer is "either, link it", I drop the sentence and the design stays silent, which is the simplest outcome.

**2. Do you want the one-line "it never holds a procedure" in the vision, or the vision untouched?** If you want it, it becomes your words and I label it [EJ]; if not, the change is design-only and the guard against the kind creeping back is gone. Nothing else in my text turns on this.
