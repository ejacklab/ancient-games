# Brief — tests for memory-check v1

You work in the repository root. Change only the files named under Limits. Do not commit.

## Task
Write acceptance tests in `memory_check/test/` for the tool in `memory_check/src/`, from the specification only:
`memory_check/REQUIREMENTS.md` (F1–F3, C1–C6, R1–R3, T1) and `memory_check/USE_CASES.md` (U1–U6). Each test is one
requirement's or use case's **Fails if** turned into a case that would catch it. Run the CLI (`bun src/cli.ts`) with
`spawnSync` against fixture projects the tests build in a temporary folder at run time (`git init`, write files,
`git add`/`git commit` as a case needs, `--home` pointed at a temporary home). Never point a test at the real home
folder or at this repository's own memory.

## Context (each fact with its source)
- The guidelines the tool checks: its own copy in `memory_check/guidelines/` (a copy of
  `docs/memory-system/SOURCE_OF_TRUTH_REQUIREMENTS.yaml` and `docs/memory-system/CACHES.md`). Entry format, index
  format and file names: `docs/memory-system/SOURCE_OF_TRUTH.md` § "What will be put in" and § "Where it is put".
- How a valid `INDEX.md` looks: run `python3 tools/memory_index.py` (write mode) only to learn the format once, then
  write each fixture's expected `INDEX.md` by hand as literal bytes (T1). Source: `tools/memory_index.py` lines 1–15.
- The tool's interface: `--project`, `--home`, `--out`, `--warn`, `--since`; exit 0 / 1 / 2 (R3). Source:
  `memory_check/REQUIREMENTS.md`.
- Do not read `runs/20261017-memory-check/nodes/implement.result.md` or the builder's progress: write from the spec.

## Lessons (from `lessons for --agent codex --kinds test`)
- Before writing a test of a function you did not just write, open that function's existing tests and assert its
  output the way they do — which fields, which form.
- A known answer given to a test must be computed by a different method from the rule under test.
- A planted break replaces a line that must exist, asserted present exactly once first, and never goes at a file's
  start or end; assert the plant's own effect before the reaction you are testing.
- When a change sends new cases into an existing code path, list that path's early returns and exemptions first, and
  test each.

## Pieces and progress (first)
Divide the work into small pieces (one per requirement group, plus fixtures). Before starting, append one `planned`
line per piece to `runs/20261017-memory-check/nodes/tests.progress.md`, then one line as each starts and ends:
`- <ISO time from date -Iseconds> · <piece-id> · <planned|start|done|fail> · <short note>` (the piece id is one word).

## Standard
- At least one case per requirement and per use case; for U2, one planted break per tool-checked requirement, each
  expected to fail exactly the requirement it breaks.
- F3/U5: hash every file of the fixture, ignored ones included, before and after a run; only `--out`'s file may differ.
- `cd memory_check && bun test` — report the counts. A test that fails because the tool is wrong stays failing:
  report it, do not weaken it.

## Limits
May change: `memory_check/test/**`, the progress file, and `runs/20261017-memory-check/nodes/tests.result.md` only.
No other AI engine. Foreground commands only.

## Result
`runs/20261017-memory-check/nodes/tests.result.md`: `status: done|partial|fail`, one sentence; the test files; the
command and its last lines; each failing test with the requirement it shows broken; CONTRADICTS (a spec line that
cannot be tested as written, quoted) or none.
