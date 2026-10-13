Method 3.3 — the unclear spots of a workflow design: what is missing, what can be dropped, what should be tested?

Asked of: Linus, 孫子, 老子, Dave (`--only linus,sun-tzu,lao-tzu,dave`). Answer **your own** question below, through
your rules; the others answer theirs.

- **Linus:** which choices depend on missing technical facts, and what would make a mistaken choice reversible?
- **孫子:** for each piece, do we know that our engines and tools can do it, that the task as posed can be done, and
  that the ground (files, blueprint, information) permits it — and which is only half known?
- **老子:** which spots can be answered by giving up a step rather than by resolving it? (Say what would be lost.)
- **Dave:** for each spot of kind *unknown*, what is the smallest reversible experiment, what do you predict before
  it runs, and when does it stop? Leave any threshold EJ has not given open.

In "Answer", list spot ids (existing ones, or new ones you raise as N1, N2 …) with your verdict for each. Do not
decide for EJ: a spot to drop is a question for EJ, not a removal.

Facts (filled in by the COO):
- The challenge and its restatement: read `runs/20261013-research-tags-retag/workflow-design.md`, section "Restatement".
- The algorithm (steps, each with its check): the same file, "Pieces, in the order they run" (A, B, R1–R6).
- The unclear-spot list: `runs/20261013-research-tags-retag/state.md`, table "Unclear spots" (U1–U9). EJ answered the six
  questions on 2026-10-13 with "go", i.e. every provisional assumption stands: control = the four labels the rows were
  labelled under; rows from docs/research (the verify/sections copy is planted); run folder as named; both passes on
  dsh deepseek-flash, fresh sessions; experts asked (this call); issue 3 by one README mapping line.
- The blueprint status: not a product change.
- Tools proved in readiness: `runs/20261013-research-tags-retag/readiness.md` (python3, node, git, dsh ran today,
  the workflow's offline harness passes 14/14, pytest 684 passed / 1 expected failure).
- The tag definitions being tested: `docs/RESEARCH_TAGS.md`, section "The tags".
