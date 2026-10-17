# Brief — P3 round R1: build until the checks pass

You are the builder of the `code-map` tool. The tests and the evaluator already exist and were written by another
engine from the same requirements.

## Read first

- `runs/20261014-code-map-vision-relay/result-trimmed.md`: the requirements; this round is **R1**.
- `runs/20261014-code-map-build/spec.md`: the contract (command line, JSON shapes, call-link rules).
- `code_map/test/`: the tests your code must pass, including earlier rounds'.
- `code_map/src/`: the tool so far, if any.

## Feedback from attempt 1 (a reviewer's CHANGE, verified by the COO)

Your attempt 1 passed the tests and the evaluator. A reviewer asked for these changes, each tied to a requirement
line. Paths refer to `code_map/src/`.

1. **A2** — "a known link within the depth is missing, or a shown link contradicts the code". `searchableDefinitions`
   stores each definition with `nodeOf`'s kind, not the `definitionKind` it computed, so `const g = () => …` and
   `const g = Effect.fn(…)(…)` are indexed as `"variable"`; `placeableKind` then refuses them, and `chain`,
   `callers`, `callees` and `tests` stop at the constant (`nodes.ts:197-213`, used at `commands.ts:430-435`, `:237`,
   `:265`, `:151`). Verified: on `export const middle = (): number => { return leaf(); };` the three commands answer
   "middle is a declaration, not an implementation to walk". In the target code base most functions are held in
   constants, in object properties, or in `Effect.fn("Name")(function* …)`. The same fix removes an unreasoned stop
   (L1).
2. **A1** — "a claim lacks its location or contradicts the code, or a checked example misses a known item". An
   exported `const g = Effect.fn(…)` called from outside is filtered out of `map.entries` for the same reason, and an
   arrow entry gets no steps because `stepsOf` treats a `VariableDeclaration` as not function-like
   (`commands.ts:307-311`, `flow.ts:103-106`).
3. **A2** — `find "<words>"` scores only definition names; the spec matches a description "over names, comments and
   strings" (`commands.ts:84-94`).

The evaluator now has cases for these forms (fixture `const-held`). This is attempt 2 of 3 for this round.


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
- `bun eval/run.ts --tool "bun src/cli.ts" --cases eval/cases/fixtures.json --out /tmp/cm-round` reports no requirement NOT MET
 .

Run all three and fix until they pass. Return the last lines of each output.
