---
name: bootstrap
description: Bootstrap a new project's agent orchestration from the Ancient Games — generate its AGENTS.md (instructions) and orchestration.mdc (workflow-design + orchestration rules) from its blueprint, and adopt the Ancient Games style. Use when a project wants to work the Ancient Games way.
---

# Bootstrap a project's orchestration

Turn the Ancient Games knowledge into a new project's **standing** orchestration files. Run once when a project
adopts the style; after that the project's AIs read its own `AGENTS.md` + `orchestration.mdc`, not the Ancient Games.

## What you produce

1. **`AGENTS.md`** — the project's instructions: what the folder is for, the key rules, how to work.
2. **`orchestration.mdc`** — the project's orchestration rules: engines, checks, loops, the five referee stages,
   and the feedback templates, instantiated for this project.

## How

1. **Read the blueprint** — `docs/blueprint/` if it exists, else ask for: vision, requirements with acceptance
   criteria, architecture, data, UI, non-functional. A project without a blueprint gets a draft one first (a
   blueprint piece).
2. **Write `AGENTS.md`** from the blueprint: name the project, what it is for, its working rules. State each rule
   through `requirement-check` (source, one thing, unit, can it fail, weak words, level, basis, links); name
   things through `meaningful-names` (one word, one job).
3. **Write `orchestration.mdc`** by mapping the project's task types onto the Ancient Games defaults — engine per
   type, check, sabotage, loop limit and exit — and the five referee stages (Gate, Guard, Corroborate, Filter,
   Prove). The feedback templates live in the workflow-design skill's `references`; reference them, do not re-copy.
4. **One copy per rule.** Point at the Ancient Games skills; do not paste their bodies into the project.

## The rules every generated file must carry

- **Every field has one writer** — a return template is the worker's; a verdict is the human's. Name who fills it.
- **Evidence lives in the project** (`runs/<run-id>/`), never `/tmp`.
- **A workflow is a checked sequence** — each step's result is verified, then becomes the next step's input. Not a
  DAG for its own sake.
- **The knowledge graph is declared** — each piece's needs and outputs, and what each must not see.
