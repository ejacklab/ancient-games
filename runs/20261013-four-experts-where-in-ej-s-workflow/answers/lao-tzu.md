I'll read that brief first.
I need to read my rule list, identity, and the workflow-design method.
# 老子 (Laozi) — where in the method my rules help most

## Answer

Ask me at **3.3 unclear spots** (every batch of questions, and every spot that would otherwise force a build on an unsettled section), at **3.6 the run's end** (the three-part stop and the backlog rule), and at **3.7 the five parallel conditions**. My rules are about *what to leave out and when to stop* — the three places where the method's own rules are hardest to get right, because there each one tempts adding, gripping, or rushing.

## How I decided

1. **3.3 unclear spots** — the most reliable place, and the most checkable. My #1 is an algorithm with a stated end point: 損之又損，以至於無為 — "Lose and lose again, until one arrives at not-doing." The method's 3.3 is where unclear spots are listed *before* any is resolved. My rule and the method's rule have the same shape: reduce, again, to a stopping point, then stop. **The question to ask me here:** for this batch of spots, which ones can be answered by giving up the step rather than by resolving it — and which one, if it went the other way, would the whole design be unnecessary? That last one is my #2 (知足不辱，知止不殆 — "knowing what is enough, one is not disgraced; knowing to stop, one is not endangered") applied to the method's own tiny test in §2. A spot that can be made to disappear by subtraction is cheaper than the spot is.

2. **3.6 the run's end — the stop and the backlog.** The method already ends a run at the three-part stop and writes everything else to `docs/blueprint/backlog.md`; that is my #3 almost word for word in function: "The work done, the self withdraws: this is the Way of heaven" (功遂身退，天之道). The method's job is *not* to grasp the whole product, and my #4 says why in the method's own vocabulary: 天下神器，不可為也 — "The world is a sacred vessel; it cannot be acted on." **The question:** at this run's end, which of the acceptance criteria in scope are genuinely the objective the challenge named, and which were added because a node found them nearby? The answer tells you which findings belong to the backlog and which belong to the design's promise. This is checkable: the criteria ids were fixed before the run, so an added one is visible by diffing against the design.

3. **3.7 the five parallel conditions** — reliable, but narrower. The method holds sequential-first and asks for five conditions before fanning out. My #7 is the same warning from the other side: 民之從事，常於幾成而敗之 — "People, in their undertakings, often fail when they are close to finishing"; 慎終如始，則無敗事 — "Careful at the end as at the beginning: then no undertaking fails." **The question:** of the joins the design adds for parallelism, which is the *last* one — the handoff into the final pass — and what check runs there? A run that is careful everywhere except its final seam fails exactly where the method says it will.

4. **Not 3.1 or 3.2** — I have almost nothing to give there, and I will say so rather than stretch. My #11 is a mindset ("Reversal is how the Way moves"), not a procedure. The method's readiness check (prove each tool by running it) and its algorithm step (a step with no nameable check is unclear) have no counterpart in my list. *My reading*, not my #n.

## What I need to know

- **Whether the piece you would bring me is a build or a research/design piece.** My #1 subtracts; it does not tell me what to remove. Given the piece's steps and deliverable I can judge; given only the challenge text I can only ask the question back.
- **Whether the criteria are already fixed, or still being drafted (3.1 blueprint status: settled / draft / incomplete / missing).** This decides my answer at 3.6: if criteria are still draft, there is nothing yet to diff against, and the question I would ask is instead "which of these is EJ's?" — 3.1's own rule that blueprint questions are not answered by silence.
- **Whether the run is near its end or near its start.** #7 is only worth asking at the end; at the start, asking it produces ceremony. My #18 (attributed) is the closest thing in my list to a timing rule — 且君子得其時則駕，不得其時則蓬累而行 — "when he gets his time, rides out; when he does not, he wanders and goes" — and it says timing matters, not what to do when it is not.

## Costs and risks

1. **My #1 costs the piece that was not needed.** If I am called on every batch of unclear spots, I will recommend subtraction and the design will lose scope the challenge actually asked for. The method's 3.3 wants each spot resolved with a provisional assumption; my rule's end point is 無為 — not-doing — and not-doing can read as "stop asking," which is the opposite of the method's job.
2. **My #4 and #5 make me unreliable anywhere the method asks for coverage.** 為者敗之，執者失之 and 我無為而民自化 both say do not grip the system. The method's 3.6 requires every criterion in scope to be covered by at least one node, and its §5 requires three named qualities. A design judged by my rules alone would drop the criterion nobody volunteered to cover. *This is the sharpest risk in my answer: my rules reward subtraction, and the method's rules sometimes require addition.*
3. **I would not be reliable at 3.5 or 3.8 — the mechanics.** My list has no rule about attempt limits, tier escalation, timers or pass-back, and the method's own 3.5 item 4 says a stronger tier gets a short handoff note after a flailing session. My #3's 功遂身退 is the *completion* of the work; it is not the method's claim that re-running a failed node on a stronger tier is a fresh node rather than a mid-session switch. I would read "withdraw after success" as "withdraw instead of retry," and that reading is wrong. *My reading, flagged.*
4. **My #15 is the weakest of the ones I lean on.** 上善若水 and its seven clauses are a mindset with no order, and the witnesses disagree at the exact words I would be leaning on: silk A has 有靜 where Wang Bi has 不爭, silk B has 而有爭 — the list records this as unresolved. If my answer at 3.7 rests on 不爭 ("because he does not contend, there is no blame"), it rests on a contested word. I do not lean on it above; I name it so you can discount it.
5. **Item 8's own wording is contested.** 知不知上，不知知病 — the second clause is read as 不知知 (Wang Bi, silk B) or 不知不知 (silk A), which point opposite ways about which disease is which. I would not hang a spot-classification rule on it, and I would not have used it if I had not checked the witnesses.

## How we would know I was right

**One test on a real design, with a number that already exists.** Take a run whose design names its pieces and its acceptance criteria, and check three things at once:

- **At 3.3:** take the batch of unclear spots and count how many are marked *information* or *unknown* that could instead have been dropped — a piece removed, a scope narrowed. If my rule is doing real work, at least one spot in a typical design disappears, and the run still ends at its objective. If nothing disappears, I have been decoration.
- **At 3.6:** diff the criteria ids in the final `changelog.md` against the ids the design fixed before the run. My answer predicts that added ids land in `backlog.md` with a date and run id, not in the criteria. If added criteria appear in scope, the grip held and I was wrong.
- **At 3.7:** in the run's own `feedback.jsonl`, find the last join and whether a check ran there. My #7 predicts the final seam is where failures cluster and where checks are most often missing.

**The falsifier, stated plainly:** my answer is wrong if, over three real designs, the spots I tell you to drop are ones the challenge's objective actually needed — measured by whether the run still hits its stop condition without them. That is checkable by the method's own §2 test, and it does not require believing anything I said.
