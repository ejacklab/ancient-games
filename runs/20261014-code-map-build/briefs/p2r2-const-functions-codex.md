# Brief — evaluator addition: functions held in constants

You wrote `code_map/eval/`. A reviewer found a case it does not cover. In the target code base (opencode) most
functions are held in constants: `const f = (...) => { ... }`, `const f = function (...) { ... }`, and Effect's
`const f = Effect.fn("Name")(function* (...) { ... })` (define a small Effect-like `fn` inside the fixture; no
dependency). Also object properties holding functions: `const svc = { get: (...) => { ... } }` and
`Service.of({ get })`.

Spec (`runs/20261014-code-map-build/spec.md`, "Call links"): the enclosing function of a call site is "the nearest
function, method or arrow, named by the `const x = Effect.fn(...)` or the property that holds it". Requirements:
`runs/20261014-code-map-vision-relay/result-trimmed.md` (A1 entry flows "as ordered steps with their decisions";
A2 chains).

## Add

- One fixture project `code_map/eval/fixtures/const-held/` with those forms, calling each other in a chain at least
  three levels deep, plus one test file (matching the case file's test pattern) that reaches the deepest one.
- Cases in `cases/fixtures.json` (with canned stub answers) that fail if a constant-held function is not walked:
  `chain` from and through a constant-held function (A2), `callers` and `callees` of one (A2), `tests` reaching one
  (A3), `map` of the folder where an exported constant-held function called from outside is an entry with its
  steps (A1), and `find "<words>"` matching a word that appears only in a comment or string inside one (A2; the spec
  says descriptions are matched "over names, comments and strings").
- `holdout.ts` must handle the new fixture.

## Must not

Write only under `code_map/eval/` and `code_map/test/eval/`. Do not read or write `code_map/src/`. No packages.

## Done when

In `code_map/`: `bun test test/eval` passes; `bunx tsgo --noEmit` exits 0; the stub passes every bundled case.
Return the new case ids and the last lines of each output.
