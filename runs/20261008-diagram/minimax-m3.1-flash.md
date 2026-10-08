I'll read the diagram and both sources, then answer.
# Review: `docs/ancient-games-algorithm.html`

## 1. Correct? — Mostly. Four things are wrong.

**a) The method's 8th step doesn't exist in the source.** `docs/WORKFLOW_DESIGN_METHOD.md` §3 runs 3.0–3.8. The diagram maps steps 1–7 onto 3.0–3.5 and then folds 3.6 + 3.7 into "Graph" — so **§3.8 ("Running a node: executors are tools, timers, pass-back, no polling") is missing**, and "**Accept** — stop at the criteria, the baseline, and 'must not change'" is invented. That three-part stop condition is real, but it lives *inside* 3.6 as the stop condition of a node that builds — not as a step of its own. So the count "8" is right only by accident.

**b) "fixed rules, no LLM" is false.** SPEC.md §4 tags every step `[spine]`, `[spine+LLM]` or `[LLM]`. Ten steps are LLM judgments: C·5, D·3, D·4, B·2, B·5, E·2, E·3, E·4, A·2, A·3. `ancient_games/stages.py:1` says the [LLM] cells "arrive here as explicit parameters, never computed here" — the referee is rule *code*, but it is fed model judgments. Saying "no LLM" on a page aimed at a newcomer invites the wrong conclusion (that nothing here needs a model).

**c) "Checks the work while it runs" is off.** The referee checks the **plan, before it runs**. Prove's PASS is "plan cleared to `<checkpoint|owner>` gate" (SPEC.md:225). Only Guard can fire at execution time, and only when `execution_status=main_executes` (stages.py:225).

**d) The return arrow lands one node off, and the run is missing.** Prove's findings are Prove's own output — `PASS | RETURN_TO_PLANNER(findings[])`. On RETURN_TO_PLANNER, `hybrid/loop.py:100` swaps the plan for `REPLAN = ("corroborate", "filter_candidates", "prove")` and SPEC.md:218 says the resume is "at C·3" — i.e. the loop is **inside** the referee, back to its own first stage, not out to the Method. There is no "Findings" node that closes into the Method in either source; the real run→method feedback is per-run and goes to `docs/TASK_TYPES_LEDGER.md` (3.4) and `docs/blueprint/lessons.md` (§4). As drawn, the loop skips the only thing that does work.

**Smaller:** "8 steps, **done before anything runs**" contradicts 3.5 — clear pieces run as loops *while* the unclear spots are still being resolved — and 3.1's blueprint pieces run before the design is complete. And 3.4's tiny path (≤3 steps → a prompt file) has **no referee at all**, so the referee is not on every task. Steps 1–7 themselves check out; the stage names and order (Gate, Guard, Corroborate, Filter, Prove) match `DEFAULT_PLAN` at `hybrid/loop.py:25` exactly. One omission inside step 6: the doc's five loop conditions become four — "a check the worker cannot edit, known to be able to fail" is gone.

## 2. Simple and direct? — Yes in tone, thin in substance.

The one-liners are well pitched. For someone meeting this cold:

- "Findings — what held, what broke" describes results of work that hasn't happened. These are the plan's own defects: a claim with no command, an action with no failable check, a metric that doesn't name its true quantity, plus the §8 lints.
- Corroborate is a clause short of the rule: the number required **is** the action's stakes (`n_required = max(stakes, governance row)`), a claim with no cited command is **dropped** (UNVERIFIED), and dispatches are capped at 3 per plan.
- Gate is "how many agents" but has two other exits: RESOLVED (the cheap probe already answered it) and count>3 → split into groups of ≤3.
- Unglossed vocabulary: stop criterion, criteria, baseline, "must not change", candidate, category, blueprint. The method's §5 qualities — **predictability, debuggability, quality control** — are the plainest words in either source and appear nowhere on the page.
- Nowhere does the reader learn where the work happens; the page ends without saying the referee clears a plan for a workflow that then runs.

## 3. One concrete improvement

Add the missing node so the loop closes on real work: `Prove PASS → the workflow runs → results land in the ledger / lessons.md → back into the method` (and fix "Accept" → "Run a node" so §3.8 is on the page).
