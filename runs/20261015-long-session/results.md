# Long-session test — results (9 runs, claude-haiku-5-5, one round)

Design and prediction: `design.md` (committed `5b35b9e` before any run). Scorer: `score.ts` (main agent's; reads the
shim log, the journal, the insight files with the guard's parser, REPORT.md, the final message and the transcript).

| Run | (a) redirected / calls | (b) failures logged | (c) valid insight answers all | (d) named | (e) pytest green + REPORT.md | Stop blocks | denies | seconds |
|---|---|---|---|---|---|---|---|---|
| A1 | 2 / 2 | 2 | yes | yes | green + yes | 0 | 0 | 77 |
| A2 | 2 / 2 | 2 | yes | yes | green + yes | 0 | 0 | 83 |
| A3 | 2 / 2 | 2 | yes | yes | green + yes | 0 | 0 | 91 |
| B1 | 2 / 2 | 2 | yes | yes | green + yes | 0 | 0 | 82 |
| B2 | 2 / 2 | 2 | yes | yes | green + yes | 0 | 0 | 80 |
| B3 | 2 / 2 | 2 | yes | yes | green + yes | 0 | 0 | 110 |
| C1 | 2 / 2 | 2 | yes | yes | green + yes | 2 | 1 | 102 |
| C2 | 2 / 2 | 2 | yes | yes | green + yes | 2 | 1 | 107 |
| C3 | 2 / 2 | 2 | yes | yes | green + yes | 3 | 1 | 99 |

How long the sessions were: 41–51 tool calls, about 80–110 s, peak context about 46,000–57,000 tokens (A1, B1, C1
measured from their transcripts) — long in steps, not long enough to reach compaction.

**Against the prediction:**
- **Arm A (rules only) — wrong.** Predicted 2/3 → 1/3 decay; measured **3/3 on every measure**. With the rules read
  once at the start, haiku carried them through 14 steps and both late engine failures.
- **Arm B (rules + hooks) — held** on (a)–(e) 3/3; the hooks never had to act (0 blocks, 0 denies); time about the same
  as A (median 82 s against 83 s).
- **Arm C (hooks only, no written rules) — held:** 3/3 on every measure. Each run hit one deny (the bare `codex exec`)
  and 2–3 Stop blocks, and learned the rest from the hooks' messages; median 102 s (about 25% slower than A).

**What this shows (my reading, n = 3 per arm, one task, one model, sessions under 60,000 tokens):** written rules that
the agent reads were followed — on short and on 14-step sessions. The hooks give the same result **without** any
written rules (arm C), so they make the rules hold even when the agent never reads them; when it does read them, the
hooks stay silent and cost nothing. Not shown: a session long enough to compact its context, other models, other tasks.
The prediction for arm A was wrong in all four rounds now (E4 ×3, this one).
