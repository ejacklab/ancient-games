# Brief — P3 round R2: write the failing tests

You write the tests for one requirement of the `code-map` tool. Another engine builds the tool afterwards and must
pass your tests without changing them.

## Read first

- `runs/20261014-code-map-vision-relay/result-trimmed.md`: requirement **R2** and its **Fails if** lines.
- `runs/20261014-code-map-build/spec.md`: the command line and JSON shapes.
- `code_map/eval/fixtures/` (you may use these projects as test inputs) and `code_map/src/` if it exists (read only).
- Tests from earlier rounds: `code_map/test/` (do not change them).

## Write

Only `code_map/test/r2/*.test.ts` (`r2` in lower case). `bun test` tests that run the tool **through its
command line** (`bun src/cli.ts ... --json`, from `code_map/`) and check the JSON against the spec. Cover every
**Fails if** line of R2, each in at least one test whose name quotes the line. Use your own small fixture
projects under `code_map/test/r2/fixtures/` where the evaluator's do not exercise a case; vary names and line
positions from the evaluator's fixtures, so a tool that memorises those cannot pass.

## The target's service style

The tool is for code like opencode's, where most calls go through Effect services. Model at least half of your
fixtures on this style (define minimal Effect-like types inside the fixture; no dependency):
- a tag `export class Permission extends Context.Service<Permission, Interface>()("@app/Permission") {}`, with an
  `Interface` of `readonly` function members;
- a layer whose implementations are constants, `const assert = Effect.fn("Permission.assert")(function* (input) { ... })`,
  returned as `Permission.of({ assert, ask })` with shorthand properties;
- callers inside other `Effect.fn` bodies that do `const permission = yield* Permission.Service` and then
  `yield* permission.assert({ ... })`, including one where `permission` and `.assert(` sit on separate lines;
- a test file that builds a fake with `Permission.of({ assert: () => ... })`.
`callees` at a caller must link to the `assert` constant's location; `callers` of that constant must list every
call site; the fake is labelled, never chosen.

## Must not

- Write nothing outside `code_map/test/r2/`. Do not write `code_map/src/`.
- Do not install packages. Read nothing else.

## Done when

`bun test test/r2` runs, and every test you wrote fails or passes for a reason you can state (with no tool yet,
they fail). Return the test names, the Fails-if line each covers, and the last lines of the run.
