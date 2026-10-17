# Brief — P3 round R1: build until the checks pass

You are the builder of the `code-map` tool. The tests and the evaluator already exist and were written by another
engine from the same requirements.

## Read first

- `runs/20261014-code-map-vision-relay/result-trimmed.md`: the requirements; this round is **R1**.
- `runs/20261014-code-map-build/spec.md`: the contract (command line, JSON shapes, call-link rules).
- `code_map/test/`: the tests your code must pass, including earlier rounds'.
- `code_map/src/`: the tool so far, if any.


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
- `bun eval/run.ts --tool "bun src/cli.ts" --cases eval/cases/fixtures.json --out /tmp/cm-round` reports R1 MET
 .

Run all three and fix until they pass. Return the last lines of each output.
