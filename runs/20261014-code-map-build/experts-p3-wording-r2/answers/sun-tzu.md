# 孫子 (Sun Tzu) — final wording of A2 and A5

## Answer

Accept seven of the nine with the wording below, reject 6, and merge 5, 8 and 9 into A5's one content boundary. Every change turns on two tests: "known" must be owned by evidence other than the tool, and every Fails-if line must be chargeable to the party that acts (the tool, or the agent in P6).

| # | Final decision | Changed from round 1? | One-line reason |
|---|---|---|---|
| 1 | accept with this wording — actor-labelled Fails-if lines, one requirement | yes — from "one line, not split" | A single line mixing tool and agent cannot be charged to either (范蠡 step 2); labelling the actor does not split A2. |
| 2 | accept with this wording: "A known place or link is one that repository source or type information establishes." | yes — from "the type checker establishes" | The type checker is the tool's own method, so it cannot also be the owner of "known" (范蠡 step 3); evidence, not method, is the boundary. |
| 3 | accept with this wording, **without** "or a stated limit" | yes — cut the limit | A limit in place of the body drops most opencode links — E1 found 17 of 18 calls in anonymous bodies (spec) — and contradicts the spec's "nearest function, method or arrow". |
| 4 | accept with this wording — shortest route; drop "regardless of traversal order" | yes — dropped the method clause | The confirmed fault is depth read as first route; source order must not change the links (use case 2). |
| 5 | accept, merged with 8 and 9 | yes — wording | "Only inside a dump" let a right answer plus a dump pass; the boundary is content the question did not ask for. |
| 6 | **reject** | yes — from accept | L1 already owns "every answer or branch that stops early names why"; a second copy gives two places to disagree (范蠡 step 8). |
| 7 | accept with this wording — actor-labelled; "whole module map", not "map content" | yes — wording | A `callees` answer *is* links, so "map content" is unclear; "whole module map" names the real boundary (Linus, 范蠡). |
| 8 | accept, merged into A5's form clause | no | The confirmed wrong pass was in the default text the agent reads (use case 4). |
| 9 | accept with this wording — positive inclusions + "no content the question did not ask for", in another section or inside the payload | yes — wording | The enumerated list goes stale and "unrelated" has no owner (范蠡 step 7); 老子's named owner `contract.ts` is not in the tool. |

**A2 The call chain through one place.** Given code or a description, the tool locates the place and returns its caller and callee chains, counted in levels from the place. The place is level 0 and each call link adds one level; a link is within the depth when its shortest route from the place is. The user sets the depth each way; when the user does not, it is six. A known place or link is one that repository source or type information establishes. When more than one place matches, the tool flags the match as ambiguous and lists every candidate with its location; the agent picks the place that fits the question best, builds its chain, and names every other candidate it did not build. Each link names the body that holds the call and gives its kind and location. A body written straight into a call is a place of its own; its calls are never shown as calls by the function that surrounds it. A function reached twice is shown once, with a reference back; the reference never hides a link that is within the depth through another route.
**Fails if:** any of these happens:
- a known place is not found;
- by the tool — an ambiguous match is not flagged, or a matching candidate is not listed with its location;
- by the agent, checked in P6 — an ambiguous match is treated as certain, or a candidate the agent did not build is not named;
- a known link within the depth is missing, or a shown link contradicts the code, including a link credited to a function that does not hold the call;
- a link lacks its kind or location;
- a function reached twice is shown twice.

**A5 One question, one answer.** A specific question gets that answer, with its evidence and its limits, not a whole-map dump, in the form the tool answers in — JSON or the default text the agent reads. The answer contains the requested result, its supporting evidence, its applicable limits and the candidates needed to resolve an ambiguity; it carries no content the question did not ask for, in another section or inside the requested payload. A whole module map is produced only when the user asks for a module map.
**Fails if:** any of these happens:
- by the tool — an answer comes inside a dump, or carries content the question did not ask for, in another section or inside the requested payload, or comes without its evidence or limits;
- by the tool — a command other than `map` returns a whole module map;
- by the agent, checked in P6 — the agent runs `map` when the user did not ask for a module map.

## How I decided

1. **My #1 — reckon the ground before committing.** 「多算勝，少算不勝，而況於無算乎？」 (my #1, `quoted`). I laid out the nine proposals, A2's lines and A5's line, read all four round-1 answers, and checked the COO's reading against them. It holds: all four accept 3, 4, 8 and 9-with-5 in substance; 2, 6 and the 1/7 split are the open points.

2. **My #11 — foreknowledge must come from outside the tool's own method.** 「必取於人，知敵之情者也」 (my #11, `quoted`). 范蠡 asked this of proposal 2 and is right: "It would make the tool's method the judge of the tool." That changed my round-1 wording from "the type checker establishes" to Linus's evidence boundary, "established from repository source or type information". It fits R1's "Built from source and type information" and leaves the independent key writer of L2 an evidence class, not the tool's algorithm.

3. **Where I hold against 范蠡:** rejecting 2 outright leaves "known" with no owner at all, and A2's missing-link line stays uncheckable. **Where I hold against 老子:** his A2 says "Known means the type checker establishes the place or the link, or the source makes a call the tool cannot resolve." The two halves have two different owners, so the word still has no single owner — the fault 2 was raised to fix (my #16, 「約束不明，申令不熟，將之罪也」, `quoted`).

4. **My #3 — keep the requirement whole; strike the root.** 「全國為上，破國次之」 (my #3, `quoted`). A2 stays one requirement and A5 stays one requirement. On 1 and 7 I changed from "not split" to actor-labelled Fails-if lines because 范蠡's step 2 is right: "A single Fails-if line that mixes the two cannot be charged to either." Naming the actor is not splitting the requirement; the spec already marks the agent half NOT CHECKED → P6.

5. **My #16 — orders clear first.** 「約束不明，申令不熟，將之罪也」 (my #16, `quoted`). This decides 7's wording: 范蠡's "Map content is unclear, because a `callees` answer *is* links" holds, so the tool clause is "no command other than `map` returns a whole module map."

6. **My #5 — move only where the fault forces it.** 「合於利而動，不合於利而止」 (my #5, `quoted`). Proposal 3's "or a stated limit" is the case: 范蠡's "a limit would drop the link: E1 found 17 of 18 opencode calls in anonymous bodies (spec)" shows the escape would gut the rule. I cut it. **My #10** — 「故兵無成勢，無恒形」 (my #10, `quoted`) — keeps the name string ("Effect.gen callback") out of the requirement; the spec's rule-table row owns it.

7. **My #4 and my #17 — know the ground; probe and read the signs.** 「知彼知己，百戰不殆」 (my #4, `quoted`); 「策之而知得失之計」 (my #17, `quoted`). Proposal 4 is the one behaviour change with a confirmed fault, so it goes in now: level 0, one level per call link, a link within the depth when its shortest route is. I dropped "regardless of traversal order" on 范蠡's step 4 ("it describes the method, not the result") and kept the result: the reference back "never hides a link that is within the depth through another route" (use case 2: a reorder must not read as a logic change).

8. **My #7 — a false pass is the deceit to catch.** 「兵者，詭道也」 (my #7, `quoted`). Proposals 5, 8 and 9 exist because a right answer followed by an unrelated default-text dump passed. A5's form clause covers both outputs (8); the exclusion covers beside the answer and inside its section (9); "only" comes out of "an answer comes only inside a dump" (5). They merge into one body and one Fails-if line.

9. **My #14 — more is not what is valued.** 「兵非貴益多也」 (my #14, `quoted`). I reject Linus's enumerated list, "unrelated definitions, links, flows and tables": a fixed list goes stale when the map gains a kind, and 范蠡's "A fixed list of excluded kinds goes stale, and 'unrelated' is a weak word" stands. **My #17 again:** 老子 ties the boundary to "a section or content the command does not answer" at `contract.ts:83-89`; there is no `contract.ts` in `code_map/src/` (the `Answer` type is in `answer.ts`). The owner he names is not in the interface, so I will not rest the wording on it. The question is the owner.

10. **My #15 — the check's own faults are the handle.** 「凡此五者，將之過也」 (my #15, `quoted`). The A5 boundary can over-fire: a required limit and an ambiguity candidate are content the question did not literally ask for. The positive inclusions in the body — requested result, supporting evidence, applicable limits, ambiguity candidates — are the guard, and the `A5-exact-*` cases are what make the line checkable.

11. **My #6 and my #14 — mix harm into benefit; do not mass on one spot.** 「智者之慮，必雜於利害」 (my #6, `quoted`). Proposal 6's benefit is a named stop; its harm is a second owner for L1's duty. 范蠡's step 8 changed my round-1 accept to reject: proposal 6's stop sentence "is L1's 'Every answer or branch that stops early names why'. Writing it twice gives two places to disagree later." 老子's finding is real — "`find` drops every match below the best score with no limit at all (`src/commands.ts:139`)" — but the home of the gap is L1; I put the residual question to EJ under question 2.

12. **My #2 and my #19 — do not rest on restraint; name the ground, act as prescribed.** 「無恃其不來，恃吾有以待之」 (my #2, `quoted`); 「散地則無戰」 (my #19, `quoted`). A5 keeps the owner's "with its evidence and its limits" and leans on L1 for a stop, which is why questions 2 and 3 must be answered. I kept "counted in levels from the place", the default six (no invented number), "the agent picks the place that fits the question best", "a function reached twice is shown once, with a reference back", and A5's title. Only a confirmed fault or an unnamed actor changed a line.

## What I need to know

1. **Does depth mean the shortest route?** My reading, Linus's condition and 老子's condition all say yes; 范蠡 asks the owner. *If yes:* proposal 4 stands as worded and the four `A2-shorter-route-*` cases are right. *If no — the first route the walk finds:* reject 4 and change those four cases instead.
2. **Does a ranked `find` that drops lower-scoring matches count as "a branch that stops early" under L1?** *If yes:* rejecting 6 is safe — L1 catches it and the tool must add a limit. *If no:* A5 needs proposal 6 (or L1 needs a clause that a ranked list is not a stop), or the dropped matches are invisible to both.
3. **Does a known link the tool cannot follow, but marks with a `dynamic` limit at its site, count as "missing" under A2?** *If yes:* the missing-link line needs "with no limit at its site naming why". *If no:* the wording stands — the edge is shown with its kind, location and reason, so it is not missing.
4. **Should the name of a body with no holder be fixed in the requirement?** My answer: no; the spec's rule-table row owns the string. *If EJ wants it in the requirement,* the name must come from EJ or the spec; I will not invent one.
5. **Do A1's "a known item" and L2's answer keys take this same definition of "known"?** *If not,* the word carries two senses across the requirements and A1's check loses its basis.

## Costs and risks

- **Actor-labelled lines, 1 and 7 (my #16):** new Fails-if strings mean the `line` fields in the evaluator cases must be re-mapped before any report can be read; A2 and A5 stay partly NOT CHECKED until P6. That is the price of a line chargeable to one actor.
- **Defining "known", 2 (my #11):** the definition is only as independent as the evidence and the key writer's method. If the tool is the only reader of "repository source or type information", the check and the tool still share one reading — and A1 and L2 keep the loose sense unless they adopt it (question 5).
- **Cutting "or a stated limit", 3 (my #2):** `belongsTo` in `nodes.ts` presently folds an unheld body's calls into the surrounding function for `callees` (my reading of the code), so the tool must change and existing `callees` answers change. A body the tool truly cannot place is now left to L1 alone.
- **Depth as shortest route, 4 (my #11, my #8):** it needs remaining-depth traversal per function, not the present one-`expanded`-map walk; a chain can widen. Runtime and memory are **not measured**. Paying for foreknowledge is the point of my #11.
- **The question-owned A5 boundary, 5/8/9 (my #16):** "content the question did not ask for" is only as sharp as the question; a strict reading can punish a required limit or a candidate. The positive inclusions are the only guard, so the `A5-exact-*` cases carry the line.
- **Rejecting 6 (my #14, my #6):** the stop-limit duty now rests entirely on L1. If L1's check does not cover a ranked `find`, the gap stays open — the harm mixed into the benefit, and the reason question 2 matters.
- **Dropping the enumerated list, 9 (my #17):** with no fixed kinds, the boundary depends on the question's wording; a vague question gives a vague boundary, so the check needs the exact-shape cases rather than a word list.

## How we would know I was right

- `A2-shorter-route-down` and `-up` turn MET, their `-reversed` twins stay MET, and `chain` on `route-depth/down.ts` and `down-reversed.ts` gives the same set of links with `routeTail` present through the shorter route — same answer, any source order (use case 2).
- `callees` on a surrounding function no longer lists a call made inside an unheld `Effect.gen` body; the link's `from` is the body's own location (`A2-inline-generator-owner`); a key written by another agent finds no link credited to the surrounding function.
- A default-text answer carrying the right answer plus an unrelated dump fails A5 (`A5-default-text`), and a JSON answer with an unrelated top-level section fails too; a right answer plus its interface-required limit still passes.
- A `find` that drops lower-scoring matches without a limit fails L1; if EJ answers question 2 "no", that test belongs to a different line and the wording must move with it.
- Every final A2 and A5 Fails-if line is named by at least one case in `COVERAGE.md`, no line is charged to the wrong actor, and the two agent bullets show NOT CHECKED → P6 until the integration test runs.
