# Lessons about this folder's code

Project facts (guard SPEC Round 18, L2): what an insight taught about these files. Lessons for agents in any project
live in `.claude/skills/agent-lessons/lessons/`.

- `hooks.ts` — ownFailureSpec: D2's guard-query exemption (F1) must not swallow a test run's exit; a call that holds a test run is never exempt (runs/20261017-round17-crossed/insight.md#review-finding-1).
- `traps.ts` — segments(): a command that opens a `( … )` group takes the separator before the group, so `pytest | (cat)` is piped (Round 17, crossed review finding 4).
- `cli.ts` — deadline wait: the deadline may be ended while wait sleeps; read it again after the sleep (runs/20261017-insight-placement/insight.md#timer-crash).
