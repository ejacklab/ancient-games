# A1 test handoff

Tests: [module-map.test.ts](test-a1/module-map.test.ts). Fixtures: `test-a1/fixtures/`.
Copy: `cm-copy-a1/`, with `node_modules -> ../../../../code_map/node_modules`.
Full output: [a1-tests-run.log](a1-tests-run.log).

Ran `bun test test/a1` from `cm-copy-a1/`: exit 1, 13 pass, 3 fail.
The three failures expose an empty sibling table for exported `Effect.fn` constants.
The copied `src/siblings.ts` only collects exported function declarations; all three fixture tools export their `execute` as a constant.

I wrote these checks. Their keys use manually chosen source anchors and expected calls, not the tool's parser.
They exercise two Effect-style projects (`service-intake`, `tool-siblings`) and one ordinary TypeScript project (`manifest-flow`).
The checks do not establish A1 for other projects or independently evaluate arbitrary natural-language claims.
No packages were installed; `code_map/` was not modified. The builder can copy the contents of `test-a1/` to `code_map/test/a1/` without changing relative paths.

Requirement check for the brief's testable clauses: who decides — pass; one thing — pass per failure condition; unit — pass; can it fail — pass; weak words — pass with the given fixtures and A1 decisions; level — pass as the task's acceptance conditions; basis — pass (A1, the spec and owner's provisional decisions); links — pass. No missing threshold or sibling decision was supplied by me.

| Test name | A1 Fails-if part | Copied tool | Failure reason |
|---|---|---|---|
| A1 service definitions, call evidence and entry decisions — "a claim lacks its location" | a claim lacks its location | PASS |  |
| A1 class methods and nested loop, else and catch evidence — "a claim lacks its location" | a claim lacks its location | PASS |  |
| A1 sibling concern cells identify their source — "a claim lacks its location" or "a checked example misses a known item" | a claim lacks its location; a checked example misses a known item | FAIL | Three sibling members, zero rows; no explanation. |
| A1 Effect entry selection respects exports and the requested module boundary — "contradicts the code" | contradicts the code | PASS |  |
| A1 ordinary entry excludes an uncalled export and a private helper — "contradicts the code" | contradicts the code | PASS |  |
| A1 Effect flow preserves source order and both decision branches — "contradicts the code" | contradicts the code | PASS |  |
| A1 long and multiline step text is complete and cites the actual source — "contradicts the code" | contradicts the code | PASS |  |
| A1 typed service call cites its real layer implementation and module-local caller — "contradicts the code" | contradicts the code | PASS |  |
| A1 definitions include Effect constants and both forms of layer service method — "a checked example misses a known item" | a checked example misses a known item | PASS |  |
| A1 definitions include ordinary functions, a class and its method — "a checked example misses a known item" | a checked example misses a known item | PASS |  |
| A1 outgoing links include construction, a method call and calls outside the module — "a checked example misses a known item" | a checked example misses a known item | PASS |  |
| A1 inline Service.of method has an incoming service-call link in the module map — "a checked example misses a known item" | a checked example misses a known item | PASS |  |
| A1 Effect-constant siblings report their shared validation step — "a checked example misses a known item" | a checked example misses a known item | FAIL | No concern rows for the known shared validation. |
| A1 Effect-constant siblings report their differing preparation steps — "a checked example misses a known item" | a checked example misses a known item | FAIL | No concern rows for the known differing preparation. |
| A1 omitting the sibling rule omits the table and states the A1 limit — "a checked example misses a known item" | a checked example misses a known item | PASS |  |
| A1 the user glob selects the sibling members rather than every similar tool — "contradicts the code" | contradicts the code | PASS |  |

Last lines of the full run:

```text
 13 pass
 3 fail
 1691 expect() calls
Ran 16 tests across 1 file. [7.07s]
```
