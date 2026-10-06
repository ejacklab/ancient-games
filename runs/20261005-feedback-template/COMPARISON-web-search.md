# Three experts on `web search` — 2026-10-06

Blind, six-whys, on `Found / Sources / Disputed`.

## Convergence (all three)

1. **"Traceable" means each claim paired to its source, not a flat list.** deepseek added `[S#]` keys; claude the
   same; minimax folded sources inline into each `Found` line. Three ways to the same fix.
2. **`Disputed` records the split, never the resolution.** The vote's count and both sides, by source id; the
   resolution is the human's (it needs a corroboration threshold no one has set).
3. **No `Effort`** — single node.
4. **The not-found case needs a home** (claude + minimax): the type's sabotage *is* "nonexistent fact → not-found",
   and the template had nowhere to put it.

## Where they differ

- **Sources separate vs inline.** deepseek + claude keep a `[S#]` list; minimax folds the URL into each claim line —
  "one fact, one writer", no join to drift. The one real template divergence.
- **Two dates** (claude only): published vs accessed — but minimax flags "dated" as two numbers, a unit question.
- **`FACT / INFERRED / GAP`** (minimax): borrowed from `research and reports`, names the not-found case (GAP).

## The sharpest catch (minimax)

**"single node; voting on contested facts" is a contradiction.** A single node is one worker — who votes? Sources
outvoting each other, or multiple workers? It decides whether this is really a loop/fan-out (and whether `Effort`
appears). That is a fix to the `TASK_TYPES` row, not the template.

## Left for EJ

1. **Who votes** — sources (one worker reports the split) or workers (a loop)? Fixes the row.
2. **The corroboration number** — how many independent sources settle a claim; what a tie does. Until then
   `Disputed` ends "unresolved".
3. **Undated sources** — admissible, or force not-found/GAP?
4. **Sources separate vs inline** — the one template split.
