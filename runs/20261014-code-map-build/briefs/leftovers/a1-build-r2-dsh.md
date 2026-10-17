# Brief — P3 round A1, round 2: build until the checks pass

You are the builder of the `code-map` tool. The tests and the evaluator already exist; other engines wrote them from
the same requirements. You work in a copy of the tool: `runs/20261014-code-map-build/builds/a1r2-dsh/code_map/`
(called **the copy** below).

## Read first

- `runs/20261014-code-map-vision-relay/result-trimmed.md`: the requirements. This round is **A1** ("The map of a
  module").
- `runs/20261014-code-map-build/spec.md`: the contract: command line, JSON shapes, call-link rules.
- The copy's `test/`: the tests your code must pass. This round's new tests are `test/a1/real-shapes-r2.test.ts`;
  4 of them fail now.
- The copy's `src/`: the tool so far.

## What the failing tests are about

Two shapes of real TypeScript code in the Effect service style:
1. **`where <Namespace>.<member>` for a service.** The service is re-exported with `export * as Permission from
   "./permission"`, and its method is a constant in a layer: `const assert = Effect.fn(...)`, returned as
   `Service.of({ assert })`. Today the lookup does not follow the namespace re-export. It falls back to a text match,
   which returns unrelated object properties named `….permission.assert`. `where` must find the layer's constant.
2. **Sibling rows when each sibling exports a tool built by a call**: `export const tool = Tool.make({ ..., execute:
   Effect.fn(...)(function* ...) })`. Today only exports whose value is a function are compared, so the table has
   members and no rows. It must compare what the members do, such as the `execute` bodies, and give `shared` and
   `varies` rows with locations. Or, when it cannot compare them, a limit saying why.

## Write

Only files under the copy's `src/`. Use the `typescript` 5.8.2 compiler API, which is already installed, and no
other dependency. The tool must work on any TypeScript project, not only the test fixtures. Never match on fixture
file names, identifiers or line numbers: a held-out copy with changed names and lines is also checked.

## Must not

- Change nothing outside the copy's `src/`.
- Do not install packages. Never import, require or run a file of the target project.
- **Do not run git.** Use relative paths only. Never write into `node_modules/`.

## Time and progress

You have 30 minutes. Work in small pieces: one failing test group at a time. After each piece, append one line to
`runs/20261014-code-map-build/nodes/a1r2-build-dsh.progress.md`: the UTC time from `date -u +%Y-%m-%dT%H:%MZ`, the
piece, and done or failed.

## Done when

In the copy:
- `bun test` passes every test;
- `bunx tsgo --noEmit` exits 0;
- `bun eval/run.ts --tool "bun src/cli.ts" --cases eval/cases/fixtures.json --out a1r2-scratch` reports A1 MET, and
  no NOT MET for any other requirement.

Return the last lines of each.
