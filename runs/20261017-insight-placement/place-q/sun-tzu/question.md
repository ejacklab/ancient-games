# Question — where do lessons live, and how do they reach each agent?

A time-boxed question: the owner (EJ) gave 20 minutes and wants two suggested versions at the end; the main agent
writes the versions from your advice, and the owner chooses. Answer within about 10 minutes of work.

Rules for this question:
- Rest each point on a fact below or one you check in this repository; a point from memory only is labelled *recall*
  and does not decide alone.
- Say "I don't know" where the facts do not answer.

## The rule already decided
When an insight is written, its **lesson** is filed at agent level — for one agent type (the main Claude agent,
opencode, Codex, agy, mcode, dsh) or for all agents — where every project's agents read it. The **project-specific
facts** stay in the project, kept with the code they are about. Example: F-682702da (the skill export skipped a
reference file) — the lesson "an export or bundle test checks every file the bundle names exists" travels; "this
repo's `tools/export_skills.py` treats requirement-check as one file" stays.

## Facts (verified 2026-10-17 unless marked)
- Insights today live per run: `runs/<run>/insight.md`, with the owner's choices in `insight-decisions.md` beside it
  (`docs/HARNESS_REQUIREMENTS.md` R12.3). 56 sections exist (`runs/20261017-insight-level/insights.md`).
- Skill roots: `~/.claude/skills` (Claude Code) and `~/.agents/skills` (Codex and the DeepSeek Harness scan it —
  reported in `CLAUDE.md`). This repo's skills are linked into both (`ls -la ~/.claude/skills`: e.g.
  `requirement-check -> ~/dev/ancient-games/.claude/skills/requirement-check`). A skill loads when its description
  matches the task; it is not read on every task.
- opencode auto-rejects files outside the repo it runs in (exit 0, no work — the main agent's memory, observed twice).
  agy headless soft-denies shell and web reads. So an engine can be relied on to read only what is in its brief or its
  working repo.
- Every engine call is briefed by the main agent from a file (`runs/<id>/briefs/<name>.md`, template
  `docs/workflow-templates/node-brief.md`). The method says memory is delivered in the brief, never left for the
  worker to ask for (`docs/WORKFLOW_DESIGN_METHOD.md` §4).
- The main agent's own lessons today sit in Claude Code's per-project memory
  (`~/.claude/projects/-home-smoke01-dev-ancient-games/memory/`, 60+ files, an index loaded every session); other
  projects and other engines never see them.
- The harness-guard (`.claude/skills/workflow-design/guard/`) sees the path of every Write, Edit and MultiEdit call
  before it runs (PreToolUse) and can add a line to the agent's context; Bash writes are seen only as a command line.
- The code map (`code_map/`, an index of this repo's code by path) is designed, not built.
- This repository is public on GitHub (ejacklab/ancient-games); anything filed in it is public.

## The decision
1. **Where does the agent-level store live?** Options so far: (a) a user-global folder such as `~/.agents/insights/`;
   (b) in this repo, as a skill linked into both skill roots; or another you can defend. Say how one-type lessons are
   kept apart from all-agents lessons.
2. **What does "kept with the code they are about" mean?** Options so far: (a) a lessons file in the code's folder;
   (b) a comment at the line; (c) an entry in the code map by path; or another.
3. **How does a lesson reach the agent that needs it** — the main agent, and an engine that reads only its brief —
   before it repeats the mistake, without flooding every brief (the owner wants less noise)?

End with **your recommended version** in five lines or fewer: the store, the project place, and the delivery.
