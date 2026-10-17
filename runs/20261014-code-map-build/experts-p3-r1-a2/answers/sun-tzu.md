# 孫子 (Sun Tzu) — accept the code-map build as the next base?

## Answer

APPROVE. The three changes attempt 1 required are present in the code I read, and on the evidence given every checked requirement line is MET (60 of 60 cases; held-out 43 MET, 0 NOT MET); the lines that are not checked (A6, L2) are the next rounds' work, not defects in this base.

## How I decided

1. **my #1 — reckon before battle.** The rule lays the war out and compares before committing. Self: `bun test` all pass, `tsgo` exit 0, 60 of 60 evaluator cases MET. Other: the held-out copy with changed names and lines — 43 MET, 0 NOT MET, 9 NOT CHECKED. A reckoning with no NOT MET favours going on. (my #1, `quoted`): 「多算勝，少算不勝，而況於無算乎？」 — "More wins, fewer does not, how much less none at all?"

2. **my #2 — be unbeatable first, then seek battle.** The attempt-1 CHANGE list was the unbeatable half, and it is now built, not promised: I read it in the code (step 7). The next rounds are the battle; this base takes the checked ground first. (my #2, `quoted`): 「故善戰者，立於不敗之地，而不失敵之敗也。是故勝兵先勝而後求戰，敗兵先戰而後求勝。」

3. **my #4 — know whether you can fight; know both sides.** The evaluator gives the tool's own side; the held-out copy gives the other side, and the builder did not write it. With danger low on both, the base can fight the next round. (my #4, `quoted`): 「知彼知己，百戰不殆；不知彼而知己，一勝一負；不知彼不知己，每戰必殆。」

4. **my #11 — foreknowledge from people, not from omens or measurement alone.** Acceptance does not rest on the code reading well, nor on the evaluator's shape: it rests on the COO running the tool as a black box on cases the builder did not choose, then on a held-out copy. (my #11, `quoted`): 「先知者，不可取於鬼神，不可象於事，不可驗於度，必取於人，知敵之情者也。」

5. **my #6 — mix harm into the benefit before deciding.** I looked for the harm first (Costs and risks): 9 lines NOT CHECKED, A6 and L2 untouched, one gap in the sibling table. None is a NOT MET, so they set the price of accepting, not the verdict. (my #6, `quoted`): 「故不盡知用兵之害者，則不能盡知用兵之利也。」

6. **my #8, applied by my reading — value victory, not duration.** Sending attempt 2 back a third time over breadth no requirement yet asks for buys thoroughness at the price of the campaign. The checked ground is won; do not spin the war out. (my #8, `quoted`): 「故兵聞拙速，未睹巧之久也。」

7. **my reading — the three attempt-1 changes, checked against the code.**
   - **(a) functions held in constants, including `Effect.fn`, indexed and walked as functions (A2).** `nodes.ts:171` gives a variable, property or property-assignment an `arrow`/`function` kind when its initializer is one; `nodes.ts:181` returns `effect-fn` for a wrapper call; `nodes.ts:109` (`wrapperBody`) finds the function passed to a callable wrapper, which is how `Effect.fn("Compute")(function* …)` is recognised; `nodes.ts:248` (`placeableKind`) admits `arrow`, `function`, `effect-fn`, `method`. `commands.ts:46` (`keysOf`) and `commands.ts:52` (`buildIndex`) index both the declaration's line and the implementation's line; `commands.ts:206` (`walkTarget`) and `commands.ts:180` (`reachableFrom`) walk the implementation. Cases A2-const-callees, A2-const-callers, A2-const-chain and A2-const-chain-through exercise exactly this.
   - **(b) exported constant-held entry functions, with their steps, in the map (A1).** `commands.ts:360` builds `entries` from functions called from outside the mapped files, filters by `placeableKind` and `isExported`, and takes steps from `flow.ts:103` (`stepsOf`), which reads the implementation body. `commands.ts:223` (`isExported`) also falls back to the module's export symbols, which is what makes `export const submit` work when the `export` keyword sits on the statement, not the declaration. Case A1-const-map expects `map.entries[].fn` at `flow.ts:25` with the steps `if (value < 0) return 0;` and `return compute(value);`.
   - **(c) `find` matching words in comments and strings (A2).** `commands.ts:104` (`writtenText`) collects the leading and trailing comment ranges and scans the declaration for comment, string and template tokens; `commands.ts:125` (`matchesByDescription`) ranks name matches above words in that written text; `commands.ts:449`–`commands.ts:457` falls back to it. Cases A2-const-find-comment and A2-const-find-string exercise this.

8. **my reading — what that evidence does not show.** Eight of the sixty cases are the builder's own fixtures, written for the three changes the builder was told about; the held-out run is the stronger sign. It reports 43 MET, 0 NOT MET, 9 NOT CHECKED, but the 9 are not named to me. So I accept the base on the checked lines and do not claim A6 or L2.

## What I need to know

1. **Do the three A6 modules have const-held siblings?** If `packages/core/src/session`, `packages/core/src/tool` + `permission.ts`, or `packages/ai` has sibling files whose shared exports are `Effect.fn` constants rather than `export function`, the sibling table (A1) will come back with `members` set but no rows and no limit. If they do, I would want that fixed before A6 is claimed; if their siblings are ordinary `export function`s, it does not bite this round.
2. **Which 9 lines are NOT CHECKED on the held-out copy?** If any is an A1, A2 or A3 line rather than A6, L2 or the P6 agent lines, my reading of "all checked lines MET" is narrower than I have taken it, and my answer becomes conditional on those lines.
3. **Does "base for the next rounds" mean the next round may start from this code, or that every requirement must be MET now?** If every requirement, then A6 and L2 are still NOT CHECKED, and I can approve the base only, not the finished tool.

## Costs and risks

- **The scale is untested (my #4; L2's line "it leaves out correctness, the build cost, the reading tokens or the time, or hides a worse result").** Every measurement given is on small fixtures; the first target is about 899,000 lines, and the map's build cost is part of L2 and has not been measured. Price: the first opencode run may show a cost the fixtures cannot.
- **The sibling table reads only `export function` declarations (my reading; `siblings.ts:11`–`siblings.ts:18`).** A sibling pair sharing `const x = Effect.fn(…)(…)` yields `{members, rows: []}`, with no `unclear` row and no limit. My reading of A1 ("a table of what siblings share and where they differ, when sibling implementations exist"; Fails if "a checked example misses a known item") is that this is a real input where the table would miss a known item. No checked example exercises it, so I do not make it a CHANGE; it is the first place to put a case when A6's case files arrive.
- **The interface lookup scans all files per owner and caches per source file (my reading; `links.ts:216`–`links.ts:233`).** On opencode's size this is the part L2's time line is most likely to flag. Price: a slow or memory-heavy first opencode run.
- **The count rests on the builder's fixtures plus one held-out copy (my #1 and my #11).** A builder who knows the test can fit it; the held-out copy offsets this, but 9 of its lines are NOT CHECKED. Price: a strong base, not a complete reckoning.

## How we would know I was right

- **Observable result 1:** re-run the evaluator on this code and get R1, R2, R3, A1, A2, A3, A5 and L1 MET at 60 of 60, with the same held-out result (43 MET, 0 NOT MET). If any of those flips to NOT MET, APPROVE was wrong.
- **Observable result 2:** run the COO's three A6 opencode case files. A6 is MET when `map` on each of the three modules passes A1's checks, including a sibling table with real rows if those modules' siblings exist. If A6 fails on the sibling table, or on `find`/chain over const-held `Effect.fn` functions, my approval was premature.
- **Observable result 3:** the L2 measurement reports correctness, total tokens including the map's build cost, and elapsed time, and says plainly when reading is cheaper. If build cost dominates at opencode scale, the base will need a performance round before L2 can pass.
