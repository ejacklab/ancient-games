# The ten harness requirements — as pasted by EJ, 2026-10-15 (outside source, author unknown)

A harness at its best covers these ten requirements:

1. Clear context delivery. Give the agent a short, durable instruction file (AGENTS.md or CLAUDE.md) plus skills and docs it can pull on demand. Treat the context window as a budget, not a dumping ground.
2. Well-designed tools. Tools should have simple, unambiguous interfaces, error messages that tell the agent how to fix the call, and explicit boundaries on what each can do.
3. Planning and task structure. Break work into a feature list or task list with clear done-criteria, so the agent doesn't declare victory early.
4. State and memory across sessions. Use progress files, checkpoints and clean handoffs so a fresh context window can resume where the last one stopped.
5. Independent verification. Run tests, linters and a separate evaluator agent so the builder doesn't grade its own work. Completion should mean evidence, not a claim.
6. Guardrails and permissions. Add sandboxing, least-privilege tool access, hard policies for risky actions and defenses against prompt injection.
7. Recovery and retries. Make steps idempotent, with rollback points and sensible retry limits, because production agents will fail.
8. Human-in-the-loop gates. Define when a human approves or decides, so people handle only the calls that need judgment instead of micromanaging.
9. Observability. Log every action, token and cost, decision point and anomaly, so you can debug and see where the agent drifts.
10. A feedback loop that improves the harness. Every agent mistake becomes a permanent fix (a rule, a check, a better tool). Review the harness as models improve, since some scaffolding exists only to compensate for today's model weaknesses.
