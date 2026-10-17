# 孫子 (Sun Tzu) — accept this round as the base?

## Answer
**APPROVE** — accept this code as the base for the next rounds. If the COO's numbers were taken on this exact nine-file tree (they say they were), I found no R2 requirement line it breaks, and the specific attempt-1 loss is closed.

## How I decided

1. **My #1 (Reckon before battle).** The round is a reckoning, and a reckoning is only as good as the entries in it. I laid the question out by the entries this round actually has: the R2 text in the requirements, the `Link`/`Limit` shapes and the "Call links (R2)" table in the spec, the frozen tests in `code_map/test/r2/`, the evaluator's R2 cases in `code_map/eval/cases/fixtures.json` with their fixtures, and the R1→R2 diff. The attempt-1 loss was a missing entry: the tool printed a place it had not compared against what `callees` could answer.

2. **My #1 again (the ordered chain).** The list gives the reading order as "the ground gives measurement, measurement gives quantity, quantity gives number, number gives the weighing of the sides, and the weighing gives victory" (quoted, list #1). I read in that order — requirement → spec shapes → frozen tests → evaluator cases → code — so the verdict rests on the requirement, not on the code's own claims.

3. **My #17 (Learn the enemy by probing and by signs).** The sign to read was the R1→R2 diff. Three additions carry the fix: `belongsTo`/`hasWrittenName` (`nodes.ts:272–289`) decide which calls belong to a place, treating an unnamed body written straight into a call as part of the enclosing place; `placeAround` (`commands.ts:216–243`) resolves a line at which no definition begins to the function written around it; and `commands.ts:249–252` routes that line to `placeAround`. Read together with `enclosingNode` (`nodes.ts:291–296`), every `from` the tool prints is the nearest function, and every nearest function is now answerable by `callees`. That is exactly the anonymous `function*` passed to `Effect.gen` that failed attempt 1.

4. **My #4 (Know whether you can fight; know the other side and yourself).** I separated what I know from what I was told. *Verified by reading:* the diff, the lookup path, the tests' anchors, the eight R2 cases and their `expect` blocks. *Reported, not reproduced:* `bun test` 179 pass, `tsgo` exit 0, the evaluator's R1/R2/R3/A1/A2/A3/A5/L1 MET, no NOT MET on the held-out copy, R2 MET on the private real-code set. I did not run the tool; the brief let me read only the named paths, so I answer on the reading and let the measurements carry the rest.

5. **My #2 (Make yourself unbeatable first).** "First make yourself unbeatable, then wait for the enemy to become beatable" (quoted, list #2). Tested against R2's four fails-if lines: implementations still go into `candidates` (`links.ts:416–419`), `to` is set only from a concrete candidate and never from `declaration` (`links.ts:429–430`), `testFake` comes from the user's `--tests` and is filtered out of `realImplementations` (`links.ts:419`), and unresolved/ambiguous are set from the count of live candidates (`links.ts:424–425`). The fix added no path that puts a declaration in `to`.

6. **My #13 ("There are roads not to be taken, armies not to be struck, cities not to be attacked, ground not to be contested, and commands of the ruler not to be accepted" — quoted, list #13).** The requirement is the limit. Every shape the code might miss that I could only guess at (types this hand-rolled lookup may not see) goes under Costs and risks or What I need to know, not under "change". A change has to be tied to a R2 line I can point at, and I cannot point at one.

7. **My #5 (Move only when it accords with advantage).** "Move when it accords with advantage and stop when it does not" (quoted, list #5). A change now would be moving on my discomfort that the builder stopped at its time limit, not on an advantage to the requirement. That is moving without advantage.

8. **My #8 (Value victory, not duration).** "clumsy speed is heard of, skilful prolongation has never been seen" (quoted, list #8). The round's victory condition — R2 met on tests, bundled cases, held-out copy and the private set — is reached on the code that exists. Holding the base back to perfect a lookup the round did not ask to be perfect would be the prolonged skill the text says it has never seen.

## What I need to know

- Was the private R2 case that failed attempt 1 a call inside a bare `Effect.gen(function* () { … })`, or inside one bound to a name (`const x = Effect.gen(…)`)? Both reach `placeAround`, but a bound one is treated by `hasWrittenName` as its own place even though `definitionKind` (`nodes.ts:171–185`) does not make it a definition — so `callees` on its line works while `where x` does not. This does not change my verdict on R2; it would change what the next round should cover.
- Does the private real-code set contain an interface that `extends` another interface, with the call made through the parent's member? If yes, and the tool answers unresolved there, then R2's first fails-if line is broken and my verdict flips to CHANGE on `links.ts:292` (`implementationsOfMember`) and `links.ts:155` (`memberOfClass`).
- Were all four reported measurements taken on this exact nine-file tree, with no later local edit?
- In the private run, did `--root` equal the tsconfig's project span? A narrower `--root` drops implementations through `isSource` (`project.ts:84–96`), so "every implementation" could be short while the run still looks clean.

## Costs and risks

- **The lookup is hand-rolled, not the checker's.** `implementationsOfMember` (`links.ts:292`), `memberOfClass` (`links.ts:155`) and `writtenObjectsOf` (`links.ts:264`) read classes that name the interface and object literals written where the type is expected. The spec names "the type checker's implementation lookup"; the code does not call it. If the checker sees an implementation these scans do not — an interface that `extends` another, a class expression, a nested class, an object literal with no contextual or annotated type, an overload signature — R2's "It also links to every implementation the type checker's implementation lookup finds" breaks. My reading; not measured (my #6, my #10).
- **A named `Effect.gen` body is a place that is not a definition.** `hasWrittenName` (`nodes.ts:272–277`) stops the walk at `const x = Effect.gen(function* () { … })`, but `definitionKind` (`nodes.ts:171–185`) does not list it, so `where`/`map` cannot name it. Link answers stay correct; A1's definition list and A2 by name are where it would show. My reading (my #4).
- **The failing private case is not in the repo.** The fix is verified against the frozen tests and the cases I can read; the exact opencode shape that failed attempt 1 is not among them, so my "closed" rests on the COO's report as much as on the code (my #4, my #11).
- **Cost against reading (L2).** `writtenObjectsOf` walks every file once and `implementationsOfMember` scans every top-level class per (owner, member). On 899k lines that is a real build cost, and L2 is not checked here (my #6, my #8, my #11).

## How we would know I was right

A round-trip measure on the private real-code set: take every `link.from` the tool prints, run `callees <from.file>:<from.line>`, and assert it is not the not-found answer and returns the link whose `from` is that same node. Re-run the exact private case that failed attempt 1 and check that the `from` line which answered not-found then now returns a link. Keep R2 MET on the evaluator's 60 bundled cases and on the held-out copy. **Observable result:** zero `from` nodes whose `callees` round-trip fails; the attempt-1 line answers with one link; R2 still MET. If any `from` line still answers not-found, I was wrong.
