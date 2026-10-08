I'll look at the actual CLAUDE.md and repo structure before answering.
Yes — EJ is right, and I'd go further than "better": the current split is actively false. "Main product" makes one half the product and the other half a means to it, but the method cannot be evaluated without the referee and the referee cannot be tuned without the method — that's a loop, not a hierarchy, and the line as written hides it while telling agents that referee work is secondary (reinforced by lines 23–24, "the code serves that purpose; it is not the goal by itself" — that sentence is the same error and has to change too). One caution: "one framework" must not flatten the parts into interchangeable — the method is prose with no oracle, the referee is deterministic code, and they have different evidence contracts.

The sentence:

> The Ancient Games is one framework with two parts: the method (`.claude/skills/workflow-design/` and `docs/WORKFLOW_DESIGN_METHOD.md`), which turns an incoming task into a designed workflow, and the referee (`ancient_games/`), which judges the work — a task comes in, the method designs it, the referee checks it, and what the referee learns feeds back into the method.

Keep the harness-root detail (`~/.agents/skills/...` and `~/.claude/skills/...` symlinks) as its own following sentence — dropping it from that spot would lose a fact agents need. Also worth checking: line 47 calls `ancient_games/` "the framework" and line 41 calls the skill "the source of truth"; both use "framework" in the sense you're trying to retire.
