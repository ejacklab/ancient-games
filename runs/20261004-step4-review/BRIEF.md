# Review brief — step 4 ("Size") of the workflow design algorithm

You are an **independent adversarial reviewer**. You are read-only. Write nothing to disk. You are one of four
reviewers working blind of each other; none of you sees another's answer.

## What you are reviewing

"Step 4" is the **Size** step of a method for designing multi-agent workflows. It exists in two copies that you must
compare, plus one diagram node:

1. `docs/WORKFLOW_DESIGN_METHOD.md` §3.4 "Size" (the source of truth)
2. `.claude/skills/workflow-design/SKILL.md`, numbered step 4 (the packaged copy agents actually read)
3. `docs/WORKFLOW_DESIGN_DIAGRAM.md` node `S4` / `DF`

Read all three yourself at those paths. The §3.4 and SKILL.md step 4 text is reproduced below for convenience, but
**the files are authoritative — quote them**.

### `docs/WORKFLOW_DESIGN_METHOD.md` §3.4, verbatim

- Up to 3 steps and nothing unclear except decisions that have a provisional assumption → one piece → a prompt
  file, with those decisions listed at the top as questions for EJ. A spot of kind information or unknown always
  means a workflow design. (Changed 2026-09-20 after trial 1, where three decisions with obvious defaults helped
  push a one-line fix out of "small"; n=1.) Blueprint spots follow the same rule: a missing or incomplete section
  always means a workflow design; a draft section alone does not.
- More than 3 steps → consider a new piece. Split only if each part keeps its own check **and** splitting changes
  how the work is done ("Split iff it changes the route", `challenge-mediation` skill).
- Risk is judged separately from size: how late a mistake would be noticed, whether it can be undone, how many
  things it touches. Tiny but risky → the prompt file gets one independent check.

**Default-first design.** When the size decision says workflow design, the design starts from a lookup, not a
blank page: each piece's category row (labelled in 3.2) or combination pipeline in `docs/TASK_TYPES.md` supplies the default pattern,
engine, check and sabotage; `others` gets the full method from first principles. A bespoke (challenger) design
replaces a default only on a written claim of ≥20% lower projected run cost **at equal coverage** (same
criteria ids, same checks, same blindness — coverage is a gate, never an axis). The decision is reviewed by the
script gate (`design_gate.py`) plus one blind fixed-checklist pass (Sonnet 5.5; a different kind when the
design builds or EJ flagged high risk), and every run reconciles its claim in `docs/TASK_TYPES_LEDGER.md` —
that ledger is how the defaults earn their n. (Added 2026-10-01 at EJ's request; n=0.)

Anchors for the number 3: Gate splits capability lists over three (`ancient_games/stages.py:109`) and the
the plan-wide cap of 3 dispatched corroborating sources (`ancient_games/registry.py:24`, used at `stages.py:309`; it caps dispatches per plan, not agents running at once — corrected 2026-10-03).

### `.claude/skills/workflow-design/SKILL.md`, step 4

> **Size.** Up to 3 steps with nothing unclear except decisions that have a default → a prompt file, questions at
> the top. More than 3 steps → consider a new piece, but split only if each part keeps its own check and the split
> changes how the work is done. A workflow design starts **default-first**: each piece's category row (labelled in
> step 2) or combination pipeline in `references/task-types.md` supplies the default pattern, engine, check and
> sabotage; a challenger design replaces a default only on a written ≥20%-lower-projected-cost claim at equal
> coverage, reviewed by `scripts/design_gate.py` plus one blind fixed-checklist pass (a different kind when it
> builds), and reconciled in the ledger (n=0). Too-small pieces cost more than they give: fixed cost per agent,
> context lost at every split, more joins. Judge risk separately from size (noticed late? cannot be undone? touches
> many things?); tiny but risky gets one independent check.

## Context you may read (read-only)

- `docs/WORKFLOW_DESIGN_METHOD.md` — §3.0–3.3 before it, §3.5–3.8 and §4–5 after it, for cross-consistency.
- `.claude/skills/workflow-design/SKILL.md` — the packaged eight steps.
- `docs/WORKFLOW_DESIGN_DIAGRAM.md` — the flow diagram and the method-section-to-skill-step map.
- `docs/TASK_TYPES.md` — the category table step 4 looks up. Check whether the columns step 4 names exist.
- `docs/TASK_TYPES_LEDGER.md` — the reconciliation ledger. Check its actual state.
- `.claude/skills/workflow-design/scripts/design_gate.py` — what the script gate really enforces (G5, G6, G7).
- `docs/EXECUTOR_KINDS.md` — engine routing, model/effort, blindness rules.
- `ancient_games/stages.py` and `ancient_games/registry.py` — the three anchors. Verify them.
- `docs/DISPATCHER_DESIGN.md`, `20260919-state.md`, `CLAUDE.md` if useful.

Do **not** treat any file's claims as true because the file says so. A citation that does not support its claim is a
finding. Where you can, quote the line.

## Required output — print exactly this structure as your final answer

```
## 0. RESTATEMENT
Step 4 in your own words, in at most 120 words, as a rule you could apply. Then state the decision it is meant to
produce (which of: prompt file / workflow design, and which pieces).

## 1. VERDICT
One line: SOUND / SOUND WITH FIXES / UNSOUND. Then the single most important problem, in one sentence.

## 2. FINDINGS
A markdown table, strongest first, at most 10 rows. Severity scale:
- BLOCKER: following step 4 as written produces a wrong route, or the challenger gate is satisfiable by a design
  that is not genuinely cheaper at equal coverage.
- MAJOR: two competent readers would route the same task differently, or a cited anchor does not support its claim.
- MINOR: wording or ambiguity a careful reader resolves.
- NOTE: observation, no fix required.
Columns: id | severity | what step 4 says (quote) | evidence (file:line, quoted line, or the counterexample) |
why it fails | concrete fix (the smallest edit that removes the problem)

## 3. CHECKLIST
Answer every row. Result is PASS, WEAK or FAIL, with one line of note. Do not invent a problem to fill a row.
| check | result | note |
C1  Every term step 4 leans on is defined or unambiguously referenced: "step", "piece", "prompt file", "provisional
    assumption" vs "default", "coverage", "projected run cost", "tier".
C2  The 3-step threshold is decidable by a reader with no access to the author — including the case of more than 3
    steps where splitting would not change the route.
C3  The three code anchors (`stages.py:109`, `registry.py:24`, `stages.py:309`) each support what they are cited
    for. Quote each line and judge.
C4  "Risk is judged separately from size; tiny but risky gets one independent check" is consistent with the
    ≤3-steps→prompt-file rule and with §3.2's rule that a hand-off must pay for itself.
C5  The default-first lookup is mechanically possible from `TASK_TYPES.md`: do the four columns step 4 names
    (pattern, engine, check, sabotage) exist for every category? What happens for `others`?
C6  The "≥20% lower projected run cost at equal coverage" rule is well-formed: who computes it, in what unit, from
    what baseline, compared how, and can a design satisfy it while being worse on predictability/debuggability?
C7  The challenger-review rule ("design_gate.py plus one blind fixed-checklist pass (Sonnet 5.5; a different kind
    when the design builds or EJ flagged high risk)") agrees with `EXECUTOR_KINDS.md` routing and the blindness
    rule in §3.7.
C8  The ledger claim — "that ledger is how the defaults earn their n" — holds against the ledger's actual state
    today (check the `reconciled` and `Actual cost` columns). Say what you counted.
C9  §3.4 and SKILL.md step 4 say the same thing. Quote both where they differ; drift is a finding.
C10 Every empirical mark in step 4 (n=1, n=0, "Changed 2026-09-20", "Added 2026-10-01", the 2026-10-03 correction)
    is accurate and correctly located.

## 4. STRONGEST COUNTEREXAMPLE
Describe one concrete, realistic task that step 4 would route wrongly or ambiguously, name the route it gives and
the route it should give. If you cannot construct one, say so and say why that is itself informative.

## 5. WHAT I COULD NOT VERIFY
Bullet list of claims you checked and could not settle, and anything outside your read access.

## 6. WHAT THIS CHECKLIST MISSED
Problems with step 4 that the checklist above does not have a row for.
```

## Rules

- Read the files. A finding with no `file:line` or quote is not a finding.
- Budget: at most about 12 tool calls and about 10 minutes. Be decisive, not exhaustive.
- A review that returns zero findings on a document carrying this many untested claims must justify that explicitly.
- Do not restate praise. Do not summarise the document for its own sake.
- Judge step 4 **as a design rule**: does a competent agent following it produce the right route? Do not review the
  quality of the `ancient_games` framework code beyond what the three anchors claim.
- Write nothing to disk.
