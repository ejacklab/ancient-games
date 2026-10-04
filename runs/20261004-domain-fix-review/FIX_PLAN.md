# FIX_PLAN — the chair's reconciliation

Three experts (claude-opus-5-5, minimax-m3.1-flash, deepseek-v4-pro) surveyed the register's 45 issues
blind. This file reconciles their verdicts into one plan. Verdict vocabulary: DIRECT · SCHEMA · DECISION ·
DOC · LATER. Agreement is computed here, not taken from the surveys.

Two fixes already in `runs/20261004-open-defects.md` (1.7 FIXED, 2.5 FIXED, 2.3 ADDRESSED) are excluded from
the fix list. Two further items are demoted by the chair in §2 and §5 because the underlying code is already
fixed and the DIRECT votes inherited a register mis-filing — see 7.4.

---

## 1. The consensus table

One row per issue any expert called DIRECT.

| issue | claude | minimax | deepseek | agreement | the fix, and the check that proves it |
|---|---|---|---|---|---|
| 1.4 | DIRECT | DIRECT | DIRECT | 3/3 | Make the `pattern` cell load-bearing in `design_gate.py`. Check: a mutation that strips `loop` from a loop-pattern building node returns CAUGHT. Fix is disputed: claude/deepseek reuse the parsed `pattern` cell, minimax adds a new `pattern_kind` column + G10. |
| 1.6 | DIRECT | LATER | DIRECT | 2/3 | G3 fires loop rules on a loop-capable node even with no `loop` object. Check: loop-strip mutation → G3 rejects, and `--self-check` reports MISSED when neutered. minimax: LATER (blocked on 1.4's column). |
| 2.1 | LATER | LATER | DIRECT | 1/3 | deepseek alone: admit hand-authored designs into `corpus_check.py`. No independence check for those designs is named, so it re-duplicates the table rather than breaking the circularity — not a consensus fix. |
| 2.2 | DIRECT | DIRECT | DIRECT | 3/3 | Exercise G5/G7. claude fixes `mutation_matrix.py`'s G5 rows to use `claim_margin`; minimax/deepseek emit a challenger arm in `corpus_check.py`. Check: threshold lowered to 0.05 → the 10% row reports MISSED (claude); a challenger ledger row reaches G5 arithmetic (minimax/deepseek). Different sides of one defect. |
| 2.6 | DIRECT | LATER | DIRECT | 2/3 | `corpus_check.py` emits the row's `pattern` beside `sabotage`, then the 1.4 rule exercises it. Check: re-emit through the gate → zero new G3 findings + the 1.4 mutation. minimax: LATER (blocked on 1.4). |
| 3.1 | DIRECT | DIRECT | DIRECT | 3/3 | `readiness.py:197-205`: `check_blueprint` returns MISSING when the map/sections are absent, and `self_test()` calls it. Check: `test_rt_15` flips (mapless blueprint not VERIFIED); `--self-test` fails on a fixture. |
| 3.2 | DIRECT | DIRECT | DIRECT | 3/3 | `readiness.py:184`: `absent_status` defaults to MISSING. Check: `test_rt_16` flips (empty directory not verified). |
| 3.3 | DIRECT | DIRECT | DIRECT | 3/3 | `readiness.py:204`: count blueprint sections, not every `.md`. Check: `test_rt_13` flips (extra `.md` files not counted). Fix is disputed: claude counts "k of 8 section files", minimax counts "map + sections (map-only = 1)". |
| 3.4 | DIRECT | DECISION | DIRECT | 2/3 | `readiness.py:326` `exit_code`: a `--require`d UNKNOWN item fails like MISSING. Check: `--require` on a timing-out stub exits 1. minimax: DECISION (EJ says what `--require` promises). |
| 3.5 | DIRECT | DIRECT | DIRECT | 3/3 | `readiness.py:158-163`: guard a non-object `model` (UNKNOWN, not an uncaught AttributeError). Check: settings `{"model":"x"}` → UNKNOWN. |
| 4.3 | DOC | DIRECT | DOC | 1/3 | minimax alone DIRECT: rewrite the `DIAGRAM.md:213` row to name step 7. Check: `grep -n "3\.8" SKILL.md` shows steps 1 and 7. Editable, but 2/3 read it as doc drift — not a consensus fix. |
| 4.5 | SCHEMA | SCHEMA | DIRECT | 1/3 | deepseek alone DIRECT: "join the pieces to the nodes" — an adapter, which house rule 7 (pick one, never blend) forbids. Others: pick one canonical format (EJ's call). Not a consensus fix. |
| 4.8 | DOC | DIRECT | DOC | 1/3 | minimax alone DIRECT: delete `information extraction` from `TASK_TYPES.md:63`. Check: `corpus_check.py --compare` stops scoring those answers as mismatches. Re-issuing the published accuracy is EJ's, so not a consensus fix. |
| 7.1 | DIRECT | DECISION | DIRECT | 2/3 | `intake.js` runs the 3.0 restatement before readiness (a required `restatement` in READY_SCHEMA). Check: an `intake_harness.mjs` sabotage case with no restatement fails step 1. minimax: DECISION (headless COO cannot do 3.0). |
| 7.2 | SCHEMA | DIRECT | DIRECT | 2/3 | `intake.js` step 1 records the test command and its output as the baseline, not only `git status`. Check: `intake_harness.mjs` asserts the baseline carries both. claude: SCHEMA (waits on 1.2's field); minimax: presumes 5.1's owner. |
| 7.3 | DIRECT | DIRECT | DIRECT | 3/3 | `intake.js:381` accepts 3.5 item 4's first exit (a fresh node on a stronger tier). Check: "fresh node on a stronger tier, then the unclear list" passes; "another round" still fails. |
| 7.4 | DOC | DIRECT | DIRECT | 2/3 | Demoted by the chair (see §2): the two DIRECTs rest on a false premise. `intake.js` never emitted the placeholder; `corpus_check.py:69` already emits the row's own check (verified). Residue is filing, not code. |
| 8.1 | DECISION | SCHEMA | DIRECT | 1/3 | See §3: the right verdict is deepseek's DIRECT (G6 checks the reviewer against every engine the cell names). Not consensus (1/3). |
| 8.2 | DIRECT | SCHEMA | DIRECT | 2/3 | `workload.py:168-171` also compares the verifier against the worker's resolved fallback (`plan.fallback` or `engines.DEFAULT_FALLBACKS`). Check: a `test_workload.py` case — codex node, claude verifier, no plan fallback → rule 5. minimax: SCHEMA (`executed_engine` field). |

---

## 2. The direct fix set

### 3/3 — 7 fixes

- **1.4** — edit `design_gate.py` so a loop-pattern building node must carry `loop`; check: a `mutation_matrix.py` row stripping `loop` returns CAUGHT. *Different fixes, same verdict:* claude/deepseek reuse the parsed `pattern` cell; minimax adds a `pattern_kind` column — that is a disagreement about the fix, not the verdict.
- **2.2** — make G5/G7 execute: claude edits `mutation_matrix.py`'s G5 rows to `claim_margin`; minimax/deepseek emit a challenger arm in `corpus_check.py`; check: lowering the G5 threshold to 0.05 makes the 10% row MISSED, or a challenger ledger row reaches G5 arithmetic. *Different targets for the same defect:* test-side (claude) versus corpus-side (minimax/deepseek).
- **3.1** — edit `readiness.py` `check_blueprint` and `self_test()`; check: `test_rt_15` flips and `--self-test` fails on a mapless fixture.
- **3.2** — edit `readiness.py:184` to default `absent_status` to MISSING; check: `test_rt_16` flips.
- **3.3** — edit `readiness.py:204` to count blueprint sections; check: `test_rt_13` flips. *Different counting targets:* claude "k of 8 section files" vs minimax "map + sections (map-only = 1)" — the exact number is unsettled even at 3/3.
- **3.5** — edit `readiness.py:158-163` to guard a non-object `model`; check: settings `{"model":"x"}` → UNKNOWN, no exception.
- **7.3** — edit `intake.js:381` to accept 3.5 item 4's first exit; check: the "fresh node on a stronger tier, then unclear list" harness case passes and "another round" still fails.

### 2/3 — 6 fixes (7.4 demoted)

- **1.6** — edit `design_gate.py` so loop rules fire on a loop-capable node with no `loop` object; check: loop-strip mutation → G3 rejects, `--self-check` reports MISSED when neutered.
- **2.6** — edit `corpus_check.py` to emit the row's `pattern`; check: re-emit through the gate → zero new G3 findings plus the 1.4 mutation.
- **3.4** — edit `readiness.py:326` `exit_code` so a `--require`d UNKNOWN item fails; check: `--require` on a timing-out stub exits 1.
- **7.1** — edit `intake.js` to run the 3.0 restatement before readiness; check: the no-restatement sabotage case fails step 1.
- **7.2** — edit `intake.js` step 1 to record the test command and output as the baseline; check: `intake_harness.mjs` asserts the baseline carries both. Depends on 5.1 (who owns the baseline) — minimax names this, claude adds the 1.2 field dependency.
- **8.2** — edit `workload.py:168-171` to compare the verifier against the worker's resolved fallback too; check: `test_workload.py` codex-node/claude-verifier/no-fallback → rule 5.

**Demoted: 7.4.** minimax and deepseek both voted DIRECT, "edit `intake.js` to emit the row's real check." That
premise is false. The emitter was `tests/workflows/corpus_check.py`, not `intake.js`, and `corpus_check.py:69`
already emits `known[c].get("check")`; `intake.js` never hardcoded a table-pointer check (its DESIGN_SCHEMA `check`
field is free text). The register's area-7 filing and its `testlog.md:72` evidence point at the corpus log, which
is a stale record, not live code. The only remaining work is refiling 7.4 and giving it a status row in
`runs/20261004-open-defects.md` — a DOC item, not a fix.

---

## 3. The three where nobody agreed

### 5.2 — the final "what is missing" pass has no owner

claude: SCHEMA · minimax: DOC · deepseek: DECISION.

**The chair rules: DECISION (deepseek).** The register files this under "Composition — work with no owner," and
`runs/20261004-open-defects.md` groups §5/§6 as things that "change the algorithm rather than correct a slip."
The pass is *demanded* (`WORKFLOW_DESIGN_METHOD.md:482`, §5 quality-control row; `:306-309`, 3.6's closing) and
*mentioned* (`SKILL.md:139`, step 8), but no step emits it as a node in 3.6's graph. The real open question is
which step owns it and whether it is a graph node at all — a design choice (budget, engine, edges) that EJ owns.
minimax's DOC correctly locates the three renderings that would have to change (SKILL step 8 vs METHOD 3.6 vs the
diagram's missing box) and gives a checkable sub-fact, but it labels an algorithm gap as doc drift. claude's SCHEMA
answers a different question: adding a `role` field and a G-rule would let the *gate* enforce "exactly one such
node," but the register's defect is that no step *produces* the node — enforcement of a node nobody emits fixes
nothing.

### 6.4 — 3.2 assigns node membership before 3.3/3.4/3.6

claude: DOC · minimax: LATER · deepseek: DECISION.

**The chair rules: DOC (claude).** Reading the method settles it. 3.2 (`WORKFLOW_DESIGN_METHOD.md:192-200`)
already says "A label is not a node," that pieces "merge into one node … the default," and that the output row
records "the node it merges into"; 3.6 (`:272`) then says "nodes = right-sized pieces." So 3.2 records a
*provisional* merge and 3.6 finalizes nodes — the register's "assigns membership before sizing" is a wording
artifact, not an ordering defect. The fix is to rename the 3.2 column "provisional node" and say 3.6 fixes it,
which is a one-line doc edit. deepseek's reorder would put "write the algorithm" after "build the graph," which is
incoherent. minimax's LATER chains 6.4 to 4.5 (pieces vs nodes), a false dependency: 3.2/3.6 are prose concepts,
not the JSON format, so no `piece_id` field is needed to fix this.

### 8.1 — the engine split defeats rule 5 (a codex reviewer reviews Codex's own code)

claude: DECISION · minimax: SCHEMA · deepseek: DIRECT.

**The chair rules: DIRECT (deepseek).** The facts (verified): `design_gate.py:51-66` `engine_kind` returns one
kind — the leading token — and G6 (`:213-224`) builds its "different kind" constraint from that single kind; but
the corpus design's engine cell literally reads "opencode `…` + Codex `…` (split: `workload.py`, opencode priority)"
(`testlog.md:105`). The data needed is already in the cell, so the fix is a code edit: G6 must compare the reviewer
against *every* engine the cell names (or `engine_kind` must return the set), checkable by a mutation whose
reviewer overlaps a builder → reject. minimax's SCHEMA adds an `engine_kinds` field the cell already carries —
unnecessary. claude's DECISION overstates a default assignment (the role map gives code review to codex) into a
"two rules conflict": rule 5 already forbids same-kind review, and the gate simply cannot see it. The downstream
consequence claude names — a split build must then be reviewed by a third kind — is real and should be recorded as
follow-up, but it follows from the fix rather than blocking it.

---

## 4. The verdicts that are not DIRECT

### SCHEMA — the field that is missing

- **1.1** — `five_things` must be an object of name → content, not five names.
- **1.2** — `baseline` (`{command, output_file}`) on a design that builds.
- **1.3** — `stop` as three named parts on a building node.
- **8.3** — the same field as 1.1; count once.
- **4.5** — the format itself: intake emits `pieces`, the gate reads `nodes`; minimax names `nodes[].piece_id`.
  Blocking: EJ picks the canonical format (claude: intake's piece; deepseek's "join them" is the blend rule 7 forbids).

### DECISION — the choice EJ faces

- **5.1** — which step records the baseline before the first building node, and stop-versus-freeze when it is already red.
- **5.3** — step-5 loops start before steps 6-7 bound concurrency, or nothing runs until step 7.
- **5.4** — what a non-product-change run ends at (recorded reason / restatement stop / narrow the promise).
- **5.5** — whether the tiny-task exit still records a baseline when it changes product code.
- **5.6** — name an engine for `others`, or rule it a never-dispatched spot.
- **6.1** — fallback engine, stronger-tier model, per-node attempt limit (ratify `engines.py:157` DEFAULT_FALLBACKS or overrule it).
- **6.2** — a run-wide replan limit (claude recommends 1; minimax names the field `replan_budget`).
- **6.3** — the challenger claim at sizing (a pre-estimate) versus after 3.6; claude notes no challenger exists yet, so it cannot bite.

### DOC — the files that disagree

- **4.1** — `SKILL.md:175` has the engine split; `WORKFLOW_DESIGN_METHOD.md` and `WORKFLOW_DESIGN_DIAGRAM.md` mention it nowhere. Blocking: settle 8.1 first.
- **4.2** — `SKILL.md:165` says three and lists four; `WORKFLOW_DESIGN_METHOD.md:476` is titled "Three qualities." minimax: DECISION (is the split a fourth quality or a rule inside quality control?).
- **4.3** — `WORKFLOW_DESIGN_DIAGRAM.md:213` says "no step"; `SKILL.md:49-53` and `:122-131` carry 3.8 in steps 1 and 7.
- **4.4** — `EXECUTOR_KINDS.md:63` and `:17` route classification to agy/gemini; `EXECUTOR_KINDS.md:156` routes it to deepseek-flash. minimax: DECISION (which is current).
- **4.6** — `WORKFLOW_DESIGN_METHOD.md` §3.1 (`:76-80`) lacks the two rules; `SKILL.md:51-57` has them.
- **4.7** — `TASK_TYPES_LEDGER.md:7` says "Coverage outcome"; `design_gate.py:39` expects `coverage_result`.
- **4.8** — `TASK_TYPES.md:63` (use case 2 teaches extraction) against `TASK_TYPES.md:120` (rule 2 forbids it as a pass-through). minimax's delete is DIRECT but re-issuing the accuracy figure is EJ's.
- **5.7** — `WORKFLOW_DESIGN_METHOD.md:333,426` (caps + item 12) against `SKILL.md` (neither). *Corrected:* the caps half of the register is wrong — `dispatch.py:41,62-64,107-109` enforces `max_roles 5` and `max_parallel 3`; only item 12 is genuinely method-only.
- **6.5** — `WORKFLOW_DESIGN_METHOD.md:213` (3.3 branches before 3.4) against `WORKFLOW_DESIGN_DIAGRAM.md:37` (Size after spots resolve). deepseek: DECISION (reorder).
- **7.4** — refile: the register files it under intake.js; the real emitter is `tests/workflows/corpus_check.py:69`, already fixed.

### LATER — the blocking reason

- **1.5** — needs a post-run witness (`git diff --name-only`) no designed run has yet produced. minimax: DECISION (EJ names the witness).
- **1.7** — FIXED (G3 rejects a table-pointing check; the mutation matrix has the row).
- **2.1** — a non-circular input needs an independent producer; deepseek's hand-authored designs carry no independence check.
- **2.3** — ADDRESSED (`mutation_matrix.py` runs in the suite, `--self-check` proves it can report a MISSED).
- **2.4** — the checklist layer is prose with no script, so a run of it is not falsifiable by a named check. claude: DECISION (EJ buys a blind fixed-checklist pass).
- **2.5** — FIXED (README states the denominators); claude notes `testlog.md:34` still prints the bare "codex 90%".

The three disputed issues (5.2, 6.4, 8.1) are in §3 and not repeated here.

---

## 5. What the three experts agreed on that deserves suspicion

Consensus is not evidence. Four cases:

**1. The SCHEMA consensus on 1.1 / 1.3 / 8.3 overstates the work.** All three label these "the design format
needs a field," but only claude checked that the format largely *exists*: `intake.js`'s DESIGN_SCHEMA (`:169-201`)
already carries `stop`, `intent`, `returns`, `files_touched`, `must_not_change`, `evidence`, `state_reads/writes`,
`brief_given/withheld`. So 1.1, 1.3, 4.5 and 8.3 are one canonical-format decision (4.5), not four field
inventions. The 3/3 SCHEMA agreement hides that the real question is whether EJ accepts the open-defects
projection — 94 of 300 designs and 150 building nodes going red — which is a *decision*, not a field name.

**2. The 3/3 DIRECT consensus on the readiness family hides two live disagreements.** 3.1/3.2/3.3/3.5 are
unanimous DIRECT with the same "flip the existing test assertion" checks, but 3.3's counting target differs
(claude: "k of 8 section files"; minimax: "map + sections, map-only = 1"), and 3.4 — the fourth member of the
same vocabulary defect — is only 2/3 because minimax thinks `--require`'s promise is an EJ decision. The
unanimity is on the *file*, not the *semantics*.

**3. The 3/3 DOC consensus on 5.7 rests on a false register premise that two of three inherited.** The register
says the 5-role/3-at-once caps "exist only in the method"; `dispatch.py:41,62-64,107-109` enforces them, so
minimax's "nothing would catch a design running six at once" is false, and deepseek's "port them to SKILL.md and
DIAGRAM.md" restates the same error. Only claude re-read the code. Same verdict, three different reasons, two of
them wrong.

**4. The "fix first" agreement is inherited, not independent.** All three lead with the gate/test/readiness
families the register itself calls "where to start," and each expert's first-fix priority matches the register's
own ranking (gate family + readiness, the mutation run, 5.1 as most serious). The experts converged on the
register's priorities rather than independently re-deriving them — which is exactly why the one expert (claude)
who re-read the code was the one who broke rank on 5.7, 6.4 and 7.4.

### Expert errors caught (inherited, not added)

- **7.4** — minimax and deepseek both voted DIRECT to edit `intake.js`; `intake.js` never emitted the
  table-pointer check — `corpus_check.py:69` did, and already emits the row's own check. Both experts inherited the
  register's "intake.js" area-7 filing.
- **5.7** — minimax's "nothing would catch a design running six at once" is contradicted by
  `dispatch.py:41,62-64,107-109`; deepseek's "caps live only in the method" repeats the same register error.
- **4.5** — deepseek's DIRECT ("join the pieces to the nodes") proposes an adapter; house rule 7 (pick one format,
  never blend) and both other experts say this is a canonical-format decision for EJ, not a mechanical join.
