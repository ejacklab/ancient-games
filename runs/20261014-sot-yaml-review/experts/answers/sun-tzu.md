# 孫子 (Sun Tzu) — will an agent follow this YAML, and what layout serves it

## Answer

**No — not reliably as a gate, though it is a fine readable annex.** The draft keeps every word but breaks the **unit** of a requirement: the level sits in a clause map, the check sits in a group string, and the open choice sits with nobody, so a reader can meet a requirement and still not know what it must do, what fails it, or whom to ask. Keep the three categories, the group ids, the unchanged `text`, the `basis` codes and the four level definitions; change A–D as below, and conditionally — if only an LLM reads the file, B and D are the high-value changes; if a script will parse it, A and C come first.

**Keep.** The spine is right: the categories name the ground — *"it is written, it is kept true, and it is read"* — which is the correct way to sort rules for a reader who arrives in one of those three situations (my #19). Keep the word-for-word requirements and the `basis` block; the round trip that carried the words over is worth keeping as a regression check. The four layout choices also map cleanly onto the house criteria (my reading): A and B are **one thing** and **can it fail**, C is **links**, D is **who decides**.

**A — Level per clause.** **Change, but only the requirements that already hold clauses at different levels** (W1.1, W1.3, W2.1, W2.2, W3.3, W3.5, W4.1, W5.3, W6.1, W6.3, K6.1, K6.3, Rd2.3, Rd3.1, Rd4.5). Give each such clause its own id and its own `level`; leave the single-level requirements with one scalar `level`. Why: today a `level` key is a paraphrase of a sentence in `text`, so the reader must match two texts by meaning and the copies can drift. Cost: it rewrites the prose the round trip certified, so that check must be re-run.

**B — Where `fails_if` sits.** **Change to one `fails_if` per requirement, plus a `check:` field naming the runner** (`lint`, `git`, `reviewer`). Why: a group check is a hard failure that does not sit on the requirement it judges, and here it contradicts the levels — W2's group `fails_if` fails on a `kind` value while W2.1 and W2.2 are `guidance`/`SHOULD`; W4's fails on a missing `changed:` line while W4.2 is `SHOULD`; and the file itself says a SHOULD *"may be skipped with a written reason."* A fail must sit on the same unit as the level it enforces. Cost: repetition, and moving a check does not create the reviewer the judged checks lack.

**C — Links.** **Change: add a `links:` list of requirement ids per requirement (and per group), keeping the inline `(K4.1)` mention for human readers.** Why: the cross-references are load-bearing — W4.1 carries the Rd5.3 exception, W1.1 leans on W3.6, K4.3 and W6.3 depend on each other — and an agent that must scan prose to resolve them can skip them. Cost: a second copy of each reference; add a lint that every id in `links:` resolves and every inline `(X)` appears in the list.

**D — Who decides.** **Change: add `who_decides` only where the text leaves a real choice open, and write `none` where it does not.** Why: the house rule in the facts is to name who settles each open choice; without it an agent facing a MUST it cannot settle will settle it itself. Rd5.3 is the model, where the text already says EJ decides whether the entry or the code is fixed. Cost: it invites readers to treat every clause as negotiable, so keep the vocabulary closed and `none` explicit.

**Other places the draft makes an agent misread or skip.**

1. **Two shapes under one key.** `level` is sometimes a scalar (`level: SHOULD`) and sometimes a map (`level: {MUST: …, SHOULD: …}`). A script must branch; an LLM may read the map's first key as the whole level.
2. **`guidance` sits under `level:`.** The file defines guidance as *"Nothing to pass or fail,"* so it is not a level; putting it in `level:` invites a reader to hunt for a pass/fail that is not there. Move explanation to its own key.
3. **Group checks gate what the levels do not** (W2, W4, K1) — repeated from B because it is the likeliest silent misread.
4. **`fails_if` mixes lint, git and judged checks in one string** (*"a secret scanner finds a credential (W3.2). For W3.1 and W3.3–W3.6, a reviewer finds such content. Those are judged checks."*) with no runner named; the reader cannot tell what to run.
5. **A MUST whose only check is judged and has no reviewer** (the facts say none is assigned; W5.3, Rd2, Rd4, Rd5, Rd6 carry judged checks). The agent can neither pass nor fail it, so it will drop it. Assign a reviewer or lower the level.
6. **`Rd2.3`'s `SHOULD: the other four`** makes the reader count a six-item list to learn a level. Index-dependent wording; tag each item with its level instead.
7. **`Rd3.1`'s example numbers.** *"about 24 KB and 200 lines"* sits against the header's *"There are no fixed numbers,"* the gate says *"fits the strictest start-file limit,"* and nobody is named who sets it. An agent may read the example as the rule.
8. **`W4.1` labels *"no owner and no approval"* as `guidance`.** A permission that cannot fail will be ignored by an agent scanning for gates; either give it a level that can fail or mark it explicitly not gated.
9. **Inline `items` have no ids** (Rd2.2, Rd2.3, Rd5.4), so no check can cite an item.
10. **Header facts are comments.** Which Markdown this holds the requirements of, and *"a comparison that measurement decides,"* live in YAML comments: scripts drop them and agents may. Promote them to fields.
11. **Group ids skip K2 and K3.** If they are labels carried from the Markdown, say so; otherwise a reader infers missing requirements.
12. **The operative clause is buried in long `text`** (W1.2's eleven-key list, W6.2's explanation). Put the gate first.

## How I decided

1. **Reckon the field first (my #1, quoted).** Before judging the layout I laid out what decides it: an agent that must obey, a script that can parse, one tool that checks (`tools/memory_index.py`), no assigned reviewer, and no measurement of YAML. The source's own line is *"One who wins the temple reckoning before battle has gained more 算; one who does not has gained fewer. More wins, fewer does not, how much less none at all?"* A review that does not first fix the unit of a requirement is reckoning with no count.
2. **Know the reader and the ground (my #4, quoted).** *"Knowing the enemy can be attacked and our troops can attack, but not that the ground does not permit battle, is half a victory."* The COO's round trip tested the words, not the ground — an agent reading YAML at session start. Word-fidelity alone is half a victory.
3. **Orders clear first, then enforced (my #16, quoted).** *"If the rules are not clear and the orders not made familiar, it is the general's fault."* An agent that cannot tell which clause a `level` binds, or which requirement a `fails_if` fails, has unclear orders; the fault is the draft's. And *"Once they are attached, if punishment is not carried out, they cannot be used"* — a MUST with no runner is an order with no punishment.
4. **Do not rest on the reader's restraint (my #2, quoted).** *"Being unbeatable lies with oneself; being beatable lies with the enemy."* A gate that depends on the agent choosing to comply rests on the reader; a gate with a check you own does not. I put every recommendation in A–D to that test.
5. **Choose by the ratio of forces (my #14, quoted).** *"not a match, be able to avoid them. So the stubbornness of a small force is the capture of a large one."* A MUST with a lint (ten to one) is enforceable, one with a human reviewer (equal) is judgeable, one with an unassigned "reviewer" (outmatched) should not be stated as a gate. This is why B must name the runner.
6. **Mix harm into benefit (my #6, quoted).** *"So the wise one's deliberation always mixes benefit and harm: mixed with benefit, the undertaking can be carried out…; mixed with harm, trouble can be resolved."* Each recommendation above carries its price below.
7. **Change the conditions, not the people (my #12, quoted).** *"So the skilled fighter seeks it in 勢 and does not demand it of people; so he can choose people and rely on 勢."* Clause-level levels, structured links and a named runner are 勢 — they make the correct reading the easy one. Telling the agent to read carefully is 責於人.
8. **Judge the structure by what it breeds (my #20, attributed).** The small land unit with the heavy tax bred many officials and frequent wars; the large unit *"with the public coffers empty and the officials in office few"* held. A `level` whose keys paraphrase the text breeds a second copy and a matching task; one larger, self-contained record per requirement breeds less to arbitrate.
9. **Strike when attention is fresh, and leave a gap (my #18, quoted).** *"Avoid keen spirit, strike when it flags"*; among the eight, *"a surrounded army, always leave a gap; a desperate enemy, do not press."* Put gates where the agent's attention is, not at the tail of a long `text`, and leave an explicit not-applicable path so an agent facing a MUST it cannot meet reports instead of improvising.
10. **Move only on advantage (my #5, quoted).** *"Move when it accords with advantage; stop when it does not."* I recommend splitting only the fifteen mixed-level requirements; a field that carries no decision is not added.
11. **Foreknowledge from people (my #11, quoted).** *"Foreknowledge cannot be taken from ghosts and spirits, cannot be got by analogy with events, cannot be verified by measurement…; it must be taken from people who know the enemy's situation."* The layout is being decided by EJ's feeling and by an analogy from Markdown/JSON token costs — neither is a reader's behaviour.
12. **Probe the reader (my #17, quoted).** *"So reckon them to know the calculation of gain and loss; stir them to know the pattern of movement and stillness; give them form to know the ground of death and life; test them to know where there is surplus and shortage."* Only putting the file before a real agent shows where it moves and where it stops.

## What I need to know

- **Will a script parse this now, or only an LLM read it?** If only an LLM, B and D matter most; if a script, A and the two-shaped `level` key come first. My recommendations above are conditional on this.
- **Is a reviewer assigned?** If yes, MUST-plus-judged is a real gate and B is lighter. If not, as the facts say, every judged MUST is a stated gate with no force, and the honest fix is to assign one or downgrade the level.
- **Does the agent ever open this file,** or does it read `SOURCE_OF_TRUTH.md`, which points here? A gate the agent never reaches cannot fail.
- **Who determines *"the strictest start-file limit among the agents that work on the project,"*** and how is it measured?
- **Are the `text` words frozen** by the round trip, or may a revision split them into clauses? Splitting spends the one check that has been run.
- **May `guidance` be skipped entirely?** If the definitions matter, they need a check to have force.

## Costs and risks

- Splitting clauses rewrites the only text the round trip certified; that check must be re-run (my #5, my #6).
- Per-requirement `fails_if` repeats text and will drift from the group string unless one is removed or linted (my #20).
- `links:` adds a second copy of each reference; dangling ids unless a lint resolves them (my #9, my #20).
- `who_decides` invites negotiation of choices that are not open; keep the vocabulary closed (my #5, my #14).
- **Formatting cannot fix the real exposure:** MUST gates whose only check a non-existent reviewer can judge. That is a level-or-owner decision, not a layout one (my #2, my #14).
- The whole exercise is being settled on a feeling and a token analogy, with YAML unmeasured; if EJ wants a readable annex, much of A–D is not worth its cost (my #5, my #11).

## How we would know I was right

A probe, not a token count (my #17, my #11):

- Take two or three engines. Give each a fresh session with only a clone, a task id and the file, and log: (a) requirements restated with the wrong level, (b) stops or questions the file already answers, (c) open choices settled by the agent itself, (d) gates the tool catches before it acts. Run once with the draft and once with the revised layout, same task.
- I was right if the revised layout lowers (a), (b) and (c) and raises (d) on a real handoff. I was wrong if it does not — then the Markdown annex is enough and the YAML need not carry the weight.
- A structural lint (one level shape per requirement; every `fails_if` names a runner; every `links:` id resolves) is a necessary but **not independent** check: the same side wrote both the file and the lint, so passing it does not show that a reader follows the file (my reading).
