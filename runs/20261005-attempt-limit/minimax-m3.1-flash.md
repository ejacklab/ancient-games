# Completing "A limit on attempts" — minimax-m3.1-flash

**What I was asked:** write the requirement 3.5's loop-ready item 2 should have been. Not defend it, not
criticise it.

**My angle:** the 孫子兵法 and game-strategy reading. That turns out to matter more than I expected, and not
for the reason I assumed. The classical source gives a strong reason the cap must be *small* and a strong
reason the cap must *not be the stop condition* — and the second one means a bare count, however well
written, is the failure mode the text names. Details in §3.

**Disclosure:** a `grep` I ran for `max_calls` returned two lines of `claude-opus-5-5.md` in this directory
before I noticed the file existed. I did not read the file and did not use those lines; the `max_rounds`
findings below are my own, and I re-derived each one by running the code. Flagging it because the brief
said work blind.

---

## 0. What I measured before writing anything

Everything below that says "today" or "passes" was run, not read.

| # | Measurement | Result |
|---|---|---|
| M1 | `design_gate.py` on its own good design, `loop.limit` mutated | rejects `absent`, `null`, `0`, `-1`, `""`, `"2"`, `1.5`, `true`, `[]`. **Accepts `99` and `10**9` with zero findings.** |
| M2 | Loop fields across every design in the repo | 170 loops in 165 files. **166 are `limit: 2`; 4 are `limit: 1`.** The 166 are a **hard-coded literal in the generator** — `tests/workflows/corpus_check.py:111` writes `{"limit": 2, "exit": "fresh node on stronger tier with handoff note", ...}` for every loop category, and `:101` does the same for the `others` scoping node. Only **2 distinct `exit` strings and 2 distinct `feedback` strings** exist across the 83 loops of the 300-design corpus, because two lines of a test file wrote them. |
| M3 | The four hand-written `limit: 1` loops | `runs/20261004-bugfix-13/design.json` n1-spec, and `runs/20261004-domain-fix-review/design.json` n1/n2/n3. Each one's `exit` says *"repairs …; a **second** failure blocks the node"* — which describes a repair the limit of 1 forbids, under the reading where the limit counts attempts. |
| M4 | `dispatch.py` with a check rigged to pass on the 3rd call, `max_rounds` = 1/2/3/4 | `max_rounds: 2` → **2 attempts**, then blocked. `max_rounds: 3` → 3 attempts, done. A node with **no `repair` field blocks after 1 attempt whatever `max_rounds` says** (`:294`). |
| M5 | `check_plan` with `budget.max_rounds` = `10**9`, `-5`, `"two"`, `true` | **All four accepted — `check_plan` never validates `max_rounds` at all.** Running them: `10**9` runs unbounded; **`"two"` crashes mid-run with `TypeError: '>=' not supported between instances of 'int' and 'str'`** at `dispatch.py:294`; **`-5` and `true` both silently cut the loop to 1 attempt** (`rounds >= -5` and `rounds >= True` are both true after the first failure). |
| M6 | A plan with **no `budget` key** | Silently takes `DEFAULT_BUDGET` (`:65`). Nothing fails, and nothing is recorded as defaulted. |
| M7 | The only two real loops in this repo | `runs/20261003-node-workdir`: gate failed round 1, dev attempt 2 fixed it, gate passed. **2 attempts, second one succeeded. n=1.** `20260919-plan-critic-issues.md`: 3 rounds, 6→5→4 problems, never closed; EJ raised `MAX_PLAN_ROUNDS` 2→3 and it still did not close. **n=1.** |

M1–M3 are the reason this is not one sentence. M4–M6 are why it is not two.

---

## 1. The completed requirements

The inherited statement is one condition on a piece. Completing it honestly needs **three**, and the
checklist's own verdicts point at all three: question 3 fails because there is no value, question 4 is HALF
because only presence is checked, and question 1 asks whether the unit is a count or a time (the rename on
2026-10-05 settled time-vs-count; it did not settle **attempts-vs-retries**, which is the off-by-one the
gate cannot see).

---

### R1 — A loop declares how many attempts it may make, and what one attempt is

| field | |
|---|---|
| **Statement** | A loop-ready piece **SHALL** state `attempts`: the maximum number of attempts that piece may make, as an integer ≥ 1, together with the word that fixes what the number counts — `attempts` (each run of the work step, the first one included) or `retries` (each *additional* run after the first). |
| **Source** | **The method, 3.5's loop-ready list item 2** (`docs/WORKFLOW_DESIGN_METHOD.md:273`), inherited from the pre-2026-10-05 wording *"A limit on attempts"* via commit `6fa569c`. The **unit** half is **mine**, 2026-10-05, from M3: the repo already contains the same number meaning two different things. |
| **Unit** | **The word the design chooses, stated in the design.** Two units are in live use and they are off by one: *attempts* (inclusive — `1` means one call, no retry) and *retries* (exclusive — `1` means one call plus one retry). `intake.js:206` uses the first (`attempt_limit: '1 for pattern step'`, and a pattern step does not retry). `runs/20261004-bugfix-13/design.json` n1-spec uses the second (its exit text describes a repair its own limit of 1 forbids). Until the design says which, `1` is ambiguous. |
| **Value** | **Not applicable — R1 constrains the declaration, not the number.** The number is R2. |
| **One failing input** | `limit: 1` on `runs/20261004-bugfix-13/design.json` n1-spec, whose `exit` says *"repairs the spec; a second failure blocks the node."* Under the *attempts* reading the exit describes work the limit forbids; under the *retries* reading it is fine. **The same number, two meanings, in one file — and it passes `design_gate.py` today** (M1). Also failing, and already rejected today: `absent`, `0`, `""`, `"2"`, `true`. |
| **Level** | **MUST.** Two reasons, and the second is quoted. (i) It is a gate the project already runs — `design_gate.py:266-276` — and RFC 2119 §6 (**VERIFIED**, fetched 2026-10-05, quoted in `FINDINGS.md` §"Verification pass") says a MUST-level imperative is for behaviour "which has potential for causing harm (**e.g., limiting retransmissions**)". A repair loop retrying an LLM call *is* a retransmission; the RFC names our case almost literally. I note the fit is an analogy, not a naming of our case. (ii) A loop with no declared unit is not runnable by a machine, which is the whole point of 3.6. |
| **Basis** | **Measured** for the ambiguity: M3, read from the files. **Measured** for the presence half: M1. The *word* `attempts` vs `retries` is **my domain reasoning**, `n=0` — but it is forced, because the repo uses both. |

---

### R2 — The number is bounded above, not merely present

| field | |
|---|---|
| **Statement** | A loop's declared attempt count **SHALL NOT** exceed **3**. |
| **Source** | **EJ, 2026-10-05 — by way of this brief, which asks for a value and accepts `open`.** I am nominating 3 as the default to ship; the number itself is not mine and not the method's. Nothing in the repo or the classical source states a ceiling — the corpus's `2` is a **test-file literal** (`FINDINGS.md` §5 failure 4 says so; M2 pins it to `tests/workflows/corpus_check.py:101,111`). A number written by the thing that generates the corpus is not a source for the number. |
| **Unit** | Attempts, in whichever unit R1 fixed. The ceiling is in the same unit as the declaration, so `3 attempts` and `3 retries` are different bounds and the design says which. |
| **Value** | **3.** Derivation, both terms `n=1`: **2** is measured sufficient (`20261003-node-workdir`, M7) and **3** is measured insufficient to converge (`20260919-plan-critic-issues.md`, M7 — three rounds, 6→5→4, never closed). The useful band is 2–3, so the ceiling goes at the top of it: `limit: 2` passes, `3` passes, `4` fails. Status **TBR** — review when `docs/TASK_TYPES_LEDGER.md` has 10 rows recording a loop that exhausted its limit. |
| **One failing input** | **`loop.limit: 99` — passes `design_gate.py` with zero findings. So does `10**9`** (M1). Both should fail. A design is currently able to buy ten thousand attempts by writing the number, which is the same defect as a check that "can only be non-empty", in a different field. |
| **Level** | **MUST.** Same RFC 2119 §6 clause (**VERIFIED**): this is the half that limits harm, and 99 is not a limit. Note the asymmetry with the *value* below — the bound is a gate; the choice within it is not. |
| **Basis** | **Measured, n=2, one observation each, and both from this repo.** That is a thin basis for a hard gate and I will not pretend otherwise: `n=1` in each direction is enough to reject 99 and to justify 3, and not enough to justify 3 over 2 as *the* number. Marked TBR for that reason. |

**The default I would ship meanwhile, and the tier split I am not inventing.** Default **2** for a
script-checked repair loop, **1** where a second attempt would receive the same information. That conditional
is not my invention — it is the repo's own, in `enhance-ancient-games.js:191-192`, from the 2026-09-19 run
that was rejected three times:

> `max_attempts` is 1 unless a later attempt would really use verification feedback; then bound it (at most
> 2) and state the stop condition in `acceptance`.

**Quoted, 2026-09-19.** This is the best available basis for a value and it is a *rule*, not a quota: 1 by
default, 2 when the second attempt would really use new information. The corpus's uniform `2` (M2) is the
degenerate case of that rule with the condition always true. I am **not** nominating a per-category table,
because I have `n=0` for every row of one and a table of guesses is worse than one honest default.

---

### R3 — The number the runner enforces is the number the design declared

**This requirement is not in the inherited wording at all.** I flag that explicitly, as the brief asks. It
is not in 3.5's list, and the checklist did not ask for it. I include it because without it R1 and R2 are
decoration, and because this repo spent 2026-10-05 converting a prose rule into an enforced one
(commit `6fa569c`: *"And the rule is enforced, not prose"*) — a declared limit the runner silently ignores
is the exact failure that commit was written against.

| field | |
|---|---|
| **Statement** | A dispatch plan's enforced attempt bound **SHALL** be derivable from the design's declared count, and a plan whose `budget.max_rounds` is absent, not an integer ≥ 1, or inconsistent with the design's `attempts` for any node it runs **SHALL** be refused. |
| **Source** | **Mine, 2026-10-05**, from M4–M6. Method 3.6's "Every node carries five things, so that it can be run, checked and resumed without asking anyone" is the requirement this serves; 3.5 item 2 is the number it serves. No existing source states it. |
| **Unit** | Attempts, per node. The design declares per node; the plan currently declares one number for the whole plan (`dispatch.py:41`, `DEFAULT_BUDGET = {"max_rounds": 2, "max_calls": 30}`), so the two are in different units as well as different places. |
| **Value** | Not a number — a **relation**. Today there is none, and that is the finding. |
| **One failing input** | Three, all of which pass today: **(a)** `loop.limit: 3` in a design, dispatched under `budget.max_rounds: 2` — the run stops at 2 and the design said 3. **(b)** `loop.limit: 2` on a node with **no `repair` field** — `dispatch.py:294` blocks it after **1** attempt, whatever the plan says. **(c)** `budget.max_rounds: "two"` — a string, accepted by `check_plan` (M5), which then raises `TypeError` mid-run instead of refusing the plan. Also **`budget` absent** → `DEFAULT_BUDGET` silently, nothing recorded (M6). |
| **Level** | **MUST.** A declared number the runner ignores cannot fail, and a rule that cannot fail is not a rule (`FINDINGS.md` §1, *verifiable*; and this repo's own `FINDINGS.md` failure 3, where a check that only checked non-emptiness was the day's main finding). |
| **Basis** | **Measured**, M4/M5/M6, all three run today. `n=3` distinct defects, one run each. |

**What R3 exposes that R1 and R2 cannot.** A limit on a *piece* is not a limit on a *run*. 3.5 item 4 says
the escalated node "has **its own limit**", so the count is per node per tier — and nothing in the method
bounds the product. A three-tier piece with a limit of 2 may make **6** attempts, and the corpus has no
field that could say otherwise (M2: 2 distinct exit strings, both "fresh node on stronger tier"). I am
**not** writing a rule for the product — that would be a fourth requirement invented from nothing. I am
recording that the multiplication is currently unbounded and belongs on EJ's list.

---

## 2. The five questions `CHECK.md` leaves

**1. Unit — count or time, or two requirements?**
**A count, and the time bound is a separate requirement that already exists and already passes.** The
count/time ambiguity was real and was fixed on 2026-10-05: 3.8 now carries the 8-hour ceiling, sourced
(EJ, quoted in commit `6fa569c`), `n=0` marked, and **enforced** — `check_plan` refuses an
`outer_timeout_s` past `MAX_CALL_SECONDS` (`dispatch.py:103`), and `FINDINGS.md` records it as the one rule
that passes all eight. So it is not part of this statement; it is its neighbour, and merging them is what
caused the original defect. **But the count is still not one unit.** It is two — *attempts* and *retries* —
and the repo uses both (M3). R1 fixes that by making the design say which. Three requirements, not two: the
unit, the bound, and the agreement between the declared number and the enforced one.

**2. Value — what number, and does it differ by tier or by kind of piece?**
**Ceiling 3, marked TBR, `n=2` (M7). Default meanwhile 2, or 1 where a second attempt gets nothing new** —
that conditional is quoted from `.claude/workflows/enhance-ancient-games.js:191-192` (2026-09-19), not
invented by me. **It does differ by tier, and that is a finding, not a design choice:** 3.5 item 4 gives each
escalated node "its own limit", so the count is per node and a three-tier piece may make 6 attempts, with
nothing in the method or the design format bounding the product. **I would leave the per-category split
open.** I have `n=0` for every row of such a table, and `docs/TASK_TYPES.md`'s category rows carry no
attempt default today — the corpus filled 2 into all of them from outside. A table of guesses would be
worse than one honest default, and the ledger (3.4: "that ledger is how the defaults earn their n") is the
mechanism that would fill it.

**3. Who sets it — the designer per node, or a default from `TASK_TYPES.md`?**
**Both, in that order, and the gate's job is the ceiling, not the value.** The category row supplies the
default (3.4's default-first design; `TASK_TYPES.md:298` already carries a `loop` block in its example JSON);
the designer may go **below** it with a reason, and may not go above 3 (R2). The reason the value cannot be
the designer's alone: a designer writing the number has an interest in the number being large, and M2 shows
what happens without a ceiling — 166 identical declarations, every one written by
`tests/workflows/corpus_check.py`, not one of them a decision. **The ledger is what turns `open` into a number**, and it already exists for this purpose.

**4. Interaction — does 3.8's 8-hour ceiling belong inside this requirement?**
**No. They are different quantities and they should stay in different sections** — and I want to be careful
here, because "keep them apart" is the answer that costs nothing. The reasons it is *right*: (i) they bound
different things (a count of calls vs. the duration of one call); (ii) they fail differently — a call that
hits the ceiling is an **executor failure**, which blocks the node and reports (3.8 item 5), and per that
same item executor failures **do not count against the attempt limit**; (iii) R1's unit problem would return
in a new place if they were merged, which is precisely how the original sentence went wrong. **The one
thing that must be said, and is not said anywhere: their product is a third quantity.** Two attempts × 8 h
= 16 h of wall clock on one node, with no rule anywhere in the method or the code. I do not think that needs
a new gate — 3.8 item 2 already requires the design to list its timers **with its cost estimate**, and a
16 h node is a cost-estimate line. So: no new rule, one line that should be in the cost estimate, and if EJ
wants it enforced rather than estimated, that is a fourth requirement and it is his to call.

**5. At the limit — is item 4's tier exit the only exit, and what if there is no stronger tier?**
**Item 4 already answers the second half correctly** (back to the unclear list or to EJ, "It was not as
clear as it looked") and I would not change a word of it. **On "is it the only exit": yes, for the loop —
and that is the problem.** There is exactly one exit, it fires on a counter, and so the counter *is* the
stop condition. CANONICAL #14's design rule, **VERIFIED** (火攻第十二, fetched by minimax and deepseek), says
stopping is decided by an advantage condition and "not by sunk cost, impatience or frustration", and its
*Violated by* is, in the note's own words: **"a retry loop whose only exit is 'a human got tired' or 'the
budget ran out'."** A bare attempt count *is* the budget running out. So the loop's exit has to carry a
second thing beside the counter: **what changed between the attempts, and what the check said each time** —
so the node reaching its limit produces a finding rather than a decision to try again. That is the one
place where the classical source changed my answer, and §3 sets it out.

---

## 3. Where 孫子兵法 helps, and where it does not

### Helps — five things, all quoted from the four notes, with their Basis labels

**(a) The cap exists because each attempt is a day of the army in the field.**
「故兵貴勝，不貴久。」— *"So in war, value victory; do not value duration."* (作戰篇) — **Basis: VERIFIED**
(`CANONICAL.md` #2; `minimax-m3.1-flash.md` #3 — the line sits between two cost lists, a hundred thousand
troops burning a thousand gold a day, and seven tenths of a household's means consumed).
*What it settles:* **why the cap is small.** Not tidiness — arithmetic. One attempt is one unit of the same
currency the chapter is counting, so `limit: 2` means two days and `limit: 99` means a campaign that eats the
state. It also gives R1's unit its meaning: an attempt is a unit of *expenditure*, which is why counting
them is the right thing to do at all. **What it does not settle:** the number. The chapter argues that
expense is fatal and says nothing about how many days is too many. I checked — the notes carry no attempt
count anywhere.

**(b) The cap is the price of admission to the expensive tier, and the ladder must be walked in order.**
「故上兵伐謀，其次伐交，其次伐兵，其下攻城。攻城之法，為不得已。」— *"The best general strikes at plans, next
at alliances, next at armies, and the lowest besieges walled cities; siege is only when there is no
alternative."* (謀攻篇) — **Basis: VERIFIED** (`CANONICAL.md` #4, all three notes; `minimax` #2 and
`deepseek` #3 VERIFIED, `claude` #4 RECALLED).
*What it settles:* **why 2 and not 99, from the cost side rather than the discipline side.** 攻城之法，為不得已
— the siege happens *only* when there is nothing cheaper left, and reaching it is itself the evidence
that the cheap rungs failed. A cap of 99 means you buy the strong tier without ever demonstrating the weak
one cannot do the piece, which is the method's own stated reason for escalating (`WORKFLOW_DESIGN_METHOD.md`
`:286-290`, EJ 2026-09-22, `n=0`). So the cap is not a brake on persistence; **it is the receipt for the
escalation.** That reframing is why R2's value is a ceiling rather than a preference: the whole design rests
on the cheap rung being given a fair, bounded hearing.

**(c) A cap is a claim on a fixed pool — this is where the interaction in Q4 comes from.**
「無所不備，則無所不寡。」— *"Guard everywhere and everywhere is thin."* (虛實篇) — **Basis: VERIFIED**
(`CANONICAL.md` #11, fetched by deepseek; minimax quoted the same sentence inside its asymmetry principle).
*What it settles:* **the ceiling's number is not free.** The chapter's sentence is a four-part clause —
guard the front and the rear is thin, and so on — and `CANONICAL`'s reading is that the part that carries
is the budget arithmetic, not the battlefield image. Every attempt spent re-running is one not spent on the
sabotage check (3.5 item 5) or the independent verifier (3.6). This is the strongest argument for a **small**
number that does not depend on the text's being about war, and it is also the honest answer to Q4: the pool
is finite, the 8-hour ceiling and the attempt count are two withdrawals against the same pool, and their
product is a third withdrawal nobody has written down.

**(d) A second attempt that repeats the first is not a second attempt.**
「故善戰者，求之於勢，不責於人，故能擇人而任勢。」— *"The skilled fighter seeks it in the configuration
(勢), and does not demand it of individuals; thus he can choose the right people and set them in the
configuration."* (勢篇) — **Basis: VERIFIED** (`CANONICAL.md` #7, all three notes).
*What it settles:* **the sharpest thing I can add to the unit.** `CANONICAL`'s design rule: *"When a node
keeps failing, change its structure first — inputs, check, contract, stop condition; only then ask whether
the agent erred."* And its *Violated by*: *"Answering a recurring error by appending 'IMPORTANT: verify
your work' instead of adding an independent check."* So R1's unit should be read as: **an attempt is a run of
the work step in which something structural differs from the previous run.** An identical rerun is not an
attempt, it is the first one again — and a loop that counts those is counting nothing, which is why the
unit needs stating at all. This is the game-strategy reading of a retry, and I have not seen it stated
anywhere in `WORKFLOW_DESIGN_METHOD.md`.

**(e) The one that changed my answer: a bare count is the failure mode, not the fix.**
「非利不動，非得不用，非危不戰。」and「合於利而動，不合於利而止。」— *"Do not move without advantage, do not
employ troops without obtaining, do not fight unless at risk… Move when it accords with advantage; stop when
it does not."* (火攻篇) — **Basis: VERIFIED** (`CANONICAL.md` #14, fetched by minimax and deepseek).
*What it settles:* **the count may not be the stop condition.** The same gate governs starting and stopping,
and `CANONICAL`'s design rule requires "an objective stop condition ('we are no longer gaining')", decided
by that condition and not by exhaustion. Its *Violated by*, in the note's own words, is a retry loop whose
only exit is **"a human got tired" or "the budget ran out."** 3.5's list, completed naively, produces exactly
that sentence: a counter, and an exit that fires when the counter is spent. **So the completed requirement
has to say what the node produces when it stops.** Not "blocked" — the last feedback, what changed between
attempts, and the check's own verdict each time, so a limit reached is a *finding about the piece* and not a
decision to try once more. This is why §2 Q5 is not answered with "yes, item 4 is the only exit" and left
there. It also has a hard counterpart: 「勝可知，而不可為。」— *"victory can be known, but not made"*
(形篇) — **Basis: VERIFIED** (`CANONICAL.md` #6) — the loop may guarantee that it stopped and reported; it
may not promise the piece passed. So the report at the limit must not be phrased as a success.

### Does not help — four things, named honestly

1. **The number.** Not 2, not 3, not 99. 兵貴勝不貴久 says *bound* the duration; it does not say *at what*.
   I looked for an attempt count across all four notes and there is none — no line yields one, and the
   ceiling in R2 is `n=2` from this repo's own two loops, not from the text. Any expert who attaches a
   classical number to this requirement has manufactured one.

2. **Attempts or retries — the off-by-one.** 兵法 is a text of principles, not a spec, and
   `CANONICAL.md`'s own "What this domain cannot supply" §3 says so in terms: *"it is a text of principles,
   not a spec; every concrete design detail — who reports to whom, what the state file looks like — must be
   supplied by the designer. Treating 孫子兵法 as a source of workflow mechanics is a category confusion."*
   Whether `limit: 1` permits one call or two is bookkeeping about our own result files. The text has no
   opinion and should not be asked.

3. **Whether the runner honours the declared number.** R3 is entirely a code fact (M4–M6) and no strategy
   text bears on it. Same for the reason it matters here: `CANONICAL` §1 records that the domain cannot
   supply a rule for honest intra-team state sharing, and a silently-ignored field is a state-sharing
   problem wearing a limits problem's clothes.

4. **The temptation I declined.** 「兵者，詭道也」— *"war is the way of deception"* — is the line one reaches
   for when thinking about retries and exhaustion, and it is the wrong reach: `CANONICAL.md` drops it
   ("Describing deceiving an adversary… a workflow that hides its state from its own verifier is abusing
   the line, not obeying it"), and `minimax` #4 flags its own mapping as **"Loose."** I am recording that I
   considered it and rejected it, because the honest version of this section is the one that says where the
   text runs out.

---

## 4. What I would change, in the order I would change it

1. **R1**, because the two-unit ambiguity is live in checked-in designs today (M3) and no gate can see it.
2. **R2's ceiling**, because `limit: 99` passing every gate in the project (M1) is the same defect as
   `FINDINGS.md`'s failure 3, in a field nobody has looked at.
3. **R3**, because it is the difference between a rule and a field — and this repo has already had one day
   spent on that distinction.
4. **The multiplication**, flagged not fixed: a three-tier piece may make 6 attempts and nothing bounds it.
5. **The gain report at the limit** (Q5), because the classical source is unusually clear that a counter is
   not a stop condition, and because it is the one item here that changes what a node *produces* rather
   than what it is allowed to do.

**Open, for EJ, and I am not closing them by guessing:** the ceiling's number (3, TBR, `n=2`); the per-tier
and per-category split (`open` — no table until the ledger has rows); the product of the attempt count and
the 8-hour ceiling (noted, not ruled on); and whether the gain report is a gate or a line in the cost
estimate.
