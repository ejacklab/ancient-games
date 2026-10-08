I couldn't do the research you asked for. Both WebSearch and WebFetch were denied in this session, so I have no sources fetched today. I didn't use `curl` to get around that, and I didn't write `runs/20261008-graph-question/claude.md`. A file there would look like a cited answer next to the other engines' answers, and this isn't one.

If you want the cited version, allow WebSearch/WebFetch and re-run me. Below is what I remember (training data up to June 2026), clearly marked as **not verified**. Use it only to decide whether the re-run is worth it.

**Unverified, from memory (n=0, no URLs fetched):**

1. **Patterns.** Anthropic's "Building effective agents" (Dec 2024) splits the field into fixed *workflows* (prompt chaining, routing, parallelization, orchestrator–workers, evaluator–optimizer) and open-ended *agents*. It advises starting with the simplest option and adding complexity only when needed. Cognition's "Don't Build Multi-Agents" (Jun 2025) argues for one agent working in sequence that shares its full context, because each action carries implicit decisions. Anthropic's multi-agent research post (Jun 2025) reports a lead agent with parallel subagents beating a single agent on research, at about 15× the tokens of a chat. It says the setup is a poor fit when agents need shared context or have many dependencies, with most coding given as the example. "Context engineering" became the name for this concern in late 2025. LangGraph still models workflows as explicit graphs. The OpenAI Agents SDK uses handoffs instead.
2. **DAG or sequential first?** As I remember it, sequential first is the consensus. Fanning out in parallel is justified only for pieces that really are independent and read-heavy. A Google/DeepMind scaling study (late 2025) reportedly found multi-agent setups *hurt* on sequential tasks and helped on parallel ones. I'm not confident of its figures.
3. **Does 3.6 still earn its place?** **Partly. Your doubt is half right.** Steps 3.0–3.5 already settle most of what the graph used to be for, and if they're done well, drawing it as a hand-wired execution DAG is mostly a formality. What the graph still gives you is a *check*. It makes you state three things no earlier step forces into the open:
   - which piece depends on which output;
   - where two branches join and who reconciles them;
   - where information must **not** flow.

   Skip those and you get the failure Cognition describes: parallel pieces making conflicting implicit decisions.
4. **Replacement.** Shrink 3.6 from "design the graph" to "derive it":
   - each piece lists what it needs as input and what it produces;
   - pieces with no path between them are the *only* candidates for running in parallel;
   - write down the context boundaries and who owns each join.

   The graph then comes out of that list rather than being designed as a step of its own.

None of this should go into the method until it's checked against sources.
