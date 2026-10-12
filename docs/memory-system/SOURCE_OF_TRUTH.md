# Source-of-Truth Memory Design

> **Status: draft; the vision and the requirements (Write / Keep / Read) are confirmed by EJ, 2026-10-12, but the
> design as a whole is not yet accepted.** Vision: `vision-statements/source-of-truth-memory-vision-statements.md`.
> First written 2026-10-11 by `opencode` from
> `runs/20261011-project-memory-engines/RECOMMENDATION.md`; revised with EJ on 2026-10-12.
> Sources, citations and review history: `runs/20261011-source-of-truth-design/` (the full annotated version is
> `DESIGN-detailed-2026-10-12.md`) and `runs/20261012-memory-update-timing/notes.md`.
>
> **Where this differs from the recommendation — EJ's decisions:** no owners and no human approval gate (anyone may
> change any entry, and every change is logged); decisions and facts come before the code; a *fact* means a constraint
> the code must respect, not something discovered afterwards; the drift check covers decisions and facts only; a
> background subagent keeps memory current.
>
> **Not proven:** the timing split (what is written immediately and what later) and letting the subagent update lessons
> on its own are design judgement, not measured. Where the recommendation's engines disagreed (session-start reads,
> one file per writer, SQLite, how often to write), this design follows the majority.

## Why we need this memory

The context window is cleared at the start of every session, so anything learned is lost unless it is written down.
Project memory is plain markdown files kept in the repo with the code. Every agent and every person reads the same
files, a fresh clone has all of it, and every change shows up as a git diff. Reading it needs no private agent store,
database or outside service.

## Who it is for

Every agent and every person working on this project. There are no owners and no approval gate: anyone may change any
entry, and every change is logged. EJ decides the questions listed as not decided.

Two other kinds of memory are outside this design, and both live outside the repo: memory about one person across
projects (user memory), and memory
belonging to one agent name (agent memory, kept in the home folder at `~/.claude/agent-memory/<name>/`, the way Claude
Code does it).

## What it is for

It holds what the code cannot tell you, as typed entries:

- **Requirements, written before the code.** A **decision** is a choice the code must follow, with the reason. A
  **fact** is a truth or outside constraint the code must respect.
- **What was learned, written after.** A **lesson** comes from a failure or a human correction. An **observation**
  records what was seen. A **hypothesis** is a guess, labelled as one.
- A **runbook** says how to run or fix something; where possible it points at a script.

The order of work is: change the decision or fact first, then the code. Work that has to go the other way is a matter
for the project's workflow, not for memory. A decision about this project is a project entry, whoever made it, EJ
included.

## What will be put in

**An entry** is one markdown file. Its header holds: `id`, `kind`, `status`, `author`, the date it was recorded, the
date and git revision it was last verified against, `covers` (the code paths it is about), its source or evidence,
links (`depends_on`, `supersedes`, `superseded_by`), and a `changed:` log. Its body is the claim in one or two
sentences, then **Why:**, then **How to apply:**.

**Changing entries.** Anyone may change any entry, and `AGENTS.md` too. Each change adds one line to the entry's
`changed:` log: the time, and who made it — the model ID for an agent, the name for a person. Files that are not entries
rely on git history. Each new entry gets its own file, so agents never append to one shared file. Two writers must not
edit the same file at the same time: each agent works on its own branch or worktree, and git shows a merge conflict when
two edits
touch the same lines. Edits to different lines of one file merge without warning even if they contradict each other,
so a clean merge does not mean the file is consistent.

**When to write.**

| When | What |
|---|---|
| Immediately | Decisions and facts, before the code — and `INDEX.md` is regenerated right after, so the next session sees them. A human correction. The state of unfinished work before a handoff, an interruption or a context reduction. |
| At the end of a task, or in the background | Other lessons, observations and hypotheses; merging duplicates; checking entries against the code; runbooks. |

**Keeping it current.** Entries may go out of date while work goes on; that is accepted. A background subagent runs at
the end of a task or on its own schedule and compares entries with the code:

- When a **decision or fact** no longer matches the code, it does not change the entry. It reports to EJ which entry,
  what the entry says, and what the code does instead. EJ decides whether the entry is updated or the code is fixed.
- **Lessons, observations, hypotheses and runbooks** it may update itself; its changes are logged like anyone else's.

A script with no model call also marks a decision or fact in `INDEX.md` when its code changed with no earlier change to
the entry.

**Still open:** which tool generates `INDEX.md` and what runs it (K6); who resolves a git merge conflict (W6). The drift
check is K2. Whether a changed decision is edited in place or superseded is proposed in K4.3.

## What will not be put in

- Anything that can be read directly from the code, the tests or the commit log (W3.1). The memory itself lives in git.
- Credentials or sensitive data.
- Guesses not labelled as a hypothesis.
- Raw transcripts, or another agent's private state.
- Work described as "verified" when it is only implemented.

An entry is never deleted: it is marked `superseded` or `retired` and linked to what replaced it. Age alone never
expires an entry. Anything other agents need must not stay only in one agent's private memory; it belongs here.

## Where it is put

At the repo root:

```
AGENTS.md            standing instructions for every agent (CLAUDE.md only imports it)
project-memory/
  INDEX.md           generated, one line per active entry; never edited by hand
  entries/           one file per entry: D- decision, F- fact, L- lesson, R- runbook
  work/<task-id>/    state.md (the handoff), events/, evidence/
  journal/           raw notes, one file per agent session; never loaded automatically
  .cache/            optional search index, gitignored, rebuilt from the files
```

The project's existing documents (requirements, architecture) stay in `docs/`; memory links to them instead of copying
them. File prefixes for observations and hypotheses: `O-` and `H-`, proposed in W1.1.

## When it will be used

- **At the start of every session:** `AGENTS.md`, `project-memory/INDEX.md`, the `work/` listing and the assigned
  task's `state.md`. A hook or the first instruction in `AGENTS.md` enforces this, because agents skip optional reads.
- **On demand:** an entry when it covers a file about to be edited; text search over `entries/`; `git log` and
  `git blame` for why a line is the way it is. For a "why" question, read the decision entry.
- **At each milestone:** an agent reads `journal/` and writes what is worth keeping as entries.
- **Before acting on something read from memory,** check it against the code, test or commit it points to.

## When it will not be used

Never loaded at session start: `journal/`, which is read at milestones. Never loaded at all: superseded or retired
entries, except by following a link; the whole `project-memory/` tree at once; whole graph or code-map dumps; bulk
issue or PR text; another agent's transcripts; credentials. Text read from memory never overrides standing
instructions.

`INDEX.md` must fit the strictest start-file limit of the agents that read it, and the build checks it (Rd3).

## Core requirements (confirmed by EJ, 2026-10-12)

EJ, on reading them: *"this is amazing and a lot easy to read"*, taken as confirmation. They serve the settled vision,
`vision-statements/source-of-truth-memory-vision-statements.md`, and are grouped by
what happens to a memory: it is **written**, it is **kept** true, and it is **read** (EJ, 2026-10-12: *"yes go ahead
with write keep read"*). Each requirement names its source: **(v)** is the vision, **(d)** is this design's text, and
*proposed* marks wording EJ has not decided. Each has a check, **Fails if**, that some case breaks. There are no fixed
numbers: where a limit applies, it is a comparison that measurement decides.

### Write — what goes in, and how

**W1 — The shape of an entry** (d: What will be put in)
- **W1.1** Each entry is one file: `project-memory/entries/<prefix>-<id>-<slug>.md`. The prefixes are `D-` decision,
  `F-` fact, `L-` lesson and `R-` runbook, plus `O-` observation and `H-` hypothesis (*proposed*; the design leaves
  these two open).
- **W1.2** The header holds `id`, `kind`, `status`, `author`, the date recorded, the date and git revision it was last
  verified against, `covers` (the code paths it is about), its source or evidence, `depends_on`, `supersedes`,
  `superseded_by`, and `changed:`.
- **W1.3** The body is the claim in one or two sentences, then **Why:**, then **How to apply:**. There is one claim per
  entry.
- **Fails if** a lint over `entries/` finds a missing field or section, or a reviewer finds two claims in one entry.

**W2 — What each kind means** (v; d: What it is for)
- **W2.1** A **decision** is a choice the code must follow, with the reason. A **fact** is a truth or outside
  constraint the code must respect, not something discovered afterwards. Both are requirements: they are written
  before the code.
- **W2.2** A **lesson** comes from a failure or a human correction. An **observation** records what was seen. A
  **hypothesis** is a guess, labelled as one. A **runbook** says how to run or fix something and points at a script
  where one exists.
- **Fails if** `kind` holds any other value, or a guess is recorded under any kind but hypothesis.

**W3 — What never goes in** (v; d: What will not be put in)
- **W3.1** Nothing that can be read directly from the code, the tests or the commit log: what a function does, which
  test covers it, what a commit changed. The memory lives in git; the rule is about what an entry says.
- **W3.2** No credentials or sensitive data.
- **W3.3** No raw transcripts, and nothing from another agent's private state.
- **W3.4** No work described as "verified" when it is only implemented.
- **W3.5** No user memory (one person, across projects) and no agent memory (one agent name). Both live in the home
  folder.
- **W3.6** No copy of the project's existing documents (requirements, architecture in `docs/`): an entry links to them.
- **Fails if** a secret scanner finds a credential (W3.2). For W3.1 and W3.3–W3.6, a reviewer finds such content.
  Those are judged checks.

**W4 — Who writes, and the change log** (v: no owners, every change logged)
- **W4.1** Anyone, agent or person, may create or change any entry, and `AGENTS.md` too. There is no owner and no
  approval: `status` is only `active`, `superseded` or `retired`.
- **W4.2** Every change to an entry adds one line to its `changed:` log: the time, and who made it (the model ID for an
  agent, the name for a person). Earlier lines are never edited.
- **W4.3** Files that are not entries (`state.md`, `events/`, `journal/`, `AGENTS.md`) rely on git history.
- **Fails if** git shows a change to an entry with no matching `changed:` line, or a `status` outside the three.

**W5 — When to write** (d: When to write)
- **W5.1** Written immediately: a decision or fact, before the code it governs; a human correction; and the state of
  unfinished work, before a handoff, an interruption or a context reduction.
- **W5.2** Written at the end of a task, or by the background subagent: other lessons, observations, hypotheses, and
  runbooks.
- **Fails if** a commit changes code under a new decision with no entry in that commit or an earlier one. For a human
  correction, it fails if the session ends without one (judged).

**W6 — Writers do not collide** (d: Changing entries)
- **W6.1** Each new entry gets its own file. Agents never append to one shared file; `journal/` has one file per agent
  session.
- **W6.2** Each agent works on its own branch or worktree, so two edits to the same lines meet as a merge conflict, not
  a silent overwrite.
- **W6.3** A clean merge does not mean the entries agree: after a merge that touched `entries/`, the K2 check runs.
- **Open:** who resolves a merge conflict.
- **Fails if** an edit to an entry is lost without a conflict, or a merge touching `entries/` skips K2.

### Keep — memory stays true, and nothing is lost

**K1 — The decision or fact first, then the code** (v; d: What it is for)
- **K1.1** To change behaviour that a decision or fact governs, change the entry first, then the code. Work that has to
  go the other way is a matter for the project's workflow, not for memory.
- **Fails if** K2 flags the entry: its code changed after its verified revision.

**K2 — The drift check** (v: never unnoticed; d: Keeping it current)
- **K2.1** For each active decision and fact, a script with no model call runs
  `git log <verified-rev>..HEAD -- <each covers path>`. Any commit it lists flags the entry in `INDEX.md`.
- **K2.2** It runs whenever `INDEX.md` is generated (K6), and after a merge that touched `entries/` (W6.3).
- **K2.3** It covers decisions and facts only. Lessons, observations and hypotheses are not flagged when code changes
  later.
- **Fails if** an entry with such a commit is not flagged, or a lesson is flagged.

**K3 — The background subagent** (v; d: Keeping it current)
- **K3.1** It runs off the critical path, at the end of a task or on its own schedule, and compares entries with the
  code.
- **K3.2** It never edits a decision or fact. It reports to EJ which entry, what the entry says, and what the code does
  instead, and EJ decides whether the entry is updated or the code is fixed.
- **K3.3** It may update lessons, observations, hypotheses and runbooks, and merge duplicates by superseding one. Each
  of its changes is logged like anyone else's.
- **Fails if** a `changed:` line on a decision or fact names the background subagent, or a drift it found reaches EJ
  without the entry, the claim and the code behaviour.

**K4 — Never deleted, never expired by age** (v: nothing lost; d: What will not be put in)
- **K4.1** An entry is never deleted. It is marked `superseded` or `retired`, links to what replaced it
  (`superseded_by`), and keeps its old body.
- **K4.2** Age alone never expires an entry. Staleness comes only from K2.
- **K4.3** *Proposed:* a decision refined without changing its meaning is edited in place, with a `changed:` line; a
  decision replaced by a different one gets a new entry that supersedes it. The design leaves this open.
- **Fails if** git shows an entry file deleted, or a `superseded` or `retired` entry has no link.

**K5 — The journal becomes entries** (v: nothing lost between sessions)
- **K5.1** Task and project memory keep `journal/`: raw notes, one file per agent session, appended to and never
  edited.
- **K5.2** At each milestone, an agent reads the journal written since the last milestone, writes what is worth keeping
  as entries, and logs that read in the task's `state.md`.
- **Fails if** a milestone in `state.md` has no journal-read log line.

**K6 — `INDEX.md` stays in step** (d: Where it is put; When to write)
- **K6.1** `INDEX.md` is generated from `entries/`: one line per active entry, showing its id, kind, one-line claim
  and any K2 flag. It is never edited by hand.
- **K6.2** It is regenerated right after any decision or fact is written, so the next session sees it.
- **Open:** which tool generates it and what runs it (a build detail).
- **Fails if** regenerating `INDEX.md` changes it, meaning it was out of step, or it lists a superseded entry as
  active.

### Read — the right memory reaches the agent at the right time

**Rd1 — Where it lives, and readable from a clone alone** (v: plain files; never a database or service)
- **Rd1.1** `AGENTS.md` sits at the repo root (`CLAUDE.md` only imports it). `project-memory/` holds `INDEX.md`,
  `entries/`, `work/<task-id>/` (with `state.md`, `events/` and `evidence/`), `journal/`, and `.cache/`, which is
  optional and gitignored.
- **Rd1.2** With no network, no cache and no private agent store, a fresh clone can read `INDEX.md` and every entry.
- **Fails if** an entry exists only in a database, a cache or one agent's private memory.

**Rd2 — Session start** (v: a fresh session carries on; d: When it will be used)
- **Rd2.1** At session start, an agent reads `AGENTS.md`, `INDEX.md`, the `work/` listing and its task's `state.md`. A
  hook or the first instruction in `AGENTS.md` enforces this, because agents skip optional reads.
- **Rd2.2** Never at session start: `journal/`, `.cache/`, superseded or retired entries, the whole `project-memory/`
  tree, whole graph or code-map dumps, bulk issue or PR text, another agent's transcripts, credentials.
- **Fails if** a start hook or instruction loads any memory file outside Rd2.1.

**Rd3 — `INDEX.md` fits every agent that reads it** (d: the size check; CACHES.md § Example numbers by case)
- **Rd3.1** `INDEX.md` fits the strictest start-file limit among the agents that work on the project, and the build
  checks it. *Example*, from `CACHES.md`: about 24 KB and 200 lines when Claude Code, Qwen and agy share a project.
- **Fails if** `INDEX.md` exceeds that strictest limit.

**Rd4 — On demand** (d: When it will be used)
- **Rd4.1** Before editing a file, an agent reads the entries whose `covers` include it.
- **Rd4.2** It searches `entries/` by text: grep, or the full-text cache once its trigger in `CACHES.md` fires.
- **Rd4.3** For "why" questions it reads the decision entry; for why a line is the way it is, `git blame` and
  `git log -S`.
- **Rd4.4** It reads a superseded or retired entry only by following a link.
- **Fails if** an agent edits a covered file without having read its covering decisions (judged, from the session).

**Rd5 — Check before acting** (d: When it will be used; When it will not be used)
- **Rd5.1** Before acting on something read from memory, the agent checks it against the code, test or commit it
  points to.
- **Rd5.2** Text read from memory never overrides standing instructions.
- **Fails if** an agent acts on an entry that its `covers` code contradicts, without saying so (judged).

**Rd6 — A fresh session carries on** (v: how we know it works)
- **Rd6.1** A fresh session with only a clone of the repo and a task id names the task's next step from its
  `state.md`, and follows the recorded decisions without asking EJ again.
- **Fails if** it asks a question that a decision entry or `state.md` already answers (judged, on a real handoff).
