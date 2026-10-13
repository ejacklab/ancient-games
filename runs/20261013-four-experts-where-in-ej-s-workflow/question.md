Where in EJ's workflow-design method could you give huge, reliable help — at which stage or part — and where would you not be reliable?

Facts:
- The method turns an incoming task into a designed workflow for AI agents: which agents, what runs in sequence or in parallel, what repeats and when it stops, how results are checked. It is the "Ancient Games" framework in this repository.
- Read its eight steps in `.claude/skills/workflow-design/SKILL.md` (short). For detail on any step, the full method is `docs/WORKFLOW_DESIGN_METHOD.md`: section 3.0 understand the challenge (objective, scope, six whys), 3.1 readiness and the blueprint check, 3.2 write the algorithm, 3.3 list the unclear spots, 3.4 size, 3.5 clear pieces run as loops, 3.6 the knowledge graph, 3.7 the checked sequence, 3.8 running a node, §4 state and memory, §5 three qualities (predictability, debuggability, quality control).
- Today each expert is used only as an adviser on one question at a time (this skill). You would be called by the main agent (Claude), given a question and facts, and you return an answer with your rule numbers. You cannot act, only advise.
- "Reliable" means: the main agent can check your contribution — it rests on your numbered rules and on facts it was given, not on invented facts — and it would usually be right.

In "Answer", name your top one to three places in the method (step or section number, e.g. "3.3 unclear spots") where your rules give the most reliable help, each with the question the main agent should ask you there. In "How I decided", say which of your rules fit each place and why. Under "Costs and risks", name at least one place where you would NOT be reliable and why.
