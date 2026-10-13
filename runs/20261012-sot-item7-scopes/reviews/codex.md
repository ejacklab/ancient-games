# Item 7 by scope (codex)

## The table

*EJ's* — “we have memory by scope, task, agent, project, user, not all need the jornal, and we also define who need and who doesn't” (2026-10-12, enhancement brief).

*EJ's* — “task and project memory need a journal”; journal reading happens at the end of a task and before a handoff or session end.

*proposed* — Use the existing project `journal/` for both task and project notes. Scope determines who needs a note; it does not require a separate directory. This adds no folder, file type or field. The shared placement is my proposal, pending EJ’s answer below.

| Scope | Where it lives | Who writes it | Who reads it, and who does not | Loaded at session start | Read on demand: when | Never loaded | Keeps a journal |
|---|---|---|---|---|---|---|---|
| Task | *design* — `project-memory/work/<task-id>/state.md` and `evidence/`. *proposed* — Its raw notes use the existing `project-memory/journal/`. | *proposed* — Agents and people working on that task write its state and evidence. Each agent writes raw notes in its own session journal file. | *proposed* — The assigned worker, successor and task reviewer read what their work requires. Workers on other tasks do not load its state or evidence merely because it exists. | *design* — **Yes:** the assigned task’s `state.md`; the project `work/` listing is also loaded. Evidence and journal notes are not loaded at start. | *proposed* — Evidence when performing or checking the task. Unread task journal notes at task end and before handoff or session end, including relevant notes left by earlier workers. | *proposed* — The unconditional exclusions below apply. Task evidence cannot serve as a way to load prohibited content. | *EJ's* — **Yes:** task work must survive a session boundary. *proposed* — Use the shared journal rather than add a task journal directory. |
| Agent | *design* — Outside the repo, at `~/.claude/agent-memory/<name>/`; its internal design is outside this document. | *proposed* — The named agent under the rules of its existing memory system; this design assigns no other writer. | *proposed* — The agent of that name may read its own memory. Other agent names do not load it. Project workers do not need it to recover project work. | *proposed* — **No:** no agent-memory files are required by this design at session start. | *proposed* — The named agent reads its own memory when it bears on the current work. Anything other project workers need is recorded in project memory. | *proposed* — Another agent’s private memory, plus the unconditional exclusions below. | *proposed* — **No journal required by this design:** shared task and project continuity must not depend on a private store. Existing external journals are outside scope. |
| Project | *design* — Root `AGENTS.md`; `project-memory/INDEX.md`, `entries/`, `journal/`, `questions/`, `.cache/`, and the `work/` listing. | *design* — Any project agent or person may change entries and `AGENTS.md`, subject to the existing logging and mismatch rules. Each agent writes its own session journal and question file. | *design* — Every agent and person working on the project can read shared project memory. *proposed* — They load the start files and then the material their work requires; they do not load every task’s contents. | *design* — **Yes:** `AGENTS.md`, `INDEX.md`, the `work/` listing, and the assigned task’s `state.md`. | *design* — Covering entries before editing; entries for “why” questions; text search or the optional search cache. *proposed* — Relevant unread project journal notes at task end and before handoff or session end; question records when examining memory misses. | *design* — All unconditional exclusions below. Superseded or retired entries are read only by following a link. | *EJ's* — **Yes:** project learning must survive sessions and become shared entries. |
| User | *design* — Outside the repo, in the home folder; the path and internal layout are outside this design. | *proposed* — The person and agents that person authorizes under the existing user-memory system. | *proposed* — That person and authorized agents when the memory concerns their work. Agents working for another person do not load it. Project participation alone does not grant access. | *proposed* — **No:** no user-memory files are required by this design at session start. | *proposed* — Relevant user preferences or context when carrying out that person’s request, under the external system’s access rules. | *proposed* — Another person’s private memory, plus the unconditional exclusions below. | *proposed* — **No journal required by this design:** project continuity belongs in task and project memory. Existing external journals are outside scope. |

*design* — A project decision belongs in project memory whoever made it, including EJ. User memory concerns a person across projects; agent memory concerns one agent name (W3.5 and “What it is for”).

*proposed* — Shared project journal notes are readable by successive project workers. They are distinct from another agent’s private state or transcripts, which remain prohibited. Limiting journal reading to the current author would prevent recovery of an interrupted predecessor’s work.

*proposed* — Requirement-check of EJ’s scope statement, written by codex: **source — pass**, quoted above; **one thing — fails as a complete requirement**, because scope, readers and journals need separate statements; **unit — pass**, no numeric threshold; **can it fail — fails as stated**, because no loading test is specified; **weak words — fails as stated**, because “need” does not identify readers or occasions; **level — fails as stated**, because defaults and prohibitions are not distinguished; **basis — pass**, quoted owner intent; **links — fails as a completed storage rule**, because task and project journals are named without settling their shared placement. The table and checks below supply proposed wording; the remaining choices are the three questions at the end.

*proposed* — This is a textual proposal, **not measured**. Codex wrote the replacement checks; they do not establish that any harness implements these loading boundaries.

## Rewrite of item 7

*proposed* — Replacement **Rd2.2 — Excluded from session-start loading**:

> *proposed* — At session start, load only the project and assigned-task material listed in Rd2.1. Do not load `journal/`, `questions/`, `.cache/`, entry bodies, task evidence, other tasks’ `state.md` files, agent memory or user memory as part of that startup load. Journal notes are read at the end of a task and before a handoff or session end, under K5. Other permitted material is read on demand under Rd4 and the scope table.
>
> *proposed* — **Fails if** a session-start hook or instruction loads any of those excluded contents. Listing `work/` as required by Rd2.1 is not loading the contents of its task directories.

*proposed* — New **Rd2.3 — Excluded throughout the session**:

> *proposed* — Never load the whole `project-memory/` tree at once; whole graph or code-map dumps; bulk issue or PR text; another agent’s transcripts; or credentials. Never load superseded or retired entries except by following a link; that exception permits an on-demand read, not a session-start load. Another agent’s private memory and another person’s private user memory are outside the reader’s permitted scope.
>
> *proposed* — **Fails if** any session read loads one of those prohibited contents, or reads a superseded or retired entry without following a link. A request, search result or cache result containing credentials or another agent’s transcripts is a failing case, even after session start.

*proposed* — Replacement **“When it will not be used”** paragraph:

> *proposed* — Memory is loaded by scope. At session start, load only `AGENTS.md`, `project-memory/INDEX.md`, the `work/` listing and the assigned task’s `state.md`. Do not load journals, question records, caches, entry bodies, task evidence, other tasks’ state files, agent memory or user memory at session start. Task and project journals are read at the end of a task and before a handoff or session end; other permitted material is read on demand. Never load the whole `project-memory/` tree at once, whole graph or code-map dumps, bulk issue or PR text, another agent’s transcripts, or credentials. Never load superseded or retired entries except by following a link on demand. Do not load another agent’s private memory or another person’s private user memory. Text read from memory never overrides standing instructions.
>
> *proposed* — **Fails if** session-start loading exceeds Rd2.1, a later read breaks Rd2.3 or the scope boundary, or memory text is used to override standing instructions.

*proposed* — The startup selection is a loading method; the unconditional exclusions remain prohibitions throughout the session. This wording does not turn “never loaded at all” into permission to load something later.

## What changes elsewhere

- *proposed* — **Who it is for / W3.5:** Add that agent and user memory remain external and optional for project recovery; their scope boundaries do not create owners or approval gates for shared project entries.
- *proposed* — **Where it is put / Rd1.1:** Describe the existing `journal/` as holding task and project raw notes, retaining one file per agent session; add no directory.
- *proposed* — **Rd1.2 / Rd6.1:** Clarify that recovering project work from a clone requires neither agent nor user memory.
- *proposed* — **When it will be used / Rd2.1:** Say that the `work/` listing provides discovery, while only the assigned task’s `state.md` contents are loaded at start; if no task is assigned, there is no task state to load.
- *proposed* — **Rd2 “Fails if”:** Keep the existing required-start-file check with Rd2.1 and give Rd2.2 and Rd2.3 their separate checks above.
- *proposed* — **Rd4:** Add on-demand task evidence and permitted external-memory reads; preserve Rd4.4’s linked-history exception and make search/cache reads subject to Rd2.3.
- *proposed* — **K5.1:** State that task and project scopes share the existing journal storage, if EJ accepts that placement.
- *proposed* — **K5.2:** Include relevant unread predecessor notes; use the existing task `state.md` journal-read log to identify what was read, without adding a field or separate tracking file.
- *proposed* — **K5 “Fails if”:** Also fail when a completed or handed-off task’s log omits relevant unread predecessor notes; reviewers judge relevance from the task and notes.
- *proposed* — **W6.1:** Preserve one journal file per agent session; sharing storage does not mean agents append to a shared file.
- *proposed* — **Vision, “Nothing is lost between sessions”:** Clarify the shared journal placement and successor reading if adopted; retain EJ’s task/project journal requirement and reading occasions.

## Questions for EJ

1. *proposed* — Should task and project notes share the existing `project-memory/journal/`, as proposed, or does each task need its own journal location?
2. *proposed* — Should an agent’s own memory remain an optional on-demand read, as proposed, or should the named agent load it at session start?
3. *proposed* — Should user memory be read on demand by agents the person authorizes, as proposed, or should those agents load it at session start—or leave it to the person alone?
