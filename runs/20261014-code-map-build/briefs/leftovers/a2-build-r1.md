# Brief — P3 round A2: build until the checks pass

You are the builder of the `code-map` tool. The tests and the evaluator already exist and were written by another
engine from the same requirements.

## Read first

- `runs/20261014-code-map-vision-relay/result-trimmed.md`: the requirements; this round is **A2**.
- `runs/20261014-code-map-build/spec.md`: the contract (command line, JSON shapes, call-link rules).
- `code_map/test/`: the tests your code must pass, including earlier rounds'.
- `code_map/src/`: the tool so far, if any.
- `code_map/test/a2/`: this round's tests. The target code base calls most functions through Effect services and
  holds most functions in constants such as `export const f = Effect.fn("F")(function* () { ... })`, imported and
  called from other files.

## Write

Only files under `code_map/src/`. The entry point is `code_map/src/cli.ts`. Use the `typescript` 5.8.2 compiler API
(already installed); no other dependency. The tool must work on any TypeScript project, not only the test fixtures:
never match on fixture file names, identifiers or line numbers. A held-out copy with changed names and lines is
also checked, and you will not see it.

## Must not

- Change nothing outside `code_map/src/`: not the tests, `code_map/eval/`, `package.json`, `tsconfig.json`,
  `bun.lock`, and add no `bunfig.toml`.
- Do not install packages. Never import, require or run a file of the target project (R1).

## Done when

In `code_map/`:
- `bun test` passes every test;
- `bunx tsgo --noEmit` exits 0;
- `bun eval/run.ts --tool "bun src/cli.ts" --cases eval/cases/fixtures.json --out ../runs/20261014-code-map-build/p3/a2-build-scratch` reports A2 MET
  and no NOT MET for R1, R2 and A5.

Run all three and fix until they pass. Return the last lines of each output.

## How to read A2 in this round

- Depth is the shortest route from the place, counted in call links. A function first reached by a longer route
  must still get the links it has within the depth from the shorter route. A reference back never hides a link
  within the depth.
- Going into a body written straight into a call (`Effect.fn("x")(function* () {...})`, `Effect.gen(...)` passed as an
  argument) adds no level.
- A call the tool cannot follow stops with a limit at its site naming why. A call the type checker resolves must be
  linked, not marked dynamic.

## Time and progress

You have 30 minutes. Work in small pieces: one failing test group at a time. After each piece, append one line to
`runs/20261014-code-map-build/nodes/a2-build.progress.md`: the UTC time from `date -u +%Y-%m-%dT%H:%MZ`, the piece,
and done or failed. That file is the only file outside `code_map/src/` you may write.
