# Answer — what memory-check should improve after this review round

## Answer
Do three things, most valuable first. (1) When `memory_check` reads staged entries but `memory_index.py` says it had nothing to check, mark every tool-checked clause `could not run`, never `pass`. (2) Add one fault-injection test over every input the tools read. (3) Only if EJ names a real project with `project-memory/`, run the tool on it once and check each verdict by hand.

## How I decided
1. **What I could read.** `findings.md` and `nodes/fix-r*.result.md` do not exist yet (Glob). `nodes/review-enhance.progress.md` ends with `judge-r1 · start` at 23:11:34 and no finish. I used the raw reviews, `review/r1-codex.md` (12 findings) and `review/r1-agy.md` (5), which are unjudged. A finding the judge rejects, or the fix loop repairs, drops out of my list. I did not run any probes (scratch-repo commands needed approval in this session). Every behaviour claim below is *my reading* of the code, *not measured*.
2. **The pattern in the reviews.** Codex #1, #7, #8 and #10 each turn "the tool could not read or did not see the input" into `not applicable` or `pass`. Agy #1 is Codex #7 again, found independently. The earlier round fixed the same class one instance at a time (commit 24e0fba: "git failures are could not run").
3. **Improvement 1: a general guard in `checks.ts`.**
   - **Case.** `tools/memory_index.py:483-485` returns "nothing to check" with exit 0 on an unborn HEAD, even for a staged check. The Python test for this (`tests/test_memory_index.py:774-785`) only runs `--check HEAD`, so the staged case is untested.
   - **Current handling.** `indextool.ts:100-101,173` records the case, but `checks.ts:262` uses it only for clauses in `AFTER_ENTRIES`. Any other tool clause with no findings falls to `pass` at `checks.ts:282`. So a staged `status: bogus` entry in a repo with no commits probably passes W4.1b.
   - **Shape.** In the tool branch (`checks.ts:237-264`): if `memory_check`'s own staged read found entries and the tool says `noMemory` or `unbornHead`, return `could not run` for every tool clause. Codex #8 (SHA-256 repos) has the same shape; I did not verify it.
   - **Serves.** U2 ("a MUST that fails is shown as passing"), U3 (a could-not-run MUST belongs in the warning), and VISION "Say a requirement passes without the evidence that shows it".
4. **Improvement 2: a fault-injection test.**
   - **What.** One parameterized test: for each input the tools read (git index, instruction files, `.claude/settings.json`, the agent-memory directory, the `memory_index.py` run), make it unreadable or absent in an odd way. Assert that no MUST becomes `pass` or `not applicable`.
   - **Case.** `cachechecks.ts` `checkRd1`'s catch block records "(unreadable)" and continues, so Rd1 can still pass (Codex #10, which I confirmed by reading). `checks.ts:212` returns `not applicable` once memory looks absent (Codex #1, not traced).
   - **Serves.** U2 and VISION "never say a requirement passes without evidence". This is the same kind of fixture U2's minimum acceptance asks for.
5. **Improvement 3, conditional: one real run.**
   - **Case.** `runs/20261017-memory-check/report.md` says "Fixtures only: no real project with `project-memory/` has been checked". `settings-diff.md` records EJ's yes and that the hook is applied, so U3 is live but demonstrated only on fixtures. A glob for `~/dev/*/project-memory/INDEX.md` found nothing.
   - **Serves.** U1/U2 acceptance on a real project.
6. **Left out.**
   - What the last round applied: the could-not-run warning, the unstaged count, the final Not applicable section (`report.md`).
   - The agent-memory path question, which is EJ's call.
   - The warning's file-name regex (`warn.ts:12`, Codex #12 and Agy #5, two engines agree). It is small and is the fix loop's to take. If the judge rejects it, it beats improvement 3 for the third slot.

## What I need to know
1. Which round-1 findings the judge accepted and which fixes landed. If the Python tool is now fixed for the unborn-HEAD and SHA-256 cases, improvement 1 shrinks to the general guard and improvement 2 moves up.
2. Is there a real project with `project-memory/` that I may read? If not, drop improvement 3 and do not build a stand-in. A fixture written to match the tool is not evidence.
3. Does `memory_check`'s staged-entry count use the same filename filter as `memory_index.py` (`[DFLOH]-*.md`)? I did not check `stagedEntries`. If the filters differ, the guard in improvement 1 would raise false could-not-run results.

## Costs and risks
- The guard can be redundant if the Python fixes land. It would then be defence in depth only.
- A false `could not run` on a MUST appears in every session warning (U3), so a wrong guard costs noise in the live hook. Item 3 under "What I need to know" is the thing to settle first.
- The fault-injection test is worth little if the fixing engine writes it, because a check written by the author of the fix is not independent. Have another engine write it (the `crossed-build-check` pattern) and show it failing before the fix.
- Both reviews' claims are the reviewers' own probes. I did not reproduce them. The brief's named files (`findings.md`, `fix-r*.result.md`) were missing, so I could not apply their verdicts.

## How we would know I was right
- **Improvement 1.** Two new tests, each shown red on the current code:
  - A repo with no commits and a staged entry with `status: bogus`, checked with no revision. Every tool-checked MUST is `fail` or `could not run`, none is `pass`, exit is 1, and `--warn` prints a line.
  - A `git init --object-format=sha256` repo with staged entries and a wrong index. The result is the same.
  - The baseline in `state.md` stays green: bun 74 pass, pytest 465 pass, tsgo clean.
- **Improvement 2.** One test table with one row per input the tools read. No row yields `pass` or `not applicable` for a MUST. A new reader added without a row fails the test.
- **Improvement 3.** The report on the named project, with each verdict hand-checked and any disagreement logged.

**Top one:** make `memory_check` report `could not run`, not `pass`, whenever its own staged read and `memory_index.py` disagree about whether entries exist.
