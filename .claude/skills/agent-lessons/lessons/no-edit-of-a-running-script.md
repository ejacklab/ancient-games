---
agents: [all]
kinds: [code-edit]
paths: ["**/*.sh", "**/*.bash"]
from: runs/20261015-ts-hybrid/insight.md#F-f44538b2
---
Never edit a script while a background run is executing it: bash reads a script as it runs, so the running copy reads
half of the new text and fails ("unexpected EOF"). Write the new version to a new file and switch between runs.
