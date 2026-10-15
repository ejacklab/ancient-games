# E1 — the 7 recorded traps through the hook handler (round 1, commit 59a81ff)

| Trap | Hybrid | Where |
|---|---|---|
| 1 codex exec without </dev/null | caught | PreToolUse |
| 2 parallel opencode starts | caught | PreToolUse, another opencode running |
| 3 opencode file outside the repo | not caught | PreToolUse |
| 4 agy soft-deny, exit 0 empty | caught | PostToolUse |
| 5 agy plan mode stops at a plan | not caught | PostToolUse (output non-empty) |
| 6 agy transient 502 at login | caught | PostToolUseFailure |
| 7 worktree refuses subagent heredoc writes | not caught | the refusal happens inside the harness; no hook payload of ours carries it |

hybrid caught: 4 of 7

Prediction: hybrid 5 of 7 (1,2,3,4,6), control 0 of 7. Measured: **4 of 7** — trap 3 missed: the outside path sits inside the quoted prompt ("Read /home/… and do what it says"), and the lint takes a quoted string as one word, so it never sees a word starting with /. Control (no guard): 0 of 7 on the Bash path, by construction.
