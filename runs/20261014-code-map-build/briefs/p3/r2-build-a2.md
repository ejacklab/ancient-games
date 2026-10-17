# Brief — P3 round R2: build until the checks pass

You are the builder of the `code-map` tool. The tests and the evaluator already exist and were written by another
engine from the same requirements.

## Read first

- `runs/20261014-code-map-vision-relay/result-trimmed.md`: the requirements; this round is **R2**.
- `runs/20261014-code-map-build/spec.md`: the contract (command line, JSON shapes, call-link rules).
- `code_map/test/`: the tests your code must pass, including earlier rounds'.
- `code_map/src/`: the tool so far, if any.
- `code_map/test/r2/`: this round's tests. The target code base calls most functions through Effect services: an
  interface, a layer built with `Effect.fn`, and an object of `const` references (`Service.of({ assert, ask })`).

## Feedback from attempt 1 (verified by the COO on the private real-code set)

Your attempt 1 passed the tests, the bundled evaluator and the held-out copy. On real code it fails this R2 line:
"an implementation the lookup finds has no link".

1. **The tool contradicts itself.** `callers <implementation>` finds a service call inside an anonymous function and
   names that function as the link's `from` (for example `{name: "Effect.gen callback", kind: "function"}` for the
   `function*` passed to `Effect.gen` inside an `execute: (input, context) => { return Effect.gen(function* () { ...
   yield* permission.assert(...) ... }) }` property). But `callees <file>:<that from line>` answers
   `not-found` — "no definition was found at ...". Every node the tool names as `from` or `to` must be accepted as a
   place by `callees`, `callers`, `chain` and `tests`, and `callees` on it must show the same link. The spec's rule
   for the enclosing function (the nearest function, method or arrow) applies to anonymous bodies too; in the target
   code base most calls are in such bodies.

Write your own fixture for this form. This is attempt 2 of 3 for this round.

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
- `bun eval/run.ts --tool "bun src/cli.ts" --cases eval/cases/fixtures.json --out /tmp/cm-round` reports R2 MET
  and no NOT MET for R1.

Run all three and fix until they pass. Return the last lines of each output.
