# Brief — P3 round R3: write the failing tests (in a staging folder)

You write the tests for one requirement of the `code-map` tool. Another engine builds the tool afterwards and must
pass your tests without changing them. Another engine is changing `code_map/src/` while you work, so you write in a
staging folder, not in `code_map/`.

## Read first

- `runs/20261014-code-map-vision-relay/result-trimmed.md`: requirement **R3** and its **Fails if** line.
- `runs/20261014-code-map-build/spec.md`: the command line, and the rules "R3 Stays offline, writes only its output"
  and "Stores nothing in the target".
- `code_map/eval/` (the evaluator's R3 check) and `code_map/src/` (read only).
- Tests from earlier rounds: `code_map/test/` (read only). Write yours in the same style as `code_map/test/a5/`.

## How to read R3 in this round

The tool's part of R3:
- the tool opens no network connection;
- it writes no file except to stdout and, when `--out` is given, that one file;
- it stores nothing in the target, and rebuilds every run from the files.

The rest of R3 is the agent's part and is checked elsewhere: what goes into git, and what is sent to outside
engines.

Test every command: `where`, `find`, `callers`, `callees`, `chain`, `tests` and `map`. For each:
- list every file under the fixture root and in the working directory before and after the run, with sizes and
  modification times, and check that nothing changed;
- run it once under `unshare -rn` (this works here; plain `unshare -n` does not) and check that it still answers;
- check that the source in `code_map/src/` imports no network module (`net`, `http`, `https`, `dgram`, `tls`, `dns`,
  `fetch` or `WebSocket` use);
- check that a fixture whose files hold a secret-looking string produces no file anywhere outside stdout and `--out`.

## Write

Only under `runs/20261014-code-map-build/staging/test-r3/`, laid out as it will sit in `code_map/test/r3/`:
`*.test.ts` files and a `fixtures/` folder. Each test's name quotes R3's Fails-if line.

To run your tests, make a copy at `runs/20261014-code-map-build/staging/cm-copy-r3/`:
- it holds `code_map/` without `node_modules/`;
- it has a link named `node_modules` pointing to `../../../../code_map/node_modules`.

Put your tests in the copy's `test/r3/` and run `bun test test/r3` there. Never write `code_map/` itself.

## Pieces and progress

Work in small pieces, one command at a time. After each piece, append one line to
`runs/20261014-code-map-build/nodes/r3-tests.progress.md`: the UTC time from `date -u +%Y-%m-%dT%H:%MZ`, the
piece, and done or failed.

## Must not

- Write nothing outside `runs/20261014-code-map-build/staging/` and that progress file.
- Do not install packages. Read nothing else.

## Done when

`bun test test/r3` runs in the copy, and every test passes or fails for a reason you can state. Return:
- the test names;
- which tests fail on the copied tool, and why;
- the last lines of the run.
