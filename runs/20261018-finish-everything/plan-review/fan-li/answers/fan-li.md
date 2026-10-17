# 范蠡 (Fan Li) — Review 6-hour plan to finish everything

## Answer
CHANGE

Current words:
`One workflow per item or pair of items, in the order above (sequential; opencode never twice at once), using the saved`
`workflows where they fit (`review-enhance` for 3; tests-first → engine → verify for 4–8; `experts-decide` for 9–11 and`
`the owner-only questions). Each step's evidence goes in `runs/20261018-finish-everything/`. Tested work is committed and`
`pushed as each item lands. Out of scope: another session's work (`TODO-2.0.md`, the code-map build).`

New words:
`One workflow per item or pair of items (sequential; opencode never twice at once). Items 2–8 run first. Item 1 prepares in a worktree branch without blocking items 2–8; the master merge waits for the other session's commit. Items 9–11 decide provisionally without 1M-token benchmark runs. Items 12 and 13 are deferred past the 6-hour window. Each step's evidence goes in `runs/20261018-finish-everything/`. Tested work is committed and pushed as each item lands. Out of scope: another session's work (`TODO-2.0.md`, the code-map build), items 12 and 13.`

Current words:
`| 12 | The evaluator at a milestone, end to end: evaluate memory_check, ingest the verdict | integration | a verdict on memory_check exists and `evaluation ingest` turned it into failures and notes (cost recorded) |`
`| 13 | The 42 older insights with no recorded choice | triage | each marked, under today's R12.2, as evidence (no choice needed) or a real failure with its top fix applied |`

New words:
`| 12 | The evaluator at a milestone, end to end: evaluate memory_check, ingest the verdict | integration | [DEFERRED past 6h window to protect token budget and engine limits] |`
`| 13 | The 42 older insights with no recorded choice | triage | [DEFERRED past 6h window to protect focus and engine limits] |`

## Why
Item 1 cannot land before the other session commits; placing it first risks stalling the sequential pipeline before human affairs have arisen (my #1, my #3).
Items 2–8 have known checks and can be completed immediately with available engines, securing high-certainty fixes at low token cost (my #4, my #18).
Measuring items 9–11 and running item 12 consumes ~4M tokens while Codex is capped until 04:00; forcing completion before Heaven's time risks exhausting the 6-hour window (my #1, my #7).
Triaging 42 older insights (item 13) while executing code fixes dilutes engine attention; stopping at the border of the 6-hour limit avoids overextension (my #10, my #13).
Deferring items 12 and 13 costs immediate backlog closure, but guarantees items 2–8 and provisional designs 9–11 finish cleanly within 6 hours (my reading).

## What I need to know
- When will the other session commit `docs/TASK_TYPES_LEDGER.md`? If before 04:00, item 1 can land as soon as prepared; if late or unknown, item 1 must remain decoupled from items 2–8.
- Does EJ require real-run token measurements for items 9–11 and 12 within these 6 hours? If yes, items 3–8 must be curtailed to free engine quota; if no, items 12 and 13 are deferred as recommended.
