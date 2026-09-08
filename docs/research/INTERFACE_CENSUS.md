# Interface census — what our own agent runs say about the tool surface

Scope: every non-successful `tool_call` event in every journal under `ablation/runs/**`
(attempt1–attempt4), classified, attributed to a candidate prevention mechanism, and
costed. Framing: internal measurement only. No prior art, no contrarian case — this
document exists to make the interface decision falsifiable against our own data.

Repo state when measured: `ancient-games` @ `3d201a4`, working tree clean,
`python3 -m pytest -q` → **318 passed in 6.31s** (run before and unchanged after; this
investigation wrote no code).

---

## 0. Headline

| | |
|---|---|
| Tool calls across all runs | **289** |
| Non-successful | **53 (18.3%)** |
| Of those, refusals that are the system working as designed (must NOT be "fixed") | **9 (17.0%)** |
| Of those, harness defects where **no** argument would have been accepted | **9 (17.0%)** |
| Of those, genuine caller-side interface failures | **35 (66.0%)** |
| Failure rate on harness v1.1 (before `tools --schema`) | **35/97 = 36.1%** |
| Failure rate on harness v1.3 + v1.4 (schema in the packet) | **18/192 = 9.4%** |

The single most important number in this document is not in the cross-tab. It is that
**`record_claim` + `record_check` went from 14 failures in 34 calls to 0 failures in 93
calls** the moment the enum values were printed into the task packet (Fisher one-sided
p = 9.0e-10), and that this drop **cannot** be explained by the boundary validation
that landed in the same commit — a validated-but-rejected call is still a failed call
and would still be counted here. Only *information reaching the model* drives a failure
class to zero. The "put the schema in the prompt" experiment has already been run in
this repo, and it worked.

## 1. Corrections to the rough pass

The rough pass counted **53** declines (correct) and bucketed them
29 SEMANTIC / 17 ARG-SHAPE / 6 unknown-tool / 1 invariant refusal. Corrected:

| rough | corrected | why the rough number was wrong |
|---|---|---|
| 29 SEMANTIC | **1** | The regex read the *proximate* reason string. Only one call (`guard`, attempt2/UC3 #30) was type-legal, precondition-legal and factually wrong about the world. |
| 17 ARG-SHAPE | **27** (24 ENUM + 3 TYPE) | 11 arg errors were journaled as `internal-error: <ValueError from journal.validate_event>` and 8 more as `internal-error: False|True|'no'`, so a reason-string regex filed them elsewhere. |
| 6 unknown-tool | **6** | Correct. |
| 1 invariant refusal | **1** `refused_by=I4`, but **9** declines are the system correctly refusing | `refused_by` is set only by the five invariants checked in `loop.step`. `checkpoint-not-cleared` (×4) and `no-prove-pass` (×4) are tool-body preconditions with `refused_by=None`. Keying "correct behaviour" on `refused_by` undercounts it 9×. |
| — | **9 FRAMEWORK** (new bucket) | Calls no argument could have satisfied: 5 from H7 ctx contamination, 3 from a v1.3 gate bug, 1 from a missing `done` capability. The rough pass had nowhere to put these; they are the most consequential class because "fixing the interface" would not have removed one of them. |

**Five of the 53 had entirely legal arguments** (`prove`, attempt2/UC1 #17,#18,#23,#24,#25).
They failed because a *different* call 15 steps earlier wrote an unvalidated `False` into
`ctx.governance_gated` before validating it (H7). Any classification built from the reason
string alone will mis-file these.

## 2. The corrected census

Per-call table: `docs/research/interface_census_rows.json` (generated; see §7 for the script).
Category definitions, fixed before counting:

| code | definition |
|---|---|
| `TRANSPORT` | (a) malformed CLI/JSON — the call never reached a tool's argument surface |
| `TYPE` | (b) wrong JSON type, or a missing required field |
| `ENUM` | (c) right type, value outside a **static** enum |
| `XFIELD` | (d) constraint referencing **other fields of the same call** (+ the static registry) |
| `PRECOND` | (e) constraint referencing **prior state** (journal / ctx / repo) |
| `SEMANTIC` | (h) type-legal and precondition-legal, but factually wrong about the world |
| `FRAMEWORK` | (g) harness defect — **no** argument would have been accepted |

Ranking rules, fixed before counting:
* **R1** Primary category is the **caller-side** defect when one exists. `FRAMEWORK` is used
  only when nothing the caller could have written would have been accepted.
* **R2** `correct_by_design` is an **orthogonal flag**, not a category: true when the refusal
  is the safety or ordering property the system exists to enforce.
* **R3** Mechanism = the cheapest single mechanism that would have **prevented** the rejected
  call, not one that merely diagnoses it faster.

```
CATEGORY       n      %
ENUM          24  45.3%
PRECOND        9  17.0%
FRAMEWORK      9  17.0%
TRANSPORT      6  11.3%
TYPE           3   5.7%
SEMANTIC       1   1.9%
XFIELD         1   1.9%
                53
correct_by_design (the refusal is the property working): 9/53 = 17.0%
```

The 9 correct-by-design refusals, which optimising away would be a regression:

| n | refusal | what it protects |
|---|---|---|
| 4 | `commit` → `checkpoint-not-cleared` | the human gate. Fired in 4 runs; every agent stopped and printed `NEED_APPROVAL` rather than trying to write its own approval. |
| 4 | `done` → `no-prove-pass` | I2′ ordering: you cannot declare done before `prove` passes. |
| 1 | `guard` → `refused_by=I4` `hard_blocked` | the owner gate, fired correctly *for the declaration the agent gave* (it had listed `eval/protocol.json` as a **consumer** of the file it was writing). |

## 3. Category × mechanism cross-tab — the deliverable

Mechanisms as named in the brief. `M0` ("fix the framework") and `--` ("nothing should
prevent this") were added because 18 of 53 fit neither the brief's six nor each other.

```
               M1    M2    M4    M5    M0    --   tot
ENUM           14     0    10     0     0     0    24
TRANSPORT       0     6     0     0     0     0     6
TYPE            3     0     0     0     0     0     3
XFIELD          0     0     0     1     0     0     1
PRECOND         0     0     0     1     0     8     9
SEMANTIC        0     0     1     0     0     0     1
FRAMEWORK       0     0     0     0     9     0     9
tot            17     6    11     2     9     8    53
```

| | mechanism | n | % |
|---|---|---|---|
| **M1** | JSON Schema at the boundary (types / required / enum), shown **and** enforced | 17 | 32.1% |
| **M4** | worked example / field-semantics note per tool in the schema output | 11 | 20.8% |
| **M0** | no interface mechanism — fix the framework | 9 | 17.0% |
| **--** | none should prevent it (correct by design) | 8 | 15.1% |
| **M2** | constrained / structured invocation (shape made impossible) | 6 | 11.3% |
| **M5** | a better error message alone (today's repair loop, clearer) | 2 | 3.8% |
| **M3** | dynamic tool availability (tool withheld when preconditions fail) | **0** | 0% |
| **M6** | nothing representational — the model could not read what it needed | **0** | 0% |

Three results in that table decide the design:

**(i) M1 + M4 = 28/53 (52.8%), and both are already built and already shipped.**
`tools --schema` prints exactly these — enum values, types, and the `NOTES` dict of
field-semantics notes. Every one of those 28 failures is from **attempt1/attempt2**,
i.e. before the schema existed. Zero are from attempt3/attempt4. This is the A/B in §4.

**(ii) M3 scores zero, and that is a real finding, not an absence of data.**
Dynamic tool availability withholds a tool when its preconditions do not hold. Nine of
the failures are precondition failures — and in 8 of the 9 the *right* behaviour is to
offer the tool and refuse it loudly, because the refusal is the human gate or the
ordering invariant, and the agent's correct next move was to stop and ask (which all
four agents did). Withholding `commit` would have converted a legible "stop, get
approval" into an invisible absence. The one remaining precondition failure
(`corroborate.action`) is not fixed by withholding `corroborate` either; it is fixed by
telling the caller which values are legal.

**(iii) M6 scores zero — nothing here was unknowable.** The one candidate was
`corroborate`'s `ctx.actor` precondition, since no tool reads ctx and no packet names the
ctx file. But the legal keys are written by the run's own `gate`/`guard` args, which
`read_journal` returns; I verified all four cases are reconstructible from the journal
the agent could already read (§5.3). The information was present and unsurfaced, which is
an M5 problem, not an M6 one.

**Second-order effect not in the table.** The 5 `FRAMEWORK`/H7 collateral failures were
caused by an earlier unvalidated `governance_gated`. M1 on that one field would have
prevented them upstream. Counting that path, M1 accounts for **22/53 (41.5%)**.

## 4. What the schema already said and the agent still got wrong

The brief's question — "is this an attention problem or a missing-information problem?"
— has to be asked against **the packet the agent actually received**, not against
today's `tools --schema`. The packets are versioned: attempt1/2 ran on the packet at
`839c3be` (before `tools --schema` existed); attempt3/4's packets are checked in beside
their journals.

```bash
git show 839c3be:ablation/packets/UC1.md | grep -n "governance_gated\|evidence_type"
#  59:  `role`, `probe: ArtifactRef`, ..., `governance_gated`,      <- name only, no type, no enum
#  50: record_claim ... {"evidence_type": "str", ...}               <- "str", no enum

grep -n "governance_gated\|one of:" ablation/runs/attempt3/UC3.packet.md | head
# 108:    governance_gated: str = 'none'  one of: none | R1 | R2 | R3 | R9  # ... never a bool
# 207:  mechanism: str  one of: interpreter-import | pytest-fail-first | ... | other:<name>
# 209:  pre_fix_result: str  one of: FAIL | null
# 216:  evidence_type: str  one of: command | file:line
```

Per-field A/B, counting calls not runs:

| field | documented in packet? | failures / calls |
|---|---|---|
| `gate.task.governance_gated` | attempt1/2: **no** | **10 / 12** |
| | attempt3/4: yes (enum + "never a bool") | **0 / 6** |
| `record_claim.evidence_type`, `record_check.mechanism`, `.pre_fix_result`, `.falsifies` | attempt2: **no** | **14 / 34** |
| | attempt3/4: yes (enums + the `falsifies` note) | **0 / 93** |
| `corroborate.framings` | attempt2/3: `"dict"` only | **3 / 14** |
| | attempt4: `dict[str, list[str]]` + a worked example | **0 / 9** |
| `guard.action.refs[].consumers` | attempt2: **no** | **1 / 9** |
| | attempt3/4: yes (the D2′ note) | **0 / 10** |
| `guard.action.tripwires` (keys) | attempt3/4: **yes** (form documented) | **1 / 10** |

Fisher one-sided exact, computed on the counts above:

```
record_claim+record_check: 14/34 before vs 0/93 after -> p = 8.99e-10
gate.governance_gated:     10/12 before vs 0/6  after -> p = 1.51e-03
all calls, v1.1 vs v1.3+:  35/97 before vs 18/192 after-> p = 9.52e-08
```

**Answer to the brief's question: it was a missing-information problem, not an attention
problem — with exactly one exception.** In every arg-shape/enum failure except one, the
packet the agent held did **not** document the violated constraint. The exception is
`guard.action.tripwires` (attempt4/UC3 #07), and it is not an attention failure either:
the schema documents the *form* of the key (`{hub-name-or-matched-ref-path: command}`)
but the *admissible* keys are computed per call from a registry lookup over that call's
own refs — here the lookup returned `hubs: []`. No static schema can carry that. The
agent read the error, which does print the computed hub list, and got it right on the
very next call.

**Confound, named and resolved.** The schema landed in the same commit (`481e553`) as
the typed adapter validation, so "shown" and "enforced" are confounded across the A/B.
They separate logically: a call rejected by boundary validation is still a *rejected
call* and is still counted in this census. Validation alone therefore cannot move a
failure class to **zero**. Only the caller ceasing to emit the bad value can, and that
requires the value reaching the model. The confound does not survive contact with the
measurement.

**Caveat.** n = 4 agents before, 4 after, on partly different task variants (UC2 → UC2J).
The per-call Fisher figures are not per-agent independent — one agent's systematic habit
contributes many calls. Directional and large, not a controlled trial.

## 5. Live defects at HEAD, proven by constructed cases

Real journals do not exercise boundaries; the record_check failures all carry *three*
simultaneous defects, so what today's code does with each one in isolation is invisible
in the data. Constructed cases (§7 script 4), run against `3d201a4`:

### 5.1 `record_check` is the one recorder with no boundary validation — still, at HEAD

```
A1 control: legal mechanism, falsifies == claim_id            -> [OK]
A2 out-of-enum `mechanism` only                               -> [internal-error] check_executed.mechanism must be one of (...)
A3 out-of-enum `pre_fix_result` only                          -> [internal-error] check_executed.pre_fix_result must be one of ('FAIL', None)
A4 documented escape hatch `other:<name>`                     -> [OK]
A5 record_claim out-of-enum evidence_type (the FIXED tool)    -> [invalid-args] evidence_type must be command | file:line, got 'suite' (str)
A6 record_check expected/observed as int (schema says str|int)-> [OK]
A7 record_check expected as a list                            -> [internal-error] check_executed.expected must be (<class 'str'>, ...)
```

`record_claim` validates `kind`, `evidence_type` and `closed_world` before writing.
`record_check` validates only `claim_id`/`mechanism`-is-a-str (`require_str`) and
`falsifies`; `mechanism`'s enum, `pre_fix_result`'s enum and `expected`/`observed`'s type
are left to `journal.validate_event` to raise, and the adapter's blanket
`except Exception` turns a caller error into `internal-error:` with a raw Python type
repr. This violates the tool layer's own stated contract (`_shared.invalid_args`:
"a bad input is the caller's error, named by field and accepted values — never an
`internal-error`").

**It also mis-signals the exit code.** End to end through the CLI:

```
call record_check '{"...","mechanism":"suite-count",...}'            -> ok=true,  exit 0
call record_check '{"...","mechanism":"grep over the written file"}' -> ok=false, exit 0   <-- caller error, "executed"
call record_claim '{"...","evidence_type":"suite"}'                  -> ok=false, exit 2   <-- correct
```

`cmd_call` returns exit 2 only when the reason starts `invalid-args:` (H10). A malformed
`record_check` therefore exits **0**, the code documented as "executed". Any wrapper or
supervisor keying on the exit code sees a success.

### 5.2 H7 contamination is the root cause of 5 "internal errors" — proven with a control

Against the v1.1 tree (`git archive 839c3be`), with a control that could have failed:

```
A. prove on a FRESH ctx (control):        ok=True   ctx.governance_gated='none'
B. gate with governance_gated=False:      ok=False  reason='internal-error: False'
   ctx.governance_gated AFTER the failed gate = False        <-- partial write
C. prove on the SAME ctx, args identical to the control: ok=False 'internal-error: False'
D. corroborate on the same ctx:                          ok=False 'internal-error: False'
```

The control passing is what makes this a root-cause finding rather than a story.
`stages.gate` assigned `ctx.governance_gated` before validating it, so one unvalidated
boolean at call #2 poisoned every ctx-reading tool for the rest of attempt2/UC1 — the
run with the worst failure rate in the corpus (16/26 = 61.5%, and `gate` never once
succeeded in it). Fixed at HEAD by the H7 adapter guard (`ctx_snapshot`/`ctx_restore`)
plus `gate`'s own `governance_gated` check.

### 5.3 Three `ctx.actor` declines were unsatisfiable, not a naming mistake

attempt3/UC2J #22, #24, #28 all read
`ctx.actor has no entry for action '<name>' (set at C·3/C·4 or by D)`. The obvious
reading — the agent guessed the action name wrong — is wrong. Against the v1.3 tree
(`git archive bc52866`), replaying that run's own `gate` args verbatim:

```
gate (attempt-3 #02 verbatim): ok=True exit=PLAN_NEEDED[]
  ctx.actor = {}   execution_status = None
  corroborate(action='delete-helpers')      -> ok=False  ctx.actor has no entry ...
  corroborate(action='delete-dead-helpers') -> ok=False  ctx.actor has no entry ...
  corroborate(action='classify-helpers')    -> ok=False  ctx.actor has no entry ...
  corroborate(action='commit')              -> ok=False  ctx.actor has no entry ...

CONTROL: same task, capability trimmed so C.4 does not split
  gate: ok=True exit=PLAN_NEEDED ctx.actor={'classify-helpers','commit','delete-helpers'}
  corroborate(action='delete-helpers') -> ok=True
```

At v1.3 the C·4 **split** branch of `stages.gate` (`count > 3` → `PLAN_NEEDED[]`) returned
without ever running `ctx.actor.update(task.actors)`. Because the agent's task had four
capabilities, its first `gate` took the split branch, and **no** action name was
acceptable to `corroborate` for the rest of the run. The agent's actual repair — calling
`gate` twice more until it happened to take the non-split branch (#27 `RESOLVED`, #30
`PLAN_NEEDED`) after which `corroborate` immediately succeeded — is visible in the journal
and is exactly what you would do if you had guessed the framework was in a bad state.
Fixed later by `47c0bea`, which is *after* both ablations.

By contrast attempt4/UC2J #46 **is** a genuine caller error: that run's `gate` took the
normal branch and set `{commit, edit-program_db.py, run-suite, scan-for-references}`; the
agent passed the whole task sentence `'delete the dead helpers from loop/program_db.py and
commit on master'` as the action. I checked all four cases for whether the legal set was
reconstructible from the journal: it was in all four (script 5). So this is an unsurfaced
enum, not unknowable state — and the fix is one this repo already ships elsewhere:
`record_check`'s `falsifies` error **enumerates** the legal values ("claim_ids recorded in
this run"), and `falsifies` never failed again after v1.2. `corroborate`'s message names
the spec section instead of the values.

## 6. Cost of the repair loop

Definitions fixed before measuring: a **wasted call** is any `tool_call` with `refused_by`
or `reason` set (i.e. not `_shared.event_ok`); a **fail streak** is a maximal run of
consecutive wasted calls; a **recovery gap** is the number of calls from a wasted call up
to and including the next successful call *to the same tool*.

```
run                harn  calls fail     % maxstreak maxgap  tool never recovered
attempt1/UC1       v1.1      2    1  50.0         1      0  gate
attempt1/UC2       v1.1      2    1  50.0         1      0  gate
attempt1/UC3       v1.1      1    0   0.0         0      0  -
attempt2/UC1       v1.1     26   16  61.5         6      5  gate(x5), prove(x5), done, corroborate
attempt2/UC2       v1.1     28    6  21.4         2      3  -
attempt2/UC3       v1.1     38   11  28.9         4      8  done, guard
attempt3/UC2J      v1.3     46    5  10.9         1     13  -
attempt3/UC3       v1.3     37    2   5.4         1      2  done
attempt4/UC2J      v1.4     62    8  12.9         6      2  <json-blob>(x6)
attempt4/UC3       v1.4     47    3   6.4         1      1  done(x2)

TOTAL 289 calls, 53 wasted (18.3%)
  v1.1  35/97  = 36.1%
  v1.3   7/83  =  8.4%
  v1.4  11/109 = 10.1%
```

**Longest retry chain on one logical action: 5 calls, never resolved.** attempt2/UC1
called `gate` five times (#02, #03, #04, #22, #26) and `gate` never succeeded in that run.
The agent probed the field systematically — `false` → `false` → `false` (unwrapped) →
`true` → `"no"` — which is precisely the search a caller runs when an enum's members are
not printed anywhere. **Longest unbroken streak of failed calls: 6** (attempt4/UC2J
#33–#38, six consecutive `<json-blob>` transport errors, all identical in shape).

**Did a run hit its ceiling because of retries? Yes — attempt3/UC2J.** Documented in
`docs/ABLATION_2.md`: the ceiling fired at 44 with `commit` and `done` still to go, and
MAIN raised it to 48; the finished journal is 46 calls. That run's 5 failures break down
as 3 unsatisfiable `ctx.actor` declines (§5.3), 1 `framings` type error, 1 correct-by-design
`commit` refusal — plus the 2 extra `gate` calls the agent spent working around the
`ctx.actor` loss. Removing the 4 avoidable calls puts the run at 42 ≤ 44 and the ceiling
never fires. *Arithmetic is exact; the counterfactual is inferential — a different call
sequence could have gone differently.*

**One defect surfaced per call.** The journal validator raises on the first bad field, so
a call with three bad fields costs three round trips. attempt2/UC3 recorded three checks:
#09/#10/#11 all failed on `pre_fix_result`, the agent fixed that, #14/#15/#16 all failed
on `mechanism`, the agent fixed that, #17/#18/#19 succeeded. **Three checks, nine calls.**
This is the cheapest thing in the whole census to fix and it is not a schema question: it
is "validate all fields and report all violations", which `corroborate._validate` already
declines to do too (it returns on the first bad claim).

## 7. Field-level hotspots

```
  10  gate.task.governance_gated            (+5 more via H7 contamination = 15)
   6  <cli>.argv[0]  (the tool-name positional)
  10  record_check.{mechanism, pre_fix_result, falsifies}   (all 10 calls carried >=2 of the 3)
   4  record_claim.evidence_type
   4  corroborate.action                    (3 of them framework, 1 genuine)
   3  corroborate.framings
   1  guard.action.refs[].consumers
   1  guard.action.tripwires (keys)
   1  done.deliverables
```

Excluding the 8 correct-by-design declines, **three surfaces account for 26 of 45
(58%)** — `gate.governance_gated`, `record_check`'s three fields, and the CLI tool slot;
counting H7 collateral, **31 of 45 (69%)**.

So: does that argue for fixing three fields rather than building a general mechanism?
**Neither, on this data — because the general mechanism was already built and has already
collected its winnings.** Two of those three hotspots (`governance_gated`,
`record_check`'s fields) are at **zero failures** across 99 calls since the schema
started printing their enums (99 calls: 6 `gate`, 93 `record_claim`/`record_check`). The residual, measured on harness ≥ v1.3 (192 calls, 18
failures), is:

| residual failure | n | still live at HEAD? |
|---|---|---|
| correct by design (`commit`, `done`) | 5 | yes, and should be |
| `ctx.actor` split-path bug | 3 | **no** — fixed by `47c0bea` |
| `done.deliverables` gap | 1 | **no** — fixed by `33da012` |
| `corroborate.framings` type | 2 | **no** — schema note added in v1.4, 0/9 after |
| CLI tool-slot collapse | 6 | **yes** |
| `corroborate.action` not in `ctx.actor` | 1 | **yes** |
| `guard.action.tripwires` keys | 1 | **yes**, and correctly handled by the repair loop |

**Eight live interface failures remain, and six of them are the CLI call shape.**

## 8. What the data supports

Stated as proved / reasoned, per the brief.

**Proved (measured or constructed and run):**
1. 53/289 calls failed; 9 are the system working as designed; 9 are harness defects no
   argument could have avoided; 35 are caller-side.
2. Failure rate fell 36.1% → 9.4% when `tools --schema` entered the packet; the
   enum-bearing tools went to 0/93. Boundary validation cannot explain a drop to zero.
3. `record_check` at HEAD still leaks caller errors as `internal-error:` for
   `mechanism`, `pre_fix_result` and `expected`, and exits 0 while doing it (§5.1).
4. `stages.gate`'s pre-validation ctx write (v1.1) caused 5 failures in calls with legal
   args; control passed (§5.2).
5. Three `ctx.actor` declines at v1.3 were unsatisfiable by any argument; control passed
   (§5.3).
6. In all four `ctx.actor` cases the legal value set was reconstructible from the journal
   the agent could already read.

**Reasoned but not verified:**
* The ceiling counterfactual for attempt3/UC2J (arithmetic exact, behaviour assumed).
* That constrained/structured invocation would have prevented the 6 transport failures.
  No run in this corpus used a structured invocation path, so this is inference from the
  failure's shape (args JSON in the tool-name positional), not measurement.
* Attributing each failure to *one* minimal mechanism. Several admit more than one; the
  cross-tab reports the cheapest sufficient one under R3.

**Insufficient data (do not report as "no effect"):**
* Whether a worked example per tool beats an enum listing. They arrived together.
* The frequency of the CLI tool-slot collapse: 6 occurrences, **1 agent, 1 run**. The
  defect is real and reproducible; its rate is `INSUFFICIENT_DATA` (n=1 run).
* Whether `record_check`'s missing validator costs anything at HEAD: zero occurrences
  since the enums were documented, so the *frequency* is unmeasured. The defect is proven
  by construction; the cost is not.
* All per-task results are n=1 run per task per attempt, as `docs/ABLATION_1–3` already say.

**The single highest-leverage fix the data supports:** *not a new mechanism* — finish
applying the one that already worked, in the two places it was not applied.
1. Give `record_check` the boundary validator every other recorder has
   (`mechanism` enum incl. `other:<name>`, `pre_fix_result` enum, `expected`/`observed`
   type), so caller errors return `invalid-args:` and exit 2. Proven broken at HEAD (§5.1);
   ~10 lines; matches `record_claim`'s existing shape.
2. Make every run-dependent field's rejection **enumerate the legal values**, as
   `record_check.falsifies` already does and `corroborate.action` does not. This is the
   only mechanism that touches the `PRECOND`/`XFIELD` residual, and no static schema can.

The one genuinely new mechanism the data argues for is **M2, structured invocation** —
it is the sole mechanism addressing the largest live cluster (6 of the 8 remaining live
failures), and no schema, example or error message can help there because the call never
reaches the argument surface. Flagged n=1 run.

**What the data argues *against*:** more general schema machinery (M1/M4 are at their
ceiling — the classes they can express are already at zero), and dynamic tool
availability (M3 = 0/53; in 8 of 9 precondition cases withholding the tool would replace
a legible refusal that agents correctly acted on with an invisible absence).

## 9. Reproduction

Journal semantics, checked before aggregating: `Journal.read()` is run-scoped and
`read_all()`/`read_events` are not. Every file under `ablation/runs/**` was verified to
hold **exactly one** `run_id` (asserted in script 1), so the two coincide here; the
unscoped `read_events` is used, which is the reader `ablation.score` itself is sanctioned
to use (`journal.read_events` docstring). Success is `_shared.event_ok`:
`refused_by is None and reason is None` — **not** `exit_type`, which carries the tool's
semantic exit and is `None` on plenty of successful calls.

Scripts (write them anywhere outside the repo; each is standalone):

**1 — census** (the 53 rows + the one-run-per-file assertion)
```python
import json, glob, os, sys
REPO = "/home/smoke01/dev/ancient-games"; sys.path.insert(0, REPO)
from ancient_games.journal import read_events
rows, per_run = [], {}
for f in sorted(glob.glob(os.path.join(REPO, "ablation/runs/**/*.jsonl"), recursive=True)):
    events = read_events(f)
    run_ids = {e["run_id"] for e in events}
    assert len(run_ids) == 1, (f, run_ids)          # journals here are single-run
    run = run_ids.pop()
    calls = [e for e in events if e["event"] == "tool_call"]
    per_run[run] = {"file": os.path.relpath(f, REPO), "n_calls": len(calls)}
    for i, e in enumerate(calls, 1):
        if e["refused_by"] is None and e["reason"] is None:   # _shared.event_ok
            continue
        rows.append({"run": run, "call_index": i, "tool": e["tool"], "refused_by": e["refused_by"],
                     "result_summary": e["result_summary"], "reason": e["reason"], "args": e["args"]})
print(json.dumps({"per_run": per_run, "failures": rows}, indent=1, sort_keys=True))
```

**2 — repair-loop metrics** (§6 table): iterate the same files, compute
`ok = refused_by is None and reason is None` per call, then maximal streaks of `not ok`
and, for each failing call, the distance to the next successful call of the same tool.

**3 — replay every failing call's verbatim args against HEAD**: `load_tools()`, build a
`ToolEnv(run_id=..., journal_path=<tmp>, ctx=Ctx(), cwd=<tmp git repo>, tools=tools)` and
call `tools[t].fn(env, args)` directly (bypassing `loop.step`, so no invariant pre-empts
the tool's own validator). Strip the journal-added `refs-paths` key from `guard` args.
Result classes: 19 `invalid-args`, 23 `declined-other`, 5 `accepted`, 6 `unknown-tool`.
The 5 `accepted` are the H7 collateral of §5.2. **State-dependent rows are not evidence
about HEAD** — a fresh empty run is not the state they were rejected in.

**4 — adversarial cases** (§5.1): the 7 `record_check`/`record_claim` calls listed, each
carrying exactly one defect, run through `tools[t].fn` as in script 3.

**5 — `ctx.actor` derivability** (§5.3): walk each journal's calls; accumulate action names
from executed `gate` (`args.task.actors` keys) and `guard` (`args.action.name`); at each
`has no entry for action` failure, report whether the wanted name is in the accumulated set.

**6 — historical trees**: `git archive 839c3be | tar -x -C /tmp/v11` and
`git archive bc52866 | tar -x -C /tmp/v13`, then `sys.path.insert(0, ...)` and
`load_tools()` (no argument — passing the extracted tools dir as well raises
`ManifestError: duplicate tool name`).

**7 — classification and cross-tab**: the per-call category/mechanism map is
`docs/research/interface_census_rows.json`, keyed `"<run>#<call_index>"` with
`[tool, category, field, mechanism, correct_by_design, note]`; §2/§3's tables are counts
over it.

**8 — CLI exit codes** (§5.1):
```bash
T=$(mktemp -d); mkdir -p $T/repo; (cd $T/repo && git init -q && git commit -q --allow-empty -m i)
python3 -m ancient_games.hybrid init --run-id adv --journal $T/j.jsonl --cwd $T/repo --ceiling 20
export ANCIENT_GAMES_RUN=$T/j.jsonl.run.json
python3 -m ancient_games.hybrid call record_check '{"claim_id":"C2","falsifies":"C2","mechanism":"grep over the written file","command":"grep","expected":"1","observed":"1"}'; echo "exit=$?"
python3 -m ancient_games.hybrid call record_claim '{"claim_id":"C3","author":"MAIN","actor":"MAIN","kind":"executable","text":"t","evidence_type":"suite","evidence_ref":"x"}'; echo "exit=$?"
```

## 10. Prior results this supersedes or corrects

* `docs/ABLATION_2.md` H12 records the two `framings` failures; this document adds that
  the same defect occurred once earlier (attempt2/UC1 #21) where it was **masked** by the
  H7 poisoning and therefore never counted — 3 occurrences, not 2.
* `docs/ABLATION_2.md` reports attempt3/UC2J as "6 refused/declined calls before the
  accepted shapes" motivating H13. The journal has **5** non-successful calls in that
  run, and **3 of the 5 were the C·4 split-path `ctx.actor` bug** (§5.3), not shape
  discovery. H13's conclusion (derive the ceiling from free-agent traces) is unaffected;
  its stated cause is partly wrong.
* Nothing here contradicts `docs/ABLATION_1.md` or `docs/ABLATION_3.md`. It adds the
  root cause of ABLATION_1's H2/H7 `internal-error: True/False` cluster (one poisoned ctx
  field, not one bug per tool) and shows H2's fix is **incomplete**: `record_check` was
  never given the validator the other adapters got.
