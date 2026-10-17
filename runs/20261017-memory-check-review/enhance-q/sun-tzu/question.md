# Question — after this round of review and fixes, what should the memory-check tools improve?

The owner (EJ) runs a time-boxed review-and-enhance workflow. Your advice is ranked; the main agent applies the top of
it and the owner may overrule. Answer within about 8 minutes of work.

Rules for this question:
- Every improvement names the use case (U1–U6 in `memory_check/USE_CASES.md`) or the vision line
  (`memory_check/VISION.md`) it serves, and the case that shows it is needed now. One that serves none is not
  proposed: the owner wants less work, not more.
- Rest each point on a file in this repository (cite it); a point from memory only is labelled *recall*.

## Facts
- The tools: `memory_check/` (TypeScript) and `tools/memory_index.py` (Python, which it runs). Source: those folders.
- This run's review findings and their verdicts: `runs/20261017-memory-check-review/findings.md`; what was fixed:
  `runs/20261017-memory-check-review/nodes/fix-r*.result.md`. Source: those files.
- The previous enhance round and what it applied: `runs/20261017-memory-check/enhance-q/compare.md`,
  `runs/20261017-memory-check/report.md`. Do not repeat what it applied.

## The decision
Rank at most three improvements, most valuable first: what it is, the use case or vision line it serves, the case that
shows it is needed, how to check it is done. End with your top one in one line.
