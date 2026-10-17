# Brief — P3 round A3: write the failing tests (in a staging folder)

You write the tests for one requirement of the `code-map` tool. Another engine builds the tool afterwards and must
pass your tests without changing them. Another engine is changing `code_map/src/` while you work, so you write in a
staging folder, not in `code_map/`.

## Read first

- `runs/20261014-code-map-vision-relay/result-trimmed.md`: requirement **A3** and its **Fails if** lines.
- `runs/20261014-code-map-build/spec.md`: the command line and JSON shapes; the section "Tests (A3)" and the
  `tests` rows of the command table.
- `code_map/eval/fixtures/` (you may use these projects as test inputs) and `code_map/src/` (read only).
- Tests from earlier rounds: `code_map/test/` (read only). Write yours in the same style as `code_map/test/a5/`.

## How to read A3 in this round

These are the owner's provisional decisions. Test against them:
- **Which files are test files is the user's:** the tool has no default and takes `--tests <glob>`. With no
  `--tests`, no file is a test file.
- **The fake rule is the user's:** `--fake-rule count` counts and lists tests whose path passes a fake;
  `--fake-rule exclude` leaves them out of both `tests` and `undecided`; with no `--fake-rule` they go in
  `undecided`, are not counted, and the answer carries the limit "fake rule not set (A3)". Test all three.
- **`count` always equals the length of the list.** Each test in the list has its path of links as evidence.
- **Static links are never called coverage:** no answer field or default-text word says "coverage" or "covered".
- **The per-function report for a whole file runs only with `--per-function`.** Without it, `tests --file <path>`
  must not produce the per-function report. The agent's part (asking the user first) is checked elsewhere.
- **A test with a known path:** a test whose body reaches the function through a chain of links, including
  through an Effect service, must be in the list.

## Write

Only under `runs/20261014-code-map-build/staging/test-a3/`, laid out as it will sit in `code_map/test/a3/`:
`*.test.ts` files and a `fixtures/` folder. The tests run the tool **through its command line**
(`bun src/cli.ts ... --json`, from `code_map/`). Cover every **Fails if** line of A3, each in at least one test
whose name quotes the line. Use your own small fixture projects. Vary names and line positions from the evaluator's
fixtures. Model at least half of them on the Effect service style in `code_map/test/r2/fixtures/`, with real and
fake implementations of a service, the fakes in test files.

To run your tests, make a copy: `runs/20261014-code-map-build/staging/cm-copy/` holding `code_map/` without
`node_modules/`, plus a link named `node_modules` to `../../../../code_map/node_modules`. Put your tests in the
copy's `test/a3/` and run `bun test test/a3` there. Never write `code_map/` itself.

## Pieces and progress

Work in small pieces: one Fails-if line at a time. After each piece, append one line to
`runs/20261014-code-map-build/nodes/a3-tests.progress.md`: the UTC time from `date -u +%Y-%m-%dT%H:%MZ`, the
piece, and done or failed.

## Must not

- Write nothing outside `runs/20261014-code-map-build/staging/` and that progress file.
- Do not install packages. Read nothing else.

## Done when

`bun test test/a3` runs in the copy, and every test passes or fails for a reason you can state. Return the test
names, the Fails-if line each covers, which fail on the copied tool and why, and the last lines of the run.
