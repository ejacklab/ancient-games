# Dave — smallest experiment for each unknown spot (method 3.3)

## Answer
Five spots are of kind *unknown*: U2, U3, U5, U6 and U7. Each one can be settled by a small experiment that only reads the code, runs no engine and writes only to `runs/20261014-code-map-build/evidence/`. All of them except the second half of U6 can run before EJ accepts the requirements (U1), because they only measure. I would run them in this order: N1, U2, N2, U3, U7, U5, the U6 baseline, then N5 before P5. I would write each prediction into `state.md` before the run starts. I leave every pass/fail threshold open for EJ.

| Id | Kind | My verdict |
|---|---|---|
| U1 | decision | EJ's to make. The experiments below can inform it, and none of them needs it first. |
| U2 | unknown | **Test.** Run the implementation lookup on one call site per service tag, and compare it with the static Effect rule on the same sites. |
| U3 | unknown | **Test, after N2.** Use the three test files the research already cites, whose answers are already known from reading. |
| U4 | decision | EJ's to make. A cheap count could inform it (see step 9). |
| U5 | unknown | **Test on one folder** (the tool plugins). Compare two detection rules against the key. |
| U6 | unknown | **Split it.** Measure the grep baseline now; test `find` in the A2 round, on the same questions, with no tuning on them. |
| U7 | unknown (risk) | **Test.** Re-check a sample of the key claims that came from reading, using a method other than reading: a planted rename plus `tsgo`. |
| U8 | information | **One canary call** right before P2 and again before P3. What to do if the quota is gone is a question for EJ. |
| N1 | unknown (new) | **Test first; it is nearly free.** The 19 references from the probe were never checked one by one. |
| N2 | unknown (new) | **Test.** Does one program over `src` and `test` build, at what memory, and does it still resolve to `.ts` files rather than `.d.ts`? |
| N3 | decision (new) | **For EJ.** If a test swaps Permission for a mock, does A3 count that test as reaching the real `assert`? |
| N4 | unknown (new) | **For EJ.** P5's "improve and rerun" reuses the same fixed questions, so it tunes on the answer keys. Should some questions be held out? |
| N5 | unknown (new) | **Test before P5.** How much do two identical runs of the same arm differ? Without that, a difference between the two arms cannot be read. |

I recommend dropping none of the spots.

## How I decided
1. **What would change my mind (my #1).** For each unknown I named the observation that would change the design:
   - U2: a single established implementation that the lookup misses means the static Effect rule has to be built.
   - U3: if the lookup returns one implementation per test, no per-file `.replace` rule is needed.
   - U7: if one key claim turns out wrong by an independent method, the keys are not fit to use as answers yet.
2. **Use the data we already have (my #5).** What has been measured:
   - one call site, `edit.ts:275` → `permission.ts:231`;
   - 19 references in 17 files, not checked one by one;
   - grep counts: 94 `Context.Service` classes in 91 files, and 93 `Service.of(` calls in 87 files (F16);
   - three test files with known wiring (F12): a mock in `mcp.test.ts`, a fixture in `tool-edit.test.ts`, the real node in `permission.test.ts`;
   - the keys: 43 claims checked by grep, 145 by reading, and quote_check confirms quotes only.

   What none of this shows: any miss rate, anything about the test program, anything about siblings or ranking. For that reason N1 comes first: its data already exists and only needs checking.
3. **U2, smallest reversible experiment (my #8, my #2).**
   - **Run:** for each of the 94 tags, take one member and one call site from `findReferences`. Call `getImplementationAtPosition` there and record one of four outcomes: Effect.fn body, something else, nothing, or several.
   - **Control (my #4):** apply the static Effect rule to the same sites. Hand-check every site where the two disagree.
   - **Price:** one LanguageService build (about 2.1 s, about 663 MB) and no Codex quota.
   - **Prediction (my #3), my reading from n=1:** most sites resolve to the Effect.fn body. The misses cluster in services whose layer does not end in `Service.of({shorthand})`, such as spreads, factories, or `Layer.succeed` with a literal. The gap between 91 files and 87 files in F16 points there. That is a hint, not evidence.
   - **Stop:** the fixed sample is fully classified. It does not grow without EJ.
   - **Why "any miss" is the trigger:** R2's Fails-if already counts an established implementation with no link as a failure. That makes this a comparison, not a new number. Who decides that an implementation is "established" is an open question (see below).
4. **N1 before U2 (my #5, my #8).**
   - **Run:** check the 19 references against the code, using quote_check plus the enclosing function of each one.
   - **Prediction:** at least two of the 19 are not call sites: the interface declaration at `permission.ts:106` and the shorthand in `Service.of` at `permission.ts:339`. If the tool turned every reference into a caller edge, it would invent callers.
   - **Stop:** all 19 are labelled.
5. **N2, then U3 (my #8).**
   - **N2 run:** build one program holding both `src` and `test` (262 test files), and record its time and heap. Check that `edit.ts:275` still resolves to `.ts` files and not `.d.ts` (the digest's caution).
   - **N2 prediction:** it builds; the heap is above 663 MB; whether it resolves to `.d.ts` is unknown.
   - **U3 run:** in that program, run the implementation lookup at `edit.ts:275`. Compare what it returns with the three test files whose answer is already known from F12.
   - **U3 prediction:** it returns several implementations, the real `assert` plus mock arrows from `Layer.mock`. That is the research's inference I4, which was never measured. If so, the lookup cannot choose per test, and a per-file `.replace` rule is needed.
   - **Stop:** the three files are classified.
   - **What remains for EJ:** whether a mocked test "reaches" the function is not something an experiment can settle. That is N3.
6. **U7 (my #4, my #10).**
   - **The concern:** the keys and the plain-reading arm come from the same model reading the same code, so they can share a blind spot.
   - **Smallest independent check:** for a sample of the claims made by reading, rename the target in a scratch copy of the clone and run `tsgo`. Its error list names the real callers. Then restore with git.
   - **My proposed sample:** one claim per question, 30 in all. That is my number, not EJ's.
   - **Prediction (my reading):** most claims hold. Wrong ones cluster on injected-service calls and on "nothing else calls X" claims, which are exactly where the tool is supposed to win.
   - **Stop:** the sample is checked. Every wrong key is reported (my #9) and fixed before P4.
   - **Rule:** the COO runs this, since the keys stay COO-only. I did not open them.
7. **U5 (my #6, my #7).**
   - **The analogy, my reading:** biology tells true kin (homology: a shared ancestor) from look-alikes (convergence: the same shape, evolved separately). The spec's "same shape in one folder" rule would admit look-alikes, because TypeScript matches types by shape, not by declared type.
   - **The candidate it suggests:** treat files as siblings when they satisfy the same declared type or factory, as checked by the type checker.
   - **Does the analogy fit (my #7)?** The key condition holds: there is a checkable "ancestor" (the declared type). What differs: code has no gradual descent, and a shared ancestor does not prove the same concerns.
   - **Run (my #8):** both rules on `core/src/tool/plugin` only, compared with the key.
   - **Prediction:** the shape rule picks up extra helper files and misses siblings that live outside the folder. The declared-type rule picks up fewer extras.
   - **Stop:** one folder is done. Only then try the providers folder.
8. **U6 (my #4, my #3).**
   - **Now:** the control can run before the tool exists. Run plain grep, using each key question's own words, and record the rank of the known place.
   - **In the A2 round:** run `find` on the same questions.
   - **Prediction:** `find` beats grep when the question's words appear in identifiers or comments. It loses on synonyms, meaning domain words that are not in the code.
   - **Stop:** one pass. No ranking tuning on the key questions, or the keys become training data (N4).
   - **What "found" means** (top 1? top k?) is EJ's to set. I leave it open.
9. **U4 and U1 are decisions (my reading).** A cheap count could help EJ with U4: on one module, count the entries under each half of the proposed rule. My prediction: "nothing in the module calls it" also catches dead and test-only helpers. The decision itself stays with EJ.
10. **N5 (my #10).** P5 and P6 compare one run per arm. Before comparing arms, run the reading arm twice on one question and measure how far tokens, time and correctness move. Prediction (my reading): tokens vary noticeably between identical runs. If they do, one run per arm is a hint (n=1), not a result.
11. **Report every outcome (my #9).** Every experiment above goes into `state.md` with its prediction and its outcome, including a prediction that turns out wrong.

## What I need to know
- **R2, "established":** who establishes that an implementation exists for U2's check? My default is a hand check of every site where the lookup and the static rule disagree. If EJ prefers another way, U2's control changes.
- **U6:** what counts as "found" for A2: the top result only, or within the top k? I leave it open.
- **U7:** how many wrong keys in the sample would mean redoing the keys, rather than fixing them one by one? Is one claim per question (30) an acceptable sample?
- **N3:** does a test that replaces the service with a mock count as reaching the real implementation?
- **N4:** should some questions per module be held out of P5's improve rounds? If so, how many?
- **N5:** how many repeats per arm in P5 and P6?
- **The planted rename for U7:** may the COO make a temporary change in the opencode clone and restore it with git, or must it work in a separate copy? Q2 covered `bun install` only.
- **Before U1:** may these measurement-only experiments run before EJ accepts the requirements? If not, all of them wait for U1.

## Costs and risks
- **U2 (my #8):** a sample of one site per tag can miss a rare pattern. "No miss in the sample" is not "no miss" (my #10).
- **U2 (my #4):** the control's ground truth is a hand check. That is the same kind of method as the keys, so it can share their blind spot.
- **N1 (my #5):** costs one pass over 19 lines. The risk is low.
- **N2 (my #8):** a combined program may need well over 663 MB. If it resolves to `.d.ts`, A3 needs a different setup, which means a design change before P3.
- **U3 (my #10):** three files is n=3. It shows whether the problem exists, not how often it happens.
- **U7 (my #4):** a planted rename touches the target repository. If restoring it fails, the clone stops matching `6dc4d4e`, and every later measurement is off. Use a copy, or check `git status` afterwards.
- **U7, test-only claims:** a renamed target only exposes callers the compiler sees. A claim about tests is still unchecked unless the test program from N2 is included.
- **U5 (my #7):** the analogy may push toward a rule that misses siblings with no shared declared type, if opencode's plugins are not typed through one factory. I have not checked that. It is a condition, not a fact.
- **U6 (my #3):** a grep baseline run on the keys means someone has seen the questions. Keep the baseline output COO-only, like the keys.
- **N4 (my #4):** holding questions out leaves fewer for improving the tool. Not holding them out lets P5 report gains that may not survive new questions.
- **N5 (my #2):** repeats double the cost of the arms. Skipping them means a single-run difference cannot be told apart from noise.
- **U8:** each canary costs one call of Codex quota.
- **Overall (my #2):** about seven small scripts and no engine calls beyond the canaries. The price is wall time before P2 and P3, against the cost of building R2 or A3 on an untested assumption.

## How we would know I was right
- Each prediction above is written into `state.md` before its experiment runs. Afterwards, each one is marked held or failed, and failures are reported with the same weight (my #9).
- Checkable predictions:
  - **N1:** at least two of the 19 references are not call sites.
  - **U2:** misses, if any, cluster in layers that do not use shorthand `Service.of`.
  - **U3:** the combined program returns more than one implementation at `edit.ts:275`.
  - **U5:** the shape rule reports more extra siblings than the declared-type rule on the tool-plugin folder.
  - **U7:** wrong keys cluster on injected-service and absence claims.
  - **N5:** two identical runs differ in tokens.
- **The test of the approach itself (my #2):** each experiment should change, or firmly confirm, a design choice: whether the static Effect rule is built, how A3 handles mocks, which sibling rule is used, and whether the keys are fit to use. If none of them changes anything, the experiments cost more than the debate they replaced, and I was wrong to put them first.
