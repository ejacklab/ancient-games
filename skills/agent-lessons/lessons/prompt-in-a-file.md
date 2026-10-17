---
agents: [all]
kinds: [engine-call]
commands: ["codex exec", "opencode run", "agy -p", "claude -p", "mcode exec", "dsh"]
from: memory prompt-in-a-file (2026-10-12)
---
Write an engine's whole prompt to a file and call the engine with a short fixed instruction that names it ("Read
<file> and do what it says"): a large argument breaks the 128 KB per-argument limit and invites shell-expansion bugs,
and the file is the exact text the engine got. For opencode name the path in the message; never use `-f`.
