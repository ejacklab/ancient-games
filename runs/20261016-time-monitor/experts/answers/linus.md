# Linus Torvalds — How often to show remaining time

## Answer

**My reading: choose B provisionally**—show used and remaining time after every tool call, include worker progress at 50%, 80%, and 100%, and state that time is up on every subsequent call. This costs additional context and hook execution time; its advantage over A in this harness remains unmeasured.

## How I decided

1. **My #3: judge the user’s actual workflow.** The brief’s use case is finishing and reporting within EJ’s limit, while seeing workers’ timestamped progress. C2 and C3 supply the observable requirements. Reminder delivery alone does not establish that the agent finishes on time.

2. **My #2 and my #18: prefer demonstrated behavior over an invented interval.** F6 reports that per-turn time updates raised negotiation closure from 4% to approximately 32% for GPT-5.1-chat-latest. Those are the paper authors’ experiments, not measurements of this harness. They support external timing feedback, without establishing the best reminder frequency here. [Negotiation study](https://arxiv.org/html/2601.13206v1)

3. **My #18: keep the comparison honest.** F1 tests budget feedback after every tool response; its budget counts tool calls rather than elapsed time. F7 supplies no comparison against fixed percentage marks. **My reading:** B has the strongest supporting precedent; neither A’s alleged sufficiency nor C’s unspecified interval has been demonstrated. B’s compact line plus fuller milestone block is also an untested combination. [Budget Tracker study](https://arxiv.org/html/2511.17006v1)

4. **My #5 and my #7: make the choice reversible and explicitly preliminary.** The main agent can select B for this run; EJ accepts or declines it afterward. Keep the cadence separable from deadline calculation and worker reporting so changing it does not discard those functions. **My reading:** this limits the cost of being wrong.

5. **My reading—requirement check:** for the cadence choice, **who decides, one thing, unit, can it fail, level, and links pass** when B is a provisional default, measured per tool response, with missing status constituting failure and no claim of equivalence between studies. **Weak words fails** if approximately 20 tokens becomes an acceptance limit; **basis fails** for any claim that B is optimal locally. Leave those values open for measurement and EJ’s review.

## What I need to know

- What added token and hook latency costs would make EJ reject B? If measured overhead exceeds their acceptable cost, reconsider the cadence.
- Can tool calls or reasoning continue across the deadline without interruption? If so, B provides feedback only when control returns; it cannot ensure an on-time report.

These questions belong in the end-of-run review, without delaying the provisional choice.

## Costs and risks

- **My #18:** at the brief’s estimated 20 tokens per call, \(k\) calls add approximately \(20k\) tokens of status text, plus milestone blocks. Actual token counts and latency need measurement.
- **My #7:** better outcomes in negotiation or search do not establish reliable deadline completion here; F1 and F6 provide supporting evidence with different tasks.
- **My #3 — my reading:** a call that crosses the deadline can prevent any post-call reminder from arriving in time.
- **My #18 — my reading:** worker progress displayed only at milestones can be stale between them, even when workers report every small piece.

## How we would know I was right

**My #2 and my #18:** I propose fake-clock checks for per-call status, milestone crossings, repeated overdue notices, and worker timestamps and ages. These check delivery mechanics; they do not establish behavioral effectiveness.

Then compare matched A and B runs: measure completed work and final-report delivery before the deadline, overrun duration, added tokens, and hook latency. B earns continued use if those measurements show a benefit at a cost EJ accepts. **No such local comparison was performed for this answer.**