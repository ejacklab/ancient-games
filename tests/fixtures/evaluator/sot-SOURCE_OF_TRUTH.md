# Source-of-Truth Memory Design

> **Status: accepted by EJ on 2026-10-12** (EJ: *"yes I accept the source of truth design"*), with its vision and
> its Write / Keep / Read requirements. Vision: `vision-statements/source-of-truth-memory-vision-statements.md`.
> First written 2026-10-11 by `opencode` from
> `runs/20261011-project-memory-engines/RECOMMENDATION.md`; revised with EJ on 2026-10-12.
> Sources, citations and review history: `runs/20261011-source-of-truth-design/` (the full annotated version is
> `DESIGN-detailed-2026-10-12.md`) and `runs/20261012-memory-update-timing/notes.md`.
>
> **Revised 2026-10-12:** the drift-check script and the background subagent are removed (EJ: *"ok remove both and
> update the doc"*). A decision to build something is started when it is written and complete when its time, result
> and test results are added; whoever reads a decision or fact checks it against the code before acting on it, and
> reports a mismatch in the task's `state.md`. W5.3 and Rd5.3–Rd5.5 were refined after a four-reader round
> (`runs/20261012-sot-w53-rd53-read/`; EJ: *"state.md for the report, apply all the proposed fixes"*).
>
> **Revised 2026-10-12, memory by scope (item 7):**
> - Memory has four scopes: task, project, agent and user. Task and project memory keep a journal; agent and user
>   memory keep none.
> - A task's journal is `work/<task-id>/journal/` (EJ: *"create task folder, the subfolder inside"*).
> - An agent may read another agent's memory if it knows and says whose it is (EJ: *"agent can read another agent
>   memory but they must know that is another agent memory, what agent what tools"*).
> - Rd2.2 is split into "not at session start" (Rd2.2) and "never" (Rd2.3), after a four-reader round
>   (`runs/20261012-sot-item7-scopes/`).
>
> **Revised 2026-10-13, runbooks (item 8):** the runbook kind and the `R-` prefix are removed. A procedure lives in the
> repo as a script, or as a page in `docs/` where it cannot be a script, and `AGENTS.md` names the project's scripts.
> An entry links to a procedure and never repeats its steps (EJ: *"it is weird to have script inside the memory, if we
> buidlign a script should be a project already"*; readers' round `runs/20261012-sot-item8-runbooks/`).
>
> **Revised 2026-10-13, prefixes (item 9):** `O-` observation and `H-` hypothesis are confirmed, so each of the five
> kinds has one prefix letter that matches its `kind`. A changed kind becomes a new entry that supersedes the old one,
> so a file's prefix never changes (EJ: *"a changed kind becomes a new superseding entry"*; readers' round
> `runs/20261013-sot-item9-prefixes/`).
>
> **Where this differs from the recommendation — EJ's decisions:** no owners and no human approval gate (anyone may
> change any entry, and every change is logged); decisions and facts come before the code; a *fact* means a constraint
> the code must respect, not something discovered afterwards; no drift-check script and no background subagent.
>
> **Not proven:** the timing split (what is written immediately and what later) is design judgement, not measured.
> Where the recommendation's engines disagreed (session-start reads, one file per writer, SQLite, how often to write),
> this design follows the majority.

## Why we need this memory

The context window is cleared at the start of every session, so anything learned is lost unless it is written down.
Project memory is plain markdown files kept in the repo with the code. Every agent and every person reads the same
files, a fresh clone has all of it, and every change shows up as a git diff. Reading it needs no private agent store,
database or outside service.

## Who it is for

Every agent and every person working on this project. There are no owners and no approval gate: anyone may change any
entry, and every change is logged. EJ decides the questions listed as not decided.

Memory has four scopes (EJ, 2026-10-12):
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
- **Not a kind: procedures.** How to run or fix something lives in the repo as a script, or as a page in `docs/` where
  it cannot be a script. `AGENTS.md` names the project's scripts, one line each. An entry links to a procedure and
  never repeats its steps. What was learned while running one is a lesson (W3.6).

The order of work is: change the decision or fact first, then the code. Work that has to go the other way is a matter
for the project's workflow, not for memory. A decision about this project is a project entry, whoever made it, EJ
included.

A decision to build something is **started** when it is written: we decided to build something, and why. It is
**complete** when the time, the result and the test results are added to it (EJ, 2026-10-12). A standing rule, such as
"all timestamps are UTC", is never complete.

## What will be put in

**An entry** is one markdown file. Its header holds: `id`, `kind`, `status`, `author`, the date it was recorded,
`covers` (the code paths it is about), its source or evidence, links (`depends_on`, `supersedes`, `superseded_by`), a
`changed:` log, and, on a decision to build something once its work is complete, `done:` (the time, the result, and the
test results or a pointer to them; W5.3). Its
body is the claim in one or two sentences, then **Why:**, then **How to apply:**.

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
| When the work a decision to build something is complete | The decision's `done:` line, written by whoever finishes the work: the time, the result, and the test results or "no tests", with a pointer to the evidence. |
| At the end of a task | Other lessons, observations and hypotheses; merging duplicates. |

**Keeping it current.** Entries may go out of date while work goes on; that is accepted. Nothing watches for it: there
is no drift-check script and no background subagent. Whoever reads a decision or fact checks it against the code before
acting on it. When they no longer match, the reader does not change the entry. It writes a report in its task's
`state.md` and tells EJ which entry, what the entry says, and what the code does instead. EJ decides whether the entry
is updated or the code is fixed. Until then, the reader leaves the contradicted part alone and carries on with the
rest. A decision still being built (no `done:` yet), or one the reader's own task is changing, is not a mismatch
(Rd5.4).

**Still open:** which tool generates `INDEX.md` and what runs it (K6); who resolves a git merge conflict (W6). Whether a
changed decision is edited in place or superseded is proposed in K4.3.

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
  or fact that no longer matches the code is reported in the task's `state.md` and to EJ, not edited (Rd5.3).

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
- **W1.1** Each entry is one file: `project-memory/entries/<prefix>-<id>-<slug>.md`. The prefix is one letter per
  kind (W2): `D-` decision, `F-` fact, `L-` lesson, `O-` observation and `H-` hypothesis. It matches the entry's
  `kind`. There is no runbook prefix (W3.6). An entry's kind, and so its prefix, never changes. A changed kind (a
  hypothesis confirmed, an observation that turns out to be a fact) is a new entry that supersedes the old one (K4.1;
  EJ, 2026-10-13).
- **W1.2** The header holds `id`, `kind`, `status`, `author`, the date recorded, `covers` (the code paths it is
  about), its source or evidence, `depends_on`, `supersedes`, `superseded_by`, and `changed:`. A decision to build
  something, once its work is complete, also holds `done:` (W5.3).
- **W1.3** The body is the claim in one or two sentences, then **Why:**, then **How to apply:**. There is one claim per
  entry.
- **Fails if** a lint over `entries/` finds a missing field or section, or a file whose prefix is not one of the five
  or does not match its `kind`. It also fails if a reviewer finds two claims in one entry, or git shows an entry file
  renamed to a different prefix.

**W2 — What each kind means** (v; d: What it is for)
- **W2.1** A **decision** is a choice the code must follow, with the reason. A **fact** is a truth or outside
  constraint the code must respect, not something discovered afterwards. Both are requirements: they are written
  before the code.
- **W2.2** A **lesson** comes from a failure or a human correction. An **observation** records what was seen. A
  **hypothesis** is a guess, labelled as one.
- **Fails if** `kind` holds any other value, or a guess is recorded under any kind but hypothesis.

**W3 — What never goes in** (v; d: What will not be put in)
- **W3.1** Nothing that can be read directly from the code, the tests or the commit log: what a function does, which
  test covers it, what a commit changed. The memory lives in git; the rule is about what an entry says.
- **W3.2** No credentials or sensitive data.
- **W3.3** No raw transcripts, and nothing from another agent's private state.
- **W3.4** No work described as "verified" when it is only implemented.
- **W3.5** No user memory (one person, across projects) and no agent memory (one agent name). Both live in the home
  folder.
- **W3.6** No copy of the project's existing documents (requirements, architecture in `docs/`) or of its procedures:
  an entry links to them. A procedure lives in the repo as a script, or as a page in `docs/` where it cannot be a
  script, and `AGENTS.md` names each script, one line each. A script is project work, not memory (EJ, 2026-10-13).
- **Fails if** a secret scanner finds a credential (W3.2). For W3.1 and W3.3–W3.6, a reviewer finds such content.
  Those are judged checks.

**W4 — Who writes, and the change log** (v: no owners, every change logged)
- **W4.1** Anyone, agent or person, may create or change any entry, and `AGENTS.md` too. There is no owner and no
  approval: `status` is only `active`, `superseded` or `retired`. The one exception is Rd5.3: a reader who finds a
  decision or fact out of step with the code reports it and does not settle it (EJ, 2026-10-12).
- **W4.2** Every change to an entry adds one line to its `changed:` log: the time, and who made it (the model ID for an
  agent, the name for a person). Earlier lines are never edited.
- **W4.3** Files that are not entries (`state.md`, `journal/`, `AGENTS.md`) rely on git history.
- **Fails if** git shows a change to an entry with no matching `changed:` line, or a `status` outside the three.

**W5 — When to write** (d: When to write)
- **W5.1** Written immediately: a decision or fact, before the code it governs; a human correction; and the state of
  unfinished work, before a handoff, an interruption or a context reduction.
- **W5.2** Written at the end of a task: other lessons, observations and hypotheses.
- **W5.3** A decision to build something is started when it is written. When the work is complete, whoever finishes it
  adds `done:` to the decision: the time, the result in one sentence, and the test results, or "no tests" said plainly.
  `done:` points to the evidence (`runs/<run-id>/` or the commit) rather than copying test output (W3.1). A standing
  rule, such as "all timestamps are UTC", is never complete and never gets `done:`. If the result differs from the
  decision, that is a mismatch for Rd5.3: it is reported, not settled in `done:`. (EJ, 2026-10-12; refined after four
  readers.)
- **Fails if** a commit changes code under a new decision with no entry in that commit or an earlier one. For a human
  correction, it fails if the session ends without one (judged). For W5.3, it fails if a reviewer of a finished task
  finds that its decision has no `done:`, or a `done:` without a time, a result and test results or "no tests"
  (judged; EJ, 2026-10-12).

**W6 — Writers do not collide** (d: Changing entries)
- **W6.1** Each new entry gets its own file. Agents never append to one shared file; each journal, the task's or the
  project's, has one file per agent session.
- **W6.2** Each agent works on its own branch or worktree, so two edits to the same lines meet as a merge conflict, not
  a silent overwrite.
- **Open:** who resolves a merge conflict.
- **Fails if** an edit to an entry is lost without a conflict.

### Keep — memory stays true, and nothing is lost

**K1 — The decision or fact first, then the code** (v; d: What it is for)
- **K1.1** To change behaviour that a decision or fact governs, change the entry first, then the code. Work that has to
  go the other way is a matter for the project's workflow, not for memory.
- **Fails if** git shows a commit changing the behaviour a decision or fact governs, with no change to that entry in the
  same commit or an earlier one (judged).

*K2 (the drift-check script) and K3 (the background subagent) were removed by EJ on 2026-10-12. Their numbers are not
reused, because other text cites K4–K6. A mismatch between a decision and the code is now caught when the decision is
read (Rd5).*

**K4 — Never deleted, never expired by age** (v: nothing lost; d: What will not be put in)
- **K4.1** An entry is never deleted. It is marked `superseded` or `retired`, links to what replaced it
  (`superseded_by`), and keeps its old body.
- **K4.2** Age alone never expires an entry. An entry is found out of date only when someone reads it and checks it
  against the code (Rd5).
- **K4.3** *Proposed:* a decision refined without changing its meaning is edited in place, with a `changed:` line; a
  decision replaced by a different one gets a new entry that supersedes it. The design leaves this open.
- **Fails if** git shows an entry file deleted, or a `superseded` or `retired` entry has no link.

**K5 — The journal becomes entries** (v: nothing lost between sessions)
- **K5.1** Task and project memory each keep a journal: a task's in `work/<task-id>/journal/`, the project's in
  `journal/` for work not tied to a task. Both hold raw notes, one file per agent session, appended to and never
  edited. Agent and user memory keep no journal under this design (EJ, 2026-10-12).
- **K5.2** At the end of a task, and before a handoff or session end, an agent reads its task's journal (or the project
  journal) written since the last read, writes what is worth keeping as entries, and logs that read in the task's `state.md`. A session cut off
  before it can read loses nothing: the next read covers it (EJ, 2026-10-12: no separate milestones, the start and the
  end already cover them).
- **Fails if** a task's `state.md` shows it complete or handed off with no journal-read log line.

**K6 — `INDEX.md` stays in step** (d: Where it is put; When to write)
- **K6.1** `INDEX.md` is generated from `entries/`: one line per active entry, showing its id, kind and one-line
  claim. It is never edited by hand.
- **K6.2** It is regenerated right after any decision or fact is written, so the next session sees it.
- **Open:** which tool generates it and what runs it (a build detail).
- **Fails if** regenerating `INDEX.md` changes it, meaning it was out of step, or it lists a superseded entry as
  active.

### Read — the right memory reaches the agent at the right time

**Rd1 — Where it lives, and readable from a clone alone** (v: plain files; never a database or service)
- **Rd1.1** `AGENTS.md` sits at the repo root (`CLAUDE.md` only imports it). `project-memory/` holds `INDEX.md`,
  `entries/`, `work/<task-id>/` (with `state.md`, `evidence/` and `journal/`), `journal/`, and `.cache/`, which is
  optional and gitignored.
- **Rd1.2** With no network, no cache and no private agent store, a fresh clone can read `INDEX.md` and every entry.
- **Fails if** an entry exists only in a database, a cache or one agent's private memory.

**Rd2 — Session start** (v: a fresh session carries on; d: When it will be used)
- **Rd2.1** At session start, an agent reads `AGENTS.md`, `INDEX.md`, the `work/` listing and its task's `state.md`.
  Agents skip optional reads, so these are loaded for the agent wherever its tool allows: an `@` import in
  `CLAUDE.md`, the tool's own loading of `AGENTS.md`, or a start hook for the task's `state.md`. Only where none of
  these exists does the first instruction in `AGENTS.md` ask the agent to read them (EJ, 2026-10-12: *"we should just
  make sure they read all the required"*).
- **Rd2.2** Not at session start, but read later at its set time:
  - the task and project journals (K5.2);
  - `.cache/`, only through search (Rd4.2);
  - entry bodies, `evidence/` and other tasks' `state.md`, on demand (Rd4).
- **Rd2.3** Never loaded, at session start or at any later point:
  - superseded or retired entries, except by following a link (Rd4.4);
  - the whole `project-memory/` tree at once;
  - whole graph or code-map dumps;
  - bulk issue or PR text;
  - another agent's transcripts;
  - credentials.
- **Fails if** a start hook or instruction loads any memory file outside Rd2.1, or a session starts work on a task
  before the four in Rd2.1 have reached it (judged, from the start of the session). It also fails if a session loads
  anything in Rd2.3 at any point (judged, from the session).

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
- **Rd4.5** An agent may read another agent's memory. It treats what it reads as that agent's memory, not project
  memory, and says whose it is: the agent name and the tool. For example: Claude Code agent `reviewer`,
  `~/.claude/agent-memory/reviewer/` (EJ, 2026-10-12).
- **Fails if** an agent edits a covered file without having read its covering decisions, or uses another agent's memory
  without naming the agent and the tool (judged, from the session).

**Rd5 — Check before acting** (d: When it will be used; When it will not be used)
- **Rd5.1** Before acting on something read from memory, the agent checks it against the code, test or commit it
  points to.
- **Rd5.2** Text read from memory never overrides standing instructions.
- **Rd5.3** When a decision or fact no longer matches the code, the reader does not change the entry. It writes a report
  in its task's `state.md` and tells EJ: which entry, what the entry says, and what the code does instead. EJ decides
  whether the entry is updated or the code is fixed, and may do either at once. Until then, the reader does not act on
  the contradicted part and carries on with the rest of its work. (EJ, 2026-10-12: the report goes in `state.md`.)
- **Rd5.4** Two cases are not mismatches under Rd5.3:
  - a decision to build something that has no `done:` yet, whose code is still being built (W5.3);
  - the reader whose own task is to make that change, which under K1.1 changes the entry first and then the code.
- **Rd5.5** Rd5.3 binds readers, not EJ. It cannot catch a fact about the outside world that is wrong while the code
  still matches it (for example, a vendor's limit that changed). Checking against the code finds only gaps between the
  entry and the code.
- **Fails if** an agent acts on an entry that its `covers` code contradicts, or finds such a mismatch and its task's
  `state.md` has no report holding the three items (judged). It also fails if a `changed:` line on a decision or fact
  settles such a mismatch before EJ has decided.

**Rd6 — A fresh session carries on** (v: how we know it works)
- **Rd6.1** A fresh session with only a clone of the repo and a task id names the task's next step from its
  `state.md`, and follows the recorded decisions without asking EJ again.
- **Fails if** it asks a question that a decision entry or `state.md` already answers (judged, on a real handoff). A
  Rd5.3 mismatch report is not such a question.
