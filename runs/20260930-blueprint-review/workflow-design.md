# Workflow design — 20260930-blueprint-review

A design, not a run. Nothing here has been executed (n=0). Sequential by default. Method:
`docs/WORKFLOW_DESIGN_METHOD.md`. Engines, models and the COO: `docs/EXECUTOR_KINDS.md`.

**The task.** After a renewal of the product's vision, core requirements, user workflows and early UX, review three
blueprint sections that depend on them and on each other: **non-functional requirements (8), system architecture (5),
data model/schema (6) with UI design (7)**. Output is findings and proposed edits. The run edits no blueprint file.

## The mutual-dependency problem, and how the design cuts it

The sections feed each other (8 → 5 → 6/7, with 5, 6 and 7 pushing back on 8 and on each other). An open-ended
"review until consistent" loop never closes (method 3.5, n=1). So:

1. **One fixed first pass**, in the order the method already gives: 8, then 5, then 6, then 7. Each is reviewed against
   the sections above it, as they stand.
2. **A scripted cross-check** (the join) that finds every place two sections disagree, using ids and a trace table,
   not opinion.
3. **A contradiction is a stop, not averaged** (3.3, 3.6). It goes to EJ as a decision, with both sides and the ids.
4. **At most 2 reconcile rounds**, and only for artifacts an EJ decision actually changed. The check is the same
   script; a round closes when the script reports no contradictions. On the limit, the rest goes to EJ.

## Questions for EJ (answer before running; a blueprint question holds back only the pieces that build on it)

| # | Question | Provisional assumption | Blueprint section |
|---|---|---|---|
| Q1 | Which product, and where is its blueprint map? (Ancient Games has no `docs/blueprint/`.) | Some product with `docs/blueprint/README.md`; the run starts by finding it and stops if absent | all |
| Q2 | Were domain model (3) and business logic (4) renewed too? They sit upstream of 5, 6 and 7 and are not in your list | Not renewed. They are read as inputs; the run checks them against the new 1–2 lightly (P1) and sends what looks stale to you, without reviewing them in full | domain, business logic |
| Q3 | Where do "user workflows" and "early UX" live? The blueprint has no user-workflow section | Workflows are in section 2 (requirements) or 7 (UI/UX), early UX is a draft of 7. If 7 is the renewed draft, then "review UI design" reviews that draft against 2 and 4 | requirements, ui/ux |
| Q4 | Are the renewed sections 1 and 2 accepted (dated in their files)? | Yes. If they are draft, the run still works (it is research/design), but its findings name the drafts assumed and nothing built from it may start | vision, requirements |
| Q5 | Findings and proposed edits only; the run changes no blueprint file? | Yes. You accept edits afterwards, as the method says | none |
| Q6 | Reconcile rounds: 2? Cap on COO-done nodes: 8 tool calls? (both my guesses) | 2 and 8 | none |
| Q7 | May `agy` be used as a verifier? Google's terms on headless `agy` are unresolved (`EXECUTOR_KINDS.md`, Open) | No. Verifiers are fresh Claude subagents, or Codex in a fresh session | none |

## Blueprint

- Kind of task: **not a product change.** It reviews the blueprint documents and edits no code, schema, UI or
  configuration. If a finding calls for a change to code, schema or UI, that is a separate task and gets its own
  blueprint check. No acceptance criteria (R/N ids) apply to this run.
- Map: per Q1. Baseline: none for a product's tests (nothing builds). The run's own baseline is
  `git status --short`, taken before the run folder exists, so the final check can show the run touched only
  `runs/<runId>/`.
- **Run criteria** (written before the run, observable; these are this run's success, not R-ids):
  - C1 every requirement changed by the renewal is listed in `delta.md`, and every one is traced to the sections
    that cite it or is marked "untraced";
  - C2 every N-criterion has a number, a way to measure it, and a source requirement, or is a finding;
  - C3 every N-criterion has an owning architecture decision, or is a finding;
  - C4 every architecture decision cites an N or R id, or is a finding (a line that serves nothing above it);
  - C5 the cross-check reports zero open contradictions, or each open one is a decision with EJ;
  - C6 the final pass finds nothing beyond C1–C5 that fails them; anything else goes to `docs/blueprint/backlog.md`
    of the product, not into this run.

## Pieces, in the order they run

All pieces are docs-only, so none **builds**. Each carries the five things (tools, context, contract, evidence,
state). Engine names follow `EXECUTOR_KINDS.md`: Codex default `gpt-6.1-sol`, high thinking `gpt-6-astra`; verifiers
are fresh sessions and never see the worker's reasoning. "COO" is the main Claude session doing the node herself
under the four conditions and the cap.

### P0 — Find the blueprint, canary, baseline

- **Steps:** 1. Locate `docs/blueprint/README.md` (Q1) and the six section files. 2. Canary for Codex (method 3.1,
  `EXECUTOR_KINDS.md`): record version and model. 3. Take `git status --short`.
- **Pattern:** step. **Builds:** no. **Depends on blueprint sections:** none (reads the map).
- **Check:** script — files exist; canary `pass`; log line `canary codex <version> pass: …`. Sabotage: run the
  canary once on an impossible task and confirm it reports `fail` (house rule).
- **Attempt limit:** 1; a failure is blocked and goes to EJ. **Needs the result of:** none.
- **Role and engine:** COO herself (a few commands, objective check) — model: her own. The canary itself runs Codex.
- **Contract — returns:** `readiness.md` filled; `state.md` updated. **May change:** `runs/<runId>/`. **Must not
  change:** anything else.
- **Evidence:** the command outputs, saved in `readiness.md`. **State:** reads nothing; writes step status, the
  Codex version, the baseline.
- **Context — given:** this design. **Withheld:** n/a.

### P1 — Renewal delta

- **Steps:** 1. From git history of sections 1, 2 and (per Q3) workflows and early UX, list every changed or new
  heading and R-id (script: `git diff` between the last accepted version and now). 2. An agent writes one line per
  change: what changed, and which sections 3–8 it could affect. 3. A light check of 3 and 4 against the new 1–2
  (Q2): listed, not reviewed.
- **Pattern:** step. **Builds:** no. **Depends on:** vision, requirements (Q4 status recorded).
- **Check:** script — every heading and R-id in the git diff appears in `delta.md` (C1, first half). Judged by the
  verifier: each "could affect" line names a section that exists.
- **Attempt limit:** 2. **Feedback on failure:** the ids the script found missing. **Exit when the limit is hit:**
  to EJ.
- **Role and engine:** analyst, Codex `gpt-6.1-sol`, default effort. Verifier: Claude subagent, fresh, sees only
  `delta.md` and the git diff.
- **Contract — intent:** scope the review to what the renewal actually changed. **Stop:** the script passes and the
  verifier passes. **Returns:** `p1-delta.md`: table of change id, what changed, sections possibly affected.
  **May change:** `runs/<runId>/p1-*`. **Must not change:** blueprint files.
- **Evidence:** the git diff command and its output, saved in `p1-evidence.txt`. **State:** reads `readiness.md`;
  writes the list of change ids.
- **Context — given:** sections 1–2 (old and new), map. **Withheld from verifier:** the analyst's reasoning.

### P2 — Trace table (script)

- **Steps:** 1. Build a table from the blueprint's ids: R-ids, N-ids, architecture decision ids or headings, schema
  tables and columns, UI screens and fields, and which of them cite which. 2. Mark dangling and orphan links.
- **Pattern:** step. **Builds:** no. **Needs the result of:** P1.
- **Role and engine:** COO herself if the ids are machine-readable (script); otherwise a Codex `gpt-6.1-sol` node
  writes the extraction script and the COO runs it.
- **Check:** script — every id cited in a section exists, and the table is regenerated identically on a second run.
  The sabotage: delete one id from a copy and confirm the script flags it.
- **Attempt limit:** 2. **Exit:** to EJ (the blueprint may not be in a checkable form, which is itself a finding).
- **Contract — returns:** `p2-trace.csv` and `p2-gaps.md`. **Must not change:** blueprint files.
- **Evidence:** the script and its output. **State:** writes the path of the table and the count of gaps.

### P3 — Review NFR (section 8)

- **Steps:** 1. For each N-criterion: a number, a way to measure, a source requirement (C2). 2. For each changed
  requirement from P1: does it need a new or changed N? 3. For each N: does it rest on a domain fact or a business
  rule that the renewal may have changed?
- **Pattern:** step (one attempt, then verifier). **Builds:** no. **Needs the result of:** P1, P2.
- **Check:** a fixed checklist, judged by a separate agent: the three questions above, per N-id, each answer citing
  a file and line. Not an open-ended review.
- **Attempt limit:** 2. **Feedback:** the checklist items failed. **Exit:** to EJ.
- **Role and engine:** reviewer, Codex `gpt-6.1-sol`. Verifier: Claude subagent, fresh; may see the checklist and
  the cited lines, not the reviewer's reasoning.
- **Contract — returns:** `p3-nfr-findings.md`: per finding: id, what is wrong, evidence, proposed edit text.
  **May change:** `runs/<runId>/p3-*`. **Must not change:** blueprint files.
- **Evidence:** file:line per finding, saved in the findings file. **State:** writes count of findings by id.
- **Context — given:** sections 1, 2, 3, 4 (as inputs), 8; `p1`, `p2`. **Withheld:** sections 5–7 (so this review
  does not bend the NFRs to the architecture that exists).

### P4 — Review architecture (section 5)

- **Steps:** 1. Each N-criterion has an owning decision, or an argument that the design meets it (C3). 2. Each
  decision cites an N or R id (C4). 3. Boundaries follow the domain (3) and the rules that need one transaction (4).
- **Pattern:** step. **Builds:** no. **Needs the result of:** P3.
- **Check:** as P3, a fixed checklist with citations, judged by a fresh agent.
- **Attempt limit:** 2. **Exit:** to EJ.
- **Role and engine:** reviewer, Codex **`gpt-6-astra`** (wrongness here is costly; high thinking is chosen on
  purpose). Verifier: Claude subagent, fresh.
- **Contract, evidence, state:** as P3, files `p4-*`. **Context — given:** sections 2, 3, 4, 5, 8, `p1`–`p3`.
  **Withheld:** sections 6–7.

### P5 — Review data model / schema (section 6)

- **Steps:** 1. Every domain entity and rule from 3–4 has a table, column or constraint. 2. Every architecture
  ownership claim from 5 is where the schema puts the table. 3. Every performance, privacy and audit N-criterion has
  an index, copy, delete mechanism or history table, or is a finding.
- **Pattern:** step. **Needs the result of:** P4. **Check:** checklist with citations, fresh agent. **Attempt limit:**
  2. **Exit:** to EJ.
- **Role and engine:** reviewer, Codex `gpt-6.1-sol`; verifier Claude subagent, fresh. Files `p5-*`.
- **Context — given:** sections 3, 4, 5, 6, 8, `p3`, `p4`. **Withheld:** section 7.

### P6 — Review UI design (section 7)

- **Steps:** 1. Every user workflow and R-id changed by the renewal has a screen or flow. 2. Every business rule shows
  up as UI behaviour (enabled, message, required). 3. How each screen gets its data fits the architecture (5).
  4. Accessibility and device N-criteria are met by named components or are findings.
- **Note:** 4 steps, one over the usual 3. Kept together because the parts share one context and one check.
- **Pattern:** step. **Needs the result of:** P4 (not P5, so P5 and P6 are independent; see Parallel candidates).
  **Check:** checklist with citations, fresh agent. **Attempt limit:** 2. **Exit:** to EJ.
- **Role and engine:** reviewer, Codex `gpt-6.1-sol`; verifier Claude subagent, fresh. Files `p6-*`.
- **Context — given:** sections 2, 4, 5, 7, 8, workflows/early UX per Q3, `p1`, `p2`, `p4`. **Withheld:** section 6.

### P7 — Cross-check (the join)

- **Steps:** 1. Run the scripted checks over the artifacts and P2's table: (a) every UI field maps to a schema
  column with the same type, required-ness and constraints; (b) every business rule appears in a schema constraint
  and in UI behaviour; (c) every N-criterion has an owner (C3); (d) every architecture decision cites an id (C4);
  (e) data ownership in 5 agrees with table locations in 6; (f) no dangling ids. 2. List each failure as a
  contradiction with both sides and ids.
- **Pattern:** step. **Needs the result of:** P3, P4, P5, P6. **Builds:** no.
- **Check:** the script itself; sabotage: alter one column type in a copy and confirm (a) fires.
- **Attempt limit:** 1 (it is deterministic). A failing check is not retried; it is a finding.
- **Role and engine:** COO herself runs the scripts. If any check needs a judgment (which field is "the same" as
  which column), a Codex `gpt-6.1-sol` node proposes the mapping and a fresh Claude subagent verifies it; the
  script then compares.
- **Contract — returns:** `p7-contradictions.md`: table of id, side A (file:line), side B (file:line), why they
  disagree. **Stop:** zero rows, or each remaining row is marked "decision needed". **Evidence:** the script and its
  output. **State:** writes count of open contradictions.

### P8 — EJ decisions, then bounded reconcile

- **Steps:** 1. The COO batches P7's contradictions and the findings from P3–P6 into one list of questions for EJ,
  each with a provisional proposal. 2. After EJ answers, the pieces whose artifacts an answer changed are
  re-reviewed (only those), then P7 runs again.
- **Pattern:** loop, **at most 2 rounds** (Q6). Check: P7's script, objective. Feedback: its real output.
- **Exit when the limit is hit:** the remaining contradictions go to EJ as open, not to a third round.
- **Role and engine:** COO herself distributes and monitors; re-reviews use the same roles as P3–P6, in fresh
  sessions.
- **Contract — stop:** P7 reports zero, or EJ has ruled on each remaining row. **May change:** `runs/<runId>/`. The
  blueprint files are edited only by EJ, or by a blueprint piece EJ accepts afterwards.
- **State:** writes round number and the count of open contradictions after each round.

### P9 — What is missing (final pass)

- **Steps:** 1. A fresh Codex `gpt-6-astra` reviewer reads the outputs of P1–P8, measured against C1–C6 only.
  2. Anything else it finds goes to the product's `docs/blueprint/backlog.md` with the date and run id (or, for this
  run, to `p9-backlog.md` until EJ approves the write).
- **Pattern:** step. **Check:** a fixed list (C1–C6): met, not met, with evidence. **Attempt limit:** 1.
- **Contract — returns:** `report.md`: for each criterion, met or not, the evidence, and the list of decisions
  still open. Ends with "not checked" items, listed honestly (Rule 8).
- **Context withheld:** the earlier reviewers' reasoning.

## Joins

P7 is the join for 5, 6 and 7. P8 is the only place a contradiction can be settled, and only by EJ. Nothing is
averaged.

## Parallel candidates (decided last)

| Pieces | Neither needs the other's result | No shared files or resources | One would not change how the other is done | Each has its own check | Time saved is worth the join |
|---|---|---|---|---|---|
| P5 and P6 | yes (each reads P4, not the other; each has the other's section withheld) | yes (own output files) | mostly: a schema finding can change what a screen needs and the reverse | yes | P7 already is the join |

**Decision: keep sequential.** The third condition is doubtful, since P5 and P6 are exactly where the mutual
dependency lives. Running them in order costs clock time only. Revisit if a real run shows P5 and P6 findings never
interact.

## Predictability

- Agents in total, first pass: P1 2, P3 2, P4 2, P5 2, P6 2, P9 1 = **11** Codex or Claude agents, plus the COO,
  plus a possible 1–2 for P7 or P2 judgment. Each reconcile round re-runs at most the pieces an answer changed
  (up to 8 agents in a round). Worst case about **11 + 2 + 2×8 = 29**.
- Bounds: attempt limit 2 per piece, 2 reconcile rounds, concurrency 1 (nothing parallel).
- Cost estimate: **unmeasured.** The only basis is the intake trial (n=1), about 300k tokens for a handful of
  agents, which suggests roughly 0.6–1M tokens for the first pass. Low confidence. Codex usage is billed separately
  from Claude tokens, and every Codex node also costs a Claude wrapper.
- Success criteria, written before the run: C1–C6 above.

## Debuggability

- Agent labels: `<piece>-<role>-<engine>-<attempt>`, e.g. `p4-reviewer-astra-1`. Every input and output is a file in
  `runs/<runId>/`. Resume point: the first piece in `state.md` that is not `done`; each piece can be rerun alone.
- The COO reads the state file and the verdicts, not the raw Codex output.

## Quality control

- P1, P2 and P7 use scripts; P3–P6 and P9 use fixed checklists with file:line citations, judged by a fresh agent that
  does not see the reviewer's reasoning. No check is "find problems".
- Sabotage checks: the canary (P0), the id-deletion test (P2), the column-type test (P7).
- Independence: verifiers are a different kind from the reviewer where allowed. `agy` is excluded until Q7 is
  settled, so verifiers are fresh Claude subagents. That gives a different model family only in part (Codex
  reviewer, Claude verifier), which is *claimed* to help and measured nowhere.
- Skipped or unrun checks are listed in `report.md`.

## Not covered

- Reviewing domain model (3) and business logic (4) in full (Q2).
- Any change to code, schema or UI.
- Whether a Codex node really ran the model the design names: the canary is meant to show it, and how the tool
  reports the model is not yet verified (`EXECUTOR_KINDS.md`).
