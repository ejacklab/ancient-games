# 范蠡 (Fan Li) — Where lessons live and reach agents

## Answer
File agent-level lessons in a user-global store partitioned by agent type so they travel across projects, keep project-specific facts directly on the ground in the code's file or immediate folder, and deliver lessons to engine workers exclusively through targeted briefs while guarding the main agent just-in-time.

**Recommended Version:**
- **Store:** `~/.agents/insights/` partitioned into `all/` and per-engine directories (`claude/`, `opencode/`, `codex/`, `agy/`, `mcode/`, `dsh/`).
- **Project place:** Inline comments at sensitive lines, or a companion `lessons.md` in the code's immediate folder.
- **Delivery:** The main agent selects and injects matching lessons into the engine worker's brief; harness-guard alerts the main agent before writes.

## How I decided
1. **The agent-level store lives in a user-global directory.** My #16 quotes: 「計然之策七，越用其五而得意。既已施於國，吾欲用之家。」 (`quoted`). What has succeeded across the wider state is taken to the household; lessons meant for every project's agents must not remain confined inside one project repository. Furthermore, this repository is public on GitHub, whereas agent lessons across EJ's private or public projects belong in user-global space (`~/.agents/insights/`).
2. **One-type lessons are kept apart by directory partitioning.** My #14 quotes: 「四封之內，百姓之事，蠡不如種也。四封之外，敵國之制，立斷之事，種亦不如蠡也。」 (`quoted`). Different actors have distinct boundaries and duties. Facts show opencode rejects files outside its working repository, while agy headless restricts shell and web reads. Segregating the global store into `all/` and dedicated subdirectories per engine (`claude/`, `opencode/`, `codex/`, etc.) prevents one engine from reading rules that apply only to another.
3. **Project-specific facts stay directly on the ground.** My #3 quotes: 「時不至，不可彊生；事不究，不可彊成。」 (`quoted`). The code map is designed but not built; relying on an unbuilt index forces what has not matured. My #2 quotes: 「持盈者與天，定傾者與人，節事者與地。」 (`quoted`). Regulating affairs goes with Earth—the material ground. Project-specific facts must sit in the file itself as inline comments or as a companion `lessons.md` in that folder, encountered directly upon reading or editing the code.
4. **Engine workers receive lessons solely through their briefs.** My #14 quotes: 「四封之內，百姓之事，蠡不如種也。四封之外，敵國之制，立斷之事，種亦不如蠡也。」 (`quoted`). The engine worker acts on the immediate spot outside the borders and relies strictly on what is handed to it. Facts verify that opencode and agy cannot be relied upon to scan outside files, and the method states memory is delivered in the brief (`docs/WORKFLOW_DESIGN_METHOD.md` §4). My #18 quotes: 「審備則可以戰乎？」王曰：「巧。」 (`quoted`). The preparations must be examined before dispatch: the main agent filters global and project lessons by the worker's engine type and target paths, placing only matching items into the brief. (*proposed change to the pattern*: Add a standardized, filtered `## Lessons` block to `docs/workflow-templates/node-brief.md` that is populated during node briefing to eliminate noise).
5. **The main agent is alerted just-in-time.** My reading: The main agent operates across the whole project. Facts confirm the harness-guard sees every Write and Edit tool call before execution (PreToolUse). Having the guard inject relevant lessons when a guarded path is touched gives the main agent the lesson right when needed, avoiding constant context noise during planning.

## What I need to know
1. If engine briefs are generated programmatically by workflow scripts (such as `intake.js`), then lesson matching can be enforced by a deterministic script; if briefs are authored manually by the main agent, then delivery depends on the agent adhering to a briefing checklist.
2. If EJ works across multiple physical machines, `~/.agents/insights/` requires a git repository to sync; if work remains on a single machine, a standard local folder is sufficient.

## Costs and risks
1. Under my #16: Storing lessons in `~/.agents/insights/` removes them from `ancient-games` version control, risking loss or uncommitted drift if the user-global folder is not backed up.
2. Under my #14: Partitioning by engine type introduces maintenance overhead and misclassification risk; a lesson mistakenly put in `all/` can impose unnecessary constraints on engines unaffected by that issue.
3. Under my #3: Rejecting an unbuilt central code map in favor of local folder notes and comments disperses project knowledge across directories, making repo-wide review harder until a code map is built.
4. Under my #18: Examining preparations before dispatch requires the main agent to review applicable lessons before writing each brief, adding preparation time to every node run.

## How we would know I was right
1. An engine run (such as `opencode` or `agy`) briefed with a targeted lesson succeeds without repeating a recorded past failure (e.g., F-682702da) and without failing from external file access.
2. Measuring brief sizes shows that zero irrelevant lessons from other engine types or unrelated directory paths are included in worker briefs.
3. When the main agent attempts an edit on a sensitive path, harness-guard or the inline code comment surfaces the constraint before the change is executed.
