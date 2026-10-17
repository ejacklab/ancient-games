---
agents: [claude-main]
kinds: [brief]
from: memory worktree-isolation-reaches-workflow-agents (2026-10-13)
---
After EnterWorktree, the isolation guard also refuses the subagents' shell heredoc writes, `HOME=…` prefixes and
writes to the main checkout — and an agent may not notice and report success. Briefs for those agents say "write files
with the Write tool", inside the worktree.
