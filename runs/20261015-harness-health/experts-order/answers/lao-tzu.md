I'll read that file first.
# 老子 (Laozi) — which comes first: vision, requirements, or use cases

## Answer

Write them forward by subtraction — vision, then the requirement's behaviours as fixed units, then use cases attached to those units as evidence — but check them in reverse, and let nothing change except a check that has been seen failing. EJ's "use cases first" holds as the checking and revision order and breaks as the writing order; whether I am right is settled by the measure at the end, not by me.

## How I decided

1. My #15 is seven parallel clauses with no order, and my #16 says outright it is not a ladder. So my reading: any rule of mine read as a sequence is being misused. That reframes the question from "which of the three is first" to "what is written when, and what is checked when."

2. My #1 is the only item of mine that is an algorithm, and its end point is subtraction: 損之又損，以至於無為 — "lose and again lose, until not-doing." Three artifacts written in one pass is three losses taken at once. The writing order is therefore the order in which each step removes work from the next, not an order of importance.

3. My #4: 天下神器，不可為也 — "the world is a sacred vessel; it cannot be acted on" — and 為者敗之，執者失之. Holding the whole of a product is that grip. So the vision cannot be a description of the product; by my #17 the use is in the emptiness — 故有之以為利，無之以為用 — and the template's emptiness is already named: "what it will not do." My #10's 儉故能廣 is why it stays spare: a spare vision is the one that can be carried to the next project, which the house rule on hardcoding demands.

4. My #6 gives EJ's instinct its weight: 其未兆易謀 and 為之於未有，治之於未亂 — act on a thing before it exists, order it before it is in disorder. A use case is the 未兆 state, and the trial is the evidence: both lists surfaced the same clause with no "fails if" and one "fails if" with no test and no code.

5. My #6 also says what is easy to hold is a thing at rest: 其安易持. A case generated before the behaviours are fixed units has no unit to hold. The trial prices this exactly — 200 cases, 20% raw coverage against 46%, the same 80% over units, and one case contradicting a decision already settled in the tests. Such a case is not evidence; by my #14 it is 自伐故有功, one that displays itself. R11.1 already agreed the cure: a case attaches to a unit and never adds to the count.

6. So the writing order is vision → units → cases, and the checking order is its reversal: a planted wrong input enters at the case and the check must fail at all three levels before it counts. My #11 names both halves honestly — 反者道之動, "reversal is the movement of the Way," and 弱之勝強…天下莫不知莫能行: everyone knows this and no one practises it. My #12 (將欲廢之，必固興之) is the reversal's name only; my list records that the words do not say who stretches or what follows.

7. My #8 closes the loop: 夫唯病病，是以不病 — "only by treating sickness as sickness is one not sick." A check never seen failing cannot be told from a check that cannot fail. The loop closes on witnessed failure at every level, not on finished documents — the same ground as the house rule and as "old use cases count only after failing on a planted violation."

8. Where EJ's order holds: checking and revision, always — my #7, 民之從事，常於幾成而敗之; 慎終如始，則無敗事. The failure is at the nearly-done stage, and the last artifact written is the first one rushed. Cases are how the nearly-done requirement is caught.

9. Where it breaks: as the first writing pass over requirement text. Concrete case, the 200-case brainstorm — same two gaps, four times the output, plus a case contradicting a settled decision. My #4's remedy, 去甚，去奢，去泰. Under my #13 (善有果而已 — "the good one has a result and that is all") the 28-case list had already produced the result.

10. The stop. My #2: 禍莫大於不知足, and 知足之足，常足矣 — "the enough of knowing enough is a lasting enough." 80% of units is a number, not an enough. The stop is a comparison in consequence: continue while an uncovered unit can be named with a loss someone decides is real; stop when the remaining units are those whose absence nobody can name a loss for. That is R11.1's "skipped by consequence, not frequency" used as the exit, and it leaves the call with EJ.

11. Who writes what. Vision: EJ alone — my #18's 良賈深藏若虛 (attributed), and the template's rule that an agent may only write down what EJ has said. Requirements: the agent that runs the engines, from EJ's said words, one maker per record. Cases: the engine that will be judged by them; an AI-generated case is evidence with a maker attached, not a maker. Each artifact must work without its maker's hand afterwards — my #5, 我無為而民自化.

12. The check each must pass. Vision: name a second project — the four lines must still hold there; if none can be named, the check cannot fail and the vision may already be a plan, which by my #3 (功成而弗居) it should then stop being called. Requirement: every clause has a "fails if" that is a comparison, and each MUST is a safety bound — the clause with no fails-if is what this check fails on. Case: it names its unit and has failed once on a planted violation of it.

13. Revision, and the discipline. My #3 again: the vision changes last, and only when a failing case contradicts its "will not do". Dropped units are this round's dead, and by my #13 戰勝，以喪禮處之 — a victory is handled with the rites of mourning. The whole answer is held by my #19's 以深爲根，以約爲紀 (attributed): depth as the root, restraint as the rule.

## What I need to know

- Whether 80% of units is a settled commitment or a placeholder. If settled, my #2 makes it EJ's to define; I do not decide it.
- Whether "what it will not do" is a clause needing a fails-if. If it does, the vision has no check of its own, and my #17 says its use is in the absence — so its check cannot be a fails-if.
- Whether an engine may restate a vision EJ has said once, or only repeat his words verbatim. That changes who may make the vision.
- Whether n=1 is enough. My #8: knowing that you do not know. One requirement cannot separate 28 from 200.

## Costs and risks

- Vision first: if it is wrong, everything below is wasted. Bounded by my #4 — a bound, not a grip — not removed.
- Units first: a clause that will not decompose into behaviours stalls. The trial shows this is real. The loop carries the cost, not the sequence (my #6).
- The cheap list: the 28-case list may miss what only a long list finds. My #13's 果而不得已 does not excuse it; the remedy is my #12's reversal — on a witnessed failure, generate more.
- One maker per artifact: the vision becomes a single queue. My #18's 君子盛德容貌若愚 (attributed) does not remove it. That is the price of a method usable in other projects.
- The consequence-stop: an open loop and a person making the call. My #18: 不得其時則蓬累而行 — when the time does not come, drift rather than press.

## How we would know I was right

- Take three requirements from the memory system's 64. Run both orders on each. Count: gaps surfaced in requirement text; gaps surfaced in checks; unit coverage; cases that could not be attached to a unit; cases that contradicted a settled decision.
- If cases-first surfaces the same gaps with fewer unattached cases at the same unit coverage, EJ's order was right and my writing order was wrong. The unattached-case count decides it, and the trial does not report it.
- Second test: plant a violation of the vision's "will not do" and see whether any case and any check fail. If nothing fails, my claim that the loop closes at all three levels is false.
