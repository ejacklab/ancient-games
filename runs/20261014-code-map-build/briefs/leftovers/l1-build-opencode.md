# Brief — P3 round L1: build until the checks pass

You are the builder of the `code-map` tool. The tests and the evaluator already exist. Other engines wrote them from
the same requirements. You work in a copy of the tool:
`runs/20261014-code-map-build/builds/l1-opencode/code_map/` (called **the copy** below).

## Read first

- `runs/20261014-code-map-vision-relay/result-trimmed.md`: the requirements. This round is **L1** ("Says where it
  stops").
- `runs/20261014-code-map-build/spec.md`: the contract: command line, JSON shapes, `Limit` and its reasons.
- `test/` in the copy: the tests your code must pass, including earlier rounds'. This round's tests are in
  `test/l1/`.
- `src/` in the copy: the tool so far.

## What this round's failing tests are about

L1: every answer or branch that stops early names why, in a limit at the place where it stopped. An empty result
means nothing was found by this analysis, never that nothing exists. Stopping early includes leaving results out:
- **A ranked search that returns only its best matches:** `find` with a description keeps only the top tier of
  matches. It must return all of them, ranked, or carry a limit saying that weaker matches were left out.
- **A walk that stops after a fixed budget of visits:** `tests` and any other walk must say where and why it
  stopped. Better still, find the test.
- **Located stops:** a branch that stops must carry its limit at that branch's place.

## Write

Only files under the copy's `src/`. The entry point is `src/cli.ts`.
- Use the `typescript` 5.8.2 compiler API, which is already installed. Use no other dependency.
- The tool must work on any TypeScript project, not only the test fixtures. Never match on fixture file names,
  identifiers or line numbers. A held-out copy with changed names and lines is also checked, and you will not see it.

## Must not

- Change nothing outside the copy's `src/`:
  - not the tests;
  - not `eval/`;
  - not `package.json`, `tsconfig.json` or `bun.lock`;
  - and add no `bunfig.toml`.
- Do not install packages. Never import, require or run a file of the target project (R1).
- **Do not run git** — no stash, checkout, reset, restore or clean. Other work in this repository is not committed.
- Use relative paths only, and never `cd` to an absolute path. Never write into `node_modules/`.

## Time and progress

You have 30 minutes. Work in small pieces: one failing test group at a time. After each piece, append one line to
`runs/20261014-code-map-build/nodes/l1-build-opencode.progress.md`: the UTC time from `date -u +%Y-%m-%dT%H:%MZ`,
the piece, and done or failed.

## Done when

In the copy:
- `bun test` passes every test;
- `bunx tsgo --noEmit` exits 0;
- `bun eval/run.ts --tool "bun src/cli.ts" --cases eval/cases/fixtures.json --out l1-scratch` reports L1 MET, and
  no NOT MET for R1, R2, R3, A1, A2, A3 or A5.

Run all three and fix until they pass. Return the last lines of each output.
