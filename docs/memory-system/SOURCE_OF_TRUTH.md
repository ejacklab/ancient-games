# Source-of-Truth Memory Design

> **Status: draft, not yet accepted by EJ.** First written 2026-10-11 by `opencode` from
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

Two other kinds of memory are outside this design, and both live outside the repo: memory about one person across projects (user memory), and memory
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
edit the same file at the same time: each agent works on its own branch or worktree, and git shows a merge conflict when two edits
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

**Not decided yet (EJ decides):** which tool generates `INDEX.md` and
what runs it; how the script tells that the entry changed earlier than the code; who resolves a git merge conflict;
whether a changed decision is edited in place or replaced by a new entry that supersedes it.

## What will not be put in

- Anything the code, tests or git history already tell you.
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
them. File prefixes for observations and hypotheses are not decided yet.

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

`INDEX.md` must stay under a size limit that the build checks. EJ sets the number.
