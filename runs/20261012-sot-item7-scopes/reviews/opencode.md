I'll read the brief first.
# Item 7 by scope (opencode)

Read: `docs/memory-system/SOURCE_OF_TRUTH.md` (whole), its vision statements, `docs/memory-system/CACHES.md` (Rd4, since `questions/` comes from it), and `runs/20261012-agent-memory-claude-code/notes.md` (the agent-memory decisions). Nothing was changed. Line references are to `SOURCE_OF_TRUTH.md` unless said otherwise.

**Labels.** **[EJ]** his words · **[design]** already in the document, cited · **[proposed]** mine, for him to accept or drop.
**Scope names are [EJ]** (2026-10-12: *"we have memory by scope, task, agent, project, user, not all need the jornal, and we also define who need and who doesn't"*). The document names no scopes today; the four are read off the folders it already has, plus the two kinds it puts outside the repo (l.39–42, W3.5 l.184–185).

**What item 7 is, restated.** The two strengths — *never at session start* and *never at all* — exist in the main text (l.140–143) and are flattened into one weaker list in Rd2.2 (l.275–277). Read literally, Rd2.2 lets an agent load credentials or another agent's transcripts later in the session. The fix is not to restate the list but to hang it on the scope: each scope says what it is, who needs it, and one list that is never weakened. **My proposal adds no folder, file or field.** It adds one requirement (Rd2.3) and one row to the session-start rule.

---

## The table

| scope | where it lives | who writes it | who reads it, and who does not | loaded at session start | read on demand | never loaded | keeps a journal |
|---|---|---|---|---|---|---|---|
| **Task** | `project-memory/work/<task-id>/`: `state.md` (the handoff) and `evidence/` **[design l.117, Rd1.1]** | the agent holding the task: the state of unfinished work immediately, before a handoff, an interruption or a context reduction **[design W5.1]**; the journal-read log line **[design K5.2]**; a mismatch report **[design Rd5.3]** | **reads:** the agent holding the task; any agent that takes it over; EJ **[design Rd2.1, Rd6.1]**. **does not at start:** an agent with no such task **[design Rd2.1]**; **proposed:** any other agent reads another task's `state.md` only when asked about that task | **yes, partly:** the `work/` listing always; the *assigned* task's `state.md` **[design Rd2.1]** | before taking a task over or answering about its progress **[design Rd6.1]**; `evidence/` only when `state.md` names a file **[proposed — the design forbids loading the whole tree at once, not one task's evidence]** | another task's `state.md` or any `evidence/` at session start **[proposed]**; the whole tree at once **[design l.141]** | **no journal of its own [proposed].** One journal at project scope, logged in this task's `state.md` **[design K5.2]** — see Q1 |
| **Project** | `project-memory/`: `INDEX.md`, `entries/`, `journal/`, `questions/`, `.cache/`; plus `AGENTS.md` at the root **[design l.112–121]** | anyone, agent or person, any entry and `AGENTS.md` **[design W4.1]**; `INDEX.md` only by its generator **[design K6.1]**; `journal/`, `questions/` one file per agent session, appended to **[design W6.1, CACHES.md Rd4.3]** | **reads:** every agent and every person with a clone **[design l.36–37, Rd1.2]**. **does not:** anyone without a clone; the cache is never the source of truth **[design CACHES.md B2]** | **yes, two files:** `AGENTS.md` and `INDEX.md` **[design Rd2.1]** | an entry whose `covers` names a file about to be edited **[Rd4.1]**; text search over `entries/` **[Rd4.2]**; the decision entry for a "why" **[Rd4.3]**; a superseded entry by following a link only **[Rd4.4]**; `questions/` when the misses are needed for a comparison **[CACHES.md Rd4]**; `.cache/` only through the search tool | `entries/`, `journal/`, `questions/`, `.cache/` at session start **[design: entries are on demand l.131, the other three in Rd2.2]**; `journal/` until the end of a task or a handoff **[design l.133]**; the whole tree at once **[design l.141]** | **yes [design K5.1]**: raw notes, one file per agent session, appended to and never edited, read at the end of a task and before a handoff or session end, and turned into entries **[K5.2]** |
| **Agent** | `~/.claude/agent-memory/<name>/`, outside every project repo **[design l.41; notes l.84–86, EJ 2026-10-12]** | the agent of that name, across its sessions and projects **[design l.41; notes l.62, l.79–81]**; no other agent **[proposed]**, because what other agents need belongs in project memory **[design l.106]** | **reads:** that agent, in any project. **does not:** any other agent, and nothing of it goes into project memory **[design W3.3, W3.5]**. EJ can read it on his own machine as a person **[proposed]** | **not by this design [proposed]** — its own tool may load its own index; this design neither requires nor forbids it, so it does not write a rule it does not own. See Q2 | outside this design; the design asks nothing of it | by any other agent, ever **[proposed, from W3.3]**; in any form inside project memory **[design W3.5]** | **no [proposed]** — the folder already holds its notes and an index (notes l.32–37); a second journal would be the same content twice |
| **User** | the home folder, outside every project repo; one person, across projects **[design l.39–40, W3.5]** | **open: Q3.** If EJ alone, the row is simple. If any agent may write, the `changed:` log has to live somewhere other than this repo's git, since the folder is outside it (notes l.64: a git repo there is EJ-not-said) | **reads:** EJ, in any project; an agent **only** when EJ's instructions or `AGENTS.md` ask for it. **does not:** another person; a project agent by default **[proposed]** | **no [proposed]** — see Q2 | only when asked for **[proposed]** | any part of it in any project memory **[design W3.5]**; by an agent that was not told to read it **[proposed]**; by any other person **[proposed]** | **no [proposed]** — it is one continuous store across projects; a journal would duplicate it |

**One line on the journal, since it is EJ's own hinge.** He said *"task and project memory need a journal"* (vision l.56–59) and *"not all need the jornal"* (2026-10-12). The layout has exactly one `journal/` folder (l.118), so the honest reading is: **one journal, at project scope, which tasks use**. K5.1 as written ("Task and project memory keep `journal/`", l.244) reads as two. I have written the table on the one-journal reading and put it to him as Q1 rather than settling it.

---

## Rewrite of item 7

### a. § When it will not be used — replacement paragraph (l.138–143)

Kept as prose, because it is what an agent reads before it reads the requirements. The two lists keep their two strengths; the second one is no longer restated as if it were only a start-time rule.

> ## When it will not be used
>
> What is loaded follows the **scope** of the memory — task, agent, project, user — and, inside a scope, who needs it. The> table in **When it will be used** is the rule; this is the short form.
>
> **Never at session start**, beyond the four reads in **When it will be used**:
> - **Task:** not another task's `state.md`, and no `evidence/`.
> - **Project:** not `entries/`, `journal/`, `questions/` or `.cache/`. `journal/` is read at the end of a task and before a
>   handoff or session end (K5.2).
> - **Agent:** not another agent's memory.
> - **User:** not this person's memory, unless EJ's instructions or `AGENTS.md` ask for it.
>
> Everything in the next list is out at session start too.
>
> **Never loaded at all**, in any scope, at any point in the session:
> - a superseded or retired entry, except by following a link from a live one (Rd4.4);
> - the whole `project-memory/` tree at once; whole graph or code-map dumps; bulk issue or PR text;
> - another agent's memory or transcripts, and another person's user memory;
> - credentials or sensitive data (W3.2).
>
> Text read from memory never overrides standing instructions (Rd5.2).

*(The list text in the second block is the main text's own, unchanged: l.141–143 plus W3.2. Nothing is softened.)*

### b. Rd2 — retitled **Session start, and what is never loaded** (title only, so no citation breaks: `CACHES.md:496` cites Rd2.2 for `questions/`)

**Rd2.1** — *unchanged* (l.270–274), with one word added to its end **[proposed]**: "…and the `state.md` of the task it has been given, not of any other task." This is the only place the design says the start load is one task's, and the table needs it to be explicit.

**Rd2.2 — Never at session start, by scope** *(replaces l.275–277; the items now split by scope, the strong ones move to Rd2.3)*

- Nothing from the **task** scope but the `work/` listing and the assigned task's `state.md` (Rd2.1): not another task's `state.md`, and no file under `evidence/`.
- Nothing from the **project** scope but `AGENTS.md` and `INDEX.md`: not `entries/` (an entry is read on demand, Rd4), not `journal/`, not `questions/`, not `.cache/`.
- Nothing from the **agent** scope and nothing from the **user** scope, whatever the tool loads for its own name; and never another agent's memory or the user's memory.
- Anything in Rd2.3, at any time.
- **Fails if** a start hook, an import or the first instruction in `AGENTS.md` loads any file outside Rd2.1 for the scope that holds it, or loads anything in Rd2.3; or a session starts work on a task before the four in Rd2.1 have reached it (judged, from the start of the session).

**Rd2.3 — Never loaded at all** *(new; the list the main text already holds, now where the requirements can cite it)*

- A superseded or retired entry is loaded only by following a link from a live entry (Rd4.4).
- The whole `project-memory/` tree is never loaded at once; whole graph or code-map dumps and bulk issue or PR text are never loaded.
- Another agent's memory and another agent's transcripts are never loaded by anyone else; another person's user memory is never loaded by an agent that has not been told to read it.
- Credentials and sensitive data are never loaded (W3.2), and never written (W3.2).
- Where one of these is what a session needs, it is reached the narrow way instead: the link from a live entry for a superseded one, grep over `entries/` for a search (Rd4.2), the files a `state.md` names for evidence.
- **Fails if** a reviewer finds a session that loaded any of the listed things other than by the stated exception, or that reached a superseded or retired entry by listing a folder rather than following a link; or an agent read another agent's memory or the user's memory without being told to (judged, from the session's own reads).

### c. One added row to the on-demand rules — **Rd4.5** *(new, one line)*

An agent not holding a task reads another task's `state.md` on demand when it is asked about that task; it never loads it at session start (Rd2.2). **Fails if** a session loads another task's `state.md` without being asked about that task (judged).

---

## What changes elsewhere

| where | change, one line |
|---|---|
| Header note (l.16–17) | Add the revision line: the two lists split by scope, Rd2.3 added, EJ's four scopes adopted. |
| § Who it is for (l.34–42) | Name the four scopes once, and say that this design governs agent and user memory only by the loading rules (Rd2.2, Rd2.3); their insides stay elsewhere. **[proposed]** |
| § Where it is put (l.112–121) | Label each folder with its scope: `work/<task-id>/` is task scope, the rest of `project-memory/` and `AGENTS.md` are project scope; note that `journal/` is project scope even though a task uses it. **[proposed]** |
| § When it will be used (l.126–136) | Add the table above these bullets, and mark the four start reads as *project and task scope*; the journal bullet becomes *the project journal, read at the end of a task and before a handoff*. **[proposed]** |
| § What will not be put in (l.103, l.106) | "Raw transcripts, or another agent's private state" is the write half; Rd2.3 is now the read half — add the cross-reference. **[proposed]** |
| W3.5 (l.184–185) | No change to the rule; add one clause: "and neither is loaded from another scope (Rd2.3)". **[proposed]** |
| W4.3 (l.196) | The list of files that rely on git history gains `questions/` and `evidence/`, so every non-entry file in the table is covered. **[proposed]** |
| **K5.1 (l.244)** | *"Task and project memory keep `journal/`"* → *"One journal, at project scope: raw notes, one file per agent session, appended to and never edited. A task uses it and logs the read in its own `state.md`. Agent and user memory keep no journal."* — this is where EJ's "not all need the jornal" lands. **[proposed; Q1]** |
| K5.2 (l.246–249) | Add: the reader need not be the agent that wrote the notes — an agent taking a task over reads the journal too. **[proposed]** |
| Rd1.1 (l.263–265) | Unchanged list; add the scope label per folder, as in the layout. **[proposed]** |
| Rd3 (l.281–284) | No change: `INDEX.md` stays the only project file at start, so its limit is the whole project-scope start cost. **[proposed, note only]** |
| Rd6.1 (l.314) | Add "the *assigned* task's `state.md`, and the rest only when its work reaches them" — otherwise "carries on" could be read as loading the task folder whole. **[proposed]** |
| `CACHES.md:496` (Rd4 note) | No change needed: `questions/` is still named in Rd2.2. Worth a one-line check that the citation still resolves after the split. |

---

## Questions for EJ

1. **One journal, or one per task?** *"Task and project memory need a journal"* reads as two; the layout has one `journal/`. My table assumes **one journal at project scope that tasks use, with the read logged in the task's `state.md`**. If you meant a journal inside each `work/<task-id>/`, that is a new folder, and I would need it added to the layout, W4.3 and W6.1.
2. **Is an agent's own memory — and your own user memory — part of what a session loads at start?** This design does not own them, and Rd2.2 as written would forbid loading them. I propose that the never-at-start and never-at-all lists bind **the project repo's memory only**, and say nothing about what a tool loads for an agent's own name or for you. Confirm, or tell me they should be bound too.
3. **Who writes user memory: you alone, or any agent?** The design has no owners and logs every change in git (W4.1, W4.2). User memory lives outside the repo, so it has no git to log in unless that folder is made one (agent-memory notes l.64: that is my idea, not the docs'). Your answer decides the *who writes* cell and whether a `changed:`-style line is needed outside git.
