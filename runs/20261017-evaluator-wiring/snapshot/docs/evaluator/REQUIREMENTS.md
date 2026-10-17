# Requirements evaluator — requirements

> **Status: accepted by EJ on 2026-10-13** (EJ: *"accept as you suggest, go"*; the five open items settled as proposed, below). Written 2026-10-13 by the COO (Claude `claude-opus-5-5`), as piece D1 of run
> `runs/20261013-requirements-evaluator/`. Nothing builds against this file until EJ accepts it (method 3.1).
>
> **Sources.** Each requirement names one:
> - **(EJ)** the challenge, or EJ's answers Q1–Q4 in the run's `state.md`;
> - **(d)** the run's `workflow-design.md`, by step E1–E10;
> - **(r)** run `runs/20261012-index-md-build/`, by node;
> - **(v)** `VISION.md`.
>
> **Levels.** **MUST** is a gate that stops a verdict being trusted. **SHOULD** is a default that may be overridden
> with a stated reason. Only the safety bounds of the verdict are MUST (RFC 2119 §6: a method does not earn MUST).
> *Proposed* marks wording EJ has not decided. There are no invented numbers: where a limit applies, calibration
> measures it.
>
> **Categories** (accepted by EJ, 2026-10-13): **EV-R — Read** (what goes in), **EV-C — Check** (how each requirement is checked),
> **EV-P — Report** (what comes out).
>
> **Words** (one word, one job):
> - a **requirement** is an id in the product's REQUIREMENTS, or a vision line under Q3;
> - a **failure case** is one case named in a requirement group's **Fails if** line;
> - a **probe** is an executable check of one failure case;
> - a **mutant** is a copy of the product broken for one failure case.

## EV-R — Read: what goes in

**EV-R1 — The spec** (EJ Q1, Q3; d E1)
- **EV-R1.1** MUST. It reads the product's REQUIREMENTS file and lists every requirement id. A requirement group's
  **Fails if** line is split into its failure cases, each tied to the group's ids. A requirement the file marks
  *open* is listed as out of scope, with that reason.
- **EV-R1.2** MUST. It reads the product's VISION file, and only the lines under **"What it will never do"** and
  **"How we know it works"**. Each becomes a requirement with an id `V<n>` (EJ, Q3). Other vision lines are context
  and get no verdict.
- **EV-R1.3** MUST. A requirement group with no **Fails if** line is listed as **untestable**, with that reason. It is
  never dropped.
- **Fails if:** an id in the file is missing from the list; an open requirement gets a verdict; a group without
  **Fails if** disappears; or a vision line outside Q3 gets a verdict.

**EV-R2 — The blind workspace** (d E2; v "never read the builder's tests")
- **EV-R2.1** MUST. Every step that uses a model sees only a workspace holding the product's code and its spec. It
  holds no test files of the product, no run folders, no git history and no build notes.
- **EV-R2.2** SHOULD. Which paths count as "the product's tests" is given per product as globs, defaulting to
  `tests/`. *Proposed:* the default is the COO's.
- **Fails if:** a marker file planted in the product's tests appears in the workspace or in any model step's input.

**EV-R3 — The input contract** (EJ Q1, Q2)
- **EV-R3.1** MUST. It is run as `.claude/workflows/evaluate-requirements.js` with `{product, spec, runId}`:
  - `product` is the product's folder at a named commit;
  - `spec` is the folder holding VISION and REQUIREMENTS;
  - `runId` names `runs/<runId>/`.
- **EV-R3.2** MUST. It writes only inside `runs/<runId>/`. The product is never changed (v).
- **Fails if:** a run changes any file outside `runs/<runId>/`, or runs without one of the three arguments.

## EV-C — Check: how each requirement is checked

**EV-C1 — The kind of check** (d E3)
- **EV-C1.1** MUST. Each failure case gets exactly one kind:
  - *executable*: a probe can run it;
  - *static*: inspecting files or config can tell;
  - *judged*: only reading code against the sentence can tell;
  - *human*: only EJ can tell.
- **EV-C1.2** MUST. The classifier gives a reason for every label. A label without a reason counts as not
  confident, and the case becomes *human*, never a forced label (EJ, 2026-10-13, accepting the proposal).
- **Fails if:** a case has no kind or two kinds, or a planted ambiguous case is given a non-human kind.

**EV-C2 — Probes** (d E4; r N1)
- **EV-C2.1** MUST. Probes are written from the spec only, in the blind workspace. Each cites its failure case id.
- **EV-C2.2** MUST. Every executable and static case has at least one probe, or the case is UNKNOWN with the reason
  "no probe".
- **Fails if:** a probe cites no case; an executable case has no probe and no UNKNOWN; or the probe writer's input
  holds a product test file.

**EV-C3 — Mutants, and the proof a probe can fail** (d E5, E6; r N3)
- **EV-C3.1** MUST. Each executable or static case has a mutant: a copy of the product broken for that case. It is
  written by a **different engine kind** from the probe writer, which never sees it.
- **EV-C3.2** MUST. Every probe is run against every mutant. A probe that stays green on its case's mutant is
  **unproven**, and its case cannot be PASS.
- **EV-C3.3** MUST. The product is restored byte for byte after each mutant, and the run checks it by hash.
- **Fails if:** a case is PASS while its probe is green on its mutant; the probe writer and the mutant writer are the
  same kind; or the product's hash differs after the matrix.

**EV-C4 — Confirming a failure** (d E8; r N2's defective test)
- **EV-C4.1** MUST. A probe that is red on the real product is shown to a fresh agent with the requirement's sentence
  and the probe's output. That agent answers **faithful** or **not faithful**, quoting both.
- **EV-C4.2** MUST. Only a faithful red probe makes a FAIL. A probe that is not faithful makes the case UNKNOWN and
  gets one repair round (EJ, 2026-10-13, accepting the proposal; basis n=1, the INDEX.md run).
- **Fails if:** a FAIL stands on a probe that was not confirmed, or a planted unfaithful probe produces a FAIL.

**EV-C5 — Judged cases** (d E9; r N4)
- **EV-C5.1** MUST. Judged cases are decided on a fixed checklist with quoted file:line evidence, by an engine kind
  different from the product's builder where that is known.
- **EV-C5.2** MUST. The judge's copy holds one planted defect for a judged case. If the judge misses it, that judging
  is void: its cases are UNKNOWN, and it is rerun once in a fresh session with a different plant.
- **Fails if:** a judged PASS stands after the plant was missed, or a judged verdict has no quoted evidence.

**EV-C6 — Engines** (`docs/EXECUTOR_KINDS.md`; d)
- **EV-C6.1** SHOULD. Each model step names its engine, model and effort in the run's plan. The defaults (accepted by EJ
  2026-10-13; n=0, checked in calibration) are:
  - classify: a Claude Haiku subagent (D0: DeepSeek has no verified one-shot call here);
  - probes: a Claude subagent;
  - mutants: Codex `gpt-6.1-sol`;
  - confirm and judge: a fresh Claude Sonnet 5.5 session, or Codex when the product was built by Claude.
- **EV-C6.2** MUST. A failed engine call (no result, an empty result, a timeout, or a wrong model) blocks that step
  and reports it. There is no fallback engine.
- **Fails if:** a step runs on an engine its plan did not name, or a blocked step produces a verdict.

## EV-P — Report: what comes out

**EV-P1 — The verdict** (EJ; v; d E10)
- **EV-P1.1** MUST. Each in-scope requirement gets exactly one verdict:
  - **PASS:** every one of its cases has a probe that is green on the product and red on that case's mutant, or a
    judged yes from a judging whose plant was found;
  - **FAIL:** at least one case has a confirmed failure;
  - **UNKNOWN:** anything else, with the reason.
- **EV-P1.2** MUST. **MEETS** only when every in-scope requirement is PASS. One FAIL or one UNKNOWN means not MEETS.
- **EV-P1.3** MUST. The verdict is computed by a script from the recorded results, never written by a model.
- **Fails if:** a requirement with no evidence is PASS; MEETS is given with an UNKNOWN; or a model's text is the
  verdict.

**EV-P2 — The report files** (d; method 3.8 item 4)
- **EV-P2.1** MUST. A run writes:
  - `verdict.json` (machine-read);
  - `verdict.md` (one row per requirement: verdict, its cases, the evidence path, and for a FAIL the repro command);
  - a coverage manifest listing every id read in EV-R1.
- **EV-P2.2** SHOULD. `verdict.md` begins with the overall answer and the counts, then the FAILs, then the UNKNOWNs
  with their reasons, then the PASSes.
- **Fails if:** an id read in EV-R1 is missing from the manifest, or a FAIL row has no repro command.

**EV-P3 — Cost** (d D5; non-functional)
- **EV-P3.1** SHOULD. Each run records its model calls, tokens as each engine reports them, and wall time. A missing
  count is written as *not reported*, never 0.
- **Open:** the cost and time an evaluation run may take. Calibration measures them first; EJ sets any limit after
  that.
- **Fails if:** a run records 0 tokens for an engine that reported none.

## Requirement check (the eight questions, run by the COO on each group)

| Group | Source | One thing | Unit | Can it fail | Weak words | Level | Basis | Links |
|---|---|---|---|---|---|---|---|---|
| EV-R1 | pass | pass | n/a | pass | pass | pass | quoted (EJ Q1, Q3) | none |
| EV-R2 | pass | pass | n/a | pass | pass | pass (R2.2 SHOULD) | design; **R2.2 default is mine** | none |
| EV-R3 | pass | pass | n/a | pass | pass | pass | quoted (EJ Q2) | none |
| EV-C1 | pass | pass | n/a | pass | pass (settled: a reason per label) | pass | design | none |
| EV-C2 | pass | pass | n/a | pass | pass | pass | run N1 | none |
| EV-C3 | pass | pass | n/a | pass | pass | pass | run N3 | none |
| EV-C4 | pass | pass | **"one round"** | pass | pass | pass | run N2; **the 1 is mine** | none |
| EV-C5 | pass | pass | n/a | pass | pass | pass | run N4 | none |
| EV-C6 | pass | pass | n/a | pass | pass | pass (C6.1 SHOULD) | **defaults are mine**, n=0 | EXECUTOR_KINDS |
| EV-P1 | pass | pass | n/a | pass | pass | pass | EJ; grade-a-run row | none |
| EV-P2 | pass | pass | n/a | pass | pass | pass | method 3.8 item 4 | none |
| EV-P3 | pass | pass | **open** | pass | pass | pass | design | none |

## Open, for EJ — settled 2026-10-13 (*"accept as you suggest"*)

Items 1, 2, 3 and 5 are settled as proposed. Item 4 stays open by that answer: calibration measures first.

1. **EV-C1.2, "with confidence":** the weak word stays until calibration shows how the classifier signals doubt.
   *Proposed:* the classifier must return a reason for each label, and a label with no reason counts as no
   confidence.
2. **EV-C4.2:** is one repair round right for an unfaithful probe? The INDEX.md run used one.
3. **EV-C6.1:** are the engine defaults right? They are mine, n=0.
4. **EV-P3:** the cost and time limits, after calibration measures them.
5. **The categories, Read / Check / Report:** proposed.
