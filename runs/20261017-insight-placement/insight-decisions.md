# Insight decisions — run 20261017-insight-placement

The owner's choice for each section of `insight.md`, recorded by the agent. One entry per section.

## Brief fact 1 — I told the experts the guard sees every Write and Edit before it runs; it does not
- decision: option 1 (the agent's option) — each fact in an expert question carries its own label and the command or file:line that checked it; a fact with neither is marked *recall*
- owner's words: "version B , others follow your pick"
- date: 2026-10-17
- applied: `.claude/skills/six-experts/SKILL.md` (`--question-file`) and the Facts heading of the three question templates in `.claude/skills/six-experts/assets/questions/`

## Timer crash — `deadline wait` failed when the deadline was ended before it woke
- decision: option 1 (the agent's option) — after the sleep, if the deadline was ended, print "<id> ended before its deadline" and exit 0; with a test that ends a deadline while wait sleeps
- owner's words: "version B , others follow your pick"
- date: 2026-10-17
- applied: `guard/src/cli.ts` (wait), test "T3: CLI wait on a deadline ended while it sleeps" in `guard/test/round10-deadline.test.ts`, red first (`nodes/wait-ended.red.txt`); `guard/SPEC.md` T3
