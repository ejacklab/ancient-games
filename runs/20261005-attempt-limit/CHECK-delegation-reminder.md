# Requirement check — the delegation retry reminder

**As stated by EJ, 2026-10-05:**

> *"let change this to a workflow design reminder for all the subagent when delegates task to cli tools and subagent
> remind them to not retry more than 3 times"*

**Normalised:** *When a task is delegated to a CLI tool or a subagent, the delegation must remind the delegate not to
retry more than 3 times.*

## What already exists, before judging it

| where | what | rendered? |
|---|---|---|
| `dispatch.py:41` | `DEFAULT_BUDGET = {"max_rounds": 2, "max_calls": 30}` — the runner's repair bound | machine-enforced, and `check_plan` now validates the type |
| `docs/workflow-templates/node-brief.md:32` | a **`attempts left: n`** field in every node brief | **nothing renders it.** Its worked example says `attempts left: 2`, typed by hand |
| `intake.js:206` | `attempt_limit: '1 for pattern step'` | design-time |
| hand-written delegations (all of today's) | **no retry bound at all** | — |

So a slot for this exists, the number is **already in two places** (the budget and the brief), the two are not
connected, and the new statement names a **third** value.

## The eight

| # | question | verdict |
|---|---|---|
| 1 | **Source** | **pass** — EJ, 2026-10-05. |
| 2 | **One thing** | **FAIL — probably two.** It bundles a *delivery mechanism* ("a reminder… remind them") with a *bound* ("not more than 3 times"). A reminder is a means; the bound is the rule. |
| 3 | **Unit** | **FAIL, three ways.** (a) **3 retries or 3 attempts?** They differ by one and **both are live in this repo** (register 12.5). (b) **Per what** — per delegation, per step, per node? (c) *"retry"* here means either a **repair after a failed check** (the runner's `max_rounds`) or a **re-run after an executor failure** — which today **blocks**; the fallback was removed. |
| 4 | **Can it fail** | **FAIL.** A reminder cannot fail. Nothing checks it was included, and nothing observes how many times a delegate retried inside its own turn — the harness counts **active subagents (8)**, not retries. |
| 5 | **Weak words** | **FAIL.** *"remind"* is the weak word: an intention, not a constraint. *"task"* names no granularity. |
| 6 | **Level** | **FAIL, mismatched.** A reminder is **guidance**. "Not more than 3" is **MUST**-shaped. One level wearing another's clothes. RFC 2119 §6 lets a harm-limiting bound be MUST — but a reminder cannot enforce one. |
| 7 | **Basis** | **HALF.** The source is you. The **number 3**: today minimax derived 3 from two `n=1` measurements (2 sufficient, 3 insufficient) and marked it **TBR**; the code uses **2**. Is 3 yours independently, or an adoption of that proposal? |
| 8 | **Links** | **FAIL — and this is the one that bites.** No relation is claimed, but there is a **conflict**: the runner's bound is **2**, the brief template's example is **2**, and this says **3**. Same knob, or different? |

**One pass, one half, six failures.**

## The fork that decides the shape

**Is this rule about (a) the delegate's own retries, or (b) the runner's loop?**

* **(a) Delegate-internal.** Invisible to us: a subagent retrying inside its own turn reports nothing, and the
  harness counts active subagents, not retries. So this can only ever be **guidance written into the brief** — it
  cannot be a MUST and nothing can check it.
* **(b) The runner's repair loop.** Already machine-bounded at `max_rounds: 2` and **checkable** — `check_plan`
  validates it now. If this is the subject, the rule is nearly written: the number changes to 3, and the brief's
  `attempts left` should be **rendered from the budget** instead of typed by hand.

The two are different requirements with the same words.

## Questions for EJ

1. **(a) or (b)** — the delegate's own retries, or the runner's repair loop?
2. **3 retries or 3 attempts?** They differ by one, and both readings are in the repo today.
3. **Does 3 replace `max_rounds: 2`**, or are they two different knobs?
4. **Should `attempts left` be rendered from the budget?** Nothing fills it today — it is typed by hand, and the
   example says 2 while the new rule says 3.
5. **Adopt minimax's basis for 3?** It has two `n=1` data points behind it (2 measured sufficient, 3 measured
   insufficient) and is marked TBR. Yours alone would be `n=0`.
