# P1 experiments: results (COO, 2026-10-14)

Script: `p1-experiments.cjs`. Outputs: `p1-E1.txt` through `p1-E4.txt`. Target: opencode `6dc4d4e`, TypeScript 5.8.2
LanguageService. Predictions were logged in `state.md` before the runs.

## E1: references to `Permission.assert` (`permission.ts:106`)

20 references: 1 definition, 1 shorthand in `Service.of` (`permission.ts:339`), and 18 call sites. The call sites
include `subagent.ts:139`, where `permission` and `.assert` sit on separate lines.

**Prediction** (Dave): at least 2 of the 19 non-definition references are not call sites. **Failed:** only 1 is.

**Design fact:** 17 of the 18 calls sit inside anonymous `function*` or arrow bodies. The tool must name the
enclosing `const x = Effect.fn(...)` or the property that holds the function, or the callers are nameless.

## E2: the implementation lookup at one call site per `Context.Service` tag in `core/src`

71 tags had a member call site; the lookup returned:

| Result | Tags |
|---|---|
| exactly one implementation | 63 |
| several implementations (for example `filesystem/watcher.ts`, `config.ts`) | 7 |
| none | 1 |

20 tags had no member call site in src, and 2 had no interface (`noCallSite` / `noInterface`).

Of the 63, my classifier auto-labelled 22 as a function body. I hand-checked 11 of the other 41:
- 10 are function implementations held as object properties (`get: Effect.fn("Agent.get")(...)`);
- 1 is a plain value (`integration.ts:706`, `revision: state.revision`).

**Prediction** (Dave): most resolve. **Held.** Misses would cluster where no shorthand `Service.of` is used:
**not testable**, because there was only 1 "none".

**My reading:** the stock lookup works broadly. The cases that need a rule are "several", which call for choosing by
layer wiring, and plain values.

## E3: one program over `core` src and test

- 750 root files, 2,827 source files, 2.8 s, about 896 MB heap. Sources resolve to `.ts`; the 2 repo `.d.ts` files
  are hand-written declarations in `src`.
- At `edit.ts:275`, the lookup returns 20 implementations: the real one (`permission.ts:231`) and 19 test mocks
  (`test/*.test.ts`, `test/plugin/fixture.ts`).
- References to `Permission.assert` including tests: 44 in 34 files, 17 of them test files, in 12 ms.

**Predictions** (Dave): the heap is above 663 MB, **held**; the result is `.ts` or `.d.ts`, **resolved: `.ts`**;
several implementations, **held**.

**Design fact:** a test file's own wiring (`.replace` or `Layer.mock`) decides which implementation that test
reaches. The lookup alone cannot.

## E4: a program over `packages/ai`

217 root files, 603 source files, 0.9 s, about 252 MB. It builds.

## E5: a network namespace for the R3 check

`unshare -n` fails ("Operation not permitted"), as 孫子 said. `unshare -rn true` exits 0. The evaluator can use
`unshare -rn`.
