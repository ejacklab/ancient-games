# Brief — P3 round A1: build until the checks pass

You are the builder of the `code-map` tool. The tests and the evaluator already exist. Other engines wrote them from
the same requirements.

## Read first

- `runs/20261014-code-map-vision-relay/result-trimmed.md`: the requirements. This round is **A1**.
- `runs/20261014-code-map-build/spec.md`: the contract: command line, JSON shapes and call-link rules.
- `runs/20261014-code-map-build/builds/a1-opencode/code_map/test/`: the tests your code must pass, including earlier rounds'.
- `runs/20261014-code-map-build/builds/a1-opencode/code_map/src/`: the tool so far.
- `runs/20261014-code-map-build/builds/a1-opencode/code_map/test/a1/`: this round's tests.

## What this round's failing tests are about

Each one is a way a module map was seen to contradict the code, or to miss a known item, on a real TypeScript code
base:
- **Sibling tables:** a sibling group with members but no rows, and no limit saying why. Members often hold their
  functions in constants written straight into a call (`export const f = Effect.fn("F")(function* () {...})`).
- **A local class built with `new`:** it is labelled "outside the repository".
- **A method on a value made by a factory and taken with `yield*`:** it is labelled "outside the repository" when
  the method is written in the repository.
- **A call to an overloaded function:** the overload signature has no body, so the link stays unresolved. The
  implementation beside it is never reached.
- **A call through an interface:** it misses an implementation that is an object returned from a function.
- **A workspace package linked under `node_modules`:** it counts as outside the repository, because the program
  keeps the link's path instead of the real one.
- **`map` of some paths:** it leaves out callers in other paths, and no limit names the scope it did not search.

## Write

Only files under `runs/20261014-code-map-build/builds/a1-opencode/code_map/src/`. The entry point is `runs/20261014-code-map-build/builds/a1-opencode/code_map/src/cli.ts`.
- Use the `typescript` 5.8.2 compiler API, which is already installed. Use no other dependency.
- The tool must work on any TypeScript project, not only the test fixtures. Never match on fixture file names,
  identifiers or line numbers. A held-out copy with changed names and lines is also checked, and you will not see it.

## Must not

- Change nothing outside `runs/20261014-code-map-build/builds/a1-opencode/code_map/src/`. That includes:
  - the tests and `runs/20261014-code-map-build/builds/a1-opencode/code_map/eval/`;
  - `package.json`, `tsconfig.json` and `bun.lock`.

  Add no `bunfig.toml`.
- Do not install packages. Never import, require or run a file of the target project (R1).
- **Do not run git** — no stash, checkout, reset, restore or clean. Other work in this repository is not committed.
- Use relative paths only, and never `cd` to an absolute path.

## Time and progress

You have 30 minutes. Work in small pieces: one failing test group at a time. After each piece, append one line to
`runs/20261014-code-map-build/nodes/a1-build-opencode.progress.md`: the UTC time from `date -u +%Y-%m-%dT%H:%MZ`, the piece,
and done or failed. That file is the only file outside `runs/20261014-code-map-build/builds/a1-opencode/code_map/src/` you may write.

## Done when

In `runs/20261014-code-map-build/builds/a1-opencode/code_map/`:
- `bun test` passes every test;
- `bunx tsgo --noEmit` exits 0;
- `bun eval/run.ts --tool "bun src/cli.ts" --cases eval/cases/fixtures.json --out node_modules/.cm-round-opencode`
  reports A1 MET, and no NOT MET for R1, R2, A2 or A5.

Run all three and fix until they pass. Return the last lines of each output.
