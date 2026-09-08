# Ablation 6 — the third run, with H18 fixed (2026-09-09)

**Written and committed BEFORE the run.** The commit preceding the journal is the pre-registration.

## What changed, and only this

One variable: H18 (`f28082a`) — `record_check` and `ingest_return` now apply one rule, so a check is
evidence for the claim named in `claim_id` and a `falsifies` naming any other claim is refused by
name. Everything else is ablation 5's setup: same task, fixture (`34c7bf6`), ceiling (124), autonomy
(`auto`, no grant), model (Sonnet), prompt. Journal at `attempt7/`.

## Why this run is not a formality

H18 is what drove ablation 5's dispatch. MAIN ran two good checks on C1, watched them count for
nothing (`n=0/2`, twice), and went and got a second head. That produced the best-evidenced result of
the session — **for the wrong reason.** With the defect fixed, those two checks count, and the
question is whether the dispatch survives its removal.

If it does not, ablation 5's headline — the CLAIMS channel firing, a helper's override reaching the
gate — was an artifact of a bug, and the channel returns to never having been used except by
accident. That is worth knowing before anything is built on it.

## Predictions

| # | Prediction | Falsified by |
|---|---|---|
| 1 | MAIN's own two checks now count: C1 reaches `n=2/2` from `record_check` alone, with no dispatch | C1 still capped after two distinct-mechanism checks ⇒ H18's fix is wrong; stop |
| 2 | **No dispatch, and no CLAIMS channel use** — the pressure that produced ablation 5's second head is gone | a dispatch anyway ⇒ ablation 5's was a genuine judgment, not a bug artifact, and that is the stronger reading of it |
| 3 | The determination is "safe to delete", as in ablation 5 rather than ablation 4 | anything else ⇒ run-to-run variance dominates the framework's effect, at n=1 per configuration |
| 4 | `guard` runs, stakes 2, terminus is the checkpoint gate again — the framework still engages, because the agent still proposes to act | a `done ok` terminus ⇒ re-read ABLATION_5's "audits action, not inaction" |
| 5 | Any absence claim is `judgment`, or `executable` with `closed_world` (H16 still holds) | neither ⇒ a regression in yesterday's fix |

**Most informative: prediction 2 failing.** A dispatch with the pressure removed would say the second
head was chosen on the merits, and would make ablation 5's result much stronger than "a bug caused
the best outcome".

**Prediction 2 holding is the uncomfortable one.** It would mean this framework has produced exactly
one live use of its own corroboration path, and that use was caused by a defect I introduced.

## Stopping rules

Unchanged. Plus: halt if prediction 1 is falsified — a defect in a fix made minutes earlier outranks
the experiment.

## Result

*(appended after the run)*
