# Task types — default patterns, combination pipelines, and the 20% rule

Agreed with EJ 2026-10-01. **n=0**: every default here is a working value until `TASK_TYPES_LEDGER.md` has
runs in it. Engines cite `docs/EXECUTOR_KINDS.md` defaults and **suggest, never override** the node contract;
every node still names its exact model and effort.

The machine-readable form of the tables is *this file*: the skill's `scripts/design_gate.py` parses it. Do not
copy the table into code or another doc — change it here, the gate follows.

## How this is used (the design rule)

1. **Guess at §3.0, label at §3.2.** The six why-questions (method 3.0) end with a *provisional* category — a
   guess from the prompt text that feeds the tiny test and a first lookup. After the algorithm is written (method
   3.2) its steps are grouped into pieces, one deliverable each, and **each piece is labelled** from this table
   (changed 2026-10-02 at EJ's request; n=0). The piece labels replace the guess; a difference is a Log line.
   A label says what kind of work a piece is, not that it needs its own agent: same-engine pieces with no independent
   check between them merge into one node (method 3.2, "a label is not a node").
   Checked against facts per piece: a piece that touches product code, schema, UI or config is never labelled
   read-only. A wrong label is a **stop and replan**, not a repair (the blueprint kind-guard's shape).
2. **Default-first.** For each labelled piece look up its row (or the combination's pipeline), adapt it to the
   specifics, then run the normal gates. Steps 2–4 of the method still run. `others` has no default: the full
   method from first principles.
3. **Challenger (the 20% rule).** A bespoke design replaces the default only with a written claim **before the
   run**: ≥20% lower projected run cost (tokens / agents / wall time) **at equal coverage** — same acceptance
   criteria ids, same checks, same blindness. Coverage is a gate, never an axis; nobody trades completeness for
   speed. "Ask three times, get three different answers" is variance, not signal — the default stands unless
   the margin is claimed and proven on paper first.
4. **Two-layer review of the decision.**
   - **Script layer (free, deterministic):** `scripts/design_gate.py` — structure, category-vs-facts, label agreement (G8: the design's
     categories equal the categories its nodes carry; the in-run review node is exempt), the
     margin arithmetic, coverage equality, pipeline well-formedness, the reviewer-kind rule, ledger rows.
   - **Checklist layer (cheap judgment):** a Sonnet 5.5 subagent, fresh session, blind to the designer's
     reasoning, judges a fixed 4-item checklist **in one pass**: does the category fit the challenge's intent?
     is the default pattern wrong for this instance, and why? does the claimed margin have a real basis? is
     anything needed absent from both designs? Verdicts binary with evidence refs — never "try to reject it".
     Two repair attempts on script failure; a checklist "no" escalates per the tier exit (fresh stronger node
     or EJ), never a third round. **Risk tier:** when the design builds or EJ flagged high risk, the checklist
     reviewer is a different kind from the designer (Codex `gpt-6.1-sol`) instead of Sonnet 5.5.
   - This reviews the *design decision*. The design's own in-run review nodes are separate and follow the
     `code review` row below.
5. **Ledger.** Every run appends one row to `docs/TASK_TYPES_LEDGER.md`: date, run id, category,
   default-or-challenger, claimed margin + basis, actual cost, coverage outcome, reconciled. A challenger that
   beats its projection twice becomes a candidate new default; a default repeatedly overridden gets its row
   rewritten. This is how the table earns its n.

## Use cases in focus (EJ, 2026-10-02)

What a software developer does daily, ranked for EJ's work. A use case is usually a pipeline of the categories
below, not one row. Evidence: the 90 real prompts of the 2026-10-02 corpus campaign, labelled by the COO (not
independent); #8 has no prompt in that corpus and is ranked on ordinary practice. n=0 for every default here.

| # | Use case | Real prompts (of 90) | Category rows it uses | Default ready? |
|---|---|---|---|---|
| 1 | Combine several sources into an algorithm | most of the ~50 "understanding" prompts | research and reports, information extraction | candidate pipeline extract → reconcile → algorithm → verify; a row only after two real runs |
| 2 | Answer a question about existing code ("where is X", "explain Y", "is Z still true") | the rest of those ~50 | repo scanning, information extraction | yes |
| 3 | Fix a bug (logs, reproduce, root cause, fix, rerun) | 7 | debugging, code generation | yes, `debugging` pipeline |
| 4 | Build a feature (plan, design, implement) | 9 | multi step planning, code generation, ui/ux dev | yes |
| 5 | Verify (tests, test data, double-confirm against the spec, grade a run) | 10 | test cases gen, test script gen, test data gen, grade a run | yes |
| 6 | Report and document (status, meeting notes, explain for others) | 5 | document and explain | yes |
| 7 | Review code (own, a teammate's, an agent's) | 3 | code review | yes |
| 8 | Learn something new (outside docs, libraries, tools) | 0 | web search, research and reports | yes |

Out of focus for now (EJ): ship and operate (deploy, CI, environment, incidents) and maintenance (refactor,
dependency upgrades). Neither has a row; one is added when a real task of that kind arrives. Session-control
directives (status, commit, stop) are not a use case: they stay tiny.

#1 is the most frequent and the riskiest: an extracted description is a hypothesis until checked against its
source, and a second LLM read is not a check (`~/skills/verify-extraction`, where a one-line summary of a 70-line
function was wrong in 5 of 6 differential rounds). Its verify step is a differential test for code and a blind
checklist with a planted wrong fact for prose; two disagreeing sources are reconciled with a reason, never averaged.

## Categories

`Touches product` is tri-state: **yes** (every piece writes product), **mixed** (the category runs read-only as
a diagnosis/validation *or* writes as a fix/generation — the design's `builds` flag says which), **no**
(read-only). Round-1 lesson: a binary column made every diagnostic debugging design look like a lie.

| Category | Touches product | Default pattern | Default engine | Default check | Sabotage (proof the check can fail) |
|---|---|---|---|---|---|
| code generation | yes | evaluator–optimizer loop | Codex `gpt-6.1-sol` | tests/build pass (script) | break the code → the check goes red |
| code review | no | maker–checker, fresh blind session | risk-tiered: Sonnet 5.5 when nothing builds; different kind from the worker when it builds (EXECUTOR_KINDS rule 5) | fixed checklist; findings with file:line | plant a known defect → the reviewer must find it |
| ui/ux dev | yes | codegen loop + human acceptance checkpoint | Codex `gpt-6.1-sol` | build/render script + EJ's acceptance (last per 3.5) | break a component → the build fails |
| debugging | mixed | loop with the failing test as objective check (a diagnosis-only run is read-only research with a repro) | Codex `gpt-6.1-sol` | repro test: red before, green after | revert the fix → red again |
| test data gen | mixed | single node, schema-validated (a validation-only run is read-only) | cheap tier (Sonnet 5.5 / `gemini-3.8-flash`) | schema validation + edge-case coverage list | corrupt a row → the validator rejects |
| test cases gen | yes | single node + review | Codex `gpt-6.1-sol` | generated tests fail on a broken implementation | a seeded mutant must be caught |
| test script gen | yes | codegen loop | Codex `gpt-6.1-sol` | script detects a seeded failure | seeded failure → non-zero exit |
| repo scanning | no | parallel sectioning, read-only fan-out | cheap tier | coverage manifest; findings with paths | plant a marker file → the scan reports it |
| multi step planning | no | plan + gate (this method) | Codex `gpt-6-astra` (high thinking) | script schema gate + checklist review | an unresolved spot → the gate fails |
| information extraction | no | single node, structured output | cheap tier | JSON-schema validation + spot-check vs source | a corrupt source field → flagged, never hallucinated |
| web search | no | single node; voting on contested facts | Codex `gpt-6.1-sol` (headless `--search` is an EXECUTOR_KINDS open item) | dated sources with URLs; claims traceable | ask a nonexistent fact → must return not-found |
| classification | no | routing node | agy `gemini-3.1-pro-high` | schema-valid label + agreement on a labeled sample | an ambiguous sample → unknown/escalate, not a forced label |
| research and reports | no | single node, or sectioning + join | Codex `gpt-6.1-sol` | answers the question; every finding carries both-side citations and a CONFIRMED/INFERRED/GAP/UNPROVEN label; missing proof never reads as PASS; join contradiction = stop | seed a known divergence → it must appear as a row with both citations; seed conflicting sources → the join stops |
| document and explain | mixed | single node + review against source | Sonnet 5.5 | fixed checklist against the source; format constraints honored (audience, .txt vs markdown, LF) | remove a fact from the source → the review flags it missing |
| grade a run | no | single node, fixed rubric | Sonnet 5.5 | rubric verdicts kept separate per dimension; run-directory evidence only; missing proof = UNKNOWN/INVALID_RUN, never PASS | grade an empty run directory → INVALID_RUN, not PASS |
| others | — | no default — the full method from first principles | — | — | — |

Step-level, not categories (they are steps inside pieces, or the scheduler itself): **file IO, shell
execution, workflow execution**. Finance is an EXECUTOR_KINDS engine assignment, not a pattern row.

## Labelling rules (round-1 lessons, 2026-10-02)

Measured on 50 executor samples (codex 25, agy 25): strict agreement was 12% / 24% before these rules
existed; every disagreement class traced to a missing definition, not to a weak model.

1. **One label per distinct deliverable — list the deliverables first, then label each.** The primary category
   is the one that answers the ask. Do not add a secondary label for work that is *inside* the primary: a
   research task reads (not also "information extraction"); a debugging diagnosis cites logs (not also
   "research and reports"). Multi-label only when the prompt asks for several *separately delivered* outputs
   ("extract the rules, write them up, then generate test cases" = three deliverables). Dropping a deliverable's
   label is as wrong as adding a passenger label (round-2: combo prompts lost their web-search and
   test-script labels).
2. **Information extraction** applies only when the deliverable *is* the structured data (a table, a schema-
   validated list, field values) — never as a passenger label.
3. **Code review vs research and reports**: review = a verdict on the quality/correctness of work against a
   standard, delivered as an issue report; research = an answer or a findings list. "Compare A to B, list
   divergences with citations" is research; "review this file against the spec, write an issue report" is
   review. **Re-validating an existing finding** against current code ("still open, resolved, or wrong?") is
   research — it updates a findings list, it does not grade work.
4. **Grade a run vs debugging**: grading applies a fixed rubric to a finished run's evidence and stops;
   debugging seeks a root cause. "Which check fired and why" is debugging; "keep the verdicts separate,
   missing proof = UNKNOWN" is grading.
5. **builds=true means the deliverable changes product or test surface** — code, schema, configuration, UI,
   test files, **and generated fixture/seed data that feeds tests or environments** (round-2: fixtures are test
   surface). Findings lists, reports, notes, diaries, command sheets are **not** builds — and neither are
   **deliverable data outputs** (a CSV/JSON table that *is* the answer): a report in data shape is still a
   report (round-3: the gate caught this mislabel on its own corpus author). A `document and explain` piece
   that writes only prose is builds=false even though it writes a file.
6. **tiny + cats=[] is for session-control directives** (status, stop, restate, commit, one-step advice) and
   one-sentence tasks **whose restatement succeeds**: tiny requires the restated problem, fix and check to be
   one sentence each. A prompt you cannot restate ("make it faster", "look into the thing from yesterday") is
   **never tiny** — it is `others` with decision spots. Classifying vague as tiny is the fail-unsafe error: it
   skips the whole method (round-2: the flash tier made exactly this error on 3/3 vague prompts). A standing
   invariant ("do not add fields unless…") is also tiny/[] — it constrains future work, it is not itself a task.
7. **Test cases gen vs test script gen** (round-2, 4 confusions in 50 samples): *cases* = the assertions —
   what behavior is checked, including that content as test code ("extend the unit tests to modules 815–817",
   "add a sabotage case"). *Script* = the machinery that runs things — runners, injectors, drivers, harness
   CLIs, their flags and error reporting ("extend run_e2e.sh with --retry"). If the deliverable would still
   make sense with a different runner, it is cases; if it is about the runner, it is script.
8. **Web search vs research and reports** (round-3): the divider is the *source locus*, not the deliverable
   shape. External sources (the web, vendor docs, "dated sources" from outside) → `web search`, even when the
   output is a report. Material inside the repo → `research and reports`.
9. **Document and explain vs research and reports / code generation** (round-3): when the deliverable is prose
   for a human audience, it is `document and explain` — even when sources must be read first, and even when the
   prose lands in a knowledge file of the repo (writing rules into EXECUTOR_KINDS.md is document and explain,
   not code generation). Research answers a question; a document is made to be read.

## Combination pipelines (seeded)

| Pipeline | Nodes (in order) | Loop sits at | Join check |
|---|---|---|---|
| research → codegen | research, codegen | codegen node | research answered its questions (checklist); else codegen does not start |
| codegen → tests → review | codegen, tests gen, review | codegen node | review checklist against the acceptance criteria |
| debugging | repro, fix, rerun | the whole piece | the repro test |
| scan → report | scan sections, report join | none | coverage manifest complete; contradictions = stop |
| grade → fix → regrade | grade, fix, regrade | the fix node | the regrade verdict on the same rubric; a FAIL surviving the regrade goes to EJ |

New combinations earn a row here only after the ledger shows the ad-hoc version ran twice.

### Candidate pipelines (not rows yet — each earns its row after two real runs in the ledger)

**build a feature (use case #4)** — EJ, 2026-10-02; n=0.

1. **Research — the main agent (COO) herself**, with a research skill, writing findings and a digest to
   `docs/research/` (method 3.8 item 9). Research agents only when there are many main sources (context room) or a
   source needs a different kind (web versus repo).
2. **Design and small examples — the COO.** The design, the acceptance criteria in scope, and the briefs for the
   next two nodes, each with a template, a worked example and the standard (method 3.8 item 8).
3. **Dev ∥ tester, in parallel** (passes the five tests of method 3.7: one shared input, different deliverables,
   separate paths).
   - *Dev* (the row's coder, Codex `gpt-6.1-sol`): implements and writes unit tests.
   - *Tester* (a different kind from the dev, EXECUTOR_KINDS rule 5): writes the test plan and test cases from
     the design and acceptance criteria only, blind to the dev's code. Its cases are first run against a
     deliberately broken build and must fail there (sabotage), or they are not used.
4. **COO review, one round, before the tester runs.** A fixed checklist, not an open read: the dev's unit tests
   pass; the baseline still passes; nothing in "must not change" changed; the result matches the design's
   examples. She may read the diff only when the feature is small by her small-node conditions.
5. **Tests run → findings to the COO.** A small issue (her small-node conditions and 8-tool-call cap,
   `docs/EXECUTOR_KINDS.md`) she fixes herself and sends back to the tester to rerun. A big issue goes back to the
   dev, at most **2 rounds**, then the tier exit or EJ. Findings outside the acceptance criteria go to the
   backlog, not into this run.

Join check: the tester's cases (proven able to fail) pass, the baseline still passes, "must not change" holds —
the three-part stop of method 3.6. Feedback: `runlog.py` wraps the dev and tester calls and logs each verdict
(method 3.8 item 10).

**Lead-in by case (EJ, 2026-10-03; n=0).** Steps 3–5 above are the same in every case. Steps 1–2 and the
tester's oracle depend on where the truth comes from:

| Case | Source of truth | Lead-in (before anything builds) | Tester's oracle | Main risk |
|---|---|---|---|---|
| A. Requirements not clear | EJ, through questions | Requirements discovery: one batch of questions, each with a provisional answer; the COO drafts R-blocks with acceptance criteria; EJ accepts them. Examples or a throwaway prototype may help EJ decide. No piece builds until requirements are settled (method 3.1, blueprint check). | The criteria EJ accepted | Building the wrong thing |
| B. Clear, migrating from an old system | The old system's behaviour | Extract the old behaviour (use case #1): its algorithm from the old code, confirmed by a differential test against the old system, never by re-reading (`~/skills/verify-extraction`); record golden input/output pairs from the old system. | Parity: the same inputs give the same outputs on old and new, plus data-migration checks | A plausible but wrong description of the old system |
| C. Clear, new feature on an existing system | The existing code plus the new requirement | Scan and understand the system (use case #2 at scale): a map of the affected areas and extension points, and the regression baseline recorded before any change. | The new criteria, plus "the baseline still passes" | Breaking something not known to be connected |
| D. Feature for a new system | EJ's blueprint | All eight blueprint sections settled first (vision, requirements, domain, logic, architecture, data, UI, non-functional), then scaffolding. | The criteria; there is no baseline yet | Architecture decided too early or too vaguely |

A run names its case in the restatement (method 3.0) and checks it against the facts at readiness: an existing
codebase is never case D, and a case-B run with no access to the old system is not ready.

**combine sources into an algorithm (use case #1)** — extract → reconcile → algorithm → verify, as described under
"Use cases in focus"; n=0.

**Recheck verbs get their own node.** When the prompt says "then regrade", "rerun afterwards", "verify after
the fix", the design must show the recheck as its own node (or an explicit loop) — a design that folds it into
the fix node was rejected by the round-3 blind review (p279). The script gate cannot see this; the checklist
layer exists for exactly this class.

## The design JSON the gate reads

```json
{
  "categories": ["research and reports", "code generation"],
  "builds": true,
  "touched_paths": ["ancient_games/x.py"],
  "pipeline": "research → codegen",
  "nodes": [{
    "id": "n1", "category": "code generation", "engine": "codex gpt-6.1-sol",
    "check": "pytest -q green", "needs": [],
    "loop": {"limit": 2, "exit": "fresh node, stronger tier, handoff note", "feedback": "the check's real output"},
    "five_things": ["tools", "context", "contract", "evidence", "state"]
  }],
  "design_source": "default",
  "estimate": {"tokens": 100000},
  "default_estimate": {"tokens": 130000},
  "coverage": {"criteria": ["R1.1"], "checks": ["pytest -q"]},
  "default_coverage": {"criteria": ["R1.1"], "checks": ["pytest -q"]}
}
```

`design_source` is `"default"` or `{"type": "challenger", "claim_margin": 0.25, "basis": "..."}`.
`default_estimate`/`default_coverage` are required for challengers only. A review node may carry
`"reviews": ["<worker id>", …]` pairing it with the workers it verifies — G6 then demands a different engine
kind from *those* workers (a reviewer of a multi-kind group is checked against the pure builders). Without
the field, a reviewer is checked against every builder. A build group spanning engine kinds **splits its
review**: one reviewer per kind group, since no single reviewer can be different-kind from both (round-3,
p195/p273). Gate findings are named G1–G7;
run `python3 .claude/skills/workflow-design/scripts/design_gate.py design.json` (or `--self-test`).

## Provenance

Added 2026-10-01 at EJ's request: categorize at intake, default pattern per category, the 20% challenger rule
after "ask 3 times get 3 different answers", script gate + Sonnet 5.5 checklist review of the decision. n=0 —
the ledger is how it earns evidence. Test corpus: `tests/fixtures/task_type_prompts.json` (16 prompts in EJ's
voice, expectations are provisional working values for EJ to correct).
