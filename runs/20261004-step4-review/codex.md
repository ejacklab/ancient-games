## 0. RESTATEMENT

Count the task’s checkable actions and preserve its deliverables. At most three steps, with only decisions carrying provisional assumptions, qualify for a prompt file; information gaps, unknowns, and missing or incomplete required blueprint sections require a workflow design. Judge risk separately: a small risky task receives an independent check. Above three steps, consider splitting only where both parts retain checks and the split changes execution. Workflow designs start from category defaults; challengers require a substantiated 20% cost reduction at equal coverage, script and blind checklist review, and subsequent reconciliation.

The intended decision is **prompt file versus workflow design, plus the pieces retained or split**. The text does not completely determine that decision above three steps.

## 1. VERDICT

UNSOUND

The challenger gate can accept a proposal with higher monetary cost and reduced blindness because it compares raw token estimates and criterion/check identifiers rather than the complete promised cost and coverage contract.

## 2. FINDINGS

Paths below are relative to `/home/smoke01/dev/ancient-games`; `design_gate.py` means `.claude/skills/workflow-design/scripts/design_gate.py`.

| id | severity | what step 4 says (quote) | evidence (file:line, quoted line, or the counterexample) | why it fails | concrete fix (the smallest edit that removes the problem) |
|---|---|---|---|---|---|
| F1 | BLOCKER | “≥20% lower projected run cost” | `design_gate.py:175–178` reads only `estimate.tokens` and `default_estimate.tokens`. An in-memory probe with 75,000 versus 100,000 tokens, but monetary estimates of 3 versus 1, returned no findings. `docs/TASK_TYPES.md:32` permits “tokens / agents / wall time.” | The rule supplies interchangeable measures without selecting one; the script silently selects tokens. Fewer tokens across different models, prices or cache mixes need not mean a cheaper run. Agent count and elapsed time are also different quantities. | Require one declared comparison metric and unit, a common accounting basis, and a cost breakdown covering models, cache, checks, joins and expected retries. Make G5 validate that declared measure. |
| F2 | BLOCKER | “at equal coverage (same criteria ids, same checks, same blindness)” | `docs/WORKFLOW_DESIGN_METHOD.md:235`; `design_gate.py:185–188` compares only sets of `criteria` and `checks`. A probe changing coverage blindness from “worker reasoning withheld” to “worker reasoning visible” returned no findings. The fixed checklist at `docs/TASK_TYPES.md:41–43` contains no explicit blindness comparison. | One of the three mandatory equality conditions is absent from both the mechanical comparison and the explicit judgment checklist. Matching labels does not establish equal reviewer access restrictions. | Add a required blindness/access contract to both coverage records, compare it in G5, and make the checklist verify its enforcement. |
| F3 | BLOCKER | “A workflow design starts default-first” | Method `:231–238`; diagram `docs/WORKFLOW_DESIGN_DIAGRAM.md:41` says `SPLIT --> S5`, while `:42–43` routes only `DESIGN --> DF --> S5`. | A fully clear task above three steps follows the diagram straight into execution loops without the default lookup or challenger decision review. | Replace `SPLIT --> S5` with `SPLIT --> DESIGN`, covering both split and unsplit outcomes. |
| F4 | MAJOR | “More than 3 steps → consider a new piece” | `docs/WORKFLOW_DESIGN_METHOD.md:226–227`; `:170` defines a step as “one action with a result that can be checked.” Neither states the output when splitting is rejected. | Four clear actions in one deliverable leave competent readers choosing between an unsplit prompt file and a one-piece workflow. Action granularity can also change the count without changing the task. | State: “More than three task actions → workflow design, even if retained as one piece.” Add a counting convention excluding checks and administrative handovers and forbidding bundling independently checkable transformations merely to meet the threshold. |
| F5 | MAJOR | “Up to 3 steps … → one piece → a prompt file” | Method `:221`; §3.2 at `:178–180` defines pieces as steps ending in one deliverable. `docs/TASK_TYPES.md:113–117` requires “One label per distinct deliverable.” | Three clear actions can produce three separately requested deliverables with different engines or mandatory review boundaries. Step 4 collapses distinctions already required by step 2. | Replace “→ one piece” with “preserve the labelled pieces; use one prompt only if they can share a session without losing required checks or routing.” |
| F6 | MAJOR | Method: “decisions that have a provisional assumption”; skill: “decisions that have a default” | Method `:221` versus skill `:93`; method `:236–237` requires a different kind when the design “builds **or EJ flagged high risk**,” while skill `:98` and diagram `:42` retain only “when it builds.” | An explicit provisional choice need not be an established default. More decisively, the packaged rule drops the independent engine requirement for high-risk read-only designs. | Use “provisional assumption” in all copies and restore “or EJ flagged high risk” in the skill and diagram. |
| F7 | MAJOR | “Anchors for the number 3”; diagram: “anchored in code, not chosen” | Method `:240–241`; diagram `:168`. `ancient_games/stages.py:109` tests `count > 3`, where `:74` returns the capability count. `registry.py:24` is `CAP = 3`; `stages.py:309` describes corroborating dispatch capacity. | These support capability splitting and dispatch limits. Neither establishes that three sequential task actions distinguish prompt files from workflows. The inference changes the quantity being measured. | Describe three as a provisional sizing heuristic inspired by unrelated framework limits, with no validation from those limits. |
| F8 | MAJOR | “every run reconciles its claim … that ledger is how the defaults earn their n” | `docs/TASK_TYPES_LEDGER.md:9,14–20` contains eight run rows. Its intervening comment at `:11–13` ends the table recognized by `design_gate.py:75–76`: “if not s.startswith('\|'): break”. The actual parser returned **one** row. | G7 misses seven current records, so passing ledger validation does not mean every recorded run was checked. | Make ledger parsing continue across the intervening comment, or keep all run rows in one uninterrupted table. |
| F9 | MAJOR | “every run reconciles its claim” | Ledger `:14–20`: seven rows say “no — token cost not measured.” The sole “yes” row at `:9` includes “agy 3 calls not measurable.” G7 at `design_gate.py:248–249` requires only nonempty actual-cost text; a reconciled row containing “not instrumented” passed an in-memory probe. | Reconciliation currently means neither complete measurement nor a projection-to-actual comparison. Consequently the ledger cannot reliably validate cost claims or establish measured defaults. | Require measured actual values in the declared projection metric and a recorded comparison; mark incomplete measurements partial rather than reconciled. |
| F10 | MINOR | “Added 2026-10-01 … n=0”; “in the ledger (n=0)” | Method `:238`, skill `:99`, diagram `:42` says “n=0 until it fills.” The ledger now contains eight default runs, one marked reconciled, and no challengers. | The unqualified zero conflates no challenger validation with no default executions. The diagram’s “until it fills” condition has already occurred. | State separate dated counts: eight recorded default runs, one nominal reconciliation with incomplete engine measurement, zero challenger runs, and zero fully measured comparable cost validations. |

## 3. CHECKLIST

| check | result | note |
|---|---|---|
| C1 — Terms defined or referenced | WEAK | “Step” and “piece” are defined at method `:170,178–180`; the prompt template is referenced at `:25`, assumptions at `:212–216`, and coverage at `:235`. Cost lacks a selected metric/accounting basis; “default” drifts from assumption, and risk tiers lack an explicit classification scale. |
| C2 — Decidable three-step threshold | FAIL | The greater-than-three, no-useful-split case has no explicit document route; “one action” also permits different defensible decompositions. See F4. |
| C3 — Three code anchors | WEAK | `stages.py:109`: **`if count > 3:`**, supported by `:74`: **`return len(list(capability))`**—supports capability splitting. `registry.py:24`: **`CAP = 3`**—supports the constant. `stages.py:309`: **“a slot remains iff dispatch_count < 3”**—with `:312–316`, supports dispatch capacity. All three support their narrow code descriptions, but none validates a three-action sizing threshold. |
| C4 — Risk independent of size and hand-off cost | PASS | Method `:229` explicitly adds the check to the prompt file. An independent reviewer satisfies §3.2’s different-kind/blind-reviewer justification at `:194–195`; it need not increase the task-action count. |
| C5 — Default lookup possible | PASS | `docs/TASK_TYPES.md:86–103` has all four named columns: 15 ordinary category rows have populated cells; the sixteenth, `others`, explicitly has no default and invokes first principles. Pipeline tables supply wiring and must be combined with category rows for engines and sabotage. |
| C6 — Cost rule well-formed | FAIL | The design supplies its own estimates and baseline; G5 checks token arithmetic, not a common measured cost basis. No particular estimator is assigned. Method §5 imposes predictability/debuggability requirements, but no relative non-regression condition; faster parallel execution can therefore qualify while worsening those qualities. |
| C7 — Reviewer routing and blindness | WEAK | Method `:236–237` agrees with `TASK_TYPES.md:40–48` on a fresh blind design reviewer and the high-risk exception. Executor rule 5 at `:432–434` prefers different kinds, and `:266–269` requires structural blindness. The skill omits high risk; G6 checks in-run build reviewers, not the separate design-decision reviewer. |
| C8 — Ledger earns defaults their n today | FAIL | Counted **eight physical run rows: eight defaults, zero challengers; one “yes,” seven “no — token cost not measured.”** The “yes” includes unmeasured agy calls. The gate parses only one row. Execution experience exists; complete comparable cost evidence does not. |
| C9 — Method and packaged step agree | FAIL | Method `:221`: **“provisional assumption”** versus skill `:93`: **“default”**; method `:237`: **“builds or EJ flagged high risk”** versus skill `:98`: **“when it builds.”** Information/unknown and blueprint routing are recovered elsewhere in the skill (`:87–92`); their omission from step 4 alone is not an additional routing defect. |
| C10 — Empirical marks and dates | WEAK | The September 20 revision and n=1 account already appear in commit `ecdc26e` dated September 20; the October 3 correction matches code and commit `9795522`. Current n=0 wording needs qualification. The default-first addition was committed October 2 (`bf6a6f8`); that neither proves nor disproves an October 1 agreement or uncommitted addition. |

## 4. STRONGEST COUNTEREXAMPLE

A team proposes replacing a cheap-model workflow for a settled parser fix with a stronger-model workflow. Both preserve the same acceptance criteria, baseline test suite, independent reviewer and access restrictions.

The projection gives:

| | Default | Challenger |
|---|---:|---:|
| Total tokens | 100,000 | 75,000 |
| Effective monetary cost per million tokens | 10 units | 40 units |
| Projected monetary cost | 1 unit | 3 units |

These are illustrative declared rates, not claims about current vendor pricing.

The challenger claims a **25% reduction** and supplies a genuine token-based explanation: the stronger model needs fewer attempts. G5 accepts the arithmetic. The fixed checklist can accept the category, instance-specific reason, real token basis and completeness without requiring monetary comparison (`TASK_TYPES.md:41–43`).

**Route permitted:** approve the challenger as cheaper.

**Route required for a monetary run budget:** retain the default, because the challenger costs three times as much. If token consumption is deliberately the objective, that must be declared before comparison; the current rule and gate do not distinguish these decisions.

Separately, the executed in-memory probe also accepted differing blindness declarations. That demonstrates missing enforcement, rather than relying solely on an estimation dispute.

## 5. WHAT I COULD NOT VERIFY

- Whether October 1 was the actual agreement or drafting date for default-first design; git establishes its October 2 commit date.
- Whether trial 1’s three decision spots caused the reported sizing failure, or whether the revised threshold subsequently improved routing. Historical wording supports the account’s existence, not its causal validity.
- Actual comparable costs, retry distributions or savings for the ledger runs. Seven explicitly lack token measurement; the eighth lacks measurements for one engine.
- Whether recorded blind reviews used enforceable access restrictions. Routing documents prescribe them, but step 4 and G5 do not establish their execution.
- Any evidence that three task actions is an effective boundary. The cited code measures capabilities and dispatches.
- No listed source was inaccessible. Review remained read-only; probes ran in memory without writing files.

## 6. WHAT THIS CHECKLIST MISSED

- **Diagram bypass of default-first review:** F3 is a control-flow defect; checking node wording or method-to-skill parity does not expose the missing edge.
- **Deliverables versus task size:** F5 shows that a task can be short while requiring several labelled pieces. C2 addresses counting, but does not explicitly test preservation of step 2’s deliverable and engine boundaries.
- **Ledger validation coverage:** C8 asks what the ledger contains, but does not ask whether the validator actually reads every row. The intervening comment makes seven records invisible to G7.