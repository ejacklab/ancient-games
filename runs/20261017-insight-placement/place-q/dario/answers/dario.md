# Answer — where lessons live and how they reach each agent

## Answer
Keep the lessons in a user-global store at `~/.agents/insights/`, with one file per agent type plus one for all agents. Keep project facts as `covers:`-tagged entries in the project's `project-memory/`. Deliver lessons by adding to the brief only the few lessons that match the node's task, and let a PreToolUse guard hook warn the main agent.

## How I decided
1. **The store has to be outside the repo.** The repo is public, and lessons carry the owner's habits, so they shouldn't be published. The existing memory design already puts agent and user memory in the home folder, not in the repo (`docs/memory-system/SOURCE_OF_TRUTH.md:23`). That points to option (a).
2. **A skill linked into both skill roots (option b) fits badly.** A skill loads only when its description matches the task (your fact). A lesson has to arrive when the task is about to repeat a mistake, not when the task sounds like the skill. Putting it in the public repo also publishes it. I have not checked whether a skill can hold per-engine files.
3. **One-type lessons stay apart from all-agents lessons by file name.** Use `all.md`, `claude.md`, `opencode.md`, `codex.md`, `agy.md`, `mcode.md` and `dsh.md`. Each lesson is a short entry with a one-line trigger, such as "when writing an export or bundle test". An engine reads `all.md` plus its own file. No tags or code are needed.
4. **"Kept with the code" should be a `covers:` entry in the project's `project-memory/`.** The existing memory design already gives an entry a `covers` header (the code paths it is about), and an agent reads the entries covering a file before editing it (`SOURCE_OF_TRUTH.md:54`, `:129`; method §4 table, Contract row). So the project fact, such as "`tools/export_skills.py` treats requirement-check as one file", goes there. It is also the same mechanism as option (c), the code map by path. The code map is not built, so this one doesn't need to wait for it.
5. **A comment at the line (option b) is the weakest.** It only helps an agent that opens that file. It also mixes the project fact into the code.
6. **A lessons file in the code's folder (option a) duplicates `project-memory/`.** It would need its own index, which `project-memory/INDEX.md` already provides.
7. **Delivery to an engine that reads only its brief.** The main agent writes the brief from a file. The method already says memory goes in the brief and is not left for the worker to ask for (method §4, "Context — memory in"). So the main agent picks lessons by matching the node's task against the triggers in `all.md` and the engine's file. It puts only those into the brief's Context section, with the entries from `project-memory/` whose `covers` match the paths. This keeps the brief small. opencode cannot read `~/.agents/insights/` at all (it auto-rejects files outside its repo), so the lessons have to be copied into the brief.
8. **Delivery to the main agent.** Today it sees only the memory index loaded at session start. I would add a guard rule. When a Write or Edit path matches a lesson's trigger, the hook adds that one lesson to the agent's context. The hook can see every Write, Edit and MultiEdit path before it runs, but sees Bash writes only as a command line, so Bash writes would be missed. I have not checked how much the hook can add, so this step depends on that.

## What I need to know
- Does the owner want lessons to travel to a second machine or a teammate? If so, a home folder won't do and the store needs a private repo.
- How much text can the guard hook add to the agent's context in one call? The delivery in step 8 depends on that.
- Who tags a lesson with its trigger, and when? If the trigger is blank or too broad, the matching in step 7 fails or floods the brief.
- Does `project-memory/` exist yet for this repo? The method says a product starts it when the first node writes an entry. Until then, project facts remain in `docs/blueprint/` or in the run's `insight.md`.
- Is the `.claude/agent-memory/<name>/` path from the memory design meant to hold these lessons? If so, this should use that path, not `~/.agents/insights/`.

## Costs and risks
- **The store is outside the repo.** It is not versioned or backed up with the code, and a fresh machine starts without it. The risk is higher if the owner never copies it.
- **Matching can miss.** A lesson with a poor trigger line never reaches the brief, and nobody notices because nothing fails.
- **Matching can flood.** Loose triggers put many lessons into every brief, which is the noise the owner wants less of.
- **Stale lessons.** A lesson stays in the home folder after its cause is fixed. The method says stored knowledge carries a date and is rechecked before it is relied on, so each lesson needs a date and an owner for rechecking.
- **The split can be wrong.** Whether a finding is a lesson (travels) or a project fact (stays) is a judgement call, and a wrong call either publishes a project fact in the shared store or hides a lesson in one project. F-682702da needed that split by hand.
- **The guard hook sees only some writes.** Bash writes are not covered.
- **Two delivery paths to maintain.** One goes through the brief, one through the hook.

## How we would know I was right
- **Replay test.** Take F-682702da and give the main agent and one brief-only engine a task that would repeat it, with the store holding only the lesson. Count how often the export or bundle test checks that every named file exists. Compare with the same task and no lessons.
- **Noise measure.** Count lesson lines in each brief over a week. If they average more than a few per brief, or the owner says the briefs are noisier, the triggers are too loose.
- **Split check.** Read 10 stored lessons and see whether any names a path, a file, or a repo-specific fact. Each one that does is a failed split.
- **Recommended version.** Store: `~/.agents/insights/all.md` plus one file per engine. Project place: `covers:`-tagged entries in `project-memory/`, with the code map added later. Delivery: the main agent puts the matching lessons into each brief, and a guard hook warns the main agent on a matching Write or Edit path.
