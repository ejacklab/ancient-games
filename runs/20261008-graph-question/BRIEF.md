# Research: does agent-workflow orchestration still need an explicit "graph"?

Context: the Ancient Games workflow-design method has nine steps. Steps 3.0–3.5 front-load the analysis — understand
the challenge, readiness, write the algorithm, list every unclear spot, size the pieces, and run clear pieces as
loops. Then 3.6 is **"The rest is a graph"** — wire the pieces into a directed graph: nodes, edges, parallel
branches, joins.

The author's doubt: with that much analysis and mediation done *ahead*, is the explicit "graph" (DAG) step still
needed, or is it vestigial — a leftover from when the graph was how you enabled parallelism and information flow?
And do the latest orchestration approaches (2025–2026) still use explicit graphs, or has a better pattern emerged?

**Use web search. Cite every claim with a URL and its date.** This is about the *current* state of the art, not
what you remember.

Answer four things:

1. What are the dominant orchestration patterns right now — DAG (LangGraph-style), hierarchical / manager–worker,
   event-driven, self-organizing / swarm, map–reduce, "context engineering", sequential-with-on-demand-parallel?
   (name them with sources)
2. Is an explicit DAG still the right model, or is it now mostly "sequential first, parallel only when it earns it"?
3. Given a method that already resolves unclear spots, sizes pieces and defines loops *before* wiring a graph — does
   the graph step still earn its place, or has it become a formality?
4. Is there a better algorithm or pattern to replace or shrink step 3.6?

Rules: blind, concise (aim under ~400 words), no file edits. Reply, or write to
`runs/20261008-graph-question/<your-engine>.md`. If the author is wrong to doubt the graph, say so plainly.
