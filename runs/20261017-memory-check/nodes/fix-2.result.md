status: done

All fourteen findings of `runs/20261017-memory-check/nodes/review.codex.md` are fixed in `memory_check/src/`: the fifteen tests of `memory_check/test/review.test.ts` (one per finding) pass, and the fifty-five of `memory_check/test/acceptance.test.ts` still do.

## Per finding

1. **An unmapped `memory_index.py` failure is never a pass** — `indextool.ts` `runMemoryIndex` now records `crashed` (a traceback, an exit code no check uses, no python3) and `unmapped` (error-level lines that name no requirement id, collected only before the size line, so a diff is never one); `checks.ts` `decidedByTool` answers "could not run" for every tool clause it finds no break in. A python that only crashes was silently passing before: it now exits 1.
2. **The clauses the tool never reached** — `indextool.ts` adds `measured`/`compared` and `indexChecksNotReached`; `checks.ts` holds `AFTER_ENTRIES = K6.1a, K6.2, Rd3.1a`, which answer "could not run" while `run.compared` is false. The recognisers are built from `INDEX_NAME` (`project-memory/INDEX.md`), which is what the tool prints, so an oversized index that also mismatches now gives Rd3.1a "could not run" and K6.1a/K6.2 "fail" as the script itself does.
3. **Presence and bytes from the staged state** — `gitchecks.ts` `stagedMemoryPaths`; `checks.ts` `runChecks` decides "project-memory/ is there" from `git ls-files -z --cached -- project-memory` (bytes already came from `stagedEntries`). `locations.ts` `hasProjectMemory` is gone. The filesystem-only observations are now labelled: F1's evidence says the location table is the working tree, and the cache requirements say the cache folder is a git-ignored working-tree folder in no snapshot.
4. **Staged deletions and renames** — `gitchecks.ts` `stagedNameStatus` (`git diff --cached -M --name-status`) is added to `entryDeletions` and `entryRenames`; `whereOf` names them "the staged state". Both accept `Rename.commit`/`Deletion.commit` of `string | null` for that.
5. **Every transition, not only the ends** — `gitrequirements.ts` `checkK43` is rewritten over `versionsOf` (the baseline, then one version per commit in the range, then the staged state) and `transitionBreaks` (claim, `source`, `depends_on`, and `covers` needing a `changed:` line that this very transition added, not a total count).
6. **`--since` takes its baseline before the range** — `versionsOf` reads the parent of the range's first commit for the path (`hasParent`, `textAt`), so an entry created before the range is still compared.
7. **A merge that drops a whole entry** — `gitchecks.ts` `entriesDroppedByMerges` compares every parent of every merge with the merge result (`git ls-tree -r`), and K4.1 names each entry a parent held and the result does not. W6.3a is unchanged, so one break is still reported once.
8. **K4.1 with no break is the reviewer's** — `checks.ts` `withReviewer` wraps `fromOutcome` for K4.1 (`git; reviewer`), so a fail is a fail and a cleared run is "needs a reviewer" (C2).
9. **Quoted header scalars** — `entry.ts` `unquote`, the same one `tools/memory_index.py:127` applies, applied to every header scalar before it is compared.
10. **Rd1 decides only clear session-start instructions** — `cachechecks.ts` `readLine` splits a line into clauses, reads the negation per clause, and recognises session-start wording, an opening verb and an indirect call; `checkRd1` returns breaks for a clear session-start open, `unresolved` for one that names the cache at the start of a session without saying what opens it (an indirect call), and `checkRd1`'s `ClauseOutcome.unresolved` reaches `fromOutcome`, which answers "needs a reviewer".
11. **The warning holds no entry text** — `warn.ts` builds each line from the requirement id, a `CATEGORY` phrase for that id, and the file names matched out of the evidence; no evidence prose is copied any more.
12. **A failing git command is "could not run"** — `gitchecks.ts` `gitRead` pushes `git <args> failed: …` into a `GitErrors` list every clause carries; `gitrequirements.ts` `snapshotErrors`/`reasons` turn a non-empty list into "could not run" instead of an empty pass. `rev-parse --verify --quiet` calls are `optional`, because "not there" is a real answer to them.
13. **The launcher disables the cache whenever it is not off** — `cli.ts` re-runs unless `BUN_RUNTIME_TRANSPILER_CACHE_PATH` is `"0"`, bun's own off value, so a caller who set it to a writable directory gets one child run with the cache off and no file written there.
14. **A fenced example is not a second header** — `entry.ts` `headerDelimiters` steps over fenced code blocks before counting `---` lines.

## Commands

- `cd memory_check && bun test` → last lines: `70 pass` / `0 fail` / `988 expect() calls` / `Ran 70 tests across 2 files. [6.59s]` (run three times, the same each time)
- `cd memory_check && ./node_modules/.bin/tsgo --noEmit -p .` → exit 0, no output

## Verification beyond the suite

Probes on fixtures (each built as the review's finding describes it, then read out of the report): a merge that drops a whole entry → `SoT:K4.1: fail` naming the parent and the merge; a `covers` edit whose only `changed:` line came from an earlier commit → `SoT:K4.3: fail`; an oversized index that also mismatches → `SoT:Rd3.1a: could not run`, `SoT:K6.1a: fail`; a python3 that only prints a traceback → every tool clause "could not run", exit 1; `git log` failing → K4.1, K4.3, W6.3a and W1.1a all "could not run"; `At session start, run scripts/warm.sh to prime project-memory/.cache/.` → `CACHES:Rd1: needs a reviewer`; `At session start, never open project-memory/.cache/index.sqlite.` → `pass`; `On demand, open …` → `pass`. A smoke run of the CLI on this repository gives the same counts as `nodes/smoke-report.md` (0 fail, 3 pass, 3 needs a reviewer, 72 not applicable, 0 could not run) and an empty warning.

## CONTRADICTS

None.