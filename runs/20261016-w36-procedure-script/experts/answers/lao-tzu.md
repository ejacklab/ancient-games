I'll read the brief first.
# 老子 (Laozi) — Can a procedure always be a script?

## Answer

No. A procedure is a script when its last step can be written as a command that exits non-zero when the job is not done; where that last line has to be a judgement, it is a page in `docs/` that names the step it cannot check and the person who decides it; where there are no steps, it is written nowhere. The agent writing the procedure chooses in the first two cases and writes the reason; the project owner decides only the cases the agent cannot — which is what I said before, that the owner decides through `AGENTS.md`, now with a test in front of it.

## How I decided

1. **A prose copy of a procedure inside memory is an addition to a thing that already exists.** My #1: 「損之又損，以至於無為」 — "Take away, and take away again, until you reach not-doing." The script already is the procedure; a second telling of it is the 「為學日益」 half, the part that gains daily. So the first half of W3.6 (no copying) and the placement rule are one rule, and it is a subtraction rule. This is why the repo's own reasoning held: a script is project work.

2. **But not everything can be a script, and the reason is in the text, not in convenience.** My #17: 「故有之以為利，無之以為用」 — "what is there makes for benefit; what is not there makes for use." A procedure's use can lie where no command reaches: which of two disputed readings is right, what a thing is called, who owns a judgement. There is no command for these, and my #4 says why gripping one is costly: 「天下神器，不可為也」 — the world is a sacred vessel that cannot be acted on. Turning a judgement into a script would make the script the decider, and a script cannot be argued with. *That the sacred vessel applies to procedures is my reading.*

3. **The test is the last step, and nothing else.** My #7: 「慎終如始，則無敗事」 — people fail when the work is nearly done, so hold the end as carefully as the beginning. A procedure's last line is where it either holds or fails. So: write the last line as a command, and say what makes it exit non-zero. If you can do both without asking anyone to weigh, judge or agree, it is a script — `scripts/<name>.sh` plus `scripts/verify.sh`. If the last line needs someone's judgement, it is a page in `docs/`, and that page's job is to name the step and the decider. If there are no steps, write nothing (my reading of my #1:損之又損 down to not-writing; the repo's `procedure-to-skill` already excludes facts with no steps and one-off tasks).

4. **The valve must be narrow, or `docs/` becomes the second memory.** My #4 ends 「去甚，去奢，去泰」 — discard the extreme, the extravagant, the excessive. A page that re-lists steps is exactly that (my reading). So the page's only content is: the step that has no check, and who decides. Nothing else.

5. **The agent will often *think* it knows which bucket, and should write the reason rather than the certainty.** My #8: 「知不知上，不知知病」 — knowing that one does not know is highest; pretending otherwise is the sickness. My list also records the wrinkle: WB and silk B read 不知知, silk A reads 不知不知 — the two point opposite ways. The clause I lean on is itself a crux, so no agent should be allowed to assert the answer from confidence. This costs nothing, because W3.6 is a SHOULD: the reason written in `state.md` is already the escape the design provides.

6. **Who decides is settled by position, not by rank.** My #9: 「是以欲上民，必以言下之。欲先民，必以身後之。」 The one who must be above the people goes below them in speech; the one who must be in front goes behind them in person. Read onto this: the decider is the one who is *behind*, and the proposal is written in words below (my reading). The agent writes the choice and the reason; the owner can overturn it without contest (my #14, 「夫唯不爭，故天下莫能與之爭」). My earlier one-line view — the owner decides, through `AGENTS.md` — stands, because that is where the scripts are already named and therefore where the owner reads anyway. Naming a decider is the price of the page.

7. **Two moments, no ceremony.** My #6: 「為之於未有，治之於未亂」 — act on it before it exists. The agent decides while writing the procedure, when it is small; the owner settles at review, which is where W3.6 is checked anyway (`check: reviewer`). My #6's other half is the price: 「輕諾必寡信」 — light promises bring little trust — so a script nobody has run once is a promise, and a promised script is worse than a page. The agent must run the script before claiming the bucket.

8. **Do not build a procedure for deciding.** My #2: 「禍莫大於不知足」 — no calamity is greater than not knowing what is enough. My #3: 「持而盈之，不如其已」 — holding it and filling it is not as good as stopping; 「功遂身退」 — when the work is done, withdraw. A rubric for classifying procedures would be the very kind of page W3.6 forbids. Two sentences of test, then stop.

9. **If the owner is not there, nothing should wait.** My #18 (`attributed`): 「且君子得其時則駕，不得其時則蓬累而行。」 The default must therefore be the agent's, not the owner's — otherwise "where it cannot be a script" becomes a queue in front of a person (my reading). The owner is a fallback, not a queue.

## What I need to know

- Whether the project owner actually reads `AGENTS.md` and the reviews. If `AGENTS.md` goes stale, the decider named there is a fiction, and step 6 collapses.
- Whether the owner reviews once per task or once per run — that changes which of the two moments in step 7 carries the weight.
- Whether this repo already holds one procedure nobody could turn into a script, and what its last step was. If such a thing exists, its last step is the test's real specimen; I have not seen it.
- Whether `docs/` is the only page location, or whether procedures also live inside `AGENTS.md` prose. The facts I was given name only `docs/`.

## Costs and risks

- **The test can be gamed into a green light.** A `verify.sh` that exits zero without checking anything satisfies "the last line is a command" while checking nothing. My #7: careful at the end is the whole point; a cheap end is the common failure. The written reason is the guard, not the test.
- **A certainty-shaped trap.** Because the clause I lean on is textually contested (my #8), an agent may treat a guess as knowledge. If the design wants certainty, that is the price of my answer.
- **Naming the owner as fallback can make the owner the front of the queue** (my #18, my #10's 「不敢為天下先」). Mitigated only by keeping the agent's default; if the owner starts getting every ambiguous procedure, the valve has become a ceremony.
- **A page that repeats steps will grow back**, and it grows quietly, because it looks like documentation. My #1: additions accrue daily unless someone subtracts. The `fails_if` line ("an entry copies a document or a procedure's steps, with no written reason") does not catch a *legitimate* page that re-lists steps — that gap is mine to name.
- **Splitting W3.6** (as others say it bundles three things) costs a cross-reference and one place for a reviewer to look (my #14: 「不自見故明」 — not displaying yourself, he is clear; the naming in `AGENTS.md` is what makes a script findable, and scattering the rule makes it less so).
- **If the owner contests the agent's call**, the fix is a written reason on both sides, and that is more paperwork than "ask the owner" — my #9's price for putting the decider behind.

## How we would know I was right

- **Take every page in `docs/` that answers "this cannot be a script" and ask two questions:** does it name the step that has no check, and does it name a person? Zero answers on either means the test is being cited, not applied.
- **Ask ten agents, for ten existing procedures, "which bucket?" and separately "what makes your script's last line exit non-zero?"** If the two answers disagree often, my test is not sharp enough to be a rule — and I would be wrong.
- **Count scripts that were written and never run once.** My #6's 「輕諾必寡信」 predicts this count will be non-zero; if it is zero, either the agent is running them or the bucketing is honest, and I would expect to see it.
- **The observation that would refute me:** procedures turned into scripts where nobody can say what non-zero means, and the repo treating those scripts as done. At that point a page was the right form and the test failed. That is the measure to watch.
