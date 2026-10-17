I'll read the brief first.
# 老子 (Laozi) — A2 and A5 wording: nine proposals, two requirement texts

## Answer

Accept six of the nine as written or nearly so (1, 2, 6, 7, 8, and3 with its name clause cut), merge 5 and 9 into one content-boundary clause, and accept 4 **only if the owner agrees that depth means shortest call distance** — without that answer the wording, not the tool, is what is wrong. Net: four sentences added to A2's body, three to A5's, both Fails-if lines split by who acts, no invented number (the six stays), and no proposed use case (none is needed to decide any of this).

| # | Decision | Rests on | Reason |
|---|---|---|---|
| 1 | **Accept** (label the halves *tool* / *agent, checked in P6*) | use case 1; A2's line as split by `eval/requirements.ts:34` | The tool's obligation and the agent's are two duties; the report already marks the agent's half NOT CHECKED, so the letter should stop hiding it inside the tool's line. |
| 2 | **Accept with this wording** — define *known* once in the body, keep the owner's word in both lines | Vision R2 ("the type checker establishes"); my #8 | "Known" has no owner, so no check can be independent of whoever declares it known. One definition, used twice, is cheaper than rewording two lines. |
| 3 | **Accept with this wording**, and **cut the name clause** — say who holds a call, not what a bodyless body is called | Vision A2's "Each link gives its kind and location"; use case 1; spec.md:92 with `eval/source.ts:41-46` | The interface and the checker already make the *nearest* body the holder; the letter must say it. The name "Effect.gen callback" is built from the call text (`src/nodes.ts:125`) and the held-out renamer only renames names matching `^[\w$.]+$` (`holdout.ts:90,143`), so fixing it in the requirement freezes a string no check can relocate. |
| 4 | **Accept with this wording** — drop "The place is level 0; each call link adds one level", keep "whatever order the tool walks" and "shorter route" | use case 4; the verified fault (COVERAGE.md:249-254) | Level 0 is already the interface's (`spec.md:32,104`); the fault is that traversal order loses a link inside the depth, so state shortest distance and order-independence, and nothing else. |
| 5 | **Accept, merged with 9** | use case 4; the confirmed default-text fault | "Only inside a dump" let a right answer followed by a dump pass. The boundary belongs in the body, so the Fails-if line stays short. |
| 6 | **Accept with this wording** | use case 4 ("say plainly when reading is cheaper") and L1 | `find` drops every match below the best score with no limit at all (`src/commands.ts:139`); the letter must say a whole answer, and a stop that says so. |
| 7 | **Accept** | use case 4; my #2 | The tool never sees the user's request; only the agent half is P6's. |
| 8 | **Accept, merged into the body's form clause** | use case 4; `spec.md:37-38` | The default text is the form the agent reads, and the confirmed fault was in the text, not the JSON. |
| 9 | **Accept with this wording** — "a section or content the command does not answer" | use case 4; my #17, #19 | "Unrelated" needs an owner the checker can apply; the interface already has one — the sections a command answers (`contract.ts:83-89`). |

**Merged:** 5 + 9 into one body sentence and one Fails-if clause; 6 + 8 into one body sentence ("in the form the tool answers in"). 1 and 7 use the same split, so A2 line 2 and A5's second clause are worded alike.

### A2 — final text

```
A2 The call chain through one place. Given code or a description, the tool locates the place and returns its
caller and callee chains, counted in levels from the place. The user sets the depth each way; when the user does
not, it is six. Known means the type checker establishes the place or the link, or the source makes a call the
tool cannot resolve. A level is the shortest call distance from the place, so every known link within the
selected depth is shown whatever order the tool walks. When more than one place matches, the tool flags the match
as ambiguous; the agent picks the place that fits the question best, builds its chain, and names every other
candidate it did not build. Each link names the body that holds the call, and gives its kind and its location. A
body written straight into a call is a place of its own or a stated limit; it is never shown as a call by the
function that surrounds it. A function reached twice is shown once, with a reference back, and links reachable
through a shorter route are still shown.
Fails if: any of these happens:
- a known place is not found;
- by the tool — an ambiguous match is not flagged, or a matching candidate is not listed with its location; by
  the agent, checked in P6 — an ambiguous match is treated as certain, or a candidate the agent did not build is
  not named;
- a known link within the depth is missing, or a shown link contradicts the code;
- a link lacks its kind or location;
- a function reached twice is shown twice.
```

### A5 — final text

```
A5 One question, one answer. A specific question gets that whole answer, with its evidence and limits, in the
form the tool answers in — JSON or the default text the agent reads. Where the answer stops short, a cap, a sample
or a first page of matches, it carries the limit that says so; a limit the interface requires for that command is
part of the answer. An answer holds the requested result, its evidence, its applicable limits and the candidates
needed to resolve an ambiguity, and no unrelated definitions, links, flows or tables, in any section of it. A
whole map is produced only when the user asks for a module map.
Fails if: any of these happens:
- by the tool — an answer comes inside a dump, or carries a section or content the command does not answer, or
  comes without its evidence or its limits; or a command other than a module map returns map content;
- by the agent, checked in P6 — the agent runs `map` when the user did not ask for a module map.
```

No wording conflicts with a use case. The only tension is between use case 4 ("fewer tokens than reading it") and proposal 4, and it binds on the **owner's depth dial**, not on the wording: under shortest-distance semantics the set of links is still bounded by the depth the user set, so nothing new is paid for.

## How I decided

1. **My #1** — *Take away, and take away again* (損之又損，以至於無為。無為而無不為。, `quoted`). I counted each proposal against what the letter or the interface already says. Nine proposals, four sentences added to A2 and three to A5. Two sentences came out: proposal 4's "The place is level 0; each call link adds one level", which `spec.md:32,104` already fixes, and proposal 1's added "lists every candidate with its location" in the body, which `spec.md:107-108` and the Fails-if line already carry.
2. **My #17** — *The use is in what is not there* (故有之以為利，無之以為用。, `quoted`). A check buys absences. Proposals 2, 5, 6 and 9 are all one absence said four ways — the answer silently missing something. That is why5 and 9 merge: one clause, tied to a rule the checker already runs.
3. **My #8** — *Know that you do not know* (知不知上，不知知病。夫唯病病，是以不病。, `quoted`). Two uses. It is 孫子's reason for proposal 2 in my own words: "known" is a foreknowledge with no source, so the type checker names it. And it is why I refuse proposal 3's name clause: I do not know that "Effect.gen callback" is the name the owner wants, and a name no check can relocate is a name the requirement should not freeze (my reading, from `src/nodes.ts:125` and `holdout.ts:90`).
4. **My #19** — *restraint as the rule* (以深為根，以約為紀，曰：「堅則毀矣，銳則挫矣。」, `attributed`). Every sharp addition here is blunted by the first thing it did not foresee. Proposal 4's level sentence duplicates the spec. Proposal 9's "unrelated … whether they appear in another section or inside the requested payload" is precise but owned by nobody; I tie it to `contract.ts:83-89`'s per-command sections instead, so a reader can settle a case from the interface.
5. **My #2** — *Know what is enough; know to stop* (知足不辱，知止不殆，可以長久。禍莫大於不知足。, `quoted`), with **my #18** — *when your time comes, ride out* (吾所以告子，若是而已。, `attributed`). The least before A5 closes and A2 starts: two Fails-if clauses changed, no case added, no new check. The least before the tool is rebuilt: one sentence about level. Everything else waits.
6. **My #6** — *Act while it is small and easy; treat as difficult* (為之於未有，治之於未亂。, `quoted`). A2 is NOT MET on the real CLI today (COVERAGE.md:249-254), so the level wording goes in while the failure is live and the builder has not started; a wording written after the repair explains a fix that already happened. **My #7** — *Be as careful at the end as at the beginning* (民之從事，常於幾成而敗之。慎終如始，則無敗事。, `quoted`) — the same sentence says the sentence matters most at the close, so the change lands before the round, not after it.
7. **My #4** — *Acting on it ruins it; gripping it loses it* (為者敗之，執者失之。…是以聖人去甚，去奢，去泰。, `quoted`). The checks must not grip the whole requirement. One line now names two obligations, one of which no tool check can decide; splitting by actor (1, 7) is 去甚 — the tool's line keeps only what the tool owes, and the price is named under Costs.
8. **My #16** — *eight parallel statements, not a ladder* (知人者智，自知者明。…死而不亡者壽。, `quoted`). I do not rank the nine proposals, and I do not read A5's four clauses as an order of work. They stay parallel in one line.
9. **My #12** — *What is to be shrunk must first be stretched* (將欲歙之，必固張之；…, `quoted`). Before cutting anything I asked what it was already doing: 5 and 9 both stretch 6's clause; 1 and 7 stretch one another; 3 is already the interface's rule.
10. **My reading**, from `spec.md:92`, `eval/source.ts:41-46`, `src/links.ts:46` and `src/commands.ts:283-289`: two different rules for "which body holds a call" live in the tool today. A link's `from` is the nearest function-like (`enclosingNode`, `links.ts:46`), and the checker demands the same (`source.ts:41-46`), but the traversal filter `belongsTo` walks past a bodyless body and gives its calls to the surrounding named function (`nodes.ts:267-271`, `commands.ts:188,228,304,308`). Proposal 3 names that disagreement; the letter should settle it on the interface's side. This is a source reading — I did not run the tool.

## What I need to know

1. **Does depth mean shortest call distance?** If yes, proposal 4 as worded stands and A2 stays NOT MET until the traversal revisits a function reached by a longer route first (`commands.ts:312-332,334-360` keep one `expanded` map per direction and never revisit). If no — if depth means "the chain the tool walked" — then `A2-shorter-route-down` and `-up` are wrong checks, the real CLI is right, and the wording should say so instead; then the fault is in the cases, not the tool. I decide conditionally: *if shortest distance, accept 4 as worded; if not, reject 4 and change the four route-depth cases.*
2. **Is a body written straight into a call a step in the chain, so its own calls sit one level below it?** My reading says yes, because the interface makes it a place (`spec.md:92`) and the letter now says it is "a place of its own". If the owner wants it to be a place only when the chain starts there, A2's level arithmetic needs its own sentence and the expected levels in `A2-const-chain` and the route fixtures may change.
3. **Is `belongsTo`'s attribution intended, or is the spec's "nearest function, method or arrow"?** I have worded it the spec's way. If the owner meant the tool's way, proposal 3 is reversed *and* `source.ts:41-46` must change, because that check would then reject every correct link inside a bodyless body.
4. **Is a ranked `find` that drops lower-scoring matches silently a "stop that says so"?** My reading is yes (`commands.ts:139`). If the owner says a ranked search is not a stop, then "a cap, a sample or a first page of matches" becomes "a cap", and `find` stays silent by design.

## Costs and risks

- **Splitting by actor changes the strings the report matches.** `eval/requirements.ts:11-24` holds the exact Fails-if lines and every case names its line; new wording means new strings, and 70 cases need their `line` fields re-mapped before any round can be read. **my #7** (act while it is easy), **my #6**.
- **The *known* definition narrows A2's missing-link clause.** A call the type checker cannot establish and that the tool does not resolve is no longer "known", so its absence no longer fails that line; L1 has to carry it. **my #17**, **my #2**.
- **A2 will read NOT MET on the real CLI until the traversal changes.** That is the intent, and it costs an attempt 2 under the stated process. **my #7**.
- **A5's body grows from two sentences to four.** Every requirement is read by the builder, and a longer requirement invites reading only the Fails-if line; the compensation is that the Fails-if line is now two short labelled halves. **my #1**, **my #19**.
- **"The command does not answer" couples the wording to `contract.ts:83-89`.** If the interface later lets a command answer a section it does not today, the wording moves with it. **my #19** (銳則挫矣).
- **Not fixing the name of a bodyless body leaves each build free to invent one,** so no check can assert it by name — only by location and kind. **my #8**, **my #3**.
- **A 70-case re-run and a relabelled report must land before A2's round starts,** or the round's verdict is attributed to a line no case names. **my #6**.

## How we would know I was right

- **Negative control first:** run the bundled cases against the current tool with the new strings. The result must still be exactly the two route-depth cases NOT MET (COVERAGE.md:249-254) and nothing else. If a line string silently stops charging, the report shows a Fails-if line that no case names.
- **Plant the confirmed fault:** append one unrelated definition to a right answer in the default text only (`render.ts`). The new A5 line must go NOT MET; today `A5-default-text` accepts it (Linus's probe: 0 mismatches).
- **Plant the attribution fault:** a link whose `from` is the surrounding named function and whose site is inside a body written straight into a call. The new letter says NOT MET, and `source.ts:41-46` already rejects it. If a correct tool fails that check, the letter and the check disagree and one of them is wrong.
- **Reverse the order and re-run:** with the root's call order reversed in `route-depth/down.ts`, both orders must keep `routeTail` at `chain.down[].children[].link.to`. Today the verdict flips with the source order — that flip is the signature of the fault proposal 4 names.
- **Count:** A2 gains four sentences and A5 three. If a fifth is proposed in round 2, **my #1** was applied wrongly.
