# Brief — P3 round A1, round 3: build until the checks pass

You are the builder of the `code-map` tool. The tests and the evaluator already exist; other engines wrote them from
the same requirements. You work in a copy of the tool: `runs/20261014-code-map-build/builds/a1r3-opencode/code_map/`
(called **the copy** below).

## Read first

- `runs/20261014-code-map-vision-relay/result-trimmed.md`: the requirements. This round is **A1** ("The map of a
  module").
- `runs/20261014-code-map-build/spec.md`: the contract: command line, JSON shapes, call-link rules.
- The copy's `test/`: the tests your code must pass. This round's new test is in `test/a1/real-shapes-r3.test.ts`;
  the mixed-group test fails now.
- The copy's `src/`: the tool so far.

## What the failing test is about

`test/a1/real-shapes-r3.test.ts`, the mixed-group test. A sibling glob covers four plugin files that share a shape
and two odd files, one with plain helper functions and one with a constant object. Today the table lists all six
members and has **0 rows**, with no limit saying why, although the four plugins alone give rows. One odd member must
not empty the table. Compare the members that share a shape, and either mark the odd members `unclear` or name them
in a limit. The earlier sibling tests must keep passing.

## Write

Only files under the copy's `src/`. Use the `typescript` 5.8.2 compiler API, which is already installed, and no
other dependency. The tool must work on any TypeScript project, not only the test fixtures. Never match on fixture
file names, identifiers or line numbers: a held-out copy with changed names and lines is also checked.

## Must not

- Change nothing outside the copy's `src/`.
- Do not install packages. Never import, require or run a file of the target project.
- **Do not run git.** Use relative paths only. Never write into `node_modules/`.

## Time and progress

You have 20 minutes. Work in small pieces: one failing test group at a time. After each piece, append one line to
`runs/20261014-code-map-build/nodes/a1r3-build-opencode.progress.md`: the UTC time from `date -u +%Y-%m-%dT%H:%MZ`, the
piece, and done or failed.

## Done when

In the copy:
- `bun test` passes every test;
- `bunx tsgo --noEmit` exits 0;
- `bun eval/run.ts --tool "bun src/cli.ts" --cases eval/cases/fixtures.json --out a1r3-scratch` reports A1 MET, and
  no NOT MET for any other requirement.

Return the last lines of each.
