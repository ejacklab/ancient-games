# Brief — one part of a memory design: runbooks

You are one of four independent readers. You do not see the others' work. Your job is to **enhance**: think it
through and propose one complete, simple answer for the owner, EJ, to decide.

## Read first

- `/home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md`, the design, accepted by EJ. Read it whole.
- `/home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/source-of-truth-memory-vision-statements.md`,
  the settled vision.
- `/home/smoke01/.claude/skills/procedure-to-skill/SKILL.md`, a skill used in this environment that turns a "how do I deploy / run / fix X" procedure
  into a runnable script plus a verify script, rather than a note.

## The problem (review item 8)

The vision lists what memory holds, from EJ's words:
- the **decisions and facts** the code must follow, written before the code;
- what was **learned** after: lessons, observations and hypotheses.

The design has a third kind the vision never mentions, the **runbook**. It is defined as *"how to run or fix
something; where possible it points at a script"* (What it is for; W2.2). It has the file prefix `R-` (layout, W1.1)
and is written at the end of a task (the When-to-write table, W5.2). W2 cites the vision as its source, but the vision
has no runbooks.

The COO offered EJ two ways:
- **(a)** Add runbooks to the vision as "how-to" memory, learned after the work, next to lessons.
- **(b)** Drop runbooks from the design. Procedures become skills or scripts (see the skill above), and memory needs at
  most a pointer.

These two are a starting point, not a limit. A third way is welcome if it is simpler.

## Your task

1. **Recommend one way**, in one sentence.
2. **Three reasons**, each grounded in the design, the vision or the skill. Quote the line you rely on.
3. **The exact text changes** your way needs:
   - in the vision;
   - in the design, by section or requirement id (W1.1, W2.2, W5.2, the layout, What it is for, and any other place
     that names runbooks).

   Each requirement you change keeps a **Fails if** check.
4. **What could go wrong** with your way: one concrete case.
5. **Questions for EJ:** at most two, and only ones whose answer changes your text.

Rules:
- Keep it simple. The owner's rule is that memory is simple, and a mechanism that is not needed is removed. Don't add
  folders, files or fields unless your way cannot work without them.
- The design has four memory scopes: task, project, agent and user. Say which scope a runbook (or what replaces it)
  belongs to.
- Label each line *EJ's* (his words), *design* (already in the document) or *proposed* (yours).
- Read only; do not change any file.

## Output — one markdown report

```
# Item 8, runbooks (<your engine name>)

## Recommendation
## Three reasons
## Text changes
## What could go wrong
## Questions for EJ
```

The launcher tells you your engine name and where the report goes.
