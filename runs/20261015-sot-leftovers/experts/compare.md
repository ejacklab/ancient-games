# Experts on the unclear spots — 20261015-sot-leftovers

Question: `../question.md` (method 3.3 template, `--only linus,sun-tzu,lao-tzu,dave`). Every line is *my reading*
unless quoted.

| | Linus | 孫子 | 老子 | Dave (control) |
|---|---|---|---|---|
| Answer (one line, *quoted*) | "keep this a small document repair, distinguish policy decisions from missing measurements, and make each change independently reversible" | "None of them is a reason to stop — *if* EJ answers U1–U5, has Rd3.1a say the limit is provisional until U4 is measured, and has the edited build script and the blind reviewer each shown able to fail" | "Three of the five can be answered by giving up a step rather than by resolving them: **U3** wholly … **U4** … and **U2** half" (rerun; the first run was empty) | "Only one spot, U4, is of kind *unknown* … I raise two new spots … Both cost almost nothing to fix" |

## On the spots

- **U1 (metadata after the first commit):** Linus — yes for `covers`, but "do not assume changing `source` or
  `depends_on` always preserves the claim"; Dave — this repo has had 1 rename in 293 commits, so stale paths are rare
  here (n=1 repo, *ran*).
- **U2:** the project owner (Linus; 孫子 notes the role has no fallback).
- **U3:** keep the example and defer the build (Linus, Dave); 孫子: Rd3.1a must say the limit is provisional until U4
  is measured. Dave: the example may be above agy's possible 12,000-character limit (W-4).
- **U4:** out of scope, backlog (all). Dave gives a sentinel-file test if it is ever brought in.
- **U5:** relative paths, if the files travel together (Linus, Dave). The COO's path check found all three kit paths
  already resolve from `docs/memory-system/`; what is missing is saying the files travel together.

## New spots raised (folded into the run, marked by who raised them)

- **Linus N1:** U1 would let two branches change `covers` differently; W6.3a says keep both sides — of a single
  value? Needs a rule.
- **Linus N2:** the reviewer gets EJ's accepted decisions (not the worker's reasoning). **N3:** the review covers the
  release-note edit and any repairs.
- **孫子 N2:** the build script holds both the data and its checks, so the hand that edits it also edits its check →
  *done*: `checks/yaml_check.py`, a separate check written before P2, self-test PASS.
- **孫子 N1 / Dave N2:** a reviewer finding one plant is n=1; whether to add a second plant is EJ's call.
- **Dave N1 / 孫子 N3:** compare the baseline by failing-test id, not count → *done*: `nodes/baseline-p2.txt`
  (`test_skills_export_is_current`, 993 passed).
- **Dave on U5:** the build script's "links resolve" checks requirement ids only, never file paths → *done*:
  `checks/paths.py`, self-test PASS (fails on a missing path).

## Check

老子 also: W3.6 carries the same `unassigned` as L5 but is outside the five — record it, do not fix it here; the review and its plant cannot be given up.

`four_experts.py check`: see `../check.txt`. Engines: Linus codex gpt-6.1-sol, 孫子 dsh, 老子 opencode
(first run empty), Dave a Claude subagent.
