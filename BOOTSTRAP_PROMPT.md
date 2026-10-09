# Bootstrap prompt — adopt the Ancient Games workflow-design + orchestration style

Copy the block below into a fresh agent session in **any project**, and replace `<PATH>` with the path to the
Ancient Games repo (or its URL). The agent reads the Ancient Games and writes the project's own orchestration files.

---

```
Adopt the Ancient Games workflow-design and orchestration style for this project.

Read the Ancient Games at <PATH>, then:

1. Load the `bootstrap` skill (skills/bootstrap/SKILL.md) and follow it — read this project's blueprint (or ask for
   it), then write this project's `AGENTS.md` and `orchestration.mdc`.

2. From now on, in this project:
   - evaluate every rule and requirement through `requirement-check` (source, one thing, unit, can it fail, weak
     words, level, basis, links);
   - name every function, field and concept through `meaningful-names` (one word, one job);
   - design every workflow through `workflow-design` (a checked sequence, not a DAG; the knowledge graph is
     declared, not drawn).

Use the Ancient Games to enhance this project's workflow design and orchestration style — and keep one copy per
rule: point at the Ancient Games skills, do not paste their bodies into this project.
```
