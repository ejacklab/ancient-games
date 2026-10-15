# E1 — round 2 (after round 3 code, commit 2c1af3d)

| Trap | Hybrid | Where |
|---|---|---|
| 1 codex exec without </dev/null | caught | PreToolUse |
| 2 parallel opencode starts | caught | PreToolUse, another opencode running |
| 3 opencode file outside the repo | caught | PreToolUse |
| 4 agy soft-deny, exit 0 empty | caught | PostToolUse |
| 5 agy plan mode stops at a plan | not caught | PostToolUse (output non-empty) |
| 6 agy transient 502 at login | caught | PostToolUseFailure |
| 7 worktree refuses subagent heredoc writes | not caught | the refusal happens inside the harness; no hook payload of ours carries it |

hybrid caught: 5 of 7

Prediction 5 of 7 (1,2,3,4,6) — **held** after the enhance round (round 1 measured 4: trap 3 now caught, C21). Traps 5 and 7 stay out of reach: 5 needs the call to declare its expected shape (plan mode is also used on purpose), 7 happens inside the harness.
