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
- 15:10 P2 store (.claude/skills/agent-lessons/, 3 seed lessons from chosen insights; guard/src/LESSONS.md, 3 facts), linked into both roots, exported with the bundle; P3 `lessons for`/`lessons check`; P4 hook (L5) as context, L6 pending. SPEC Round 18. Tests: round18-lessons 31/31, 3/3 planted breaks killed (nodes/mutants.txt); guard 1408; Python 1133.
- 15:10 flaky: 3 C17 tests (round3, process list) failed once while the experts' engines ran, passed on rerun — logged for the insight.
- 15:25 round 2 part 1: L6 provisional = hold once (delivery-q: five of six; Dario: context); P6 node-brief Lessons section, six_experts.py lessons per engine (3 tests), crossed-build-check refuses a brief without Lessons (harnesses pass); P7 16 memory notes → 15 lesson files (17 in store), memory index pointer agent-lessons-store; Python 1136; crossed check on round 1 running (wf_e1507bdd-867).
- 15:28 found: the live Bash hook (installed PreToolUse Bash runs this repo's cli.ts) marked 7 lessons shown for this session — engine, node and read lessons, the commands the crossed-check workflow's agents ran — and the main agent got no hold (my reading: subagents' calls reach the hook under the parent session id). Logged in insight.md; docs check on subagent fields sent.
- 15:33 docs: a subagent's hook input has agent_id (hooks reference). Provisional (insight option 1): shown marks keyed <session>#<agent_id or main>; test red first (nodes/agent-marks.red.txt). Live: the main agent's next Bash call was held (the first real delivery, before the call ran) — by an enforced lesson's pointer only, which was noise. Provisional: an enforced lesson never holds a call; lessons for still lists it (test red first, nodes/enforced.red.txt). Guard 1449/1449.
