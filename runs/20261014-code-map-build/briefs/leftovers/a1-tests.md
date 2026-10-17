# Brief — P3 round A1: write the failing tests (in a staging folder)

You write the tests for one requirement of the `code-map` tool. Another engine builds the tool afterwards and must
pass your tests without changing them. Another engine is changing `code_map/src/` while you work, so you write in a
staging folder, not in `code_map/`.

## Read first

- `runs/20261014-code-map-vision-relay/result-trimmed.md`: requirement **A1** and its **Fails if** line.
- `runs/20261014-code-map-build/spec.md`: the command line and JSON shapes; the section "Module map (A1)".
- `code_map/eval/fixtures/` (you may use these projects as test inputs) and `code_map/src/` (read only).
- Tests from earlier rounds: `code_map/test/` (read only). Write yours in the same style as `code_map/test/a5/`.

## How to read A1 in this round

These are the owner's provisional decisions and the spec's rules. Test against them:
- **The sibling rule is the user's:** one `--siblings <glob>` per sibling group. With no `--siblings`, there is no
  table, and the answer carries the limit "no sibling rule given (A1)".
- **When a sibling group is given, the table says what the members share and where they differ.** One row per
  concern, each `shared`, `varies` or `unclear`, each with locations.
  - A group whose table has members but no rows, and no limit saying why, fails "a checked example misses a known
    item".
  - Members often hold their functions in constants (`export const execute = Effect.fn("x")(function* () {...})`),
    not only in `export function` declarations.
- **Entry flows:** an entry is a function that is exported and called from outside the paths given. Its steps are
  listed in source order with their decisions, each with its location.
- **Every claim gives its file and lines.**
- **Definitions** include functions, methods, classes and `Effect.fn` constants. That includes service methods
  implemented inside a layer (`Service.of({ method })`).

## Write

Only under `runs/20261014-code-map-build/staging/test-a1/`, laid out as it will sit in `code_map/test/a1/`:
`*.test.ts` files and a `fixtures/` folder.
- The tests run the tool **through its command line** (`bun src/cli.ts ... --json`, from `code_map/`).
- Cover the **Fails if** line of A1: a claim lacking its location, a claim contradicting the code, a checked example
  missing a known item. Each test's name quotes the part it covers.
- Use your own small fixture projects. Vary names and line positions from the evaluator's fixtures.
- Model at least half of them on the Effect service style in `code_map/test/r2/fixtures/`. Include a sibling group:
  several files that each implement the same service or tool shape, with shared steps and differing steps.

To run your tests, make a copy at `runs/20261014-code-map-build/staging/cm-copy-a1/`:
- it holds `code_map/` without `node_modules/`;
- it has a link named `node_modules` pointing to `../../../../code_map/node_modules`.

Put your tests in the copy's `test/a1/` and run `bun test test/a1` there. Never write `code_map/` itself.

## Pieces and progress

Work in small pieces, one part of the Fails-if line at a time. After each piece, append one line to
`runs/20261014-code-map-build/nodes/a1-tests.progress.md`: the UTC time from `date -u +%Y-%m-%dT%H:%MZ`, the
piece, and done or failed.

## Must not

- Write nothing outside `runs/20261014-code-map-build/staging/` and that progress file.
- Do not install packages. Read nothing else.
- Never forbid a word outright when the tool may use it to deny the claim. "not execution coverage" is a denial, not
  a claim.

## Done when

`bun test test/a1` runs in the copy, and every test passes or fails for a reason you can state. Return:
- the test names;
- the part of the Fails-if line each covers;
- which fail on the copied tool, and why;
- the last lines of the run.
