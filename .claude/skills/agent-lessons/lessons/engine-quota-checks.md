---
agents: [all]
kinds: [engine-call]
commands: [claude, agy, codex, opencode]
from: memory engine-quota-checks (2026-10-16)
---
To see an engine's quota before a long run: Claude Code, `claude -p "/usage" </dev/null`; agy, `agy -p "/usage"
</dev/null` (not in `--help`); Codex has no command — read the last non-null `rate_limits` in its newest session log
(`primary` 5-hour, `secondary` weekly); opencode shows only local totals (`opencode stats`), not what is left.
