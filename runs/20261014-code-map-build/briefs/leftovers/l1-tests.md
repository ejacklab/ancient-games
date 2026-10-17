# Brief — P3 round L1: write the failing tests (in a staging folder)

You write the tests for one requirement of the `code-map` tool. Another engine builds the tool afterwards and must
pass your tests without changing them. Another engine is changing `code_map/src/` while you work, so you write in a
staging folder, not in `code_map/`.

## Read first

- `runs/20261014-code-map-vision-relay/result-trimmed.md`: requirement **L1** and its **Fails if** line.
- `runs/20261014-code-map-build/spec.md`: the command line, the JSON shapes, and `Limit` with its reasons.
- `code_map/eval/fixtures/` (you may use these projects as test inputs) and `code_map/src/` (read only).
- Tests from earlier rounds: `code_map/test/` (read only). Write yours in the same style as `code_map/test/a5/`.

## How to read L1 in this round

- **Every answer or branch that stops early names why**, in a limit at the place where it stopped. The reasons are
  the depth the user set, dynamic behaviour, outside the repository, another process, not found, or another stated
  reason. This covers every command: `find`, `where`, `callers`, `callees`, `chain`, `tests` and `map`.
- **Stopping early includes leaving results out.** Some examples:
  - a ranked search that returns only its best matches and drops weaker ones;
  - a walk that stops after a fixed budget of visits or steps;
  - a list cut to a size.

  Each of these must say so in a limit. The answer must never look complete when it is not.
- **An empty result means nothing was found by this analysis, never that nothing exists.** Check both the JSON and
  the default text.

Two places in the current code to test, by their shape:
- `find` with a description, where some definitions match by name and others match only in their comments or
  strings. Either all the matches come back, or the answer carries a limit saying weaker matches were left out.
- `tests` (and any walk) over a call graph larger than a few hundred functions between the test and the function.
  Either the test is found, or the answer carries a limit naming why the walk stopped. Generate such a fixture with
  a small script in the test, rather than writing it by hand.

## Write

Only under `runs/20261014-code-map-build/staging/test-l1/`, laid out as it will sit in `code_map/test/l1/`:
`*.test.ts` files and a `fixtures/` folder.
- The tests run the tool **through its command line** (`bun src/cli.ts ... --json`, from `code_map/`).
- Cover both parts of L1's **Fails if** line, each in at least one test whose name quotes the part.
- Model at least half of the fixtures on the Effect service style in `code_map/test/r2/fixtures/`.

To run your tests, make a copy at `runs/20261014-code-map-build/staging/cm-copy-l1/`:
- it holds `code_map/` without `node_modules/`;
- it has a link named `node_modules` pointing to `../../../../code_map/node_modules`.

Put your tests in the copy's `test/l1/` and run `bun test test/l1` there. Never write `code_map/` itself.

## Pieces and progress

Work in small pieces, one test group at a time. After each piece, append one line to
`runs/20261014-code-map-build/nodes/l1-tests.progress.md`: the UTC time from `date -u +%Y-%m-%dT%H:%MZ`, the
piece, and done or failed.

## Must not

- Write nothing outside `runs/20261014-code-map-build/staging/` and that progress file.
- Do not install packages. Read nothing else.
- Never forbid a word outright when the tool may use it to deny the claim. For example, "none found by static
  analysis" denies that the result is proof of absence.

## Done when

`bun test test/l1` runs in the copy, and every test passes or fails for a reason you can state. Return:
- the test names;
- the part of the Fails-if line each covers;
- which tests fail on the copied tool, and why;
- the last lines of the run.
