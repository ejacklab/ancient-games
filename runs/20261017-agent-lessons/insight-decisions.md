# Insight decisions — run 20261017-agent-lessons

The owner's choice for each section of `insight.md`, recorded by the agent. One entry per section.

## Lessons used up by subagents — the main agent got none
- decision: option 1 (the agent's option) — key the shown marks by session and agent (the payload's agent_id when there is one), so each agent gets each lesson once
- owner's words: "yes to settings, all follow your picks"
- date: 2026-10-17
- applied: `guard/src/hooks.ts` (lessonLines), `guard/src/lessons.ts` (marker files per session#agent), test "L5: each agent of a session gets a lesson once", red first (`nodes/agent-marks.red.txt`), commit c6b452f
- filed: none (a tool fix)

## F-0969936e — 范蠡's agy call answered nothing: a file read was auto-denied
- decision: option 1 (the agent's option) — a file an expert question or brief cites lives inside the repo: copy an outside source into the run folder and cite the copy
- owner's words: "yes to settings, all follow your picks"
- date: 2026-10-17
- applied: `.claude/skills/six-experts/SKILL.md` (`--question-file`)
- filed: `.claude/skills/agent-lessons/lessons/cite-files-inside-the-repo.md`

## F-c64c0bbb — criterion C4 not met: it named the mechanism, and the design changed
- decision: option 1 (the agent's option) — a criterion names the outcome, never a mechanism an open question of the run still decides
- owner's words: "yes to settings, all follow your picks"
- date: 2026-10-17
- applied: the lesson below, given before a write to a criteria file
- filed: `.claude/skills/agent-lessons/lessons/criteria-name-outcomes.md`
