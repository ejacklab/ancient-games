---
agents: [all]
kinds: [brief]
paths: ["runs/*/*question*.md", "runs/*/briefs/*.md"]
from: runs/20261017-insight-placement/insight.md#brief-fact-1
---
Each fact in a question or brief for another agent carries its own label and the file:line or command that checked
it; a fact with neither is marked recall. One "verified" label over a block of facts hides a recalled one.
