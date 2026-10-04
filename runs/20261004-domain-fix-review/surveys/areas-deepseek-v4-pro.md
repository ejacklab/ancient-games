# Area survey — deepseek-v4-pro

Verdicts key: DIRECT (editable now, check named) · SCHEMA (design format needs a field) · DECISION (EJ only) · DOC (prose disagrees) · LATER (not now / not verifiable).

## Area 1. The gate cannot reject

| issue | verdict | what would fix it, or what blocks it |
|---|---|---|
| 1.1 | SCHEMA | The design JSON's `five_things` entries are bare names with nothing behind them, so G3 cannot check contents — the format needs a per-item content/value field. |
| 1.2 | SCHEMA | A building design has no `baseline` field for the gate to require, so method 3.6's baseline is unenforceable — add a `baseline` field carrying the pre-build test command and its output. |
| 1.3 | SCHEMA | A building node has no `stop` field, so the three-part stop cannot be checked — add a `stop` field (limit, exit, evidence) to the node schema. |
| 1.4 | DIRECT | Edit `design_gate.py` to add a G-rule that consumes the parsed `pattern` cell; the check is a new mutation in `tests/workflows/mutation_matrix.py` that perturbs `pattern` and asserts the gate flags it. |
| 1.5 | LATER | The contradiction now fires, but the remaining self-reference needs an independent record of what a run actually built and touched, which no artefact captures yet — not verifiable now. |
| 1.6 | DIRECT | Edit `design_gate.py` so loop-bound checks fire on a loop-capable node even when no `loop` object is present; the check is a mutation that strips the `loop` field and asserts G3 rejects. |
| 1.7 | LATER | Already fixed — G3 rejects a check that names the table and the mutation matrix has a mutation for it; nothing further to do. |

## Area 2. The test could not fail

| issue | verdict | what would fix it, or what blocks it |
|---|---|---|
| 2.1 | DIRECT | Edit `tests/workflows/corpus_check.py` to admit independent hand-authored or mutated designs instead of only building them from the TASK_TYPES cells the gate parses; the check is a seeded-bad design producing a GATE finding. |
| 2.2 | DIRECT | Edit `tests/workflows/corpus_check.py` to emit a share of challenger `design_source` designs; the check is the corpus report showing G5/G7 findings rather than zero coverage. |
| 2.3 | LATER | Already addressed — `tests/workflows/mutation_matrix.py` exists (18/18) and `--self-check` proves it can report a MISSED; nothing further now. |
| 2.4 | LATER | The checklist layer is prose in `docs/TASK_TYPES.md` with no runnable script, so running it is a manual pass not verifiable by a named check — defer until it is automated. |
| 2.5 | LATER | Already fixed — the corpus README names the denominators, a documentation correction; nothing more to do. |
| 2.6 | DIRECT | Edit `tests/workflows/corpus_check.py` to emit the row's `pattern` beside `sabotage`; the check is the emitted design carrying `pattern` and, after 1.4, the mutation matrix exercising it. |

## Area 3. Step 1 — the readiness script

| issue | verdict | what would fix it, or what blocks it |
|---|---|---|
| 3.1 | DIRECT | Edit `readiness.py` so `check_blueprint` fails when its own detail says map MISSING or 0 sections, and make `--self-test` call it; the check is `--self-test` asserting a map-MISSING directory is not VERIFIED. |
| 3.2 | DIRECT | Edit `readiness.py` to default `absent_status` to a non-verified status; the check is a run in an empty directory (or a pytest) asserting `verified` is no longer reported for absent or empty. |
| 3.3 | DIRECT | Edit `readiness.py` so the section count reads the blueprint's own sections, not every `.md` in the directory; the check is a directory with extra `.md` files reporting the blueprint's count. |
| 3.4 | DIRECT | Edit `readiness.py` `exit_code` so a `--require` tool that is UNKNOWN (timeout or non-zero exit) fails like MISSING; the check is `--require` on a tool that times out exiting 1. |
| 3.5 | DIRECT | Edit `readiness.py` to guard the model-list parse and only count rc==0 with a parseable list; the check is a pytest feeding a non-object `model` and asserting no uncaught AttributeError. |

## Area 4. The three renderings disagree

| issue | verdict | what would fix it, or what blocks it |
|---|---|---|
| 4.1 | DOC | `SKILL.md` carries the engine split while `docs/WORKFLOW_DESIGN_METHOD.md` and `docs/WORKFLOW_DESIGN_DIAGRAM.md` mention it nowhere — reconcile the three files. |
| 4.2 | DOC | `SKILL.md` says three qualities but lists four, and `docs/WORKFLOW_DESIGN_METHOD.md` §5 is still titled "Three qualities" — align the count and the title. |
| 4.3 | DOC | The 3.8 mapping row in `docs/WORKFLOW_DESIGN_DIAGRAM.md` says "no step" while `SKILL.md` carries 3.8 inside steps 1 and 7 — correct the row to match the skill. |
| 4.4 | DOC | In `docs/EXECUTOR_KINDS.md` the role map routes `classification` to agy/gemini while the routing row in the same file says deepseek-flash — make the file agree with itself. |
| 4.5 | DIRECT | Edit `.claude/workflows/intake.js` (or `design_gate.py`) to join the emitted `pieces` to the consumed `nodes`; the check is a test that runs an intake design through the gate and asserts the node list connects. |
| 4.6 | DOC | `docs/WORKFLOW_DESIGN_METHOD.md` 3.1 never received the two rules added to skill step 1 in `SKILL.md` — port them over. |
| 4.7 | DOC | `docs/TASK_TYPES_LEDGER.md` header says "Coverage outcome" while `design_gate.py` expects `coverage_result` — align the names (the positional read is why the check still passes). |
| 4.8 | DOC | The use-case table in `docs/TASK_TYPES.md` teaches adding `information extraction` to a pass-through prompt, which rule 2 in the same file forbids — correct the example to the rule. |

## Area 5. Composition — work with no owner

| issue | verdict | what would fix it, or what blocks it |
|---|---|---|
| 5.1 | DECISION | EJ must choose which step records the baseline before the first building node, and what happens when it is already red. |
| 5.2 | DECISION | EJ must assign an owner step for the final "what is missing" pass that §5 and 3.6 both demand but no step places in the graph. |
| 5.3 | DECISION | EJ must reorder so step 5's loops run only after steps 6-7 define nodes, edges and the 5-role/3-at-once caps, or bound step 5's concurrency. |
| 5.4 | DECISION | EJ must define what a non-product-change run ends at, since its promise to end at acceptance criteria cannot hold for that class. |
| 5.5 | DECISION | EJ must decide whether the tiny-task exit may skip readiness, or must run a reduced blueprint-and-baseline check. |
| 5.6 | DECISION | EJ must name an engine for the `others` bucket (or reject unmatched pieces) so 3.2's routing and 3.6's engine requirement agree. |
| 5.7 | DOC | The 5-role/3-at-once caps and item 12's "no finding id" gate live only in `docs/WORKFLOW_DESIGN_METHOD.md` — port them to `SKILL.md` and `docs/WORKFLOW_DESIGN_DIAGRAM.md`, or mark them method-only. |

## Area 6. Decisions the algorithm never makes

| issue | verdict | what would fix it, or what blocks it |
|---|---|---|
| 6.1 | DECISION | EJ must set the fallback engine, stronger-tier model and attempt-limit value that the tier exit and executor-failure rerun depend on. |
| 6.2 | DECISION | EJ must set a run-wide replan limit so exhausted nodes returned to planning cannot renew their budgets indefinitely. |
| 6.3 | DECISION | EJ must move the challenger decision to after 3.5/3.6 produce the loops and caps, or define what the pre-estimate may legitimately project. |
| 6.4 | DECISION | EJ must reorder so node membership (3.2) follows 3.3, 3.4 and 3.6 instead of preceding them. |
| 6.5 | DECISION | EJ must fix the 3.3 branch on prompt-file vs design to follow 3.4's decision, and align `docs/WORKFLOW_DESIGN_DIAGRAM.md` with the reorder. |

## Area 7. The runnable form, `intake.js`

| issue | verdict | what would fix it, or what blocks it |
|---|---|---|
| 7.1 | DIRECT | Edit `.claude/workflows/intake.js` to run the method 3.0 text-understanding and restatement step before dispatching readiness; the check is a run whose state file shows the restatement written first. |
| 7.2 | DIRECT | Edit `.claude/workflows/intake.js` to record the test command and its output as the baseline, not only a git status snapshot; the check is a run whose baseline carries both. |
| 7.3 | DIRECT | Edit `.claude/workflows/intake.js` to accept 3.5 item 4's first exit (a fresh node on a stronger tier) without requiring "unclear" or "EJ"; the check is such an exit string being accepted. |
| 7.4 | DIRECT | Edit `.claude/workflows/intake.js` to emit the row's real check instead of a table pointer; the check is the gate no longer rejecting the emitted check as naming the table. |

## Area 8. My own construction, observed failing

| issue | verdict | what would fix it, or what blocks it |
|---|---|---|
| 8.1 | DIRECT | Edit `design_gate.py` G6 to compare the reviewer against every engine that touched the artifact, not the cell's leading token; the check is a mutation where the reviewer's engine overlaps a builder's and the gate rejects. |
| 8.2 | DIRECT | Edit `engines.py` `DEFAULT_FALLBACKS` (or add a re-appointment rule) so a codex fallback cannot leave a same-kind verifier; the check is a pytest asserting the verifier is a different kind after the fallback. |
| 8.3 | SCHEMA | `five_things` is the bare template list with nothing behind the names — the format needs a per-item content field so values can be checked. |

## What I would fix first

1. **Close the gate's last dead rule (1.4 and 1.6).** The gate is the algorithm's only mechanical enforcement, and `pattern` is still parsed-and-unused while loop checks fire only when a loop already exists. Check: `python3 tests/workflows/mutation_matrix.py` gains a `pattern` mutation and a "loop-capable node with no loop field" mutation, both reported CAUGHT and the script exiting 0.
2. **Un-circularise the test (2.2 and 2.6).** Make `tests/workflows/corpus_check.py` emit challenger `design_source` designs and the row's `pattern`, so G5/G7 and the pattern rule actually execute. Check: `python3 tests/workflows/corpus_check.py --emit-designs DIR` writes designs carrying a challenger source and a `pattern` field, and the report shows non-zero G5/G7 coverage.
3. **Add the `baseline` field (1.2), which 5.1 depends on.** The register calls the ownerless baseline the most serious single defect, and it is blocked on the schema, so EJ must settle the field first. Check: once the field exists, the mutation matrix's `m_no_baseline` entry flips from HOLE to CAUGHT.

## Where 孫子兵法 does not help

- **1.2 — the missing `baseline` field.** The text does say to write the pre-commit assessment before committing (CANONICAL #1, 廟算, VERIFIED), but it says nothing about *which JSON field* carries it or its type; CANONICAL.md's own "What this domain cannot supply" #3 concedes the text "gives no … schema." A field name is a spec decision, not a strategy one.
- **4.7 — the ledger header vs `coverage_result`.** A header saying "Coverage outcome" against a gate field named `coverage_result` is pure naming drift; no principle from 孫子兵法 bears on whether two tokens match, and manufacturing one would be false (not from a note).
- **3.4 — `--require` passing a tool that is UNKNOWN rather than MISSING.** 知彼知己 (CANONICAL #3, VERIFIED) supports "measure your own tools," but it has nothing to say about how a script maps a timeout or a non-zero exit to a status token; that is a vocabulary bug in `readiness.py`, not a question of strategy (not from a note).
