status: done

The four tests of `memory_check/test/enhance.test.ts` pass with the fifty-five of `acceptance.test.ts` and the fifteen of
`review.test.ts`, and only `memory_check/src/` changed.

## Per item

1. **R1, the last `## Not applicable` section** — `report.ts` gained `applicable()`, which every result section (the
   tool's own, MUST, SHOULD, guidance, CACHES.md) now filters through, and `notApplicable()`, which appends a
   `## Not applicable` section after "This run" holding every "not applicable" result through the same `line()` row
   format, sorted by level then id (or `- none` when there are none). No section header follows it.
2. **R1, the unstaged count** — `gitchecks.ts` gained `unstagedMemoryFiles(root)` and `UnstagedMemory`: one read-only
   `git status --porcelain -uall -- project-memory` (GIT_OPTIONAL_LOCKS=0, via `git()`), keeping a line only when the
   working-tree column is `M`, `D` or `T`, or the line is `??` — a change the index already holds is one the checks do
   read, so it is not counted; `-uall` keeps the count a count of files rather than of collapsed folders. A failing
   `git status` is `error`, never `0`. `checks.ts` carries it on `CheckRun`; `report.ts` prints a
   `## Files changed but not staged (R1)` section between the locations and the results with
   `- <N> file(s) under `project-memory/` changed but not staged, and so not checked by this run[: the names, up to 5] (git status --porcelain -uall -- project-memory; the checks read the staged state, C5)`, or `- the count could not be read: …`.
3. **R2/U3, "could not run" in the warning** — `warn.ts` takes every MUST whose verdict is `fail` **or**
   `could not run` (`F1` excepted: the missing `AGENTS.md` keeps its own line), and `SAYS`/`GENERIC` are now keyed by
   verdict, so a line reads `memory-check: SoT:K4.3 could not run — an entry's claim, source, depends_on or covers
   changed without the log line for it`. The line is still built from the id, the category phrase and the file names
   matched out of the evidence — no evidence prose, no entry text.

## Commands

- `cd memory_check && bun test` → last lines: `74 pass` / `0 fail` / `1001 expect() calls` / `Ran 74 tests across 3 files. [7.10s]` (run four times, the same each time; before the change: `70 pass`, `4 fail`)
- `cd memory_check && ./node_modules/.bin/tsgo --noEmit -p .` → exit 0, no output

## Probes beyond the suite

On fixtures: a staged modification of an entry and a staged deletion of one → count 0 (the snapshot holds them, the
checks read them); an unstaged deletion of `project-memory/work/plan.md` → 1, named; two untracked files in two folders
→ 2, both named; `git status` exiting 128 → `- the count could not be read: git status --porcelain -uall -- project-memory failed: fatal: injected`; an injected `git log` failure → the warning holds five "could not run" lines (W1.1a, W1.1b, W6.3a, K4.1, K4.3), no entry text, exit 1. A run on this repository keeps the counts of
`nodes/smoke-report.md` (0 fail, 3 pass, 3 needs a reviewer, 72 not applicable, 0 could not run) and an empty warning.

## CONTRADICTS

None. R1's "a list of what needs a reviewer, and last a section `## Not applicable`" and U3's "one line per MUST that
fails or could not run" are the texts the tests pin; no requirement or use case contradicts either change.