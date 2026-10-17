# Report — review-enhance of memory-check (run 20261017-memory-check-review)

Written by the workflow's report step; its Write was refused ("Subagents should return findings as text"), so the main
agent saved the text it returned, with the main agent's corrections marked **[main agent]**.

## Bottom line
- Round 1 ran its reviews: Codex 12 findings (11 P1, 1 P2, `review/r1-codex.md`), agy 5 (`review/r1-agy.md`; its
  output starts with leaked thought text).
- **The judge step failed**: its model call was refused by the model's safeguard filter (API error, request
  req_011Cg82MiozZjQKgNC1Woo4f). No `findings.md` exists; the 17 findings are **unjudged**. **[main agent]** The
  workflow then went on to the enhance step instead of stopping — a bug in `review-enhance.js`, fixed after the run: a
  judge that returns nothing is retried once, then the rounds stop with a problem and nothing is fixed or enhanced
  (harness check 8).
- The experts picked two enhancements (`enhance.md`); both were reproduced as failing tests and built.

## Enhancements picked and built
- **E-1** (5 of 6 experts): a check that could not read its input never reads as clean — `memory_check/src/checks.ts`
  (runChecks, sotResult, decidedByTool), `memory_check/src/cachechecks.ts` (checkRd1).
- **E-2** (2 of 6 experts, both with a probe): `--out` may never overwrite memory — `memory_check/src/command.ts`; a
  memory target is exit 2, nothing written.
- Reproduced red first: `nodes/reproduce-enh.red.txt` (E-1 4 rows, E-2 5 targets; 4 controls green).
- Verified (23:45): `bun test` 87 pass, 0 fail (baseline 74); pytest 465 passed; tsgo clean; smoke run exit 0.
- **[main agent]** The report step called the tests not independent; they are: the reproduce step (a Claude agent)
  wrote `memory_check/test/review-enh.test.ts`, and opencode wrote the fix.

## Open
- Judge the 17 raw findings (12 Codex, 5 agy); fix the accepted ones.
- **[main agent]** C3 ("never changes `memory_index.py`") conflicted with the owner's "memory_index.py in scope";
  the owner's decision is newer, so C3 is amended (2026-10-17).
- The owner: which agent-memory location F1 names; a real project to calibrate on (U6).
- Not measured: that memory-check's staged read uses the same `[DFLOH]-*.md` filter as `memory_index.py`.
