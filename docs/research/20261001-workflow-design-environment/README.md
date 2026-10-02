# Research — the workflow-design environment, 2026-10-01

One working session (EJ + assistant) researching what the workflow-design skill designs *for*: the state of
skills as a standard, the tools on this machine, what Claude Code natively supports, the known execution
patterns, and how many copies of the method's algorithm exist. Written down before any of it is built on,
per method §4: stored knowledge carries a date and is rechecked before it is relied on.

## Files

| File | What it holds | How it was obtained |
|---|---|---|
| `SKILLS_OPEN_STANDARD.md` | SKILL.md as an open standard, ~40 tools, progressive disclosure, the skills/tools/scripts stack | web research (reported) + local checks (verified) |
| `TOOL_INVENTORY.md` | what is installed and logged in on this machine, and what stays unknown | local read-only commands (verified); no quota spent |
| `CLAUDE_CODE_CAPABILITIES.md` | subagent limits, five parallel mechanisms, CLI surface, hooks | official docs via search agent (reported) + local `claude --help` on 2.1.286 (verified) |
| `EXECUTION_PATTERNS.md` | the well-known ways to execute agent work: topology × routing authority × trigger | web research (reported) + `20260919-state.md` (local) |
| `ALGORITHM_COPIES.md` | census: how many copies of the workflow-design algorithm exist and where they drift | local file reads (verified) |
| `OPEN_QUESTIONS.md` | every decision proposed this session and not yet made by EJ | session record |

## Status legend (house rules)

- **verified** — a command run on this machine on 2026-10-01 proved it.
- **reported** — a source claims it (web results are untrusted external content; docs may lag the installed
  version). Recheck before relying.
- **n=0 / n=1** — how many real runs back a rule or number.

Nothing here is committed to the method, the skill or EXECUTOR_KINDS yet; see `OPEN_QUESTIONS.md` for what
is proposed and waiting on EJ.
