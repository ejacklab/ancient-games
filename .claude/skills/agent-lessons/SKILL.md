---
name: agent-lessons
description: Lessons learned from agents' failures, for one agent type (the main Claude agent, opencode, Codex, agy, mcode, dsh) or for every agent, in any project. Use when filing the lesson of an insight whose fix the owner chose, when writing a brief for an engine (put the matching lessons' text in it), or before testing, editing code or calling an engine in a way a lesson may cover. NOT for facts about one project's code — those go in a LESSONS.md beside that code.
---

# Agent lessons

A **lesson** is what an insight teaches an agent type, or every agent, in any project. A **project fact** is what
the same insight says about one project's code; it stays in that project, in a `LESSONS.md` in the code's own folder.
The guard's spec, Round 18 (`workflow-design/guard/SPEC.md`), is the one copy of the format and the matching rules.

## A lesson file — `lessons/<slug>.md`

```
---
agents: [all]                 # or: claude-main, opencode, codex, agy, mcode, dsh
kinds: [code-edit, test]      # test, code-edit, engine-call, brief, command
paths: []                     # optional globs, for a kind of file ("**/*.test.ts")
commands: []                  # optional command words ("git", "codex")
from: runs/<run>/insight.md#<id>
enforced_by: ""               # a check or test that now enforces it
---
The lesson, in one to three sentences. No path from one project: that is a project fact.
```

## Filing

When the agent applies an insight's fix (R12.3: the option it ranks first; the owner may overrule), it files:
- the lesson, here, when it holds for an agent type or every agent anywhere;
- the project facts, in the `LESSONS.md` of the folder that holds the code, as ``- `<file name>` — <fact>``;
- `filed:` with both files, on the fix's entry in `insight-decisions.md`.

A lesson the owner overrules is removed. When a check or test comes to enforce a lesson, set `enforced_by`; the lesson
is then given only as a pointer to that check.

## Getting the matching lessons

- The main agent: the guard gives them before a Write, Edit or Bash call (Round 18, L5), once per session each.
- An engine: `bun <ancient-games>/.claude/skills/workflow-design/guard/src/cli.ts lessons for --agent opencode
  --kinds test --paths <files>` prints them; put that text in the brief's Lessons section, never a path to read.
- `lessons check` reports invalid lesson files.
