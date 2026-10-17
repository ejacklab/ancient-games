I'll read the brief first.
# 老子 (Laozi) — Do five loud plants show A5's checks would catch an A5 failure?

## Answer

**Per plant**

1. **limits-dropped — not enough for A5.** Both A5 cases still read MET under it; the catch came from L1, A1, A2, A3 and R2 lines, and from tests asserting *their* limits. It proves the limits log is load-bearing elsewhere, not that A5's own "or without its … limits" clause is checked.
2. **where-inside-dump — enough, but it does not say which check caught it.** The only plant that moves A5's own line, and also the loudest form of the fault: stuffing `matches` with every definition also breaks A2's exact-match and ambiguity checks, so the credit cannot be assigned to A5.
3. **site-dropped — not an A5 plant at all.** 21 tests, R2 and A1; A5 never sees it. Good news about the tests, no news about A5.
4. **callers-unasked-map — the most A5 of the five, and the thinnest cover.** One assertion (`expect(answer.map).toBeUndefined()` in one test) and zero A5 evaluator cases. It was one line from being invisible.
5. **not-found-limit-dropped — enough for L1, not for A5.** One test, one L1 case; A5's own missing-name test asserts the same limit, so the two overlap rather than cover.

**The small, quiet fault that would show more** (each is one or two lines, each passes every check as they stand): (a) in `render.ts`, append the program's definitions to the default text answer — every one of the 13 frozen tests and all 60 evaluator cases run `--json`, and `A5-default-text` only asserts the text *includes* the location; (b) in the `where`/`find` branch, `answer.matches = matches.slice(0, 25)` — a partial list presented as the answer with no limit saying so, past A2 (fixtures are small) and past L1 (no fixture exceeds 25); (c) in the `callees` branch, add `answer.matches = [place.node]; answer.ambiguous = false;` — one answer section more than was asked, in a key that both `expectFocused` and `contract.ts`'s `allowedSections` permit.

**STRENGTHEN**, tied to A5's Fails-if line: (1) *"a whole map is produced unasked"* — one A5 check on the default text channel, which `spec.md:37` calls the default, failing when the text carries any `file:line` the question did not ask for; (2) *"or without its … limits"* — one A5 case whose correct answer must carry a named limit, because `A5-specific-answer` currently expects `limits: []`, so by construction a limits-free answer is A5-MET; (3) *"an answer comes only inside a dump"* — narrow the one clause in `expectFocused`/`allowedSections` that lets `matches` ride along on `callers`/`callees`/`chain`/`tests`, exempting the ambiguous-name branch the interface requires.

## How I decided

1. **my #2** — "Know what is enough and you are not disgraced; know to stop and you are not endangered" (`quoted`). Five of five caught is enough to know the checks bite. Nothing here argues for rebuilding the round; it argues for one quiet check before closing.
2. **my #11** — "weakness overcomes the hard and strong … everyone in the world knows it and no one can practise it" (`quoted`). Four of these five plants are the loud kind, the kind everyone catches. The fifth, `callers-unasked-map`, is the soft kind, and it needed a single assertion to die.
3. **my #6** — "Act on it before it exists; order it before it is in disorder" (`quoted`). A check that is absent cannot fail later. Two of A5's four clauses have no case on the channel the interface calls default.
4. **my #15** — seven parallel clauses with no order (`quoted`, a mindset and not a sequence). A5's line names four separate faults: inside a dump, no evidence, no limits, whole map unasked. Each needs its own check. A5 owns two cases, both `where leaf`, one JSON and one text.
5. **my #8** — "Knowing not-knowing: highest" (`quoted`; the witnesses differ on the second clause and my list records the sense as disputed). I take only the structure the words give: `A5-specific-answer` expects `limits: []`, so A5's own line calls a limits-free answer correct. That is the whole of my case that the line is under-tested.
6. **my #1** — "Lose and lose again, until one arrives at not-doing" (`quoted`). Every plant *adds* something: a map, every definition, a dump. A5's quiet failures are subtractions — a limit, a section, one line of text. Subtraction is what the round has not tested against.
7. **my #7** — "People in their undertakings often fail when they are close to finishing; careful at the end as at the beginning" (`quoted`). The round's last step is its report, and on the private opencode set A5 did not move for any of the five plants. Conditional, because I was not told whether that set has A5 cases at all.
8. **my #17** — "in its nothing lies the cart's use" (`quoted`; my list notes the words do not say to remove anything, that would be an application). **My reading**, built on those words: every check here is a positive assertion — `expectFocused` tests the keys that are there, `textIncludes` tests the text that is there — and none of them looks at what the answer left out. The use of an answer is in the part it does not print. This is the hinge of my verdict, and it is my reading, not my list's words.

## What I need to know

1. Does the private eight-case opencode set contain any A5 case, and any text-format case? If it has none, A5 on real code is unmeasured and should read NOT CHECKED there, not MET — which changes step 7 from "the checks were not enough" to "the checks were never run".
2. Is the default text channel inside A5's scope, or is A5 about the JSON Answer only? `spec.md:37–40` puts "One question per run (A5)" on printed output generally, so I read it as in scope; if the round's owner says agents only ever read `--json`, my change (1) drops to last and the verdict is STRENGTHEN with two changes.
3. Who owns `code_map/eval/`? If the text check lands in `matcher.ts` it is worth more; if it must land in `code_map/test/a5/` it is worth less, because the builder reads that file. That is not a reason to skip it, but it changes what the evidence proves.
4. A5 carries a standing NOT CHECKED part (`requirements.ts:36`, the agent's unasked map, P6). If closing on the tool part alone is already the practice, my #2 says stop after change (1) and (2).

## Costs and risks

- Each change costs, and the cost of change (1) falls on held-out cases: a new text expectation must survive the generator's rewriting of witnesses and cases (`COVERAGE.md:5`, `:108`), or held-out text cases fail for the wrong reason and the report will read as a tool regression. **my #7.**
- Change (3) can break the interface as written: `spec.md:41–42` requires `where`, `callers`, `callees`, `chain` and `tests` to return candidates in `matches` with `ambiguous: true` for a duplicated name. Narrow the section list without exempting that branch and you have taken a required behaviour away. **my #4**, and **my #3** — filling the vessel to the brim is not as good as stopping.
- Every check here sits in a file the builder can read. A builder who knows the text check can pass it without making the text answer focused; the evidence bought is smaller than it looks. **my #2**, **my #11**.
- Three quiet plants cost one more round of check time and, on present evidence, will return a weaker result than five did — which is precisely why they are worth the round. **my #1.**

## How we would know I was right

- Run the three quiet plants against attempt 1 unchanged, on the frozen tests, `tsgo`, the bundled cases, the held-out copy and the private set. If all three pass everything, the plants were heavy-handed and CLOSE was premature. If any one is caught, I am wrong and CLOSE stands.
- The cheap observable: for each plant, whether A5 itself appears in the report's A5 row. Today that is 1 of 5. If the quiet plants do not move it, the line reads 0 of 8 on A5's own account and every catch came from another requirement's line.
- After strengthening, each of the two new A5 cases must be NOT MET on a copy that violates its clause and MET on attempt 1. A new check that is MET on the violating copy is decoration, and should be counted as no check at all.
