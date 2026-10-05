# NOTE — nightly timeout design

## Gate status: NOT RUN

Every attempt to run `design_gate.py` came back "This command requires approval", and the rules said not to
ask. Instead I traced `design.json` through `validate_design` and `check_baseline` by hand: G1, G2, G3 (all five
contents, loops on the two `debugging` nodes), G4, G6, G8, G9, G10 and G11 all come out with no findings. G5 does
not apply because the design is `default`. That is a hand trace, not a run. Run the command before trusting it.

## What I decided

- **Not tiny.** The problem cannot be restated in one sentence because I do not know which job it is, and the
  only real check (tonight's run) is a day away. So this is a workflow design, not a prompt file.
- **Default-first, the `debugging` pipeline** (repro, fix, rerun). Here "rerun" is tonight's real run, graded.
  Five nodes run in sequence and nothing runs in parallel, because each node needs the previous one's result:
  `n1-diagnose` (Codex, strong tier: locate the job, root cause, a red repro, the baseline) → `n2-fix` (opencode,
  cheap tier, loop of 2, then a fresh Codex node) → `n3-review` (Claude Sonnet, blind and a different kind from
  both workers) → **EJ deploys** → tonight's run → `n4-grade` (Sonnet, fixed rubric, blind to the workers) →
  `n5-standup-note` (Sonnet, checked by the COO against the state file and the grade).
- **Diagnose and fix are separate nodes** on purpose. The hand-off buys an objective check: no fix starts until a
  repro is red and the baseline is recorded.
- **Raising the time limit is not a fix.** It is in `must_not_change`, and the reviewer has a planted-defect
  sabotage for exactly that case.
- **Deploying is a human checkpoint, not a node** (Rule 6). If the fix is not deployed before tonight, `n4` still
  grades the run and reports "fix not in run" (rubric dimension f).
- **One night is one attempt.** A FAIL tonight goes to EJ for a later grade → fix → regrade run. It does not loop
  inside this design.

## Questions I could not answer (written as U1–U6 in design.json, each with a provisional assumption)

1. **Which nightly job is it?** Nothing in this repo is called nightly. `touched_paths` and `baseline.command`
   are therefore marked `UNRESOLVED`, and `n1` fills them in before anything builds. The gate only checks that
   these fields are non-empty, so it accepts them. That is a gap in the gate, not proof the design is concrete.
   One candidate, not assumed: the stage2a e2e suite on dev116, which has its own skill.
2. Can the timeout be reproduced offline? If not after 2 attempts, `n1` stops and goes back to EJ.
3. Is raising the limit acceptable? I assumed no.
4. Who deploys, and by when? I assumed EJ, after review passes.
5. What does "grade" mean? I assumed a six-dimension rubric: completed, duration vs limit, stages, outputs, no
   new failures, fix commit present.
6. Standup audience and format? I assumed at most 6 lines of markdown for tomorrow's standup. The node does not
   post it anywhere.

## Assumptions the prompt did not cover

- "Tonight's run" means the first nightly run after the fix, and grading it is how we find out whether the fix
  held. It does not mean some separate run.
- The standup note comes after the grade, so it is for tomorrow morning.
- Engines follow the table and EJ's role memory (Codex for strong work, opencode for cheap code, Sonnet for
  review, grading and docs). None of them were canaried in this session, so readiness is still unverified.
- The cost estimate (~450k tokens) is unmeasured (n=0).
- `n5` counts as a "builder" to the gate only because `document and explain` is a mixed category and the design
  builds. Under labelling rule 5 the note is prose, so it is not a build. I gave it a sabotage check anyway to
  satisfy G9.
