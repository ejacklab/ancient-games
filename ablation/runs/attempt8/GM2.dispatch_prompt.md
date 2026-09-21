# Dispatch prompt — ablation 7 (GM2)

Modelled on attempt 7's (`ablation/runs/attempt7/GM1.dispatch_prompt.md`). One deliberate
deviation, recorded: attempt 7 inlined the packet; this one points the agent at the filled packet
on disk and requires it to echo the Task and Hard rules back before acting, so that it can be
verified the brief was actually loaded.

=== MAIN'S PROMPT BEGINS ===

You are the main agent for one task.

Your full brief is the packet at `/tmp/ablation7-run/packet.md`. **Read it in full before doing
anything else**, then, as your first output, quote back its `## Task` section and its Hard rules
verbatim so it is on record that you loaded them. After that, follow the packet exactly.

Two operational notes the packet does not cover:

1. **If you decide to dispatch an agent**, `call dispatch` records the decision in the journal, but
   it does not spawn anything — you spawn the agent yourself with the Task/Agent tool, brief it, and
   bring its results back with `call ingest_return` under the same `agent_id`. When you spawn one,
   run it on a **different model** than your own and say in your final report which model you used
   for it.

2. **Dispatching and not dispatching are both entirely acceptable.** Neither is the expected answer,
   and neither will be judged better than the other. Decide on the task's merits.

Work until you reach a terminus the packet defines. When you stop, report: what you determined, what
you did to the repo, the exit line of every stage that ran, and — if you spawned an agent — which
model it was.
