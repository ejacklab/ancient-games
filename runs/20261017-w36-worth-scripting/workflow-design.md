# Workflow design — 20261017-w36-worth-scripting

A design, not a run. Sequential. Method: `docs/WORKFLOW_DESIGN_METHOD.md`. Written 2026-10-17 by the COO
(`claude-opus-5-5`) at EJ's request: *"design a workflow to use the 6 experts to research and fix item 13"*. State:
`state.md`. Nothing here has run.

## Questions for EJ

| # | Question | Provisional assumption | Blueprint section |
|---|---|---|---|
| Q1 | How much time does the run have? (The harness asks for it; the steps check the clock.) | 45 minutes | none |
| Q2 | Who makes the final call on the W3.6 wording: you, after reading the experts, or the experts' majority, with you able to overrule after? | you decide, then the COO applies and pushes in the same step | the design (W3.6) |

## Restatement (method 3.0)

**Objective.** TODO item 13's open point is settled and written into W3.6: *may a procedure a script could do stay a
`docs/` page because it runs rarely, and who decides that?* Settled means a rule an agent can apply, with no invented
threshold, and the design's checks still passing.

**In scope:** the question, web research on it, the six experts, W3.6 in `SOURCE_OF_TRUTH_REQUIREMENTS.yaml` (through
`runs/20261014-sot-yaml-review/build_requirements.py`), the prose sentence on procedures in `SOURCE_OF_TRUTH.md`, the
release note, the state file. **Out of scope:** every other TODO item; the `procedure-to-skill` skill; measuring
how often procedures run.

**Whys.** (1) Problem: W3.6 says a procedure is a script unless a step *cannot* be scripted; it says nothing about a
procedure that *could* be scripted but is not worth it, so an agent either scripts every one-off or invents its own
reason. (2) Now: W3.6 was just settled for "cannot"; Linus and 孫子 raised "worth it" in the same round. (3) Shape: one
decision, needing outside knowledge (when automation pays) and judgement. (4) Failure: low; a SHOULD, nothing is live.
(5) Stop: at the one sentence (or two) in W3.6. (6) Done: EJ accepts the wording; the checks pass.

**Provisional category** (*inferred*): decision with research — the `experts-decide` workflow is its runnable form.

## Blueprint

- Kind: fix to the design document (EJ's product). Acceptance: W3.6 answers "worth it" and "who decides" with no
  invented number (EJ's rule: a trigger is a comparison, never a threshold asked for up front); the YAML's build
  script, `checks/yaml_check.py` and `checks/paths.py` (in `runs/20261015-sot-leftovers/`) pass.
- Baseline: the three checks pass today (2026-10-16, after `9441faa`).

## The algorithm (method 3.2)

| # | Step | Check |
|---|---|---|
| 1 | Research from the web: when does scripting a procedure pay off, and what happens to rarely-run scripts and rarely-run docs (drift, rot)? | each finding labelled verified (source opened) or unverified, with its link |
| 2 | Six experts, one round, on the question with the research added | `six_experts.py check` per expert; one rerun for an expert with no usable answer; `compare.md` |
| 3 | The COO writes one proposed W3.6 wording from the comparison, with each expert's own wording beside it | EJ picks or edits it (Q2) |
| 4 | Apply: W3.6 text, `fails_if`, `who_decides`; the prose sentence; a release-note entry; the state | the three checks pass; commit and push in the same step (EJ, 2026-10-16) |

## Pieces, in the order they run

### P1 — Research and experts (the saved `experts-decide` workflow)
- **Steps:** steps 1 and 2, as one run of `.claude/workflows/experts-decide.js` with
  `{run: "runs/20261017-w36-worth-scripting", question: "runs/20261017-w36-worth-scripting/question.md",
  out: "experts", needsWeb: true, research: "<the research question in step 1>"}`.
  - `needsWeb: true` because the research is from the web; 范蠡 then runs on Claude, since agy headless cannot use
    the web (the skill's rule).
  - Not `approveOrChange`: the answer is an open choice, not APPROVE/CHANGE on a fixed text.
  - No `insights` named: Dave chooses from the insight index himself.
- **Pattern:** the workflow's own: research once, ask each expert (老子 alone, after the others, because opencode
  cannot run twice at once), check each, rerun once, compare.
- **Check:** the workflow's — `six_experts.py check` per expert (written by Claude: it checks sections and citations,
  not whether a rule was applied well); research findings labelled. **Exit:** the workflow returns `time_up` when the
  clock runs out; then the COO reports what came back.
- **Context — given:** `question.md`, with the research added by the workflow. Every file it cites is inside the
  repo (the skill it quotes is copied to `sources/`). **Withheld:** this design, the COO's draft wording.
- **Evidence:** `research/experts.md`, `experts/<id>/`, `experts/compare.md`, `nodes/experts.progress.md`.
- **Role and engine:** the workflow's agents; the experts on their own engines (Linus codex or mcode, 范蠡 Claude,
  孫子 dsh, 老子 opencode, Dave Claude Opus, Dario Claude Sonnet).

### P2 — Proposal and decision
- **Steps:** the COO reads `compare.md`, writes one proposed wording with the experts' own beside it, and gives it to
  EJ with the agreement and disagreement shown side by side, never averaged.
- **Check:** EJ (Q2). **Role:** the COO; EJ decides.

### P3 — Apply and close (COO)
- **Steps:** edit W3.6 in `build_requirements.py` (text, `fails_if`, `who_decides`), rebuild the YAML, edit the
  prose sentence, add a release-note entry, strike item 13 in `runs/20261014-sot-yaml-review/state.md`, commit and
  push (only the files this run changed).
- **Check:** script — the build script, `yaml_check.py`, `paths.py` (all shown able to fail in run
  `20261015-sot-leftovers`). **Must not change:** any other record, any other doc.
- **Evidence:** the checks' output in `nodes/p3.result.md`.

## Joins

P2 reads every expert answer and the research together; a disagreement goes to EJ with both sides quoted.

## Parallel candidates

None: each piece needs the one before it. Inside P1, the workflow runs five experts together and 老子 after.

## Predictability

- Agents: 1 research agent, 6 experts (at most 6 more on reruns, one each), 1 compare agent, plus the workflow's
  check steps on a small model. The COO does P2 and P3.
- Cost (*not measured*; from earlier runs): the experts take about 5–15 minutes of wall time (run
  `20261016-w36-procedure-script`: about 10 minutes for five); research one web agent; P3 a few minutes. Total about
  30–45 minutes, inside Q1's time.
- Success criteria, written before the run: W3.6 answers "worth it" and "who decides" with no invented number; EJ
  accepts the wording; the three checks pass.

## Debuggability

Labels research, ask:<id>, check:<id>, compare (the workflow's), then p2, p3. Files as listed. Resume point: the
workflow's progress file and `state.md`. Every change is in one commit.

## Quality control

- Script: the three design checks; `six_experts.py check`. Judged: the experts (advice only). EJ's: the wording.
- Experts on this design's unclear spots (method 3.3): **not asked** — the run itself is a six-expert review of the
  one open question; a round on its design would cost a second round for a two-step workflow.
- **The three qualities:** predictability — the bounds and estimate above; debuggability — the workflow's per-step
  files and one commit; quality control — every check named, EJ decides.
