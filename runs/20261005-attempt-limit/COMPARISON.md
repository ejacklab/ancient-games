# Three experts complete "A limit on attempts." — 2026-10-05

The requirement check is in `CHECK.md` (four failures, one half). The brief is in `BRIEF.md`. Three experts answered
it blind: `claude-opus-5-5.md`, `minimax-m3.1-flash.md`, `deepseek-v4-pro.md`.

## What the check found, before anyone wrote anything

> **"A limit on attempts."** — item 2 of 3.5's loop-ready list
>
> **Source** FAIL · **Unit** FAIL, twice (count or time? and no value at all) · **Can it fail** HALF (presence is
> checked, value is not) · **Weak words** FAIL ("limit") · **Basis** FAIL · One thing, Level, Links pass.

## The three answers

| | claude-opus-5-5 | minimax-m3.1-flash | deepseek-v4-pro |
|---|---|---|---|
| shape | **5 requirements** (R1–R5): the bound, the run obeying it, the unit, the value, a reason to raise it | **3 requirements** (R1–R3): declare the unit, bound it above, make the runner obey the declared number | **1 requirement**, kept whole, because the check says "one thing" passes |
| value | **`open`**, ship default **2** "because it is the number in force, **not because anything supports it**" | **`3`** — a proposed ceiling, derived from the repo's only two real loops | **`open`** — "no number is sourced anywhere" |
| level | MUST for the bound; SHOULD for the value; a written reason to exceed it | MUST for the declaration; the ceiling is the number | MUST for existence, SHOULD for the number |
| time | explicitly **out of scope**, and claims **no link** to 3.8's ceiling | same, with the unit named | same, with the unit named |
| measured? | read the code and the method | **ran seven measurements** before writing (M1–M7) | read the code and the method |

**All three left the number itself to EJ, or proposed one while saying plainly that it is not sourced.** Not one
invented a value and presented it as the answer — which is what the brief asked for and what the checklist's
question 5 requires.

## Where they converged

1. **The value is EJ's.** All three said so, and two wrote `open` outright.
2. **The default to ship meanwhile is 2.** All three, because that is what the code already does — and claude named
   the trap: *"I chose it because it is the number in force, **not because anything supports it**."*
3. **The bound's existence earns MUST; the number does not.** All three reached RFC 2119 §6 independently, and two
   quoted its own example — *"limiting retransmisssions"* — as our case almost literally.
4. **Time is a different requirement.** All three kept 3.8's 8-hour ceiling out of this one, and claude stated it as
   a **negative link**: *"These requirements do not restate it and claim **no link** to it (question 8)."* After this
   morning's invented "runtime half", that is the checklist working on a real case.
5. **The same 孫子兵法 principle**, from the same note: 故兵貴勝，不貴久 — *"value victory, not duration"* (作戰篇,
   **VERIFIED**, CANONICAL #2). Two experts used it for the same point: set the bound **before** starting.

## Where they diverged, and it is the interesting part

- **minimax proposes a ceiling of 3**, and derived it: *2 is measured sufficient* (the node-workdir run: gate failed
  round 1, attempt 2 fixed it) and *3 is measured insufficient to converge* (the plan-critic loop: 3 rounds, 6 → 5 →
  4 problems, never closed). So the useful band is 2–3 and the ceiling goes at its top. **Marked TBR, review at 10
  ledger rows.** The other two left any ceiling open.
- **minimax found a unit ambiguity the others did not: `attempts` vs `retries`.** Both are in live use in this repo
  and they are **off by one** — `intake.js:206` counts attempts (`1` = one call, no retry) while
  `runs/20261004-bugfix-13/design.json` n1-spec counts retries (its exit describes a repair its own `limit: 1`
  forbids). *"The same number, two meanings, in one file — and it passes `design_gate.py` today."*
- **minimax's own reading of the classical text cuts against a bare count:**
  > *"The classical source gives a strong reason the cap must be **small** and a strong reason the cap must **not be
  > the stop condition** — and the second one means a bare count, however well written, is the failure mode the text
  > names."*
- **claude adds R5** — exceeding the category default requires a written, non-placeholder reason — as the way to make
  "a node with `limit: 99` passes every gate" checkable **without inventing a ceiling**. It marked R5 *"mine… open
  until EJ accepts it"*.

## Three real defects the answers exposed

**1. `limit: true` passed every gate — FIXED.** `isinstance(True, int)` is `True` in Python. Found by claude
answering checklist question 4, *"name one failing input"* — it listed `true` among them. Verified, fixed, and pinned
by a mutation. **The matrix is now 29/29 caught, 0 holes.**

**2. `check_plan` never validated the budget's own keys — FIXED.** minimax measured it (M5): `max_rounds: "two"`
reached `rec["rounds"] >= b["max_rounds"]` and **raised `TypeError` mid-run**; `-5` and `true` made that comparison
true on the first failure, so the loop **silently stopped after one attempt**; `10**9` was taken as no bound at all.
Verified independently, fixed for type and positivity, pinned by a test. **The ceiling on `max_rounds` is
deliberately not pinned — that is a number, and numbers are EJ's.**

**3. The design's limit and the runner's limit are different numbers — OPEN, and it is decision C.** claude's R2 and
minimax's R3/M4 found the same thing from opposite ends: a design node with `loop.limit: 1` and `repair` set gets
**2** attempts, because the runner uses `budget.max_rounds` and nothing carries `loop.limit` into `plan.json`. So the
design can state a bound the run does not apply. That is *"nothing compares the plan to the design"* — decided as C
on 2026-10-05 — arriving as a concrete instance rather than a principle.

## Also recorded

- **The corpus's `limit: 2` is not evidence of anything.** minimax measured it (M2): 166 of 170 loops are `limit: 2`,
  written by **two lines of a test file** (`tests/workflows/corpus_check.py:101,111`). Across 83 loops in the corpus
  there are only **2 distinct `exit` strings and 2 distinct `feedback` strings**, because the generator wrote them.
  *"A number written by the thing that generates the corpus is not a source for the number."*
- **A partial blindness breach, self-disclosed.** minimax reported that a `grep` for `max_calls` returned two lines of
  claude's file before it noticed the file existed. It says it did not read or use them and re-derived every finding
  by running the code. Flagged by the expert, unprompted.

## Open for EJ

1. **The value.** `open` in all three answers. Default to ship meanwhile: **2** (claude, deepseek) — what the code
   already does.
2. **A ceiling, or none?** minimax proposes **3** with a derived basis (2 measured sufficient, 3 measured
   insufficient) and marks it TBR. claude instead proposes *a written reason to exceed the default*, which needs no
   ceiling.
3. **`attempts` or `retries`?** They differ by one and both are in the repo. minimax's R1 makes the design state
   which — which fixes the ambiguity without choosing.
4. **Does the design's number have to reach the plan?** That is decision C, and this is the first case where it bites.
