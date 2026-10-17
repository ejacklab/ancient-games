# Brief — fix memory-check v1 against its failing acceptance tests

You work in the repository root. Change only `memory_check/src/` (and, if needed, `memory_check/package.json` or a
`memory_check/bunfig.toml`), the progress file and the result file below. Do not change the tests, the four docs or
the guidelines. Do not commit.

## Task
Make the 8 failing tests of `memory_check/test/acceptance.test.ts` pass by fixing the tool, not the tests. Each was
judged real by the main agent against `memory_check/REQUIREMENTS.md` (read it: C1, C4 and C6 changed today):

1. **F3/U5 (2 tests)** — a run writes 8 files under the fixture's home, `home/.bun/install/cache/…`: the bun runtime,
   not the tool's code, but F3 forbids any file but the report. Stop bun writing there for a run of the tool (for
   example its auto-install or its caches), and say in the result what you changed and why it is enough.
2. **C2** — every pass and fail needs evidence of the form file:line, or the command and its output: `CACHES:Rd1`'s
   pass has none, and `SoT:K4.3`'s ("1 entry file(s) compared …") names no file or command.
3. **C4** — with no `project-memory/.cache/`, `CACHES:B2` (B2.2) must be "not applicable", not fail (C4, C6 as changed).
4. **U2 SoT:K4.1** — a staged entry whose `status` is `superseded` with no `superseded_by` link passes; it must fail
   (C5: files are read from the staged state).
5. **U2 CACHES:B2** — the fail's evidence must name the `.gitignore` file(s) it looked in.
6. **U2 SoT:Rd3.1a** — an oversized `INDEX.md` passes; it must fail on size (see how `tools/memory_index.py` reports
   size, and whether its `--check` exit or text carries it).
7. **U2 SoT:W6.3a** — a merge commit that drops a `covers` path and a `changed:` line one side added gets "needs a
   reviewer"; git shows it, so it must fail (C2: a tool-found break of a mixed tool+reviewer record fails).

## Lessons (from `lessons for --agent opencode --kinds code-edit`)
- When a change sends new cases into an existing code path, list that path's early returns and exemptions first, and
  test each with one of the new cases.
- Each fact in a brief carries its source; every file it cites lives inside the repo.

## Pieces and progress (first)
One piece per numbered item. Before starting, append one `planned` line per piece to
`runs/20261017-memory-check/nodes/fix-1.progress.md`, then one line as each starts and ends:
`- <ISO time from date -Iseconds> · <piece-id> · <planned|start|done|fail> · <short note>` (the piece id is one word).

## Standard
- `cd memory_check && bun test` — all 55 pass; `./node_modules/.bin/tsgo --noEmit -p .` clean.
- Rerun the smoke report: `cd memory_check && bun src/cli.ts --project .. --out ../runs/20261017-memory-check/nodes/smoke-report.md; echo "exit $?"`.

## Limits
May change: `memory_check/src/**`, `memory_check/package.json`, `memory_check/bunfig.toml`, the progress file, the
smoke report, and `runs/20261017-memory-check/nodes/fix-1.result.md`. No other AI engine. Foreground commands only.

## Result
`runs/20261017-memory-check/nodes/fix-1.result.md`: `status: done|partial|fail`, one sentence; per item what changed
(file and function); the test and typecheck commands with their last lines; CONTRADICTS or none.
