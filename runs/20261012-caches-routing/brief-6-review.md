# Brief 6 — blind review of a design section (run 20261012-caches-routing)

Review the design section `runs/20261012-caches-routing/verify/section-review-copy.md` (cited below as "doc:N"). You
did not write it. Change no files and print your review to stdout.

**Read only these files:**
- the section itself;
- `runs/20261012-caches-routing/bench/results.md` and `bench/results.json`: the benchmark;
- `runs/20261012-caches-routing/nodes/runtime-recall.json`: the test-impact recall against coverage;
- `runs/20261012-caches-routing/queries.json`: the questions and their answers;
- `runs/20261012-caches-routing/nodes/gold-verdicts.json`: the answer check;
- `runs/20261012-caches-routing/nodes/audit-0.json`: the harness audit;
- `runs/20261012-caches-routing/cov/suite-timing.txt`;
- `docs/memory-system/vision-statements/caches-memory-vision-statements.md`.

Read nothing else in `runs/20261012-caches-routing/`.

**Check each item and give PASS or FAIL with doc:N and the line in the source:**
1. **Numbers.** Every number in the section must match its source exactly, allowing for rounding as written.
2. **Claims.** Every conclusion must follow from the numbers it cites. Flag one that overreaches, for example one
   resting on a small n stated as settled, or a comparison across different question subsets.
3. **Labels.** Inference is marked as such ("my reading", "proposed"), and the limits of each check are stated.
4. **Routing table.** Each row's "use" must be supported by its evidence column. Flag any row where another route did
   as well or better on the cited evidence.
5. **Vision.** Nothing in the section breaks a never-rule of the vision. Where it conflicts with the vision, it must
   say so and leave the change to EJ.

Raise only real problems, ones that would make a reader route wrongly. Do not raise style.

**Output:**
- first line: `VERDICT: ACCEPT` or `VERDICT: REPAIR`;
- the five items;
- then the findings, each with doc:N, what is wrong, the source evidence, and a severity (high, medium or low).
