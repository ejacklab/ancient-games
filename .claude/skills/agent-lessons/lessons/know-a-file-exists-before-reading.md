---
agents: [all]
kinds: [command]
commands: [cat, head, grep, sed]
from: memory read-only-listed-paths (F-e82a6f58, F-4981093a, 2026-10-16)
enforced_by: harness-guard Round 13 (the read-missing hold)
---
Know that a file exists before reading it: read a step's status first, and the files it was meant to write in a later
call, once the status says they were written; to probe a file on purpose, guard the read.
