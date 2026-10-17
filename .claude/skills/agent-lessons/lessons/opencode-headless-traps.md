---
agents: [all]
kinds: [engine-call]
commands: ["opencode run"]
from: memory opencode-parallel-db-lock (2026-10-13)
---
opencode headless: several `opencode run` calls started together can fail with "database is locked" (exit 1, empty
output), so start them one at a time and check every exit code; and a file outside the repo it runs in is
auto-rejected, the run exiting 0 with no work done, so copy its inputs into the repo first. A command with an
absolute path can be rejected the same way even when the path is inside the repo (`external_directory`), so a brief
for opencode says: relative paths only, never `cd` to an absolute path.
