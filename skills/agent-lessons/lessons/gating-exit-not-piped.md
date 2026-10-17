---
agents: [all]
kinds: [command]
commands: ["git merge", "git push", "git commit"]
from: runs/20261015-score/insight.md#F-1e90a8e1
---
Never pipe a command whose exit gates the next step (`git merge … | tail -1 && …`): the pipeline's exit is the last
command's, so `&&` goes on after a failure. Print its exit (`; echo "exit $?"`) or use `set -o pipefail`.
