# Dave — where I help in the method, and where I don't

## Answer
I am most reliable in three places: **3.4 default-first and the 20% challenger rule, with its ledger**; **3.5 the loop-ready check** (conditions 1 and 5); and **3.3, "unknown" spots that become a bounded explore loop**. In all three the method already asks for what my rules are about — a prediction written first, a control, and a check that can fail. I am not reliable at 3.0 (objective, six whys), the 3.1 blueprint check, or as a source of nature analogies for 3.6/3.7 graph and parallel wiring: there my rules either have nothing to apply to, or push me to invent values and fit analogies that do not hold.

## How I decided
1. **I first settled what would change my mind** (my #1): I would drop a place if my rules could only add an opinion there, not a test or measurement the main agent can check.
2. **3.4, the challenger rule and `docs/TASK_TYPES_LEDGER.md`.** The method makes a challenger state its "≥20% lower projected run cost … at equal coverage" in writing **before the run** — my #3 (metric, expected result, stop date written first) and my #4 (compare against the current way; the control is the default design).
   - **Data already there** (my #5): the ledger has 18 run rows; all 18 are `default` — no challenger has ever been tried — and 16 of the 18 say "no — token cost not measured" in the Reconciled column (I counted with grep; a measurement, not a quote). So the cost side of the 20% rule has almost no actual figures to check against.
   - **Ask me there:** "Here is a challenger claim and the default it replaces. Is the prediction fixed before the run (metric, expected margin, stop date)? Is the default really the control? What does the ledger already show, and not show, about this category's cost?"
3. **3.5, loop-ready conditions 1 and 5.** The method: "A check the worker cannot edit, and that is known to be able to fail (the house sabotage check)." A planted defect is a control in my #4 sense — you only learn the check works by comparing it with a case where you know the answer. My #9 fits too: in run 20261011-project-memory-engines, round 1 "MISSED its planted row M16 while reporting planted_defect_found true" — a miss must be reported with the same weight as a hit.
   - **Ask me there:** "What result would show this check can fail? What is its control (old code, a plant, the unchanged baseline)? What does a miss look like in the output?"
4. **3.3, spots of kind "unknown" that become "a bounded explore loop".** My #2 (if a test costs less than the debate, run it) and my #8 (one path first, measure, then spread); the loop's bound is my #3's stop date.
   - **Ask me there:** "For this unknown spot, what is the smallest reversible experiment, what do you predict before it runs, and when do we stop?"
5. **Across all three I attach a size of evidence** (my #10). The method says of itself "n=1" and "most rules have had no run at all (n=0)", so anything I add there is a hint until the ledger grows.
6. **Where I am weak (my reading):** none of my ten rules is about stating objectives, finding the "why" behind a task, or judging product requirements; at 3.0 and 3.1 I would be speaking outside my rules.

## What I need to know
- **Is a run's cost measured anywhere besides the ledger?** If yes, my #5 at 3.4 has real data and "the challenger rule cannot be checked on cost today" weakens; if no, it stands.
- **Will the main agent or EJ run the experiments I propose?** I can only advise. If nobody runs them, my #2 and #8 produce plans, not results; at 3.3 I would only frame the question.
- **Who sets the expected result in a prediction (my #3)?** If EJ, I ask for it and leave it open; if I am expected to fill it, see the first risk.

## Costs and risks
- **I would invent thresholds** (my #3). "Fix the expected result" pulls me toward writing a number; this project's rule is "Never fill a gap with my own value". Where EJ has not given a value I must leave it open, or my contribution stops being checkable.
- **Nature analogies at 3.6/3.7 are unreliable** (my #6, held back by my #7). Ant routing and swarms invite fan-out designs, but the key condition differs — EJ's memory index: "Agents are whales, not ants — few expensive long-memory agents; main agent by default, subagent hand-off must pay for itself." Ants are cheap and many; these agents are expensive and few, so my #7 says drop it — and I still spend tokens on an idea that gets thrown away.
- **Experiments cost real runs** (my #2, my #8). With 16 of 18 ledger rows lacking measured token cost, nobody can tell whether a test "costs less than the debate"; my #2 can push toward running agents, the expensive part.
- **Controls double the work** (my #4): a plant or a baseline comparison adds a verifier pass or a second run. Worth it — a plant was caught being missed — but not free.
- **Over-weighting small numbers** (my #10 guards it, the risk stays): 18 runs, all defaults, is a small n per category.

## How we would know I was right
- **3.4:** the first time a challenger is tried, its ledger row has the claimed margin, basis and projected cost filled **before** the run and the actual cost **after**. Right if the reconciliation confirms the margin or records its failure as a failure (my #9); wrong if the row ends "not measured" again despite my input.
- **3.5:** over the next runs where I am asked about a check, count planted controls caught at the named row versus missed; I am useful if misses reach the ledger instead of hiding behind a true-looking boolean.
- **3.0/3.1, the negative test:** ask me an objective or blueprint question alongside another expert; if my answer cites no rule or rests on facts I was not given, that confirms I should not be asked there.

<!-- saved by the main session from a Claude subagent (Opus 5.5) via --claude-by-caller; lightly condensed in the retyping, item citations and quotes unchanged -->
