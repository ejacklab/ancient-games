A decision for the harness (a real one, not a test question): **what should a pre-flight check verify in a question
file or a worker brief before it is handed to an AI engine** (Claude, Codex, opencode/MiniMax, dsh/DeepSeek,
agy/Gemini)?

Facts:
- A brief or question is a Markdown file the main agent writes; the engine is told "read <file> and do what it says".
  Runners: `.claude/skills/six-experts/scripts/six_experts.py` (expert questions) and the CLI calls in
  `docs/EXECUTOR_KINDS.md` (worker briefs). The brief template: `docs/workflow-templates/node-brief.md`.
- A check here means a script that runs before the engine starts, with no AI call, and either passes or fails the file
  (it can fail; it never fixes the file itself).
- The check costs time on every engine call, so each thing it verifies should pay for itself.

The decision: list what the check should verify (each item: what it looks for, how a script can tell, and the failure
it prevents), in order of value, and what it should deliberately not verify. Say how we would know the check helped.
