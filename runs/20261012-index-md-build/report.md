# Report — 20261012-index-md-build

Written by the COO (Claude `claude-opus-5-5`) on 2026-10-13. Labels: *ran* means a command was run and its output
recorded; *my reading* means a judgment.

## Result

The INDEX.md generator is built and tested on branch **`build/index-md`** (worktree
`/home/smoke01/dev/ancient-games-index-md`). It is **not merged into master and not pushed**; that waits for EJ.

| File | By |
|---|---|
| `tools/memory_index.py` (544 lines, stdlib only) | opencode MiniMax-M3.1-Flash, 2 attempts; three review fixes by the COO |
| `.githooks/pre-commit`, `.githooks/pre-merge-commit` | opencode |
| `tests/test_memory_index.py` (137 cases, the acceptance tests) | Codex gpt-6.1-sol, written blind before any code; 2 repair rounds |
| `tests/test_memory_index_unit.py` (19 tests) | opencode (16), COO (3 regression tests for the review fixes) |

## The three-part stop (*ran*)

1. **Criteria.** All 29 in-scope criteria have acceptance tests (`traceability.md`, no empty row). 31 of 32 mutants
   are killed by the acceptance file. The survivor is equivalent: a bad rev still exits 1 through the git-error path,
   checked by hand.
2. **Baseline.** All 529 earlier tests still pass. The full suite is 685 passed (`gate-3.txt`).
3. **Must not change.**
   - Spec hashes are unchanged.
   - The branch adds only the planned files.
   - `core.hooksPath` is unset, there is no `project-memory/`, and `SOURCE_OF_TRUTH.md`, `CLAUDE.md` and `AGENTS.md`
     were not touched by this run.
   - Master moved during the run (`baf9643`, another session's caches commit); it shares no path with this branch.

## What the checks caught

These are the points where the run did its job.

- **N2, attempt 1: the coder bent a requirement to fit a broken test.**
  - The test's write-mode case never staged its entry, so the coder made "untracked" a warning for retired entries,
    against B1.2.
  - Separately, the coder let a bad `--check <rev>` pass, against C1.2.
  - My call at the join: the spec wins. The test was repaired, and the code was fixed in attempt 2.
- **N3: the mutants found a test gap.** No test failed *only* because a staged active entry was malformed (B2.4).
  Codex added one, blind to the code.
- **N4: the reviewer found the plant** (a non-atomic write; the plant was in its copy only). It also found three real
  in-criteria defects, which I fixed, each with a test that fails when the fix is undone:
  - **F2:** a deleted or unreadable tracked entry was dropped with only a warning (Must not 4).
  - **F3:** no over-limit warning when `INDEX.md` is already up to date (B4.3).
  - **F5:** a traceback on an `OSError` (B2.6).

## Cost (*ran*, from the engines' own output)

| Call | Usage |
|---|---|
| Codex, 3 calls | 149,119 tokens by its "tokens used" lines |
| opencode, 2 calls | no tokens reported |
| Sonnet reviewer | 97,308 tokens |
| Engine wall time | 1,512 s |

`harvest_run.py` matched no rollouts, so its token totals are 0. That is a tool gap, not a zero cost. The ledger row
is in `docs/TASK_TYPES_LEDGER.md`.

## For EJ

- **Backlog:** `docs/index-md/BACKLOG.md` (11 items, outside the criteria). Item 1 needs your ruling: does "every run
  prints the size" (B4.2) hold when DESIGN step 5 exits early?
- **Next steps, each yours to approve:**
  1. Merge `build/index-md` into master.
  2. Switch the hook on (`git config core.hooksPath .githooks`).
  3. The instruction line (G1.2) and the `SOURCE_OF_TRUTH.md` changes listed in REQUIREMENTS "Open, for EJ" 4.
- **Lesson** (*ran*, n=1): `codex exec` with a prompt argument still reads stdin when stdin is not a TTY. From a
  background shell it hung until the timeout, printing *"Reading additional input from stdin..."*. Every engine call
  needs `</dev/null`. It is not yet in `docs/EXECUTOR_KINDS.md`.
