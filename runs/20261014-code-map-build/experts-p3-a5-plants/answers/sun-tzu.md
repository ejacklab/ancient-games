# 孫子 (Sun Tzu) — do the five plants prove A5's checks catch an A5 failure?

## Answer

No. The plants show the round's gate catches gross breakage — all five fail `bun test` — but they do not show A5's own check catches A5 failures: only one plant (`where-inside-dump`) is marked A5 NOT MET; the other four are charged to R2/A1/A2/A3/L1, and no A5 assertion lives on the held-out or private sets. One concrete A5 failure passes every check (below).

Per plant:

- **limits-dropped — not enough.** A real A5 failure (answers lose their limits), but A5's evaluator line never fires; caught by 7 frozen tests and under L1/R2/A1/A3.
- **where-inside-dump — enough.** A real "answer only inside a dump"; the A5 case `A5-specific-answer` fires, and the frozen tests fire.
- **site-dropped — not enough.** A real "without its evidence", but A5's line never fires; caught by 21 frozen tests and under R2/A1/A2/L1.
- **callers-unasked-map — not enough.** A real "whole map produced unasked", but the evaluator charges it to A1/A2 through the generic contract, not to A5; only a builder-readable frozen test names it A5.
- **not-found-limit-dropped — not enough.** A real "without its limits", but A5's line never fires; caught by one frozen test and under L1.

**Verdict: STRENGTHEN**, before closing A5 — tie each change to A5's Fails-if line: (a) "an answer comes only inside a dump": add an A5 *text-format* case that can fail a dump (today the text case only checks two strings are present); (b) "without its evidence": add an A5 case on a link-bearing command (`callers`/`callees`/`chain`/`tests`), because every A5 case today runs only `where`; (c) "without its limits": add A5 cases on limit-bearing paths (`where <missing>` → not-found; `callers` with no `--tests`), because `A5-specific-answer` expects `limits: []`; (d) "a whole map is produced unasked": assert `map` absent in an A5 case, so the attribution is A5 and not only A1/A2; (e) put at least one A5 assertion on the held-out rename/shift copy and the private opencode set, where the builder cannot read it.

## How I decided

1. **Laid the requirement out before judging it** (my #1, "So lay it out by five matters, compare it by seven reckonings, and search out the true situation", `quoted`). A5's Fails-if has three prongs: (a) an answer comes only inside a dump; (b) an answer comes without its evidence or limits; (c) a whole map is produced unasked. I tabulated each plant against the prong it imitates and the check that actually fails.

2. **Read the evidence table as a count** (my reading). All five plants fail `bun test` (7, 4, 21, 1, 1). The evaluator marks A5 itself NOT MET for 1 of 5. The other four are marked under R2, A1, A2, A3, L1. The core set separates only `site-dropped` from its A1/A2 baseline.

3. **Asked the other side's ground** (my #4, "There are five ways to know victory: one who knows when he can fight and when he cannot wins…", `quoted`). I checked what the evaluator's A5 cases exercise: `A5-specific-answer` and `A5-default-text` both run only `where leaf`. They never run `callers`, `callees`, `chain`, `tests`, `find`, or `map`, and never walk a path that must carry a limit. So prongs (b) and (c) have no A5 case at all.

4. **Verified why the wrong lines fire** (my reading, `code_map/eval/contract.ts` and `run.ts`). `validateAnswer` runs on every JSON case and rejects a section not belonging to its command (`allowedSections`); for text cases it is skipped and only `textIncludes` substrings are checked. That is why the unasked map on `callers` is charged to A1/A2 — whichever A1/A2 case runs `callers` — and never to A5, and why text output is checked only for presence, never for focus.

5. **Linus — real failure, caught for the right reason?** (my #15, "These five are the general's faults, the calamities of using troops", `quoted`). All five are faults a user would see, and each maps to a prong: 1→(b), 2→(a), 3→(b), 4→(c), 5→(b). But only plant 2 is caught *on A5's line*. Plants 1, 3 and 5 are caught on other requirements' lines; plant 4 is caught on A1/A2 (and by one A5 frozen test). The round reads 5 of 5 only because the builder-readable frozen tests also fail.
   **A concrete A5 failure that passes every check** (my #10, "an army in its victory avoids the solid and strikes the empty", `quoted`): the solid is `--json`; the empty is the default text output. Make the text renderer print every definition in the program (or the whole module map) for any question, while ensuring the asked name and its `file:line` appear somewhere in that text. This passes because all 13 frozen tests append `--json` and never read text; `A5-default-text` only requires that `leaf` and `chain/logic.ts:3` appear; `validateAnswer` is skipped for text; every other requirement's case is JSON; `tsgo` is untouched; bundled A5 stays MET; and the held-out and private sets never mark A5 NOT MET. A user asking one question sees the answer only inside a dump — the Fails-if clause verbatim.

6. **范蠡 — close now or first do something?** (my #2, "Do not rely on their not coming; rely on having the means to meet them", `quoted`). The round's A5 defense rests on the builder not shipping an unread fault — reliance on the other side's restraint, not on a check of ours. And (my #11, "it must be taken from people who know the enemy's situation", `quoted`): the held-out copy and the private opencode set are exactly those people, and neither carries an A5 assertion. Something must be done first: strengthen the prongs, then close.

7. **孫子 — caught only by readable checks? What is left to character?** All five. Plants 1, 3, 4 and 5 are caught (for A5 anyway) by the frozen tests, which the builder may read; plant 2 is caught by the bundled A5 case, also readable, and its held-out NOT MET is the same case transformed. No plant is caught by an A5 check the builder cannot read. (my #7, "War is the way of deception", `quoted`; my #10.) Left to the builder's good character is the behavior no readable check can fail: the focus of the default text output, and A5-relevant limits or evidence on queries and reasons the frozen and bundled cases never exercise. (my #12, "So the skilled fighter seeks it in 勢 and does not demand it of people; so he can choose people and rely on 勢", `quoted` — change the conditions, not the person.)

8. **老子 — too heavy-handed?** (my #17, "So reckon them to know the calculation of gain and loss; stir them to know the pattern of movement and stillness; give them form to know the ground of death and life; test them to know where there is surplus and shortage", `quoted`). These are the loud probes: drop every limit, delete every site, return every definition, attach a whole map. Each trips many tests at once (21, 7, 4, 1, 1), so the result cannot say which check did the work, and cannot say whether a quiet fault passes. A small, quiet fault shows more: leave JSON intact and make only the text output verbose; or keep the match exact and the fields well-formed but swap one branch's specific limit for a generic `other` limit, or move the limit to a path the frozen test does not touch (e.g. `find`'s no-match). One prong at a time.

9. **Weighed the move** (my #5, "Do not move without advantage… move when it accords with advantage", `quoted`). Closing now buys time and leaves the dump, the untested evidence prong, and the untested limit prongs in place. The advantage of a few targeted cases outweighs the delay.

10. **Kept the harm column honest** (my #6, "So the wise one's deliberation always mixes benefit and harm", `quoted`). The plants are an honest harm column as far as they go — they are the COO's, and they share the COO's blind spots, exactly as the evidence file says. But the benefit side, "5 of 5 caught", is overstated for A5.

## What I need to know

- Do the held-out copy and the private 8-case set contain any A5 case beyond the two bundled `where leaf` cases — in particular a link-bearing, limit-bearing, or text-focus case? If they do, the hidden A5 signal is stronger than the table shows and my STRENGTHEN verdict narrows to the text prong alone. I have not seen those case files; the identical bundled/held-out NOT MET columns suggest they do not, but that is inference.
- Does the round gate treat a frozen-test failure as A5's own result, or only as "`bun test` failed"? The plants all fail the frozen tests, so under the gate as written all five already fail the round. My verdict is about the evaluator and the hidden layer — which is what matters when a future fault is *not* in the frozen set.
- Is the default text output governed by A5, or is `--json` the contract and text only a convenience? The spec calls text the default for an agent, so I assumed it is governed. If it is not, drop STRENGTHEN item (a).

## Costs and risks

- Adding cases lengthens the round (my #8, "So in war value victory, not duration", `quoted`). Keep them few: one text-focus, one link-evidence, one or two limit cases, one map-absent, one hidden A5 assertion.
- A text-size or exclude check can be brittle and fail on harmless formatting (my #6). Set the bound by the observable A5 failure — a one-name question answered with a definitions dump — not by taste.
- Closing now bets on the builder's restraint (my #2). The price is a shipped text dump and unstated limits at opencode scale, which no hidden check would report.
- Training the checks only on loud plants (my #10) leaves the quiet flank — text, and limits on untested branches — open.

## How we would know I was right

Write the text-dump fault as a sixth plant and run it through the round as it stands: it should pass all 13 frozen tests, keep A5 MET on bundled and held-out, leave the private A1/A2 baseline unchanged, and keep `tsgo` at 0. If it passes, the gap is real. Then add the four targeted A5 cases (text focus, link evidence, limit-bearing path, map-absent) plus one hidden A5 assertion, and re-run the sixth plant together with a quiet limit-substitution plant: each should then be marked NOT MET on A5's line, while `site-dropped` and `where-inside-dump` stay NOT MET. If a quiet fault is still missed, the checks are still reading presence, not focus.
