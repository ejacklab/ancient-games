---
agents: [all]
kinds: [command]
commands: ["jq", "python3 -c", "python -c", "node -e"]
from: runs/20261017-workflows/insight.md#F-3caba088
---
Before parsing a tool's output file, print its top-level keys (one command), then write the parse against what is
there, never against an assumed shape.
