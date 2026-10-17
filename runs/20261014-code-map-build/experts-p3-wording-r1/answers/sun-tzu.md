# 孫子 (Sun Tzu) — the wording of A2 and A5

## Answer

Decide the ground first: A2 is five Fails-if lines, A5 is one compound line; I matched each proposal to the clause it changes before accepting any (my #1). **Accept all nine in substance, but keep each requirement whole — reject the tool/agent split in 1 and 7, and merge 5, 6, 8 and 9 into A5's one line.** The one decision the owner must make outside the wording is that depth means shortest call distance.

| # | Decision | Rests on (use case / Vision line) | Reason |
|---|---|---|---|
| 1 | accept with this wording — **not split** | U1, U4; A2's own words ("the agent picks … and names every other candidate") | The tool must list every matching candidate with its location, or the agent cannot name them; the requirement stays one line, so the tool half and the agent half are not separated. |
| 2 | accept with this wording | U4; R2's basis ("the type checker establishes") | "Known" has no owner. Name it: a link is one the type checker establishes; a place is one the given code or description points to. |
| 3 | accept | U1, U4 (opencode's typed injected services; E1 found 17 of 18 calls in anonymous bodies); A2's "a shown link contradicts the code" | A link must name the body that holds the call; the surrounding function must not be credited with a call made inside a body written straight into a call. |
| 4 | accept with wording, conditional resolved **yes** | U1, U2; A2's "a known link within the depth is missing" | Depth is shortest call distance, so traversal order must not drop a link reachable through a shorter path. The fault is confirmed, not hypothetical. |
| 5 | accept; merged into A5's one line | U4; A5's "not a whole-map dump" | "Only inside a dump" lets a correct answer plus a dump pass; "with unasked sections" closes it. Merged with 6, 8, 9. |
| 6 | accept with wording; merged | U4; A5's "with its evidence and limits" | Defines the whole answer, requires a limit where the answer stops short, and makes an interface-required limit part of the answer. Merged with 5, 8, 9. |
| 7 | accept with this wording — **not split** | U1; A5's "A whole map is produced only when the user asks for a module map" | "No command other than a module map returns map content" is the checkable tool condition; the agent's "only when the user asked" stays in the same requirement. |
| 8 | accept with wording; merged | U4; the spec's default text output | Text is the default and the agent reads it; if A5 does not cover it, the agent's real output path is unguarded. Merged with 9. |
| 9 | accept with wording; merged | U1, U4; A5's "not a whole-map dump" | Gives "dump" a boundary — unrelated map content, in another section or inside the payload — and states it applies to JSON and text. Merged with 5, 6, 8. |

**Merged:** 5, 6, 8 and 9 all land on A5's one Fails-if line; I fused them into one body and one line rather than four clauses (my #14, 老子's merge). 1 and 7 are accepted as clarifications but not as splits. 2 and 4 share the phrase "the type checker establishes", so A2 has one wording for a link, not two.

**On the unheld body's name:** the requirement should fix **ownership**, not the string. A body written straight into a call is a place of its own or a stated limit; the interface already forces a `name`, so the requirement should not freeze "Effect.gen callback". A fixed string would be a constant form for a shape that varies (my #10, quoted: 「故兵無成勢，無恒形」 — "So an army has no fixed 勢 and no constant form").

**Final A2 — The call chain through one place.** Given code or a description, the tool locates the place and returns its caller and callee chains, counted in levels from the place; the place is level 0, and each call link adds one level. The user sets the depth each way; when the user does not, it is six. Every link the type checker establishes that is reachable within the selected depth is included, regardless of traversal order, and reaching a function again does not lose a link reachable through a shorter path. When more than one place matches, the tool flags the match as ambiguous and lists every matching candidate with its location; the agent picks the place that fits the question best, builds its chain, and names every other candidate it did not build. Each link names the body that holds the call and gives its kind and location. A body written straight into a call is a place of its own or a stated limit; it is never shown as a call by the function that surrounds it. A function reached twice is shown once, with a reference back.
**Fails if:** any of these happens:
- a place the given code or description points to is not found;
- an ambiguous match is not flagged or a matching candidate is not listed with its location, or the agent treats an ambiguous match as certain or does not name a candidate it did not build;
- a link the type checker establishes within the depth is missing, or a shown link contradicts the code, including a link credited to a function that does not hold the call;
- a link lacks its kind or location;
- a function reached twice is shown twice.

**Final A5 — One question, one answer.** A specific question gets that whole answer, with its evidence and its limits, in the form the command answers in — the default text or JSON — and not a whole-map dump. Where the answer stops short — a cap, a sample, a first page — it carries the limit that says so. A limit the interface requires for that command is part of the answer. The answer contains the requested result, its supporting evidence, its applicable limits and the matching places needed to resolve an ambiguity; it excludes unrelated definitions, links, flows and tables, whether they appear in another section or inside the requested payload, in JSON and in the default text. A whole map is produced only when the user asks for a module map; no command other than a module map returns map content.
**Fails if:** an answer comes inside a dump or with unasked sections; lacks its evidence, its limits, or the limit that says where it stops short; carries unrelated definitions, links, flows or tables, in another section or inside the requested payload; or a whole map is produced unasked, or a command other than a module map returns map content.

## How I decided

1. **My #1** — I reckoned the ground before committing: laid out A2's five Fails-if lines and A5's one compound line, and matched each proposal to the clause it changes. 「多算勝，少算不勝，而況於無算乎？」 — "More wins, fewer does not, how much less none at all?" (my #1, `quoted`).
2. **My #17** — I learned the tool by probing the allowed sources, not by assuming: `links.ts` sets a link's `from` to `enclosingNode` = the nearest function, and `commands.ts` `chainDown`/`chainUp` stop expanding a function already in `expanded`. 「策之而知得失之計」 — "reckon him (策) to know the gains and losses of his plans" (my #17, `quoted`). This grounds proposals 3 and 4.
3. **My #11** — "known" has no owner, so a check and the tool would share one fallible reading. 「必取於人，知敵之情者也」 — "it must be got from people who know the enemy's situation" (my #11, `quoted`); the list also says this foreknowledge "must be got from people", and paying for it is part of the rule. So link = "the type checker establishes"; place = "the given code or description points to". Proposal 2.
4. **My #3, my #13** — a requirement is not split into pieces. 「全國為上，破國次之」 — "a whole state is best, a broken one next" (my #3, `quoted`); 「君命有所不受」 — "ruler's commands one does not accept" (my #13, `quoted`). So I reject the tool/agent *split* in proposals 1 and 7 but keep every duty inside the one requirement. The evaluator/P6 division is a checking matter, not a wording matter.
5. **My #16** — orders must be clear; a vague word is the writer's fault. 「約束不明，申令不熟，將之罪也」 — "If the rules are not clear and the orders not made familiar, it is the general's fault" (my #16, `quoted`). This is why "only inside a dump" and an unnamed "form" had to be replaced.
6. **My #7, my #2** — a false pass is the deceit to catch; do not rely on the agent's restraint. 「兵者，詭道也」 (my #7, `quoted`) and 「無恃其不來，恃吾有以待之」 — "Do not rely on their not coming; rely on having the means to meet them" (my #2, `quoted`). This grounds A5's dump/text gaps (5, 8, 9) and A2's wrong-owner link (3).
7. **My #4, my #6** — know the other side and yourself; mix harm into benefit. 「知彼知己，百戰不殆」 (my #4, `quoted`) and 「智者之慮，必雜於利害」 (my #6, `quoted`). Each accepted proposal's price is named under Costs and risks.
8. **My #14, my #15** — do not mass on the same spot; the check's own faults are the handle against it. 「兵非貴益多也」 — "in war more is not what is valued" (my #14, `quoted`); 「凡此五者，將之過也」 (my #15, `quoted`). This is why 5/6/8/9 became one A5 line, not four clauses.
9. **My #19, my #5** — name the ground, then act as prescribed; move only on advantage. 「散地則無戰」 (my #19, `quoted`) and 「合於利而動，不合於利而止」 (my #5, `quoted`). A5 keeps the owner's "One question, one answer" and its map clause; only what the confirmed faults required was changed.

## What I need to know

- Does depth mean **shortest call distance**? I answered yes (the place is level 0, each call link adds one level). If the owner means "the first path the walk finds", proposal 4 is a behaviour change, not a clarification, and the wording should say so.
- May A2 and A5 keep the agent's duty inside the requirement (as the Vision's A2 does), or does the owner want it moved to the P6 contract? I kept it whole (my reading of "not split into pieces"); if moved, A2's line 2 loses its second half.
- Is a body written straight into a call always a **place of its own**, or may the tool state a limit instead? Proposal 3 permits both; the tool today names it ("Effect.gen callback").
- For `find "<code or words>"`, is a matched place one "the type checker establishes"? If not, my place wording ("the given code or description points to") is the right owner.
- Can "unrelated" be checked without a boundary from the owner? I kept Linus's word; otherwise it stays a wording that only a human can apply.

## Costs and risks

- **Proposal 3 (my #2, my #16):** the unheld body becomes its own place, but `belongsTo` in `nodes.ts` presently folds its calls into the surrounding function for `callees`. The tool must change, and existing `callees` answers for surrounding functions will change.
- **Proposal 4 (my #11, `quoted`: "pay for it"):** depth as shortest distance costs a rework of chain traversal (remaining depth per function) and can widen a chain. Without it, A2's missing-link line stays NOT MET — `A2-shorter-route-down` and `-up` already fail on the real CLI.
- **"The type checker establishes" (my #11):** the check is only as independent as the checker both sides read; if the tool is the checker's only interpreter, the check and the tool still share one reading.
- **A5 "unrelated" (my #16):** no measurable boundary. A strict reading can punish a legitimate answer (the query header, a `seen` limit's `ref`); a loose reading lets a dump pass.
- **A5 form + content boundary (my #4):** one missing limit or extra table may now fail A5 and L1/A1 at once, so a report can count one fault three times.
- **Splitting rejected (my #3):** the agent's half stays inside A2 and A5, so the evaluator still reports part of each NOT CHECKED and cannot show the tool's part alone.
- **Merging 5/6/8/9 (my #14):** a denser single A5 line; a reader must hold the whole line, and one over-broad clause can fail a correct tool.

## How we would know I was right

- **A test:** all four `A2-shorter-route-*` cases MET on the real CLI, with the depth-three tail link present through the shorter route whichever sibling order the source uses. If a reversed order is needed to pass, proposal 4 was not applied.
- **A test:** `callers` on an unheld generator body returns `from` at the body's own location, never the surrounding function's; and `callees` on the surrounding function no longer lists calls made inside the unheld body.
- **A test:** a default-text answer carrying the right answer plus an unrelated definition, and a JSON answer carrying an unrelated top-level section, each fail A5; a right answer plus its interface-required limit passes (proposals 5, 6, 8, 9).
- **An observable:** every A5 Fails-if clause in the final wording has a case that fires it (`A5-exact-callees`, `A5-default-text`, `A5-exact-not-found`, `A5-exact-depth-stop`), and every clause those cases charge appears in the wording — no clause left unchecked, no case left unnamed (my #1: the count is only usable when the counts are laid out).
