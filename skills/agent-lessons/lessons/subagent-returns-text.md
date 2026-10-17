---
agents: [claude-main]
kinds: [brief]
from: memory subagent-report-files-refused (F-c60edad6, 2026-10-16)
---
A Claude Code subagent's Write of a report file can be refused ("Subagents should return findings as text"): ask a
researcher subagent for its digest first and its full findings as text after it, and save them yourself. For a
read-only caller of bun, set `BUN_RUNTIME_TRANSPILER_CACHE_PATH=0`, or bun writes a cache under HOME.
