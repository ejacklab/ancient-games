# Four experts and Dave — EJ's 80% coverage process

Question: `../expert-question-coverage.md`. Answers: `answers/`. Labels: *quoted* (from an answer), *my reading*, *not measured*.

| | Linus | 范蠡 | 孫子 | 老子 | Dave (control) |
|---|---|---|---|---|---|
| Answer (one line) | Holds for finding and ranking tests; count distinct reviewed behaviours; rarity alone does not justify skipping | Count over fixed acceptance criteria; basics 100%; an independent reviewer marks basic/rare | Fix the units from the requirement before generating; AI cases are evidence, units are the denominator | Count over cases worded from the requirement; one sentence names what is not tested | Count over behaviour classes; generate twice to test the drift; settle who marks by a blind trial |
| Main items used | #4 #5 #9 #10 #13 | #3 #7 #14 #16 #17 #18 | #1 #8 #11 #13 #16 #20 | #1 #2 #4 #7 #14 #16 #19 | #1 #4 #5 #6 #7 #8 |

## Where they agree (all five)

- **What holds:** reusing old use cases first, 80% as a target and not a gate, and leaving rare cases untested on purpose.
- **What breaks: 80% of an AI-generated list measures the generator.** The same requirement gives 15 or 60 cases; 12 tested is 80% of one and 20% of the other (Dave, 孫子, 范蠡). Padding: *quoted* Linus, "Adding ninety passing variations of those same eight behaviors gives 98%, while the same two behaviors remain untested."
- **The fix: the denominator comes from the requirement, not from the AI.** The AI's cases become evidence attached to fixed units. The unit differs by name — distinct behaviours (Linus), acceptance criteria (范蠡), units fixed before generating (孫子), cases worded from the requirement (老子), behaviour classes (Dave) — the same idea: one test per behaviour, variants do not add to the count.
- **The AI's list has blind spots.** 100% of the list is not 100% of the requirement. *Quoted* 老子: a list of twelve success cases passes 12/12 "and the one case that can break the requirement was never in the denominator".
- **An old use case counts only if it can still fail on the new requirement** — shown on a planted violation (Linus, 孫子, 老子, Dave; 范蠡 keeps reuse without this condition). *Quoted* 孫子: an old green case counted while the changed behaviour is untouched "is 費留".
- **The test to settle it:** generate the list twice for one requirement with different prompts and compare. Each predicts the count over raw cases moves and the count over requirement units does not. Two generations are an engine call — EJ's go-ahead.

## Where they disagree (side by side, not averaged)

| Point | Positions |
|---|---|
| **Who marks basic or rare** | Linus: the writer proposes with reasons; a reviewer challenges the **whole** list, because "Reviewing only the rare list cannot catch a missing case" · 范蠡: an independent reviewer marks — the writer "will naturally label difficult cases 'rare'" · 孫子: the writer marks against a **written, mechanical** criterion ("basic if removing the behaviour turns a test red"); the reviewer can fail the marks; EJ owns the criterion and the rare list · 老子: no per-case mark — a case worded from the requirement is basic by construction; the writer may exclude only what the requirement does not name, in one sentence · Dave: don't argue it, run a blind trial (writer vs independent marker); the disagreements go to EJ |
| **What makes a case skippable** | Linus: consequence and whether the damage can be undone, not frequency — "a rare interruption permanently corrupts saved work" · 老子: what it costs if it fires against what covering it costs · 孫子: a safety bound is never skippable, and EJ marks that set · 范蠡, Dave: rarity, with the marks checked |
| **What the 80% sits on** | 范蠡: basic criteria at **100%**; the 80% applies to permutations across them · the others: 80% over the units, with every uncovered unit rare (the main agent's clause, supported by 孫子 and 老子; Dave: the clause only moves the gaming into the label unless someone other than the writer sets it) |

*My reading:* 老子 and 范蠡 each change what the 80% means — 老子 says so: "over my denominator it means something different from what EJ pictured". That is EJ's call.

## What each added that the others did not

- **Linus** — deferred and failing cases stay in the denominator and are shown apart; a duplicate description must not move the number (a check that can fail); the eight requirement checks on R11.1: who decides, unit and weak words (basic, rare) still fail.
- **范蠡** — two worked cases: an email validator (15 vs 60 cases) and a balance transfer where 18 of 22 UI variants pass while the race condition goes untested.
- **孫子** — grow the list by probing (reckon, stir, make it take form, test it), not only by AI imagination; ask what a "possibility" is a possibility *of* — input value, input class, behaviour, or user journey.
- **老子** — the basic/rare condition has to hold when the list is written, not be inspected at the end; the coverage number must not be read as health; if the exclusions outnumber the covered cases, the cut failed.
- **Dave** — capture–recapture: two runs finding n1 and n2 classes with m in common estimate about n1·n2/m in total — a lower bound only, since two LLMs share blind spots; a record of escaped bugs would let "rare" be checked against history. He also asks whether "very basic things" means *must test* or *too trivial to test*; the brief assumed the first.

## What they need to know (merged, for EJ)

1. **Count the 80% over units from the requirement** (behaviours / acceptance criteria), with the AI's cases as evidence — yes? All five say so.
2. **Skippable by frequency, or by consequence?** Linus and 老子 say consequence; 孫子 adds a safety case is never skipped.
3. **Who marks** — the writer against a written criterion with a reviewer who can fail it (孫子), an independent marker (范蠡), no marks at all (老子), or a blind trial first (Dave)?
4. **Old use cases count only after failing on a planted violation of the new requirement** — yes?
5. **Run the two-generation trial** on one past requirement? It is a small paid call.
6. Is there a record of escaped bugs per requirement? (Dave, 老子 — it would let "rare" be checked.)

## Check

- `four_experts.py check`: 9 failures, all 老子. Each is the list's own Guodian text written in traditional characters or without the list's editorial brackets: the list has 为之者败之，执之者远之 / 执之者○（失）之, 人之败也，亘（恒）于其○（且）成也败之, 圣人之才（在）民前也, 以深爲根 / 以約爲紀 (`seats/lao-tzu-list.md` lines 56, 80, 96). Script changes, not inventions — read by the main agent, not by the check. `--sabotage`: 2 failures, as required.
- Engines (`status.json`): linus codex 74 s · fan-li agy 86 s, no fallback · sun-tzu dsh 80 s · lao-tzu opencode 110 s · Dave a Claude subagent.
- 老子's answer again begins with a stray line ("I'll read the brief first.").
- All five read the same brief, written by the main agent, which named the 15-vs-60 weak spot. Their agreement on it is not independent evidence for it.
