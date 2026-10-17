# The text of P1–P3 (accepted by EJ, 2026-10-18: "use a workflow to run your three provisional decisions")

## For `docs/WORKFLOW_DESIGN_METHOD.md`, a new paragraph after the one ending "This is what lets a run end."

**The evaluator at a milestone.** The requirements evaluator (`docs/evaluator/`, code on branch `build/evaluator`)
judges a product against its vision, use cases and requirements. It runs on a milestone build, or a build the owner
names — never per task or per node: one evaluation costs about a million tokens and twenty minutes. Its `verdict.json`
reaches the guard through `guard/src/cli.ts evaluation ingest <verdict.json> --run runs/<run> --baseline <the
product's last accepted verdict.json>`: each requirement group that fails with a FAIL case the baseline did not fail
becomes one failure found by the evaluator (R12.2); an UNKNOWN is a note for the owner in `evaluator-notes.md`; an
evaluation that crashed, timed out or was blocked is a note too, never a failure, because a crash is no judgment. When
the owner accepts the build, its verdict becomes the product's baseline for the next evaluation.

## For `.claude/skills/workflow-design/SKILL.md`, a sentence after the one ending "top-ranked fix applied (R12.3)"

At a milestone build, or one the owner names, the requirements evaluator judges the product, and
`guard/src/cli.ts evaluation ingest` turns its verdict into evaluator failures and owner notes against the last
accepted verdict (method 3.6).

## For `docs/METHOD_CHANGELOG.md`, a line in the Added section

- 2026-10-18 — 3.6: "The evaluator at a milestone" — the evaluator runs on milestone or owner-named builds, never per
  task; its verdict reaches the guard by `evaluation ingest` against the last accepted verdict; a crashed run is a
  note, not a failure (run 20261017-evaluator-wiring, P1–P3, accepted by EJ).
