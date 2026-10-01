# TODO

## Encode method 3.0 (restate the challenge) in intake.js

Added to the method 2026-10-01; `intake.js` still embeds the challenge verbatim and never asks for a restatement.
Agreed shape (not scheduled):

- the step-1 readiness agent also writes the restatement (objective, in scope, out of scope) into the
  `runs/<runId>/state.md` Restatement block;
- one `restatement` field in its structured output, and one fixed yes/no check in script code: it names an
  objective, an in-scope and an out-of-scope; a challenge that allows two readings stops at step 1 as an unclear
  spot of kind decision;
- no new agent and no new loop;
- a sabotage case in `tests/workflows/intake_harness.mjs`: an empty or one-sided restatement must fail the check;
- then drop "Not yet encoded in `intake.js`" from `docs/WORKFLOW_DESIGN_METHOD.md` §3.0 and the n=0 row note in
  `docs/WORKFLOW_DESIGN_DIAGRAM.md` §6.
