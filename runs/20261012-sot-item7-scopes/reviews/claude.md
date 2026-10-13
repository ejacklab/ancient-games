# Item 7 by scope (claude)

Read: `docs/memory-system/SOURCE_OF_TRUTH.md` (whole), its vision statement, and `CACHES.md` Rd4 and B4.1 (for
`questions/` and `.cache/`). I did not read the other readers' reports. Labels: **EJ's** (his words), **design**
(already in the document, with its place), **proposed** (mine).

**The fix in one sentence** (*proposed*): Rd2.2 should list only what is *not loaded at start but is read later*, and a
new Rd2.3 should list what is *never loaded at any time*, sorted by scope. Then the main text and the requirements say
the same thing at the same strength.

## The table

Four scopes, plus one row for the things that belong to no memory scope. In the main text's "never loaded at all" list,
three items (graph or code-map dumps, bulk issue or PR text, credentials) are not memory of any scope. They need their
own row so that they don't end up attached to a scope by accident.

| | **Task** | **Project** | **Agent** | **User** |
|---|---|---|---|---|
| **Where it lives** | `project-memory/work/<task-id>/`: `state.md` and `evidence/` (*design*, Where it is put) | `AGENTS.md`, `project-memory/INDEX.md`, `entries/`, `journal/`, `questions/`, `.cache/` (*design*, Rd1.1) | Home folder, `~/.claude/agent-memory/<name>/` (*design*, Who it is for). Outside this design. | Home folder, one person across projects (*design*, Who it is for). Outside this design. |
| **Who writes it** | The agent working the task writes `state.md` before a handoff, an interruption or a context reduction (*design*, W5.1). It also writes `evidence/` (*proposed*: the design names the folder but not its writer). | Anyone, agent or person, writes entries and `AGENTS.md` (*design*, W4.1). `INDEX.md` is generated, never written by hand (*design*, K6.1). Each session writes its own `journal/` file (*design*, W6.1). The agent that asked a question writes the `questions/` record (*CACHES Rd4.2*, proposed there). `.cache/` is written only by its rebuild (*design*). | The agent with that name, only (*design*: "belonging to one agent name") | That person and the agents working for them (*proposed*: the design says only "one person") |
| **Who reads it** | The agent assigned the task, and anyone who takes it over (*design*, Rd2.1, Rd6.1). Any agent may read another task's `state.md` on demand, because there are no owners (*proposed*, from W4.1). | Every agent and person on the project (*design*, Who it is for) | That agent name only (*proposed*, from *design* W3.3 "another agent's private state" and the vision's "a private agent store is invisible to the other agents") | Agents working for that person (*proposed*) |
| **Who does not read it** | No agent reads another task's `state.md` at session start; it reads only its own (*design*, Rd2.1) | Task agents do not read `questions/`; it is read only by the cache comparison (*proposed*, from *CACHES* Rd4.3: "read by the comparison"). Nobody reads `.cache/` as text; it is used only through search (*proposed*, from Rd4.2). | Every other agent (*proposed*; this is what the design needs from agent memory) | Other people's agents; and the project memory never copies it (*design*, W3.5) |
| **Loaded at session start** | Yes: the assigned task's `state.md` and the `work/` listing (*design*, Rd2.1). No: `evidence/` and other tasks' folders (*proposed*). | Yes: `AGENTS.md` and `INDEX.md` (*design*, Rd2.1). No: `entries/` bodies, `journal/`, `questions/`, `.cache/` (*design*, Rd2.2). | Decided by that agent's own tool; outside this design (*proposed*) | Decided by the person's tool; outside this design (*proposed*) |
| **Read on demand: when** | `evidence/` when `state.md` or a `done:` line points to it (*proposed*, from W5.3). Another task's `state.md` when your task depends on it or you take it over (*proposed*). | An entry when its `covers` includes a file about to be edited (*design*, Rd4.1). Text search (Rd4.2). The decision entry for a "why" question (Rd4.3). A superseded or retired entry only by following a link (Rd4.4). `journal/` at the end of a task and before a handoff or session end (*EJ's*, K5.2). `questions/` when the cache comparison runs (*CACHES* B1, K3). `.cache/` through search, once its trigger has fired (*design*, Rd4.2). | By that agent, when its tool decides (*outside*) | By that person's agents (*outside*) |
| **Never loaded** | Nothing beyond the rows "Never, any scope" and Rd2.3 (*proposed*) | The whole `project-memory/` tree at once (*design*). Superseded or retired entries, except by following a link (*design*). | Never by another agent: not its transcripts, and not its private memory (*design*, "another agent's transcripts"; *proposed*: widened to "private memory" to match W3.3) | Never by another person's agents (*proposed*) |
| **Keeps a journal** | **Yes** (*EJ's*: *"task and project memory need a journal"*). The task's raw notes become entries when the task ends (K5.2); `state.md` holds only the handoff. | **Yes** (*EJ's*). Nothing is lost between sessions: notes stay until an agent turns them into entries (K5). | **No**, as far as this design goes (*EJ's*: *"not all need the journal"*; only task and project were named). Anything other agents need goes into a project entry, not a journal (*design*, What will not be put in). | **No**, as far as this design goes (*EJ's*, same basis) |

**Never, any scope** (*design*, the main text's list; *proposed*: kept out of the scope rows): whole graph or code-map
dumps; bulk issue or PR text; credentials.

**How task and project share one journal** (*proposed*, the smallest version that works). The design has a single
`project-memory/journal/` with one file per agent session. A session works on one task (Rd2.1: "its task's
`state.md`"). So I propose that **a journal file's name starts with its task id**. Then the task's journal is the set of
files with its id, and the project's journal is the whole folder. This adds no folder and no field, only a naming rule.
Without it, K5.2 ("the journal written since the last read") has two problems:
- **Two tasks running at once read each other's files**, which can turn one note into two entries.
- **The task-end read covers a whole folder**, which comes close to the "whole `project-memory/` tree" that must never be
  loaded.

Question 1 gives EJ the other option.

## Rewrite of item 7

### Replacement for "When it will not be used" (main text)

> **Never loaded at session start:**
> - `journal/`, read at the end of a task and before a handoff or session end;
> - `questions/`, read only by the cache comparison;
> - `.cache/`, used only through search;
> - another task's `work/` folder and the agent's own `evidence/`, read when a link or a takeover leads to them.
>
> **Never loaded at all, at any point in a session:**
> - superseded or retired entries, except by following a link;
> - the whole `project-memory/` tree at once;
> - whole graph or code-map dumps;
> - bulk issue or PR text;
> - another agent's transcripts or private memory;
> - credentials.
>
> Agent memory is read only by the agent it belongs to, and user memory only by that person's agents. Text read from
> memory never overrides standing instructions.
>
> `INDEX.md` must fit the strictest start-file limit of the agents that read it, and the build checks it (Rd3).

Labels:
- The two lists: *design*. The second list keeps the main text's items and the words "never loaded at all".
- "At any point in a session": *proposed*. It closes the reading that the brief points out.
- `questions/`, `.cache/`, `work/` and `evidence/` in the first list: *proposed*. `questions/` and `.cache/` are already
  in Rd2.2; the rest is new.
- "Or private memory": *proposed*, from W3.3.
- The agent and user sentence: *proposed*.

### Replacement for Rd2.2, and a new Rd2.3

> **Rd2.2** Not at session start, but read later at the time this design sets:
> - `journal/`, at the end of a task and before a handoff or session end (K5.2);
> - `questions/`, by the cache comparison (`CACHES.md` B1, K3);
> - `.cache/`, through search (Rd4.2);
> - another task's `work/` folder, and the agent's own `evidence/`, when a link or a takeover leads to them.
>
> **Rd2.3** Never loaded, at session start or at any later point:
> - superseded or retired entries, except by following a link (Rd4.4);
> - the whole `project-memory/` tree at once;
> - whole graph or code-map dumps;
> - bulk issue or PR text;
> - another agent's transcripts or private memory (agent memory is read only by the agent it belongs to);
> - another person's user memory;
> - credentials.
>
> **Fails if** a start hook or instruction loads any memory file outside Rd2.1. It also fails if a session starts work
> on a task before the four in Rd2.1 have reached it (judged, from the start of the session). It also fails if a hook,
> an instruction or a session's record shows any item of Rd2.3 loaded at any point (judged, from the session; for a
> superseded or retired entry, if no link led to it).

Labels:
- The first two "Fails if" sentences: *design*, unchanged.
- The third: *proposed*.
- Rd2.2: *design* for the first three items; the times are taken from K5.2, CACHES and Rd4.2. The fourth item is
  *proposed*.
- Rd2.3: *design* for the main text's items; *proposed* for "or private memory" and "another person's user memory".

**My reading, not EJ's: what "credentials" covers.** In this section, "never loaded" means *read into an agent as
memory*. It does not stop a tool from using a credential it is configured with (for example, `gh` authenticating). I
left the word unchanged; if EJ means something stricter, the word stays and only this note changes.

## What changes elsewhere

- **Status header** (*proposed*): add a line saying "Revised 2026-10-12, not yet accepted: item 7, the loading rules by
  scope (Rd2.2, Rd2.3)".
- **Who it is for** (*proposed*): add one sentence: "Agent memory is read only by the agent it belongs to, and user
  memory only by that person's agents; this design needs nothing else from them."
- **Where it is put** (*proposed*, only if Question 1 keeps one folder): change the `journal/` line to "raw notes, one
  file per agent session, named with its task id; never loaded automatically".
- **When it will be used** (*proposed*): under "On demand", add "`questions/` by the cache comparison only; `.cache/`
  only through search; another task's `state.md` or `evidence/` when a link or a takeover leads to it".
- **When it will not be used**: replaced, as above.
- **W6.1** (*proposed*, only if Question 1 keeps one folder): "`journal/` has one file per agent session, and its name
  starts with the task id."
- **K5.1** (*proposed*): "Task and project memory keep `journal/` (one folder: a task's journal is its files, the
  project's is the whole folder). Agent and user memory keep no journal under this design."
- **K5.2** (*proposed*): change "reads the journal written since the last read" to "reads its task's journal files
  written since the last read". Add one line to its Fails if: "or the read covered other tasks' files".
- **Rd2.2**: replaced. **Rd2.3**: new, as above.
- **Rd4.4**: no change. Rd2.3 now cites it as the only way to reach a superseded or retired entry.
- **Vision statement**: no change. It already says *"Task and project memory keep a journal"* and that agent and user
  memory live outside the repo.
- **`CACHES.md` Rd4.3**: no change. Its "read by the comparison" is now the only reader of `questions/`, and Rd2.2 cites
  it.

## Questions for EJ

1. **Where does a task's journal live?**
   - **(a)** One `project-memory/journal/` folder, each file named with its task id (my default above). This adds no
     folder.
   - **(b)** A `journal/` inside each `work/<task-id>/`. Then the project-level `journal/` holds only sessions that have
     no task, or goes away.

   Option (b) changes the Task and Project rows' "Where it lives" and "Keeps a journal". Either way: does a session ever
   run with no task (for example, a discussion with you)? If it does, whose journal is that session's file?

2. **Where does Claude Code's per-project memory belong?** This is the memory in the home folder,
   `~/.claude/projects/<project>/memory/`, where your notes about this project are kept today. Is it **user memory**
   (one person), **agent memory** (one tool), or **project memory kept in the wrong place**? The design says *"a
   decision about this project is a project entry, whoever made it, EJ included"* and *"anything other agents need must
   not stay only in one agent's private memory"*. Codex, agy and opencode do not read that folder. The answer decides
   which row it falls under, and whether Rd2.3 or W3.5 already rules out its project decisions.
