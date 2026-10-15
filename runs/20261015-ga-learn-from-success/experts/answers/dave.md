# Dave: learning from mistakes inside successes, not from total failure

## Answer
The principle holds for this harness in a narrower form. The useful signal is the contrast between a failing attempt and a passing attempt of the same task, so failures inside a successful task (near misses) are the ones most worth an insight. It does not hold in its strong form, that a total failure teaches nothing. A GA's fitness is one number, but a harness failure comes with an error text and evidence, so the key condition differs (my #7).

My proposal is conditional:
- **R12.2:** keep it unchanged.
- **R12.3:** add a near-miss / total-failure label and the contrast each one learns from.
- **R12.7:** make every path list the mistakes inside it.
- **R12.7, only if EJ will pay for one repeat run per parent:** a child becomes a parent only when its gain is bigger than the parent's own run-to-run spread.

## How I decided

1. **What would change my mind (my #1).** Take insights that have a fix and a planted-repeat check (R12.3). If fixes from total-failure insights pass that check as often as fixes from near-miss insights, the principle does not carry over and R12.3 should stay as it is. If near-miss fixes pass clearly more often, it carries over.

2. **The data we already have (my #5).** The one recorded parent path, `runs/20261015-learn-success/success-path.yaml`, has `failures: 4` and `successes: 1` under `measures`, and a `failures:` list (R12.1-missing-output, R12.2-test-failed, R12.2-command-error). So the first parent is itself a success with mistakes inside it, which is the case EJ remembers.
   - What this shows: near misses happen and the YAML already records them.
   - What it does not show: whether insights on them lead to better fixes. That is not measured; n=1 path.
   - The n=3-per-arm test (claude-haiku, one task) found few mistakes of the agents' own. Total failures of whole tasks look rare here, so how much they matter is not measured.

3. **Where the principle holds, with cases (my reading, from the researcher's F1–F9, F48–F50).**
   - **Case 1, a failure that has a passing sibling.** Today a test failed during coding and then passed after a change. The failed attempt and the passed one differ in one place, which is a "near miss" (F50, Winston; reported). Active CMA and Michalski's LEM also use the worst only in contrast to the best (F48 reported, F49 verified).
   - **Case 2, all-pass or all-fail gives no spread.** A check that only ever passes teaches as little as one that only ever fails: DAPO drops prompts at accuracy 1 as well as 0 (F4, verified). R12.7's success lines make this visible for the first time, because a check's failures can now be read against how often it ran.
   - **Case 3, a success that hides a mistake.** Today an agent got an empty result from a fake engine and called the real engine binary instead. The task looked successful, but it went around a planted control. If that run became a parent, the bypass would be copied into its children. This is the "mistake inside a success" in its sharpest form, and today R12.7 does not ask a path to record it.

4. **Where it breaks, with cases (my #7, analogy check).**
   - **Same as GA:** parent, change, select (the (1+1)-ES, F17 verified).
   - **Different, and it matters, point 1: the failure signal.** In a GA a total failure is a fitness of zero with no gradient (F1, F3). In this harness a total failure comes with an error message and evidence, and an LLM agent can reason from that text. Reflexion is built on that idea (F47, reported: 91% vs 80% pass@1 on HumanEval, abstract only).
   - **Case 4, a run that failed as a whole and still taught something.** The 2026-09-19 planning-decision run ended `plan_rejected`, and it is what exposed two wrong state-file claims (from the project's memory notes; I did not re-read that run).
   - So total failures stay logged and analysed. I would not weaken R12.2.
   - **Different, point 2: the noise.** A GA scores thousands of variants and ES scores many offspring. Here there is one child per task, run on an LLM engine that varies from run to run. At n=1, "the child beat its parent" may just be noise (my #10). That is my reading; the spread is not measured. One example of the risk: the parent's `minutes_to_merge: 8`, and a 2% change on that is about 10 seconds.

5. **How nature solves it (my #6), from my own research.**
   - **Germinal centres in the immune system.** B cells mutate, then compete for survival signals; cells with lower antigen affinity are deleted, and selected cells "may also restart the whole cycle". This is the same as borrow a parent, change it, select, borrow again.
     - What is different: the body selects among many variants at once. The harness has one child per task, so the condition "selection among many" does not hold and selection here is noisier. That supports the noise check below.
   - **Dopamine and prediction error.** Learning "is blocked when the stimulus is paired with a fully predicted reward", and it happened mainly when there was "a reward prediction error" (Waelti, Dickinson and Schultz, Nature 2001; abstract only).
     - What carries over: a success that was predicted teaches little, and so does a failure that was predicted. R12.2's expected-vs-actual field and R12.7's prediction written before the run already capture this. The mechanism fits, so I would add nothing.
   - **Ant colonies (MMAS).** Only the best tour deposits pheromone, but evaporation "avoid[s] the convergence to a locally optimal solution", and a minimum bound keeps other trails alive.
     - What carries over: R12.7's "every path stays recorded" is the minimum bound. There is no evaporation yet. The risk is that the agent keeps proposing the same single elite path. That matches the researcher's F11 and F27–F31, where pure elitism under-explores and deceptive problems trap the single best.
   - **Aviation incident reporting (NASA ASRS).** It collects voluntary "safety incident/situation reports … to lessen the likelihood of aviation accidents". In other words, people learn from the events that did not become accidents, which is the near-miss idea at an institutional scale.

6. **R12.2: no change proposed (my #9).** It already says "A failure is logged even when a retry later passes", which is exactly what captures a near miss. It also records expected vs actual, which is the prediction error. Narrowing it to near misses only would drop exactly the cases in step 4, so I propose nothing new here.

7. **R12.3: proposed text (proposed, not EJ's).**
   > For each failure, the insight says which kind it is — a **near miss** (a later attempt at the same step, or the task, passed) or a **total failure** (nothing in the task passed it) — and names the contrast it learns from: for a near miss, what differs between the failing attempt and the passing one; for a total failure, the nearest recorded path of the same category and the first step where this run departed from it, or that no such path exists.

   - **Fails if:** an insight gives a failure no kind; a near miss names no difference; a total failure names neither a nearest path nor "none exists".
   - **Planted check:** an insight file with a near miss whose difference is left blank must be flagged.

8. **R12.7: proposed change A (proposed). Record the mistakes inside a success.** Add to the path's required fields:
   > the failures recorded during the task (R12.2), and every step done other than as designed (a workaround), with what it went around

   - **Fails if:** a path lists fewer failures than the session's failure log holds for that task; a step whose engine or binary differs from the design is not listed as a workaround.
   - **Planted check:** a session log with 3 failures and a path that lists 2 must fail. A path containing today's real-binary workaround with no workaround line must fail.
   - The current YAML already has a `failures:` list, so this mainly makes an existing practice a requirement.

9. **R12.7: proposed change B, only if EJ accepts the cost (proposed; my #4, #10). Measure noise before naming a parent.** Replace "A child that improves on its parent's value … becomes a parent" with:
   > A child becomes a parent when its gain over the parent's value is larger than the parent's own run-to-run spread on that measure (two runs of the parent, same task); until the spread is measured, the child is recorded as *improved, not confirmed*.

   - This is a comparison, not a threshold (house rule). It decides only which path becomes a parent. It never blocks or discards work, so the 2% stays an aim.
   - **Fails if:** a child is marked as a parent with no spread recorded, or with a gain no bigger than the spread.
   - **Planted check:** a child whose gain is smaller than the recorded spread, marked as a parent, must be rejected.

10. **A smaller option I would only note (my reading, ACO and MAP-Elites).** When more than one recorded path matches, the design names the one it borrowed, lists the others, and says why it chose that one. **Fails if:** a design names one parent while other matching paths exist and are not listed. I rank this below A and B because only one path exists today.

11. **What my research added beyond the researcher's file.** The germinal-centre cycle, the dopamine blocking result, ant-colony evaporation and bounds, and aviation incident reporting, as listed in steps 5 and 6. Nothing else came from my own research. I did not re-check the researcher's 50 findings; I rely on their labels.
   - [Wikipedia, Affinity maturation](https://en.wikipedia.org/wiki/Affinity_maturation): quotes "bind antigen with lower affinity will be out-competed, and be deleted"; secondary source.
   - [Wikipedia, Germinal center](https://en.wikipedia.org/wiki/Germinal_center): quotes "Selected B cells may also restart the whole cycle of mutative centroblast division and centrocyte selection"; secondary source.
   - [Waelti, Dickinson & Schultz 2001, abstract](https://folia.unifr.ch/unifr/documents/300256): quotes "learning is blocked when the stimulus is paired with a fully predicted reward". I read the abstract only, so this is reported. A secondary page says fully predicted rewards cause no change in firing; I did not verify that in the primary.
   - [Wikipedia, Ant colony optimization](https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms): quotes "Only the global best tour or the iteration best tour are allowed to add pheromone" and "avoiding the convergence to a locally optimal solution"; secondary source, read to character 100000 only.
   - [NASA ASRS overview](https://asrs.arc.nasa.gov/overview/summary.html): the page does not use the word "near-miss", so treating it as near-miss learning is my reading.
   - Could not verify: Scholarpedia "Reward signals" (expired certificate) and Wikipedia "Reward prediction error" (404).

## What I need to know
- **Which GA source EJ learned the principle from.** The researcher found no source with EJ's wording. If EJ meant elitism ((1+1)-ES, F17), R12.7 already covers it and change A is the main addition. If EJ meant "no signal from all-zero fitness" (F1, F3), the R12.3 change matters more.
- **How often tasks here end as total failures.** If almost never, the R12.3 total-failure branch is rarely used and could be left out.
- **Whether EJ will pay for one repeat run per parent** (paid engine calls need their go-ahead). If not, drop change B and report each child's gain as n=1, unconfirmed.
- **Whether "success" means the task or each check.** The near-miss label in R12.3 depends on that.

## Costs and risks
- **R12.3 label (my #9):** more insight fields per failure, about one extra paragraph each. The risk is that an agent labels a failure "total" to avoid naming a contrast, and the planted check catches only the blank-field case. A further risk is that the near-miss framing makes total failures look less important; R12.2's MUST stays, so nothing stops being logged.
- **R12.7 change A (my #4):** a guard check has to match a path's failures against the session log, which is new TypeScript in the guard. Spotting a workaround is not a clean mechanical test: "engine differs from design" catches today's case but not every workaround.
- **R12.7 change B (my #2, #10):** one extra parent run per category, paid, and slower growth of parents, since children wait as "improved, not confirmed". Without it, the risk is that noise gets selected as improvement and the paths drift with no real gain. My reading: this risk is real at n=1, but the spread is not measured.
- **The option in step 10 (my #6, #7):** low cost. Without it, the risk is a single elite path getting copied repeatedly. That rests on GA evidence (F11, F27–F31) and is unmeasured here.
- **Every analogy above (my #7):** GA, immune and ant systems select among many candidates; this harness has n=1 per child, so all borrowed mechanisms are weaker here than in their source.

## How we would know I was right
- **Experiment 1, about the principle (my #3, #4).** Before any results:
  - Fix the measure: the share of insight fixes that pass their planted-repeat check (R12.3).
  - Fix the prediction: near-miss insights do better than total-failure insights.
  - EJ sets the stop date.
  - Arms: near-miss insights vs total-failure insights. Control: insights written under the current R12.3, with no label.
  - Change my mind if total-failure fixes do as well or better (my #1).
  - Use existing insight files first (my #5), which costs nothing. Report the result even if it is null (my #9).
- **Experiment 2, about change B (my #2, #8).** With EJ's go-ahead, rerun the round-5 parent path twice on one feature task and record `minutes_to_merge` and `failures`.
  - If the spread is larger than 2% of the parent's value, a single child's "2% better" cannot be read, and change B is needed.
  - If the spread is smaller, drop change B.
  - One path only, then decide whether to spread it.
- **Planted checks.** Each proposed "Fails if" is shown failing once on its planted input, as described in steps 7–9, before it is trusted.
