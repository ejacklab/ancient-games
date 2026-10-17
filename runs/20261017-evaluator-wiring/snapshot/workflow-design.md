# Workflow design — 20261013-requirements-evaluator

A design, not a run. Nothing here has run. Method: `docs/WORKFLOW_DESIGN_METHOD.md`. Written 2026-10-13 by the COO
(Claude `claude-opus-5-5`) at EJ's request: *"design a workflow that based on the product visions and requirements to
develope an evalutor that check do the developed software meet all the requirements"*. Beside it: `state.md`,
`design.json` (gate input).

## Questions for EJ (Q1–Q3 change the shape; Q4 is the blueprint and is not answered by silence)

| # | Question | Provisional assumption |
|---|---|---|
| Q1 | Is the evaluator **reusable**, for any product whose requirements carry ids and **Fails if** lines? Or is it only for the INDEX.md generator? | Reusable. The INDEX.md generator is the first target and the calibration product, because it is the only built software here with requirements. |
| Q2 | What form should it take? | A Workflow script, `.claude/workflows/evaluate-requirements.js`, with stdlib Python helpers next to the workflow-design scripts. The arguments are `{product, spec, runId}`, and each run writes to `runs/<runId>/`. |
| Q3 | Which **vision** lines are checked? | The **"never"** lines and the **"How we know it works"** lines, which are already written as checks. The rest of the vision (who it is for, the problem) is context, not evaluated. |
| Q4 | **Blueprint.** The evaluator is a new product, so it needs its own vision and requirements, accepted by you, before anything builds (method 3.1). | D1 drafts them in `docs/evaluator/` from this design, and you accept or correct them. The build waits for that. |

## Restatement (method 3.0)

**Objective.** A tool that takes a product's vision and requirements plus the built software, and answers per
requirement **PASS**, **FAIL** (with a repro) or **UNKNOWN** (with the reason). It also gives one overall answer:
**MEETS** only when every in-scope requirement passes. Its PASS can be trusted because every check behind it was shown
to be able to fail.

**In scope:**
- the evaluator itself: its blueprint, scripts, node briefs and workflow;
- its calibration on the INDEX.md generator.

**Out of scope:**
- fixing what it finds in the INDEX.md generator (that goes to `docs/index-md/BACKLOG.md`);
- non-software products (designs, documents);
- performance and security testing beyond what a requirement states.

**Whys.**
1. **Problem.** "Tests pass" is the builder's claim about the builder's tests. This run's history shows why that is
   not enough. The builder bent the code to fit a defective test (N2), the tests missed a requirement until mutants
   found it (N3), and only the review saw three defects (N4). An evaluator that starts from the spec, not from the
   build, is the independent check.
2. **Now.** The first product went through the full SDLC, and its evidence is fresh.
3. **Shape.** It generalises what worked in run `20261012-index-md-build`: blind tests from the spec, mutants per
   Fails if, a judged checklist with a plant, and a missing proof never counting as PASS.
4. **Failure.** A false PASS would wave broken software through, which is the expensive failure; a false FAIL costs a
   look. So the asymmetry is designed in: PASS needs proof, and everything else is FAIL or UNKNOWN. **Risk: high.** It
   will gate other work, and a false PASS shows up late.
5. **Stop.** At a working, calibrated evaluator with known-answer results. Running it on other products comes later.
6. **Done.** The calibration (D5) shows it FAILs seeded faults against the right requirement, never PASSes an
   untestable requirement, and backs every claim on the clean product with evidence.

**Category** (*inferred*): code generation + test cases gen + document and explain (the node briefs) + code review.
Calibration is grading the evaluator: "grade a run", with missing proof = UNKNOWN.

## The evaluator: what it does when it runs (the product's algorithm)

This is what D1 turns into requirements. Each step names its check.

| # | Step | Who | Check |
|---|---|---|---|
| E1 | **Read the spec.** Parse REQUIREMENTS (ids, groups, each **Fails if** split into failure cases, status in scope or *open*) and the vision's "never" and "how we know" lines into `requirements.json`. | script | Id count equals a grep of the file. A group with no Fails if is listed as **untestable**, never dropped. |
| E2 | **Build a blind workspace.** Copy the product code and the spec into `runs/<id>/workspace/`, **without** the product's own tests, its run folders or its git history. | script | A listing of the workspace. A planted `tests/` marker must be absent. |
| E3 | **Classify each failure case:** *executable* (a probe can run it), *static* (inspect files or config), *judged* (only reading can tell), or *human* (EJ). | model, cheap tier | Schema-valid, and every case has exactly one kind. An ambiguous case becomes *human*, not a forced label. |
| E4 | **Write probes** for executable and static cases: tests that each cite their case id, written from the spec, blind to the product's tests and to how it was built. | model A | Collects; `trace_check` finds every case id. |
| E5 | **Write mutants:** one broken copy of the product per failure case, written from the spec and the code, blind to the probes. | model B, a different kind from A | Each applies to exactly one place in the code. |
| E6 | **Prove the probes can fail:** run every probe against every mutant (the `mutate.py` matrix). A case whose probe is red on no mutant is **unproven**. | script | The matrix is complete, and the originals are restored. |
| E7 | **Run the probes on the real product.** | script | Each probe has a recorded outcome. |
| E8 | **Confirm every FAIL:** a fresh agent reads the spec sentence, the probe and its output, and answers whether the probe is faithful to the sentence. An unfaithful probe makes the case **UNKNOWN** and gets one probe repair. | model C, fresh | A yes or no, with both quoted. |
| E9 | **Judge the judged cases** on a fixed checklist with quoted file:line, with **one planted defect** in its copy. | model C, a different kind from the builder | The plant is found, or the judging is void. |
| E10 | **Verdict** per case and per requirement: **PASS** = the probe is green on the product **and** red on its mutant (or a judged yes with a found plant); **FAIL** = a red probe that E8 confirmed; otherwise **UNKNOWN**, with the reason. **MEETS** only if every in-scope requirement is PASS. | script | Table-driven: empty evidence is UNKNOWN, never PASS. |

E1, E2, E6, E7 and E10 are scripts, so a fixed result needs no model. Models are used only where only a model can do
the work (E3, E4, E5, E8, E9). E4 and E5 are different kinds, so a probe and the mutant that proves it do not share
blind spots.

## Blueprint (for the evaluator)

- **Kind of task:** new product.
- **Sections needed:**
  - vision and requirements (missing → D1);
  - architecture (this table plus Q2, drafted in D1);
  - non-functional: cost per evaluation run and wall time, drafted in D1 as **measured at calibration**, not as a
    number up front.
- **Acceptance criteria:** proposed by D1, ids `EV…`, fixed when EJ accepts. Every one is covered by a building
  piece below.
- **Baseline:** `env -u NO_COLOR python3 -m pytest -q` (685 at `21b2597`).

## Pieces, in the order they run

### D0 — Readiness (the COO)

- **Steps:**
  1. Prove the engines with one canary each, with `</dev/null` (memory: engine calls need it).
  2. Record the baseline.
  3. Fix the calibration product at a commit (INDEX.md generator at `21b2597`).
- **Check:** script. **Builds:** no. **Evidence:** `nodes/d0-1.result.md`.

### D1 — Blueprint piece: the evaluator's vision and requirements (the COO drafts, EJ accepts)

- **Steps:**
  1. Draft `docs/evaluator/VISION.md` and `REQUIREMENTS.md` from this design and Q1–Q3. Use three lifecycle
     categories (proposed: **Read** the spec, **Check** the product, **Report** the verdict), ids `EV-R…`, `EV-C…`,
     `EV-P…`, each with a source and a **Fails if**.
  2. Run each requirement through `requirement-check`.
  3. EJ accepts.
- **Check:** EJ's. **Builds:** no.
- **Blocks:** every piece that builds.
- **Note:** it proposes the criteria D2–D5 cover.

### D2 — The script parts (code generation; loop)

- **Two modules:**
  - **`spec_parse.py`** (E1): the spec to `requirements.json`.
  - **`verdict.py`** (E10): probes × matrix × confirmations × judged results to `verdict.json` and `verdict.md`.

  Plus a small COO change: `trace_check.py` and `mutate.py` from run `20261012-index-md-build` move next to the
  workflow-design scripts, made generic (case ids from `requirements.json`, the target file as an argument).
- **Engines:** the split from `workload.py`. At 2 modules, opencode leads 3 of 4 nodes, and one module is self-tested
  (*ran* on the same shape, 2026-10-12). Tests come before code in each module, as in the INDEX.md run (N1 → N2).
- **Check:** `feature_gate.py check`. Known-answer fixtures:
  - `spec_parse.py` on the three real spec files gives the grep counts (INDEX.md: 11 Fails-if groups over 32 ids);
  - `verdict.py` on hand-made matrices, including "no evidence" giving UNKNOWN.
- **Loop:** 3 attempts, then the stronger tier, then EJ.
- **Covers:** the `EV-R…` and `EV-P…` criteria D1 proposes.
- **May change:** the two modules, their tests, and the two moved scripts.

### D3 — The model-node briefs (document and explain; the COO)

- **Steps:**
  1. Write the five briefs (E3 classify, E4 probes, E5 mutants, E8 confirm, E9 judge), each with a template, a worked
     example **from the INDEX.md run** (real cases: the B1.2 staging defect, the B2.4 gap, the plant) and the
     standard.
  2. Name the default engine per role. These are proposed and checked at D5:
     - E3: `deepseek-flash`, the classifier row;
     - E4: a Claude subagent, so it is not Codex, which wrote the calibration product's tests;
     - E5: Codex `gpt-6.1-sol`;
     - E8 and E9: a Claude Sonnet 5.5 fresh session, or Codex when the product was built by Claude.
- **Check:** a judged checklist (the brief's three parts present, every example traceable to the run folder).
  `quote_check.py` on the quoted examples. **Builds:** yes (the briefs are the product's prompts).

### D4 — The workflow script (code generation; loop)

- **Steps:**
  1. `.claude/workflows/evaluate-requirements.js` wires E1–E10 with the checks in script code.
  2. An offline harness, `tests/workflows/evaluate_harness.mjs`, in the style of `intake_harness.mjs`, runs it with
     stubbed agents.
- **Check:** the harness passes, including a stub agent that returns a wrong verdict, which the script must catch.
  `feature_gate.py`.
- **Engine:** Codex `gpt-6.1-sol`, high effort. The harness is written by opencode, so the code and its tests come
  from different engines.

### D5 — Calibration: the evaluator's own acceptance (grade a run)

This is where it earns trust. Each run is a real evaluation, with the cost recorded.

| Run | Input | Known answer | Fails if |
|---|---|---|---|
| K1 | INDEX.md generator at `21b2597`, its spec | No FAIL without a repro the COO can rerun. Disputed items such as B4.2 ("every run prints the size", backlog 1) may come back FAIL **or** UNKNOWN; a PASS on B4.2 needs a probe that covers the invalid-entry path. | a FAIL that does not reproduce; a PASS whose probe is green on its mutant |
| K2 | k seeded variants of the same commit. Each has **one** fault mapped to one requirement group. The faults are fresh, written by the COO and kept out of every file the evaluator reads, **not** the 32 committed in `runs/20261012-index-md-build/sabotage/`. | each variant: not MEETS, and FAIL (or UNKNOWN) on the mapped group | a variant judged MEETS; a FAIL on the wrong group only |
| K3 | the spec with one planted untestable requirement ("the output must be pleasant to read") and one requirement deleted | the planted one is **untestable / UNKNOWN**, never PASS; the deleted id is absent from the verdict and from the coverage manifest | a PASS on the planted one |
| K4 | the workspace of K1 | no `tests/`, no `runs/`, no `.git`; a planted marker in the product's `tests/` never appears | the marker is read |

- **Compared with:** K2's detection is measured **against the product's own acceptance tests** on the same variants
  (`tests/test_memory_index.py`). The evaluator should catch what they catch, and the comparison is the number EJ
  sees. No threshold is set up front (memory: comparisons, not numbers).
- **Check:** script for K2–K4 (expected against actual), and the COO plus EJ for K1's disputed items.
- **Exit:** a miss sends the piece that missed (D2, D3 or D4) one repair round, then K reruns, then EJ.

### D6 — Blind review (code review)

- **What:** a different kind from D2's and D4's builders reviews the scripts, the workflow and the briefs against
  `docs/evaluator/REQUIREMENTS.md` on a fixed checklist, with one plant. Findings in criteria are fixed (the COO when
  small, otherwise a builder round); the rest goes to `docs/evaluator/BACKLOG.md`.
- **Engine:** a Claude subagent (Sonnet 5.5) if Codex and opencode built it.

### D7 — Close (the COO)

- **Steps:**
  1. Traceability: `EV` id → test → calibration run.
  2. Baseline and must-not.
  3. A ledger row.
  4. A report with the K1–K4 table and the **cost per evaluation run** (the non-functional number D1 left to be
     measured).
  5. EJ accepts.

## Joins

- **D1 → everything.** If EJ accepts different criteria than proposed, D2–D5 are planned again.
- **D5 K1:** an evaluator FAIL that the product's own tests pass is a contradiction. It stops, and the COO decides
  with the spec sentence quoted: an evaluator bug goes back to D2–D4, and a product bug goes to
  `docs/index-md/BACKLOG.md`. Never averaged.

## Parallel candidates

- **D2's two modules** are independent: no shared files, each has its own check, and neither needs the other. They
  pass the five conditions, but they stay **sequential**, because the time saved (minutes) does not pay for the join
  (EJ: sequential first).
- **D3** (briefs, COO) **∥ D2** (engines) passes all five, with different paths and different checks. It is the only
  candidate, and the unit is **engine processes alive: 1 opencode or Codex call while the COO writes briefs**.

## Predictability

- **Design source:** default rows per piece. Pipeline: "codegen → tests → review", plus a grade-a-run calibration.
  The ledger row is reconciled at D7.
- **Agents:**
  - build: about 6–9 engine calls (D2: 4 nodes plus repairs; D4: 2; D6: 1);
  - calibration: each K run is a full evaluation of about 5 model calls (E3, E4, E5, E8, E9), so K1–K3 is about 15.
- **Bounds:**
  - D2 and D4: 3 attempts plus 2 on the stronger tier;
  - D5: 1 repair round per miss;
  - D6: 1, plus 1 if the plant is missed.
- **Cost estimate** (*not measured*, scaled from run `20261012-index-md-build`):
  - building: about 0.5–1M tokens;
  - calibration: about 0.6–1.2M tokens.

  The real per-run cost of an evaluation is the number D5 measures.

## Debuggability

- **Every piece:**
  - `briefs/<piece>.md` (input);
  - `nodes/<piece>-<attempt>.result.md` (output);
  - `raw/` (gitignored);
  - `runlog` events.
- **Every K run** is its own evaluator run folder, so a wrong verdict can be traced to the probe, the mutant or the
  confirmation that made it.
- **Resume point:** the last done row in `state.md`.

## Quality control

- **Scripts:** E1, E2, E6, E7 and E10; the gates for D2 and D4; and the K2–K4 expected-against-actual checks.
- **Judged:** D3's checklist, D6, and E8/E9 inside every evaluation.
- **EJ's:** Q1–Q4, the K1 disputed items, and the acceptance.
- **Sabotage for each check:**
  - The probes are proved by E6's mutants, inside every evaluation, not only at build.
  - The judge is proved by E9's plant.
  - The evaluator as a whole is proved by K2 (seeded faults), K3 (a planted untestable requirement) and K4 (a planted
    marker).
- **The rule that makes the evaluator worth having:** PASS needs both a green probe on the product and that probe's
  red on a mutant. Missing proof is UNKNOWN, never PASS. That is the "grade a run" row's rule, applied to every
  requirement.
- **The three qualities:**
  - **Predictability:** bounds and estimate above.
  - **Debuggability:** a file per attempt and a folder per K run.
  - **Quality control:** every check has a named sabotage, and the calibration grades the evaluator itself.
