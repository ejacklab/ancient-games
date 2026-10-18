# Requirements evaluator — product vision

> **Status: accepted by EJ on 2026-10-13** (EJ: *"accept as you suggest, go"*). Written 2026-10-13 by the COO (Claude `claude-opus-5-5`), as piece D1 of run
> `runs/20261013-requirements-evaluator/`. Each line names its basis:
> - **[EJ]**: EJ's words or decision, from the challenge or the answers to Q1–Q4 (`state.md`);
> - **[run]**: what happened in run `runs/20261012-index-md-build/`;
> - **[design]**: this run's `workflow-design.md`;
> - **[proposed]**: the COO's wording, not yet said by EJ.
>
> Sibling: `REQUIREMENTS.md`.

The evaluator answers one question about a piece of software: **does it meet all of its requirements?** It takes the
product's vision and requirements and the built software. For each requirement it answers PASS, FAIL or UNKNOWN, and
it gives one overall answer, MEETS or not [EJ: *"an evalutor that check do the developed software meet all the
requirements"*].

**Who it is for.**
- EJ, deciding whether to accept a build [EJ].
- The COO, at the end of a run that builds, as the check that does not come from the builder [design].
- It works for any product whose requirements carry ids and **Fails if** lines, not only one product [EJ, Q1].

**The problem it solves.** "The tests pass" is the builder's claim about the builder's own tests. In the first full
build here:
- the builder bent the code to fit a defective test [run: N2 attempt 1];
- the tests missed a requirement until broken copies of the code exposed the gap [run: N3, B2.4];
- three defects were seen only by a reviewer [run: N4, F2 F3 F5].

An evaluator that starts from the spec, not from the build, is the independent check [design].

**What it will never do.**
- **Never say PASS without proof.** A PASS needs a check that passes on the product and was shown to fail on a broken
  copy. Anything less is UNKNOWN [design; the "grade a run" rule in `docs/TASK_TYPES.md`: missing proof is never
  PASS].
- **Never say FAIL without a repro.** Every FAIL carries the command that shows it, and a second agent has confirmed
  the check is faithful to the requirement's own sentence [design; run: N2's defective test].
- **Never drop a requirement.** A requirement it cannot check is reported as UNKNOWN or untestable, with the reason
  [design].
- **Never read the builder's tests, notes or history.** It sees the product code and the spec only, so it cannot
  inherit their blind spots [design; run: N1 was written blind, and it found what the builder bent].
- **Never change the product.** It writes only inside its own run folder [design].

**Kept simple.** Fixed steps run as scripts, and models are used only where reading prose is the work: classifying a
case, writing probes, writing broken copies, confirming a failure, judging what cannot be run [design]. One engine per
step, and no fallback [`docs/EXECUTOR_KINDS.md`].

**How we know it works** [proposed; measured in D5 of the run]:
- On seeded faults, each in one known requirement, it never answers MEETS, and it names the faulty requirement.
- A planted requirement that cannot be checked comes back UNKNOWN, never PASS.
- On the clean INDEX.md generator, every FAIL it reports reproduces.
- Its catch rate on the seeded faults is shown next to that of the product's own acceptance tests on the same faults.
