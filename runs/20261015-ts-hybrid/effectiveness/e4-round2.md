# E4 round 2 — rules present in the folder but not named by the task

Same as round 1 except TASK.md no longer says "Read RULES.md" (RULES.md is still in the folder). claude-haiku-5-5,
n = 3 per arm, in parallel. Prediction (committed before the run, `prediction.md` addendum): arm A 0–1/3 on (a), 0/3
on (b)–(d); arm B 3/3 on all.

| Run | (a) `</dev/null` | (b) failure records | (c) valid insight answers every failure | (d) named in final message | Stop blocks | seconds |
|---|---|---|---|---|---|---|
| A1 | yes | 2 | yes | yes | — | 59 |
| A2 | yes | 1 | yes | yes | — | 39 |
| A3 | yes | 1 | yes | yes | — | 41 |
| B1 | yes | 3 | yes | yes | 4 | 203 |
| B2 | yes | 4 | yes | yes | 1 | 72 |
| B3 | yes | 3 | yes | yes | 5 | 839 — killed by the 900 s outer timer (exit 124) |

**Against the prediction: wrong again for arm A.** All three arm-A agents listed the folder, found RULES.md on their
own, and followed it — including the guard CLI for logging and `insight` for checking. (The "blocks" counted in A
transcripts are the CLI's own `insight` output, not hooks.) Arm B: 3/3 as predicted.

**Cost of the hooks:** B took 203 / 72 / 839 s against A's 59 / 39 / 41. B3: after the first Stop block the agent ran
`find /` (moved to the background after 120 s), then a command that wrote the insight and ran `cli.ts insight`, which
also passed 120 s and went to the background; its final answer was at 09:04:47 and the process was killed at the 900 s
timer, 9 minutes later — *my reading:* the session waited on the backgrounded command. Re-running `cli.ts insight` in
that sandbox afterwards took 0.02 s, so the 120 s stall is **not reproduced and its cause is not established**.

**What rounds 1 and 2 show together (my reading, n = 6 per arm, one short task, one model):** when the rules are in
the working folder, haiku finds and follows them; the hooks add correctness only at the margin (a format slip, round 1
A2) and cost time — sometimes a lot (B3). The case where hooks should matter most — rules nowhere in reach, or a long
session where they are far back — is still not measured. The block message also sent B agents searching for where
insights go (`find /`) — the message should say the exact path to write.
