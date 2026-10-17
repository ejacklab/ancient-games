# State — run 20261016-time-monitor (time-boxed, method 3.8 item 14)

Request: "you got an hour, build them in test them and optimise them" (the three time monitors), then: workers return
status reports with a timestamp; always divide the task into small pieces.
Start 2026-10-16 10:22:01 +0800 · **deadline 11:22:01 +0800** · background timer fires 11:17 (way 2, dogfooded).

## Pieces
| # | Piece | State |
|---|---|---|
| P1 | spec (guard Round 10) | — |
| P2 | deadline module + CLI | — |
| P3 | hook reminders | — |
| P4 | progress files + status | — |
| P5 | brief template + four-experts timestamps | — |
| P6 | tests (Codex from spec) + mutants | — |
| P7 | optimise: hook cost per call | — |
| P8 | report, commit | — |

## Provisional decisions (item 14; the owner accepts or declines at the end)
- **D1 How often the guard adds the time:** (B) a one-line `harness-guard clock:` status after every tool call, plus the
  fuller `harness-guard time:` block with the workers' progress at 50/80/100%, and time-up on every call after the
  deadline. Reason: every tested design shows the budget at every step, a budget given once fails
  (`research/reminders.md` F1, F3, F5, F6, F8); no source tested marks-only. Experts (`experts/`): Linus, 范蠡, 孫子,
  老子 all advise B; 孫子: hold B to the measured hook cost (C6). Dave (rerun after F-173e0190): B, "treat it as the
  starting setting… test (A) later as a separate arm".
- **D2 Which tools carry the clock:** every tool after a call (install `--print` without a matcher), not only Bash and
  writes. Reason: the review showed Read/Grep/web calls would never see the clock (finding 3); one hook run measured
  0.02 s. Applying it to the installed settings is the owner's (harness config).

## Log
- 10:22 start; criteria written.
- 10:2x research F1–F8 saved; experts 4/5 answered B; Dave's claude call empty (runner bug, fixed, rerunning); round 10 code + Codex tests 42/42 after integration; guard 1257/1257.
- 10:3x review: 10 findings, all fixed or answered (review-answers.md, 6105656); deadline end added; guard 1264/1264, Python 1083; report written.
- 2026-10-17T01:32Z D1 accepted as clock only, marks removed. Question (main agent's, above): how often the guard adds the time; option (B), written by the main agent from the experts' advice: a one-line clock after every call plus a fuller block with the workers' progress at 50/80/100%, time-up after the deadline. EJ, during run 20261017-workflows: "I prefer clock more than the 50% 80% and 100%", the marks being "not able to well predict, specific when exploring solutions". The clock line and the time-up line stay; the 50/80/100% block, `--marks` and the raised mark records were removed in guard commit 07b67a9; workers' progress is read with `deadline status`.
- 2026-10-17T01:32Z D2 declined. Question (main agent's, above): which tools carry the clock; the main agent's choice: every tool (no matcher). EJ, during run 20261017-workflows: "guard watches back to bash and file writes only" — the after-call hooks stay on PostToolUse "Bash|Write|Edit|MultiEdit" and PostToolUseFailure "Bash". The owner TODO below is closed: the installed `~/.claude/settings.json` already has those matchers (read 2026-10-17T01:32Z).

## TODO (owner)
- [x] (closed 2026-10-17: D2 declined, the installed matchers stay) **Update the installed hooks in `~/.claude/settings.json`** so the clock reaches every tool: replace the
  harness-guard hooks with the output of `bun .claude/skills/workflow-design/guard/src/cli.ts install --print
  claude-code` (PostToolUse and PostToolUseFailure lose their `matcher`). Back up the file first. Parked by the owner
  2026-10-16 to brainstorm a new idea first.
