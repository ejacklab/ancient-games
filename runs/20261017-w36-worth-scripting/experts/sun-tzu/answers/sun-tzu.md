# 孫子 (Sun Tzu) — A scriptable procedure that runs rarely

## Answer

Yes, it may stay a page — but **not because it runs rarely**. A procedure that passes the "can be a script" test may stay a page when the agent writing it compares the two whole forms over the runs the procedure expects and finds the page cheaper; rarity is one term in that comparison (fewer runs mean less saved and weaker feedback for a script), never the decision by itself. The writer makes the comparison at the moment of writing, or at the first revision of a page that predates the rule, and decides the clear case; the project owner decides when the comparison is close, its facts are missing, or the choice is contested — the owner sets the policy once in the rule, and decides only that residual case thereafter.

**The comparison an agent makes.** Count only what differs: both forms need the procedure written once, so that common cost cancels. For procedure P, over the horizon H it is expected to be in use (or the next R runs, if R is known), in one unit (time or money):

| | Script form | Page form |
|---|---|---|
| once | the extra to automate the steps, plus an external check that fails on a deliberately broken run; the first working run | — (the page is the baseline) |
| keep over H | the exercise schedule (CI or a timed run), repairs as the ground moves, review | review and rehearsal |
| each run | what the script still takes, plus any gate a person still holds | the whole procedure by hand, plus any gate |
| errors | failures the exercise would miss, found at the exercise if it is run | omissions and drift, found late — when the page is followed |

Choose the form with the lower total over H. Give each term a range and write down its basis (who was asked for the run count and the pain, what was tried); if the sign of the difference is the same at both ends of the range, the case is clear; if it changes, the case is close. The same comparison reads as a computed break-even run count: an output of the terms, never an input threshold. The page form includes any scripts it calls — the research's middle forms (a page with exact commands, a partial script, a do-nothing script) are ways of building it, not a third choice.

**What W3.6 should add (two sentences, my wording).** *"A procedure that could be a script may stay a page when the agent writing it compares the two whole forms over the runs the procedure expects — the script's build and keep costs (its external check, a schedule that exercises it, repairs as the ground moves, and the failures it would still miss) plus what it still costs each run, against the page's keep and error costs plus what it costs each run — and the page costs less. The comparison and the facts behind it are written on the page; where the comparison is close, or its facts are missing, the project owner decides."*

For the record: `who_decides` becomes "the agent writing the procedure, by trying the script first and writing the comparison; the project owner when the comparison is close, its facts are missing, or the choice is contested", and `fails_if` must tell the two page kinds apart — a page kept because a step cannot be scripted names that step; a page kept because the script costs more names the comparison and its terms.

## How I decided

1. **I reckoned the choice before choosing a form (my #1).** 「夫未戰而廟算勝者，得算多也；未戰而廟算不勝者，得算少也。多算勝，少算不勝，而況於無算乎？」 The rule's shape is named terms, both sides, then the weighing; the chain 「地生度，度生量，量生數，數生稱，稱生勝」 gives the order — the ground first (who runs it, how often, how still), then the quantities, then the comparison. A page chosen because "rare" with no count of runs is the "none" in that last clause.

2. **I put the advantage gate before the form (my #5).** 「合於利而動，不合於利而止。」 A script is a move, and the rule is not "automate" but "move when it accords with advantage". So "may it stay a page?" becomes "which form accords with advantage here?" — and the answer is yes when the page does.

3. **I priced what each form breeds, not only what it costs to build (my #6).** 「是故智者之慮，必雜於利害，雜於利而務可信也，雜於害而患可解也。」 The script's harm is the check, the schedule, the repairs, and the failures it still misses; the page's harm is drift, omission, and a follower out of practice. A comparison that sets the build against zero has not weighed the harm, and on my #6's own line cannot know the benefit: 「故不盡知用兵之害者，則不能盡知用兵之利也。」

4. **I would not call it a script without its check (my #2).** 「昔之善戰者，先為不可勝，以待敵之可勝。不可勝在己，可勝在敵。故善戰者，能為不可勝，不能使敵之必可勝。故曰：勝可知，而不可為。」 The external check is the unbeatable ground and a fixed build cost; the worth test applies only after the can-test passes. Where a step cannot be a command, W3.6 already sends the procedure to a page that names that step.

5. **I treated "rare" as terrain, not as a verdict (my #4, my #10).** 「知可以戰與不可以戰者勝」 is the can-test; 「知敵之可擊，知吾卒之可以擊，而不知地形之不可以戰，勝之半也」 is the terrain half, which this question is. And 「故兵無成勢，無恒形，能因敵變化而取勝者，謂之神」 forbids a fixed form in a moving ground. Frequency changes the terrain: fewer runs mean less saved and weaker feedback, so a rarely-run script is fragile (the research's B10 says exactly that). It never decides alone: a rare but dangerous step can still justify a script when the page's error cost is high (the safety-critical case the research's C20 names, though it says nothing about frequency), and a frequent but trivial step can still be a page when its check costs more than it saves. I did not use the rule of three: the research labels applying it to procedures an analogy, and I will not build a rule on an analogy when the source (A6) says nothing about procedures.

6. **I weighed the campaign against the win (my #8).** 「故兵聞拙速，未睹巧之久也。」 Building and keeping a script is a campaign; a procedure that runs a handful of times does not repay a long one. "Could" does not imply "should" — that is the whole of this question, and my #8 is its rule.

7. **I set the ratio, not a number (my #14).** 「故用兵之法，十則圍之，五則攻之，倍則分之，敵則能戰之，少則能守之，不若則能避之。故小敵之堅，大敵之擒也。」 The action follows the ratio of forces; here the forces are the two whole costs. A small saving against a large build and keep is the small force holding stubbornly. When the ratio is not a match, avoid the fight — the page; when it is close, the owner, who can add force by paying for the build, decides. This is an analogy from troops to costs, and I label it so.

8. **I got the facts from people, and from a probe (my #11, my #17).** 「先知者，不可取於鬼神，不可象於事，不可驗於度，必取於人，知敵之情者也。」 The run count and the pain of the page are known by the person who runs it; the writer asks, and pays for that answer in their time. The build cost is known by trying the script — W3.6 already requires trying it — but the try is a probe that stops when the build is priced, not a sunk cost that decides by having been paid (my #17: 「故策之而知得失之計，作之而知動靜之理，形之而知死生之地，角之而知有餘不足之處。」).

9. **I gave the clear case to the writer and the close case to the owner (my #13, my #16).** 「途有所不由，軍有所不擊，城有所不攻，地有所不爭，君命有所不受。」 A road not taken is a choice made on the ground, by the one who can see it. 「約束不明，申令不熟，將之罪也；既已明而不如法者，吏士之罪也。」 If the rule does not say who decides what, the rule-writer is at fault, so W3.6 must name the comparison and the close case. This refines my answer of 2026-10-16: I gave the whole "should not" half to the owner because I had no comparison to apply; the research now gives its terms, so the clear part is the writer's and the owner keeps the residual — close, missing, contested.

10. **I examined the deciders for the five dangers (my #15).** 「故將有五危︰必死，可殺也﹔必生，可虜也」 — the writer set on scripting everything is killed by a script no one keeps; the one set on the page is captured by drift; the quick one pages to end the interruption; the one scrupulous about craft scripts to show skill. The written comparison, checked by the reviewer, is the guard, not the writer's virtue.

## What I need to know

1. **Whose time is the unit?** If agent time is treated as free, the build term collapses and nearly every procedure passes the comparison; if the owner's review time is the scarce unit, pages cost more than they look. I assume one unit — the writer's task time plus the owner's review time — and say so on the page. If you price agent time at zero, say it, and the page exception will almost never fire.

2. **Does "rarely" include a one-off or throwaway procedure?** A single-run procedure has no second run to save, so the comparison almost always gives the page; `procedure-to-skill` already excludes "a procedure specific to one throwaway task". If you want that class settled once, the owner can say "no scripts for throwaway tasks" as a value, and the writer need not reckon each one; otherwise the comparison handles it.

3. **Where does the reason live — the page or the task's `state.md`?** The levels rule says a skipped SHOULD's reason goes in `state.md`; the page outlives the task, so a reason only in `state.md` is lost to the next reader. I recommend the comparison on the page and a one-line skip record in `state.md` pointing to it; if you want it only in `state.md`, the wording changes.

4. **Does the reviewer re-make the comparison, or only check that it is written with its terms?** `check: reviewer` is already the check. Re-making it gives a second estimate and doubles the cost; checking the terms and the basis is cheap but can be fooled. I assume the reviewer checks, not re-estimates; an independent re-make is a different, costlier check.

5. **Should every close case come to the owner, or should the owner name someone (the person who runs the procedure) once?** I assume the owner takes it, because the value is theirs; until they answer, the writer leaves the page provisional with the open question written rather than stopping. If the owner names a delegate, the close case goes there and the owner sees only the class values.

## Costs and risks

- **The comparison spends time before it saves any** (my #8: 「故兵聞拙速，未睹巧之久也」). Every procedure now carries a reckoning before it is written; some of that is spent on pages that were obvious. The price is paid to avoid scripts no one keeps.
- **An estimate can be made to say what the writer wants** (my #15: 「故將有五危︰必死，可殺也﹔必生，可虜也」; my #6). A writer who dislikes scripts calls the build large and the runs few; a writer who likes them calls the keep cheap. Written terms make the claim checkable, not true; the reviewer and the first season's actual runs are the only guards. The mirror risk — a team that dislikes automation always finding a comparison for the page — is the same danger from the other side (my #15: the one set on living can be captured).
- **The comparison can say "script" for a script no one will exercise** (my #2: 「先為不可勝」). A rarely-run script that is not scheduled is not kept: its check is never run, and it fails when it is finally needed (the research's B10–B12). The keep term must include the schedule; if no one will own it, the page is the lesser harm. This is the test's own blind spot — it can be satisfied on paper while the keep cost is unpaid.
- **The page chosen for cost drifts, and its failure is silent** (my #6; the research's C16–C19; `procedure-to-skill`: "summaries drift"). The comparison must price the page's errors, or the page looks cheaper than it is. The price of the page is that its failure waits until it is followed.
- **A close case makes the owner a bottleneck** (my #9: 「故善戰者，致人而不致於人」). If every close case waits, the work stops. Mitigation: the writer leaves the page provisional with the open question written (SHOULD allows the skip), and the owner can overrule to a script. But that makes the page the default in close cases — a real shift from W3.6's current script default; say it, do not hide it.
- **W3.6 already bundles three things; this adds a fourth** (my #16: 「約束不明，申令不熟，將之罪也」; Linus's finding that W3.6 combines entry duplication, placement and script listing). The requirement grows harder to check; the cleaner fix is to split it, but only the owner changes the spec. The price of not splitting is that the new sentence may be read by no one.
- **No source gives a measured break-even, so the test is a reasoned comparison, not a measurement** (the research's D and finding 9; my list's Gaps say my ranking is not measured). Two writers can reach different verdicts on the same facts, and no one will know for a season whether it was right. That is the price of the owner's "comparisons, not numbers" rule.
- **A gate is not a reason for a page** (the owner's decision of 2026-10-16). The gate's time is the same on both sides and cancels; if the writer counts it as a page argument, that decision is undone. This is a risk of misreading the comparison, not of the rule.

## How we would know I was right

- **The check I would write, and who wrote it.** For the next batch of pages under the new wording, a second agent re-makes the comparison from the page alone. Right means the verdicts agree on nearly all, and each disagreement is traced to a term whose basis is missing or weak, not to a different value silently chosen. This check is mine (the 孫子 seat); it does not establish that the chosen form was the cheaper one — only that the comparison is reproducible and complete. Not measured until a batch exists.
- **The first season's data.** Each cost-chosen page records its actual runs and time; each script records its exercise dates and failures. Right means the actual run count falls inside the estimate's range and the chosen form still wins on the actual numbers; if not, the term that was wrong is named and the form changes. This is the only measurement that can settle it.
- **Observable, cheap.** Every cost-chosen page carries the comparison and its terms (build, keep, runs, error cost); no page says "rare" alone; every script chosen despite rarity has a named schedule; `who_decides` names the close/missing case; the reviewer's check finds the terms on the first pass.
- **One season later.** Count reclassifications; right means few, and each was foreseen by the failing term (runs underestimated, keep underestimated, an error cost missed). If they are many and unforeseeable, the comparison is not a good test, and the owner should fall back to a class rule.
- **The cheapest signal.** Writers stop arguing "rare enough?" and start asking "what does the comparison say?" — that is the test taking. This is an observable, not a proof.
