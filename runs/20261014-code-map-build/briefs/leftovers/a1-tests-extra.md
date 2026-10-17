# Brief — P3 round A1: more failing tests, for the shapes of real code (staging)

You wrote `runs/20261014-code-map-build/staging/test-a1/module-map.test.ts` earlier, or another engine did. Read it,
then add one more file beside it: `runs/20261014-code-map-build/staging/test-a1/real-shapes.test.ts`, with its
fixtures under `staging/test-a1/fixtures/`. Do not change the existing file.

A1's Fails-if line: "a claim lacks its location or contradicts the code, or a checked example misses a known item".
The links a map shows are claims. The limits it gives are claims too. Each shape below is a way a map was seen to
contradict the code, or to miss a known item, on a real TypeScript code base. Write one small fixture and at least
one test per shape. Check through `map` (`--json`), and where it fits, through `callers` or `callees` too.

1. **A local class built with `new`.** A file defines `class LocalError extends Base {}` and, in the same file or one
   it imports, calls `new LocalError(...)`. The link must point to the class in the repository. It must not carry
   the reason "outside the repository".
2. **A method on a value made by a factory and taken with `yield*`.** For example
   `const steps = yield* Steps.make(...)` and then `steps.attempt(...)`, where `make` returns an object whose
   `attempt` is defined in the repository. The link must reach that `attempt`, or carry a limit that does not
   contradict the code. "Outside the repository" contradicts it.
3. **An overloaded function.** It has two or three overload signatures and one implementation, all in the
   repository, and is called through an imported namespace (`Auth.header(...)`). The link must reach the
   implementation. "No implementation found" contradicts the code.
4. **A call through an interface that several objects implement**: for example `transport.prepare(...)`, where
   `transport: Transport` and three objects in the repository implement `Transport`. The link must list every
   implementation as a candidate, marked ambiguous. It must not list one of them as the target.
5. **A type from another package in the same repository** (a workspace package linked under `node_modules`). A call
   into it must not carry the reason "outside the repository". The fixture needs a second package folder and a link
   in its own `node_modules`. Build both inside the fixture with a small setup step in the test, not by hand.
6. **The edges of the paths given.** `map src/a` where functions in `src/b` call functions in `src/a`. Either the
   map lists those callers, or it carries a limit that names the scope it did not search.

Model the fixtures on the Effect service style in `code_map/test/r2/fixtures/` where it fits.

Use the same copy as before to run them: `runs/20261014-code-map-build/staging/cm-copy-a1/`. Refresh its `src/` from
`code_map/src/` first. Run `bun test test/a1` there.

## Pieces and progress

One shape at a time. After each, append one line to `runs/20261014-code-map-build/nodes/a1-tests.progress.md`: the
UTC time from `date -u +%Y-%m-%dT%H:%MZ`, the shape, and done or failed.

## Must not

- Write nothing outside `runs/20261014-code-map-build/staging/` and that progress file. Never write `code_map/`.
- Do not install packages. Do not run git.

## Done when

The new tests run in the copy, and each passes or fails for a reason you can state. Return:
- the test names and the shape each covers;
- which tests fail on the copied tool, and why;
- the last lines of the run.
