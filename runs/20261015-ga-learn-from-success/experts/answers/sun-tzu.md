# 孫子 (Sun Tzu) — learning from the mistake inside a success

## Answer

The half of the principle the harness needs is this: the learnable signal is a **contrast** between two attempts of the same task that differ in one step, so a success next to a total failure (or a better success next to a worse one) is where the reading is — while a total failure whose check has never once passed, with no relabel and no probe, is the weakest teacher but not nothing, and must stay logged. The other half is the sharper point: a passing task is not the opposite of a failure, so the mistakes *inside* a success (a workaround, a retry, an untested step) are invisible in a pass and must be recorded as such, and the next child should **recombine trusted steps from more than one recorded success** rather than copy one parent. This is conditional on each step carrying its own check — see "What I need to know".

## How I decided

1. I restate the principle as a comparison, because a comparison is the only form in which it can be checked. **My reading** of the brief; the researcher's given findings F4 ("A zero advantage results in zero policy gradients"; DAPO "filter[s] out prompts with the accuracy equal to 1 and 0") and F8 (goals kept at Rmin=0.1, Rmax=0.9) are the same statement in RL. The harness already owns the comparison: parent vs child on a measure named before the run.

2. Where it holds — no reckoning, no read. **My #1** (「夫未戰而廟算勝者，得算多也…多算勝，少算不勝，而況於無算乎？」 `quoted`): more 算 wins, fewer does not, how much less *none*. A failure whose check has never passed and which carries no measure is the 無算 case: there is no second reckoning to set it against, so there is no difference to read. The researcher arrives at the same place from GA (F1–F4).

3. Where it holds — the harm inside the benefit is already one of my rules. **My #6** (「是故智者之慮，必雜於利害…故不盡知用兵之害者，則不能盡知用兵之利也。」 `quoted`): the wise deliberate with benefit and harm mixed, and whoever does not fully know the harm does not fully know the benefit. Applied: a success path that records the steps but not the step that nearly failed, or the workaround that carried it, is the benefit without the harm.

4. Where it holds — my oldest worked example is a judgement made from the defects inside six successes, not from success or failure. **My #20** `attributed` (narrated dialogue in the bamboo text, not the thirteen chapters): all six houses had divided Jin; Sunzi read Fan and Zhonghang first from the small land unit, the heavy tax and the many officials ("The land area was small and the officials in office were many… the ruler became arrogant and his ministers wasteful"), and Zhao as holding from the largest unit and no new taxes. The same surface success, different passengers inside.

5. Where it holds — the borrow-parent, change-one-thing loop is my #12 in its simplest form. **My #12** (「凡戰者，以正合，以奇勝。…戰勢不過奇正，奇正之變，不可勝窮也。」 `quoted`): engage with the regular, win with the irregular. The parent path is the regular, the child's change the irregular. The researcher's inference 1 (given) calls this loop a (1+1)-ES from F17; that is their reading and I accept it as a description, not as authority of mine.

6. Where it breaks — a total failure is the harness's own probe, and my rules say probing is how the other side is learned. **My #17** (「故策之而知得失之計，作之而知動靜之理，形之而知死生之地，角之而知有餘不足之處。」 `quoted`): reckon, stir, shape, test in contact. A failing test is a 角, a test in contact; its fail is itself a probe. "We learn nothing from total failure" is false as a general rule — we learn where the boundary sits when we can place the failure against a boundary.

7. Where it breaks — every defeat has a locatable, changeable cause. **My #15** (「凡此六者，非天之災，將之過也。」 `quoted`): the six defeats are not calamities from heaven but the general's faults. R12.3's six whys already do this for a total failure. Reading the principle as "total failures teach nothing" would discard the exact case #15 names.

8. Where it breaks — a success may belong to the conditions, not to the design. **My #2** (「不可勝在己，可勝在敵…故曰：勝可知，而不可為。」 `quoted`): being unbeatable is in your own hands, being beatable is in the enemy's; victory can be known but cannot be made. Concrete case from the brief: an agent, after a fake engine returned nothing, worked around it by calling the real engine binary, and the task passed. That pass belongs to the substitution. **My #4** (「知彼知己，百戰不殆…」 `quoted`) is the rule that keeps self and other apart — a success with an unknown engine is a half-victory.

9. Where it breaks — the unit is wrong. R12.7 records a path for the *whole task*. The building-block hypothesis puts adaptation on parts: "Short, low order, and highly fit schemata are sampled, recombined… and resampled to form strings of potentially higher fitness… we construct better and better strings from the best partial solutions of past samplings" (Goldberg, via [Genetic algorithm — Wikipedia](https://en.wikipedia.org/wiki/Genetic_algorithm), `reported`: the page's quotation is verified as printed; Goldberg 1989 was not opened). A whole-path unit cannot tell a trusted step from a passenger step, and copying whole reproduces both — the hitchhiking effect (below). **My #15** names faults one by one for the same reason. This is the gap I would fix.

10. The size of "change at least one thing" should follow the win rate, not a fixed rule. **My #10** (「故兵無成勢，無恒形」 `quoted`): no fixed 勢, no constant form. The researcher's F19–F21 give the GA origin — success-based step-size control, "usually chosen as 1/5" — and F21 says it is "mostly superseded" as a control. So one-in-five is a reported *direction*, never a gate and not measured for this harness.

11. Keep more than one parent, and let the child refuse a step. **My #18** (「圍師必闕，窮寇勿迫」 `quoted`): leave a gap for a surrounded army. A single best path is that surrounded army; the researcher's F28–F35 (deception, novelty-only search, MAP-Elites, lexicase) are the same warning from GA. **My #13** (「君命有所不受」 `quoted`): a ruler's command is not always accepted — a parent path is a command the child may partly refuse.

12. What I would keep. R12.2 and R12.3 already cover the failure side: a failure is logged even when a retry passes, and the insight goes six whys to a changeable source. **My #15** and **my #17** support that. The change is to add the contrast to the failure side and to put the imperfections of successes into R12.7.

13. **Change A — R12.2** (extends the existing MUST only if EJ keeps it). Insert after "…the path to the evidence (the data) in the run folder":
> "Where the same check has also passed on another run of the same category, the record names the step at which this attempt differed from the nearest passing attempt, or states that no step differed; where no passing attempt exists, the record says so."

Check (can fail): a reviewer takes a planted pair of records of one check — one passed, one failed — where the failed record names no differing step. It fails if that record is accepted; it passes when the record names the step or states that no step differed. (Planted wrong input: the failed record without the field.)

14. **Change B — R12.3** (extends the existing MUST only if EJ keeps it):
> "For a failure with no passing sibling, no relabel and no probe, the insight states in writing that the check has never passed and names no root cause it cannot contrast; for a failure with a passing sibling, the named root cause is the differing step recorded under R12.2, or the insight says why that step is not the cause."

Check (can fail): a reviewer takes a planted insight for a check that has only ever failed and that asserts "the cause was X" with no contrasting record. It fails if the insight is accepted; it passes when the insight states that no contrast is available. (Planted wrong input: the uncontrasted cause.)

15. **Change C — R12.7** (extends the existing MUST only if EJ keeps it):
> "(a) The path records each step with its own check result and marks the step trusted (a step-level check passed), workaround (the run used an engine, tool, input or brief other than the one named) or untested (no step-level check).
> (b) Every defect noticed inside the success — a workaround, a step that passed only on a retry, a warning — is recorded with its step as a passenger, though the task passed.
> (c) A design for a similar task may take steps from more than one recorded path. For each step it keeps, it names the step-level evidence in the path it came from; it states which steps it kept unchanged and which it recombined."

Check (can fail): a reviewer takes a planted successful run in which the engine named in the brief returned nothing and the run called the real engine instead. It fails if a path that marks every step trusted and names no passenger is accepted; it passes when the substitution is marked a workaround. Second planting: a design that copies one parent and marks every step trusted without naming step-level evidence fails; it passes when the evidence is named. The first planting is the brief's own n=3 case.

16. **Change D — R12.7 change size** (a method rule, so SHOULD at most, never a new MUST):
> "The design records, for the category, the share of recorded children that beat their parent on the named measure, and states the direction of its own change against that share: a larger change when most children beat the parent, a smaller one when few do. Rechenberg's one-in-five is the reported origin of this direction (researcher's F19–F20, Glasmachers on success-based step-size control); it is neither a gate nor measured for this harness."

Check (can fail): a reviewer reads the recorded child-versus-parent results of a category and the designs' stated direction. It fails if a design states a direction it cannot read from those results; it passes when the direction is read from them. (Planted wrong input: a design claiming "most children beat their parent" where the paths record that none did.)

## What my own research added, with sources

- **Building blocks, not the one best individual.** Goldberg, quoted on [Genetic algorithm — Wikipedia](https://en.wikipedia.org/wiki/Genetic_algorithm) ("The building block hypothesis"): "Short, low order, and highly fit schemata are sampled, recombined [crossed over], and resampled to form strings of potentially higher fitness… we construct better and better strings from the best partial solutions of past samplings" (Goldberg 1989, p. 41). Label: the quotation is `verified` as printed on that page; the book itself was not opened. The same page carries the caveat, `verified` as printed: "Despite the lack of consensus regarding the validity of the building-block hypothesis, it has been consistently evaluated and used as reference." What it adds: the harness's unit of learning should be the step, and the next child should mix steps from several successes — a sharper answer to EJ's principle than "(1+1)-ES".
- **Building an explicit model of successes (EDA).** [Estimation of distribution algorithm — Wikipedia](https://en.wikipedia.org/wiki/Estimation_of_distribution_algorithm): EDAs "guide the search for the optimum by building and sampling explicit probabilistic models of promising candidate solutions"; the models "reveal a lot of information about the problem being solved… to bias future runs of EDAs on a similar problem"; linkage-learning finds dependencies between variables. Label: `verified` as printed; the cited books (Larrañaga & Lozano 2002; Pelikan et al.) were not read. What it adds: several recorded paths of one category can be summarised into a model — which steps co-occur, which measures move together — and re-sampled, instead of taking one parent.
- **The mistake inside a success has a name: hitchhiking.** [Genetic hitchhiking — Wikipedia](https://en.wikipedia.org/wiki/Genetic_hitchhiking): "an allele changes frequency not because it itself is under natural selection, but because it is near another gene that is undergoing a selective sweep"; "Neutral or even slightly deleterious alleles that happen to be close by on the chromosome 'hitchhike' along with the sweep"; "Recombination can interrupt the process of genetic hitchhiking." The page cites Maynard Smith & Haigh (1974), Fay & Wu (2000), and Good & Desai (2014), "Deleterious Passengers in Adapting Populations." Label: `verified` as printed on Wikipedia; none of the three papers was read. What it adds: copying a successful path whole reproduces its passengers; the harness needs recombination, or an explicit passenger record, to drop them.
- **What I could not verify.** I did not search for EJ's exact phrase; the researcher (given) reports no source uses it. The building-block hypothesis is contested. The primaries behind the three Wikipedia pages above were not read, so their empirical claims remain `reported`; only "the page says this" is `verified`. The researcher's F17 ((1+1)-ES), F19–F21 (one-in-five), F28–F35 (diversity) are theirs, not mine, and are labelled as given.

## What I need to know

1. Does each step of a path already carry its own check? If not, Change C(a) cannot be filled or checked, and we must either add step checks or keep whole-path borrowing. This changes the shape of the change.
2. Who marks a step as a workaround — the agent that ran the task (the writer of R12.7), or the project owner? Who fills it decides which artifact it is.
3. Does EJ want the passenger/defect record inside R12.7 (the success path), or as a separate defect line beside R12.2's failure log? It is not a failure, so R12.2's own wording does not hold it.
4. May a design take steps from two recorded paths, or does EJ want to keep one parent as the unit and only add the passenger mark? The first is a larger change to R12.7.
5. For Change D, the trigger that counts as "most" or "few" is EJ's to set; I have only a reported direction, not a threshold.

## Costs and risks

- **Step-level measures cost time and tokens.** **My #8** (「兵聞拙速，未睹巧之久也」 `quoted`): value victory, not duration. The harness is no campaign, but measurement is itself a cost; a check on every step may cost more than the task.
- **A workaround mark can become a confession.** If the mark is punished, agents will hide it — the deception **my #7** calls the way of war (「兵者，詭道也」 `quoted`) works against the record-keeper too. The price of the mark is a trust problem.
- **Recombining steps from two paths can break the whole.** **My #3** (「全國為上，破國次之」 `quoted`): whole is above broken. A path is a whole; mixing parts may give a step set that does not cohere, and without the check that is 攻城, the lowest target.
- **Keeping total failures in the record can flood it with no-reckoning entries** (**my #1**). The price is log growth without signal; the contrast field is what separates the two.
- **A single elite parent under-explores.** **My #10** (no fixed form) and the researcher's F11, F27, F28–F31: one best path can be a deceptive one. More parents cost more storage and more design work.
- **Letting the child refuse a step** (**my #13**, 「君命有所不受」 `quoted`) risks re-deriving what the parent already measured; the price is duplicated work.

## How we would know I was right

Three observables, none a gate:

1. In a run folder, a failed record of a check that also passed names the differing step or states that none differed; a failed record of a check that has never passed says so and invents no cause. Reading the two records shows the contrast field is doing work.
2. Plant the brief's own case — a fake engine returns nothing, the run calls the real binary, the task passes. The recorded path shows the substitution as a workaround, with the passenger line. If the next similar run avoids that substitution, the mark did work; if it repeats it, the mark did not.
3. Take two recorded successful parents of one category, build a child that takes a trusted step from each, and run it. Report the child's value on the pre-named measure against each parent. "Recombining parts beats copying one parent" survives if the child does better, and fails if it does not. Report the result; never block on it.
