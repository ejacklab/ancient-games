# Ancient Games — skills bundle

Three skills, self-contained so another project can drop them in and use them. No symlinks — everything here is a
real file.

| skill | what it does | triggers on |
|---|---|---|
| `workflow-design` | the method half of the Ancient Games: turn a task into a designed workflow (or decide none is needed) | designing a workflow / deciding none is needed |
| `requirement-check` | evaluate a rule / requirement / threshold against the eight questions | a stated rule or requirement |
| `meaningful-names` | the clean-code standard for naming (one word, one job) | naming / a name that does several jobs |

## Use it

Copy a skill's folder into one of the skill roots the tool scans:

```
cp -r skills/workflow-design  ~/.claude/skills/     # Claude Code
cp -r skills/workflow-design  ~/.agents/skills/     # DeepSeek Harness / Codex
```

`requirement-check` and `meaningful-names` are general standards — install them anywhere, not just Ancient Games
projects. `workflow-design` is the member of the Ancient Games framework (method + referee + knowledge).

## Relationship to the rest of the repo

`docs/` is the **source of truth** for the method (`WORKFLOW_DESIGN_METHOD.md`), the task types, the executor kinds
and the templates. This folder is the **portable export**: when you change a doc, copy the change here too so the
bundle stays current. The scripts under `skills/workflow-design/scripts/` are the running machinery (gate,
dispatcher); they read `docs/TASK_TYPES.md` from the repo they run in.
