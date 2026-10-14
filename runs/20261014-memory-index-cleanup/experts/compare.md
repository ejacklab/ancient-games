# Experts on the unclear spots — memory_index.py cleanup design

Question: `question.md` (method 3.3 template, `--only linus,sun-tzu,lao-tzu,dave`). 范蠡 is not asked at this step.

| | Linus | 孫子 | 老子 | Dave (control) |
|---|---|---|---|---|
| Answer (one line, *quoted*) | "Keep the two-check scope, but resolve the gaps in baseline preservation, engine readiness, verification and rollback before building." | "the task as posed can be done … The ground is half known" | "Give up the step, and the spot stops being a question." | "None of the seven listed spots … is of kind unknown … N3 is the one that matters most: once the id-form check exists, 13 existing rejection tests can pass for the wrong reason." |
| Main new spots | ASCII digits; fixture migration loses coverage; who may commit; bound miscounted (8 → 11) | spec edits never reach the worktree; `trace_check.py` has no B2.7; canaries unproved; worktree path | N2's exit on Codex breaks blindness; keep the `=======` fixture; run only old mutants inside the diff | masked rejection tests (fixture-id lint); per-mutant control; trailing-junk mutant; `d990dab` merges cleanly |

## Where they agree

*My reading.* All four keep the scope to the two checks and leave Q1 and Q2 to EJ. Linus and Dave both found the
masking risk: after the ids change, old tests can pass on the id alone (Linus: "Green tests after rewriting inputs
alone do not prove their original coverage survived").

## Where they disagree

- **Old mutants.** 老子: run only those inside N2's diff (*quoted*: "Twenty-odd mutant runs that were killed by code
  this run never edited"). Dave: run all, compared mutant by mutant with a control taken before N2. Kept: Dave's, since
  the run is a script and the control is what catches masking.
- **Q1.** 老子: branch from `d990dab`, no merge. Linus: an isolated integration branch. Both stay as options for EJ.
- **The evaluator (D5).** 老子 would drop it; Linus would keep it as optional evidence once it is known which spec it
  reads. Kept as the default, with Linus's condition.

## What each added

Folded into `../workflow-design.md`, each marked with who raised it. See `../state.md`, log line "X done".

## What they need to know (for EJ)

1. Q1 and Q2 (unchanged).
2. Should Unicode digits pass the id check? The default is ASCII only (Dave, Linus).

## Check

`four_experts.py check`: 2 failures — "fan-li: no answer file" (not asked, by design) and 老子 以深為根 vs 以深爲根 (a
script variant). The check was written by Claude; it does not establish that the rules were applied well. One factual
error found by reading: 孫子 said `tools/evaluator/` does not exist; it is on branch `build/evaluator`.
