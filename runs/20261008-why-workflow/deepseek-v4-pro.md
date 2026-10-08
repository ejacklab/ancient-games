# What the workflow design still buys, sequential-only

## 1. Concrete advantages for purely-sequential work

- **An explicit algorithm, written before work starts.** A prompt chain discovers its ordering as it goes; a workflow fixes decomposition, dependencies and handoffs first, making the sequence inspectable and changeable without a full re-run.
- **A designed handoff contract.** In a chain, step N+1 receives whatever N happened to output. A workflow names the state each node emits and the next consumes, so the compression (one agent's result = the next agent's input) is deliberate, not accidental.
- **Bounded verify/repair loops with objective checks.** A chain re-prompts on vibes; a workflow names the loop limit and stop condition, which can be audited.
- **Independent verification.** Worker and verifier are separate nodes even when sequential, so a result is not self-graded.
- **Readiness gating and engine choice.** The blueprint check and per-node executor assignment happen before any agent is spent.
- **Reproducibility and resumability.** The graph plus state lets you resume, re-run, and see what each node produced; a chain leaves only chat history.

## 2. Still worth it, or ceremony?

Still worth it, but the value moves. With parallel gone it is no longer an orchestration tool — coordination was what parallelism bought. What remains is a **planning and audit layer**: the part that thinks about the work before doing it. For a short, obvious task it is ceremony; where the ordering or a handoff matters, it makes the sequence a decision, not an accident.

## 3. The one thing

**An inspectable plan, separate from execution.** The workflow is an artifact a human (or the next agent) can read *before* any node runs, so a wrong order or a weak handoff is caught at design time — the cost of one look — instead of after five prompts have compounded it. That separation of designing from doing is the one thing a plain "prompt → prompt → prompt" cannot provide.
