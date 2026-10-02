# Digest — Claude Code mods and plugins (2026-10-02)

Full findings: `FINDINGS.md` (same folder). Status: **parked by EJ** — skip for now.

**Answer.** A mod is a plugin whose JS/TS hooks run inside the Claude Code process (panes, status line, toasts, tool-call rewrite or deny). Added in Claude Code 2.1.287 (2026-10-01), on by default; the local `plugin-authoring` skill still calls the API early access.

**Confidence.** Local skill facts verified by reading the skill and the type declarations; web facts partly *reported* (a summarizing fetch tool), so re-read hooks, skills, sub-agents and changelog pages raw before building.

**Cautions.** A mod runs with the user's full permissions, unsandboxed, and sees every prompt and tool call. Hooks and mods run only inside Claude Code; Codex, agy and qwen nodes never run them, so any rule that must hold across engines stays a script plus the state file.

**Ranked fit to the method (value over cost).** 1 package `workflow-design` as a classic plugin (critic: do a one-hour compatibility check first); 2 gate-on-write hook for `design_gate.py` (critic: below the status line until the hook-to-model path is verified); 3 status line from `state.md`; 4 blueprint guard (none until a skipped-blueprint incident is logged); 5 readiness at `SessionStart` (use a slash command instead); 6 cost hook (premature); 7 live pane (premature). Critic's extra option: do nothing and log one skipped-step incident.

**Verify first.** How a classic hook's script result reaches the model (raw hooks page plus one throwaway run); what the installed Codex plugin's Stop hook does (timeout 900); whether mods load in the CLI inside WSL2 and in headless `claude -p`.

**Decision it triggers.** None now (EJ: skip). Reopen if a script is skipped in a real run.
