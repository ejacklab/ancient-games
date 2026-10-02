# Census: copies of the workflow-design algorithm — 2026-10-01

Status: **verified** by local file reads on 2026-10-01 (line counts as of that moment; the §3.0 restatement
edit landed the same day and touched six of these files, confirming the sync cost).

One algorithm, **four substantive copies** plus partial encodings:

| # | Where | Form | Coverage |
|---|---|---|---|
| 1 | `docs/WORKFLOW_DESIGN_METHOD.md` (287 ln pre-3.0) | canonical prose, §3.0–3.7 + blueprint check, state/memory, three qualities | everything |
| 2 | `.claude/skills/workflow-design/SKILL.md` (150 ln pre-3.0) | its own condensed rewrite as steps 1–8 — **real prose, not a link** | everything except the §4 memory tables |
| 3 | `docs/WORKFLOW_DESIGN_DIAGRAM.md` (209 ln) | the same algorithm as mermaid diagrams + a mapping table | everything |
| 4 | `.claude/workflows/intake.js` (690 ln) | executable encoding: SECTIONS, TASK_KINDS, MUST_NEED, R1.1 regex, MAX_STEPS_PER_PIECE=3, fixed yes/no checks | **steps 1–4 only** |

Partial encodings:

- `tests/workflows/intake_harness.mjs` (380 ln) — the strictest statement of the steps-1–4 invariants, as
  sabotage cases. Steps 1–4 are therefore triple-encoded; a rule drifting out of intake.js fails here.
- Templates (`docs/workflow-templates/`, 5 files) — output shapes, not rules; state.md's step table lists the
  algorithm's steps.
- `CLAUDE.md` — a one-line summary pointer.

## What is actually single-copy

Only the *file links*: `references/method.md` → METHOD, `references/executor-kinds.md` → EXECUTOR_KINDS,
`assets/templates/` → `docs/workflow-templates/` (all symlinks, verified). The algorithm's **text** exists in
three independent prose/diagram forms plus code. CLAUDE.md's "one copy of each" claim is true for the linked
files, not for the algorithm.

## Cost of a change

One rule change touches up to 5 places (METHOD, SKILL, DIAGRAM, intake.js, harness) — the §3.0 addition
touched METHOD, SKILL, DIAGRAM and 3 templates (intake.js deliberately deferred to `TODO.md`).

## Drift observed (2026-10-01, cosmetic only)

- SKILL "decisions that have a default" vs METHOD "provisional assumption" — same meaning.
- SKILL step 8 = METHOD 3.6 split out — documented in the DIAGRAM mapping table.
- Tier rule (n=0) worded consistently in both.
- DIAGRAM drawn from both sources the same day; in sync at census time, nothing keeps it that way.

## Structural note

Steps 5–8 (loops, graph, sequential-first, acceptance-criteria stop) have **no runnable encoding** —
prose/diagram only. The skill's SKILL.md restating nearly the whole method while also linking
`references/method.md` is the main duplication; progressive disclosure (SKILLS_OPEN_STANDARD.md) argues for
a thin body: trigger + step names + pointer. Proposed, **not approved** — see OPEN_QUESTIONS.md.
