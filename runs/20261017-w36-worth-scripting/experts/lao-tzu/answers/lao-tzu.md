I'll read the brief first.
# 老子 (Laozi) — May a scriptable procedure stay a page for rarity?

## Answer

Yes, conditionally — it may stay a page when the task's `state.md` names both sides of one comparison: what the script would save (the effort and the mistakes it removes, counted only over runs on ground that stays still) against what it costs to build it and to keep it exercised after every change around it — and no number may stand in for either side. The agent writing the procedure writes that comparison and the page; what the saving is *worth* is the project owner's to weigh, because the agent is the one in front and puts itself behind (my #9).

## How I decided

1. **The comparison is already in my list, and it has no number in it** (my #2, `quoted`): 「甚愛必大費，多藏必厚亡，知足不辱，知止不殆，可以長久。」 — "great fondness must mean great expense, and much hoarding must mean heavy loss. Knowing what is enough, one is not disgraced; knowing to stop, one is not endangered; one can last long." The words measure *much* against *loss* and promise only 可以長久. So the test a rule may use is "this much against that much", never "at least N times a year" (the owner's house rule on thresholds; research A9 in the brief: no source found gives a measured break-even frequency).

2. **The two sides are not symmetric, so the rule must name both** (my #6, `quoted`): 「為之於未有，治之於未亂。」 — "Act on it before it exists; order it before it is in disorder." The first script is the cheap half, while it is small — and 「多易必多難」, "much taken as easy must bring much difficulty". The expensive half is keeping it: run, or exercised, after every change around it (research A2, B2, B10, B11 — brief:73–75, 110–111). So the comparison is *first script + keeping* against *saving*, and rarity alone never decides either side (my reading).

3. **Rarity by itself is not a reason, because both forms decay when unused** (my #7, `quoted`): 「民之從事，常於幾成而敗之。慎終如始，則無敗事。」 — "People, in their undertakings, often fail when they are close to finishing. Careful at the end as at the beginning: then no undertaking fails." A page nobody followed goes stale with nothing to signal it, and the person following it is out of practice; a script nobody runs breaks unseen (research C16, C18, C19, D — brief:134, 146–149, 167). The written comparison is the end of the work, where the failure is (my #7).

4. **One case flips the answer: a procedure run only when something has gone wrong** (my #13, `quoted`): 「兵者不祥之器，非君子之器，不得已而用之，恬淡為上。」 — "Weapons are instruments of ill omen, not the gentleman's instruments; when it cannot be avoided he uses them, and calm indifference is best." A script is a weapon held ready (my reading of the application). If the one time it runs is the emergency, an unexercised script is verified at the one moment it is needed, by a person whose hands have forgotten — so keep the page and *exercise the page* (game days, runbook tests — research C16, C18), or write the script and exercise it on a schedule (research B14, C16). Conditional: emergency-only ⇒ exercise, do not merely script.

5. **What the page is for stays the empty part** (my #17, `quoted`): 「三十輻共一轂，當其無，有車之用。…故有之以為利，無之以為用。」 — "in its nothing lies the cart's use … what is there makes for benefit; what is not there makes for use." A page kept for rarity must still name what it is for and what the script could not hold, or it is only a summary (the repo's own `procedure-to-skill`:15: "A prose description of a procedure is a summary of the memory, and summaries drift").

6. **A middle form, because all-or-nothing is the wrong shape** (research A3, A7, A8 — brief:77, 93–103): a page carrying the exact commands, then a do-nothing script, then partial automation. What must not happen is a number pretending to be a decision — "the third time, then script" is an analogy from duplicated code, not from operations (research A6, brief:88–92), and I cite it as such.

7. **Who decides** (my #9, `quoted`): 「欲先民，必以身後之。是以聖人處上而民不重，處前而民不害。」 — "wanting to be ahead of the people, one must in person put oneself behind them. So the sage is above and the people do not feel the weight; he is in front and the people are not harmed." The agent writing the procedure is the one in front: it is the one that reads the ground and it may not weigh its own ease, so it decides provisionally and writes the comparison down. The value of a saving is the owner's ground, so that half is the owner's (my #18, `attributed`: 「且君子得其時則駕，不得其時則蓬累而行。」 — "a gentleman, when he gets his time, rides out; when he does not get his time, he goes off like drifting tumbleweed"), and the owner's time is not the agent's. W3.6's `who_decides` line (`docs/memory-system/SOURCE_OF_TRUTH_REQUIREMENTS.yaml:299`) already says this; what is missing is the *moment* and the *reason written*.

8. **The moment is where the skip already happens** (the same file, `levels:`, lines 31–33): SHOULD "may be skipped with a reason written in the task's `state.md`". So the mechanism is in place and W3.6 need only say what the reason is — a named comparison — not create a new gate (my reading).

9. **The two sentences to add to W3.6**, after "A procedure lives in the repo as a script with an external check." (my wording, after my #1's shape — a repeated step and its end point and nothing more: 「損之又損，以至於無為。無為而無不為。」 `quoted` — the keeping is a subtraction that goes on, so a script must be paid for out of what remains, not out of its first run):

   > A procedure that could be a script may stay a page when the task's `state.md` names both sides of the comparison — what the script would save, the effort and the mistakes it removes counted over runs on ground that stays still, against what it costs to build it and to keep it exercised after every change around it — and neither side is replaced by a number. The agent writing the procedure writes that comparison and the page; the project owner decides what the saving is worth, and decides it wherever it is contested, which is what the comparison is written for.

   And the matching `fails_if` clause (it is `check: reviewer`, line 298, so the reviewer's job is the *presence* of both sides, not their weight): *"...or a procedure page names no step a script cannot do and no `state.md` comparison naming both sides, with no written reason."*

10. **Proposed change to the pattern.** Our pattern has the main agent decide provisionally from advice and send only an exhausted question to EJ. Here two seats hold different halves of one decision — Linus (`runs/20261016-w36-procedure-script/experts/answers/linus.md:19`) calls it "a cost judgment, not technical impossibility"; 孫子 (`…/sun-tzu.md:4`) says the "should not" half "is a value, not a reckoning". I propose the answer format carry one extra line — **the comparison, in one sentence, in the same shape every seat uses** — and that each half be marked owner-or-agent, so the `state.md` line can be copied without rewriting and the main agent knows which half it may not decide for EJ (my #9).

## What I need to know

1. Who is the project owner for W3.6 changes in this repo, and are they reachable *at the moment an agent writes a procedure*? If not, my step 7 reduces to: the agent writes the comparison and the open question in `state.md`, and the owner rules later. This changes the who, not the test.
2. For each procedure page now in `docs/`: how often it ran in the last year, and what it saved when it ran. I was not given this, so I cannot say how many pages the rule would release into scripts — and I will not guess a count.
3. Which of those pages are emergency-only (run only after something broke)? Those flip at step 4.
4. Does anything today run the repo's scripts on a schedule or in CI? If nothing does, the keeping side of every comparison is heavier than I have assumed (research B15 is `reported`, brief:127–129), and my answer is biased toward pages.
5. Is W3.6's `check: reviewer` the project owner or a separate reviewer? It decides whether step 9's `fails_if` is checkable at all.

## Costs and risks

- **My answer legitimises pages that should have been scripts** (my #7): a rarely-run page decays silently and is followed by someone out of practice (research C16, C18, C19). Price: W3.6 buys correctness-at-rest at the cost of work per run, and says so nowhere.
- **The comparison is judged once, on a forecast, by the agent** (my #8, `quoted`: 「知不知上，不知知病。」 — "Knowing not-knowing: highest. Not-knowing knowing: sickness"). The agent cannot know how often the procedure will run; my step 4's exception is the only case I can name where knowing matters most. Price: forecasts are wrong, so the `state.md` line must carry a date to be re-read.
- **The agent's "enough" may be its own convenience** (my #2:甚愛必大費，多藏必厚亡 — much hoarding means heavy loss; and my #4, `quoted`: 「為者敗之，執者失之。」 — "one who acts on it spoils it; one who holds it loses it"). A script nobody decided not to build is held, not used. Price: this is exactly why the value half is the owner's; if no owner rules, the agent keeps the page and the hoarding has no name.
- **Rarity as permission will be used as a pretext** (my #14, `quoted`: 「少則得，多則惑。」 — "little, then gained; much, then confused"; and my #3, `quoted`: 「持而盈之，不如其已」 — "To hold it and fill it is not as good as stopping"). Procedure pages multiply, each a summary nothing checks. My #6 cuts the other way — 多易必多難 — so rarity must not be *sufficient*, or easy procedures stay pages forever.
- **Reviewers can check that a comparison exists, not that it is right** (`check: reviewer`, line 298). A rule that says "compare" without naming the two sides produces unverifiable prose that satisfies the check. Price: step 9's `fails_if` wording, which is the part that can fail.

## How we would know I was right

1. **One pass, this repo, today:** count the procedure pages in `docs/` that have a `state.md` line naming both sides. If nearly none do, then either the rule is unimplementable as written or the pages are unjustified — and the gap itself is the measurement, not a number I invent.
2. **After the rule is in:** the number of procedure pages that later became scripts, and how many runs each had at the moment it was converted. If conversion clusters around a count, the honest rule is that count and my "no number" claim is wrong for this repo; if conversions happen at 1–2 runs or never, the comparison is carrying the weight and the rule stands (measure, do not assume — research A6's "rule of three" is an analogy about duplicated code, brief:88–92).
3. **The failure case:** a page kept for rarity followed after the world changed, failing at a step the script would have failed at too. That failure proves the comparison predicted nothing, and the fix is to the rule, not to the page.
4. **Owner-decisions requested:** the count per run. If it is zero, the value half has silently stayed with the agent and my #9 is being violated in practice — the clearest sign my step 7 does not work as written.
