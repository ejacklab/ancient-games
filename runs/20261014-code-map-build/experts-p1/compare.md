# Four experts on the unclear spots (method 3.3), merged with the COO's measurements

Answers: `answers/linus.md`, `sun-tzu.md`, `lao-tzu.md`, `dave.md`. Measurements:
`../evidence/p1-experiments-summary.md`. `check`: 4 pass; the fan-li FAIL is expected, since 范蠡 was not asked.

| Spot | Experts (short) | Measured since | Where it stands |
|---|---|---|---|
| U1 accept the requirements | all: EJ's decision; it blocks only P3 | — | **EJ** |
| U2 implementation-lookup misses | Dave and 孫子: test it; 老子: keep both paths and record `via`; Linus: one success is not a miss rate | E2: 63 of 71 tags resolve to one implementation, 7 to several, 1 to none | settled: the stock lookup, plus a wiring rule for "several". Spec gets `via` (老子) |
| U3 tests with mocks | Linus and 老子: a test that swaps in a mock reaches the mock, not the real function; Dave: EJ decides | E3: 1 real and 19 mock implementations at `edit.ts:275` | **EJ** (the mock rule); the per-test-file wiring rule is needed either way |
| U4 entry flows | 老子: keep only "exported and used outside"; Linus: show the consequences first | — | default: 老子's rule |
| U5 siblings | Dave: by declared type; 老子: same exported member names, as candidates; Linus: underspecified | — | experiment on `tool/plugin` in P3 (A1) |
| U6 `find` from words | all: rank candidates, flag ambiguity, measure later; "found" (top 1 or top k) is EJ's | — | measured in P4 and P5; threshold left open |
| U7 keys share a blind spot | Dave: recheck a sample with a planted rename plus tsgo; 老子: check each tool claim at its own line; 孫子: quote_check cannot check readings | — | default: both (Dave's, in a copy of the clone; 老子's in the evaluator) |
| U8 Codex quota | Linus: wait, never pass an unavailable check; 老子: pick a substitute now | — | default: wait and log the stop |
| New: references are not calls (Dave N1, Linus N2) | — | E1: 18 calls, 1 shorthand; callers sit in anonymous bodies | spec: a caller edge only where the reference is called; name the enclosing `Effect.fn` const or property |
| New: one src+test program (Dave N2, Linus N1) | — | E3: builds in 2.8 s, about 896 MB, resolves to `.ts` | settled |
| New: packages/ai (孫子 N5) | — | E4: builds in 0.9 s, about 252 MB | settled |
| New: R3 network check (孫子 N1, Linus N3) | — | E5: `unshare -n` fails; `unshare -rn` works | spec: `unshare -rn`. R3's git and engine parts are checked as "writes nothing outside its output" |
| New: map size budget (老子 N1) | — | — | spec: `map` prints a budgeted summary, and the rest is reached by narrower questions |
| New: tools + permission is two paths (老子 N2) | — | — | spec: `map` takes several paths |
| New: P5 tuning on the keys (Dave N4, Linus N4) | hold some questions out | — | default: half of each module's questions held out |
| New: noise between runs (Dave N5) and a reading-arm ceiling (老子 N3) | — | — | default: 2 runs per arm; both arms get the same stopping instruction |
| New: P6 "blind" undefined, `claude -p` token fields unproven (孫子 N2, N3) | — | — | prove the token fields before P5; define blind as "labels hidden, input words replaced", as in the POC |
