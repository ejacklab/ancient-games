# Prediction — written before any probe code (Dave #3)

**Metric.** Of the seven recorded harness traps (Dave's list in `experts/answers/dave.md`), how many would the built
`harness_health.py` flag before dispatch, on a setup that reproduces each one.

**Control.** Plain `readiness.py`: 0 of 7 (it probes no permissions or behaviour).

**Prediction (main agent).** 0 of 7. Dave predicted ≤2 of 7 for config probes in general; this build probes only
Claude Code and Codex config, and the two config-dependent traps are opencode's allowed paths (#3) and agy's allow
rules (#4), whose formats stay `unknown`. Trap #1 (codex stdin hang) is not a config setting. If it flags any trap, the
prediction is wrong and the report says so.

**Stop.** Scored in step 6 of `workflow-design.md`, before the independent review.
