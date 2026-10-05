# deepseek-v4-pro — completing "A limit on attempts."

Engine: deepseek-v4-pro. Brief: `runs/20261005-attempt-limit/BRIEF.md`. The statement being completed is
`docs/WORKFLOW_DESIGN_METHOD.md` §3.5, loop-ready list, item 2 (before today's rename: *"A limit on attempts."*).

## 1. The completed requirement

One statement. The checklist's "one thing" passes (CHECK.md: "one condition on a piece"), so this stays **one**
requirement, not two. The time bound that the old wording accidentally pulled in is a *different* requirement
(3.8's 8-hour ceiling) and is kept out of this one — see answer 4.

**R1 — the attempt limit**

| field | content |
|---|---|
| **Statement** | Every loop SHALL stop after at most N attempts, where N is a positive integer and one attempt is one run of the repair step (one fresh, bounded call per 3.8.1). |
| **Source** | EJ's agreed method — `WORKFLOW_DESIGN_METHOD.md` §3.5 item 2, as renamed 2026-10-05: *"a limit on the **number** of attempts — a count, not a time limit."* The presence-and-positivity half is already enforced by `design_gate.py:269`. |
| **Unit** | attempts — a **count** of repair runs. One attempt = one run of the repair step = one fresh bounded call (3.8.1). Explicitly not a duration; a duration is 3.8's 8-hour ceiling, a separate requirement that must keep using the word "time", never "attempts". |
| **Value** | `open`. No number is sourced anywhere. |
| **One failing input** | `limit` absent, empty, `TBD`, `0`, `-1`, or a non-integer (`"two"`, `1.5`, `null`) — each is refused today by `design_gate.py:269` ("node … loop has no attempt limit"). |
| **Level** | MUST for the existence of the bound (a safety matter, below). The *number* N is a SHOULD — a default, overridable per node with a written reason — because "how many attempts" is a tuning default, not a safety bound; RFC 2119 §6 (VERIFIED) forbids MUST for a method. |
| **Basis** | The *existence* rule is quoted from the method (EJ's agreed text), so it is not a guess. The *number* is `n=0`: the corpus's `limit: 2` is the harness's emitted default, not a decision — CHECK.md records this. |

Why the existence half earns MUST: an unbounded loop never stops, cannot be watched, and leaves nothing to resume
from (the method's own §3.4 and §3.8 language). RFC 2119 §6 (VERIFIED) names "limiting retransmisssions" as exactly
the class of behaviour that earns a MUST — a retry limit is that class. A method preference is not.

### The value, and what fails for being too high

CHECK.md's sharpest finding is not the missing number but this: **`limit: 99` passes every gate in the project.**
The upper side has no failing input. I will not fix that by inventing a maximum, because a maximum is the same
thing as the value, and the value is not mine to set. So:

- **Today the upper side is honestly unenforced.** That is a stated gap, not a hidden one: the requirement binds
  the *lower* side (there must be a finite positive count) and leaves the *upper* side (how high is too high) open
  until EJ names N.
- **The moment EJ sets N**, `limit > N` (for the tier N is set on) becomes the missing failing input, and
  `design_gate.py`/`check_plan` should reject it exactly as they reject absence today.

**What I would ship meanwhile.** Keep the corpus's existing `limit: 2` as the placeholder default, marked `n=0` and
recorded as "pending EJ's number" — not as a decision. I do not change it, because (a) changing it to some other
number would be inventing a new value, and (b) 2 is already what the fixtures emit, so shipping it changes nothing
while the label fixes the attribution. Escalation to a stronger tier is a *fresh node with its own limit* (3.5
item 4), so each node carries its own number anyway; a single global value would not survive that structure.

## 2. The five answers

1. **Unit — count or time?** Count. One requirement, not two. EJ read the old wording as a time bound and the
   method means count; the rename at 3.5 already settled this. Time stays 3.8's 8-hour ceiling, which is its own
   complete requirement and passes all eight questions (FINDINGS, "The ceiling"). The two must never share the word
   "attempts" again.

2. **Value — what number, and does it differ by tier or kind?** `open`. No source gives a number: not the method
   (n=1, "tried on nothing yet"), not `TASK_TYPES.md` (its `limit: 2` is a fixture, and CHECK.md traces 2 to the
   harness, not to a decision). Whether it differs by tier or kind is also open — the method's structure already
   implies per-node values (each node's loop has its own `limit`), so a per-node default set once by EJ is the
   natural shape, but I will not assert it as decided.

3. **Who sets it — designer per node, or a TASK_TYPES.md default?** The designer sets it per node, and that is
   already the mechanics: the gate reads `loop.limit` off each node. Whether `TASK_TYPES.md` should carry a
   *decided* default (rather than the fixture's 2) is open — that is the one place a default belongs if EJ wants
   one, because it is the table `design_gate.py` parses.

4. **Interaction with 3.8's 8-hour ceiling — inside or separate?** Separate. The ceiling is 3.8's, already
   complete, and already a passing requirement. This requirement is the count; the ceiling is the time. They were
   "wearing the same three words" only in the old wording, and the rename is what un-wears them. Re-merging them
   would recreate the exact ambiguity the check caught.

5. **At the limit — is the tier exit the only exit, and what when there is no stronger tier?** The normal exit is
   the check passing; the limit is the *failure* exit. At the limit, 3.5 item 4's tier escape applies: a fresh node
   on a stronger tier with a short handoff note and its own limit; when that limit is hit too, or there is no
   stronger tier, the piece returns to the unclear list or to EJ ("it was not as clear as it looked"). I am
   restating item 4, not adding to it.

## 3. Where 孫子兵法 helps, and where it does not

Quotes are from the four notes only, with their Basis labels.

**Where it bears on this requirement.**

- **That there must be a hard cap at all — an ending over dragging on.** CANONICAL #2, *"Bound the duration: value
  an ending over dragging on"* — 故兵貴勝，不貴久 ("value victory, not duration"), Basis **VERIFIED**. Its design
  rule is the requirement in miniature: *"Every loop and every run gets a hard cap … and a stop condition, set
  before it starts. When the cap is hit the loop stops and reports its state; it does not ask for 'one more
  pass.'"* This is the classical warrant for the existence half (MUST): the loop must end on a decided condition,
  not on exhaustion of patience.

- **What the limit is *for* — stop when the gain stops, not when sunk cost says continue.** CANONICAL #14, *"Act
  only on named advantage … and stop when the gain stops"* — 合於利而動，不合於利而止 ("move when it accords with
  advantage; stop when it does not"), Basis **VERIFIED**. Its design rule: *"Every loop has an objective stop
  condition ('we are no longer gaining'), and stopping is decided by that condition, not by sunk cost, impatience
  or frustration."* This is the honest reading of *why* "one more pass" is forbidden after the limit: the next
  attempt is bought only on named advantage, never on having already paid for the last one.

- **That bounded retries are a defensive invariant, not an optimisation.** deepseek-v4-pro #4, 先為不可勝 ("first
  make yourself impossible to defeat"), Basis **VERIFIED** — its design rule names *"bounded retries"* in the list
  of things to build first *"so the worst outcome is 'no progress', never 'damage'."* The attempt limit is
  loss-prevention: it caps the cost of a piece that cannot pass, rather than improving the chance a piece passes.

**Where a strategy text has nothing useful to say.**

1. **The number itself.** 兵貴勝，不貴久 says an ending beats dragging on; it does not say *after how many tries*.
   No note carries a count, and none should be read as one. That is exactly why the value is `open`: the classical
   source gives the shape (a cap exists, and the cap binds) but is silent on the magnitude, and no measurement in
   this repo supplies one either.

2. **The count-versus-time ambiguity.** "Attempts" meaning either a count or a duration is a modern lexical problem
   — one term, two meanings, two sections — which is requirements-engineering (Berry et al., and the checklist's
   "unambiguous"/"complete" items), not strategy. 孫子兵法 has no concept of "attempts" as a measurable unit
   distinct from wall-clock time, so it cannot tell you to write "a count, never hours"; that sentence comes from
   the method's own rename, not from any classical line.

3. **The mechanics — which field, which gate, who sets the default.** The JSON field `loop.limit`, the
   `design_gate.py:269` presence check, and whether the designer or `TASK_TYPES.md` supplies the default are
   workflow mechanics. The notes themselves say this is out of scope — CANONICAL, "What this domain cannot supply",
   #3: *"A concrete org chart, message format, or decision protocol … must be supplied by the designer. Treating
   孫子兵法 as a source of workflow mechanics is a category confusion."* I am applying that caveat to my own answer:
   the two things I quoted bear on the *policy* (cap exists, cap binds, cap stops), and nothing in the notes tells
   me the field name or the number.
