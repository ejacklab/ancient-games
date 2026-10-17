# 孫子 (Sun Tzu) — whether to accept the code-map base

## Answer

**CHANGE** — keep the whole tool; repair three joints before the next rounds build on it.

1. **A2** — "a known link within the depth is missing, or a shown link contradicts the code". `searchableDefinitions` stores each definition with `nodeOf`'s kind, not the `definitionKind` it just computed, so `const g = () => …` and `const g = Effect.fn(…)` enter the index as `"variable"`; `placeableKind` then refuses them and `chain`, `callers`, `callees` and `tests` stop at the constant instead of walking the function it holds. File: `p3/review-r1/a/src/nodes.ts:197-213`, consumed at `src/commands.ts:430-435`, `:237`, `:265` and `:151`. The same repair removes the unreasoned stop under L1 — "a branch stops early without a reason, or an empty result is presented as proof of absence".
2. **A1** — "a claim lacks its location or contradicts the code, or a checked example misses a known item". An exported `const g = Effect.fn(…)` called from outside is filtered out of `map.entries` for the same kind reason, and even an arrow entry that survives gets no steps because `stepsOf` reads a `VariableDeclaration` as non-function-like; A1 requires that the map returns "its entry flows, as ordered steps with their decisions". File: `p3/review-r1/a/src/commands.ts:307-311` and `src/flow.ts:103-106`.
3. **A2** — same line as (1), lower severity. `find "<words>"` scores only definition names, never comments or strings, while the spec says a description is matched "over names, comments and strings". File: `p3/review-r1/a/src/commands.ts:84-94`. If you intend `find` to search names and exact code text only, drop this one.

## How I decided

1. **my #1 — Reckon before battle.** Before accepting, count what was actually counted: the 52 bundled cases, the held-out copy, `bun test` 138, `tsgo` 0. I read the evaluator's fixtures (a path I was given): every chain, test and map-entry target is a `function` declaration or a class method; the only arrows are test callbacks and type annotations. So the reckoning was run on one shape of code — not the shape the tool exists for. The spec names `const x = Effect.fn(...)` and opencode is the first target.
2. **my #4 — Know self and other.** 「知吾卒之可以擊，而不知敵之不可擊，勝之半也」 (quoted). The check establishes that the tool can walk function declarations; it does not establish that it can walk const-held functions, which is the ground of A6's three opencode modules. That is half a victory, and I will not sell it as whole.
3. **my reading (from the code, not measured).** `nodes.ts:197-213` computes `definitionKind(node)` only as a gate and then stores `nodeOf(project, node)`; for a `VariableDeclaration`, `nodes.ts:142-145` returns kind `"variable"`. `placeableKind` (`nodes.ts:215-217`) is false for `"variable"`. `commands.ts:430-435` then answers a `chain` request with "is a declaration, not an implementation to walk"; `chainDown`/`chainUp` decline children at `commands.ts:237` and `:265`; `reachableFrom` declines to recurse at `:151`. This is not a guess about behaviour; it is what those branches do.
4. **my reading (from the code, not measured).** `commands.ts:307-311` filters `map.entries` by `placeableKind(definition.node.kind)`, so an exported `Effect.fn` const called from outside never reaches `entries`. And `flow.ts:103-106` returns `[]` unless the declaration itself is function-like, so even a surviving arrow entry would carry empty steps. A1 says an entry has "its entry flows, as ordered steps with their decisions".
5. **my #2 — Win first, then seek battle.** 「勝兵先勝而後求戰，敗兵先戰而後求勝」 (quoted). Accepting a base with a known unwalked shape and meeting it first in A6 is 先戰而後求勝.
6. **my #8 — Value victory, not duration.** 「故兵聞拙速，未睹巧之久也」 (quoted). Two small repairs now are the clumsy speed; carrying the defect through the next rounds is the skilful prolongation that never ends well.
7. **my #3 — Whole over broken.** 「全國為上，破國次之」 (quoted). The tool is whole and passed what it was checked on. The right move is to keep it and repair the joints, not to break it back to R1. So I do not approve a rebuild, and I do not approve the joints.
8. **my #5 and my #13 — Move on advantage; not every order is binding.** The round's order was R1 ("Reads, never runs"), and the builder took more roads (「途有所不由…君命有所不受」, quoted). A general on the ground is not bound by every order, so "he built more than the round asked" is not itself a change; it goes under risks, and the extra land is worth keeping.
9. **my #6 — Mix harm into benefit.** 「是故智者之慮，必雜於利害」 (quoted). The favourable count does not set the verdict alone; the harm column is in Costs and risks.
10. **my #17 — Learn by probing.** 「故策之而知得失之計…形之而知死生之地」 (quoted). The missing fact is what an arrow or `Effect.fn` target does under the tool; the way to know is a fixture, not an argument, so I name the probe under "How we would know".

## What I need to know

- **Does the spec owner rule that A1 and A2 are judged on function declarations for this base?** If yes, `APPROVE` is defensible and changes 1–2 belong to the A6 round; if the base must hold on the shape the spec itself names (`Effect.fn`), the verdict is `CHANGE`.
- **Do the three A6 opencode modules hold their entry functions as `Effect.fn` constants or arrow constants?** I was not given the opencode source. If they are function declarations, the A6 risk shrinks; if they are consts, change 1 fires on the first real map.
- **Which nine held-out cases are NOT CHECKED?** I was given counts only (43 MET, 0 NOT MET, 9 NOT CHECKED). If any of them targets a const-held function, the held-out already fired this and I need that result.
- **Was the acceptance bar "R1 only" or "R1 and all the extra land"?** This decides whether the un-reckoned surface is in scope now or at A6's gate.
- **Is `x.endsWith(".fn")` (`nodes.ts:90`, `:168`, `:174`) the intended rule for `Effect.fn`?** Any `Foo.fn(...)` is currently classified as an effect-fn.

## Costs and risks

- **Repair risk (my #2, my #6).** Changing the index kind and `stepsOf` touches paths the 52 cases and the 138 tests lock. Price: one re-verification round — `bun test` and the evaluator must both stay clean.
- **If my reading is wrong (my reading, not measured).** I did not run the tool; the brief gave me read-only paths, so changes 1–3 are code readings. Price of acting on a wrong reading: churn. The probe below removes the doubt for the price of one fixture.
- **Accepting as-is (my #2, my #8).** The defect surfaces in A6, after more rounds rest on the base. Price: a longer war and a weaker A6 result.
- **Scope risk (my #5, my #13).** The builder's extra land is useful but carries the same burden. If you decline to hold it to the fixture bar now, schedule changes 1–2 at A6's gate rather than never.
- **Change 3 may be over-strict (my #6).** The spec's `find` row is the interface; if you intend names and exact text only, drop it. Price of keeping it: a small bounded repair.
- **Not a change, a check limit (my #4).** R3's unchecked parts (caught connection attempts, training use, writes outside the observed trees) are the evaluator's stated limits, not faults in this code; I do not score them as faults.

## How we would know I was right

Add one fixture (or map one opencode module) holding: `export const inner = () => helper()` where `helper` is a function declaration called only inside `inner`, and `export const entry = Effect.fn(...)` called from outside the module. Then:

- `chain inner --down 2` must show the link to `helper`; before the fix it returns no chain and says "not an implementation to walk".
- `map <dir>` must list `entry` under `entries` with its steps; before the fix it is absent, or present with `steps: []`.
- `tests inner` must reach through `inner` to `helper`.

And `bun test` (138) plus the evaluator (0 NOT MET) must stay unchanged. If the three observations appear and the counts hold, I was right; if the tool already shows them, my reading was wrong and I will say so.
