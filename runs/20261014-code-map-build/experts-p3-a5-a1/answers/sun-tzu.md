# 孫子 (Sun Tzu) — accept round A5 as the next base?

## Answer

**APPROVE.** On the facts given — `bun test` 192 pass, `tsgo` exit 0, the evaluator MET on R1/R2/R3/A1/A2/A3/A5/L1, the held-out copy with no NOT MET, and the private opencode set unchanged from round R2 — this round's one change (two hunks in `links.ts`) buys the missing caller evidence for a wrapper-held function without costing a single already-MET line, so it is fit to carry the next rounds. The approval is conditional on the four tests that failed before this round being among the passes now (see "What I need to know").

## How I decided

1. **my #1 (Reckon before battle)** — the rule is to "compare the two sides on seven questions" before committing. Here the count is the comparison: 192 pass, `tsgo` exit 0, eight requirement lines MET, held-out with no NOT MET, private set unchanged. 「多算勝，少算不勝，而況於無算乎？」 (`quoted`). The base comes out ahead on the reckoning, so I do not refuse the ground.

2. **my #4 (Know whether you can fight)** — know yourself and the other side: 「知彼知己，百戰不殆」 (`quoted`). Myself is the 60 bundled cases and the frozen A5 tests; the other side is the held-out copy with changed names and lines, and the private set from the real opencode code. Both sides are reported, and neither shows a loss.

3. **my #2 (Make yourself unbeatable first)** — the next rounds will stand on this base, so the question is whether anything known breaks it, not whether the enemy happens to stay away: 「無恃其不來，恃吾有以待之；無恃其不攻，恃吾有所不可攻也。」 (`quoted`). The private set's "no change from round R2" and the kept MET lines are that "means to meet them".

4. **my #17 (Learn the enemy by probing and by signs)** — the held-out copy and the private set are the probes (形/角 probes), and the signs read back are "no NOT MET" and "no change": 「故策之而知得失之計，作之而知動靜之理，形之而知死生之地，角之而知有餘不足之處。」 (`quoted`). No sign of a break appeared.

5. **my #8 (Value victory, not duration)** — 「故兵貴勝，不貴久。」 (`quoted`). The round's whole cost is one added predicate and one reused helper; it cleared four failing tests. Prolonging the round for more polish is the "skilful prolongation" the source says it has never seen.

6. **my #3 (Whole over broken)** — "Prefer keeping things whole to breaking them" (`quoted`). The diff keeps all nine files and every previously MET line whole; nothing was broken to win a line.

7. **my #13 (Not every road is taken)** — 「途有所不由…君命有所不受。」 (`quoted`). A6 and L2 are not checked in this round; that is a named limit of the ground, not a defect in the code, and it does not stop A5 from being the base.

8. **my #11 (Foreknowledge must come from people)** — the foreknowledge here comes from a private set drawn from the real opencode code and an evaluator built by a different hand (Codex), not only from the builder's own fixtures: 「必取於人，知敵之情者也。」 (`quoted`). That is the part of the evidence I weight most.

9. **my reading** — the change is narrow. `isWrapperResult` now also returns true for a written function type, and `namedImplementation` still returns the callee's written declaration only when `definitionKind` is truthy, i.e. only when that declaration carries a body (arrow, function expression, or a wrapper body). That guard is what keeps R2's "a declaration is presented as proof of an implementation" from firing on the code I read. The second hunk in `lookupImplementation` replaces the same condition with the new `isFunctionType` helper — same test, no new behaviour.

10. **my reading** — "the private set shows no change from round R2" proves no regression; it does not prove the mended path is exercised anywhere in the real opencode code. I record that under costs, not as a change, because I found no requirement line the code contradicts.

## What I need to know

- Are the four tests that failed before this round among the 13 A5 tests, and are all 13 among the 192 now passing? If any still fails, my approval is withdrawn and those tests are the change.
- Does the private set contain at least one `export const f = Effect.fn(...)` held function whose callers are asked for? If not, "no change" is silent about the very path this round mended, and the fix's worth on the first target is unmeasured.
- Are A6 and L2 deliberately held for a later round? If the next rounds build A6 on this base, A6's footing remains unproven.

## Costs and risks

- **The widened predicate is also a handle (my #15, my #10).** `isWrapperResult` now answers yes to every written function type, not only a wrapper's return. The `definitionKind` guard limits what that can resolve to today, but a future caller of the predicate inherits the wider answer. The price of the fix is a broader test on a shared path.
- **The new path is proven on fixtures, not on the real ground (my #11).** The private set's "no change" is a shield against regression, not evidence for the fix; that evidence lives in the bundled and frozen cases.
- **Accepting carries two unproven lines (my #13, my #1).** A6 and L2 are NOT CHECKED. Accepting the A5 slice means the next rounds inherit a base whose A6 and L2 behaviour has not been counted.
- **The fix does not name what it excludes (my #7, deception is not wanted here).** For a declaration the tool cannot classify, the call may still stop as unresolved; that is the safe side, but the base's answers should keep saying so.

## How we would know I was right

- **A measure:** run the frozen A5 tests and the full suite on this accepted copy and see 13 of 13 A5 tests and 192 of 192 total pass, `tsgo` exit 0, and every previously MET evaluator line still MET. If any MET line flips, I was wrong.
- **A probe of the new path:** add one case shaped `export const f = Effect.fn("F")(function* () { … })` with a caller outside the module, and ask for `callers`. A correct base returns that caller with its call site. If it returns none, or any shown link contradicts the code, the fix did not hold and the base should not have been accepted.
- **An observable on the real ground:** run the private set again. "No change from R2" is the confirmation I rest on; any change there is the signal that my reckoning was too favourable.
