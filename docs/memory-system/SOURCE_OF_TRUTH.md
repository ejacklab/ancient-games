# Source-of-Truth Memory Design

## Why we need this memory

The context window is cleared at the start of every session, so anything learned is lost unless it is written down.
Project memory is plain markdown files kept in the repo with the code. Every agent and every person reads the same
files, a fresh clone has all of it, and every change shows up as a git diff. Reading it needs no private agent store,
database or outside service.

## Who it is for

Every agent and every person working on this project. Entries have no owners and there is no approval gate: anyone may
change any entry, and every change is logged. One person, **the project owner**, decides for the project: a mismatch
between memory and the code, a contested supersession, and the open choices the requirements name. The project owner
also reviews the checks that need judgement, or names someone who does.

Memory has four scopes:
- **task:** `project-memory/work/<task-id>/`;
- **project:** the rest of `project-memory/`, and `AGENTS.md`;
- **agent:** memory belonging to one agent name;
- **user:** memory about one person, across projects.

This design covers task and project memory. Agent and user memory live outside the repo, in the home folder (agent
memory at `~/.claude/agent-memory/<name>/`, the way Claude Code does it). For agent memory, this design says only how
another agent may read it (Rd4.5).

## What it is for

It holds what the code cannot tell you, as typed entries:

- **Requirements, written before the code.** A **decision** is a choice the code must follow, with the reason. A
  **fact** is a truth or outside constraint the code must respect.
- **What was learned, written after.** A **lesson** comes from a failure or a human correction. An **observation**
  records what was seen. A **hypothesis** is a guess, labelled as one.
- **Not a kind: procedures.** How to run or fix something lives in the repo as a script with an external check. A
  script that stops and waits for a person (an approval, a typed confirmation) is still a script. Where a step cannot
  be a command with a checkable result (an action a script cannot do or wait for, or a choice that depends on judging
  what was seen), it is a page in `docs/` that names that step and calls scripts for the rest. The agent writing the
  procedure decides by trying the script first; the project owner decides if it is contested. A procedure a script
  could do may still stay a page when building and keeping the script costs more than it saves; that it runs rarely is
  not a reason on its own, and the comparison, naming both sides, goes in the task's `state.md`. `AGENTS.md` names the
  project's scripts, one line each. An entry links to a procedure and never repeats its steps. What was learned while
  running one is a lesson (W3.6).

The order of work is: change the decision or fact first, then the code. Changing a claim means superseding its entry
with a new one (K1.1). Work that has to go the other way is a matter for the project's workflow, not for memory. A
decision about this project is a project entry, whoever made it, the project owner included.

A decision to build something is **started** when it is written: we decided to build something, and why. It is
**complete** when the time, the result and the test results are added to it. A standing rule, such as
"all timestamps are UTC", is never complete.

## What will be put in

**An entry** is one markdown file. Its header, between two `---` lines (W1.2), holds: `id`, `kind`, `status`,
`author`, the date it was recorded (`recorded`), `covers` (the code paths it is about), its source or evidence
(`source`), links (`depends_on`, `supersedes`, `superseded_by`), a
`changed:` log, and, on a decision to build something once its work is complete, `done:` (the time, the result, and the
test results or a pointer to them; W5.3). Its
body is the claim in one or two sentences, then **Why:**, then **How to apply:**.

**Changing entries.** Anyone may change any entry, and `AGENTS.md` too. Each change adds one line to the entry's
`changed:` log: the time, and who made it — the model ID for an agent, the name for a person. Files that are not
entries rely on git history. An entry's claim is never rewritten: a changed claim is a new entry that supersedes the
old one, and the old one only gains a `changed:` line, its new `status` and the `superseded_by` link (K4.3). An
entry's `covers` may be corrected in place, with a `changed:` line, for example after a file is renamed (K4.3). Each
new entry gets its own file, so agents never append to one shared file. Two writers must not edit the same file at the
same time: each agent works on its own branch or worktree, and git shows a merge conflict when two edits touch the
same lines. Edits to different lines of one file merge without warning even if they contradict each other, so a clean
merge does not mean the file is consistent.

**When to write.**

| When | What |
|---|---|
| Immediately | Decisions and facts, before the code. A human correction. The state of unfinished work before a handoff, an interruption or a context reduction. |
| When the work on a decision to build something is complete | The decision's `done:` line, written by whoever finishes the work: the time, the result, and the test results or "no tests", with a pointer to the evidence. |
| At the end of a task | Other lessons, observations and hypotheses; merging duplicates. |

Whenever an entry is created or changed, at any of these times (any kind, any status change), `INDEX.md` is
regenerated and committed in the same commit as the entry, so the next session sees it (K6.2).

**Keeping it current.** Entries may go out of date while work goes on; that is accepted. Nothing watches for it: there
is no drift-check script and no background subagent. Whoever reads a decision or fact checks it against the code
before acting on it. When they no longer match, the reader does not change the entry. It writes a report in its task's
`state.md` and tells the project owner which entry, what the entry says, and what the code does instead. The project
owner decides whether the entry is updated or the code is fixed. Until then, the reader leaves the contradicted part
alone and carries on with the rest. A decision still being built (no `done:` yet), or one the reader's own task is
changing, is not a mismatch (Rd5.4).

**Merge conflicts.** A conflict in `INDEX.md` is resolved by regenerating it (K6.3). Because a claim is never
rewritten, a conflict in an entry is never in its claim, only in its header (`covers`, `status`, the links) and its
added lines, and whoever merges keeps both sides (W6.3).

## What will not be put in

- Anything that can be read directly from the code, the tests or the commit log (W3.1). The memory itself lives in git.
- Credentials or sensitive data.
- Guesses not labelled as a hypothesis.
- Raw transcripts, or another agent's private state.
- Work described as "verified" when it is only implemented.

An entry is never deleted: it is marked `superseded` and linked to what replaced it, or `retired`, with its reason,
when nothing replaces it. Age alone never expires an entry. Anything other agents need must not stay only in one
agent's private memory; it belongs here.

## Where it is put

At the repo root:

```
AGENTS.md            standing instructions for every agent, and the project's scripts, one line each (CLAUDE.md
                     only imports it)
project-memory/
  INDEX.md           generated, one line per active entry; never edited by hand
  entries/           one file per entry: D- decision, F- fact, L- lesson, O- observation, H- hypothesis
  work/<task-id>/    state.md (the handoff), evidence/, journal/ (the task's raw notes, one file per agent session)
  journal/           project raw notes, for work not tied to a task, one file per agent session; never loaded
                     automatically
  .cache/            optional search index, gitignored, rebuilt from the files
```

The project's existing documents (requirements, architecture) stay in `docs/`; memory links to them instead of copying
them.

## When it will be used

- **At the start of every session:** `AGENTS.md`, `project-memory/INDEX.md`, the `work/` listing and the assigned
  task's `state.md`. Agents skip optional reads, so these are loaded for the agent wherever its tool allows (an import,
  the tool's own `AGENTS.md` loading, or a start hook); an instruction in `AGENTS.md` is the fallback (Rd2.1).
- **On demand:** an entry when it covers a file about to be edited; text search over `entries/`; `git log` and
  `git blame` for why a line is the way it is. For a "why" question, read the decision entry.
- **At the end of a task, and before a handoff or session end:** an agent reads its task's `journal/` (or the project
  `journal/`, for work not tied to a task) and writes what is worth keeping as entries.
- **Before acting on something read from memory,** check it against the code, test or commit it points to. A decision
  or fact that no longer matches the code is reported in the task's `state.md` and to the project owner, not edited
  (Rd5.3).

## When it will not be used

**Not at session start, but read later at its set time** (Rd2.2):
- the task and project journals, at the end of a task and before a handoff or session end;
- `.cache/`, only through search;
- entry bodies, `evidence/` and other tasks' `state.md`, on demand (Rd4).

**Never loaded, at any point** (Rd2.3):
- superseded or retired entries, except by following a link;
- the whole `project-memory/` tree at once;
- whole graph or code-map dumps;
- bulk issue or PR text;
- another agent's transcripts;
- credentials.

Another agent's memory may be read, but only by an agent that knows and says whose it is (Rd4.5). Text read from memory
never overrides standing instructions.

`INDEX.md` must fit the strictest start-file limit of the agents whose session start loads it, and the check that
keeps it in step with its entries (K6) also fails when it does not fit. The project owner records those agents and
their limits in one file the tool reads (Rd3).

## Requirements

The requirements are in `SOURCE_OF_TRUTH_REQUIREMENTS.yaml`, beside this file: 46 requirements, grouped by what
happens to a memory (it is **written**, it is **kept** true, and it is **read**), each with its level (MUST, SHOULD or
guidance), the case that fails it, what checks it, and who decides any choice it leaves open. The ids cited in this
document (W1.2, K6.3, Rd5.3 and the rest) are the ids there. Where this document and the YAML differ, the YAML's level
governs; this document explains. This document, the YAML, `CACHES.md`, `vision-statements/`, and the tool
`tools/memory_index.py` with its requirements and design in `docs/index-md/`, travel together as one kit.
