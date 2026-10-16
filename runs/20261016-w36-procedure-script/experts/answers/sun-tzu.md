# 孫子 (Sun Tzu) — A procedure, a script, and who decides

## Answer
A procedure cannot always be a script: it can be one only when every step follows from inputs the procedure names, an objective check can decide its outcome with no person reading it, and it will run again on ground that stays still; where any of the three fails it is a page in `docs/`, and where only a human gate interrupts it, a script that stops at that named gate. The test decides the clear case, so the **agent writing the procedure** applies it at the moment of writing — that is who reads the ground — while the **project owner** decides the case the test leaves open and should close `who_decides` now by naming the test, because an unclear order is the rule-writer's fault and not the agent's (my #16); if "should not" is in scope as well as "cannot", the test decides the "cannot" and the owner decides the "should not", for that half is a value, not a reckoning.

If W3.6 should change, I would rewrite its placement clause as: *"A procedure lives in the repo as a script when every step follows from inputs it names, an objective check can decide its outcome, and it will run again on ground that stays still; otherwise it lives as a page in `docs/` and names which of the three failed. The agent writing the procedure applies this test and records the result; the project owner decides the case the test leaves open."*

**The test an agent can apply** (my reading, built from my #2, #4, #8, #13, #19). For a procedure P, answer four questions from what is written and what runs:

1. **Determinacy** — does each step's action follow from inputs the procedure names, or does a step say *judge / decide / review / assess* something not among them? A step needing a live judgement is not script-determined.
2. **Check** — can you write the check that decides pass/fail with no person reading it, the `verify.sh`? If not, P cannot be a script.
3. **Repeat and ground** — will P run again, close enough to the same ground (same tools, same environment, same interfaces)? Count runs against build plus upkeep.
4. **Path** — does P need a human act, a secret, an approval, or a physical move at some step? Name that step.

**Verdict.** 1, 2, 3 all yes → script; if 4 names a step, the script runs to that gate and stops, and the gate is named in `AGENTS.md`. **2 no → page**, naming the missing check; this is the decisive failure, because an unwritten check is the unbeatable ground you do not have. **3 no → page** (one-off, or ground moving faster than upkeep; the facts say `procedure-to-skill` itself excludes "a procedure specific to one throwaway task"). **1 no and the judgement is the substance → page**; if the judgement is confined to one branch, script the rest and leave the gap at that branch (my #18). For "should not" — policy, irreversibility, secrets, steps already owned by another document — the mechanical test cannot decide; that is the owner's call, and W3.6's own `fails_if` already covers the copy.

## How I decided

1. **I reckoned before choosing the form (my #1).** 「夫未戰而廟算勝者，得算多也…多算勝，少算不勝，而況於無算乎？」 — *"One who wins the temple reckoning before battle has gained more 算… More wins, fewer does not, how much less none at all?"* The question picks between two grounds for a procedure whose ground I have not measured, so I measured first. My #1's chain 「地生度，度生量，量生數，數生稱，稱生勝」 gives the order: the ground first (who runs it, where, how often, what it touches), then the steps, then the weighing of the two forms. Choosing the form first and justifying it after is 無算.

2. **I put the verifier before the script (my #2).** 「昔之善戰者，先為不可勝，以待敵之可勝…故曰：勝可知，而不可為。」 — *"The skilled fighters of old first made themselves unbeatable and waited for the enemy to become beatable… victory can be known but cannot be made."* A script's unbeatable ground is its check. If I cannot state that check, I cannot make the procedure safe, and the enemy — a moved file, a renamed tool — decides the outcome. Hence: **no objective check, no script.** The repo already has this shape: `procedure-to-skill` builds `scripts/procedure.sh` *plus* `scripts/verify.sh` (a fact given to me, not my rule).

3. **I asked whether the ground permits battle (my #4).** 「知可以戰與不可以戰者勝」 — *"one who knows when he can fight and when he cannot wins"* — and 「…而不知地形之不可以戰，勝之半也」…「知天知地，勝乃可全」 — *"knowing… but not that the ground does not permit battle, is half a victory… know heaven and ground, and victory can be whole."* A script that runs but cannot know whether it should is half a victory. Two signs decide it: a step needing a live judgement the script cannot read, and ground that moves between runs.

4. **I refused the constant form (my #10).** 「故兵無成勢，無恒形，能因敵變化而取勝者，謂之神。」 — *"an army has no fixed 勢 and no constant form; one who can take victory by changing with the enemy is called divine."* "Always a script" or "always prose" is a constant form in a moving ground, so the answer must classify, not command.

5. **I classified by ground and acted as prescribed (my #19).** 「是故散地則無戰，輕地則無止…死地則戰。」 — *"So on scattered ground, do not fight; on light ground, do not halt… on dead ground, fight."* That is a table from condition to response, with no steps; the test above is that table, made to fit a procedure.

6. **I located the first decision where the ground is read (my #13, my #17).** 「途有所不由…君命有所不受。」 — *"There are roads one does not take… ruler's commands one does not accept."* The general on the ground is not bound by a standing order that does not fit it. And 「故策之而知得失之計，作之而知動靜之理…」 — *"reckon them to know the calculation of gain and loss; stir them to know the pattern of movement and stillness."* The writer is the one who can probe: attempt the script and its check, and read the sign when the attempt fails. So the writer makes the first call, at the moment of writing or first change, before the procedure is committed.

7. **I kept the ruler on the rule and the appeal (my #16, my #11).** 「約束不明，申令不熟，將之罪也；既已明而不如法者，吏士之罪也。」 — *"If the rules are not clear and the orders not made familiar, it is the general's fault; if they are already clear and are not followed as the law requires, it is the officers' fault."* W3.6's `who_decides` is unassigned, so the fault is the rule-writer's: EJ closes it by naming the test. 「先知者…必取於人，知敵之情者也。」 — *"Foreknowledge… must be taken from people who know the enemy's situation."* The unclear case goes to the one who knows the procedure, and to the owner, and that knowledge is paid for in their time.

8. **I sought it in 勢, not in people (my #12).** 「故善戰者，求之於勢，不責於人，故能擇人而任勢。」 — *"the skilled fighter seeks it in 勢 and does not demand it of people; so he can choose people and rely on 勢."* The rule should force the answer from conditions, so the clear case needs no person to decide it. This refines my earlier recorded line (the project owner): the owner owns the rule and the contested case; the ground decides the clear one.

9. **I examined the decider for the five dangers (my #15).** 「故將有五危︰必死，可殺也﹔必生，可虜也…」 — *"The general has five dangers: set on dying, he can be killed; set on living, he can be captured…"* The writer set on scripting everything is killed by a brittle script; the writer set on prose is captured by drift; the quick one scripts to end the interruption; the one scrupulous about craft scripts to show skill. These are reasons to make the test mechanical rather than trust the writer's virtue.

10. **I wrote the harm before the benefit (my #6) and weighed what each form breeds (my #20).** 「是故智者之慮，必雜於利害」 — *"the wise one's deliberation always mixes benefit and harm."* See the two sections below.

## What I need to know

1. **Does "cannot" in W3.6 include "should not"?** The question says both; W3.6 says only "cannot". If "should not" is in scope, my test covers only the first half and the owner must own the second; the wording must say which half is meant. This one changes the shape most.
2. **Who for — are these procedures run by agents only, or by people too?** I was not given it. If people run them, the ground changes and the page may be the only form that works across this repo's several engines and human hands.
3. **Will scripts run unattended here?** Are there secrets, approvals, network calls to people, or physical steps? If so, condition 4 bites often and most procedures become scripts with named gates rather than pages.
4. **How often do procedures repeat, and who pays the upkeep?** Condition 3 needs a threshold or someone's estimate. I was given no number and no budget, and I will not invent one (the list's own Gaps mark my ranking "not measured").
5. **Does the owner want `who_decides` closed as I propose — the writer for the clear case, the owner for the open one?** My answer changes the requirement and only EJ changes it. Until then agents keep guessing.
6. **Is W3.6's `check: reviewer` the project owner or a separate reviewer?** If a reviewer already exists, the *who* is named and only the test is missing; if not, the independent re-application in the section below is not available.

## Costs and risks

- **The test spends speed before it buys it** (my #8: 「故兵聞拙速，未睹巧之久也」 — *"one hears of clumsy speed, but has not seen skill that is prolonged"*). Requiring a written check before a script delays automation, and some procedures that could become scripts will sit as pages for a while. The price is paid to avoid a script that is silently wrong.
- **Any test can be gamed by a weak check** (my #7: 「兵者，詭道也」 — *"War is the way of deception"*; my #15). A check must be shown to fail on a deliberately broken run; an asserted check is worth nothing.
- **Owner-decides makes the owner a bottleneck** (my #9: 「故善戰者，致人而不致於人」 — *"the skilled fighter brings others and is not brought by them"*). Mitigation: W3.6 is SHOULD, so the writer defaults to the page and writes the open question in the task's `state.md` rather than stopping.
- **Defaulting to the page costs repetition and leaves the page to drift** (my #6: name the harm). The facts' own skill says a prose description "summaries drift". This is visible harm; a wrong script is hidden harm, which is why I prefer the page when the check is absent.
- **Adding the test to W3.6 adds a fourth thing to a requirement already judged to bundle three** (my #16: an unclear order is the rule-writer's fault). If it stays bundled, the test may be read by no one. The price is EJ's time to split or reword.
- **Deciding by 勢 means no named author for each classification** (my #12, my #13). If a verdict is wrong, blame is diffuse. Mitigation: the writer records the four answers in the task's `state.md`; that gives a name and a reason to appeal.
- **A script that grows dependencies and churn falls** (my #20: the houses that multiplied officials and fought often fell first). Keep the script small and carrying its own check; if it cannot stay small, the page is the form that holds.
- **The value of this test is not measured** (my list's Gaps). I am not claiming it makes this seat's reviews better.

## How we would know I was right

- **A test I would write, and who wrote it.** For the next batch of procedures under the reworded W3.6, the writer records the four answers; a second agent who did not write the procedure re-applies the test from the text alone. Right means the verdicts agree on nearly all, and every disagreement is traced to a wording gap that is then fixed. This check is mine (孫子's seat) and it does **not** establish that the chosen form was best for the work — only that the test is applicable and consistent, and it cannot show that a writer did not game the check.
- **Observable, cheap.** Every procedure classified "script" has a `verify.sh` that fails when the script is deliberately broken (one broken run per script); every "page" names the condition that failed; no entry copies a procedure's steps, so W3.6's `fails_if` stays false; the `who_decides` field no longer reads `unassigned`.
- **One season later.** Count reclassifications. Right means few, and each was foreseen by the condition that failed — the page that should have been a script failed the **check**, the script that should have been a page failed the **ground**.
- **The cheapest signal.** Writers stop asking "can this be a script?" and start asking "can I write its check?" That is the test taking.
