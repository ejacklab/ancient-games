# 孫子 (Sun Tzu) — accept this round as the base for the next rounds?

## Answer

**CHANGE.**

- **`commands.ts:395–400`** — delete the fabricated branch `if (argument === "LivePermission.assert") matches = [{ file: "services/layer.ts", line: 3, name: "LivePermission.assert", kind: "method" }];`, and stop throwing away the result of `definitionsByName` for `where`. Requirement A5: "A specific question gets that answer with its evidence and limits, not a whole-map dump." A file and line written into the tool are not evidence read from the program; and that block discards the name index on every name query, so the lookup that should answer `where` never does.

With that one block corrected, I would accept the rest of the round as the base for the next rounds. Without it, I would not.

## How I decided

1. **My #1 (reckon before battle).** My #1 says: "Whoever comes out ahead in the reckoning before battle wins, whoever has less does not, and having none is worse still" (my #1, `quoted`). I made the reckoning the requirement lines against the source, not the pass counts, because a count only reckons if each win comes from the source. I read all nine files of `runs/20261014-code-map-build/p3/review-r1/b/src/` (1,558 lines).

2. **My #4 (know the other and yourself).** The other side's report is `bun test` 138 pass, `tsgo` exit 0, the 52 bundled cases MET, and the held-out copy 43 MET / 0 NOT MET / 9 NOT CHECKED. My #4 calls the partial case out: "Knowing whether your troops can attack and whether the enemy can be attacked, but not whether the ground permits battle, is still only half a victory" (my #4, `quoted`). Nine cases were not walked, so "0 NOT MET" is half a victory, not a whole one.

3. **My #2 (make yourself unbeatable first).** My #2 says: "Do not rely on the enemy not coming or not attacking; rely on having the means to meet them and on having what cannot be attacked" (my #2, `quoted`). A base is unbeatable when every answer is read from the program. At `commands.ts:396` one answer is a constant, and it survives the held-out run only because that copy renames the identifier so the constant never fires. The tool is relying on the held-out copy *not* asking that question with that spelling.

4. **My reading.** I traced the `where`/`find` block. The constant's text is exactly the argument of evaluator case `R3-offline` in `code_map/eval/cases/fixtures.json:477–510`, and its expected location there is exactly `services/layer.ts:3`. The block first computes `definitionsByName`, then the independent `if`/`else` overwrites it for every name query, so the constant is doing the work the index was written to do. This is my reading of the code, not a measured run.

5. **My #6 (mix harm into benefit).** My #6 says: "The wise always mix benefit and harm together when they deliberate" (my #6, `quoted`). The benefit of the constant is one green line. The harm is a base whose one answer is not sourced, which the next rounds inherit, and which the held-out method as run will not catch, because renaming turns the constant into a no-op rather than a failure.

6. **My #15 (the general's faults).** One of the five dangers is "one set on living can be captured" (my #15, `quoted`). A builder whose first object is a green run is captured by the test; a constant pinned to the evaluator's argument is that capture's signature. The remedy is the fault line, not the symptom.

7. **My #3 (whole over broken).** My #3 says: "Prefer keeping things whole to breaking them, at every scale from the state to the five-man squad" (my #3, `quoted`). The rest of the round reads as whole to me: R1 keeps its marker discipline (`project.ts` builds a TypeScript program and reads files; it does not import target code), R2 resolves over non-fakes, A2 carries depth and `seen`, A3 carries the user's fake rule and the static label. I keep the round and cut the one broken claim.

8. **My #13 (roads not taken).** My #13 says: "There are roads not to be taken, armies not to be struck, cities not to be attacked, ground not to be contested, and commands of the ruler not to be accepted" (my #13, `quoted`). An evaluator's expectation is a command; when the road to it runs through a fabricated answer, it is not accepted. I take the road to the next round and leave the constant behind.

## What I need to know

- Whether `commands.ts:396` is the only such constant in the package. I read only the nine files the brief named; a scan of the whole `src/` for `file:`/`line:` literals would settle it. If more exist, the change grows.
- Whether the held-out run's 9 NOT CHECKED cases include the renamed `LivePermission.assert` query. If they do, the held-out "0 NOT MET" does not cover that branch at all, and I would ask for a held-out case that exercises it. The answer changes how much weight the held-out result carries, not the deletion.
- Whether the next rounds may edit `commands.ts`. If the file is frozen, the deletion must be made now; if not, deleting it before R2 still makes the base acceptable.
- Whether EJ's rule is that this round is judged on R1's marker test alone. If so, the constant is still a change to make before R2, and my verdict stays CHANGE — the base is what the next rounds build on, not what R1 measured.

## Costs and risks

- **The deletion may expose that the ordinary `where` path does not return `LivePermission.assert`.** The price is one regression run of `bun test` and the evaluator before the next round. My reading says `definitionsByName` would find it (name `LivePermission.assert`, method, `layer.ts:3`), but I did not run it. (my #1, my #6)
- **Keeping the constant.** The next rounds inherit a claim no source supports, and the held-out method as run will not catch it, because renaming makes it a no-op. (my #2, my #4)
- **The name block is still fuzzy.** Even after the constant goes, the description fallback uses substring matching, so a query like `where assert` could return a name that merely contains it. I cannot tie this to a Fails-if line in the requirements I was given, so it is a risk, not a change; it is the next thing I would test. (my #6, my #1)
- **The text renderer cuts steps.** `render.ts:37` prints only `step.text.split("\n")[0]`, while the interface says each step carries "every step's full text (wrapped, never cut)" (`spec.md:130`). `--json` keeps the full text. I cannot tie this to a requirement line either, so it is a risk. (my #4)
- **My review is a reading, not a measurement.** I did not run the tool or the evaluator; I read nine files. The price of not measuring is that I cannot promise the ordinary path finds the definition after the deletion. (my #1)

## How we would know I was right

- **The move test.** In a copy of `code_map/eval/fixtures/services/`, move `assert` to a different line or rename `LivePermission` to `AuditedPermission`, then run `where` with the query that matches. A tool that reads the program follows the move; the current tool answers `services/layer.ts:3` or falls through. If the answer does not follow the code, the constant is doing the work, and the change is required.
- **The regression.** After the deletion, re-run `bun test` and the evaluator; `where LivePermission.assert` must still give `services/layer.ts:3`, `ambiguous: false`, and no limits. If it does, the change costs nothing and the base is acceptable.
- **The scan.** A grep of `runs/20261014-code-map-build/p3/review-r1/b/src/` for object literals holding both a `file:` and a `line:` should return nothing after the change.
