# Dave — how often the guard shows the time

## Answer
Choose **(B)**: a one-line status on every tool call, plus the fuller block with the workers' progress at 50%, 80% and 100%. It is the only option the research has tested. Treat it as the starting setting, not a final one: write down the prediction before the run, run it against a control, and test (A) later as a separate arm. Drop (C), because its N would be a number we made up.

## How I decided
1. **What would change my mind** (my #1): a measured comparison in which marks-only (A) finishes within the deadline as often as per-call (B) while adding less context. If that came out, I would switch to A. No such measurement exists. The research says so in its own words: "No source compares fixed-fraction marks or end-only notices with per-step updates (not measured)" (reminders.md digest).
2. **Data we already have** (my #5):
   - Per-step updates were tested and helped. In BATS (F1, F2), Gemini-2.5-Pro reached 12.8% at budget 10 against ReAct's 12.6% at budget 100, with 40.4% fewer search calls. In the negotiation study (F6), deal closure went from 4% to 32%. Anthropic updates after each tool call (F3) and runs a continuous countdown (F4, a vendor claim).
   - A budget given once fails. s1 got 40% control against 100% with forcing (F5). F6's limit-given-once arm fared poorly, and "On the Clock" found the prompt alone fails (F8).
   - The data does **not** show where A falls between those two ends. A is more than "once" and less than "every step", and that middle is unmeasured. F7 confirms that the negotiation study had no fraction-based arm.
3. **Vision first** (brief rule): the use case is that "the agent cannot feel time pass". s1's own line says "our model cannot reliably count tokens" (F5), and F6 says "LLMs struggle to internally track elapsed time". Under A, between 0% and 50% the agent knows nothing, and that gap is the failure the vision describes. B closes it, and its mark blocks still satisfy criterion C2 ("at reminder marks").
4. **Experiment instead of argument?** (my #2): an A-against-B behaviour test needs several timed agent runs per arm. That costs more than the 15 minutes left for this question, so the test cannot settle the matter now. Instead I take the tested option and schedule the test (step 7).
5. **How nature does it** (my #6, *recall*): animals keep time with an internal clock, which outside cues such as daylight reset now and then. **Does the analogy fit?** (my #7): no. The key condition differs. An animal has a clock to reset, and the agent has none (F5, F6). Occasional cues only make sense for a system that runs its own clock between them, so the analogy gives A no support, and I drop it.
6. **Option C** (my #10, my reading): every N calls or every N minutes needs an N nobody has measured. Picking one would be a guess presented as a setting. Rejected.
7. **Small and reversible** (my #8): B is a single output line from a hook that already runs after every tool call, and turning it down to A later is a one-flag change. Start with what has evidence, then measure whether the cheaper option holds up.
8. **How sure** (my #10): this is a moderate hint, not a law. There are four independent sources, but none uses this harness, a wall-clock limit in minutes, or Claude Code hooks. BATS and s1 measure token or call budgets, not time.

## What I need to know
- **Does the hook's per-call line stay in context for the rest of the session?** If it does, a long session adds about 20 tokens times the number of calls (about 2,000 tokens for 100 calls, using the brief's estimate, not a measurement). If the owner thinks that is too much for runs that long, then use A plus a status line only after time is up, and say clearly that it is untested.
- **Does criterion C6 already measure the hook's cost per call?** If it measures only the hook's run time and not the tokens it adds, then B's real price is unmeasured and should be added to C6's before-and-after figures.
- **How many tool calls does a typical time-boxed run make?** If it is only a few dozen, B's cost is trivial and this question barely matters.

## Costs and risks
- **Context cost** (my #5, #10): about 20 tokens per call, a figure the brief estimated, not one I measured. It adds up over long sessions.
- **The research is about a different budget** (my #7, #10): F1, F2 and F5 are token or call budgets, and only F6 and F8 are about time. Results may not carry over to a wall-clock limit.
- **Pressure to cut work short** (F4, vendor claim): a visible countdown can make a model "scope it down aggressively, or stop early". F4 says this about too small a budget, not about how often the time is shown, so applying it to B is *my reading*. Watch for it.
- **The agent may tune out the line** (*recall*, unmeasured): a line that never changes may get ignored. The fuller mark blocks are there to counter that.
- **A goes untested if B is never challenged** (my #4, #9): adopting B without ever running A means we never find out whether the quieter option is enough.

## How we would know I was right
Before running (my #3), write down:
- **Metric:** whether the run finishes and reports before the deadline (yes/no) and how many minutes it runs over.
- **Second metric:** tokens the guard adds per run.
- **Expected result:** B finishes on time at least as often as the no-guard control, at a cost of about 20 tokens per call.
- **Stop date:** the end of the next time-boxed run.

Then run the same small task with a short deadline (for example 10 minutes) under three arms: **no guard (control, my #4)**, **B**, and **A**. If A matches B on finishing on time, switch to A and record B's extra cost as wasted. If B wins, keep it. If both lose to the control, report that too (my #9). One run per arm is n=1, a hint (my #10). Repeat before calling it settled.
