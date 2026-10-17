# Linus Torvalds — Where lessons live and reach agents

## Answer

My recommendation is a user-global lesson store, separated into all-agents and engine-specific lessons, with project facts versioned in the project and indexed by the code paths they concern. The main agent selects lessons before acting and embeds their operative text in each worker’s brief; storing a lesson alone does not deliver it.

## How I decided

1. **Check what remains undecided — my reading.** Applying requirement-check separately to lesson placement and project-fact placement: **pass** one thing, unit, can it fail, basis and links; **FAIL** who decides, weak words and level. The implementation still needs a decider for audience and relevance, a concrete meaning for keeping facts with code, and a distinction between advice and binding rules. My provisional choices follow below; they do not replace EJ’s decisions.

2. **Choose the data before the delivery mechanism — my #9.** Use `~/.agents/insights/all/` and `~/.agents/insights/<agent-type>/`, with one canonical record per lesson. Record its trigger, lesson, source finding and decision status. The main agent proposes audience and applicability; EJ’s recorded choice governs an adopted fix. This preserves the separation between proposals and chosen fixes in [R12.3](/home/smoke01/dev/ancient-games/docs/HARNESS_REQUIREMENTS.md:59). The supplied brief establishes that current Claude project memory misses other projects and engines. A skill linked into two roots still depends on activation, so I would not make it the delivery guarantee.

3. **Use the project’s documented storage format — my #13 and my #5.** My reading of keeping facts with code is: version them in the same repository, name the affected paths, and review them when those paths change. The existing [memory design](/home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md:53) already provides entries with `covers` and evidence. Use that format where adopted; retain existing project files during the documented transition. Comments can explain a local constraint, but I would avoid duplicating the historical record in comments and a folder lessons file. A code map can later index these records without becoming another authoritative copy.

   F-682702da demonstrates why dates matter: the historical failure was omission of a reference file, but the current [exporter copies reference directories](/home/smoke01/dev/ancient-games/tools/export_skills.py:150). A project record should preserve the failure and fix, rather than teach that the old defect still exists.

4. **Deliver a self-contained instruction — my #11 and my #18.** Before their own task, the main agent consults the global index and reads records matching the task operation and their agent type, plus applicable project records. Before dispatch, they repeat selection for the worker’s type and task, then embed the lesson’s ID, operative instruction and check in the brief. An external path alone cannot serve a worker limited to its brief. This follows [method §4](/home/smoke01/dev/ancient-games/docs/WORKFLOW_DESIGN_METHOD.md:591). All-agents describes audience; it does not mean every lesson belongs in every brief.

5. **Separate existing capability from proposed protection — my #2 and my #7.** The supplied guard fact conflicts with checked-in code: [installation registers PreToolUse for Bash](/home/smoke01/dev/ancient-games/.claude/skills/workflow-design/guard/src/install.ts:26), and [the handler returns immediately for other tools](/home/smoke01/dev/ancient-games/.claude/skills/workflow-design/guard/src/hooks.ts:105). Write/Edit/MultiEdit appear after use. That does not establish prevention before a file edit.

   **Proposed change to the pattern:** add explicit lesson selection before main-agent execution and worker dispatch. If a worker discovers work outside its brief’s scope, the main agent refreshes the brief before that work proceeds. This adds a delivery step; its reliability is **not measured**.

## What I need to know

- Which startup instruction mechanism is actually loaded across projects for each main-agent harness? If none is verified, global delivery remains conditional on installing and checking that entry point.
- What omission rate and added context does EJ consider acceptable? I do not know; no noise or coverage target was supplied.

These remain questions for the main agent’s provisional versions within this time box.

## Costs and risks

- **My #9:** A global store needs distribution and maintenance across machines. It also needs care when private lessons enter a public project brief.
- **My #5 and my #13:** Path-indexed project records avoid a new storage system, but path renames and stale facts require maintenance.
- **My #11 and my #18:** Selection reduces unrelated text but can miss a lesson. Brief snapshots can also become stale during a long task.
- **My #2 and my #7:** Startup instructions and reminders provide no demonstrated guarantee that an agent applies the lesson. I cannot claim prevention from placement alone.

## How we would know I was right

My proposed check, **not run and not independent evidence**, is to replay F-682702da in a disposable fixture from a different project. Test both a fresh main-agent session and a worker given only its brief. Observe whether the export lesson arrives before action and whether a deliberately missing named reference is detected. Include an unrelated task and a lesson for another engine to expose unnecessary delivery.

Measure omitted applicable lessons, irrelevant lessons delivered, added context, selection time and repeated failures. Passing this replay would establish that case, not universal recall.

**Recommended version — provisional:**

- **Store:** `~/.agents/insights/all/` and separate agent-type directories, with triggers and source IDs.
- **Project place:** versioned project records with explicit code-path coverage; comments only for local explanations.
- **Delivery:** verified main-agent startup entry point, selection before work, and selected lesson text embedded in worker briefs.