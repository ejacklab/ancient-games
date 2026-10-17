# Brief — P3 round A1, round 2: three more failing tests for real-code shapes (staging)

Add one file: `runs/20261014-code-map-build/staging/test-a1/real-shapes-r2.test.ts`, with its fixtures under
`staging/test-a1/fixtures/`. Do not change the existing files there. Read `real-shapes.test.ts` for the style, and
`runs/20261014-code-map-build/spec.md` for the JSON shapes.

A1's Fails-if line reads: "a claim lacks its location or contradicts the code, or a checked example misses a known
item". Each shape below was seen to fail on a real TypeScript code base, written in the Effect service style. Write
one small fixture and at least one test per shape.

1. **`where <Namespace>.<member>` for a service.** A file `permission.ts` defines:
   - an `Interface` with `readonly assert: (...) => Effect<...>`;
   - a tag `class Service extends Context.Service<Service, Interface>()("@app/Permission") {}`;
   - a layer that defines `const assert = Effect.fn("Permission.assert")(function* (...) {...})` and returns
     `Service.of({ assert })`.

   An `index.ts` re-exports it with `export * as Permission from "./permission"`. Elsewhere, in other files, two
   unrelated objects have a property path ending in `permission.assert`, for example
   `context.permission.assert = (...) => ...`.

   `where Permission.assert` must include the layer's `assert` constant, and may include the interface member. The
   two unrelated objects must not be the only matches. If they are listed at all, the answer is ambiguous.
2. **A sibling group shaped like plugin tools.** Write four files, each under `tools/`. Each exports `Input` and
   `Output` schemas (`Schema.Struct(...)`, with minimal Effect-like types defined in the fixture) and a tool built by
   a call, for example `export const tool = Tool.make({ name, input: Input, execute: Effect.fn("x")(function* (input)
   {...}) })`.
   - All four check a permission in their `execute`.
   - Two read files and two write files.

   `map tools --siblings 'tools/*.ts'` must return sibling rows: at least one `shared` concern (the permission check)
   and one `varies` concern (read against write), each row with locations.
3. **An interface whose implementations are objects returned from functions in different files.** Write `transport.ts`
   with `interface Transport { prepare(...): ...; execute(...): ... }`, and three files, each exporting a factory
   `export const httpTransport = (...): Transport => ({ prepare: ..., execute: ... })`. One factory returns an object
   built in a nested helper.

   A call `transport.prepare(...)` through a `transport: Transport` must list all three `prepare` implementations as
   candidates, and be marked ambiguous.

Run them in `runs/20261014-code-map-build/staging/cm-copy-a1/`:
1. Refresh its `src/` from `code_map/src/` first.
2. Copy your file and fixtures into its `test/a1/`.
3. Run `bun test test/a1` there.
4. Run `bunx tsgo --noEmit` there too. Your fixtures and test must type-check: annotate recursive functions, and do
   not import packages that are not installed.

## Must not

- Write nothing outside `runs/20261014-code-map-build/staging/`. Never write `code_map/`.
- Do not run git, and install nothing.

## Done when

The new tests run, and each passes or fails for a reason you can state. tsgo reports no error in your files. Return:
- the test names;
- which tests fail on the copied tool, and why;
- the last lines of the run.
