# Linus Torvalds — Keep or remove `--mark`?

## Answer

My reading: provisionally remove `--mark P`, keeping `deadline wait` for the deadline itself. The price is losing a convenient early timer; restore it if a concrete workflow demonstrates that need.

## How I decided

1. **My #13 — solve the immediate need.** The brief’s accepted use case is a clock after Bash or file writes, plus a time-up line. It supplies no observed task requiring a percentage timer. That supports removal; it does not prove an early timer could never help.

2. **My #2 — require evidence for the alternative.** The brief reports no `--mark` use in `runs/`, and the time-monitor run used plain `sleep`. Waking early to write a report is a plausible application, but its benefit is **not measured**. Conversely, an agent-started timer differs from automatic reminders: removing reminders alone does not establish that this timer violates EJ’s decision.

3. **My reading — requirement-check of retaining the optional timer.** **Pass:** who decides—the agent; one thing—an early wake-up; unit—percentage of the time budget; weak words—an explicit P; level—optional capability; links—the brief distinguishes it from automatic reminders. **FAIL:** can it fail—no acceptance criterion establishes when this capability earns its place; basis—no demonstrated benefit. Those gaps remain open for end-of-run review.

4. **My #3 — protect actual workflows.** The reported search establishes no matching invocation in the searched run files. It does not establish absence of callers elsewhere. Removal is justified provisionally, with that limitation explicit.

5. **My #5 and my #7 — keep the decision reversible and preliminary.** Make removal a separate reversible change. The main agent decides within the run; EJ accepts or declines it afterward. No change to their working pattern is needed.

## What I need to know

For end-of-run review:

- Does a caller outside the searched run files depend on `--mark`? If yes, preserve that workflow or provide its replacement before removal.
- Has an actual task needed an early wake-up that the accepted clock behavior and existing timer approach could not supply? If yes, reconsider retention against that task.

## Costs and risks

- **Remove — my #3 and my #5:** lose the percentage-based convenience and risk breaking an undiscovered caller. Restoration takes work.
- **Keep — my #13 and my #18 (`attributed`):** retain an additional behavior to explain and verify without demonstrated benefit. Its maintenance cost is **not measured**; neither is any saving from removal.

## How we would know I was right

My proposed checks, for the implementing agent to run:

- Verify that ordinary `deadline wait` still prints at the deadline and the accepted clock behavior still works.
- Check callers beyond the reported run-file search.
- Observe subsequent runs for a task blocked by the missing early timer.

Functional checks establish preserved behavior, not that nobody needs `--mark`. A demonstrated workflow that removal prevents would be evidence to reverse my recommendation.