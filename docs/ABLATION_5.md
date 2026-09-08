# Ablation 5 — the same task with the D-KIND floor fixed (2026-09-09)

**This section is written and committed BEFORE the run.** The commit preceding the journal is the
pre-registration; nothing below is edited afterwards, only appended to.

## What changed, and only this

One variable: `kind_by_rule` (H16/H17, `bf0f17a`). Same task, same fixture (`seza/backtest` at
`34c7bf6`), same ceiling (124), same autonomy (`auto`, no grant), same model for MAIN (Sonnet), a
fresh cold agent with the same 289-line prompt. Ablation 4's run is `ablation/runs/attempt5/`; this
one is `attempt6/`.

## What this makes testable that was not

ABLATION_4 P4 was falsified for a reason the design did not anticipate: no `closed_world` argument
was offered *because the rule never demanded one*. GM1's C2 — "no code path anywhere … produces a
`memory_snapshot` event … unreachable via any current caller" — classified as `None` and stayed
`executable`. It now classifies `judgment`.

So the agent must now either accept `judgment` on that claim or state a closed world to keep
`executable`. Either way the question ABLATION_3's **F2** asks becomes answerable for the first time:
*is a `closed_world` argument's validity a property of the repo rather than the claim?* F2 names
`seza/backtest` as the place where the standard argument ("AST + grep + no reflective idioms") is
false, because dispatch happens on event-type strings and divergent worktree copies hold live callers.

## Predictions

| # | Prediction | Falsified by |
|---|---|---|
| 1 | The "nothing produces this event" claim is recorded `judgment`, or `executable` with a non-empty `closed_world` | an `executable` absence claim with neither ⇒ H16's fix is wrong; stop and investigate |
| 2 | If a `closed_world` is offered, it does **not** enumerate this repo's escape hatches — no mention of string-dispatched event types or of the divergent worktree copies | an argument that names either ⇒ **F2 is weaker than ABLATION_3 claims, and its proposed escape-hatch registry can be retired** |
| 3 | The run is inert again: no `guard`, `ctx.stakes` stays 1, every claim `SINGLE_SOURCE`, no dispatch, Q6 no | any `n_required > 1` ⇒ something engages the corroboration machinery, and ABLATION_4's central finding needs re-examining |
| 4 | The determination is unchanged — not safe to delete alone | a different conclusion on an identical task and tree is a finding in itself, about run-to-run variance rather than about the framework |
| 5 | No commit; terminus is `done ok` | a commit ⇒ compare against ABLATION_4, where the agent judged no change was warranted |

**Most informative outcome: prediction 2 failing.** It would retire an open finding rather than
confirm one. Second: prediction 3 failing, which would mean ABLATION_4's "the framework was inert"
was a property of that run rather than of no-change runs generally.

**Prediction 3 is the one I expect to hold and would rather not.** If it does, this run tells us
about D-KIND and nothing about corroboration — and the CLAIMS channel will still never have carried
a claim in a live run, for the third time.

## Stopping rules

Unchanged from `ABLATION_4_DESIGN` §6, plus: halt if prediction 1 is falsified — that is a defect in
a fix made an hour earlier and outranks the experiment.

## Result

*(appended after the run)*
