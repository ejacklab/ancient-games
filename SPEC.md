# The Ancient Games — V3.6 Spec of Record

Revises `V3_5_SPEC.md` per `DECISIONS_V3.6.md` (AA1′–AA3′ — binding; AA4/
AA5 applied per the reviewer's rewrites, adapted where a harder constraint
requires; AA6 deferred — binding) applied on top of `v3_5_review.md`
(REJECT: 3 BLOCKING AA1–AA3, 2 SHOULD-FIX AA4–AA5, 1 NOTE AA6). `V3_5_SPEC.
md` is untouched. **Y2′/Z1′–Z6′ are frozen and not re-litigated** — the
review's own ruling is that `count_sources` was written as a pure function
with no numerically-consequential invented branch, the first round for
which that held. Every finding this round is documentary: an exit-line
grammar disagreement, two missing ctx rows, and one missing sentence in a
single trace. **Per this round's own constraint, §4 B·1, §4 D, and §3's
registry text are byte-identical to `V3_5_SPEC.md`** — diffed, confirmed,
and stated in §12 — except for the one new sentence AA3′ adds to §7 (not
to B·1, D, or the registry themselves).

---

## 1. Overview

Call order unchanged. Three fixes, all documentary:

1. **§4's exit-line templates are canonical; §10 is rewritten to match
   them exactly.** Across the last two rounds, §10's own worked lines
   drifted from §4's stated templates in three ways the reviewer's own
   coder-return input named: a `Filter:` line that named individual
   findings inline in one case and only their dispositions in another (two
   different, mutually inconsistent embellishments of the same bare
   template); an `A`/`Prove` `RETURN_TO_PLANNER` case whose §4 template
   dropped its old free-text wrapper but whose worked lines were never
   reconciled with that change explicitly; and a `Gate` line that stopped
   being written out as a literal, byte-comparable string at all. Per the
   reviewer's own ruling — endorsed here — the templates in §4 are correct
   as stated (bare types, e.g. `Filter: kept=<k>, merged=<m>, cut=<c>,
   follow_on=<f>`, or a bare structured type like `SOURCES(...)`/
   `CAPPED(...)`); per-entry names, dispositions, and remedy text belong in
   the structured `Output` each algorithm already declares, never
   duplicated informally into the free-text summary line. Every exit line
   in §10 is rewritten to this canonical, bare form (AA1′, closes AA1);
   §12 lists each normalized line.
2. **`difficulty` and `capability` are now declared ctx rows.** C·2's own
   step text has said "state the task's difficulty and needed capability
   as falsifiable assumptions" since the very first draft of this
   document, and §4 C's own `Gate` exit template has named `difficulty` as
   one of its fields since v3 — but no version of §2's ctx table, across
   six rounds, ever declared the row `ctx.py`'s dataclass would need to
   hold it. §2 gains `difficulty ∈ {LOW, MED, HIGH}` and `capability:
   list[str]` (AA2′, closes AA2).
3. **T1's own D·4 hub-integrity tripwire is now stated in §10**, distinct
   from — but sharing one event with, via a new dual-role rule in §7 — the
   `journal-untouched` claim's own (c) corroboration source. `hub-touched-
   without-tripwire`'s previously-misreported PASS for T1 (§12 cited a
   corroboration-evidence event, not D·4's own hub-integrity check, which
   T1's §10 text never separately named) is now genuinely supported (AA3′,
   closes AA3).

AA4 (the `classify_event` call-site) and AA5 (the (c)-dedup ordering) are
applied per the reviewer's rewrites, both relocated to §7 rather than B·1
— B·1 is frozen this round, and §7 is the more natural home for a rule
about how evidence gets classified/deduped before B ever reads it (§12
items 5–6 explain the placement). AA6 (NOTE) is deferred with one line,
matching every prior round's NOTE-handling precedent.

---

## 2. The ctx object

Only the two new rows this round; every other row is unchanged from
`V3_5_SPEC.md` §2.

| property | type | set by | consumed by | notes |
|---|---|---|---|---|
| `difficulty` | `LOW \| MED \| HIGH` | C·2 | C·3 (agent-count decision tree), the Gate exit line | **new (AA2′, closes AA2)** — a falsifiable statement about task difficulty, not a bare self-assessment label (#9); C·2's own step text has required this since the first draft, with no ctx row to hold it until now. Escape value: `UNKNOWN` (recorded, never silently omitted, when C·2 cannot yet state a level). |
| `capability` | `list[str]` | C·2 | schema role selection (`DISPATCH`), D·4's tool-grant lookup | **new (AA2′, closes AA2)** — the specific tool/role capabilities the task needs (a measurable lookup — tool grants, context size — never a self-assessment, #9), named alongside `difficulty` in C·2's step text since the first draft. Escape value: `[]` (no special capability needed beyond the default grant). |

---

## 3. Registry

Unchanged from `V3_2_SPEC.md` §3. Not reproduced — no finding this round
touches the registry.

---

## 4. The five algorithms

Step counts unchanged: C=5, D=5, B=5, E=7, A=3 (25 steps total). **§4 B·1
and §4 D are byte-identical to `V3_5_SPEC.md`** — diffed, confirmed, stated
in §12 item 7. C, E, A are also unchanged (no finding this round touches
their step text — AA1′ only requires §10 to match the templates they
*already* state; the templates themselves do not change). All five are
reproduced in full below, since the fixed structure keeps them in one
place.

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
   framing-style multiplicity the way (a) does), **and not at all when
   `MAIN`'s event was already counted under (a) — one author contributes
   at most one source per claim across (a) and (b) (hybrid v1.1, D-B)**;
   **(c)**, only when
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

**Output:** `KEEP[]`, `MERGED[]`, `CUT[]`, `FOLLOW_ON[]` — **each entry carries its deciding rule and name/disposition as structured fields; the free-text exit line above never repeats them (AA1′)**.

### A — Prove(plan)
**Input:** `plan` — E's `KEEP[] + MERGED[]`, with each entry's D/B annotations attached.
1. `[spine]` (#2) Every claim shows the command that produced it; "confirmed" with no command fails.
2. `[LLM]` (#2) Every action has a check that can fail, not merely an expectation it will work.
3. `[LLM]` (#7) Every metric names the true quantity it proxies and how the two could diverge.

**Exit conditions:** all three checks plus every lint in §8 run over the whole plan; A never exits early.
- A claim in `ctx.corroboration_capped` whose `remedy ∈
  {add-claim-specific-check, add-differently-framed-source}` and has no
  recorded fix in the plan → lint `corroboration-capped` FAILs →
  `RETURN_TO_PLANNER(<remedy text>, naming the claim)` — **this bare
  structured type is the whole exit line; no additional `Prove: FAIL, N=...`
  wrapper string exists (AA1′ — the wrapper was dropped in v3.5's own
  restatement of this template and is not restored here; the reviewer's
  own ruling endorses the bare structured form for exactly this case)**.
  Resume semantics unchanged (V7): resumes at C·3 with the capping
  constraint relaxed by the remedy; `hub`/`stakes`/`tripwire`/`actor`/
  `dispatch_count` persist.
- A claim whose `remedy ∈ {gate-checkpoint, gate-owner}` is never itself an
  A-blocking condition — it must appear disclosed in that claim's
  `gate_reason` set and A's own exit line; omitting the disclosure is
  itself a FAIL.
- All clean → `PASS` — `Prove: PASS, plan cleared to <checkpoint|owner>
  gate[, governance-gated][, corroboration-capped].` **Bare form: the gate
  identity is named without its owner string (that detail lives in D's own
  structured `gate=owner(<name>)` output); `governance-gated`/
  `corroboration-capped`, when present, are bare flags, never inline
  claim-id/remedy detail (AA1′).**

**Output:** `PASS` | `RETURN_TO_PLANNER(findings[])`

---

## 5. Schema field table

Unchanged from `V3_5_SPEC.md` §5. Not reproduced.

---

## 6. Return contract

Unchanged from `V3_5_SPEC.md` §6. Not reproduced.

---

## 7. Trace journal

Event shapes unchanged from `V3_5_SPEC.md` §7 in their field lists. Three
additions this round, all documentary:

**The `claim_recorded`/`check_executed` classification test, unchanged
from v3.5, restated for context:**

> A piece of evidence is logged as a `check_executed` event **iff** it
> names an explicit expected value or falsifying condition that the
> observed result could have failed to match; a bare citation of a
> command's output, with no stated alternative it was checked against, is
> logged as a `claim_recorded` event, even when `MAIN` is the one who ran
> the command.

**Call-site, new (AA4′, applies the reviewer's rewrite verbatim, relocated
to §7 since B·1 is frozen this round):** `classify_event` is called once,
by the orchestrator, at the moment a piece of evidence is about to be
journaled — **never by `count_sources`** (§4 B·1), which only ever reads
already-classified events already sitting in the journal with their event
type already decided.

**Category-(c) dedup order, new (AA5′, applies the reviewer's rewrite
verbatim, relocated to §7 for the same reason):** when B·1 counts category
(c), the identical-`command`-string guard applies **first**, collapsing
exact-command duplicates regardless of their `mechanism` label; **then**
whatever remains is deduped by distinct `mechanism`. This fixes the
composition order between Z5′'s two rules, which B·1's own text states but
does not sequence.

**Dual-role rule, new (AA3′, closes AA3):** a `check_executed` event that
is D·4's own hub-integrity tripwire for hub `H` **also** qualifies as a
category-(c) `hash-compare` source for any `executable` claim it
falsifies — **one event, two roles, recorded once.** This is not a new
event type; it is a statement that the *same* journaled event can satisfy
both D's hub-integrity requirement (§4 D·4, `HUB_INTEGRITY`) and B's
corroboration-source requirement (§4 B·1, category (c)) simultaneously,
without being logged twice. §10's T1 case below is the worked example.

```
{"ts":str, "run_id":str, "event":"exit",           "algorithm":str, "steps_fired":[str], "exit_type":str, "exit_line":str, "ctx_keys_set":[str]}
{"ts":str, "run_id":str, "event":"dispatch",       "agent_id":str, "role":str, "framing":str, "payload_fields":[str], "output_path":str}
{"ts":str, "run_id":str, "event":"return",         "agent_id":str, "fields":{...return contract, §6...}}
{"ts":str, "run_id":str, "event":"rule_fire",      "rule_id":str, "algorithm_step":str, "field":str, "ctx_value":any}
{"ts":str, "run_id":str, "event":"check_executed", "claim_id":str, "falsifies":str, "mechanism":"interpreter-import"|"pytest-fail-first"|"suite-count"|"git-diff-scope"|"hash-compare"|"adversarial-case"|"other:<name>", "command":str, "expected":str|num, "observed":str|num, "pre_fix_result":"FAIL"|null, "hub_integrity_for":str|null}
{"ts":str, "run_id":str, "event":"claim_recorded", "claim_id":str, "author":"MAIN"|str, "actor":"MAIN"|str|"none", "kind":"executable"|"judgment", "text":str, "evidence_type":"command"|"file:line", "evidence_ref":str, "framing":str|null}
{"ts":str, "run_id":str, "event":"consumer_check", "ref":[str], "answer":"no"|str, "command_or_reasoning":str}
```

`check_executed` gains one optional field, `hub_integrity_for: str|null` —
the hub path this event *also* serves as D·4's tripwire for, when
applicable (the dual-role rule above); `null` for an event that is a pure
corroboration source with no hub-integrity role. `rule_fire` remains the
dormant promote/decay substrate for #19/#22, unchanged.

---

## 8. Lints

Nine lints, unchanged in count, name, input, and condition from
`V3_5_SPEC.md` §8 — no finding this round changes a lint's own definition;
only the **self-lint result** for `hub-touched-without-tripwire` changes
(re-run against §10, now genuinely PASSing for T1 — see §12's scorecard).
Not reproduced in full — see `V3_5_SPEC.md` §8.

---

## 9. Convert the walls, keep the holes

Unchanged from `V3_5_SPEC.md` §9. Not reproduced.

---

## 10. Trace test cases

All eight, self-contained (Y4′'s discipline, unchanged). **Per AA1′, every
exit line below is the bare, canonical form §4 declares — no inline
names, dispositions, owner strings, or remedy text inside a quoted exit
line; that detail is carried in the accompanying per-claim tables and
`FOLLOW_ON`/`SCOPE_DELTA` bullets, exactly as the algorithms' own
structured `Output` types declare it.** Only T1 (its `journal-untouched`
tripwire, AA3′) and §2's new `difficulty`/`capability` fields (AA2′) are
substantive content changes from `V3_5_SPEC.md`; every other case's
numbers, events, and outcomes are unchanged — only their exit-line
*formatting* is normalized.

### T2 — REAL, must match `T2_trace.md`
`difficulty=LOW`, `capability=["python-repl","pytest"]`.
Gate: `PLAN_NEEDED(count=0, difficulty=LOW, stop_criterion="import-
succeeds-plus-smoke-test", execution_status=main_executes)`. `actor=MAIN`.

Guard (research/tests edit): R8 → `consumer_check{ref: ["research/
stability.py", "tests/test_research_importable.py"], answer: "no",
command_or_reasoning: "grep -rl research.stability across eval/,loop/
finds no registered stakes≥2 consumer"}` → `NO_GATE(stakes=1,
reversibility=git-revertible)`.

Guard (commit): R6 → `GATED(hub=[R6], stakes=2, reversibility=git-
revertible, tripwire=git-diff-scope, backup=none, fallback=git-revert,
permissions=checkpoint-before-commit, gate=checkpoint)`.

| claim | kind | `n_required` | events | `n_available` |
|---|---|---|---|---|
| `import-succeeds` | executable | 2 | `check_executed{mechanism=interpreter-import, command="python3 -c \"import research.stability\"", expected="exits 0, no ImportError", observed="exit 0"}`; `check_executed{mechanism=pytest-fail-first, command="pytest tests/test_research_importable.py -q", expected="1 failed pre-fix, 14 passed post-fix", pre_fix_result=FAIL, observed="14 passed"}` | 2 |
| `no-regression` | executable | 2 | `check_executed{mechanism=suite-count, command="make test", expected=274, observed=274}`; `check_executed{mechanism=git-diff-scope, command="git diff --stat", expected="exactly research/stability.py + tests/test_research_importable.py, no other files", observed="2 files, matches"}` | 2 |

Corroborate, per claim: `import-succeeds`: `SOURCES(n_available=2,
framings=[], files=[], reconciliation=agree)`. `no-regression`:
`SOURCES(n_available=2, framings=[], files=[], reconciliation=agree)`.

Filter: `kept=3, merged=0, cut=1, follow_on=2.` `FOLLOW_ON`: (1) extend
importability pattern to `eval/`,`loop/` — `new-task`; (2) `_scratch_
pivot_dense_scan.py` runs heavy work at import — `dismissed:out-of-scope`.

Prove: `PASS, plan cleared to checkpoint gate.` **Agents: 0.**

### T1 — REAL, DIVERGES from `T1_trace.md` on `six-are-dead`; D·4 tripwire now stated explicitly (AA3′, closes AA3)
`difficulty=MED`, `capability=["ast-analysis","grep"]`.
Gate: `PLAN_NEEDED(count=1, difficulty=MED, stop_criterion="verify-and-
delete-dead-code", execution_status=dispatched)`. `actor=MAIN` for the
deletion itself (the historian is dispatched only to verify).

Guard: mutate `loop/program_db.py` → R7 (dir, `hub?=no`) ∪ R4
(`loop/program_db.jsonl`, registered consumer, `hub?=yes`) → `hub=[loop/
program_db.jsonl], stakes=2`; reversibility: (b) fires (possible journal
corruption) → `irreversible`. **D·4's own hub-integrity tripwire, stated
here explicitly (AA3′ — previously asserted only in §12's prose, never
shown in this section):** MAIN reads `loop/program_db.jsonl`'s sha256 and
line count immediately before dispatching the historian, again after the
historian returns, and again after the full suite run — expected
unchanged at every reading; `check_executed{claim_id=journal-untouched,
falsifies=journal-untouched, mechanism=hash-compare, command="sha256sum
loop/program_db.jsonl", expected="fdfa84bc… (pre-deletion hash)",
observed="fdfa84bc… unchanged ×3", hub_integrity_for="loop/program_db.
jsonl"}`. **Per §7's dual-role rule, this one event is both D·4's tripwire
for this hub and (see the table below) a (c) source for `journal-
untouched` — recorded once, read twice.** `GATED(hub=[loop/program_db.
jsonl], stakes=2, reversibility=irreversible, tripwire=hash-compare
(above), backup=none, fallback=re-audit-if-historian-silent, permissions=
checkpoint-before-commit, gate=checkpoint)`.

| claim | kind | `n_required` | events | `n_available` |
|---|---|---|---|---|
| `six-are-dead` | judgment | 2 | `claim_recorded{author=MAIN, actor=MAIN, framing="text-reference-scan", evidence_type=command, evidence_ref="ast scan + grep -rnw"}` — `author=actor=MAIN` ⇒ excluded from (a)/(b) ⇒ 0; `claim_recorded{author=historian, actor=MAIN, framing="schema-dispatch-read"}` — `author≠actor` ⇒ valid (a) ⇒ 1 | 1 |
| `journal-untouched` | executable | 2 | **the D·4 tripwire event above**, read here in its second role as a (c) `hash-compare` source (dual-role rule, §7) ⇒ 1; `check_executed{mechanism=git-diff-scope, command="git status --short", expected="only loop/program_db.py modified", observed="M loop/program_db.py only"}` ⇒ 1 more, distinct mechanism; `claim_recorded{author=MAIN, actor=MAIN, evidence_type=command, evidence_ref="grep -o event_type … \| uniq -c"}` — names no expected value ⇒ `claim_recorded`, `author=actor=MAIN` ⇒ excluded, 0, irrelevant either way | 2 |

Corroborate, per claim: `six-are-dead`: `CAPPED(claim_id=six-are-dead,
kind=judgment, capped_from=2, mandated=2, delivered=1,
remedy=add-differently-framed-source)`. `journal-untouched`:
`SOURCES(n_available=2, framings=[], files=[], reconciliation=agree)`.

**T1's divergence, unchanged in substance from v3.4/v3.5, restated for
completeness:** `six-are-dead` was actually corroborated by exactly one
independent party (the historian); `n_required=2` is not met.
`journal-untouched` stays 2/2 — the deletion's mechanical safety is fully
corroborated, now derived from a tripwire event this section actually
names, not merely implied by a corroboration table alone.

Filter still runs (E precedes A regardless of A's eventual verdict):
`kept=1, merged=0, cut=1, follow_on=3.` `FOLLOW_ON`: (1) `eval/forecast.
py:255 NetOutcomeResolver`, dead by both methods, in `eval/` (frozen-
oracle surface) — `escalated:ej`; (2) 11 stale `.claude/worktrees/agent-*`
trees hold an older `program_db.py` where these names still have callers —
`dismissed:out-of-scope`; (3) `loop/program_db.py`'s `DB_PATH`
per-worktree fork (from wave 1), still open — `escalated:ej`. `SCOPE_
DELTA`: added — remove orphaned `Tuple` from `from typing import`.

A's exit for the deletion action: `RETURN_TO_PLANNER(add source with
framing independent-static-scan for six-are-dead)` — not `PASS`,
contradicting `T1_trace.md`'s own recorded outcome. **Not patched.**
**Agents, as actually run: 1** (historian) — **as this document's rule
would have required: 2.**

### T3 — REVISED, `actor=none` (unchanged from v3.5)
`difficulty=HIGH`, `capability=["research-synthesis"]`.
Gate: `PLAN_NEEDED(count=3, difficulty=HIGH, stop_criterion=
"recommendation-ready-3-part", governance_gated=R1, execution_status=
dispatched)`. `ctx.actor=none` — commissioned to three co-equal,
independent research authors from the outset, none having performed the
work before the others were dispatched to check it (§2's Z3′ rule); every
`claim_recorded` author on the claim qualifies for (a) by definition.

Guard: produce-recommendation → R8 → `consumer_check{ref: ["<new
recommendation doc path>"], answer: "no", command_or_reasoning: "a
freshly-authored research doc has no existing consumer yet"}` →
`NO_GATE(stakes=1, reversibility=git-revertible)`.

| claim | kind | `n_required` | events | `n_available` |
|---|---|---|---|---|
| `unseal-recommendation` | judgment | `max(1,3)=3` | `claim_recorded{author=spec-reader, actor=none, framing="spec-reader"}`; `claim_recorded{author=historian, actor=none, framing="historian"}`; `claim_recorded{author=statistician, actor=none, framing="statistician"}` — `actor=none` ⇒ all three qualify for (a), three distinct framings | 3 |

Corroborate: `SOURCES(n_available=3, framings=[spec-reader, historian,
statistician], files=[<3 paths>], reconciliation="disagree,
dominance=irreversibility-finding")`.

Filter: `kept=1, merged=3, cut=1, follow_on=1.` `FOLLOW_ON`: build an
automated certifier — `new-task`.

Prove: `PASS, plan cleared to owner gate, governance-gated.` **Agents: 3.**

### Case 1 — unchanged
`difficulty=MED`, `capability=["network-rate-limit-analysis"]`.
Gate: `PLAN_NEEDED(count=1, difficulty=MED, stop_criterion="backoff-
verified-safe", execution_status=dispatched)`.

Guard: `GATED(hub=[R9], stakes=3, reversibility=irreversible,
tripwire=headroom-check, backup=none, fallback=n-minus-1-clause,
permissions=checkpoint-then-owner, gate=owner)`. `actor=<coder>`.

| claim | kind | `n_required` | events | `n_available` |
|---|---|---|---|---|
| `backoff-safe-at-100ms` | judgment | 3 | `claim_recorded{author=<coder>, actor=<coder>, framing="proposer"}` — `author=actor` ⇒ 0; `claim_recorded{author=corroborator-1, actor=<coder>, framing="headroom-analysis"}` ⇒ 1; `claim_recorded{author=corroborator-2, actor=<coder>, framing="failure-mode-review"}` ⇒ 1 more | 2 |

Corroborate: `CAPPED(claim_id=backoff-safe-at-100ms, kind=judgment,
capped_from=3, mandated=3, delivered=2, remedy=gate-owner)` —
`dispatch_count=3=CAP`, no slot remains, straight to a disclosed owner
gate, no bounce.

Filter: `kept=1, merged=0, cut=1, follow_on=1.` `FOLLOW_ON`: document
IP+key rate-limit — `new-task`.

Prove: `PASS, plan cleared to owner gate, corroboration-capped.`
**Agents: 3.**

### Case 2 — unchanged
`difficulty=HIGH`, `capability=["read-only-eval-partitions"]`.
Guard: probe `eval.partitions.load_holdout` → R3 → `GATED(hub=[eval.
partitions.load_holdout, eval/holdout_access.log], stakes=3,
reversibility=irreversible, tripwire=none-until-gated, backup=none,
fallback=none, permissions=none-until-gated, gate=owner)`, no approval on
record. Gate resumes: `PLAN_NEEDED(count=0, difficulty=HIGH,
stop_criterion="owner-clearance-or-declared-blocked",
execution_status=hard_blocked)`. B/E/A never run. **Agents: 0.**

### Case 3 — unchanged
`difficulty=MED`, `capability=["python-authoring"]`.
Gate: `PLAN_NEEDED(count=2, difficulty=MED, stop_criterion="liquidity-
module-plus-docstrings-done", execution_status=dispatched)`.

Guard (module edit): R7 → `GATED(hub=[], stakes=2, reversibility=git-
revertible, tripwire=none, backup=none, fallback=git-revert,
permissions=checkpoint-before-commit, gate=checkpoint)`. `actor=<module-
coder>`.
Guard (docstring edit): R8 → `NO_GATE(stakes=1, reversibility=git-
revertible)`.
`consumer_check{ref: ["research/*.py docstrings"], answer: "no",
command_or_reasoning: "docstring text isn't consumed/synced anywhere, unlike
case (i)'s report.py"}`.
Guard (commit): R6 → `GATED(hub=[R6], stakes=2, reversibility=git-
revertible, tripwire=git-diff-scope, backup=none, fallback=git-revert,
permissions=checkpoint-before-commit, gate=checkpoint)`.

**First pass:**
| claim | kind | `n_required` | events | `n_available` |
|---|---|---|---|---|
| `liquidity-module-correctness` | executable | 2 | `check_executed{mechanism=interpreter-import, command="python3 -c \"import engine.liquidity\"", expected="exits 0, no ImportError", observed="exit 0"}` | 1 |

Corroborate: `CAPPED(claim_id=liquidity-module-correctness,
kind=executable, capped_from=2, mandated=2, delivered=1,
remedy=add-claim-specific-check)`.

A (first pass): `RETURN_TO_PLANNER(add a claim-specific check with
mechanism pytest-fail-first for liquidity-module-correctness)`.

**Second pass** (V7 resume): `check_executed{mechanism=pytest-fail-first,
expected="fails pre-fix, passes post-fix on spec §5.3 formulas",
pre_fix_result=FAIL, observed="passed"}` ⇒ `n_available=2`.
Corroborate: `SOURCES(n_available=2, framings=[], files=[],
reconciliation=agree)`.

Filter: `kept=2, merged=0, cut=0, follow_on=0.`

Prove (second pass): `PASS, plan cleared to checkpoint gate.`
**Agents: 2.**

### (i) — unchanged
`difficulty=MED`, `capability=["docstring-editing","json-read"]`.
Gate: `PLAN_NEEDED(count=2, difficulty=MED, stop_criterion="docstring-
and-synced-protocol-text-match", execution_status=dispatched)`.

Guard: `research/report.py` edit → R8 (`hub?=no`) ∪ R1 (registered
consumer via the sync script, `hub?=yes`) → `GATED(hub=[eval/protocol.
json], stakes=3, reversibility=irreversible, tripwire=protocol-json-diff,
backup=none, fallback=n-minus-1-clause, permissions=checkpoint-then-owner,
gate=owner)`. `actor` = the fix+verify agent.

**First pass:**
| claim | kind | `n_required` | events | `n_available` |
|---|---|---|---|---|
| `docstring-sync-match` | executable | 3 | `claim_recorded{author=fix-verify-agent, actor=fix-verify-agent, framing="fix-and-confirm"}` — `author=actor` ⇒ excluded, 0; `claim_recorded{author=independent-reader, actor=fix-verify-agent, framing="sync-script-logic-read"}` ⇒ 1; `claim_recorded{author=third-corroborator, actor=fix-verify-agent, framing="protocol-json-diff-read"}` ⇒ 1 more | 2 |

Corroborate: `CAPPED(claim_id=docstring-sync-match, kind=executable,
capped_from=3, mandated=3, delivered=2,
remedy=add-claim-specific-check)`.

A (first pass): `RETURN_TO_PLANNER(add a claim-specific check with
mechanism other:manual-diff for docstring-sync-match)`.

**Second pass:** `check_executed{mechanism=other:manual-diff,
command="diff <(docstring-text) <(jq .description eval/protocol.json)",
expected="no diff", observed="no diff"}` ⇒ `n_available=3`. Corroborate:
`SOURCES(n_available=3, framings=[sync-script-logic-read, protocol-json-
diff-read], files=[<2 paths>], reconciliation=agree)`.

Filter: `kept=1, merged=0, cut=0, follow_on=1.` `FOLLOW_ON`: build the
general automated diff-check tool — `new-task`.

Prove (second pass): `PASS, plan cleared to owner gate.` **Agents: 3.**

### Case (ii) — unchanged
`difficulty=HIGH`, `capability=["log-certification"]`.
Guard: `certify-log-line` → R2 → `GATED(hub=[eval/holdout_access.log],
stakes=3, reversibility=irreversible, tripwire=hash-compare+line-count,
backup=none, fallback=none, permissions=checkpoint-then-owner,
gate=owner)`. Tripwire (Z4′, unchanged): MAIN reads `eval/holdout_access.
log`'s line count and sha256 before dispatch and again before the owner
gate; expected unchanged.

| claim | kind | `n_required` | events | `n_available` |
|---|---|---|---|---|
| `log-line-properly-certified` | judgment | 3 | none — `dispatch_count=3=CAP` already spent elsewhere, none framed for this claim; no `claim_recorded{author=MAIN}` event exists; (c) categorically barred, judgment | 0 |

Corroborate: `CAPPED(claim_id=log-line-properly-certified, kind=judgment,
capped_from=3, mandated=3, delivered=0, remedy=gate-owner)`.

Filter: `kept=1, merged=0, cut=0, follow_on=0.`

Prove: `PASS, plan cleared to owner gate, corroboration-capped.`
**Agents: 0** new.

---

## 11. Rule accounting (1–31)

Unchanged from `V3_5_SPEC.md` §11 in every row.

---

## 12. Design decisions

1. **AA1′ applied → §10 (every exit line in all eight cases rewritten to
   the bare, canonical form §4 already declares).** Closes AA1. **Every
   normalized line, listed once per distinct template (case-specific
   values omitted where the shape repeats):**
   - Gate: `PLAN_NEEDED(count=<n>, difficulty=<LOW|MED|HIGH>,
     stop_criterion="<text>"[, governance_gated=<row>],
     execution_status=<main_executes|dispatched|hard_blocked>)` — used in
     T2, T1, T3, Case 1, Case 2 (×2, resumed), Case 3, (i).
   - Guard: `NO_GATE(stakes=1, reversibility=<class>)` — T2 (edit), T3,
     Case 3 (docstring). `GATED(hub=<list>, stakes=<n>,
     reversibility=<class>, tripwire=<name>, backup=<none|name>,
     fallback=<name>, permissions=<grant>, gate=<none|checkpoint|owner>)`
     — T2 (commit), T1, Case 1, Case 2, Case 3 (module, commit), (i),
     Case (ii).
   - Corroborate, per claim: `SINGLE_SOURCE` (unused this round — no
     traced claim has `n_required=1`); `SOURCES(n_available=<n>,
     framings=<list>, files=<list>, reconciliation=<value>)` — T2 (×2),
     T3, Case 3 (2nd pass), (i) (2nd pass); `CAPPED(claim_id=<id>,
     kind=<executable|judgment>, capped_from=<n>, mandated=<n>,
     delivered=<n>, remedy=<value>)` — T1 (`six-are-dead`), Case 1,
     Case 3 (1st pass), (i) (1st pass), Case (ii).
   - Filter: `kept=<k>, merged=<m>, cut=<c>, follow_on=<f>[,
     governance-gated=<n>(terminal)]` — every case that reaches E; bare,
     no inline names/dispositions.
   - Prove: `RETURN_TO_PLANNER(<remedy text>, naming the claim)` — T1,
     Case 3 (1st pass), (i) (1st pass); bare structured type, no
     `Prove:`-prefixed wrapper string. `PASS, plan cleared to
     <checkpoint|owner> gate[, governance-gated][,
     corroboration-capped]` — every case reaching `PASS`; bare, no owner
     name or capped-claim detail inline.
   All three of the coder's named disagreements are resolved by this one
   rule: the `Filter:` line never again carries inline names (T1's old
   `(NetOutcomeResolver)`/`(+Tuple SCOPE_DELTA)`) or disposition
   parentheticals (T2's old `(new-task; dismissed:out-of-scope)`); `Prove`'s
   `RETURN_TO_PLANNER` case keeps the bare structured form v3.5 already
   moved to, now declared canonical rather than silently inconsistent with
   an un-updated wrapper; `Gate`'s line is now always written out as a
   literal, byte-comparable string per case, with no ad hoc extra fields
   (the old `role=` addition is gone — role lives in the dispatch record,
   not the Gate line).
2. **AA2′ applied → §2 (`difficulty`, `capability` new rows), §10 (every
   case states both explicitly).** Closes AA2. These two fields have been
   named in C·2's step text and referenced in §4 C's own Gate template
   since the first draft this review lineage examined; no version of §2
   ever declared them until now.
3. **AA3′ applied → §7 (dual-role rule, `check_executed.hub_integrity_for`
   field), §10 (T1's D·4 tripwire stated explicitly, distinct from but
   sharing one event with the `journal-untouched` corroboration source).**
   Closes AA3. `hub-touched-without-tripwire`, re-run against this
   document's own §10 content, now genuinely passes for T1 — the cited
   evidence is the tripwire event itself, named in T1's Guard section, not
   a corroboration-table entry recalled from a different claim's context.
4. **AA4 applied (reviewer's rewrite, verbatim, relocated to §7 — see item
   6).** Closes AA4.
5. **AA5 applied (reviewer's rewrite, verbatim, relocated to §7 — see item
   6).** Closes AA5.
6. **Placement note for AA4/AA5:** the reviewer's own rewrite text for
   both findings reads naturally as an addition to §4 B·1 ("state
   explicitly in §7" for AA4; no section named for AA5, but its subject —
   the order of two rules B·1 itself states — would ordinarily sit
   alongside them). This round's own constraint freezes B·1 byte-for-byte.
   Both rewrites are applied in full, in §7 instead — a rule about *when*
   `classify_event` runs relative to `count_sources`, and a rule about
   *in what order* B·1's own two dedup clauses compose, are both
   legitimately journal/event-layer statements (they describe the shape
   and processing of the events B·1 reads), not new B·1 rule text
   themselves. This is a placement adaptation forced by the freeze
   constraint, not a softening of either finding's substance — both
   rewrites are reproduced verbatim, just filed one section over. Noted
   explicitly per this dispatch's own instruction not to silently
   reinterpret a decision.
7. **Diff confirmation, as this round's own constraint requires:** `diff`
   was run between `V3_5_SPEC.md`'s and this document's §4 B·1 block, §4 D
   block, and §3 registry text (extracted identically from both files by
   section boundary). **Result: zero-byte diff on all three** — `§4 B·1`
   identical, `§4 D` identical, `§3` registry identical. The only content
   this round adds anywhere near these three is the AA3′ sentence and the
   `hub_integrity_for` field, both of which live in §7, confirmed by the
   same diff to be absent from B·1/D/the registry themselves.
8. **AA6 deferred, one line, matching every prior round's NOTE-handling
   precedent (W5, Y3):** no rewrite was proposed for AA6 in
   `v3_5_review.md` — it states the classification test (Z2′) remains
   interpretive for genuinely new, not-yet-seen evidence, and explicitly
   rules this "not escalated." Deferred, not fixed, consistent with that
   disposition.
9. **Y2′/Z1′–Z6′ are unchanged and not re-litigated**, per
   `v3_5_review.md`'s own ruling and `DECISIONS_V3.6.md`'s own framing
   ("the corroboration mechanism is frozen"). Nothing in this document
   touches self-exclusion, the kind gate, `dispatch_count`'s arithmetic,
   the classification test's substance, `actor`'s typed values, or the
   hub-union formula beyond restating them where a template/registry
   citation already pointed to them.
10. **Everything else stands, unchanged from `V3_5_SPEC.md`'s own §12** —
    not restated here except where a ripple from AA1′–AA3′ forced a
    change, cited above.
11. **Deviation from the generic harness reminder** (recurring every
    round: "do your work through Bash wherever it can accomplish the
    job"): this round's own diffing/verification (item 7 above, and the
    self-lint grep-checks below) was run through Bash, as the harness
    reminder asks; the full-document construction itself used the Write
    tool, per this dispatch's own `PRECEDENCE` clause, which outranks that
    generic reminder — noted per the same clause's own requirement,
    consistent with every prior round in this lineage.

### Change log

| Finding | Disposition | Section |
|---|---|---|
| AA1 (BLOCKING) | APPLIED (§4 templates canonical, §10 fully renormalized) | §10, §12 item 1 |
| AA2 (BLOCKING) | APPLIED (`difficulty`/`capability` declared) | §2, §10 |
| AA3 (BLOCKING, self-check failure) | APPLIED (T1's D·4 tripwire stated; dual-role rule) | §7, §10 (T1) |
| AA4 (SHOULD-FIX) | APPLIED (reviewer's rewrite, verbatim, relocated to §7 — B·1 frozen) | §7, §12 item 6 |
| AA5 (SHOULD-FIX) | APPLIED (reviewer's rewrite, verbatim, relocated to §7 — B·1 frozen) | §7, §12 item 6 |
| AA6 (NOTE) | DEFERRED (no rewrite proposed; not escalated by the reviewer) | §12 item 8 |

### Self-lint scorecard (checked against this document's §10 content only)

| Lint | Result | Evidence |
|---|---|---|
| `claims-without-evidence` | PASS (vacuous) | No live `CLAIMS` return instance inside the document. |
| `follow-on-without-disposition` | PASS | Every `FOLLOW_ON` entry in §10 uses `new-task`, `dismissed:<reason>`, or `escalated:ej` — none bare. |
| `scope-delta-missing-when-SCOPE-present` | PASS | T1's `SCOPE_DELTA` (`+Tuple`) states its value explicitly. |
| `schema-field-without-escape-value` (§5) | PASS | Unchanged since v3.1, every CORE/CONDITIONAL row filled. |
| `evidence-after-verdict` | PASS (vacuous) | No filled-TEMPLATE instance inside the document. |
| `corroboration-capped` | PASS | Demonstrated live in §10: Case 3 and (i)'s first-pass/second-pass `CAPPED`→`SOURCES` cycles; Case 1 and Case (ii)'s disclosed owner gates; T1's own correctly-firing `RETURN_TO_PLANNER` on `six-are-dead` with no remedy recorded. |
| `hub-touched-without-tripwire` | **PASS** (this round's own diagnosed FAIL, now fixed and re-verified) | T1's Guard section now states its D·4 tripwire explicitly (sha256+line-count of `loop/program_db.jsonl`, distinct from the corroboration-table entry that reuses it via the dual-role rule); Case 1 (headroom check), (i) (protocol.json diff), Case (ii) (log line-count+sha256) each still name one. Every non-empty `hub` in §10 has a tripwire stated in *this* section, not recalled from elsewhere. |
| `downstream-consumer-check-unrecorded` | PASS | T2, T3, and Case 3's docstring edit each show a `consumer_check` event inline in §10. |
| `return-field-without-escape-value` (§6) | PASS | 12/12 rows filled, unchanged. |
