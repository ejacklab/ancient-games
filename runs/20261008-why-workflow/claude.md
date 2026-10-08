I saved this answer in `runs/20261008-why-workflow/claude.md`. I didn't read the other engines' answers in that folder. This is my own reasoning, with no source checked (n=0).

**1. What it still gives you, even when everything is sequential**

- **You have a plan before you spend tokens.** The algorithm is written first, so a wrong step is caught on paper, where fixing it is cheap. A plain chain of prompts only finds its plan by running it.
- **The unknowns get named.** Listing the unclear spots makes "we don't know X" visible. A plain chain lets the model quietly guess X and then build on that guess.
- **Every step has a check, and every loop has a limit.** In a plain chain, a step stops when the reply "looks done."
- **Steps hand off through a file, not a chat reply.** Each step's result goes into a state file with a contract. You can inspect it, resume from it after a crash or lost context, and pass it to a different engine or a cheaper or stronger model.
- **It can decide that no workflow is needed.** The sizing step gives a clear way out for tasks of one to three steps.

**2. Is it worth it, or just ceremony now?**

Partly ceremony. Without parallel work, the knowledge-graph and sequential-first steps come down to "it's a straight line" and could be one sentence each. The other steps never depended on parallel work. Parallel is where the method looked impressive, not where it paid for itself.

**3. The one thing that justifies it**

**A checked handoff between steps.** A sequential chain compresses work, but it also stacks up errors. A wrong output at step 2 becomes the trusted input for every step after it, and nothing later questions it. Parallel branches fail separately; a chain's errors build on each other. So sequential work needs a written, objective check at each handoff even more than parallel work did. A plain "prompt → next prompt → next" chain has nowhere to put that check, and the workflow design does. That's its whole case.
