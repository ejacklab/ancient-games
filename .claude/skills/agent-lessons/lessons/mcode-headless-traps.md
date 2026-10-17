---
agents: [all]
kinds: [engine-call]
commands: ["mcode exec"]
from: memory mcode-headless-traps (2026-10-16)
---
mcode (MiniMax Code): call it by its full path, since only interactive shells put it on PATH. `exec --mode
lightweight` has no tools and cannot read `--file` attachments, so send the content on stdin with `--input -`;
`--permission off` lets it write. Inputs of tens of KB stalled (exit 4, "LLM request timed out") where a 9 KB brief
answered in 20 s.
