# If parallel is gone, what does the workflow design still buy?

The Ancient Games method is now sequential-first. Parallel fan-out is essentially deprecated — it duplicates work
(each branch re-reads and re-discovers), while a sequential handoff compresses (one agent's result is the next
agent's input). The method still has nine steps: understand, readiness, write the algorithm, list unclear spots,
size, loops, knowledge graph, sequential-first, run a node.

The author's question, sharpened:

> If everything is sequential anyway, what is the ADVANTAGE of the workflow design over just doing the task step by
> step? What does it buy that a plain "prompt → next prompt → next" does not?

Answer plainly, no more than ~300 words:

1. Name each concrete advantage the workflow design still gives, for purely-sequential work.
2. Is it still worth it, or has it become ceremony once parallel is gone?
3. The ONE thing that justifies it, if any.

Reason it out; cite a source only if you actually have one. Blind, no file edits (reply, or write to
`runs/20261008-why-workflow/<your-engine>.md`).
