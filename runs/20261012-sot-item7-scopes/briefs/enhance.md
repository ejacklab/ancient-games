# Brief — enhance one part of a memory design: what is loaded, by scope

You are one of four independent readers. You do not see the others' work. Your job is to **enhance**, not to audit:
build on the owner's idea and propose a complete, simple version.

## Read first

- `/home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md` — the design, accepted by its owner EJ. Read
  it whole. The parts this is about: "When it will be used", "When it will not be used", "Where it is put", Rd1, Rd2,
  Rd4, K5 (the journal), W3.5.
- `/home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/source-of-truth-memory-vision-statements.md`.

## The problem (review item 7)

The design says what is never loaded in two places, with two strengths:
- The main text, "When it will not be used", has two lists: never at session start (`journal/`), and never loaded at
  all (superseded or retired entries except by a link, the whole `project-memory/` tree, whole graph or code-map
  dumps, bulk issue or PR text, another agent's transcripts, credentials).
- Rd2.2 puts all of them under "never at session start" only. Read literally, it lets an agent load credentials or
  another agent's transcripts later in the session.

## EJ's idea — build on this

EJ, 2026-10-12: *"my original idea is, we have memory by scope, task, agent, project, user, not all need the jornal,
and we also define who need and who doesn't"*.

Earlier, also EJ: *"task and project memory need a journal"* and *"an agent will go read the journal"* (now: at the end
of a task and before a handoff or session end).

So the loading rules should follow the **scope** of the memory: task, agent, project, user. For each scope, say who
needs it and who doesn't, and whether it keeps a journal.

What the design says today about each scope:
- **Task:** `project-memory/work/<task-id>/` with `state.md` (the handoff) and `evidence/`.
- **Project:** `project-memory/entries/`, `INDEX.md`, `journal/`, `questions/`, `.cache/`, and `AGENTS.md`.
- **Agent:** outside this design, in the home folder at `~/.claude/agent-memory/<name>/`.
- **User:** outside this design, in the home folder (one person, across projects).

## Your task

Propose, for EJ to decide:

1. **A table by scope** (task, agent, project, user). Columns:
   - where it lives;
   - who writes it;
   - who reads it, and who does not;
   - loaded at session start: yes or no, and which files;
   - read on demand: when;
   - never loaded: what;
   - keeps a journal: yes or no, with one line why.
2. **The rewrite of item 7:** the replacement text for Rd2.2 (and a new Rd2.3 if needed) and for the "When it will not
   be used" paragraph. Each requirement keeps a **Fails if** check. Keep the "never at all" items as strong as the
   main text has them.
3. **What changes elsewhere** in the design if your table is adopted: name the section or requirement id, and say the
   change in one line.
4. **Questions for EJ:** only ones whose answer changes the table. At most three.

Rules:
- Keep it simple: the owner's rule is that memory is simple, and a mechanism that is not needed is removed. Do not
  add folders, files or fields unless the table cannot work without them; if you add one, say why.
- Agent and user memory are outside this design today. You may say what this design needs from them, such as "never
  loaded by another agent", but do not design their insides.
- Label each line *EJ's* (from his words), *design* (already in the document) or *proposed* (yours).
- Do not fill a missing value with your own number.
- Read only; do not change any file.

## Output — one markdown report

```
# Item 7 by scope (<your engine name>)

## The table
## Rewrite of item 7
## What changes elsewhere
## Questions for EJ
```

The launcher tells you your engine name and where the report goes.
