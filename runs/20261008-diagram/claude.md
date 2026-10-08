# Review of docs/ancient-games-algorithm.html — engine: Claude (Opus 5.5), blind

## 1. Correct?

Mostly. The five stages are named right, in the right order (SPEC §1/§4 call order C→D→B→E→A), and each one-line
gloss matches CLAUDE.md. Four things are wrong or overstated:

1. **The loop is drawn as running; it is not wired.** `docs/WORKFLOW_DESIGN_DIAGRAM.md:157` — "There is no code path
   between them: nothing in `.claude/workflows/` imports or calls the framework." The method borrows names and the
   number 3 from the referee (§5 there); no referee finding goes back into the method. "Task → Method → Referee →
   Findings ↺" is the intended design (CLAUDE.md), shown as if it were how a run works today.
2. **"Checks the work while it runs" is wrong.** The referee clears a plan: Gate sizes the task before drafting, Prove
   asks "is the plan cleared" (SPEC §4 A, `Prove: PASS, plan cleared to <gate>`). It checks the plan before the work
   lands, not the work as it runs.
3. **"no LLM" is half-true.** The code makes no LLM calls, but about half of the 25 steps are `[LLM]` judgments that
   are handed in as inputs (`ancient_games/stages.py:3`, "the `[LLM]`-cell inputs as explicit parameters"). Accurate
   wording: "fixed rules, no LLM calls; the judgments are handed in".
4. **"8 steps" mixes two numberings.** The method has nine sections, 3.0–3.8. The diagram's list is the skill's
   "understand" plus its steps 1–6 and 8, with 3.7 (sequential first) folded into Graph and **3.8 (running a node:
   timers, pass-back, no polling) missing**. "Accept" is not a method section; it is the skill's step 8, drawn from
   3.6. Also "done before anything runs" contradicts 3.5: clear pieces run as loops while unclear spots are resolved.

## 2. Simple and direct?

Yes for layout — one row, two columns, short lines. For a first-time reader:

- **Jargon without a hint:** "six whys", "blueprint", "default-first", "unclear spot", "candidates", "independent
  sources". "Filter — which candidates survive" says nothing unless you know a candidate is a proposed action.
- **Missing:** what the referee takes in (a plan's actions and claims) and what it gives back (pass, or "return to
  planner"). Without that the Method → Referee arrow has no meaning.
- **Missing:** which arrows exist today and which are planned (point 1 above).

## 3. One improvement

Draw the feedback arrow dashed and label it "planned — not wired yet", and change the referee line to "clears the plan
before work lands — 5 stages, fixed rules, no LLM calls".
