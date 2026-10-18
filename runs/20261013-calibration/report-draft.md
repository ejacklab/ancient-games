# Report — run 20261013-requirements-evaluator

Written by the COO (Claude `claude-opus-5-5`), 2026-10-13. Labels: *ran* means run, with the output recorded; *my
reading* means a judgment; *not measured* means what it says. **DRAFT: K1d, the live run after R1, is pending.**

## What exists

On branch `build/evaluator` (worktree `/home/smoke01/dev/ancient-games-evaluator`); **not merged, not pushed**:

- **Spec, accepted by EJ 2026-10-13:** `docs/evaluator/VISION.md` and `REQUIREMENTS.md`, 26 requirements EV-R / EV-C /
  EV-P. `DATA.md` is the COO's interface detail.
- **Scripts, stdlib only:** `tools/evaluator/` holds `spec_parse.py`, `workspace.py`, `probe_matrix.py`, `verdict.py`
  and `model_io.py`.
- **The workflow:** `.claude/workflows/evaluate-requirements.js`, 30 labelled steps.
- **Six model-step briefs:** `docs/evaluator/briefs/`.
- **Tests:**
  - 862 in the suite, including about 180 for the evaluator;
  - a 20-case offline harness.

  Every module's tests were written before its code, by a different engine.

## Calibration (D5), on the INDEX.md generator at 21b2597

| Run | Result |
|---|---|
| K1 | **Failed the pre-registered bar.** 49 of 49 probes red, 0 of 28 FAILs reproduced. Four bugs: relative paths; confirmation with no failure output; judge files never written; judge paths. Each fixed with a regression test. |
| K1b / K1c | 24 PASS, 1 FAIL, 6 UNKNOWN. **The one FAIL is real:** the spec says `[DFLOH]` (runbooks dropped after the build pinned it), while the generator accepts `R-`. It reproduces. |
| K2 | 6 hidden faults. The evaluator turned the faulted case PASS → FAIL in **5 of 6**, each exactly the right case; the product's own tests caught **6 of 6**. The miss was masked by an over-specified probe. |
| K3 | A planted requirement with no Fails if → UNKNOWN, never PASS. |
| K4 | No model step read the product's tests; the planted marker was never seen. |

## Blind review (D6) and repair R1

- **The reviewer** (Claude Sonnet 5.5, blind) found the plant and the COO's withheld note, plus 20 findings in
  criteria. The COO ran the three worst, and all three held.
- **The fix order** came from the four experts and Dave. Dave measured the guarded versions of F4 and F5.
- **The R1 repair:**
  - tests first, by opencode (68 tests) and Codex (29), written against the old code, where 59 + 24 of them were red;
  - code by Codex and opencode;
  - two corrected rules and the F9 probe environment by the COO.
- **R1's results** (*ran*):
  - 862 passed; harness 20/20;
  - F1 → MEETS: no;
  - F3 → `EV-P1-F2` is cited;
  - F5 → a recorded timeout, an all-red run and an error-only red are all UNKNOWN, while a healthy kill is PASS;
  - control: re-deciding the 7 recorded runs changes 0 cases.

## Known limits (not fixed; by design or narrowed)

- **F5(c)**, Dave's guarded rule, does not judge a single-probe mutant run that has no `runs` key.
- **F2 and F9** are narrowed, not enforced. There is no OS-level isolation here: a model that goes looking can still
  read outside its folder.
- **Requirements about the product's own tests** (such as C2) cannot be checked in a blind workspace; they come out
  UNKNOWN.

## The COO's own errors in this run

- **A wrong known answer.** My known-answer regex had the same blind spot as the rule it checked: CACHES ids, and
  "is opened".
- **An incomplete fix.** I widened a parser rule and missed a third assertion that depended on it.
- **The strict F5(c).** I wrote it into the contract after Dave had measured why the guarded version was right.
- **The INDEX.md spec commit.** `21b2597` committed the INDEX.md spec after another session had changed it, and the
  commit message claims it is the spec the build used.
- **Briefs written to paths that were refused,** and engines launched before the files existed: twice.
- **The F9 probe-environment part** was in DATA.md and in no engine's brief.

## Open, for EJ

- **O8:** EV-C3.2's wording against DATA.md's E10 rule (deferred to the end, as EJ asked).
- **Dropping `R-` and runbooks** in the INDEX.md generator (EJ: yes). Not started: it is on master, outside this
  worktree.
- **Merging `build/evaluator`.**
