I checked the page against `WORKFLOW_DESIGN_METHOD.md`, `SPEC.md`, `ancient_games/stages.py`, the skill and `WORKFLOW_DESIGN_DIAGRAM.md`. The same review is saved in `runs/20261008-diagram/claude.md`; I didn't edit anything else.

## 1. Correct?

The five stages have the right names, in the right order (Gate, Guard, Corroborate, Filter, Prove), and the one-line description of each is accurate. Four things are wrong or overstated:

1. **The loop is drawn as if it already works, but nothing connects the two parts.** `WORKFLOW_DESIGN_DIAGRAM.md:157` says: *"There is no code path between them: nothing in `.claude/workflows/` imports or calls the framework."* The method borrows names and the number 3 from the referee code. No referee findings go back into the method. The feedback arrow is the intended design, not how a run works today.
2. **"Checks the work while it runs" is wrong.** The referee checks a plan. Gate decides the agent count before drafting starts, and Prove's output is "plan cleared to <gate>". It approves the plan before the work happens; it does not watch the work.
3. **"No LLM" is only half true.** The code makes no LLM calls. But about half of the 25 steps are judgments an LLM makes, which are passed in as inputs (`stages.py:3`).
4. **"8 steps" mixes the method's numbering with the skill's.** The method has nine sections, 3.0 to 3.8. The page's list follows the skill instead:
   - "Accept" is the skill's step 8; in the method it is part of 3.6, not a section of its own.
   - 3.7 (sequential first) is folded into "Graph".
   - **3.8 (running a node: timers, result files, no polling) is missing.**
   - "Done before anything runs" contradicts 3.5, where clear pieces already run as loops while the unclear spots are being settled.

## 2. Simple and direct?

The layout is clean: one row for the loop and two columns under it. For someone seeing it for the first time:
- **Terms are used without explanation:** "six whys", "blueprint", "default-first", "unclear spot", "candidates". For example, "Filter — which candidates survive" means nothing unless you know a candidate is a proposed action.
- **The arrow from Method to Referee has no meaning yet.** The page doesn't say what the referee receives (a plan's actions and claims) or what it returns (pass, or send back to the planner).
- **The page doesn't separate what works today from what is planned** (see point 1).

## 3. One improvement

Draw the feedback arrow dashed with the label "planned — not wired yet", and change the referee line to "clears the plan before work starts — 5 stages, fixed rules, no LLM calls."

Separately, several connectors (Gmail, Google Drive, Google Calendar, Figma, Slack, etc.) need sign-in before they can be used, and the `definite` server failed to connect. None of them were needed for this review.
