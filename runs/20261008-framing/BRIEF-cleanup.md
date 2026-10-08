# Update CLAUDE.md: one framework, two parts, one loop

Read the three experts' framing verdicts in `runs/20261008-framing/` (`claude.md`, `minimax-m3.1-flash.md`,
`deepseek-v4-pro.md`). They all agree: the current `CLAUDE.md` wrongly splits the project into "the main product is
`.claude/skills/workflow-design/`" and, separately, "`ancient_games/` — the framework".

Fix `CLAUDE.md` only, and only as follows:

1. Replace the "The main product is ..." line with the one-framework sentence (merged from the three experts):
   "The Ancient Games is one framework for agent work: the workflow-design method (`.claude/skills/workflow-design/`)
   is the part that turns an incoming task into a designed workflow, and `ancient_games/` is the part that referees
   the work, with the referee's findings feeding back into the method."

2. Update the `ancient_games/` bullet in "The knowledge here" so it reads as **a part** (the referee), not "the
   framework".

3. Keep the harness-root symlink detail (`~/.agents/skills/...`, `~/.claude/skills/...`) as its own following
   sentence, not crammed into the main sentence.

4. **Do NOT touch the "Working with EJ here" section.** The requirement-check (eight questions), the two rules
   (never fill a gap, never add structure), "ask only what changes the shape", "who is this for", and "evidence lives
   in the project" are EJ's own words and stay verbatim.

5. A light consistency pass over "What this folder is for" and "The knowledge here": fix any phrasing that still
   implies two separate products. Do not add new content, rules, or sections.

Print a summary of exactly what you changed, line by line.
