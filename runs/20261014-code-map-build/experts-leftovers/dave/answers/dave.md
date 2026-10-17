# Dave — eight code-map decisions for the opencode run

## Answer
I agree with the COO on six decisions. I differ on two: **3** (b, not c) and **6** (c for now, not a). I also add one clause to **1**, so that a false `dynamic` label cannot excuse a link. Every pick is provisional. Each one has a cheap test, listed below, that would confirm it or flip it.

| # | My pick | One-line reason |
|---|---|---|
| 1 | **a, with one change:** "a known link within the depth is missing with no limit at its site naming why, or a shown link **or a limit** contradicts the code" (the rest of the line as settled in round 2) | L1 already names "dynamic behaviour" as a reason to stop, so b would make A2 fail what L1 allows. But a on its own lets any `dynamic` label excuse a direct call the type checker resolves, and no other line charges a false limit. |
| 2 | **a** | A2's unit is the link, and going into a body written straight into a call is not a call in the source. Counting it would also change the levels when someone rewrites a plain function as `Effect.gen`: a style change would read as a logic change, against "track changes". |
| 3 | **b** | "Known" must be something a key writer can establish without the tool's own method, which is the control (my #4). c's link half makes the type checker judge the tool's links, so links the type checker cannot see, such as a callback passed as a value, drop out of A2 with no flag. With 1's wording, nobody needs c to settle 1 any more. |
| 4 | **b, provisional** | No failure on record shows that "its limits" misses an interface-required limit. A planted copy that drops "fake rule not set (A3)" settles it: if A5's line does not charge it, switch to a. |
| 5 | **b** | The evaluator gives one verdict per Fails-if line (spec.md:150, 155–157) and already separates the tool's part from the agent's (spec.md:162–164). A line naming both actors cannot carry one verdict. |
| 6 | **c for this run.** Run with no `--fake-rule`; the spec's undecided path already gives c (spec.md:121–122) | a is the right rule for a test that really swaps in a fake. But `throughFake` marks every path through a call site whose candidates include a fake (spec.md:117), and the tool has no rule for Effect wiring (spec.md:99–100). So at the site with 1 real implementation and 19 fakes, exclude would also drop tests that wire the real one. Switch to a once that is measured. |
| 7 | **c, with a's rule as the check on each glob** | The interface takes one glob per group (spec.md:131). a's interface rule, my P1 pick, is not an input the tool takes, so it becomes the control instead: every file a glob matches must implement that group's service tag. |
| 8 | **b in the tool, a on opencode** | Test layout differs from repository to repository, so a default in the tool would be a guess. On opencode, a covers the `test/` folders the case files already use (spec.md:189–190); widen it if a fake turns up outside them. |

## How I decided
1. **my #1:** for each decision I first named the observation that would flip it. They are under "What I need to know" and "How we would know I was right". A decision with no such observation (2, 5) rests on the unit or the spec's structure. Measuring would not change those two.
2. **my #5, the data I have:**
   - the probe found 63 of 71 service tags with one implementation, 7 with several and 1 with none (COO's facts, brief);
   - one call site has 1 real implementation and 19 test fakes (COO's facts);
   - the confirmed default-text false pass on A5 (round-2 answers);
   - 范蠡 found no failure traced to the word "known" (r2 `fan-li.md`, step 3).

   What this data does not show: how many `dynamic` limits the tool emits on opencode, how many tests through fake-bearing sites wire the real implementation, and which test pattern the probe used. The COO's "about half as far" on decision 2 is marked *not measured* in the brief.
3. **my #9 and my #2:** two wording rounds left "known", the interface-required-limit clause, and both of the owner's questions unsettled (compare.md, rows 2 and 6, and the "Questions only the owner can settle" section). That is a null result, and I report it as one. Every test below costs less than a third round.
4. **Decision 1** (my reading of result-trimmed.md):
   - L1 (lines 88–89) lists "dynamic behaviour" as a named reason to stop early, so b would make A2 contradict L1.
   - R2's Fails-if line "an implementation the lookup finds has no link" (line 36) charges a false `dynamic` label only on a service or interface call. For a direct call, nothing charges a limit that states a false reason. L1 only fails a stop with *no* reason.
   - Widening "a shown link contradicts the code" to "a shown link or a limit" closes that gap without a new line. A `dynamic` limit on a call the type checker resolves contradicts the code; on a computed member it does not.
5. **Decision 3:**
   - **my #4:** a check whose key comes from the tool's own method has no control. 老子's own cost line concedes this for c ("makes the key for the missing-link line as dependent as the tool's own reading", r2 `lao-tzu.md`).
   - The lesson *criteria-name-outcomes* points the same way: define "known" by what the evidence establishes, not by a mechanism.
   - **my #10, how sure:** low. The probe covers service tags only. There, b and c could give different verdicts at most on the 1 tag with no implementation, and with 1's wording an honest `unresolved` passes under both. Where they would differ more (callbacks, computed members) is not measured.
6. **Decision 2** (my reading, with the vision's line 13, "track changes"):
   - Three of four experts keep "each link adds one level" (compare.md, row 4).
   - Linus: "No extra chain level follows merely from lexical nesting."
   - **my #3:** the COO's reach estimate is a prediction and should be written down before anyone measures it. It does not decide my pick, which rests on the unit.
7. **Decision 4:**
   - **my #5:** no recorded failure.
   - **my #8:** adding the sentence later costs one sentence, so wait.
   - **my #2:** the planted test is cheaper than the 2–2 argument.
8. **Decision 5** (my reading of spec.md:150–164): one verdict per line forces one actor per line. A2 stays one requirement; only its bullets are separate. That is not a split.
9. **Decision 6:**
   - **my reading:** spec.md:117 marks `throughFake` by the call site's candidate list, not by what the test wires.
   - **my #6:** *recall*, and it does not decide. Immune cells tell self from non-self by each cell's own marker, not by the tissue around it. The mechanism to borrow: classify each test by the implementation its own setup wires.
   - **my #7:** what is the same is classifying individuals in a mixed population. What differs is that a cell's marker is always visible, while a test's wiring may sit in helpers that static reading cannot follow. That key condition is unknown, so I use the analogy only to design the measurement (test 6 below), not the rule.
   - **my #8:** the no-flag path costs no code and is reversible.
10. **Decision 7:**
    - **my #9:** my P1 pick (a) does not fit the interface as built. I report that and move to c.
    - **my #4:** a becomes the control on each glob.
    - **my #8:** fix the `tool/` glob first, check it, then do the other two modules.
11. **Decision 8:**
    - **my #5:** the case files already use opencode's `test/` folders (spec.md:189–190).
    - **my reading:** extra patterns that match nothing cost nothing.
12. **Insights:** `runs/20261014-code-map-build/insight.md#F-60cad515` (read an answer only after its run passed). I relied on the round-2 answers only after compare.md's check line said all four ran, with 范蠡's answer saved by the COO. It changed no pick. No category was named. Going by the index's check column, the other rows are about the guard, hooks, criteria and expert runners, not code-map wording. I read only their index rows, not their sections.
13. ***Proposed change to the pattern*** (my #2, my #9): when two wording rounds leave the same split, make the next trial a planted-copy or counting experiment, not a third wording round. What it changes: the "three failed trials" before a question goes to EJ would include at least one measurement.

## What I need to know
1. **For 6:** of the tests whose path passes the site with 1 real implementation and 19 fakes, how many wire the real implementation? *If none,* exclude loses nothing and I switch to a. *If any,* c stands, because exclude would drop a test with a known path (A3, line 75).
2. **For 3:** on the three A6 modules, are there links an independent reader establishes from source that the type checker does not? *If none,* b and c give the same verdicts and I would not hold out against c.
3. **For 4:** does the evaluator's A5 line charge an answer that drops "fake rule not set (A3)"? *If not,* switch to a.
4. **For 7:** can `--siblings` exclude a file, as in "`tool/*.ts` minus the registry"? The spec says only "one glob per sibling group" (spec.md:131). *If not,* either the spec gains exclusion or the group is given file by file.
5. **For 8:** which test pattern did the probe use for its 63/7/1 count, and is any candidate of the 7 tags with several implementations a fake outside pattern a? *If yes,* widen a for opencode.

## Costs and risks
- **1 (my #4):** every `dynamic` limit needs a key decision on whether the type checker resolves that site, which costs review time. The new words also change a Fails-if string, so case `line` fields must be re-mapped.
- **2 (my #10):** the level number no longer shows nesting, so the agent must read `from`. A body the framework never runs still shows its calls at level 1. Lexical ownership does not prove invocation (Linus, r2).
- **3 (my #4):** b is broad; 范蠡 says it "rules out nothing", so key writers may over-claim. With 1's wording an honest limit still passes, so the tool pays in flags, not failures. If A1 and L2 do not take the same sense, "known" carries two senses (孫子, question 5).
- **4 (my #8):** if "its limits" is read as only the limits the tool chose to emit, a dropped required limit passes until the planted test runs.
- **5 (my #10):** new strings mean re-mapping case `line` fields. 老子 counted 10 of 70 cases; I did not check that count.
- **6 (my #8):**
  - every `tests` answer through a fake-bearing site carries an undecided list and a limit, which means more tokens, against the vision's "fewer tokens than reading" (line 16);
  - the count is a lower bound until the rule is set;
  - the owner may read leaving the A3 rule unset as against their intent.
- **7 (my #4):** each module's glob needs upkeep. Without exclusion, the registry enters the `tool/` group. The check catches it, but the sibling table has a wrong member until the glob is fixed.
- **8 (my #5):** a fake outside the four patterns counts as real and can turn a resolved target ambiguous (R2, line 38).

## How we would know I was right
Write each expected result down before running (my #3), with the run's deadline as the stop date. Report a null result with the same weight as a success (my #9).
1. **Planted copy for 1:** it marks one direct call the type checker resolves as `dynamic` and drops the link. Expected: my wording gives A2 NOT MET; the COO's 1a alone gives MET, a false pass. Control: the unplanted tool gets the same verdict under both wordings.
2. **For 2:** rewrite one fixture function from a plain function into `Effect.gen(function* …)` with the same calls. Under a, the `chain` levels stay the same; under b, they shift. Separately, measure how far depth 6 reaches on one session entry under both counts, against the COO's written prediction.
3. **For 3:** for every `dynamic` or `unresolved` link on the three modules, an agent that does not use the tool says whether the source establishes the target. Count the sites where b and c give different verdicts. A count of 0 means the choice changed nothing.
4. **For 4:** a planted copy that drops "fake rule not set (A3)" must make A5 NOT MET.
5. **For 6:** at the site with 20 implementations, an agent reads each test whose path passes it and records real, fake or cannot tell. If every test is fake, switch to a; if any is real, c is confirmed.
6. **For 7:** for each glob, every matched file implements the same service tag, and the `tool/` registry is absent.
7. **For 8:** re-run the resolution count with pattern a and compare it with the probe's 63/7/1 as the control. If any target moves between resolved and ambiguous, explain it file by file.
