# Item 8, runbooks (claude)

Labels: **[EJ]** his words; **[design]** already in `SOURCE_OF_TRUTH.md`, the vision, or a named source file;
**[proposed]** mine. Line numbers refer to the files as read on 2026-10-13.

## Recommendation

[proposed] Take way (b) without a pointer entry. Drop the runbook kind. A procedure is a script in the repo, or a
page in `docs/` where it cannot be a script. `AGENTS.md` names the scripts, and anything learned while running one
is a lesson. The vision does not change.

**Scope** [proposed]: the procedure belongs to the **project** scope, but it is held as code, a script in the repo,
and not as a memory entry. Its one pointer is a line in `AGENTS.md`, which the design already counts as project
memory ([design] *"project: the rest of `project-memory/`, and `AGENTS.md`"*, Who it is for). A procedure used
across projects, such as `~/skills/stage2a-e2e-dev116`, is **user** scope and stays outside this design (W3.5).

## Three reasons

1. **The vision already leaves runbooks out, so way (b) keeps a settled vision settled.**
   - [design, vision] *"It holds what the code cannot tell you"*.
   - [design, vision] The vision has two kinds: *"the decisions and facts the code must follow, written before the
     code; what was learned after: lessons, observations and hypotheses."*
   - [EJ] *"ok the vision is confirm"*.
   - [proposed] A script is code. A runbook that "points at a script" holds the very thing the vision says the code
     can tell you. Way (a) reopens a vision EJ has settled in order to add a kind that the next two reasons show is
     not needed. Way (b) changes no vision text, and W2's source tag *"(v; d: What it is for)"* becomes true.

2. **The procedure is the memory. An entry about it is either a duplicate pointer or prose that drifts.**
   - [design, skill] `procedure-to-skill`: *"The procedure is the memory. A prose description of a procedure is a
     summary of the memory, and summaries drift."*
   - [design] The runbook *"says how to run or fix something and points at a script where one exists"* (W2.2).
   - [design] W3.1 forbids *"Nothing that can be read directly from the code"*.
   - [proposed] Where the script exists, the R- entry is only a pointer. The source recommendation already puts that
     pointer in `AGENTS.md` ([design] `RECOMMENDATION.md` l.120: *"AGENTS.md — canonical standing instructions:
     commands, constraints, …"*), and this repo already does it ([design] `CLAUDE.md`: *"Tests:
     `env -u NO_COLOR python3 -m pytest -q`"*). Where no script exists, the entry is prose steps, which is the drift
     the skill warns about.

3. **The source gave runbooks two homes, and the design already sends one of them to `docs/`.**
   - [design] `RECOMMENDATION.md` l.130: *"R-0002-<slug>.md — runbook; prefer a script, the entry only points at
     it"*.
   - [design] `RECOMMENDATION.md` l.137: *"docs/ … the project's existing requirements, architecture and runbooks;
     memory links here, does not copy."*
   - [design] W3.6: *"No copy of the project's existing documents … an entry links to them."*
   - [proposed] Dropping R- removes the duplicate home and leaves `docs/` for a procedure that cannot be scripted.
   - [proposed] It also costs no retirement under K4. I listed `~/dev/*/project-memory` and searched `~/dev` for
     `project-memory/entries/R-*`, and found nothing, so no runbook entry exists. I wrote and ran that check myself.
     It does not establish that nothing exists outside `~/dev`.

## Text changes

### Vision (`source-of-truth-memory-vision-statements.md`)

[proposed] **None.** Its two kinds and *"what the code cannot tell you"* already exclude runbooks.

### Design (`SOURCE_OF_TRUTH.md`)

**Header**: add a revision note after the item-7 block. [proposed]
> **Revised 2026-10-1x, runbooks (item 8):** the runbook kind and the `R-` prefix are removed. How to run or fix
> something is a script in the repo, or a page in `docs/` where it cannot be a script. `AGENTS.md` names it, and what
> was learned running it is a lesson (W3.7). Four-reader round: `runs/20261012-sot-item8-runbooks/`.

**What it is for**: replace the third bullet.
- Old [design]: *"A **runbook** says how to run or fix something; where possible it points at a script."*
- New [proposed]: *"How to run or fix something is not an entry: it is a script in the repo, or a page in `docs/`
  where it cannot be a script, and `AGENTS.md` names it. What was learned while running it is a lesson."*

**When to write** table, third row.
- Old [design]: *"Other lessons, observations and hypotheses; merging duplicates; runbooks."*
- New [proposed]: *"Other lessons, observations and hypotheses; merging duplicates."*

**Where it is put**: change the layout block, two lines.
- Old [design]: `AGENTS.md            standing instructions for every agent (CLAUDE.md only imports it)`
- New [proposed]: `AGENTS.md            standing instructions for every agent, and the scripts it runs (CLAUDE.md only imports it)`
- Old [design]: `entries/           one file per entry: D- decision, F- fact, L- lesson, R- runbook`
- New [proposed]: `entries/           one file per entry: D- decision, F- fact, L- lesson`

**W1.1**
- Old [design]: *"The prefixes are `D-` decision, `F-` fact, `L-` lesson and `R-` runbook, plus `O-` observation and
  `H-` hypothesis (proposed; …)."*
- New [proposed]: *"The prefixes are `D-` decision, `F-` fact and `L-` lesson, plus `O-` observation and `H-`
  hypothesis (proposed; the design leaves these two open). There is no runbook prefix (W3.7)."*
- **Fails if** [design, unchanged]: *"a lint over `entries/` finds a missing field or section, or a reviewer finds two
  claims in one entry."* [proposed] Add: *"…or a file in `entries/` has a prefix outside these."*

**W2.2**
- Old [design]: *"… A **hypothesis** is a guess, labelled as one. A **runbook** says how to run or fix something and
  points at a script where one exists."*
- New [proposed]: *"… A **hypothesis** is a guess, labelled as one."* Delete the runbook sentence.
- **Fails if** [design, unchanged]: *"`kind` holds any other value, or a guess is recorded under any kind but
  hypothesis."* [proposed] This now fails on `kind: runbook`, and no new check is needed.

**W3.7**: new. [proposed]
> **W3.7** No runbooks. How to run or fix something is a script in the repo, which is code (W3.1). Where it cannot
> be a script, it is a page in `docs/`, linked and not copied (W3.6). `AGENTS.md` names each script that an agent
> runs on this project. A lesson learned while running a script is a lesson entry, and its **How to apply:** points
> at the script instead of repeating its steps.

W3's **Fails if** line becomes [proposed]: *"…For W3.1 and W3.3–W3.7, a reviewer finds such content. Those are judged
checks."* Add for W3.7: *"It also fails if an entry's body lists the steps of a procedure, or if a procedure that this
project's agents run exists only in a home-folder skill or script (judged)."*

**W5.2**
- Old [design]: *"Written at the end of a task: other lessons, observations, hypotheses, and runbooks."*
- New [proposed]: *"Written at the end of a task: other lessons, observations and hypotheses."*
- **Fails if** [design, unchanged]: W5's check names no runbook, so it stands as written.

**Other places checked** [proposed]:
- Rd1.1, W2's source tag, `CACHES.md` and the other files in `docs/memory-system/` do not name runbooks. I checked
  with grep, and none of them needs a change.
- *"Anything other agents need must not stay only in one agent's private memory; it belongs here"* (What will not be
  put in) can stay. W3.7's second Fails-if clause now does that job for procedures.

## What could go wrong

[proposed] **Case: a fix ends up in the home folder, where no clone can find it.**

1. An agent repairs a broken deploy by hand.
2. It does what `procedure-to-skill` says, and that skill *"defaults to `~/skills/<name>/`"* [design, skill]. The fix
   is now user-scope and on one machine.
3. A fresh clone does not have it. Neither does Codex on another host, nor any engine that does not scan that folder.
4. Under the current design, the R- entry was what would have pulled the procedure into the repo. Without it, W3.7's
   second clause is the only guard, and it is a judged check that nobody runs automatically.

The outcome is the failure that Rd6 exists to catch: the next session asks EJ how to deploy again.

[proposed] To soften it without a new mechanism, W3.7 names the repo as the procedure's home. The skill's default path
is a different document, and I have not proposed changing it.

## Questions for EJ

1. **Should `AGENTS.md` name the project's scripts, one line each?** That is my default, and it is the only pointer
   this way keeps. The other answer leaves finding them to code search. That would remove the `AGENTS.md` sentence
   from W3.7, from What it is for and from the layout line, and drop the matching part of the Fails-if.
2. **A procedure that cannot be scripted: a page in `docs/` (my default), or a lesson entry?** If it should be a
   lesson, W3.7 and What it is for say "a lesson" instead of `docs/`. A lesson's **How to apply:** would then be
   allowed to hold steps, and W3.7's "an entry's body lists the steps of a procedure" check would be dropped.
