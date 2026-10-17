---
agents: [all]
kinds: [engine-call]
commands: ["agy -p"]
from: memory agy-headless-traps (2026-10-13)
---
agy headless (`-p`): a tool that needs shell or web permission is soft-denied, and the run exits 0 with nothing on
stdout (the reason only on stderr); `--mode plan` answers with a plan, not the deliverable. A brief for agy says: no
shell commands, no URL fetches, the answer itself as the final message. Resume a run with `--conversation <id>`.
