# Summary — four readers on item 7, by scope

COO (Claude `claude-opus-5-5`), 2026-10-12, from `reviews/{claude,codex,opencode,agy}.md`, each written blind.
Nothing here is applied yet.

## Where all four agree

| Scope | Lives | Read at session start | Read on demand | Never | Journal |
|---|---|---|---|---|---|
| **Task** | `work/<task-id>/`: `state.md`, `evidence/` | own task's `state.md`, plus the `work/` listing | `evidence/` when a `state.md` or `done:` points to it; another task's `state.md` when taking it over or asked about it | other tasks' folders at start | **yes** (EJ) |
| **Project** | `AGENTS.md`, `project-memory/` | `AGENTS.md`, `INDEX.md` | entries (Rd4); `journal/` at the end of a task and before a handoff; `questions/` by the cache comparison; `.cache/` only through search | the whole tree at once | **yes** (EJ) |
| **Agent** | home folder | not this design's business | only by that agent | never by another agent | **no** (all four) |
| **User** | home folder | not this design's business | only by that person's agents | never by another person's agents | **no** (all four) |

Plus, in no scope at all: graph or code-map dumps, bulk issue or PR text, credentials. These are never loaded.

**The rewrite all four converge on:**
- **Rd2.2** — not at session start, read later at its set time: `journal/`, `questions/`, `.cache/`, entry bodies,
  `evidence/`, other tasks' `state.md`.
- **Rd2.3 (new)** — never loaded, at any point in the session:
  - the whole `project-memory/` tree at once;
  - graph or code-map dumps;
  - bulk issue or PR text;
  - another agent's transcripts or private memory;
  - another person's user memory;
  - credentials;
  - superseded or retired entries, except by following a link (Rd4.4).

  It has its own judged check over the whole session.
- **The main text** gets the same two lists. Elsewhere: name the four scopes once in "Who it is for"; label each folder
  with its scope in "Where it is put"; K5.1 says agent and user memory keep no journal.

## Where they differ: the journal's home

All four noticed the same thing: EJ said *"task and project memory need a journal"*, but the layout has one `journal/`.
- **claude** keeps one `journal/`, with each file name starting with its task id. The task's journal is then its own
  files, and the project's is the whole folder. Without this, two tasks running at once would read each other's notes.
- **codex, opencode, agy** keep one shared `journal/` and add nothing.
- **Per-task folder** `work/<task-id>/journal/` was offered as the alternative by claude and agy.

## The questions that change the table

1. **Journal home** (all four): one shared `journal/` with files named by task id, or a `journal/` in each task
   folder? And whose journal is a session with no task, such as a discussion with EJ?
2. **Agent and user memory at start** (codex, opencode): should this design say anything about what a tool loads for
   its own agent or for EJ? opencode proposes no: the never-lists cover only reading *across* scopes, such as one agent
   reading another's memory.
3. **Claude Code's per-project memory** (claude): `~/.claude/projects/<project>/memory/` holds notes about *this
   project*, but only Claude Code reads it. Is it user memory, agent memory, or project memory kept in the wrong place?
   The design says *"anything other agents need must not stay only in one agent's private memory"*.
