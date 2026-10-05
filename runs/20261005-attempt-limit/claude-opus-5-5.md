# Completing "A limit on attempts" — claude-opus-5-5

Expert brief: `BRIEF.md` in this folder. Written blind, 2026-10-05.

## What I read and what I could check

**Read:** `CHECK.md`; `FINDINGS.md` §2 and its verification pass; method §3.4–§3.8; the four 孫子 notes;
`design_gate.py:263-275`; `dispatch.py:41,60-110,262-296`; `intake.js:206,422-425`; `TASK_TYPES.md:44,192,240,260,298`;
`research/20261003-feature-cases/CRITIC.md:113-115` and rows B12, B17, D20.

**Not possible in this session:** running code, and reading git history. Both were refused by the permission system,
and I did not try another way round. So every claim about code behaviour below is marked **read** (inferred from the
source), never **ran**. The commit that first wrote "A limit on attempts" is **not traced**.

**The method was already edited today.** §3.5 item 2 now reads *"A limit on the **number** of attempts — a count, not
a time limit."* That edit answers half of Unit (count, not time). It does not answer the other half (what counts as
one attempt), and it does not supply a value, a level, a source or a basis. `CHECK.md` checks the old wording; I
complete both.

### What the code does today (all `read`)

This is what the completed requirement has to land on. Three findings matter:

1. **"2" means two different counts.** `dispatch.py:41` sets `max_rounds: 2`. The loop at `dispatch.py:291-295` adds
   one to `rounds` after each failed check and blocks the node when `rounds >= max_rounds`. So `2` means **two worker
   calls in total: the first try and one repair.** `TASK_TYPES.md:44` says *"Two repair attempts on script failure"*.
   Read plainly, that is **three** calls: the first try and then two repairs. The same number, written in two places,
   counts two different things. This is the failure `CHECK.md` found, one level down.
2. **The limit in the design is not the limit the run uses.** The gate checks each node's `loop.limit`
   (`design_gate.py:269`). The dispatcher never reads a per-node limit: `grep limit dispatch.py` finds only line 17.
   It uses a single plan-wide `budget.max_rounds`. Also, a node with no `repair` field is blocked after its **first**
   failed check, whatever `max_rounds` says (`dispatch.py:294`). That node's real limit is 1. Method §3.6 records
   that nothing compares the design with the plan, and says this is deliberate. I am only noting that the attempt
   limit is one of the things that goes uncompared.
3. **The gate lets one bad value through.** `isinstance(True, int)` is `True` in Python, and `True < 1` is `False`.
   So `"limit": true` passes `design_gate.py:269` as if it were 1. (`read`, from Python's rule that `bool` is a
   subclass of `int`; not run.) `check_plan` never validates `max_rounds` at all. A string there would reach the
   comparison at line 294 and raise `TypeError` at run time, instead of being refused before the run.

**Where the value 2 came from:** `CRITIC.md:114` resolved a conflict between research findings with *"Pick the
2-round cap (it is the method's current, documented rule)"*. That is the whole basis. The 2 is kept because it was
already there. No source for the number itself appears anywhere I read.

---

## 1. The completed requirements

The original is one statement in the checklist's sense: one condition on a piece. Completing it still means splitting
it, because it mixes three kinds of claim. RFC 2119 §6 says they belong at different levels:

- **that a bound exists, and that the run obeys it.** This limits harm. RFC 2119 §6 (VERIFIED in
  `FINDINGS.md`) gives exactly this as its own example of where a MUST is justified: *"to limit behavior which has
  potential for causing harm (e.g., limiting retransmisssions)"* (the RFC's own spelling). A retry limit is the
  textbook case.
- **what one attempt is.** This is a definition. Without it the number has no unit.
- **what the number is.** This is a method choice, and §6 says a method does not earn MUST.

That gives five statements: R1–R2 are MUST, R3 is a definition, R4 is the value, and R5 makes the value checkable.

### R1 — The design states the limit

| field | |
|---|---|
| **Statement** | Each loop-ready piece SHALL state its attempt limit `L` as a whole number of at least 1. |
| **Source** | Method §3.5 item 2, as renamed 2026-10-05 after EJ read the old wording as a time bound. The original author is **not traced** (git history was not readable here). The level reasoning (RFC 2119 §6) is **mine**. |
| **Unit** | attempts, as defined in R3 |
| **Value** | none. R1 requires that a value is present, not what it is (R4 covers that). |
| **One failing input** | `limit` absent · `0` · `""` · `"TBD"` · `"—"` · `"2"` (a string) · `2.0` · `-1` · `true`. Today's gate refuses all of these **except `true`** (see finding 3), so the gate needs `not isinstance(v, bool)` added. |
| **Level** | **MUST.** An unbounded loop is behaviour that can cause harm. RFC 2119 §6's own example is a retransmission limit. |
| **Basis** | **quoted** for the level: RFC 2119 §6, VERIFIED in `FINDINGS.md`. **n=1** for the need: the planner/critic loop that ran 6 → 5 → 4 and never closed (§3.5; `20260919-plan-critic-issues.md`). |

### R2 — The run stops at the limit the design stated

| field | |
|---|---|
| **Statement** | When a piece's `L`-th attempt fails its check, the runner SHALL make no further attempt on that node and SHALL take the piece's exit (§3.5 item 4). |
| **Source** | **Mine.** It is implied by "limit" but never written down. I stated it separately because finding 2 shows the design and the run use different numbers. |
| **Unit** | attempts (R3), counted **per node**. The stronger-tier node in item 4 is a new node and has its own count. |
| **Value** | `L` from R1 |
| **One failing input** | A design node with `loop.limit: 1` and `repair` set, run under the default plan budget (`max_rounds: 2`). The dispatcher makes 2 attempts, so R2 fails. A node with `loop.limit: 3` and no `repair`: the dispatcher stops after 1 attempt. That is safe, but the run did not do what the design said. **Absent:** a plan with no `budget`. Today this silently takes `DEFAULT_BUDGET` (`dispatch.py:65`), so nothing fails, and per R1 it should. |
| **Level** | **MUST**, on the same ground as R1. A bound that the run does not apply bounds nothing. |
| **Basis** | **read** (`dispatch.py:291-295`). Whether to fix this by carrying `L` into `plan.json` per node, or to accept the gap under §3.6's "nothing compares them" decision, is **EJ's call**. |

### R3 — What counts as one attempt (the unit)

| field | |
|---|---|
| **Statement** | One attempt is one worker call on the piece whose result is given to the piece's check. The first call counts. A call that ends in an executor failure (§3.8 item 5) is not an attempt. |
| **Source** | *First call counts*: **mine**. It follows §3.5's loop sentence (*"the agent attempts, the check runs"*) and the dispatcher's counting (`dispatch.py:291-294`). *Executor failure excluded*: **quoted**, method §3.8 item 5: *"Executor failures … do not count against the attempt limit, the node is **blocked** and goes to EJ."* |
| **Unit** | worker calls whose result reaches the check |
| **Value** | not a number; a definition |
| **One failing input** | `TASK_TYPES.md:44`, *"Two repair attempts"*, set next to a dispatcher limit of 2. Under R3 that sentence promises 3 attempts where the code makes 2, so one of the two must change. **Open, not covered by R3:** a `partial` result (§3.8 item 5: *"retry only the remainder as a new small call"*). Whether that call counts as an attempt is undecided, and I leave it **open** for EJ. |
| **Level** | **definition.** It has no level of its own; it carries R1's and R2's. |
| **Basis** | **read** (code) and **quoted** (§3.8). Including the first call was chosen because the running code already counts that way (CLAUDE.md Rule 12: the code is the arbiter). **Flag for cleanup (Rule 7):** `TASK_TYPES.md:44` and `:192` ("at most **2 rounds**") need rewording in attempts, or EJ decides the other way and the code changes. |

### R4 — The value

| field | |
|---|---|
| **Statement** | A piece's `L` SHOULD equal the default attempt limit for its category. |
| **Source** | **open.** The value is EJ's to set. |
| **Unit** | attempts (R3) |
| **Value** | **open.** **Default to ship meanwhile: 2 attempts** (the first try and one repair). This is what `dispatch.py:41` already does. I chose it because it is the number in force, **not because anything supports it**. |
| **One failing input** | R4 is a SHOULD, so a different value is not a failure on its own. R5 is what makes a departure checkable. Inputs that do fail: a category row with no default, or a default of `TBD`. |
| **Level** | **SHOULD.** It is a default that may be overridden with a reason. RFC 2119 §6: a method does not earn MUST. |
| **Basis** | **guess, n=0.** The only recorded basis is circular (`CRITIC.md:114`: kept because it was there). **Review when** the ledger holds enough loop runs to show, per category, which attempt produced the pass. The number of rows is EJ's to set. I am not inventing it. Evidence that one value may not suit every kind of piece, all from the project's own research: B12 (verified) found that feeding back the error raised success by 5.5% on average and by +12.33% for GPT-4 *in the first iteration*. B17 (reported) is Airbnb's mechanical migration: 75% of files done within 10 iterations, and a long tail of 50–100 retries. D20 (verified abstract) found critical vulnerabilities up 37.6% after five rounds of LLM "improvements". Whether the default differs by category is **open** (Q2 below). |

### R5 — Raising the limit needs a written reason

| field | |
|---|---|
| **Statement** | A design whose `L` is greater than its category default SHALL carry a non-placeholder `limit_reason` beside it. |
| **Source** | **Mine.** It is RFC 2119's meaning of SHOULD (*"the full implications must be understood and carefully weighed"*, RECALLED wording) turned into something a script can check. It is not EJ's. It is a proposal, **open until EJ accepts it**. |
| **Unit** | attempts, compared with the default from R4 |
| **Value** | none of its own. It uses R4's default. |
| **One failing input** | `limit: 5`, default 2, no `limit_reason`. Also `limit_reason` set to `""`, `"TBD"` or `"—"`. A **lower** limit needs no reason, because it costs less and is no less safe. |
| **Level** | **SHOULD-level rule with a MUST-level record.** The value may be overridden; the reason may not be left out. |
| **Basis** | **guess, n=0.** It answers `CHECK.md`'s *"No value fails: a node with `limit: 99` passes every gate"* without inventing a ceiling. **Review when** EJ decides R4. If EJ sets a hard maximum instead, R5 becomes that MUST and this version is dropped. |

### Out of scope on purpose: time

This requirement bounds **count only**. The time one attempt may take is §3.8's: the per-task timers, and the ceiling
*"no single call runs longer than the ceiling: 8 hours (EJ, 2026-10-05; n=0)"*. That ceiling already passes all eight
questions (`FINDINGS.md`, "The ceiling"). These requirements do not restate it and claim **no link** to it (question
8). The word "attempts" is never used for time, and "hours" is never used for count.

---

## 2. The five questions

**Q1 — Unit.** **Count.** Time is a separate requirement that already exists (§3.8). The count also needs R3 to define
what one attempt is: it includes the first call and excludes executor failures. Without R3, "2" meant 2 calls in the
code and 3 calls in `TASK_TYPES.md:44`. That is the same ambiguity as count versus time, one level down.

**Q2 — Value.** **Open.** Ship **2 attempts** meanwhile (R4), labelled n=0 and inherited. Whether it should differ by
kind of piece: the project's own research suggests it might. Mechanical translation got value from many iterations
(B17, reported). Security-sensitive fix loops got worse with more rounds (D20). `CRITIC.md` already deferred this
exact choice "for a decision after a real migration run". I leave it **open** for that reason: the evidence points two
ways, and no run here has measured it. By tier: the stronger-tier node gets "its own limit" (§3.5 item 4). I would
give it the same default until measured, and mark that n=0 as well.

**Q3 — Who sets it.** The **default** comes from one place, and the **designer** may lower it freely or raise it with a
reason (R5). Two parts are **open**. First, *which one place*: today the number sits in prose in
`TASK_TYPES.md:44/192/260` and as a constant in `dispatch.py:41`, and `TASK_TYPES.md` has no column for it. Second,
whether the designer's `L` should reach the dispatcher per node (R2's failing input). Both are EJ's.

**Q4 — The 8-hour ceiling.** **Keep it separate.** The two count different things: hours per call, and attempts per
node. The deleted caps rule (§3.7) is this project's record of what happens when two units share one sentence. One
consequence follows from multiplying them, and it is a fact about the two rules, not a new rule: with L = 2 on each of
two tiers and the 8-hour ceiling, one piece can use **4 calls × 8 h = 32 hours** of engine time before it reaches EJ.
No requirement bounds a whole loop's time or tokens. The run's `max_calls: 30` is a third count, per run, and it does
not bound time either. **Whether a per-loop time or token budget is wanted is a new requirement, and EJ's.** I do not
write it.

**Q5 — At the limit.** Item 4's exit stands: a fresh stronger-tier node with a handoff note. When that limit is also
hit, or there is no stronger tier, the piece goes back to the unclear list or to EJ. That is not the only way a loop
ends, though. The code also stops on an executor failure (blocked, not counted), on an UNCLEAR return, and on the run's
`max_calls` (`dispatch.py:274, 282, 284`). **What remains open:** item 4 says *"the unclear list **or** EJ"*. That is an
"or" with no rule for choosing (question 2 of the checklist). My reading of §3.5's *"It was not as clear as it
looked"* is that the unclear list is the default and EJ is the exception for builds and high-risk pieces. That is my
reading, not the text. **EJ's to settle.**

---

## 3. Where 孫子兵法 helps, and where it does not

### Where it bears

- **Have a bound, and set it before starting.** 故兵貴勝，不貴久 — *"So in war, value victory; do not value
  duration."* (作戰篇). **Basis: VERIFIED** (CANONICAL #2). The canonical design rule: *"Every loop and every run
  gets a hard cap … set before it starts. When the cap is hit the loop stops and reports its state; it does not ask
  for 'one more pass.'"* This supports **R1**, and supports setting `L` at design time rather than in the middle of
  the loop. The companion line 兵聞拙速，未睹巧之久也 is **RECALLED** (claude only). Its narrow reading praises
  nothing about clumsiness, so I do not use it to argue for a *low* limit.

- **The stop is decided by a condition, not by sunk cost.** 合於利而動，不合於利而止 — *"Move when it accords
  with advantage; stop when it does not."* With 主不可以怒而興師，將不可以慍而致戰 (火攻篇). **Basis: VERIFIED**
  (CANONICAL #14). The deepseek note's "violated by" is exactly the loop without R2: *"a retry loop whose only exit is
  'a human got tired' or 'the budget ran out'."* A limit fixed in advance is how a loop gets an exit that frustration
  cannot move. The line also suggests a second exit, *stop when the gain stops* (the check's output did not improve).
  **At the shipped default of 2 that exit can never fire before the limit**, because there are not two failures to
  compare until the limit is already reached. So I do not add it. It matters only if EJ raises `L` to 3 or more.

- **Hitting the limit is information about the plan, so the answer is not more force.** 上兵伐謀 … 其下攻城。攻城之法，
  為不得已 — *"the lowest besieges walled cities; siege is only when there is no alternative"* (謀攻篇). **Basis:
  VERIFIED** (CANONICAL #4). The minimax note's "violated by" names the move R5 guards against: *"The third failed
  verification triggers 'add four more reviewers and a longer loop', skipping the rung of rewriting the plan that was
  wrong."* Raising `L` is that longer siege. Item 4's *"goes back to the unclear list … It was not as clear as it
  looked"* is 伐謀, going back to the plan.

- **The limit guarantees an end, not a pass.** 不可勝在己，可勝在敵 … 勝可知，而不可為 (形篇). **Basis: VERIFIED**
  (CANONICAL #6; deepseek lists "bounded retries" among the defensive invariants). This sets the *level*. That the
  loop stops is the half in our control, so R1 and R2 can be MUST. That it passes is not in our control, so no value
  of `L` can be justified as "enough to succeed". This is also why R4 is a SHOULD.

- **A tension the notes expose and I do not resolve.** 求之於勢，不責於人 (勢篇), **Basis: VERIFIED** (CANONICAL #7):
  when a node keeps failing, change its structure, not the agent. The minimax note's "violated by" is *"A failing node
  is re-run with a stronger model and the run is called a success once the strong model happens to hold a line the
  design left open."* That describes item 4's tier exit when it succeeds. The tier exit is a **cost** rule (§3.5:
  cheap tier first). Sunzi does not price tiers, so the text cannot settle this. I record it: a pass on the stronger
  tier is not evidence that the piece was well designed.

### Where it has nothing to say

1. **The number.** No line in the four notes gives 2, 3 or 10, or any way to derive one. 廟算's *"more counting wins"*
   is about planning before the battle, not about how many times to retry. Reading it as "more attempts win" would be
   manufacturing a principle.
2. **Count versus time.** 久 is **duration**, and so is the canonical rule's *"iterations, budget, or time"*. The text
   cannot tell attempts from hours. If anything its word favours EJ's original time reading. Q1 is settled by this
   project's code and §3.8, not by Sunzi.
3. **What counts as one attempt.** Whether the first call counts, executor failures, `partial`, a per-node versus a
   plan-wide budget: this is bookkeeping, and the text has no view on it.
4. **Whether the limit should differ by kind of work.** Only the project's own empirical rows (B12, B17, D20) speak to
   this. The text does not.

**Left out on purpose:** 朝氣銳，晝氣惰，暮氣歸 (morale decays over the day) would fit D20's finding that later
rounds get worse. CANONICAL dropped it because its only transcription is corrupted. I cannot quote it cleanly, so I do
not use it.

---

## 4. My statements against the eight questions

| | Source | One | Unit | Can fail | Weak words | Level | Basis | Links |
|---|---|---|---|---|---|---|---|---|
| R1 | method + mine, labelled | ✓ | attempts (R3) | ✓ (`true` leak noted) | ✓ | MUST | quoted + n=1 | none |
| R2 | mine | ✓¹ | attempts, per node | ✓ | ✓ | MUST | read | refers to item 4 (same list) |
| R3 | mine + quoted §3.8 | ✓ | worker calls | ✓ | `partial` **open** | definition | read + quoted | §3.8 item 5, quoted |
| R4 | **open** | ✓ | attempts | ✓ (missing or `TBD` default) | ✓ | SHOULD | n=0 guess, review trigger EJ's | none |
| R5 | mine, proposal | ✓ | attempts vs default | ✓ | ✓ | SHOULD + record | n=0 | uses R4's default |

¹ R2 says "no further attempt **and** take the exit". I kept that as one statement because both halves are a single
event, the stop. If a reviewer reads it as two, split it.
