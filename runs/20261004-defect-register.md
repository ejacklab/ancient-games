# Defect register — 2026-10-04

Every issue found by the day's four blind reviews, merged and numbered.

**119 located findings → 44 distinct issues.** The gap is duplicate discovery: the same defect was often found by
several engines, and the later reviews re-found defects the earlier ones had reported from a different direction.
That repetition is evidence, not noise — but it is not 119 problems.

## How this was produced, and how far to trust it

| review | scope | engines | located | discarded |
|---|---|---|---|---|
| `runs/20261004-step1-review` | step 1 (Readiness): skill step 1, method 3.1, readiness.py, the blueprint diagram, the template | 4 (agy produced 0) | 24 | 0 |
| `runs/20261004-algorithm-review` pass 1 | the algorithm as prose: method, skill, diagram | 4 | 35 | 0 |
| `runs/20261004-algorithm-review` pass 2 | the FULL algorithm: 14 artefacts, 3,202 lines, incl. tables, templates, gate, intake.js | 4 | 24 | 1 |
| `runs/20261004-corpus-fulltest` | the 300-prompt corpus **test log** — behaviour, not prose | 4 | 36 | 1 |

16 engine-calls, 4 engines. Every finding had to carry `file:line` and a **verbatim quote**, and every quote was
checked against the real file; 2 of 121 could not be checked and were discarded. So the findings are quoted
accurately — which is not the same as being *right*, so each issue I could check myself is marked **✓** below (I
re-read the code, or ran it). Issues without **✓** are engine claims I have not independently confirmed.

## 1. The gate cannot reject — 7 issues

| # | issue | where | found by | ✓ |
|---|---|---|---|---|
| 1.1 | **FIXED 2026-10-05 — G3 requires the five things' contents (`check_five`).** G3 checks that five field **names** appear, not their contents | `design_gate.py:146` | claude, codex (p2); claude, opencode (log) | ✓ |
| 1.2 | **FIXED 2026-10-05 — G10 requires `baseline.command` and an owner.** No rule for a **baseline**, though every building node's stop requires one | `design_gate.py:150` | claude, opencode | ✓ |
| 1.3 | **FIXED 2026-10-05 — the stop carries method 3.6's three parts in both formats.** No rule for the **three-part stop** itself | `design_gate.py:150` | claude, opencode | ✓ |
| 1.4 | `pattern` and `sabotage` are parsed from every category row and **used 0 times** | `design_gate.py:93` | claude, opencode | ✓ |
| 1.5 | G2 takes `builds` and `touched_paths` **from the design itself** — self-referential | `design_gate.py:130` | claude | |
| 1.6 | Loop rules run only if a loop already exists | `design_gate.py:150` | opencode | |
| 1.7 | The check string only has to be non-empty, not executable | `design_gate.py:144` | agy | |

**This is the family that matters most.** The gate is the algorithm's only mechanical enforcement, and it passes
300 designs built from its own table while having no rule for the baseline or the stop condition the algorithm
promises on every building node.

## 2. The test could not fail — 6 issues

| # | issue | where | found by | ✓ |
|---|---|---|---|---|
| 2.1 | **Circular**: designs are emitted from the same TASK_TYPES cells the gate parses, so agreement is by construction | `testlog.md:6,9` | claude, opencode | ✓ |
| 2.2 | All 300 designs are `design_source: "default"`, so G5 (the 20% challenger rule) and G7 (ledger) never execute | `testlog.md:83` | agy, claude, codex | ✓ |
| 2.3 | No mutation/negative controls: the test has never rejected anything, so it is not known to be able to | `testlog.md:18` | all 4 | ✓ |
| 2.4 | The checklist review layer — the semantic layer the file says catches what the script cannot — never ran | `TASK_TYPES.md:284` | claude, opencode | |
| 2.5 | The reported accuracies had no denominator: codex's 90% is r2+r3, dropping r1 where it mismatched 25 of 25 | `testlog.md:34` | opencode | ✓ |
| 2.6 | Sabotage and the pattern column are never exercised by the corpus run | `design_gate.py:93` | claude, opencode | ✓ |

## 3. Step 1 — the readiness script — 5 issues

| # | issue | where | found by | ✓ |
|---|---|---|---|---|
| 3.1 | **The blueprint check can never fail**: an existing directory is always `VERIFIED`, even when its own detail says `map MISSING` or `0 sections`; `--self-test` never calls it | `readiness.py:197-205` | opencode | ✓ |
| 3.2 | Absent and empty directories report **`verified`** (`absent_status` defaults to it) — reproduced in an empty dir: rc=0, "verified \| absent" | `readiness.py:184` | opencode | ✓ |
| 3.3 | "N sections" counts every `.md` in the directory, not the blueprint's sections | `readiness.py:204` | opencode, claude | ✓ |
| 3.4 | `--require` passes a tool that is `UNKNOWN` (timeout, non-zero exit) rather than `MISSING` | `readiness.py:326` | codex | |
| 3.5 | Any `rc == 0` with output counts as a verified model list; a non-object `model` raises an uncaught `AttributeError` | `readiness.py:139,163` | codex | |

3.1, 3.2 and 3.3 are one root cause seen three times: **a status vocabulary that cannot express "absent" or
"unknown"**, in the step whose entire job is separating verified from unknown.

## 4. The three renderings disagree — 8 issues

| # | issue | where | found by | ✓ |
|---|---|---|---|---|
| 4.1 | The **engine split exists only in the skill** — method and diagram have zero mentions of it | `SKILL.md:175` vs both | all 4 (pass 1) | ✓ |
| 4.2 | The checklist says **three** qualities and lists **four**, and method §5 is still titled "Three qualities" | `SKILL.md:165`, `METHOD.md:476` | all 4 | ✓ |
| 4.3 | **FIXED 2026-10-05** — the row now names step 1 (tools, timers, no polling) and step 7 (the evidence a node's claims are judged by, `read` vs `ran`), instead of "no step" **The 3.8 mapping row is wrong in both directions** — the skill carries 3.8 inside steps 1 *and* 7. I added that row today | `DIAGRAM.md:213` | all 4 (pass 2) | ✓ |
| 4.4 | **FIXED 2026-10-05 — the Classifier row said `agy`; EJ's instruction and the routing table both say DeepSeek.** `classification` is still routed to **`agy`/gemini-3.1-pro-high** in the role map, while the routing row in the same file says `deepseek-flash` | `EXECUTOR_KINDS.md:63` | codex, claude | ✓ |
| 4.5 | **FIXED 2026-10-05 — one shape: the gate reads the fields `intake.js` emits.** `intake.js` emits **`pieces`**; `design_gate.py` consumes **`nodes`** — nothing joins them | `intake.js:178,238` | claude, codex, agy | ✓ |
| 4.6 | Method 3.1 never received either of the two rules added to skill step 1 | `METHOD.md:79` | claude | ✓ |
| 4.7 | The ledger header says "Coverage outcome"; the gate's field list says `coverage_result` (doc drift — the ledger check still passes, so the gate is positional) | `TASK_TYPES_LEDGER.md:7` | agy | ✓ |
| 4.8 | **FIXED 2026-10-05 — use case 2 taught `repo scanning, information extraction`, a pairing that occurs in 0 of 300 labels.** The TASK_TYPES use-case table **teaches the pairing the expected labels penalise**: it instructs adding `information extraction` to "answer a question about existing code" prompts, which rule 2 forbids as a pass-through | `TASK_TYPES.md:63` | agy, claude, opencode | ✓ |

4.8 is the one that changes a *score* into an *algorithm defect*: the models were penalised for following the table.

## 5. Composition — work with no owner — 7 issues

| # | issue | where | found by | ✓ |
|---|---|---|---|---|
| 5.1 | **The baseline has no owner.** 3.6 requires one recorded before the first node that builds; no step produces it, and nothing says what happens if it is already red | `METHOD.md:295-296` | agy, claude, opencode | ✓ |
| 5.2 | The final **"what is missing" pass has no owner** — §5 and 3.6 both demand it, no step places it in the graph | `METHOD.md:306` | claude, opencode | |
| 5.3 | **Step 5 runs loops before steps 6-7 define** the nodes, edges and the 5-role/3-at-once caps, so the concurrency is unbounded when it starts | `METHOD.md:245`, `SKILL.md:102` | codex, opencode, agy | ✓ |
| 5.4 | The promise that a run **ends at the acceptance criteria** is broken for the whole non-product-change class | `METHOD.md:131` | agy, opencode | ✓ |
| 5.5 | **The tiny-task exit skips readiness**, so a small product change builds with no blueprint criteria and no baseline | `METHOD.md:24-25`, `DIAGRAM.md:19` | codex, claude | ✓ |
| 5.6 | **FIXED 2026-10-05 — and it was a bug, not a decision.** The code half was false (no step requires a node to name an engine; method 3.7 says each node names its own). What was real: `TASK_TYPES.md:103` gives `others` an engine cell of `—`, the harness passed that placeholder straight through, and **the gate accepted a design whose engine was an em dash** (`engine_kind` returned `unknown` and nothing objected). New rule **G11** rejects it; the harness resolves `others` to a documented engine. Pinned by a mutation. **`others` has no engine**, yet 3.2 sends every unmatched piece there and 3.6 requires every node to name one | `EXECUTOR_KINDS.md:164` | agy, claude | ✓ |
| 5.7 | ~~The 5-role/3-at-once caps and item 12's gate exist only in the method~~ **CORRECTED 2026-10-05:** `dispatch.py:41,63-64,108-109` enforces both caps on a *dispatch plan*, so the caps are not method-only. What is missing is a cap rule in `design_gate.py`, which validates a design and sees no caps at all. Item 12's gate is still method-only | `METHOD.md:333,426` | claude, opencode | |

## 6. Decisions the algorithm never makes — 5 issues

| # | issue | where | found by | ✓ |
|---|---|---|---|---|
| 6.1 | **ANSWERED BY THE CODE — `engines.py:157` DEFAULT_FALLBACKS and `intake.js` `attempt_limit` both exist; pinned by test_dispatch.py:129.** A node's fallback engine, stronger-tier model and attempt-limit value are undecided, though the tier exit and the executor-failure rerun both depend on them | `METHOD.md:382` | claude | |
| 6.2 | **ANSWERED BY THE CODE — `dispatch.py:41` max_rounds=2, enforced at `:292`, pinned by test_dispatch.py:145.** No run-wide replan limit, so returning exhausted nodes to planning can renew their budgets indefinitely | `METHOD.md:314` | codex | |
| 6.3 | **WITHDRAWN 2026-10-05.** METHOD.md:245 says every run *reconciles its claim in `docs/TASK_TYPES_LEDGER.md`* — the 20% is a provisional number with a named mechanism for correcting it, and the row is n=0 until the ledger fills. Making a projected claim before the structure exists is what a projection is. The challenger decision is taken during sizing, before 3.5/3.6 produce the loops and caps whose cost it projects — and the gate then re-checks the estimate | `METHOD.md:234` | opencode | |
| 6.4 | **DOWNGRADED 2026-10-05.** 3.3 records, per spot, *which steps cannot start until it is resolved* — so only the blocked pieces wait and the rest are decided at once. Not circular. What remains is small and real: 3.2 forward-references 3.4 (*"Same warning as 3.4: fixed cost per agent…"*, METHOD.md:198) and its merge test uses *"its context would not fit"*, a size 3.4 produces. 3.2 assigns node membership *before* 3.3 lists the spots, 3.4 sizes, and 3.6 builds the graph | `METHOD.md:178,200` | agy, claude | |
| 6.5 | **WITHDRAWN 2026-10-05 — false positive.** 3.3 does not branch on prompt-file vs design; it states both cases conditionally (*"In a prompt file a provisional assumption stands…; a workflow design's questions are answered before the run…"*). The applicable sentence can be read after 3.4 decides. Nothing is used before it exists. 3.3 branches on prompt-file vs design before 3.4 decides which; the diagram resolves spots before Size though 3.4 sizes on spot *kinds* | `METHOD.md:213`, `DIAGRAM.md:37` | agy, claude | |

## 7. The runnable form, `intake.js` — 4 issues

| # | issue | where | found by | ✓ |
|---|---|---|---|---|
| 7.1 | Dispatches readiness **before method 3.0**, skipping the text-only understanding step and the restatement-based tiny test | `intake.js:623` | codex | ✓ |
| 7.2 | **FIXED 2026-10-05 — the design carries `baseline.command` (G10) and intake.js V6 verifies it, not a git snapshot.** Its only baseline is a `git status` snapshot, not the test command **and output** the stop condition requires | `intake.js:507` | opencode | |
| 7.3 | Refuses any loop exit that does not mention "unclear" or "EJ", though 3.5 item 4's first exit is a fresh node on a stronger tier | `intake.js:381` | claude | |
| 7.4 | ~~The checks it emits are placeholders pointing back at the table~~ **MIS-FILED:** the emitter was never `intake.js` — it was `tests/workflows/corpus_check.py:68` and `tests/test_task_types.py:44`, both fixed on 2026-10-04. Filing it under the runnable form sent two experts to the wrong file | `testlog.md:72` | claude | |

## 8. My own construction, observed failing — 3 issues

| # | issue | where | found by | ✓ |
|---|---|---|---|---|
| 8.1 | **ANSWERED BY G6 — the gate requires a different-kind reviewer per build group; pinned by a matrix mutation.** **The engine split can defeat rule 5**: code generation is split between opencode and Codex, so a `codex` reviewer reviews code Codex partly wrote — it passes G6 only because `engine_kind` reads the cell's leading token | `testlog.md:105` | claude | ✓ |
| 8.2 | **RESOLVED BY REMOVAL 2026-10-05.** EJ: the fallback was over-engineering — there is already a check before the workflow is built, opencode now has priority over codex, and a failure reports back on its own. `DEFAULT_FALLBACKS`, the per-node `fallback`, the retry in `run_node` and the `check_plan` validation are gone: one engine per node, and a failure blocks the node and goes to EJ. The same-kind clash cannot happen because nothing changes engine mid-run. 511 tests pass. **`DEFAULT_FALLBACKS["codex"]` is Claude**, so after a fallback a Claude-appointed verifier is no longer a different kind, and no rule restores it | `engines.py` | codex | ✓ |
| 8.3 | **FIXED 2026-10-05 — a node's five things are contents, not a list of names.** Every node's `five_things` is the bare template list — `['context','contract','evidence','state','tools']` with nothing behind them | `testlog.md:72-79` | claude, opencode | ✓ |

## Totals

| area | issues |
|---|---|
| 1. The gate cannot reject | 7 |
| 2. The test could not fail | 6 |
| 3. Step 1 / readiness script | 5 |
| 4. The three renderings disagree | 8 |
| 5. Composition — work with no owner | 7 |
| 6. Decisions never made | 5 |
| 7. The runnable form | 4 |
| 8. My own construction | 3 |
| **total distinct** | **45** |

Checked by me: 29 of 45. Engine-only: 16.

## What is not in this register

- **G, H and I from the algorithm review produced no findings at all** — no engine found a case where the gate
  enforces something no step states, where a table omits a field a step assumes, or where a template lacks a field a
  step demands. A blank result, recorded so it is not re-asked.
- **The recommendations**, which are not defects: the mutation run (all four engines), running the checklist layer,
  and giving the corpus negative controls.
- **The unreviewed engines' behaviour**: agy produced nothing when the evidence was on disk and everything when it
  was inlined. That is a fact about agy, filed in the run READMEs rather than as a defect of the algorithm.

## Corrections found by running the workflow (2026-10-05)

Two rows here were wrong, and it took a workflow to find them: `5.7` claimed the caps were method-only when
`dispatch.py` enforces them on a dispatch plan (the *gate* has no cap rule — that is the real gap), and `7.4` was
filed under the runnable form when the emitter was the corpus harness, which sent two experts to edit the wrong file.
Both are corrected above. `runs/20261004-domain-fix-review/` has the three surveys, the chair that caught them, and
the verifier that then corrected the chair's own corrections.


## Found by Claude Code, 2026-10-05 — a placeholder satisfied two new rules

Given one fresh challenge (`p273`) and no help, Claude Code produced a passing design and then pointed out that two
of the fields it had honestly marked `UNRESOLVED` would be **accepted by the gate anyway** — because G10 and the G2
`touched_paths` clause tested only for emptiness.

Confirmed with four cases (`TBD` as a command, `["UNRESOLVED"]` as paths, `—` as an engine, both at once) and closed
as **G12**: a placeholder is a promise to fill a field in later, not a value. Two mutations pin it.

It is the same lesson as the rest of the register, arriving from a new direction: **a check that only asks whether a
field is non-empty cannot fail**, and the honest-but-unknown case is exactly where it fails silently. The
consequence is deliberate — a design whose baseline is `UNRESOLVED` no longer passes, because it should be a
question rather than a design.


## 9. Found while answering the `others` question — 1 issue

| # | Finding | Evidence | Reviewers | ✓ |
|---|---|---|---|---|
| 9.1 | **The gate cannot tell which node writes.** `builds` and `touched_paths` are design-level, so a design says "something here builds" and names files, but no node carries the fact. G13 can therefore only catch a *wholly* unclassified design that builds in one node; a three-node design with the writer first passes. This is register 1.5's missing witness seen from the node side, and it is why "`others` may not build" was not expressible as a rule | `design_gate.py` G2/G13; found 2026-10-05 | claude code (found it by being blocked by it) | |


## 10. The plan is not compared with the design — decision C, 2026-10-05

| # | Finding | Evidence | Decision |
|---|---|---|---|
| 10.1 | **Nothing compares the runnable plan to the design the gate approved.** `check_plan(plan, base)` receives only the plan and checks its internal consistency, so a plan can drop every node's `check` (verified: still passes) or swap an engine while keeping its model (verified: only the missing `model`/`inner_timer` is caught, not the change). A design's guarantees therefore do not survive the crossing by any mechanism | `dispatch.py:51`; tested against `runs/20261003-node-workdir/plan.json` | **C — leave it (EJ, 2026-10-05).** One author writes both and can see both; a checker would guard against an author standing right there. Recorded in `METHOD.md` 3.7 as a decision with its revisit condition. |

### Corrected here: the design's `engine` field is not a bug

I claimed earlier on 2026-10-05 that "every design fails at dispatch on its first node" because a design node's
`engine` is prose (`'agy (EJ, 2026-10-04)'`) while `dispatch.py:261` reads a bare name plus a separate `model`.

**That was wrong.** Designs are not dispatched; plans are. A real plan (`runs/20261003-node-workdir/plan.json`) has
`"engine": "codex"` and `"model": "gpt-6.1-sol"` — exactly the shape dispatch reads. And method 3.4 says the design
starts from a table lookup, so the design quoting the table's engine cell is the design doing its job, at *kind*
level, while the plan names the exact engine at *run* level. Two artifacts, each right for its own level.

The lesson, recorded because it is the third instance in one day: **checking a claim means checking that the two
things being compared are the same artifact.** 6.5 was a conditional read as a branch; 5.6's "3.6 requires an
engine" was false; this was a design judged by the dispatcher's rules.


## 11. Found while answering the 1.5 question — 2 issues

| # | Finding | Evidence | Reviewers | ✓ |
|---|---|---|---|---|
| 9.2 | **FIXED 2026-10-05, and NOT by requiring git.** EJ: *"I don't want git be a must here"* — so the fix went the other way. `intake.js` STEP 1 no longer runs `git status --short` unconditionally: it checks `git rev-parse --is-inside-work-tree` first, and in a plain directory records "no git here" and moves on. The baseline is now explicitly unconditional — a command and its output, no git involved — which is also why 7.2's "not a snapshot" reasoning still holds. `METHOD.md` 3.1 records the decision. **A run needs git, and nothing checks the product is a git repository.** Readiness requires the `git` *binary* (`readiness.py:40`) but never that the directory is a repo, while `intake.js` STEP 1 runs `git status --short` unconditionally before creating anything. Outside a repo that prints `fatal: not a git repository` and exits non-zero, so a non-git product dies at the first step of every run with no readiness warning. **EJ raised this** ("(a) sounds like must have a git if I am not wrong") while choosing the witness for 1.5 | `readiness.py:40`; `intake.js` STEP 1 | EJ (found it), 2026-10-05 | |
| 9.3 | **STEP 1 called the git snapshot "the baseline"**, contradicting the 7.2 fix three places over (`intake.js:279-282`, `:601`, `:630` all say the baseline is the product's test command and its output). So 7.2 was only half-applied: the verification step was corrected and the step that *records* the baseline was not. **FIXED 2026-10-05** — STEP 1 now takes two separate "before" records: the working state (git) and the baseline (the test command and its output) | `intake.js:553` | found by following EJ's question | ✓ |

## Where to start

The gate family (1) and the test family (2) are one story: the gate cannot reject, and the test was built so that it
would never need to. **The mutation run is the cheapest decisive step** — it costs no model calls, and it either
shows the gate catching known-bad designs or quantifies how much of it is decorative. 5.1 (the baseline has no
owner) is the most serious single defect in the algorithm itself.
