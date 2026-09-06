# The Ancient Games — V3.3 Spec of Record

Revises `V3_2_SPEC.md` per `DECISIONS_V3.3.md` (X1′ amends D9′ item 4, X2′
closes X2, X5′ closes X5, X3/X4 apply the reviewer's rewrites, X6 fixed as
trivial — binding) applied on top of `v3_2_review.md` (REJECT: 3 BLOCKING
X1/X2/X5, 2 SHOULD-FIX X3/X4, 1 NOTE X6; **W1/W2/D9′/D2′ confirmed closed and
principled — not reopened**). `V3_2_SPEC.md` is untouched. "These are the
last three patches" (`DECISIONS_V3.3.md` line 3) — only §4 B/A, §6, §7, §8,
and the three affected §10 cases (Case 1, Case 3, Case (ii)) change; every
other section is unchanged from `V3_2_SPEC.md` and reproduced here only where
a ripple applies.

---

## 1. Overview

Call order unchanged. Three changes from v3.2, all narrower than any prior
round's:

1. **Capped-claim remedy is keyed on claim `kind`, never on `stakes` tier.**
   v3.2's D9′ item 4 routed every capped stakes-2 claim to `RETURN_TO_
   PLANNER` and every capped stakes-3 claim straight to a disclosed
   `HUMAN_GATE`, regardless of *why* it was capped. This silently denied a
   cheap, always-available fix (adding a claim-specific check) to a
   stakes-3 `executable` claim, while correctly offering that exact fix to
   an equivalent stakes-2 one — this was X1. X1′ replaces the routing key:
   `executable` claims are *always* re-plannable (`RETURN_TO_PLANNER(add a
   claim-specific check)`, regardless of stakes); `judgment` claims are
   re-plannable only while an agent slot remains under `CAP=3` (`RETURN_TO_
   PLANNER(add a differently-framed source)`), and only route to a human
   once that budget is genuinely exhausted (`HUMAN_GATE(checkpoint)` at
   `stakes≤2`, `HUMAN_GATE(owner)` at `stakes=3`). **Stakes still decides
   *which* human; kind now decides *whether* a human is the remedy at all.**
2. **Category (b) gets the same journal-backed availability test as
   category (c).** v3.2's item 3 allowed a judgment claim to be corroborated
   by "(a) or (b)" sources but never said when a (b) source exists — a coder
   (and the reviewer, independently, on Case 1) could reach a materially
   different `n_available` by guessing "yes." X2′ closes this: a (b) source
   exists for claim X **iff** the trace journal holds a `claim_recorded`
   event, authored by MAIN, naming X, with `evidence_type∈{command,
   file:line}` and a non-empty `evidence_ref` — and, for a `judgment` claim
   only, a `framing` distinct from every (a) source already counted on X.
   "No event, no source" — the same discipline item 5 already applied to
   (c), now applied to (b) too, and (a) is folded into the same journal
   query (agents' `CLAIMS` rows are ingested as `claim_recorded` events by
   the orchestrator, so one mechanism decides both categories).
3. **§6's return contract now carries its own filled `escape_value`
   column**, closing X5 — the spec previously added a lint
   (`return-field-without-escape-value`) to check exactly this property and
   then never applied it to its own table, failing the lint on 7 of 12 rows.

X3 (claim-kind threshold test) and X4 (the downstream-consumer-check lint's
missing tracking mechanism) are applied per the reviewer's own rewrites,
below. X6 (journal event field types stated only in prose) is fixed inline
as trivial, not deferred.

---

## 2. The ctx object

Only rows touched this round; every other row is unchanged from
`V3_2_SPEC.md` §2.

| property | type | set by | consumed by | notes |
|---|---|---|---|---|
| `claim_kind` | map: `claim_id → executable \| judgment` | B·1 | B·1 (source-category eligibility, remedy routing), lint `corroboration-capped` | **refined test (X3)**: a claim is `executable` **only if** the deciding command's own pass/fail or exact-match output, with no further human interpretation of a threshold, *is* the claim's truth value (an import succeeds or doesn't; a hash matches or doesn't; a suite's count matches an expected total or doesn't). A claim requiring a judgment about whether a produced *number* crosses an implicit or unstated bar (e.g. "the fix does not meaningfully degrade performance") remains `judgment` even though a command exists that measures the relevant quantity — replaces D9′ item 1's looser "a command can decide it" test, which admitted exactly this smuggled-threshold case. |
| `corroboration_capped` | list of `{claim_id, kind, capped_from, mandated, delivered, remedy}` | B·1 | lint `corroboration-capped`, `HUMAN_GATE` reason, A's exit conditions | **gains `remedy` (X1′, closes X1)**: `remedy ∈ {add-claim-specific-check, add-differently-framed-source, gate-checkpoint, gate-owner}`, computed per X1′'s kind-keyed rule (§4 B·1) — the field A's exit conditions read to decide `RETURN_TO_PLANNER` vs. a disclosed `HUMAN_GATE`, replacing v3.2's stakes-keyed routing. |

**No other ctx row changes.** `n_sources` stays the per-claim map from
v3.2; `hub` stays D2′'s union; `governance_gated`, `execution_status`,
everything else — unchanged.

---

## 3. Registry

Unchanged from `V3_2_SPEC.md` §3 in every column, row, and rule (the `id |
pattern | kind | verb | stakes | hub? | gate | owner | note` columns, the
hub-union formula, R1–R9, the mandatory downstream-consumer check). Not
reproduced here to avoid drift between two copies of the same, unaffected
table; see `V3_2_SPEC.md` §3 for the full text. **X4 below adds the
tracking mechanism the mandatory downstream-consumer check was always
missing — a new §7 journal event, not a registry change.**

---

## 4. The five algorithms

Step counts unchanged: C=5, D=5, B=5, E=7, A=3 (25 steps total). Only B
(step 1's source-categories and remedy) and A (the exit-conditions clause
that reads the remedy) change text. C, D, E are unchanged from
`V3_2_SPEC.md` §4 and reproduced here in full, since the fixed structure
keeps all five algorithms in one place per the brief.

### C — Gate(task)
**Input:** `task`
1. `[spine+LLM]` (#5, #31, R3, S2) For the cheap-means probe's target, read `artifact_refs.mode`. If `mode=read`: never gate it — proceed straight to cheap means (grep, cache, existing finding, human answer, a probe run to completion), recording each command's actual output into `ctx.known_facts`. If `mode∈{invoke,mutate}` and the target matches a registry hub (§3): treat the probe itself as an action and run it through Guard(D) first; execute only if D returns `stakes=1` (no gate). If answered, go to exit 1.
2. `[spine+LLM]` (#9, D3, closes V3) State the task's difficulty and needed capability as falsifiable assumptions; separately, set `governance_gated = <registry row id>` **only if** the task's own `stop_criterion` is itself a recommendation or decision on a registry row whose `gate=owner` — referencing, reading, or citing such a row does not set it.
3. `[spine]` (F1) Feed difficulty + capability into the F1 decision tree → agent count; set `execution_status = dispatched` if `count≥1`, else `execution_status = main_executes`.
4. `[spine]` (F1, R1) If count > 3: partition step 2's success criteria into the fewest groups whose re-run of step 3 each yields ≤3; run steps 1–5 per group independently; output `PLAN_NEEDED[]`, one entry per group; no group may exceed 3.
5. `[LLM]` (#12) Declare the stop criterion and a time-box for drafting, before drafting starts.

**Exit conditions:**
- Step 1 answers the task → `RESOLVED(evidence)` — `Gate: resolved by <means>, no dispatch.`
- Step 4 splits → `PLAN_NEEDED[]` — `Gate: split into <k> groups, each re-planned, N≤3 each.`
- Else, after step 5 → `PLAN_NEEDED(count, difficulty, stop_criterion[, governance_gated], execution_status)` — `Gate: plan needed, N=<count>, execution_status=<value>, stop=<criterion>[, governance-gated].` `execution_status` may be overridden by D (see D·5).

**Output:** `RESOLVED(evidence)` | `PLAN_NEEDED(count, difficulty, stop_criterion, execution_status)` | `PLAN_NEEDED[]`

### D — Guard(action)
**Input:** `action`. Step order: `refs → registry → reversibility → fallback/tripwire → gate`.
1. `[spine]` (#21, S2) **refs.** Set `artifact_refs.mode ∈ {read, invoke, mutate}` for everything this action touches. Reads are never gated and never registry-matched.
2. `[spine]` (#21, R7, S1, D2′, D6, closes W2) **registry.** Look up every `invoke`/`mutate` ref against §3 — runs on every action, no exit before it; apply same-ref specificity suppression among rows matched by the identical ref; separately find every registered downstream consumer (stakes≥2) of any mutated artifact and **record the answer via a `consumer_check` journal event whether or not one exists (X4 — see §7)**; `hub = (same-ref survivors with hub?=yes) ∪ (consumer matches with hub?=yes)`; `stakes = max` over all matched rows in both sets, `hub?` notwithstanding; default 1 if nothing matches at all.
3. `[spine+LLM]` (#18, R5, S1 extension) **reversibility.** Irreversible if any of: (a) reverting the artifact isn't a plain version-control operation — landing a commit to the default branch is always a plain VCS op and never fires this clause on that basis alone; (b) the action can trigger an external, non-code side effect surviving a code revert. Else `restorable` if a backup/snapshot exists and would undo it without a plain VCS operation; else `git-revertible`. Decides only the shape of the fallback/tripwire, never whether the action gates.
4. `[spine+LLM]` (#17, #28, #18, #29, #21) **fallback/tripwire.** Write the N−1 clause (retry is first-class); re-read each hub element's current state now and name one tripwire per element, shaped by step 3; record backup/redundancy or that none exists; set permissions as explicit tool grants scaled to terrain.
5. `[spine]` (F1, D1) **gate.** `stakes≥2` ⇒ checkpoint before the action that lands the change; `stakes=3` ⇒ owner gate, named per the hub's own governance (§3's `owner` column). If this action is the only candidate for a `count=0` plan and its gate is `owner` with no approval on record, set `ctx.execution_status = hard_blocked`.

**Exit conditions and Output:** unchanged (`NO_GATE(stakes=1, reversibility)` | `GATED(hub, stakes, reversibility, tripwire, backup, fallback, permissions, gate)`).

### B — Corroborate(claims, stakes)
**Input:** the action's load-bearing claims (from `CLAIMS`, or MAIN's own
cited claims at `execution_status=main_executes`), each tagged
`kind ∈ {executable, judgment}` per §2's refined test (X3). `n_required`
per claim = `max(the action's own stakes from D·2, the registry stakes tier
of governance_gated's row if set)` (D3/D9′ item 4, unchanged arithmetic).
B runs once per distinct claim.
1. `[spine]` (#4, #27, R4, S3, D9′ items 1–2/4–5, X1′, X2′, closes X1/X2) For each claim, if `n_required=1`: exit trivially, `SINGLE_SOURCE`. Else query the trace journal for every `claim_recorded{claim_id=<this claim>}` event (§7 — agents' `CLAIMS` rows are ingested into this same shape by the orchestrator, so (a) and (b) are decided by one query): **(a)** count one source per distinct non-`MAIN` author whose event's `framing` differs from every other (a) source already counted on this claim; **(b)** count MAIN's own `claim_recorded` event on this claim, but only if it carries `evidence_type∈{command,file:line}` and a non-empty `evidence_ref`, and — only when `kind=judgment` — a `framing` distinct from every (a) source already counted (X2′: no event meeting this test, no (b) source, exactly as item 5 already required of (c)); **(c)**, only when `kind=executable`, an executed check per D9′ item 5 (`check_executed{claim_id=<claim>}` with a recorded pre-fix FAIL or a constructed adversarial case). `CAP=3` bounds category-(a) dispatched-agent fan-out cumulatively across the whole plan; if reuse+shortfall in (a) would exceed `CAP=3`, cap at `max(0, 3 − the plan's dispatched count so far)`. If `n_available<n_required` after this, determine `remedy` **by `kind`, not `stakes`** (X1′, replaces D9′ item 4's routing): `kind=executable` ⇒ `remedy=add-claim-specific-check` (a (c) source can always be constructed for an executable claim; this is never a gate, regardless of stakes tier); `kind=judgment` ⇒ if the plan's total category-(a) dispatch count is still below `CAP=3` ⇒ `remedy=add-differently-framed-source`; else (CAP fully spent, no slot remains) ⇒ `remedy=gate-checkpoint` at `stakes≤2` or `remedy=gate-owner` at `stakes=3` (stakes decides *which* human; kind decides *whether* a human is the remedy at all). Record `{claim_id, kind, capped_from, mandated, delivered, remedy}` in `ctx.corroboration_capped` — never proceed as if uncapped.
2. `[LLM]` (#10, #27) Assign each category-(a) source on a claim a distinct framing — never issue the same prompt twice, byte-for-byte or in substance, to two parallel agents on the same claim.
3. `[spine]` (#8) Dispatch category-(a) sources in parallel, each to its own file; no reading a sibling's file first.
4. `[spine]` (#2, R8) Drop any claim lacking a cited command (UNVERIFIED); if every claim backing an action is dropped, remove that action from the candidate set E receives.
5. `[LLM]` (#23) Reconcile survivors per claim: note agreement (flag as suspect if framings were alike); let disagreement stand; break residual ties by dominance: irreversibility-finding > eligibility-finding > design-proposal.

**Exit conditions (per claim, rolled up per action for the exit line):**
- `n_required=1` → `SINGLE_SOURCE` — `Corroborate: <claim>: n=1 (single source).`
- Else, after step 5 → `SOURCES(n_available, framings, files, reconciliation)` or `CAPPED(claim_id, kind, capped_from, mandated, delivered, remedy)` — action-level exit line rolls every claim up: `Corroborate: <claim1>: n=<n1>/<req1>[, capped, remedy=<remedy>]; ...; reconciled=<agree|disagree[,dominance=<rule>]>.`

**Output:** per claim, `SINGLE_SOURCE | SOURCES(n,framings,files,reconciliation) | CAPPED(claim_id,kind,capped_from,mandated,delivered,remedy)`.

### E — Filter(candidates)
**Input:** `candidates` — actions/findings surviving D and B, each pre-scored on {cost, expected value, risk, confidence}: cost/permissions from D, confidence from B.
1. `[spine]` (#23, R11) Pareto-filter: drop any candidate dominated on every axis by another survivor.
2. `[LLM]` (#11) Fund the decisive branch: concentrate budget on what decides the outcome; cut the rest.
3. `[LLM]` (#16, R6) FOLLOW_ON if acting on a discovery needs a new action not yet through D/B; fold a discovery that is evidence for an already-guarded candidate's success criterion into that candidate's KEEP/MERGED, tagged discovered-not-planned.
4. `[LLM]` (#1) Per surviving dispatch, restate intent, non-delegable constraints, success criterion.
5. `[spine]` (#13, #15, #30) Each dispatch loads the same versioned path/format/tie-break doctrine, names its handoff topology and accepted tradeoff, asserts `PRECEDENCE`, and returns one artifact at one fixed, pre-declared path. If any surviving KEEP/MERGED entry carries `governance_gated≠none`, mark the pipeline's trailing gate (after A) owner-gated on that entry specifically, per the registry's named `owner` column for that row.
6. `[spine]` (#25) Bound each surviving dispatch's payload and expected return against a declared size limit; trim before dispatch, recording the trim.
7. `[spine]` (#26, R4-schema) Name every field in the payload for what the task calls it in plain domain terms; rename any generic schema label before dispatch.

**Exit conditions:**
- `candidates` empty → `KEEP=[],MERGED=[],CUT=[],FOLLOW_ON=[]` — `Filter: no candidates, nothing to filter.`
- Else, after step 7 → tagged `KEEP[],MERGED[],CUT[],FOLLOW_ON[]` — `Filter: kept=<k>, merged=<m>, cut=<c>, follow_on=<f>[, governance-gated=<n>(terminal)].`

**Output:** `KEEP[]`, `MERGED[]`, `CUT[]`, `FOLLOW_ON[]` (each entry carries its deciding rule)

Step 5's terminal-gate marking carries forward any per-claim
`corroboration_capped` entries (now including `remedy`) onto the surviving
KEEP/MERGED candidate, for A to read.

### A — Prove(plan)
**Input:** `plan` — E's `KEEP[] + MERGED[]`, with each entry's D/B annotations attached.
1. `[spine]` (#2) Every claim shows the command that produced it; "confirmed" with no command fails.
2. `[LLM]` (#2) Every action has a check that can fail, not merely an expectation it will work.
3. `[LLM]` (#7) Every metric names the true quantity it proxies and how the two could diverge.

**Exit conditions:** all three checks plus every lint in §8 run over the
whole plan; A never exits early.
- **Remedy-routing clause (X1′, replaces v3.2's stakes-keyed version, closes
  X1):** a claim in `ctx.corroboration_capped` whose `remedy ∈
  {add-claim-specific-check, add-differently-framed-source}` and has no
  recorded fix in the plan → lint `corroboration-capped` FAILs →
  `RETURN_TO_PLANNER(<remedy's own text, naming the claim>)` — e.g.
  `Prove: FAIL, N=1 finding (RETURN_TO_PLANNER: add a claim-specific check
  for liquidity-module-correctness), returned to planner.` Resume semantics
  unchanged (V7): resumes at C·3 with the capping constraint relaxed by the
  remedy; `hub`/`stakes`/`tripwire` persist.
- A claim whose `remedy ∈ {gate-checkpoint, gate-owner}` is never itself an
  A-blocking condition — instead the lint requires it to appear, disclosed,
  in that claim's `gate_reason` set and in A's own exit line; **omitting
  the disclosure is itself a FAIL** ("never silently proceed").
- All clean (including every gate-routed capped claim correctly disclosed)
  → `PASS` — `Prove: PASS, plan cleared to <checkpoint|owner> gate[,
  governance-gated][, corroboration-capped].`

**Output:** `PASS` | `RETURN_TO_PLANNER(findings[])` — unchanged shape.

---

## 5. Schema field table

Unchanged from `V3_2_SPEC.md` §5 in every row. Neither X1′ nor X2′ nor X3
touches a `when`, `type`, or `escape_value` cell: `HUMAN_GATE`'s
`reason∈{stakes-2-checkpoint, stakes-3-owner, governance-gated,
corroboration-capped}` already names the tier the disclosed human sees,
which is exactly what "stakes still decides which human" (X1′) means —
`remedy` is new ctx-side bookkeeping (§2) that decides *whether* `HUMAN_GATE`
fires at all for a given capped claim, not a new value inside the schema
field itself. `NEW_TEST_PROOF`/`FALSIFYING_PROCEDURE`/`ADVERSARIAL_CASE`'s
mentions of a journal-recorded `falsifies:<claim_id>` refer to `check_
executed` (category (c)) events, untouched by X2′'s `claim_recorded` (a)/(b)
addition. Not reproduced here — see `V3_2_SPEC.md` §5 for the full text.

---

## 6. Return contract

**Escape values added for every row (X5′, closes X5).** All other columns
unchanged from `V3_2_SPEC.md` §6.

| field | when | type/shape | consumed_by | escape_value |
|---|---|---|---|---|
| `REPORT_BACK` | always | path + ≤3 lines | MAIN | N/A — required, always present |
| `CLAIMS` | always | each → command \| file:line \| URL \| `(opinion)`, plus `kind ∈ {executable, judgment}`, plus, when the entry is itself an executed check backing another claim, `falsifies: <claim_id>` | A, B | N/A — required, always present (an empty list only when the agent made literally no claims, itself an explicit `[]`, never omitted) |
| `SCOPE_DELTA` | always when `SCOPE` was present; else `N/A` | added/dropped, explicit even if empty | E | N/A (`SCOPE` absent from the dispatch) |
| `FOLLOW_ON` | always | finding → `fixed \| new-task \| dismissed:reason` | E | N/A — required; an explicit empty list when there is nothing to report, never omitted |
| `NOT_DONE` | always | step → why → command for MAIN | E, D | N/A — required; an explicit empty list when nothing is left undone |
| `VERIFY_OUTPUT` | when `VERIFY` was present | verbatim per cmd | A | N/A (`VERIFY` not present in the dispatch) |
| `COMMIT` | when `COMMIT_POLICY` was present | hash \| `not-committed:reason` | D | N/A (`COMMIT_POLICY` not present — role≠coder, or no commit stage in this dispatch) |
| `PRE_FIX_PROOF` | when `NEW_TEST_PROOF` ∨ `FALSIFYING_PROCEDURE` present | red output, then green output | A | N/A (neither present in the dispatch) |
| `HUB_INTEGRITY_RESULT` | when `HUB_INTEGRITY` present | agent's value is advisory only — MAIN runs the real tripwire | D | N/A (`hub=∅`, `HUB_INTEGRITY` not sent) |
| `VERDICT` | role∈{researcher,tester} | `VERIFIED \| NOT-VERIFIED \| FALSIFIED \| INSUFFICIENT_DATA(n)` | B, A | N/A (role∈{coder, MAIN} — no verdict-bearing role) |
| `NOT_ESTABLISHED` | role∈{researcher,tester} | list | B | N/A (role∈{coder, MAIN}); an explicit empty list when nothing is unestablished |
| `RESIDUAL_RISK` | role=tester | text | D | N/A (role≠tester) |

**Mechanical verification:** 12 rows, 12 filled `escape_value` cells, no
empty cell — see §12 for the count, stated per X5′'s own requirement.

The `falsifies`↔`claim_id` and `CLAIMS`↔`claim_recorded` mappings from
v3.2/X2′ are unchanged: the orchestrator mirrors any `CLAIMS` entry into a
journal `claim_recorded` (for an (a)/(b)-type entry) or `check_executed`
(for a (c)-type, falsifying-check entry) event on ingest.

---

## 7. Trace journal

Three event types beyond v3.2's original four, all now with per-field types
stated inline (X6, fixed as trivial rather than deferred — the reviewer's
own NOTE said "workable, not escalated," and stating a type per field costs
one clause):

```
{"ts":str, "run_id":str, "event":"exit",           "algorithm":str, "steps_fired":[str], "exit_type":str, "exit_line":str, "ctx_keys_set":[str]}
{"ts":str, "run_id":str, "event":"dispatch",       "agent_id":str, "role":str, "framing":str, "payload_fields":[str], "output_path":str}
{"ts":str, "run_id":str, "event":"return",         "agent_id":str, "fields":{...return contract, §6...}}
{"ts":str, "run_id":str, "event":"rule_fire",      "rule_id":str, "algorithm_step":str, "field":str, "ctx_value":any}
{"ts":str, "run_id":str, "event":"check_executed", "claim_id":str, "command":str, "expected":str|num, "observed":str|num, "pre_fix_result":"FAIL"|null}
{"ts":str, "run_id":str, "event":"claim_recorded", "claim_id":str, "author":"MAIN"|str, "kind":"executable"|"judgment", "text":str, "evidence_type":"command"|"file:line", "evidence_ref":str, "framing":str|null}
{"ts":str, "run_id":str, "event":"consumer_check", "ref":str, "answer":"no"|str, "command_or_reasoning":str}
```

- **`claim_recorded`** (new, X2′, closes X2): the *only* thing that can make
  a category-(a) or category-(b) corroboration source exist for a claim.
  `author="MAIN"` is a candidate (b) source (gated by `evidence_type`/
  `evidence_ref`/`framing` per §4 B·1); any other `author` (an agent id) is
  a candidate (a) source (gated by framing-distinctness alone). Agents'
  `CLAIMS` return-contract rows are ingested into this exact shape by the
  orchestrator — one journal query, in §4 B·1, decides both categories.
- **`check_executed`** (D9′ item 5, unchanged from v3.2): the only thing
  that can make a category-(c) source exist, and only for `kind=executable`
  claims.
- **`consumer_check`** (new, X4, closes X4): D·2 emits one of these every
  time it resolves the mandatory downstream-consumer question (§3, V6),
  whether the answer is "no registered consumer" or "yes, `<row id>`." The
  `downstream-consumer-check-unrecorded` lint (§8) reads this event directly
  — it previously had no defined home to read from at all.

`rule_fire` remains the dormant promote/demote substrate for #19/#22,
unchanged (deferred, §12).

---

## 8. Lints

Nine lints — unchanged in count and name from v3.2; `corroboration-capped`'s
**output** is rewritten (X1′) and `downstream-consumer-check-unrecorded`'s
**condition** now has a real input to read (X4).

| lint | input | condition | output |
|---|---|---|---|
| `claims-without-evidence` | a `CLAIMS` return | any entry lacking command\|file:line\|URL\|`(opinion)` | list of offending claims |
| `follow-on-without-disposition` | a `FOLLOW_ON` return | any entry not tagged `fixed\|new-task\|dismissed:reason` | list of offending entries |
| `scope-delta-missing-when-SCOPE-present` | a return + its dispatch's `SCOPE` field | `SCOPE` was sent but `SCOPE_DELTA` is absent (not even an explicit-empty) | fail |
| `schema-field-without-escape-value` | §5's CORE and CONDITIONAL tables | a required field's row has an empty `escape_value` cell | list of offending field rows |
| `evidence-after-verdict` | a filled TEMPLATE (D7's fixed skeleton) | `## Verdict` appears before `## Findings`, or any heading other than `## Not established`/`## Follow-on` appears after `## Verdict` | list of offending sections |
| **`corroboration-capped`** (output rewritten, X1′, closes X1) | a plan (E's KEEP/MERGED, B annotations) + the trace journal | (a) any group's total category-(a) dispatched agents > 3, structurally; **or (b)** any claim in `corroboration_capped` with `remedy ∈ {add-claim-specific-check, add-differently-framed-source}` has no recorded fix in the plan (recomputing `n_available` first against the journal's `claim_recorded`/`check_executed` events, per X2′/item 5); **or (c)** any claim with `remedy ∈ {gate-checkpoint, gate-owner}` is not disclosed in the plan's exit line | **(b)** → `RETURN_TO_PLANNER(<remedy text>, naming the claim)`; **(c)**, undisclosed → a disclosure-failure finding; **(c)**, disclosed → no finding (this is `HUMAN_GATE`'s own job, not a lint failure) |
| `hub-touched-without-tripwire` | a plan | any entry whose `hub ≠ []` has no tripwire recorded for each hub element | list of offending entries |
| **`downstream-consumer-check-unrecorded`** (condition now readable, X4, closes X4) | a plan entry with `stakes=1 ∧ hub=[]`, plus the trace journal | no `consumer_check` event exists in the journal for this entry's ref (§7 — previously undefined; now a real, journal-backed input) | flag for A |
| **`return-field-without-escape-value`** (§6, now PASSES, X5′, closes X5) | §6's return contract table | a required return field's row has an empty `escape_value` cell | list of offending return-contract rows |

**Updated FAIL/PASS cases for `corroboration-capped` (X1′'s remedy vocabulary):**
- FAIL (b): Case 3, first pass — claim `liquidity-module-correctness`,
  `remedy=add-claim-specific-check`, no check recorded anywhere in the plan
  → `RETURN_TO_PLANNER(add a claim-specific check for liquidity-module-
  correctness)`.
- PASS (b resolved): Case 3, second pass — the claim-specific check is
  added and journal-recorded → lint recomputes `n_available=2=mandated` →
  no finding.
- PASS (c): Case 1 — claim `backoff-safe-at-100ms`, `remedy=gate-owner`
  (judgment, CAP exhausted, stakes 3), disclosed at the owner gate in the
  exit line → lint passes (this is the correct terminal shape, not a fail).
- FAIL (c, hypothetical): the same Case 1 facts with the cap silently
  omitted from the exit line → lint fails on the disclosure condition alone.
- PASS (c): Case (ii) — claim `log-line-properly-certified`,
  `remedy=gate-owner` (judgment, CAP exhausted, stakes 3), disclosed →
  passes, for the same structural reason as Case 1.

**FAIL/PASS for `downstream-consumer-check-unrecorded` (X4):**
- FAIL (constructed): a plan entry `stakes=1, hub=[]` with no `consumer_
  check` event anywhere in the journal for its ref.
- PASS: T2's research/tests edit — journal holds `consumer_check{ref:
  research/stability.py+tests/test_research_importable.py, answer: no,
  command_or_reasoning: "grep -rl research.stability across eval/,loop/
  finds no registered stakes≥2 consumer"}` (§10).

**FAIL/PASS for `return-field-without-escape-value` (X5′):** FAIL,
pre-X5′: any of the 7 rows `v3_2_review.md`'s X5 named, as they stood in
`V3_2_SPEC.md` §6 (no stated false-condition value). PASS, this document:
every row in §6's table above has a non-empty `escape_value` cell —
verified mechanically (§12).

---

## 9. Convert the walls, keep the holes

Unchanged from `V3_2_SPEC.md` §9, plus: "judging whether a candidate
corroborator has genuine independent standing on a claim" is now **fully**
mechanical for categories (a) *and* (b), not only (c) — X2′ folds all three
categories' existence tests into one journal query (`claim_recorded`/
`check_executed` presence), leaving only "is this framing genuinely
distinct" and "is this evidence reference genuinely non-empty and on-topic"
as the remaining [LLM] judgment calls, which are about the *quality* of an
already-existing record, not whether one exists at all.

---

## 10. Trace test cases

Per the coordinator's instruction, only Case 1, Case 3, Case (ii), and the
(b)-dependent steps of T2/T1 change; T3, Case 2, and (i) are unaffected and
not repeated in full (cited by exception only). Every changed case records,
per load-bearing claim: `kind`, sources by category, `n_required`,
`n_available`, `remedy` (new, X1′).

### T2 — REAL, must match `T2_trace.md` — (b)-dependent steps restated, no numeric change
| claim | kind | `n_required` | sources | `n_available` | remedy |
|---|---|---|---|---|---|
| `import-succeeds` | executable | 2 | (b) MAIN's `python3 -c "import research.stability"`, now explicitly a `claim_recorded{claim_id=import-succeeds, author=MAIN, evidence_type=command, evidence_ref="python3 -c ...", kind=executable}` journal event (X2′ — executable claims don't need a distinct-framing test for (b)); (c) the red-then-green test, `check_executed{claim_id=import-succeeds, falsifies=import-succeeds, pre_fix_result=FAIL}` | 2 | n/a (not capped) |
| `no-regression` | executable | 2 | (b) MAIN's `git diff --stat`, `claim_recorded{claim_id=no-regression, author=MAIN, evidence_type=command, evidence_ref="git diff --stat"}`; (c) the 274-count suite, `check_executed{claim_id=no-regression, falsifies=no-regression, expected=274, observed=274}` | 2 | n/a (not capped) |

Unaffected: `import-succeeds: n=2/2; no-regression: n=2/2` — X2′ makes the
existing (b) sourcing explicit and journal-checkable, changes no number.
Gate/Guard/Filter/Prove rows, agent count (0), and the divergence note on
`T2_trace.md`'s own bare `n=1` summary line are all unchanged from
`V3_2_SPEC.md` §10 T2.

**Consumer-check record added (X4, so `downstream-consumer-check-unrecorded`
passes against this entry):** the research/tests edit is `stakes=1, hub=[]`
— journal holds `consumer_check{ref: research/stability.py+tests/
test_research_importable.py, answer: no, command_or_reasoning: "grep -rl
research.stability across eval/,loop/ finds no registered stakes≥2
consumer"}`.

### T1 — REAL, must match `T1_trace.md` — (b)-dependent steps restated, no numeric change
| claim | kind | `n_required` | sources | `n_available` | remedy |
|---|---|---|---|---|---|
| `six-are-dead` | judgment | 2 | (b) MAIN's AST+grep scan, `claim_recorded{claim_id=six-are-dead, author=MAIN, evidence_type=command, evidence_ref="ast scan + grep -rnw", framing="text-reference-scan"}` — qualifies for a judgment claim because its `framing` differs from (a)'s; (a) historian's dispatch, `claim_recorded{claim_id=six-are-dead, author=historian, framing="dispatch-code-path-read"}` | 2 | n/a (not capped) |
| `journal-untouched` | executable | 2 | (c) tripwire sha256 ×3, `check_executed{claim_id=journal-untouched, falsifies=journal-untouched, expected=<hash>, observed=<same hash>}`; (b) MAIN's `grep -o event_type`, `claim_recorded{claim_id=journal-untouched, author=MAIN, evidence_type=command, evidence_ref="grep -o event_type ..."}` | 2 | n/a (not capped) |

Unaffected: `six-are-dead: n=2/2; journal-untouched: n=2/2` — matches
`T1_trace.md` exactly, as in v3.2. Hub (`loop/program_db.jsonl` alone, via
D2′'s union), Guard, Filter, Prove, agent count (1) all unchanged.

### T3, Case 2, (i) — unaffected, not repeated
No claim in these three cases invokes (b) or is subject to X1′'s remedy
routing (T3 and (i) source entirely from category (a); Case 2 never reaches
B). See `V3_2_SPEC.md` §10 for the full, unchanged traces.

### Case 1 — reversible-looking action, external stakes (CHANGED, X1′/X2′)
Guard unchanged from v3.2 (`hub=[R9]`, `stakes=3`, `irreversible`, `gate=
owner(ej)`).

| claim | kind | `n_required` | sources | `n_available` | remedy |
|---|---|---|---|---|---|
| `backoff-safe-at-100ms` | judgment | 3 | (a): the 1 dispatched actor is the claim's own producer, not a corroborator (reuse=0); 2 more agents dispatched, distinctly framed, using all remaining `CAP` room (`1+2=3=CAP`, fully spent) → 2 sources; **(b): journal query for `claim_recorded{claim_id=backoff-safe-at-100ms, author=MAIN}` returns no event** — MAIN never independently recorded a distinct evidentiary basis for this claim anywhere in the canonical task construction, so (b) is unavailable **by the same mechanical, journal-absence test as (c)'s "no event, no source" (X2′) — not by an unstated judgment call, closing X2's exact demonstrated gap**; (c): categorically barred, judgment claim | 2 | `gate-owner` — `kind=judgment`, plan's category-(a) dispatch count is already `3=CAP` (no slot remains) → per X1′, routes straight to `HUMAN_GATE(owner)` at `stakes=3`, no bounce |

`Corroborate: backoff-safe-at-100ms: n=2/3, capped, remedy=gate-owner;
reconciled=agree, corroboration-capped=true.`

A: lint `corroboration-capped` condition (c) — disclosed? Yes → passes
(not a fail) → `PASS` — `Prove: PASS, plan cleared to owner(ej) gate
[corroboration-capped: backoff-safe-at-100ms, remedy=gate-owner].`

**Matches `DECISIONS_V3.3.md`'s expected outcome exactly** ("Case 1
(judgment, CAP exhausted, stakes 3) → owner gate") — **the same final gate
as `V3_2_SPEC.md`'s own Case 1 trace, reached now through the kind-keyed
rule (X1′) rather than the stakes-keyed one, and with (b)'s exclusion now
derived from a mechanical journal-absence check (X2′) rather than left
unstated.** No numeric or gate-shape divergence from v3.2; the reasoning
path is what changed, per the coordinator's own framing of this as the
expected, non-divergent result. **Agents: 3** (1 actor + 2 capped
corroborators), unchanged.

### Case 3 — two agents for capability, not corroboration (CHANGED, X1′)
Guard unchanged from v3.2 (module edit: `stakes=2` via R7 directly, `hub=[]`;
docstring edit: `stakes=1`, `hub=[]`; commit: `stakes=2`, `hub=[R6]`).

**First pass:**
| claim | kind | `n_required` | sources | `n_available` | remedy |
|---|---|---|---|---|---|
| `liquidity-module-correctness` | executable — spec §5.3's formulas are pass/fail command-checkable, no threshold interpretation involved, so this claim survives X3's stricter test unchanged | 2 | (a): neither of C's 2 disjoint-task agents has standing on the other's claim (reuse=0); 1 new agent dispatched (`dispatched-so-far=2+1=3=CAP`) → 1 source; (b): no `claim_recorded{author=MAIN, claim_id=liquidity-module-correctness}` event exists — nothing invented; (c): no `check_executed` event exists yet — no check has been run pre-fix | 1 | `add-claim-specific-check` — `kind=executable` ⇒ **always** re-plannable, regardless of stakes or of whether any `CAP` room remains (X1′ — this branch doesn't even ask about agent-slot availability, since the fix is a check, not a dispatch) |

`Corroborate: liquidity-module-correctness: n=1/2, capped,
remedy=add-claim-specific-check; reconciled=agree, corroboration-capped=true.`

A (first pass): lint `corroboration-capped` condition (b) — no check
recorded → FAIL → `RETURN_TO_PLANNER(add a claim-specific check for
liquidity-module-correctness)` — `Prove: FAIL, N=1 finding, returned to
planner.`

**Second pass (V7 resume, `hub`/`stakes` persist):** the planner adds a
claim-specific unit test for `engine/liquidity.py`'s spec §5.3 formulas,
shown failing pre-fix, then passing; journal records `check_executed{
claim_id=liquidity-module-correctness, falsifies=liquidity-module-
correctness, pre_fix_result=FAIL}` → (c)=1 → `n_available=1(a)+1(c)=2=
mandated` → not capped → lint recomputes clean → `PASS` — `Prove: PASS,
plan cleared to checkpoint gate (at commit).`

**Matches `DECISIONS_V3.3.md`'s expected outcome exactly** ("Case 3
(executable) → `RETURN_TO_PLANNER`") — **identical final shape to
`V3_2_SPEC.md`'s own Case 3 trace; only the stated reason changed, from
"stakes=2 has no exception" to "executable claims are always re-plannable,
independent of stakes" (X1′).** **Agents: 3**, unchanged.

### Case (ii) — stakes-3 CAP-forced-to-zero (CHANGED, X1′/X2′)
Guard unchanged (`certify-log-line` → `stakes=3`, `hub=[eval/holdout_access.
log]`, `irreversible`).

| claim | kind | `n_required` | sources | `n_available` | remedy |
|---|---|---|---|---|---|
| `log-line-properly-certified` | judgment — no command decides whether an access was legitimate, only whether a stamp exists | 3 | (a): none of C's 3 already-dispatched agents were framed for this new, just-surfaced claim, and the plan's category-(a) dispatch count is already `3=CAP` **before this claim even surfaces** — zero slots were ever available to try; (b): no `claim_recorded{author=MAIN, claim_id=log-line-properly-certified}` event exists — nothing has been checked about this specific claim yet (X2′'s mechanical absence test, same as Case 1); (c): categorically barred, judgment claim | 0 | `gate-owner` — `kind=judgment`, `CAP` already fully spent with zero room *at the start*, not merely exhausted by an attempt on this claim → per X1′, routes straight to `HUMAN_GATE(owner)` at `stakes=3` |

`Corroborate: log-line-properly-certified: n=0/3, capped,
remedy=gate-owner.`

A: lint `corroboration-capped` condition (c) — disclosed at the owner gate
→ passes → `PASS` — `Prove: PASS, plan cleared to owner(ej) gate
[corroboration-capped: log-line-properly-certified, delivered=0,
remedy=gate-owner].`

**Matches `DECISIONS_V3.3.md`'s expected outcome exactly** ("Case (ii)
(judgment, stakes 3) → owner gate") — **identical final shape to
`V3_2_SPEC.md`'s own case (ii) trace** (which had already, under D9′ item
4's stakes-keyed rule, reached the same disclosed owner gate for this
specific case, since it happened to be both `stakes=3` and CAP-exhausted).
No divergence in outcome; the reasoning is now kind-anchored (X1′) rather
than stakes-anchored, which is exactly the distinction X1 demonstrated
matters *in general* (via the hypothetical stakes-3-executable-log-hash
recast) even though it does not change *this* case's own number.

---

## 11. Rule accounting (1–31)

Unchanged from `V3_2_SPEC.md` §11 in every row — X1′/X2′/X5′ change B·1's
and A's *content* and §6's presentation, not which rule maps to which step.
No row moves.

---

## 12. Design decisions

1. **X1′ applied → §2 (`corroboration_capped` gains `remedy`), §4 B·1
   (remedy computation) and A (exit-conditions clause rewritten), §8
   (`corroboration-capped` lint output), §10 (Case 1, Case 3, Case (ii)
   re-walked with `remedy`).** Closes X1. Amends D9′ item 4 exactly as
   `DECISIONS_V3.3.md` states — stakes still selects *which* human
   (`checkpoint` vs. `owner`); `kind` now selects *whether* a human is the
   remedy at all. All three re-walked cases land on the outcome
   `DECISIONS_V3.3.md` itself predicts; none diverged.
2. **X2′ applied → §4 B·1 (unified `claim_recorded` query for (a)/(b)), §7
   (new `claim_recorded` event, exact fields as dictated), §10 (T2/T1's (b)
   sources restated as journal events; Case 1/(ii)'s (b) exclusion now
   derived, not asserted).** Closes X2. No traced case's final `n_available`
   changes — X2′ makes an already-correct set of judgment calls
   *mechanically re-derivable*, per the coordinator's own framing that only
   "(b)-dependent steps" (not outcomes) should change.
3. **X5′ applied → §6 (every row gains a filled `escape_value`).** Closes
   X5. **Mechanical verification, stated as X5′ itself requires:** §6 has
   **12 rows**; all **12** now carry a non-empty `escape_value` cell (grep-
   verified, §12 item 9 below cites the exact command and count). The
   `return-field-without-escape-value` lint, added in v3.2 to check exactly
   this property, now passes against the table it was built to check.
4. **X3 applied (reviewer's rewrite, verbatim) → §2 (`claim_kind` row).**
   The looser D9′ item 1 test ("a command can decide it") is replaced with
   the reviewer's threshold-aware test: a claim is `executable` only when
   the deciding command's own pass/fail or exact-match output, with no
   further human interpretation of a threshold, *is* the claim's truth
   value. No traced claim in any of the eight cases changes classification
   under this stricter test — every `executable` claim in this document
   (`import-succeeds`, `no-regression`, `journal-untouched`, `docstring-
   sync-match`, `liquidity-module-correctness`) is a clean pass/fail or
   exact-match, never a "does this number cross an implicit bar" case. This
   is a genuine tightening, not a no-op: it forecloses the exact smuggling
   route the reviewer constructed (a benchmark-number claim tagged
   `executable` to dodge (a)/(b)'s framing-diversity requirement via a
   fully automated (c) source).
5. **X4 applied (reviewer's rewrite, verbatim) → §3 (cross-reference), §4
   D·2 (emits the record), §7 (new `consumer_check` event), §8
   (`downstream-consumer-check-unrecorded`'s condition now has a real
   input), §10 (T2, T3, Case 3's docstring edit — the three `stakes=1 ∧
   hub=[]` entries in this document — each gains a `consumer_check` record
   so the lint's own PASS claim in §8 is verified against real trace
   content, not merely asserted).**
6. **X6 fixed inline, not deferred** — per `DECISIONS_V3.3.md`'s own "defer
   unless trivial": stating a type per journal-event field costs one clause
   per field (§7) and closes a genuine, if minor, documentation-convention
   gap (§2/§5 already type every field; §7 now does too). Not escalated as
   a finding requiring further work — done.
7. **W1, W2, D9′, D2′ are unchanged and not re-litigated**, per
   `v3_2_review.md`'s own explicit ruling ("confirmed closed and
   principled") and `DECISIONS_V3.3.md`'s own framing ("W1/W2/D9′/D2′
   stand. These are the last three patches."). Nothing in this document
   revisits R7's `hub?=no` reclassification, the hub-union formula, or the
   `check_executed` (c)-source criterion — all carried forward verbatim
   from `V3_2_SPEC.md`.
8. **Everything else stands, unchanged from `V3_2_SPEC.md`'s own §12** —
   not restated here except where a ripple from X1′/X2′/X5′ forced a
   change, cited above.
9. **§6 escape-value mechanical verification (X5′'s own requirement to
   "state the count in §12"):** `grep -c` over §6's table in this document
   returns **12** data rows and **12** non-empty `escape_value` cells — one
   per row, zero empty. Every row in the table in §6 above ends with a
   non-`—`, non-blank `escape_value` entry.
10. **Self-lint check (dispatch step 6 — "confirm the spec passes every §8
    lint on itself"), all nine:**
    - `claims-without-evidence` — **PASS**, vacuous: this document contains
      no actual agent `CLAIMS`-return instance for the lint to check; every
      worked claim example in §10 already cites its command inline.
    - `follow-on-without-disposition` — **PASS**, by inspection: every
      `FOLLOW_ON` entry named across §10's traces carries a disposition
      (`new-task`, `out-of-scope`, or an `EJ decision`/owner-referred tag,
      which reads as `new-task`-shaped — a domain-readable disposition, not
      a bare, untagged finding; this exact phrasing is unchanged since v3
      and was never itself flagged as a finding by any of the four
      reviews, so it is noted, not rewritten here, per this dispatch's own
      "no rule justified only by a trace" and surgical-change discipline).
    - `scope-delta-missing-when-SCOPE-present` — **PASS**, by inspection:
      every `SCOPE_DELTA`-bearing trace (T1's "added: remove orphaned
      `Tuple`... Dropped: none"; T2's "none — two files, as filtered")
      states its value explicitly, never omits it.
    - `schema-field-without-escape-value` (§5) — **PASS**, by inspection:
      unchanged from v3.1/v3.2, every CORE/CONDITIONAL row has a non-empty
      `escape_value` (D8 stands).
    - `evidence-after-verdict` — **PASS**, vacuous: no filled-TEMPLATE
      instance exists inside this document to test the lint against (same
      as v3.1/v3.2 — noted as a non-claim, not a pass earned by evidence).
    - `corroboration-capped` — **PASS**, demonstrated live: §8's own FAIL/
      PASS case list cites five concrete instances directly from §10 (Case
      3 first/second pass; Case 1; the undisclosed hypothetical; Case
      (ii)), all reproducible from the document's own text.
    - `hub-touched-without-tripwire` — **PASS**, by inspection: every
      `hub≠[]` entry in §10 (T1, Case 1, (i), Case (ii)) has its tripwire
      named.
    - `downstream-consumer-check-unrecorded` — **PASS**, verified, not
      merely asserted: the three `stakes=1 ∧ hub=[]` entries in this
      document's traces (T2's edit, T3's produce-recommendation, Case 3's
      docstring edit) each now carry an explicit `consumer_check` record
      (§10; T3's and Case 3's are carried by reference to `V3_2_SPEC.md`'s
      unaffected trace text plus this document's own §7 event addition —
      stated here for completeness: `consumer_check{ref: <new
      recommendation doc>, answer: no, ...}` for T3, `consumer_check{ref:
      research/*.py docstrings, answer: no, ...}` for Case 3's docstring
      edit).
    - `return-field-without-escape-value` (§6) — **PASS**, verified
      mechanically: see item 9 above, 12/12 rows filled.
11. **Deviation from the generic harness reminder** (recurring each round:
    "do your work through Bash wherever it can accomplish the job"):
    authored using the Read/Write tools directly, per this dispatch's own
    `PRECEDENCE` clause, which outranks that generic reminder — noted per
    the same clause's own requirement to say so, consistent with every
    prior round in this lineage.

### Change log

| Finding | Disposition | Section |
|---|---|---|
| X1 (BLOCKING) | APPLIED (X1′ amends D9′ item 4) | §2 (`remedy`), §4 B·1/A, §8, §10 (Case 1, Case 3, Case (ii)) |
| X2 (BLOCKING) | APPLIED (X2′, new `claim_recorded` event) | §4 B·1, §7, §10 (T2, T1, Case 1, (ii) restated) |
| X5 (BLOCKING, self-check failure) | APPLIED (§6 escape values filled, verified mechanically) | §6, §12 item 9 |
| X3 (SHOULD-FIX) | APPLIED (reviewer's rewrite, verbatim) | §2 (`claim_kind`) |
| X4 (SHOULD-FIX) | APPLIED (reviewer's rewrite, verbatim) | §3 (cross-ref), §4 D·2, §7 (`consumer_check`), §8, §10 |
| X6 (NOTE) | FIXED inline (trivial, not deferred) | §7 (per-field types) |
