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

**The intended experiment did not happen, and the run found something worse than what it was testing.**

Ablation 6 concluded *not safe to delete*, proposed no change, and therefore never called `guard` —
so `ctx.stakes` stayed 1, `n_required` was 1, and every claim cleared as `SINGLE_SOURCE`. **The
corroboration pressure that H18 was supposed to be tested against was absent for a reason unrelated
to H18.** Prediction 2 held, but it holds vacuously: no dispatch was needed because no count was
short, not because the count now closes without one. This run is a replication of ablation 4, not a
test of H18.

| | ablation 4 | ablation 5 | ablation 6 |
|---|---|---|---|
| Determination | not safe | **safe** | not safe |
| `guard` | never called | GATED, stakes 2 | never called |
| `n_required` | 1 | 2 | 1 |
| Dispatch / CLAIMS | no / no | **yes / yes** | no / no |
| Terminus | `done ok` | the gate | `done ok` |

### Predictions

| # | Prediction | Outcome |
|---|---|---|
| 1 | MAIN's two checks count; C1 reaches 2/2 without a dispatch | **UNTESTABLE.** `n_required` was 1, and the one check was recorded *after* `corroborate` and `prove` anyway. Never entered a count. |
| 2 | No dispatch, no CLAIMS | **held, vacuously** — see above. It is not evidence about H18. |
| 3 | Determination "safe to delete" | **FALSIFIED.** Not safe, matching ablation 4. |
| 4 | `guard` runs, stakes 2, terminus the gate | **FALSIFIED.** No guard, stakes 1, `done ok`. |
| 5 | An absence claim is `judgment`, or `executable` with `closed_world` | **held mechanically, failed in substance** — see below. |

### The finding: H16's fix moved the floor, it did not remove it

C2 reads: *"**No code in the current repo constructs** a memory_snapshot event and **no test
exercises** the graph_memory-importing branch."* That is an absence claim by any reading. Yesterday's
widened rule — the list **and** the structural half — classifies it as **None**, and it was recorded
`executable` with no `closed_world` and no override.

Why: the structural half looks for a negation bound to an *unbounded scope*, and its scope vocabulary
is `any|anywhere|anything|all|every|entire|whole|repo-wide`. C2 wrote **"the current repo"**. One
word outside a list, again.

```
'No code in the current repo constructs a memory_snapshot event'  -> None
'No code anywhere in the repo constructs it'                      -> judgment
'No code in the entire repo constructs it'                        -> judgment
```

ABLATION_4 said "widening alone is another floor" and I built a structural half specifically to avoid
that — but the structural half's scope list **is a word list**. Two designs, three runs, three
escapes. The claim that this rule can be fixed by adding patterns is now falsified by its own third
counterexample.

**Stop patching it.** ABLATION_4's own candidate fix already named the alternative: treat "is this an
absence claim?" as an `[LLM]` classification with the keyword rule as a floor beneath it. That puts a
model call inside `record_claim` — a cost and determinism change to the tool layer, and an owner
decision, not a defect fix. **Not to be made on n=3 by the person who wrote the last two attempts.**

### H17 is why we know

`Q7` answered **yes** — no violations — and then reported *"rule did NOT classify 2 executable
claim(s): ['C1-graph-memory-imported', 'C2-no-current-producer'] — read these, the rule cannot"*.
Reading them is how the miss was found. Under the old scorer this run would have scored a clean
`Q7 = yes` and the escape would have been invisible for a fourth time. **The coverage report was
non-empty on its first live use.**

Note also that the agent's own report claimed C2 was *"executable w/ closed_world"*. The journal says
`kind_override=False, closed_world=None`. Scoring from the journal rather than the report is what
caught that too.

### The structural finding is now n=3

Ablation 5 proposed to act and got the whole apparatus: guard, stakes 2, a capped count, a second
head, a human gate. Ablations 4 and 6 proposed no change and got none of it — no guard, stakes 1,
single-source, straight to `done ok`.

**Engagement is fully determined by the conclusion.** Concluding "leave it alone" is self-exempting:
it removes the mutation, which removes the guard, which removes the stakes, which removes the
corroboration requirement. The framework cannot audit the one conclusion that avoids it — and 2 of 3
runs reached exactly that conclusion.

Two of three also disagree with the third about the answer, so the framework's strongest run reached
the minority verdict. Which is right remains open, and is the question at ablation 5's gate.

### Not established

- **Whether H18's fix changes behaviour under pressure.** The comparison this run was designed to
  make never happened. Testing it needs a task where the agent must act — the fixture should probably
  make deletion clearly correct, so the run reaches `guard` and stakes 2.
- Whether ablation 4/6 or ablation 5 is right about `graph_memory.py`. Still at the gate.
- n = 1 per configuration. Three runs, two configurations, and the one that engaged the framework
  ran only once.
