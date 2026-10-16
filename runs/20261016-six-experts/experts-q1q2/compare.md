# Four experts — the 6 insight categories, how related ones are picked, and Dave's engine

Answers: 范蠡 and 孫子 in `experts-q1q2/answers/`; Linus and 老子 in `experts-q1q2-opencode/answers/` (rerun after
F-7f938bdf). Linus ran on opencode: Codex had 0% quota.

| | Linus (opencode) | 范蠡 (agy) | 孫子 (dsh) | 老子 (opencode) |
|---|---|---|---|---|
| Categories | 4 Source kinds + 2 flags (engine, cause unconfirmed): "the six-category count is EJ's number … not something today's corpus supports" | 6: config, tool, check-guard, check-test, instruction-spec, instruction-workflow | 6: Source kinds, instruction → brief / handoff, check → check-noisy / check-blind, tool → engine-output, config → environment | 6 moments: before it starts, starting it, while it runs, reading the result, checking it, keeping it |
| Related insights | (c) both; Dave may add, cites every id | (c) both | (c) both; cites `<file>#<id>` | (c) in a fixed order; Dave writes one line if the named moment was wrong |
| Dave's engine | Claude Sonnet 5.5, cached prefix, ≈$0.03/question; same engine as today for the n=1 trial — one variable per trial | Claude Opus 5.5, ≈$0.02–0.05 with caching; revisit at 200k tokens or a category over 50k | Claude Sonnet 5.5 for Dave and Dario, ≈$0.05; revisit at 100k per question or 922k total | Claude Sonnet 5.5; no engine change for ≈80–100 working days if the load is subtracted, never accumulated |

## Where they agree (quoted from the answers)
- (c) both, for picking related insights: all four.
- Sonnet 5.5: three of four (Linus, 孫子, 老子); 范蠡 Opus 5.5.
- The Source field is the starting point: Linus, 范蠡, 孫子.

## Where they disagree (side by side, not averaged)
- **Six or four:** Linus — four plus two flags, six is not supported by the data; 范蠡, 孫子, 老子 — six.
- **What splits:** 范蠡 splits by what kind of check/instruction; 孫子 by noisy vs blind checks and brief vs handoff;
  老子 drops Source and sorts by the moment the fix belongs.

## What the main agent decided (provisional; EJ accepts or declines at the end) — see state.md D1, D2
