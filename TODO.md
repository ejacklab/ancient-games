# TODO

## Encode method 3.0 (understand the challenge) in intake.js

Added to the method 2026-10-01 (six whys + categorization added the same day); `intake.js` still embeds the
challenge verbatim and never asks for a restatement. Agreed shape (not scheduled):

- the step-1 readiness agent also writes the restatement (objective, in scope, out of scope, the six whys,
  categories inferred per `docs/TASK_TYPES.md`) into the `runs/<runId>/state.md` Restatement block;
- one `restatement` field in its structured output, and one fixed yes/no check in script code: it names an
  objective, an in-scope and an out-of-scope; a challenge that allows two readings stops at step 1 as an unclear
  spot of kind decision; the category is validated against the TASK_TYPES table and the facts (G2's shape);
- optionally run the design JSON through `.claude/skills/workflow-design/scripts/design_gate.py` at the check
  phase instead of re-implementing its rules;
- no new agent and no new loop;
- a sabotage case in `tests/workflows/intake_harness.mjs`: an empty or one-sided restatement must fail the check;
- then drop "Not yet encoded in `intake.js`" from `docs/WORKFLOW_DESIGN_METHOD.md` §3.0 and the n=0 row note in
  `docs/WORKFLOW_DESIGN_DIAGRAM.md` §6.

## Dispatcher layer (direction adopted 2026-10-03, not built)

EJ adopted a friend's design idea: a layer, not the COO, spawns and supervises agents, so the method's prose rules
become code that cannot be skipped. It would join the scripts already built — `runlog.py` (two timers, events),
`validate_result.py` (pass-back), `harvest_run.py` (feedback), `quote_check.py` (explorer) — and enforce the caps
(5 roles per run, 3 at once), the executor-failure retry on the fallback, and the model check. Ancient Games (a
referee that decides how many agents and journals every decision) is the natural home. The COO keeps planning and
algorithm design. Design written 2026-10-03: `docs/DISPATCHER_DESIGN.md`. Built the same day as
`scripts/dispatch.py` (steps 1–4); open: a live canary per engine adapter, the first real run, and EJ's two
remaining decisions (§8).
