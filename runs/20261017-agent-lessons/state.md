# State — run 20261017-agent-lessons

Request: "go, follow your picks, max 3 hours and 3 rounds" — build `~/.claude/plans/agent-lessons-version-b.md`.
Limit: 3 hours (deadline D-a3cd912c, 14:55 → 17:55) or 3 rounds, whichever first (method 3.8 item 14).
Criteria: `criteria.yaml` (C1–C10).

## Picks the owner told me to follow (from the plan)
- Lessons about commands are delivered where the guard already lints Bash (PreToolUse for Bash), by command word.
- A lesson is filed after the owner's choice of the insight's option.
- The settings change: shown to EJ as a diff, applied after EJ's yes (R12.3 as changed by EJ at 14:57: "a fix to a harness's config must get yes from the owner").

## Rounds
| Round | Pieces | State |
|---|---|---|
| 1 | P1 verify docs · P2 store + seeds · P3 `lessons for` · P4 guard PreToolUse context | start |
| 2 | crossed check on round 1 + fixes · P6 brief template + workflows · P7 move memory lessons | — |
| 3 | P8 planted-repeat delivery test · settings command for EJ · report | — |

## Provisional decisions
(none yet)

## Log
- 14:55 deadline started; P1 sent to a claude-code-guide agent.
- 15:04 P1 answered (claude-code-guide, hooks.md): additionalContext verified, added "alongside the tool result"; before-execution not in docs → delivery question to the six experts (delivery-q, running).
- 15:10 P2 store (.claude/skills/agent-lessons/, 3 seed lessons from chosen insights; guard/src/LESSONS.md, 3 facts), linked into both roots, exported with the bundle; P3 `lessons for`/`lessons check`; P4 hook (L5) as context, L6 pending. SPEC Round 18. Tests: round18-lessons 31/31, 3/3 planted breaks killed (nodes/mutants.txt); guard 1408? see next line; Python 1133.
- 15:10 flaky: 3 C17 tests (round3, process list) failed once while the experts' engines ran, passed on rerun — logged for the insight.
