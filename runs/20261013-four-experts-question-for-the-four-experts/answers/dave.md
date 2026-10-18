# Dave — the order and method for fixing the 20 findings

## Answer
Fix them in four rounds, each one a narrow change:
- **(A)** the paths that can give a false PASS or a false MEETS: F1, F5, F4, F19, F10 with F12, and F11;
- **(B)** the paths that drop a requirement: F14, F3, F20, F15;
- **(C)** the paths that weaken blindness: F8, F2, then detection only for F9;
- **(D)** defer F6, F7, F13, F16, F17's model check and F18, and list them as known gaps.

Do F5 and F4 the guarded way I measured below, because the obvious versions break 4 and 3 frozen tests.

## How I decided
1. **What would change my mind** (my #1). For each fix, the deciding observation is this: does a new test fail when
   the fix is undone, while the frozen tests still pass and the recorded runs keep their verdicts? If a fix needed a
   frozen test weakened, I would drop that version of the fix.
2. **The data we already have** (my #5). I read the recorded calibration runs (k1, k1b, k1c, k2-1…6, k3) and found
   three things:
   - **F5 happens in practice.** In k1 (and k3, which reuses k1's matrix) all 49 probes are red on the product and
     on every one of the 27 mutants. That was the K1 path bug, and on the product side it produced 28 FAILs. The same
     all-red pattern on the mutant side is how F5 produces a false PASS. In k1b, k1c and k2-1…6 no mutant is all-red.
   - **The plant check proves less than "8 of 8" suggests.** After K1, `plant_found` is true in 8 of 8 runs. But
     each run has exactly one judged case (V5-F1), so the judge could tell which case was planted with or without
     the `plant_case` key. On this product, fixing F2 changes nothing that can be measured.
   - **The 10 recorded runs cannot test F1 or F5** (see step 4).
3. **I wrote predictions down before testing** (my #3). The metric was failures across the 6 evaluator test files;
   the control was 79 passed. All 5 predictions held.
4. **I ran the small experiment instead of arguing** (my #2, my #4). I applied each candidate fix alone to a scratch
   copy in `/tmp` and ran the evaluator tests against the unchanged code as control.

   | Candidate fix | Frozen-test result |
   |---|---|
   | F1: `meets = bool(requirement_rows) and all(...)` | 79 passed. No existing test covers the empty spec, so a new test is needed. |
   | F3: citation regex built from `spec_parse.ID` plus `-F[0-9]+` | 79 passed. It now matches `EV-P1-F2` and `EV-C3.3-F1`; `B1-F1`, `W1.3-F2` and `V5-F1` match as before. |
   | F4 obvious version: `restored is not True` → UNKNOWN | **3 failed** (judged-only tests that have no matrix.json) |
   | F5 strict: a mutant that turns every probe red gives no PASS | **4 failed**. The frozen PASS fixture has only one probe. |
   | F5 guarded: same rule, but only when the mutant has 2 or more probe results | 79 passed |

   I then ran the current `verdict.decide()` against the F1 and F5-guarded versions on all 10 recorded runs. Result:
   **0 case changes and the same `meets`** everywhere. That is a null result (my #9): the existing calibration never
   exercises these failure modes, so "5 of 6 seeded faults caught" tells us nothing about F1, F4 or F5. Each of them
   needs a fixture built for it.
5. **The order** (my #8, one path at a time). Within each round, cheapest first. Run the full suite and the
   recorded-runs control after every fix, not once at the end.
   - **Round A, false PASS or MEETS:** F1; F5 (the guarded rule now; later an optional top-level key in
     `probe_matrix` for why a run went red, which is a DATA.md contract change); F4 (take the baseline before the
     product run, and treat a missing `restored` as not restored only when matrix.json exists); F19 (the runner
     returns `verdict.json` raw, which reduces the risk without removing it); F10 with F12 (refuse a reused runId that
     holds model files, keep `runId` inside `runs/`, and add F17's "wrote no file" check here); F11 (wrong-shaped
     model JSON exits 2).
   - **Round B, a requirement dropped or uncounted:** F14 (compare a raw count of ids with the manifest); F3 (one id
     grammar, imported from `spec_parse`; there are three copies today and only the last differs); F20 (report
     probes that cite no case or an unknown case); F15 (two classify entries for one case → human).
   - **Round C, blindness:** F8 (defaults stay, `--exclude` adds; exclude nested `tests/`, `test_*.py`, `conftest.py`
     and build notes); F2 (move `plant_case` out of `judge-input.json`; `plants.json` is still readable, so this
     narrows the leak without closing it); F9 (detection only within one session; real enforcement needs OS-level
     isolation).
   - **Round D, defer:** F6 and F7 are missing features, not wrong answers, and both end in the safe direction
     (UNKNOWN). F13, F16, F17's model-used check and F18 are reporting gaps.
6. **Nature analogy for F5** (my #6, my #7). A T cell is activated only by two signals: a specific one and an
   independent one confirming real danger. Borrowed: PASS needs a specific signal (the cited probe is red on its
   mutant) plus a "the run was healthy" signal (some other probe stayed green, or an explicit no-timeout record). In
   the body the second signal comes from a separate cell, but here both come from the same pytest run. That covers
   timeouts and whole-product breakage; it does not cover a syntax error that breaks only the cited file.
7. **How sure I am** (my #10). The frozen-test results are deterministic, so they are solid. The calibration
   observations come from one product and 9–10 runs, all with a single judged case: a hint, not a law. Whether
   rounds A to C fit in one session is my reading.

## What I need to know
- **DATA.md:** may E6 gain an optional mutant-error key, and may a missing `restored` mean "not restored"?
- **F6 and F7:** both are accepted requirements, so deferring them leaves the evaluator short of its own spec.
- **F10:** refuse a reused runId (my default), or move the old files aside?
- **F11:** does the workflow stop on exit 2?
- **F2:** is there a product with 2 or more judged cases? Without one, the F2 fix cannot be measured.
- **K2 rerun:** `k2_score.py` reads the fault list from a session scratch path; it needs a home that survives and
  that workers still cannot read.

## Costs and risks
- **F4 obvious version:** breaks 3 frozen tests, measured. The guarded version costs one more condition.
- **F5 strict version:** breaks 4 frozen tests, measured. The guarded version still has a one-probe hole and a
  single-file syntax-error hole.
- **F5 full version:** must be an additive, optional key, or it breaks the exact-equality frozen tests (my reading).
- **F3:** the first character becomes uppercase-only, measured with 0 frozen failures.
- **F8:** wider excludes could strip a product file named `test_*.py` (my reading).
- **F10:** wiping a reused folder destroys evidence; refusing costs the operator a new runId.
- **F2 and F9:** narrowed, not closed.
- **The control:** the recorded runs cannot show the F1 and F5 fixes work; only new fixtures can.

## How we would know I was right
- **Per fix:** a new test is red with the fix undone and green with it; the 762 tests still pass; the harness stays
  at 10/10.
- **Control:** re-deciding the 10 recorded runs gives 0 case changes, except changes stated in writing beforehand.
- **Fixtures:** an empty spec → MEETS no; a hanging mutant or one that breaks every probe → UNKNOWN; a probe writing
  into the product copy → `restored: false`.
- **K2 rerun:** at least 5 of 6 seeded faults still caught.
- **Self-evaluation on the EV spec after F3:** the "no probe" UNKNOWNs drop from all of them to fewer.

*(Saved by the COO from Dave's hand-back. Dave wrote scratch files only, outside the repo: `/tmp/dave-exp/` and
`/tmp/dave-scripts/`.)*
