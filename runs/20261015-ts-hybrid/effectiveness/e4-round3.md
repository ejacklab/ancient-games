# E4 round 3 — arm B again, after the round-3 code (C23 no duplicates, C24 the block names where to write)

Same setup as round 2 (rules in the folder, not named by the task), arm B only, n = 3, claude-haiku-5-5.

| Run | (a) | (b) records | (c) valid insight | (d) named | Stop blocks | `find /` | seconds |
|---|---|---|---|---|---|---|---|
| B1 | yes | 1 | yes | yes | 1 | 0 | 35 |
| B2 | yes | 2 | yes | yes | 0 | 0 | 50 |
| B3 | yes | 2 | yes | yes | 1 | 0 | 49 |

Round 2 arm B for comparison: records 3 / 4 / 3, blocks 4 / 1 / 5, 203 / 72 / 839 s (B3 killed at the 900 s timer).
Round 2 arm A (no hooks): 59 / 39 / 41 s.

**Against the prediction (committed before the run): held** — 3/3 on (a)–(d), blocks ≤ 2, fewer duplicate records,
every run under the slowest round-2 time, no `find /`. The hooked arm now runs as fast as the rules-only arm did
(35–50 s against 39–59 s). n = 3, one task, one model.
