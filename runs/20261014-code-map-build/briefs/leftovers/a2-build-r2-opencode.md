# Brief — P3 round A2, round 2: build until the checks pass

You are the builder of the `code-map` tool. The tests and the evaluator already exist. Other engines wrote them from
the same requirements. You work in a copy of the tool:
`runs/20261014-code-map-build/builds/a2r2-opencode/code_map/` (called **the copy** below).

## Read first

- `runs/20261014-code-map-vision-relay/result-trimmed.md`: the requirements. This round is **A2** ("The call chain
  through one place").
- `runs/20261014-code-map-build/spec.md`: the contract. Its rule for the enclosing function of a call: "the nearest
  function, method or arrow, named by the `const x = Effect.fn(...)` or the property that holds it". The owner's rule
  for this round: a body written straight into a call is its own place, and going into it adds no level.
- In the copy, `test/`: the tests your code must pass. This round's new test is in `test/a2/nested-inline.test.ts`;
  one of its tests fails now.
- In the copy, `src/`: the tool so far.

## What the failing test is about

An inline callback sits inside a call chain held by a const:
`const providerStream = source(input).pipe(Stream.runForEach((update) => Effect.gen(function* () { ... })))`. The
const holds the result of the call, not the callback. So the callback is an inline body of the named function
around it, and its calls are that function's callees. Today the tool treats the callback as named after the const,
and the calls drop out of the enclosing function's `callees`.

Keep this case working: `const attempt = Effect.fn("x")(function* () {...})`. There, the generator is the function
the const names.

## Write

Only files under the copy's `src/`. Use the `typescript` 5.8.2 compiler API, and no other dependency. The tool must
work on any TypeScript project. Never match on fixture names, identifiers or line numbers.

## Must not

- Change nothing outside the copy's `src/`.
- Install nothing.
- **Do not run git.**
- Use relative paths only. Never write into `node_modules/`.

## Time and progress

You have 25 minutes. After each piece, append one line to
`runs/20261014-code-map-build/nodes/a2r2-build-opencode.progress.md`: the UTC time from `date -u +%Y-%m-%dT%H:%MZ`,
the piece, and done or failed.

## Done when

In the copy:
- `bun test` passes every test;
- `bunx tsgo --noEmit` exits 0;
- `bun eval/run.ts --tool "bun src/cli.ts" --cases eval/cases/fixtures.json --out a2r2-scratch` reports no NOT MET.

Return the last lines of each.
