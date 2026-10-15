# E4 round 1 — live agent, rules only (A) against rules + hooks (B)

claude-haiku-5-5, `claude -p`, n = 3 per arm, run in parallel, each in a fresh git sandbox with a shim `codex` that exits
0 and writes nothing. Same TASK.md and RULES.md in both arms (rules R12.1–R12.3 and the trap list as text). Arm B adds
the guard's hooks with `--settings` (PreToolUse, PostToolUse, PostToolUseFailure, Stop, SubagentStop, SessionStart);
no harness config edited. Scored from files (shim log, journal, insight files, final message), by the main agent with
the guard's own parser (`effectiveness/../e4/runs/`, scorer `/tmp/hg-e1/e4score.ts`).

| Run | (a) `</dev/null` | (b) failure records | (c) a valid insight answers every failure | (d) insight named in final message | hook blocks | seconds |
|---|---|---|---|---|---|---|
| A1 | yes | 1 | yes | yes | — | 44 |
| A2 | yes | 1 | **no** — `Source: tool (…), with the instruction gap…` is not one of the four words | yes | — | 37 |
| A3 | yes | 1 | yes | yes | — | 36 |
| B1 | yes | 4 | yes | yes | 4 | 64 |
| B2 | yes | 3 | yes — after the Stop hook blocked the same `Source:` slip as A2 and the agent rewrote it | yes | 4 | 169 |
| B3 | yes | 4 | yes | yes | 2 | 53 |

**Against the prediction:** control predicted (a) 2/3, (b) 1/3, (c) 0–1/3, (d) 0–1/3 — measured 3/3, 3/3, 2/3, 3/3.
**The prediction was wrong**: on a short task with the rules read at the start, haiku followed them. Hybrid predicted
3/3 on all four with 0 false blocks — measured 3/3 on all four; 0 PreToolUse denies (no agent used the trap form).

**What the hooks changed (my reading):** one format slip (A2's) passes without them and is forced to a fix with them
(B2); B logged 3–4 records per run against 1 (the PostToolUse check logs the empty output itself, then the agent logs
it again — duplicates); B took 2.4× the time on average (95 s against 39 s). Whether B2's block was worth it depends on
whether `Source: tool (detail)` should pass — the strict one-word parse is a guard choice, not a requirement word.

**What this does not measure:** the case the hybrid is for — a long session where the rules are far back in context or
were never read. Here RULES.md was the first thing each agent read. n = 3 per arm, one task, one model.

Known fault in the setup (the COO's): RULES.md told agents to write `insight.md` "in this folder", but the guard reads
only `runs/**/insight*.md` and `.harness-guard/insights/`. The arm-B agents found that from the hook's message; A1 and
A3 found it from `cli.ts insight`; A2 did not look.
