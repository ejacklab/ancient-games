# Requirements evaluator — backlog

Findings outside the accepted requirements, and limits found by calibration, that did not become work in run
`runs/20261013-requirements-evaluator/`. EJ decides what becomes a requirement.

## For EJ to decide

1. **O8: when is a case "proven"?** EV-C3.2 says *"A probe that stays green on its case's mutant is unproven, and its
   case cannot be PASS."* Read literally, that is per probe: every probe of a case must fail on the mutant.
   DATA.md E10 (and `verdict.py`) give PASS when **at least one** of the case's probes fails on its mutant. The
   requirement and the contract say different things (D6 review O8). EJ asked to discuss this at the end.

## Known limits (narrowed, not closed)

2. **F2 and F9 (blindness)** are narrowed, not enforced:
   - judge call 1 works in `/tmp/evaluator-judge-<runId>/` and is never told the run folder;
   - Codex writes mutants in a view with no probes, under its write sandbox;
   - probes run with a scratch `HOME` and `TMPDIR`.

   Reads outside these folders are not prevented, because there is no OS-level isolation here.
3. **F5(c) is guarded:** a single-probe mutant run is not judged by it. Without a recorded `runs` status, an
   all-red single-probe run still counts as proof (Dave measured this hole).
4. **Requirements about the product's own tests or `.git`** (INDEX.md's C2, V6) cannot be checked in a blind
   workspace. They come out UNKNOWN, which is correct, but they are never checked at all.
5. **A probe that starts its own clean Python** under the scratch `HOME` cannot find a pytest installed in the user's
   site-packages (seen in K1e). It lands on UNKNOWN (safe), but the probe says nothing.
6. **The model actually used by each step is not verified** from inside a Workflow script (F17).
   `cost.json` says `"models": "requested, not verified"`, and `"tokens": "not reported"`.

## Outside criteria, from the D6 review (not fixed)

7. **O1:** duplicated helpers across modules (`_probe_key`, `_read_json`, `InputError`). One name, one job means one
   copy.
8. **O2–O4:** names doing two jobs. `verdict` is a string, a tuple element and a dict; `product` is an outcome map and
   a path. The `LAST_OUTPUT` side channel in `probe_matrix.py` remains.
9. **O5:** some briefs say both "Write tool" and "temp name and rename".
10. **O7:** `confirm-check`'s voided count can overcount.
11. **O9:** the judge brief's "may contain a planted defect" also appears in call 2's clean copy.

## Calibration coverage

12. **One product only.** The evaluator is calibrated on one product, the INDEX.md generator, and on no product
    with 2 or more judged cases. So the plant check was exercised with one judged case, or none.
