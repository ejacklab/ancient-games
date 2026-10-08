# Review — `docs/ancient-games-algorithm.html` (deepseek-v4-pro)

## 1. Correct?

Mostly correct, with two real problems on the method side.

- **Referee — correct.** All five stages are right, in the right order: Gate (how many agents),
  Guard (which actions need approval), Corroborate (how many independent sources a claim needs),
  Filter (which candidates survive), Prove (is the plan cleared). This matches CLAUDE.md, SPEC §4, and
  `ancient_games/stages.py` exactly. No stage missing, none misnamed.
- **Loop — correct, drawn forward.** Task → Method → Referee → Findings → back into Method matches
  CLAUDE.md. It is not backwards.
- **Method — the list is a lossy re-mapping, not a faithful reading of 3.0–3.8.**
  - The source has **nine** sections (3.0–3.8); the diagram shows "8 steps" by merging 3.6
    ("the rest is a graph") with 3.7 ("sequential first; parallel last") into one "Graph" bullet,
    and it **drops 3.8 ("Running a node" — executors as tools, two timers, no polling, pass-back
    contract) entirely**.
  - Step 8 is named **"Accept"**, a word that does not appear in the source. Its content (stop at the
    criteria, the baseline, and "must not change") is the run's three-part stop from 3.6 — stated
    accurately — but "Accept" reads as human sign-off, and the method uses "accept" for a different
    thing (EJ accepting a blueprint section).
- Minor: "no LLM" is faithful to CLAUDE.md and to the code (`stages.py` is spine-only; the `[LLM]`
  cells are passed in as inputs), but SPEC §4 labels several referee steps `[LLM]`/`[spine+LLM]`, so a
  reader cross-checking SPEC may find the phrase odd.

## 2. Simple and direct?

The loop and the referee half are clear for a newcomer. The method half is where it gets confusing:
"8 steps" versus nine sections will trip anyone checking against the doc; "Graph — the rest wires up"
presumes you know what "the rest" is; "Accept" sounds like approval instead of a stop condition; and
the dropped 3.8 means a reader who follows the link won't find the "how a node actually runs" step
(executors, timers, no polling, pass-back).

## 3. One improvement

Split "Graph" back into 3.6 and 3.7, rename "Accept" to the run's three-part stop, and give 3.8
(run a node — executors, timers, no polling, pass-back) its own bullet so the list matches
sections 3.0–3.8.
