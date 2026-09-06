# The Ancient Games — V3.5 Spec of Record

Revises `V3_4_SPEC.md` per `DECISIONS_V3.5.md` (Z1′–Z6′ — binding; **Y2′
stands unchanged**) applied on top of `v3_4_review.md` (REJECT: 4 BLOCKING
Z1–Z4, 2 SHOULD-FIX Z5–Z6, 0 NOTE). `V3_4_SPEC.md` is untouched. This round
is definitions-only: the reviewer's own release criterion — write B as a
pure function, `count_sources(claim, events, cap_state, framings) ->
(n_available, remedy)`, from the text alone — surfaced three missing
*definitions* (a parameter's shape, a classification boundary, a type's
missing value) and one self-check failure, none of them a defect in the
self-exclusion mechanism itself, which `v3_4_review.md` states plainly
"survived three adversarial constructions" and is **not reopened**.

---

## 1. Overview

Call order unchanged. Four fixes, all narrower than any prior round's, none
touching Y2′'s corroboration mechanism:

1. **`cap_state`'s shape is now a declared ctx property, not an inference.**
   Every round since v3.1 referenced "the plan's dispatched count so far"
   in prose; nothing ever backed it with a ctx field a pure function could
   read. §2 gains `dispatch_count: int`; `count_sources`'s `cap_state`
   argument is exactly `(dispatch_count, CAP=3)` (Z1′, closes Z1).
2. **The `claim_recorded`/`check_executed` boundary is now a stated test,
   not an asserted classification.** T1's `journal-untouched` claim turned
   on whether a bare `grep -o event_type | uniq -c` scan counts as an
   executed check (immune to actor-exclusion) or a cited assertion (subject
   to it) — v3.4 asserted the former with no stated rule. §7 now states:
   evidence is `check_executed` iff it names an explicit expected value or
   falsifying condition the observed result could have failed to match; a
   bare output citation with no stated alternative is `claim_recorded`
   even when MAIN ran the command (Z2′, closes Z2). Re-walking T1 under
   this test reclassifies the grep scan as `claim_recorded` (excluded,
   `author=actor=MAIN`) — but the real run's own `git status --short`
   check (already in `T1_trace.md`'s own Actions table, previously omitted
   from this claim's corroboration count) *does* name an explicit expected
   value ("only `loop/program_db.py` modified") and fills the gap.
   `journal-untouched` stays **2/2** — the stated test, applied honestly,
   does not manufacture a second divergence here; it is recorded as such,
   not assumed in advance.
3. **`actor` gains its third, no-producer value, typed and ruled.** §10's
   own T3 trace used `"none-distinct"`, a value §2's two-value union
   (`agent-id | MAIN`) never declared. §2 now types `actor ∈ {agent-id,
   MAIN, none}`, with `none` meaning exactly what T3 needs it to mean —
   commissioned to co-equal independent authors from the outset, no prior
   performer — and states that every author qualifies for (a) in that case
   (Z3′, closes Z3).
4. **Case (ii) now states its own tripwire in §10 itself.** v3.4's §12
   claimed `hub-touched-without-tripwire` passes for Case (ii), but §10's
   own text never named one for its non-empty hub — the identical
   "§12 asserts what §10 doesn't show" failure Y4 found, recurring one
   round later in a different lint. §10 now states it directly (Z4′, closes
   Z4).

Two SHOULD-FIX items close alongside: **Z5** (category (c)'s `mechanism`
dedup trusts a self-reported label) gets a disclosed [LLM]-judgment caveat
in §9 plus a spine-checkable partial guard in B·1 (two `check_executed`
events with identical `command` strings count once, regardless of label).
**Z6** (category (b) had no stated cardinality) is closed: (b) counts at
most once per claim, stated in B·1.

---

## 2. The ctx object

Only rows touched this round; every other row is unchanged from
`V3_4_SPEC.md` §2.

| property | type | set by | consumed by | notes |
|---|---|---|---|---|
| `actor` | map: `action_id → agent-id \| MAIN \| none` | C·3/C·4, or D at `execution_status=main_executes` | B·1 (self-exclusion test), journal `claim_recorded.actor` | **type extended (Z3′, closes Z3)** — was `agent-id \| MAIN` only. `actor(X) = none` iff `X`'s action was commissioned to multiple co-equal, independent authors from the outset, with no one of them having already performed the work before the others were dispatched to check it (T3's pattern — three research angles commissioned together, none pre-existing the others). **When `actor(X) = none`, every `claim_recorded` author on `X` qualifies for (a) by definition** — there is no producer to exclude, so (a)'s `author≠actor(X)` test is vacuously true for every author. |
| `dispatch_count` | `int`, plan-wide, monotonically non-decreasing | C·3/C·4 (incremented once per category-(a) dispatch at plan-drafting time); incremented again by B·1 for every `RETURN_TO_PLANNER`-triggered new category-(a) dispatch | B·1 (`cap_state`, the remedy's slot-remains test) | **new (Z1′, closes Z1)** — the plan-wide running count of category-(a) dispatches made so far. `count_sources`'s `cap_state` argument is exactly the pair `(dispatch_count, CAP=3)`; a slot remains iff `dispatch_count < 3`. This is what every round's prose ("the plan's dispatched count so far") meant, now backed by a declared field a pure function can actually read. |

**No other ctx row changes.**

---

## 3. Registry

Unchanged from `V3_2_SPEC.md` §3. Not reproduced — no finding this round
touches the registry.

---

## 4. The five algorithms

Step counts unchanged: C=5, D=5, B=5, E=7, A=3 (25 steps total). Only B·1
(Z1′/Z2′/Z5′-item-2/Z6′) and B·2 (unaffected, restated for completeness)
change text; C, D, E, A are unchanged from `V3_4_SPEC.md` §4 and
reproduced in full below.

### C — Gate(task)
**Input:** `task`
1. `[spine+LLM]` (#5, #31, R3, S2) For the cheap-means probe's target, read `artifact_refs.mode`. If `mode=read`: never gate it — proceed straight to cheap means, recording each command's actual output into `ctx.known_facts`. If `mode∈{invoke,mutate}` and the target matches a registry hub (§3): treat the probe itself as an action and run it through Guard(D) first; execute only if D returns `stakes=1` (no gate). If answered, go to exit 1.
2. `[spine+LLM]` (#9, D3) State the task's difficulty and needed capability as falsifiable assumptions; separately, set `governance_gated = <registry row id>` only if the task's own `stop_criterion` is itself a recommendation or decision on a registry row whose `gate=owner`.
3. `[spine]` (F1) Feed difficulty + capability into the F1 decision tree → agent count; set `execution_status = dispatched` if `count≥1`, else `execution_status = main_executes`; set `ctx.actor` for each drafted action (an assigned agent, `MAIN`, or `none` per §2's Z3′ rule when the action commissions co-equal independent authors from the outset); increment `ctx.dispatch_count` once per category-(a) agent this plan dispatches.
4. `[spine]` (F1, R1) If count > 3: partition step 2's success criteria into the fewest groups whose re-run of step 3 each yields ≤3; run steps 1–5 per group independently; output `PLAN_NEEDED[]`, one entry per group.
5. `[LLM]` (#12) Declare the stop criterion and a time-box for drafting, before drafting starts.

**Exit conditions:**
- Step 1 answers the task → `RESOLVED(evidence)`.
- Step 4 splits → `PLAN_NEEDED[]`.
- Else, after step 5 → `PLAN_NEEDED(count, difficulty, stop_criterion[, governance_gated], execution_status)`.

**Output:** `RESOLVED(evidence)` | `PLAN_NEEDED(count, difficulty, stop_criterion, execution_status)` | `PLAN_NEEDED[]`

### D — Guard(action)
**Input:** `action`. Step order: `refs → registry → reversibility → fallback/tripwire → gate`.
1. `[spine]` (#21, S2) Set `artifact_refs.mode ∈ {read, invoke, mutate}` for everything this action touches.
2. `[spine]` (#21, R7, S1, D2′, D6) Look up every `invoke`/`mutate` ref against §3, no exit before it; find every registered downstream consumer of any mutated artifact and record the answer via a `consumer_check` journal event whether or not one exists; `hub = (same-ref survivors with hub?=yes) ∪ (consumer matches with hub?=yes)`; `stakes = max` over all matched rows in both sets; default 1 if nothing matches.
3. `[spine+LLM]` (#18, R5, S1 extension) Irreversible if (a) reverting isn't a plain VCS op (landing a commit is always plain VCS, never fires on that basis alone) or (b) an external, non-code side effect survives a code revert. Else `restorable` or `git-revertible`. Decides only fallback/tripwire shape, never whether the action gates.
4. `[spine+LLM]` (#17, #28, #18, #29, #21) Write the N−1 clause; re-read each hub element's fresh state and name one tripwire per element; record backup/redundancy or that none exists; set permissions as explicit tool grants.
5. `[spine]` (F1, D1) `stakes≥2` ⇒ checkpoint before landing; `stakes=3` ⇒ owner gate. If this is the only candidate for a `count=0` plan and its gate is `owner` with no approval on record, set `execution_status=hard_blocked`.

**Exit conditions and Output:** unchanged (`NO_GATE(stakes=1, reversibility)` | `GATED(hub, stakes, reversibility, tripwire, backup, fallback, permissions, gate)`).

### B — Corroborate(claims, stakes)
**Input:** the action's load-bearing claims, each tagged `kind ∈
{executable, judgment}` (§2's X3 test). For claim `X`: `author(X)` = a
given `claim_recorded` event's `author` field; `actor(X)` = `ctx.actor` for
the action `X` is about (`agent-id`, `MAIN`, or `none` — §2, Z3′).
`n_required(X) = max(action's own stakes from D·2, governance_gated's
registry stakes if set)`. `cap_state = (ctx.dispatch_count, CAP=3)` — §2,
Z1′. B runs once per distinct claim.

1. `[spine]` (#4, #27, R4, S3, **Y2′ [unchanged, stands], Z1′, Z2′,
   Z5′-item-2, Z6′ — the complete rule, released as
   `count_sources(claim, events, cap_state, framings) -> (n_available,
   remedy)`**) For each claim `X`, if `n_required(X)=1`: exit trivially,
   `SINGLE_SOURCE`. Else, classify every candidate piece of evidence on `X`
   per the boundary test stated in §7 (Z2′): it is a `check_executed`
   event iff it names an explicit expected value or falsifying condition
   the observed result could have failed to match; otherwise it is a
   `claim_recorded` event, regardless of who ran the underlying command.
   Query the journal for every `claim_recorded{claim_id=X}` and
   `check_executed{claim_id=X, falsifies=X}` event so classified, and count
   `n_available(X)` as the number of distinct sources among: **(a)** each
   `claim_recorded` event on `X` whose `author ≠ actor(X)` — vacuously true
   for every author when `actor(X)=none` (Z3′) — counted once per distinct
   `framing` among these; **(b)** `MAIN`'s own `claim_recorded` event on
   `X`, counted **only when `actor(X) ≠ MAIN`** and it carries
   `evidence_type ∈ {command, file:line}` with a non-empty `evidence_ref`
   — **at most once per claim, regardless of how many qualifying
   `MAIN`-authored events exist for it** (Z6′, closes Z6: (b) has no
   framing-style multiplicity the way (a) does); **(c)**, only when
   `kind(X) = executable`, each `check_executed{claim_id=X, falsifies=X}`
   event, counted once per distinct `mechanism ∈ {interpreter-import,
   pytest-fail-first, suite-count, git-diff-scope, hash-compare,
   adversarial-case, other:<name>}` among these, regardless of who ran it
   — **but two `check_executed` events on `X` whose `command` strings are
   identical count once regardless of their `mechanism` labels** (Z5′
   item 2, a spine-checkable partial guard against mislabeling; whether two
   *differently-worded* commands are honestly distinct checks remains an
   [LLM] judgment call, disclosed in §9); this is also why `X`'s own
   originating evidence counts as one source iff it is itself a `check_
   executed` event under the classification test above — a `judgment`
   claim's originating evidence can never pass that test (no command
   decides a judgment, so nothing it produces names a falsifiable expected
   value), so when that opinion's author is also `actor(X)`, it
   independently fails (a)'s and (b)'s tests too: the self-exclusion,
   unchanged from Y2′. If `n_available(X) < n_required(X)`: `kind=
   executable` ⇒ `remedy=add-claim-specific-check`; `kind=judgment` ⇒
   `remedy=add-differently-framed-source` only if `cap_state`'s
   `dispatch_count < 3` (a slot remains) **and** B·2's framing enumeration
   for this task names a framing not yet used on `X`; otherwise `remedy=
   gate-checkpoint` (`stakes≤2`) or `remedy=gate-owner` (`stakes=3`).
   Record `{claim_id, kind, capped_from, mandated, delivered, remedy}` in
   `ctx.corroboration_capped`; increment `ctx.dispatch_count` for every new
   category-(a) dispatch this remedy triggers.
2. `[LLM]` (#10, #27, Y1) Before assigning any framing, enumerate the finite set of genuinely distinct framings available for this claim — step 1's remedy check reads this enumeration for an unused entry, never an open-ended search; assign each category-(a) source a distinct entry from it, never issuing the same prompt twice, byte-for-byte or in substance.
3. `[spine]` (#8) Dispatch category-(a) sources in parallel, each to its own file; no reading a sibling's file first.
4. `[spine]` (#2, R8) Drop any claim lacking a cited command (UNVERIFIED); if every claim backing an action is dropped, remove that action from the candidate set E receives.
5. `[LLM]` (#23) Reconcile survivors per claim: note agreement (flag as suspect if framings were alike); let disagreement stand; break residual ties by dominance: irreversibility-finding > eligibility-finding > design-proposal.

**Exit conditions (per claim, rolled up per action for the exit line):**
- `n_required=1` → `SINGLE_SOURCE`.
- Else, after step 5 → `SOURCES(n_available, framings, files, reconciliation)` or `CAPPED(claim_id, kind, capped_from, mandated, delivered, remedy)`.

**Output:** per claim, `SINGLE_SOURCE | SOURCES(n,framings,files,reconciliation) | CAPPED(claim_id,kind,capped_from,mandated,delivered,remedy)`.

### E — Filter(candidates)
**Input:** `candidates` — actions/findings surviving D and B, each pre-scored on {cost, expected value, risk, confidence}.
1. `[spine]` (#23, R11) Pareto-filter: drop any candidate dominated on every axis by another survivor.
2. `[LLM]` (#11) Fund the decisive branch: concentrate budget on what decides the outcome; cut the rest.
3. `[LLM]` (#16, R6) `FOLLOW_ON` if acting on a discovery needs a new action not yet through D/B, tagged with a disposition from `{fixed, new-task, dismissed:<reason>, escalated:<owner>}`; fold a discovery that is evidence for an already-guarded candidate's success criterion into that candidate's KEEP/MERGED, tagged discovered-not-planned.
4. `[LLM]` (#1) Per surviving dispatch, restate intent, non-delegable constraints, success criterion.
5. `[spine]` (#13, #15, #30) Each dispatch loads the same versioned doctrine, names its handoff topology and tradeoff, asserts `PRECEDENCE`, returns one artifact at one fixed path. If any surviving KEEP/MERGED entry carries `governance_gated≠none`, mark the pipeline's trailing gate owner-gated on that entry, per the registry's `owner` column.
6. `[spine]` (#25) Bound each surviving dispatch's payload/return against a declared size limit; trim before dispatch, recording the trim.
7. `[spine]` (#26, R4-schema) Name every field in the payload for what the task calls it in plain domain terms.

**Exit conditions:**
- `candidates` empty → `KEEP=[],MERGED=[],CUT=[],FOLLOW_ON=[]`.
- Else, after step 7 → `Filter: kept=<k>, merged=<m>, cut=<c>, follow_on=<f>[, governance-gated=<n>(terminal)].`

**Output:** `KEEP[]`, `MERGED[]`, `CUT[]`, `FOLLOW_ON[]`

### A — Prove(plan)
**Input:** `plan` — E's `KEEP[] + MERGED[]`, with each entry's D/B annotations attached.
1. `[spine]` (#2) Every claim shows the command that produced it; "confirmed" with no command fails.
2. `[LLM]` (#2) Every action has a check that can fail, not merely an expectation it will work.
3. `[LLM]` (#7) Every metric names the true quantity it proxies and how the two could diverge.

**Exit conditions:** all three checks plus every lint in §8 run over the whole plan; A never exits early.
- A claim in `ctx.corroboration_capped` whose `remedy ∈
  {add-claim-specific-check, add-differently-framed-source}` and has no
  recorded fix in the plan → lint `corroboration-capped` FAILs →
  `RETURN_TO_PLANNER(<remedy text>, naming the claim)`. Resume semantics
  unchanged (V7): resumes at C·3 with the capping constraint relaxed by the
  remedy; `hub`/`stakes`/`tripwire`/`actor`/`dispatch_count` persist.
- A claim whose `remedy ∈ {gate-checkpoint, gate-owner}` is never itself an
  A-blocking condition — it must appear disclosed in that claim's
  `gate_reason` set and A's own exit line; omitting the disclosure is
  itself a FAIL.
- All clean → `PASS` — `Prove: PASS, plan cleared to <checkpoint|owner> gate[, governance-gated][, corroboration-capped].`

**Output:** `PASS` | `RETURN_TO_PLANNER(findings[])`

---

## 5. Schema field table

Unchanged from `V3_4_SPEC.md` §5. No Z-finding touches a `when`/`type`/
`escape_value` cell. Not reproduced — see `V3_4_SPEC.md` §5.

---

## 6. Return contract

Unchanged from `V3_4_SPEC.md` §6 (12 rows, `FOLLOW_ON`'s four-value
disposition enum, all escape values filled). Not reproduced — see
`V3_4_SPEC.md` §6.

---

## 7. Trace journal

**The `claim_recorded`/`check_executed` classification test is now stated
explicitly (Z2′, closes Z2):**

> A piece of evidence is logged as a `check_executed` event **iff** it
> names an explicit expected value or falsifying condition that the
> observed result could have failed to match (a hash that could have
> differed, a count that could have been off, an import that could have
> errored, a diff scope that could have included an unexpected file). A
> bare citation of a command's output, with no stated alternative it was
> checked against, is logged as a `claim_recorded` event **even when
> `MAIN` is the one who ran the command** — running a command and reading
> its output is not, by itself, an executed *check*; naming what would have
> counted as failure is what makes it one.

Event shapes, otherwise unchanged from `V3_4_SPEC.md` §7:

```
{"ts":str, "run_id":str, "event":"exit",           "algorithm":str, "steps_fired":[str], "exit_type":str, "exit_line":str, "ctx_keys_set":[str]}
{"ts":str, "run_id":str, "event":"dispatch",       "agent_id":str, "role":str, "framing":str, "payload_fields":[str], "output_path":str}
{"ts":str, "run_id":str, "event":"return",         "agent_id":str, "fields":{...return contract, §6...}}
{"ts":str, "run_id":str, "event":"rule_fire",      "rule_id":str, "algorithm_step":str, "field":str, "ctx_value":any}
{"ts":str, "run_id":str, "event":"check_executed", "claim_id":str, "falsifies":str, "mechanism":"interpreter-import"|"pytest-fail-first"|"suite-count"|"git-diff-scope"|"hash-compare"|"adversarial-case"|"other:<name>", "command":str, "expected":str|num, "observed":str|num, "pre_fix_result":"FAIL"|null}
{"ts":str, "run_id":str, "event":"claim_recorded", "claim_id":str, "author":"MAIN"|str, "actor":"MAIN"|str|"none", "kind":"executable"|"judgment", "text":str, "evidence_type":"command"|"file:line", "evidence_ref":str, "framing":str|null}
{"ts":str, "run_id":str, "event":"consumer_check", "ref":[str], "answer":"no"|str, "command_or_reasoning":str}
```

`claim_recorded.actor` now accepts `"none"` (Z3′) alongside `"MAIN"` and an
agent id, matching §2's extended type. `rule_fire` remains the dormant
promote/demote substrate for #19/#22, unchanged.

---

## 8. Lints

Nine lints, unchanged in count, name, and condition from `V3_4_SPEC.md`
§8. Only the **self-lint result** for `hub-touched-without-tripwire`
changes this round (Z4′ — Case (ii) now genuinely has one, stated in §10).
Not reproduced in full — see `V3_4_SPEC.md` §8 for every lint's input/
condition/output; §12 below carries this round's self-lint scorecard,
checked against this document's own §10.

---

## 9. Convert the walls, keep the holes

Unchanged from `V3_4_SPEC.md` §9, plus one disclosed [LLM] judgment call
(Z5′ item 1, closes Z5): **"is a claimed `mechanism` label an honest
description of a genuinely distinct check, or a relabeled repeat of the
same one — [LLM] judgment call, not spine-verifiable from the event alone."**
The identical-`command`-string guard in B·1 (Z5′ item 2) catches the
*mechanical* case (the exact same command, relabeled); it cannot catch two
differently-worded commands that happen to test the same underlying thing —
that remains a human/agent judgment, now named as such rather than left
implicit the way framing's own distinctness question already was.

---

## 10. Trace test cases

All eight, self-contained (Y4′'s discipline, unchanged). **Per the
coordinator's instruction, only T1's `journal-untouched`, T3's `actor`
value, and Case (ii)'s tripwire change; every other case's numbers, events,
and outcomes are unchanged from `V3_4_SPEC.md` §10** and are stated here in
full only where needed to keep each case self-contained.

### T2 — REAL, must match `T2_trace.md` — unchanged
Gate: `PLAN_NEEDED(count=0, execution_status=main_executes)`, `actor=MAIN`.
Guard: research/tests edit → R8 → `stakes=1, hub=[]`,
`consumer_check{ref: ["research/stability.py", "tests/test_research_
importable.py"], answer: "no", command_or_reasoning: "grep -rl research.
stability across eval/,loop/ finds no registered stakes≥2 consumer"}` →
`NO_GATE(stakes=1)`. Commit → R6 → `stakes=2, hub=[R6]` → `GATED(gate=
checkpoint)`.

| claim | kind | `n_required` | events (each satisfies Z2′'s test: names an explicit expected value) | `n_available` | remedy |
|---|---|---|---|---|---|
| `import-succeeds` | executable | 2 | `check_executed{mechanism=interpreter-import, command="python3 -c \"import research.stability\"", expected="exits 0, no ImportError", observed="exit 0"}`; `check_executed{mechanism=pytest-fail-first, command="pytest tests/test_research_importable.py -q", expected="1 failed pre-fix, 14 passed post-fix", pre_fix_result=FAIL, observed="14 passed"}` | 2 | n/a |
| `no-regression` | executable | 2 | `check_executed{mechanism=suite-count, command="make test", expected=274, observed=274}`; `check_executed{mechanism=git-diff-scope, command="git diff --stat", expected="exactly research/stability.py + tests/test_research_importable.py, no other files", observed="2 files, matches"}` | 2 | n/a |

`Corroborate: import-succeeds: n=2/2; no-regression: n=2/2; reconciled=agree.`
Filter: `kept=3, cut=1, follow_on=2 (new-task; dismissed:out-of-scope)`.
Prove: `PASS, plan cleared to checkpoint gate.` **Agents: 0.**

### T1 — REAL, DIVERGES from `T1_trace.md` on `six-are-dead` (unchanged from v3.4); `journal-untouched` re-walked under Z2′ (closes Z2, stays 2/2)
Gate: `PLAN_NEEDED(count=1, execution_status=dispatched)`, `actor=MAIN` for
the deletion itself. Guard: mutate `loop/program_db.py` → R7 (dir, `hub?=
no`) ∪ R4 (`loop/program_db.jsonl`, registered consumer, `hub?=yes`) →
`hub=[R4], stakes=2, irreversible` → `GATED(gate=checkpoint)`.

| claim | kind | `n_required` | events | `n_available` | remedy |
|---|---|---|---|---|---|
| `six-are-dead` | judgment | 2 | `claim_recorded{author=MAIN, actor=MAIN, framing="text-reference-scan", evidence_type=command, evidence_ref="ast scan + grep -rnw"}` — no expected/falsifying condition named for the *conclusion itself* ("dead" is a synthesis, not a command result), and `author=actor=MAIN` excludes it from (a)/(b) independently regardless ⇒ 0; `claim_recorded{author=historian, actor=MAIN, framing="schema-dispatch-read"}` — `author≠actor` ⇒ valid (a) ⇒ 1 | **1** | `add-differently-framed-source` — judgment, `dispatch_count=1<3` (a slot remains, Z1′) **and** an unused framing exists (e.g. "independent-static-scan") ⇒ `RETURN_TO_PLANNER(add source with framing independent-static-scan for six-are-dead)` |
| `journal-untouched` | executable | 2 | **Re-walked under Z2′'s classification test:** `check_executed{mechanism=hash-compare, command="sha256sum loop/program_db.jsonl", expected="fdfa84bc… (pre-deletion hash)", observed="fdfa84bc… unchanged ×3"}` — names an explicit expected value, could have differed ⇒ (c); `check_executed{mechanism=git-diff-scope, command="git status --short", expected="only loop/program_db.py modified", observed="M loop/program_db.py only"}` — names an explicit expected scope, could have included an unexpected file ⇒ (c), a **second, independent** mechanism (already present in `T1_trace.md`'s own Actions table, previously omitted from this claim's count); `claim_recorded{author=MAIN, actor=MAIN, evidence_type=command, evidence_ref="grep -o event_type … \| uniq -c"}` — **reclassified**: names no expected value or falsifying alternative, just "count and read" ⇒ `claim_recorded`, not `check_executed`; `author=actor=MAIN` ⇒ excluded, contributes 0 (irrelevant to the total either way) | **2** (hash-compare + git-diff-scope, both genuinely (c)) | n/a — **stays 2/2, no second divergence** |

`Corroborate: six-are-dead: n=1/2, capped, remedy=add-differently-framed-
source; journal-untouched: n=2/2; reconciled=agree(journal-untouched only).`

**Z2′'s own required verification, stated plainly:** the grep-event-scan's
reclassification from `check_executed` to `claim_recorded` does **not**
manufacture a second T1 divergence, because the real run's own `git status
--short` check — already present in `T1_trace.md`'s Actions table
("scope | `git status --short` | `M loop/program_db.py` only") — genuinely
names an explicit expected scope and was simply never counted toward this
claim's corroboration in any prior round's trace. Applying Z2′'s stated
test honestly to *everything the real run actually produced* (not just to
what earlier drafts happened to cite) finds the missing second source
already sitting in the record. This is the outcome `DECISIONS_V3.5.md`
itself names as the one to record if it's what the re-walk yields — it is.

Filter still runs (E precedes A regardless of A's eventual verdict):
`kept=1(+Tuple SCOPE_DELTA), merged=0, cut=1(NetOutcomeResolver),
follow_on=3.` `FOLLOW_ON: (1) eval/forecast.py:255 NetOutcomeResolver, dead
by both methods, in eval/ (frozen-oracle surface) → escalated:ej; (2) 11
stale .claude/worktrees/agent-* trees hold an older program_db.py where
these names still have callers → dismissed:out-of-scope; (3)
loop/program_db.py's `DB_PATH` per-worktree fork (from wave 1), still open
→ escalated:ej.`

**T1's divergence, unchanged from v3.4, restated for completeness:** `A`'s
exit for the deletion action is `RETURN_TO_PLANNER(add source with framing
independent-static-scan for six-are-dead)`, not `PASS` — contradicting
`T1_trace.md`'s own recorded `PASS`/commit-awaiting-checkpoint outcome. The
deletion's *mechanical* safety (`journal-untouched`, 2/2) is fully
corroborated; its *judgment* call (`six-are-dead`) was, by this standard,
one independent head short. **Not patched.** **Agents, as actually run:
1** (historian) — **as this document's rule would have required: 2**.

### T3 — REVISED, `actor` value corrected (Z3′, closes Z3; outcome unchanged)
Gate: `PLAN_NEEDED(count=3, governance_gated=R1)`. `ctx.actor =` **`none`**
for the produce-recommendation action (not `"none-distinct"`, a value §2
never typed until this round) — commissioned to three co-equal,
independent research authors from the outset, with none of them having
performed the work before the others were dispatched to check it (§2's
Z3′ rule, matched exactly). **When `actor=none`, every `claim_recorded`
author on the claim qualifies for (a) by definition** — there is no
producer to exclude. Guard: produce-recommendation → R8 → `stakes=1,
hub=[]`, `consumer_check{ref: ["<new recommendation doc path>"], answer:
"no", command_or_reasoning: "a freshly-authored research doc has no
existing consumer yet"}` → `NO_GATE(stakes=1)`.

| claim | kind | `n_required` | events | `n_available` | remedy |
|---|---|---|---|---|---|
| `unseal-recommendation` | judgment | `max(1,3)=3` | `claim_recorded{author=spec-reader, actor=none, framing="spec-reader"}`; `claim_recorded{author=historian, actor=none, framing="historian"}`; `claim_recorded{author=statistician, actor=none, framing="statistician"}` — `actor=none` ⇒ all three authors qualify for (a) vacuously, three distinct framings ⇒ 3 | 3 | n/a |

`Corroborate: unseal-recommendation: n=3/3; reconciled=disagree,
dominance=irreversibility-finding.` Filter: `kept=1, merged=3, cut=1,
follow_on=1 (build an automated certifier → new-task), governance-gated=1
(terminal, owner=ej).` Prove: `PASS, plan cleared to owner(ej) gate
[governance-gated].` **Agents: 3.** Outcome unchanged from every prior
round — only the `actor` value's type and stated rule changed.

### Case 1 — unchanged
Guard: `hub=[R9], stakes=3, irreversible, gate=owner(ej)`, `actor=<coder>`.

| claim | kind | `n_required` | events | `n_available` | remedy |
|---|---|---|---|---|---|
| `backoff-safe-at-100ms` | judgment | 3 | `claim_recorded{author=<coder>, actor=<coder>, framing="proposer"}` — `author=actor` ⇒ 0; `claim_recorded{author=corroborator-1, actor=<coder>, framing="headroom-analysis"}` ⇒ 1; `claim_recorded{author=corroborator-2, actor=<coder>, framing="failure-mode-review"}` ⇒ 1 more | 2 | `gate-owner` — judgment, `dispatch_count=3=CAP` (`1(actor)+2(corroborators)`, no slot remains) ⇒ straight to `HUMAN_GATE(owner)`, `stakes=3`, no bounce |

`Corroborate: backoff-safe-at-100ms: n=2/3, capped, remedy=gate-owner.`
Filter: `kept=1, cut=1, follow_on=1 (new-task)`. Prove: disclosed → `PASS,
plan cleared to owner(ej) gate [corroboration-capped: backoff-safe-at-
100ms, remedy=gate-owner].` **Agents: 3.**

### Case 2 — unchanged
Guard: probe `eval.partitions.load_holdout` → R3 → `stakes=3, irreversible,
gate=owner(ej)`, no approval on record, only candidate for `count=0` →
`execution_status=hard_blocked`. B/E/A never run. **Agents: 0.**

### Case 3 — unchanged
Guard: module edit → R7 → `stakes=2, hub=[]`, `actor=<module-coder>`;
docstring edit → R8 → `stakes=1, hub=[]`, `consumer_check{ref: ["research/
*.py docstrings"], answer: "no", command_or_reasoning: "docstring text
isn't consumed/synced anywhere, unlike case (i)'s report.py"}` →
`NO_GATE`. Commit → R6 → `stakes=2, hub=[R6]` → `GATED(gate=checkpoint)`.

**First pass:**
| claim | kind | `n_required` | events | `n_available` | remedy |
|---|---|---|---|---|---|
| `liquidity-module-correctness` | executable | 2 | `check_executed{mechanism=interpreter-import, command="python3 -c \"import engine.liquidity\"", expected="exits 0, no ImportError", observed="exit 0"}` — the module-coder's own basic check, immune to actor-exclusion (regardless of who ran it) | 1 | `add-claim-specific-check` — executable, always re-plannable; no agent dispatch attempted for this claim |

`Corroborate: liquidity-module-correctness: n=1/2, capped, remedy=add-
claim-specific-check.` Prove (first pass): `RETURN_TO_PLANNER(add a
claim-specific check with mechanism pytest-fail-first for
liquidity-module-correctness)`.

**Second pass** (V7 resume): `check_executed{mechanism=pytest-fail-first,
expected="fails pre-fix, passes post-fix on spec §5.3 formulas",
pre_fix_result=FAIL, observed="passed"}` — distinct mechanism ⇒ +1 ⇒
`n_available=2=mandated` → `PASS, plan cleared to checkpoint gate (at
commit).` **Agents: 2.**

### (i) — unchanged
Guard: `research/report.py` edit → R8 (`hub?=no`) ∪ R1 (registered
consumer via the sync script, `hub?=yes`) → `hub=[R1], stakes=3,
irreversible` → `GATED(gate=owner(ej))`. `actor` = the fix+verify agent.

| claim | kind | `n_required` | events | `n_available` | remedy |
|---|---|---|---|---|---|
| `docstring-sync-match` | executable | 3 | `claim_recorded{author=fix-verify-agent, actor=fix-verify-agent, framing="fix-and-confirm"}` — `author=actor` ⇒ excluded, 0; `claim_recorded{author=independent-reader, actor=fix-verify-agent, framing="sync-script-logic-read"}` ⇒ 1; `claim_recorded{author=third-corroborator, actor=fix-verify-agent, framing="protocol-json-diff-read"}` ⇒ 1 more | 2 | `add-claim-specific-check` — executable; `dispatch_count=3=CAP` already spent, irrelevant to this remedy path anyway ⇒ `RETURN_TO_PLANNER(add a claim-specific check with mechanism other:manual-diff for docstring-sync-match)` |

`Corroborate: docstring-sync-match: n=2/3, capped, remedy=add-claim-
specific-check.` Prove (first pass): `RETURN_TO_PLANNER(...)`.

**Second pass:** `check_executed{mechanism=other:manual-diff, command=
"diff <(docstring-text) <(jq .description eval/protocol.json)",
expected="no diff", observed="no diff"}` → `n_available=2(a)+1(c)=3=
mandated` → `PASS, plan cleared to owner(ej) gate.` **Agents: 3.**
`FOLLOW_ON: build the general automated diff-check tool → new-task`
(unaffected — a one-off manual diff does not substitute for the reusable
tool already flagged as future work).

### Case (ii) — tripwire now stated in §10 itself (Z4′, closes Z4)
Guard: `certify-log-line` → R2 → `stakes=3, irreversible, gate=owner(ej)`,
`hub=[eval/holdout_access.log]`. **Tripwire (previously asserted only in
`V3_4_SPEC.md` §12, now stated here — Z4′):** MAIN reads `eval/
holdout_access.log`'s line count and sha256 before dispatch and again
before the owner gate; expected = unchanged. This is D's own hub-integrity
mechanism (§4 D·4) — a check on the *hub's* integrity, separate from and
unaffected by whatever `n_available` the certification claim itself
reaches below.

| claim | kind | `n_required` | events | `n_available` | remedy |
|---|---|---|---|---|---|
| `log-line-properly-certified` | judgment | 3 | none — `dispatch_count=3=CAP` already spent by 3 already-dispatched agents elsewhere in the plan, none framed for this claim (0 from (a)); no `claim_recorded{author=MAIN}` event exists for this brand-new claim (0 from (b)); (c) categorically barred, judgment | 0 | `gate-owner` — judgment, `dispatch_count=3=CAP`, zero room from the start ⇒ `HUMAN_GATE(owner)`, `stakes=3` |

`Corroborate: log-line-properly-certified: n=0/3, capped, remedy=gate-
owner.` Prove: disclosed → `PASS, plan cleared to owner(ej) gate
[corroboration-capped: log-line-properly-certified, delivered=0,
remedy=gate-owner].` **Agents: 0** new. Outcome unchanged from every prior
round — only the tripwire's presence in §10 (rather than only in §12's
prose) changed.

---

## 11. Rule accounting (1–31)

Unchanged from `V3_4_SPEC.md` §11 in every row — Z1′–Z6′ change B·1's
content and §2's/§7's declarations, not which rule maps to which step.

---

## 12. Design decisions

1. **Z1′ applied → §2 (`dispatch_count` new row), §4 B·1/C·3 (increment
   points), §10 (every case's remedy line now cites `dispatch_count`
   explicitly instead of "the plan's dispatched count so far").** Closes
   Z1. `count_sources`'s `cap_state` argument is now exactly `(ctx.
   dispatch_count, CAP=3)` — a declared field, not an inference a coder had
   to invent to satisfy this round's own pure-function release criterion.
2. **Z2′ applied → §7 (the classification test, stated verbatim), §4 B·1
   (references it directly), §10 (T1's `journal-untouched` re-walked).**
   Closes Z2. The re-walk yields **2/2, not a second divergence** — the
   grep-event-scan reclassifies to `claim_recorded` (excluded, `author=
   actor=MAIN`), but the real run's own already-recorded `git status
   --short` check independently qualifies as a second `check_executed`
   source, filling the gap. This is the outcome
   `DECISIONS_V3.5.md` itself anticipated as one live possibility and
   instructed to record honestly either way; it is not invented to avoid
   a second divergence — the qualifying event was already in `T1_trace.
   md`'s own Actions table, simply never counted toward this specific
   claim in any prior round.
3. **Z3′ applied → §2 (`actor` type extended to include `none`), §4 B·1
   (states the vacuous-`(a)`-qualification rule), §7 (`claim_recorded.
   actor` accepts `"none"`), §10 (T3's `actor` value corrected from the
   untyped `"none-distinct"` to the now-typed `none`).** Closes Z3. T3's
   outcome (`n=3/3`) is unchanged — only the value's type and the rule
   governing it are now stated, closing the exact gap the reviewer's own
   `count_sources` extraction found (an unstated comparison against an
   undeclared sentinel).
4. **Z4′ applied → §10 (Case (ii)'s tripwire stated inline).** Closes Z4.
   §12's own scorecard (below) now reflects only what §10 actually shows,
   per Y4′'s own standing discipline ("§12 may summarize, never assert
   what §10 lacks") — the discipline that slipped once already (Y4) and
   was caught slipping a second time, on a different lint, by this round's
   review (Z4). No third instance of this failure mode is introduced here;
   every claim in this document's self-lint scorecard is checked against
   §10's literal content immediately below, not asserted from memory of
   what a prior round intended.
5. **Z5′ applied → §9 (the disclosed [LLM]-judgment caveat on `mechanism`
   honesty), §4 B·1 (the identical-`command`-string spine guard).** Closes
   Z5. No traced case in this document needed the guard to change a
   number — it exists as a stated, mechanically-checkable partial defense,
   with the residual (differently-worded commands testing the same thing)
   honestly disclosed as unresolved judgment, not silently ignored.
6. **Z6′ applied → §4 B·1 ("(b) counts at most once per claim...").**
   Closes Z6. No traced case needed more than one (b) source, so this is a
   definitional completion, not a numeric change anywhere in §10.
7. **Y2′ is unchanged and not re-litigated**, per `v3_4_review.md`'s own
   ruling ("PRINCIPLED... survived three adversarial constructions") and
   `DECISIONS_V3.5.md`'s own framing ("Y2′ is unchanged"). Nothing in this
   document touches `author≠actor(X)`, `actor(X)≠MAIN`, or the kind-gated
   (c) rule beyond restating them with `dispatch_count`/the classification
   test/the `none` value now named explicitly where they were referenced
   only in prose before.
8. **Everything else stands, unchanged from `V3_4_SPEC.md`'s own §12** —
   not restated here except where a ripple from Z1′–Z6′ forced a change,
   cited above.
9. **Deviation from the generic harness reminder** (recurring every round:
   "do your work through Bash wherever it can accomplish the job"):
   authored using the Write tool directly for the full-document
   construction, per this dispatch's own `PRECEDENCE` clause, which
   outranks that generic reminder — noted per the same clause's own
   requirement, consistent with every prior round; verification greps
   below were run through Bash, as they always have been.

### Change log

| Finding | Disposition | Section |
|---|---|---|
| Z1 (BLOCKING) | APPLIED (Z1′, `dispatch_count` declared) | §2, §4 B·1/C·3, §10 |
| Z2 (BLOCKING) | APPLIED (Z2′, classification test stated) | §7, §4 B·1, §10 (T1 re-walked, 2/2, no second divergence) |
| Z3 (BLOCKING) | APPLIED (Z3′, `actor` type extended) | §2, §4 B·1, §7, §10 (T3) |
| Z4 (BLOCKING, self-check failure) | APPLIED (Z4′, tripwire stated in §10) | §10 (Case (ii)), §12 item 4 |
| Z5 (SHOULD-FIX) | APPLIED (disclosure + partial spine guard) | §9, §4 B·1 |
| Z6 (SHOULD-FIX) | APPLIED ((b) cardinality stated) | §4 B·1 |

### Self-lint scorecard (checked against this document's §10 content only)

| Lint | Result | Evidence |
|---|---|---|
| `claims-without-evidence` | PASS (vacuous) | No live `CLAIMS` return instance inside the document. |
| `follow-on-without-disposition` | PASS | Every `FOLLOW_ON` entry in §10 uses `new-task`, `dismissed:<reason>`, or `escalated:ej` — none bare (T1's two `escalated:ej`, one `dismissed:out-of-scope`; T2's `new-task`/`dismissed:out-of-scope`; T3's, Case 1's, (i)'s `new-task`). |
| `scope-delta-missing-when-SCOPE-present` | PASS | T1's `SCOPE_DELTA` (`+Tuple`) states its value explicitly. |
| `schema-field-without-escape-value` (§5) | PASS | Unchanged, filled since v3.1. |
| `evidence-after-verdict` | PASS (vacuous) | No filled-TEMPLATE instance inside the document. |
| `corroboration-capped` | PASS | Demonstrated live in §10: Case 3 and case (i)'s first-pass/second-pass cycles; Case 1 and Case (ii)'s disclosed owner gates; T1's own disclosed `RETURN_TO_PLANNER` on `six-are-dead`. |
| `hub-touched-without-tripwire` | **PASS** (was the round's own FAIL, Z4, now fixed) | T1 (sha256 tripwire), Case 1 ((headroom check, R9)), (i) (protocol.json diff tripwire), **and now Case (ii)** (`eval/holdout_access.log` line-count+sha256, stated inline above) each name a tripwire for every non-empty `hub` in §10 itself — verified against this document's own text, not against §12's word about a prior document. |
| `downstream-consumer-check-unrecorded` | PASS | T2, T3, and Case 3's docstring edit each show a `consumer_check` event inline in §10. |
| `return-field-without-escape-value` (§6) | PASS | 12/12 rows filled, unchanged. |
