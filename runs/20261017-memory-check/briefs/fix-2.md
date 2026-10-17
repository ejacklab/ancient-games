# Brief — fix memory-check against the review's 14 findings

You work in the repository root. Change only `memory_check/src/` (and `memory_check/package.json` if needed), the
progress file and the result file below. Do not change any test, the four docs or the guidelines. Do not commit, and
do not stage anything.

## Task
Make `memory_check/test/review.test.ts` pass (15 tests, one per finding, each failing now for the reason its finding
names) while `memory_check/test/acceptance.test.ts` keeps passing. The findings, with file:line and the input that
shows each: `runs/20261017-memory-check/nodes/review.codex.md`. The requirements they rest on:
`memory_check/REQUIREMENTS.md` (C2 results and evidence, C3 memory_index.py, C5 snapshot and history, R2 warning, F3
read only). In short:

1. memory_index.py failures that map to no requirement, or a Python error, become "could not run", never pass.
2. Checks memory_index.py did not reach (after entry validation fails) are "could not run"; fix the `mismatch`
   recogniser (Python prints `project-memory/INDEX.md`).
3. Presence and bytes for staged verdicts come from the staged state, not the working tree.
4. Staged deletions and renames are seen by K4.1 and the rename clauses.
5. K4.3 checks every transition in history, not only the endpoints; each covers edit needs its own changed: line.
6. `--since` takes its baseline from before the range.
7. A merge that drops a whole entry one side added fails (K4.1 or W6.3a).
8. K4.1 with no mechanical break is "needs a reviewer" (C2: mixed git+reviewer record).
9. Header scalars are unquoted before comparison (`status: "superseded"`).
10. Rd1 decides only clear session-start instructions; anything unresolved is "needs a reviewer".
11. The warning is built from ids, categories and file names, never entry text.
12. A git command that fails makes its checks "could not run", never an empty pass.
13. The launcher disables bun's transpiler cache whenever it is not already disabled.
14. A fenced code block inside an entry body is not a second header (W6.1a).

## Lessons (from `lessons for --agent opencode --kinds code-edit`)
- When a change sends new cases into an existing code path, list that path's early returns and exemptions first, and
  test each with one of the new cases.
- opencode headless auto-rejects a command with an absolute path, even inside the repo, and then stops with no work done.
  **Use relative paths only, from the repository root; never `cd` to an absolute path.** (That is why the first run of
  this brief did nothing.)

## Pieces and progress (first)
One piece per numbered finding. Before starting, append one `planned` line per piece to
`runs/20261017-memory-check/nodes/fix-2.progress.md`, then one line as each starts and ends:
`- <ISO time from date -Iseconds> · <piece-id> · <planned|start|done|fail> · <short note>` (the piece id is one word).

## Standard
- `cd memory_check && bun test` — all tests of both files pass; `./node_modules/.bin/tsgo --noEmit -p .` clean.

## Limits
May change: `memory_check/src/**`, `memory_check/package.json`, the progress file, and
`runs/20261017-memory-check/nodes/fix-2.result.md`. No other AI engine. Foreground commands only.

## Result
`runs/20261017-memory-check/nodes/fix-2.result.md`: `status: done|partial|fail`, one sentence; per finding what changed
(file and function); the test and typecheck commands with their last lines; CONTRADICTS or none.
