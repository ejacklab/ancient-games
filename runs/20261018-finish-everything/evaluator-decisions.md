# Evaluator — items 8–11, decided on paper (provisional, the main agent's; for the owner to accept or decline)

All six experts (plan-review/compare.md): no ~1M-token measuring run for these inside the window. Each item below
gives the question, what the code does today (read, with file:line), my pick and why, and what would change it.

## Item 8 — the judge's folder in /tmp (EV-R3.2)
- **Conflict, not a bug.** `docs/evaluator/REQUIREMENTS.md:52` EV-R3.2 (MUST): "It writes only inside
  `runs/<runId>/`." `docs/evaluator/DATA.md:376` (repair R1, F2): the judge's folder is built "outside the run
  folder, at `/tmp/evaluator-judge-<runId>/`" so judge call 1 never sees the run folder (blindness).
  `tools/evaluator/model_io.py:240-244` does that; nothing removes the folder after the merge
  (`/tmp/evaluator-judge-run` is still there from an earlier run).
- **Pick: keep F2's folder, remove it after `judged-merge` has copied `judge-1.json` in.** F2 is newer and tested
  (R1, 862 tests); the blindness it buys is a requirement too (EV-B). The /tmp folder is then scratch, which the
  project allows ("Scratch in /tmp is fine; it is the refer-back artifact that must not stay there", CLAUDE.md).
- **For the owner:** EV-R3.2 would read "It writes only inside `runs/<runId>/`, apart from the judge's scratch folder
  in `/tmp`, which it removes before it ends." A requirement text: yours to accept.
- Built in this run: see state.md item 8 (tests first, then the code).

## Item 9 — five result states
- **Today.** `verdict.json` has PASS / FAIL / UNKNOWN per case and requirement (`tools/evaluator/verdict.py`); a
  blocked run writes no verdict. The guard's bridge (Round 19) already turns them into three outcomes: FAIL → a
  failure, UNKNOWN → a note, blocked → a could-not-run note. memory_check has five (pass, fail, needs a reviewer,
  not applicable, could not run).
- **Pick: no change to the evaluator now.** The two states the experts asked for already exist one level up:
  *could not run* is the blocked run (a note, never a failure, P2 accepted) and *not applicable* is `out_of_scope`.
  The remaining split — UNKNOWN as "needs a reviewer" against "no probe could be written" — matters only if the
  owner reads them differently. Item 12's verdict shows how many UNKNOWNs there are and why; that count decides it.
- **Changes my pick:** item 12 showing UNKNOWNs of two kinds that need different actions.

## Item 10 — use cases as an input
- **Today.** The evaluator reads VISION.md and REQUIREMENTS.md only (`spec_parse.parse(requirements_text,
  vision_text)`); USE_CASES.md is not read. The project's rule is that a use case wins a conflict with a requirement.
- **Pick: design written, not built.** Each use case's Fails-if and minimum acceptance become cases of a group named
  by the use case id (`U3-F1`, …), parsed by the same rules as a requirement paragraph; a use case that cites
  requirement ids links its group to theirs, so a use case FAIL with its requirements PASS is reported as a gap in
  the requirements. Not built now: it changes EV-P1 (what the evaluator reads), an accepted requirement, and each
  extra group costs probes and mutants (about +5–10% tokens per use case group, *not measured*).
- **For the owner:** whether the evaluator reads use cases at all. If yes, this design is the first build.

## Item 11 — O8, when a case is "proven"
- Already asked of the experts on 2026-10-14 (`runs/20261014-four-experts-question-for-the-four-experts/compare.md`).
  None chose the literal per-probe reading A; four of five keep reading B (a case is proven when at least one of its
  probes fails on its mutant). Dave measured on recorded runs: A loses 51 of 72 PASSes for 0 extra faults caught.
- **Pick: reading B, as the code already does; EV-C3.2 reworded** to "A case whose probes all stay green on its
  case's mutant is unproven, and its case cannot be PASS." Add the reported duty most experts named: a probe red on no
  mutant in the run is listed in the verdict as unproven (a note, no verdict change). No code change in this run.
- **For the owner:** the EV-C3.2 wording (a requirement text). The reported list is a later build.
