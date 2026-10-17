---
agents: [all]
kinds: [engine-call]
commands: [codex]
from: memory codex-config-key-check (2026-10-15)
---
To prove a Codex config key's name without spending quota, run `codex -c 'key="bogus"' login status </dev/null`: a
real enum key answers "unknown variant", listing its values; a misspelled key is accepted silently.
