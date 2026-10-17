status: done

Both picks of `enhance.md` are implemented: every "pass" or "not applicable" now needs a read that worked, and `--out`
can no longer reach a memory location. `test/review-enh.test.ts` is green and nothing else moved.

## E-1 — a check that could not read its input never reads as clean

- `memory_check/src/checks.ts` `runChecks`: the staged `git ls-files --cached -- project-memory` read keeps its own
  reasons (`memoryPathErrors`, folded into `snapshotGitErrors` for the notes), so `StagedRead.failed` / `.reason` say
  whether "no memory" was read or only failed.
- `memory_check/src/checks.ts` `sotResult`: a failed staged read turns the "not applicable" return at :212 into
  "could not run" naming the git error, for every record but the `OUTSIDE_PROJECT_MEMORY` exemption and guidance
  records (E-1a).
- `memory_check/src/checks.ts` `decidedByTool`: with `checks` including `tool`, `(run.noMemory || run.unbornHead)`
  while the staged read found memory is "could not run" through `indexChecksNotReached` — it sits after the break
  check and before `AFTER_ENTRIES` (:262) and the final pass (:282), so a real fail still wins and the exemptions
  still get their own result (E-1c unborn HEAD, E-1d SHA-256 ids).
- `memory_check/src/cachechecks.ts` `checkRd1`: an unreadable session-start file is collected instead of skipped, and
  a scan with one is `couldNotRun` (a break still outranks it), so Rd1 is not a pass (E-1b).

## E-2 — `--out` must never overwrite memory

- `memory_check/src/command.ts` `realTarget`: resolves `..` and every symlink along the path, for a file that does
  not exist yet (deepest existing ancestor realpath'd).
- `memory_check/src/command.ts` `memoryTargets`: the F1 locations as paths — `AGENTS.md`, `CLAUDE.md`,
  `project-memory/INDEX.md` as files; `entries/`, `work/`, `journal/`, `.cache/` and `<home>/.claude/agent-memory`
  as folders.
- `memory_check/src/command.ts` `outMustNotBeMemory`, called in `main` inside the usage try-block before the run:
  a memory file, or any path inside a memory folder, is a usage error — exit 2, nothing written.

## Checks

- `cd memory_check && bun test` → `87 pass` / `0 fail` — `Ran 87 tests across 4 files. [10.17s]`
  (baseline 74; +13 from `test/review-enh.test.ts`)
- `python3 -m pytest -q tests/test_memory_index.py tests/test_memory_index_unit.py` → `465 passed in 29.85s`
- `cd memory_check && ./node_modules/.bin/tsgo --noEmit -p .` → no output, exit 0
- This repo's own report, unchanged: `0 fail, 3 pass, 3 needs a reviewer, 72 not applicable, 0 could not run`, exit 0
  (matches `runs/20261017-memory-check/report.md:23`).

## CONTRADICTS

none