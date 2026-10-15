# Brief — review (read-only)

You are reviewing branch `feat/integrate-r11-r13` in this git worktree (the current folder is the repository root)
against its base `master`: `git diff master...HEAD` plus the uncommitted changes (`git diff`, `git status`). Do not
change any file except your result file.

## What the change claims

1. `harness_health.py` reports R11 and R12 (R10 replaced by R12): spec `runs/20261016-integrate-r11-r13/spec-harness-health.md`.
2. The guard's `doctor`, `rates`, `insight` gained `--json`: `.claude/skills/workflow-design/guard/SPEC.md` Round 7.
3. R13 (use cases and requirements) moved, unchanged with its ids, from `docs/HARNESS_REQUIREMENTS.md` to
   `.claude/skills/requirement-check/references/use-cases-and-requirements.md`; the skill's description and a new
   section cover it; every live pointer was moved (`workflow-design/SKILL.md`, `bootstrap/SKILL.md`,
   `docs/WORKFLOW_DESIGN_METHOD.md` item 13, `docs/workflow-templates/blueprint.md`).
4. The criteria the run is scored on: `runs/20261016-integrate-r11-r13/criteria.yaml`.

## Find defects

- Code that does not do what its spec says; a check that cannot fail; a test that passes against wrong code; a guard
  output reaching the report raw; a file written during a harness-health run; a crash path.
- R13's text: compare the reference file with the `## R13` section removed from `docs/HARNESS_REQUIREMENTS.md`
  (`git show master:docs/HARNESS_REQUIREMENTS.md`). Any word changed is a defect.
- A live doc or skill (not `runs/`, not the generated `skills/` copy) that still sends a reader to R13 in
  `HARNESS_REQUIREMENTS.md`, or repeats R13's text.
- The requirement-check section: does it add a rule R13 does not state (a defect: "never add structure that was not
  given"), or misstate what the guard's `register` command checks (read `guard/src/register.ts`)?

Run what you need (`env -u NO_COLOR python3 -m pytest -q tests/test_harness_health.py`, `cd
.claude/skills/workflow-design/guard && bun test`). Do not call any other AI engine.

## Result

Write `runs/20261016-integrate-r11-r13/nodes/review.result.md`: `status: done`; then one numbered finding per defect —
severity (high / medium / low), `file:line`, what is wrong, the input or reading that shows it, and the fix you
suggest. End with "Checked and found nothing" for each claim above where that is true. No praise, no summary.
