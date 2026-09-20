# Ablation 4 — design: does the CLAIMS channel work when an agent can see it?

Design only. Pre-registered before the run, so the result cannot be rationalised afterwards.
Written against `9329c78` (D-KIND closed on both paths, 363 tests green).

---

## 0. The blocking prerequisite — measured, not assumed

**A free agent currently cannot know what to return.** `tools --schema` tells it:

```
ingest_return  side_effects=none  cost=cheap  -> list[event]
  agent_id: str
  fields: dict          <- and nothing else
  actor: str  # ...
  framing: str
```

Meanwhile `schema.RETURN_CONTRACT` specifies twelve return fields with shapes and escape values —
`REPORT_BACK`, `CLAIMS` ("always required"), `SCOPE_DELTA`, `FOLLOW_ON`, `NOT_DONE`, `VERDICT`,
`NOT_ESTABLISHED`, and five more. It is consumed by the lints, which check that the *contract itself*
is well-formed. It is **never rendered into the ablation packet**: `grep -c "REPORT_BACK\|NOT_DONE"`
over `ablation/packets/UC{1,2,3}.md` returns **0, 0, 0**.

So the historic result — two live `return` events, zero CLAIMS entries, both agents inventing their
own field names (`strongest_attack`, `verdict`, `factual_errors`, `bears_on_C4`) — is **fully
explained by the packet**, and says nothing about the agents or the channel. They were asked for
`fields: dict` and they supplied a dict.

This is H12's defect class exactly (ABLATION_2: *"both agents passed a prose string; the schema line
for `framings` is not explicit enough"*), on a different field.

> **P0 — must land before the run: render `RETURN_CONTRACT` where the agent reads it.** The `fields`
> note in `cli.NOTES`, keyed `("ingest_return", "fields")` — F4 made that possible — naming the
> required fields and CLAIMS' entry shape, plus the contract table in the packet.
>
> Running before P0 produces a guaranteed-uninformative run. It would repeat attempt 4 and we would
> learn the same nothing, more expensively.

---

## 1. What this run is for

**Primary question.** With the contract visible, does a free agent route a dispatched worker's
findings through `ingest_return`'s CLAIMS — and when it does, does the now-guarded path behave?

**What it cannot establish, stated up front.** D-KIND holding on the CLAIMS path is *mechanically
guaranteed* at `9329c78` — unit-tested, sabotage-checked, one writer. A live run does not test the
rule. It tests whether the **situation arises at all** and whether the interface is usable under
free choice. That is an interface result, not a correctness one. Anyone reading this later should
not upgrade it into evidence that D-KIND "works", which the tests already establish more strongly.

**Secondary, opportunistic — ABLATION_3's open F2.** *"A `closed_world` argument's validity is a
property of the repo, not of the claim."* F2 names `seza/backtest` as the place where the standard
argument ("AST + grep + no reflective idioms") is **false**, because dispatch happens on strings and
divergent worktree copies hold live callers. If the task is sited there, the run tests F2 for free.

---

## 2. Task

**Candidate A (recommended): "Is `loop/graph_memory.py` safe to delete?" in `seza/backtest`.**

Why this one:

- **The central claim is a judgment** — an absence claim, so B·1 forces a second head or a gate.
  That is the precondition for a dispatch happening at all.
- **Two genuinely different framings exist, and they disagree.** A module-level import scan reports
  nothing; `program_db.py:551` holds `from loop import graph_memory` **inside a function body**, with
  three call sites below it. Static-scan and runtime-import-probe are not the same instrument here —
  which is exactly the distinction ABLATION_3's F1 says the framing rule cannot currently make.
- **Ground truth is known and documented**, so the run can be scored rather than admired:
  `seza/CLAUDE.md` records the lazy import and that removal "needs surgery judged not worth the risk."
- **F2 is live on this repo**: the naive `closed_world` argument is false here, and whether the agent
  notices is the F2 test.
- It is **real work** — the answer is useful whichever way it lands.

**Candidate B (fallback): a synthetic fixture with the same shape.** Cheaper and hermetic; loses the
F2 test and the real-repo escape hatches, which are half the value. Use only if siting on a real repo
is judged too risky.

**Not** a repeat of UC2J or UC3. Both are answered, and a repeat tests memory, not the framework.

---

## 3. Setup

| | |
|---|---|
| Repo | a **copy** of `seza/backtest` at a pinned commit — never the live tree. The agent may delete. |
| Ceiling | 124 (`default_ceiling()` today: 2× the longest free-agent journal) |
| Autonomy | `auto`, no pre-authorisation grant — a D-KIND override must reach the checkpoint gate and stop there. That is the disclosure path under test. |
| Dispatch | genuinely a second agent, as in attempt 4's `adv-1`. A simulated worker makes the independence fictional and the run worthless. |
| Nudge | **none.** As in attempt 4: state that dispatching and not dispatching are both acceptable. UC2J's correct *refusal* to dispatch is a valid outcome and must stay available. |
| Journal | `ablation/runs/attempt5/` |

---

## 4. Pre-registered predictions

Recorded now so the result cannot be fitted afterwards.

| # | Prediction | Falsified by |
|---|---|---|
| 1 | With P0 landed, the agent returns worker findings as `CLAIMS` rather than ad-hoc fields | ad-hoc field names again ⇒ the contract is still not reaching the agent; a packet defect, not an agent one |
| 2 | It dispatches, because a genuinely different framing exists (UC3's pattern, not UC2J's) | a reasoned refusal naming why the second instrument would differ — that is a *result*, not a failure, and repeats attempt 4's discrimination |
| 3 | The worker's `graph_memory is unused` claim is recorded `judgment`; any `executable` needs `closed_world` | an `executable` with no `closed_world` on the CLAIMS path ⇒ the fix at `9329c78` is wrong; investigate before anything else |
| 4 | The naive closed_world argument ("AST + grep") is offered **and is false here** — the lazy import at `program_db.py:551` defeats it | the agent enumerates dynamic-import sites unprompted ⇒ F2 is weaker than ABLATION_3 thought |
| 5 | The run ends at the checkpoint gate with the override disclosed, not at a commit | a commit under an undisclosed override ⇒ a second bypass; stop the run and treat as a defect |

**The most informative single outcome is prediction 4 failing.** That would mean the closed-world
argument generalises further than F2 claims, and F2's proposed registry of escape hatches is
unnecessary.

---

## 5. Scored by

`ablation/score.py` as-is (Q1–Q5 from the journal, never from the agent's report), plus three
questions this run adds — computed from the journal, same rule:

- **Q6 — CLAIMS used?** any `return` event whose `fields` carry a non-empty `CLAIMS` list.
- **Q7 — kind honest?** every `claim_recorded` whose text matches `ABSENCE_PATTERNS` is `judgment`,
  or carries `kind_override=True` with a non-empty `closed_world`.
- **Q8 — escape hatches enumerated?** does any recorded `closed_world` name the dynamic-import site?
  (F2. Judged by reading, not computed — and labelled as such.)

Q6 and Q7 are mechanical. Q8 is a reading, and must be reported as a reading.

---

## 6. Cost and stopping rules

One run, one task. n stays 1; ABLATION_3 already says two agreeing runs are "directional, not
statistical," and this design does not pretend otherwise.

**Stop the run early if:**
- prediction 3 fails — a correctness defect outranks the experiment;
- prediction 5 fails — a commit under an undisclosed override is a second bypass;
- the agent is blocked by a harness defect for more than two consecutive calls. Log it as a v1.6
  candidate and stop; a run spent fighting the interface measures the interface, which is what
  P0 was supposed to have fixed.

**Do not** turn any single-run finding into a rule change. ABLATION_3's F1 is explicitly *"not to be
built on n=1"*, and this run is n=1 as well.

---

## 7. Open, for the owner

1. **P0 first?** It is a small change (one `NOTES` entry, one packet section) but it is a harness
   change made *because of* a planned run, which needs saying out loud.
2. **Candidate A or B** — real repo copy, or synthetic fixture.
3. **Who is the dispatched worker?** Attempt 4 used a real subagent. Same again, or a different model
   deliberately, to decorrelate harder?
