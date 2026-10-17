---
agents: [all]
kinds: [engine-call]
commands: [codex, opencode, mcode, agy, dsh, claude]
from: memory engine-calls-need-dev-null (2026-10-12)
---
Give every headless engine call stdin from /dev/null (`< /dev/null`): `codex exec` reads stdin whenever it is not a
TTY, even with the prompt as an argument, and a background call then hangs until the outer timeout with no output.
