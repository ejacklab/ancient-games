# Question — is the requirements evaluator ready to be the judge of every build?

The owner (EJ) changed the rule today: a failure is what the **evaluator** judges wrong against the product's vision,
use cases and requirements, or the owner's correction (`docs/HARNESS_REQUIREMENTS.md` R12.2). The guard already counts
only failures found by `evaluator` or `owner` (`.claude/skills/workflow-design/guard/src/insight.ts`, `JUDGES`). Nothing
runs the evaluator yet. Before the wiring is designed, check the evaluator itself. The owner decides.

Rules for this question:
- Every file you need is a copy inside this repository, under `runs/20261017-evaluator-wiring/snapshot/` (the
  evaluator lives on branch `build/evaluator`, not on master). Cite those copies by path and line.
- A point from memory only is labelled *recall* and does not decide alone. Say "I don't know" where the files do not
  answer.

## Facts (each with its source)
- What the evaluator is meant to do: `snapshot/docs/evaluator/VISION.md` (PASS / FAIL / UNKNOWN per requirement, MEETS
  overall; never PASS without proof, never FAIL without a repro, never reads the builder's tests) and its 26
  requirements, `snapshot/docs/evaluator/REQUIREMENTS.md`; data formats `snapshot/docs/evaluator/DATA.md`; known
  limits `snapshot/docs/evaluator/BACKLOG.md`.
- Its code: `snapshot/tools/evaluator/*.py` (stdlib only); its workflow `snapshot/.claude/workflows/evaluate-requirements.js`
  (30 labelled steps); briefs `snapshot/docs/evaluator/briefs/`; tests `snapshot/tests/test_evaluator_*.py`.
- Its tests pass: 177 passed on `build/evaluator` at 35856de (`runs/20261017-evaluator-wiring/nodes/evaluator-tests.txt`,
  run by the main agent in a temporary worktree today).
- Its one real use: calibration on the INDEX.md generator, `snapshot/runs/20261013-calibration/report.md`; the run's
  state and design: `snapshot/state.md`, `snapshot/workflow-design.md` (the K1–K1d lines: about 0.8–1.2M subagent
  tokens and 20+ minutes per evaluation; 0 of 28 FAILs reproduced on the first live run, 2 reproduced after repair).
- What building memory-check today taught (`runs/20261017-memory-check/report.md`): most review findings were passes
  where the tool could not decide; five result states were needed (pass, fail, needs a reviewer, not applicable,
  could not run); tests written from the spec found three spec errors; reproduce-before-fix sorted real findings.

## The decision
1. **Does the evaluator do what its vision says?** Name what works (with evidence) and what does not, by its
   requirement ids (EV-…). Especially: can it ever report PASS without proof, and can a crash or a timeout read as
   anything but UNKNOWN?
2. **What blocks using it as the judge of every build?** Its inputs (it reads vision and requirements — not use
   cases), its cost per run, its result states, its output format, and how a FAIL would become a guard failure
   (`guard/src/cli.ts fail --found-by evaluator`).
3. **What must change first, and what can wait?** At most five items, most important first, each with the
   requirement or use it serves.

End with your verdict in three lines: ready / ready after X / not ready because Y.
