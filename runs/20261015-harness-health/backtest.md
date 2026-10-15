# Backtest — the seven recorded harness traps (scored on paper, 2026-10-15)

Prediction (`prediction.md`, written before the probe code): **0 of 7**. Control (plain `readiness.py`): 0 of 7.
Traps as listed by Dave (`experts/answers/dave.md`), from this project's memory notes. "Flagged" means a line in
`harness_health.py`'s output names the trap's cause before dispatch. Scored by the main agent by reading the built
probes against each trap — *my reading*, not a run on fixtures that reproduce each trap.

| # | Trap | Kind | harness_health output | Flagged |
|---|---|---|---|---|
| 1 | `codex exec` hangs when stdin is not `</dev/null` | behaviour | no line about stdin | no |
| 2 | parallel opencode starts → "database is locked" | behaviour | no line | no |
| 3 | opencode auto-rejects files outside the repo, exit 0, no work | config + behaviour | `opencode · permissions and sandbox · unknown` | no — the line says the format is unverified, not the cause |
| 4 | agy soft-denies shell / read_url, exit 0, empty output | config + behaviour | `agy · permissions and sandbox · unknown` | no — same |
| 5 | agy `--mode plan` stops at a plan | behaviour (a flag) | no line | no |
| 6 | agy transient 502 at login | behaviour | no line | no |
| 7 | worktree isolation refuses subagents' heredoc writes | behaviour | no line | no |

**Result: 0 of 7, as predicted.** The prediction held; Dave's wider bound (≤2 for config probes in general) also holds.

What this shows: what the built check finds — no deny list, no sandbox setting, approval policy unset, the bypass prompt
skipped — is a different class from the failures this project has actually hit, which are behaviour at dispatch.
What it does not show: whether the guardrail findings would have prevented any incident — none recorded here was a
guardrail failure. *My reading:* traps 3 and 4 would become flaggable once the opencode and agy formats are verified,
and the other five only by a canary (EJ's question Q2) or a trap catalogue with its fix as the help (Q6).
