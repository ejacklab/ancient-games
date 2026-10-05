# Requirement check — "A limit on attempts."

Run against the checklist in `docs/research/20261005-requirement-statements/FINDINGS.md` §2.

**The statement as written** (`docs/WORKFLOW_DESIGN_METHOD.md`, 3.5's loop-ready list, item 2 — the wording before
today's rename):

> *"A piece is loop-ready only if it has all five: … 2. A limit on attempts."*

**What already checks it:** `design_gate.py:269` — `if not isinstance(lp.get("limit"), int) or lp["limit"] < 1:` →
*"node {nid} loop has no attempt limit"*. So **absence** fails. **No value fails**: a node with `limit: 99` passes
every gate in the project.

## The eight

| # | question | verdict |
|---|---|---|
| 1 | **Source** | **FAIL** — item 2 of a list. No attribution for the rule, no basis for its existence. |
| 2 | **One thing** | **pass** — one condition on a piece. (It is a fragment: the sentence is *"A piece is loop-ready only if it has all five:"*.) |
| 3 | **Unit** | **FAIL, twice.** (a) *"attempts"* does not say whether it bounds a **count** (how many tries) or a **time** (how long one try may run) — EJ read it as time; the method means count. (b) **there is no value at all**, so the limit is whatever the reader assumes. |
| 4 | **Can it fail** | **HALF.** Presence is checked (a positive integer is required). **Value is not** — nothing can fail for being too high. |
| 5 | **Weak words** | **FAIL** — *"limit"* names no quantity, unit or value. |
| 6 | **Level** | **pass** — a necessary condition ("loop-ready only if"), and an unbounded loop is a safety matter, so MUST is defensible. But it does not say what must be true of the **value**. |
| 7 | **Basis** | **FAIL** — no basis for the rule and none for any number. The corpus's `limit: 2` comes from the harness emitting 2, which is a harness default, not a source. |
| 8 | **Links** | **pass** — item 4, *"an exit for when the limit is hit"*, refers to it inside the same list. |

**Four failures, one half, three passes.**

## The questions this leaves — for a person, not for me to fill in

1. **Unit.** Does the limit count *attempts*, bound *time*, or is it two requirements?
2. **Value.** What number, and does it differ by tier or by kind of piece? If it stays open, what is the default?
3. **Who sets it.** The designer per node, or a default from `TASK_TYPES.md`?
4. **Interaction.** 3.8 now bounds one call at 8 hours. Does that belong inside this requirement, or stay separate?
5. **At the limit.** Item 4 gives the tier exit. Is that the only exit, and what happens when there is no stronger
   tier?
