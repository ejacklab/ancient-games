I'll research this. Let me start by checking the local method definition so my answer is grounded against what step 3.6 actually says.
Research done (read-only; plan mode blocks the file write — say the word and I'll write `runs/20261008-graph-question/<engine>.md`).

## 1. Dominant patterns now

- **Sequential / single-threaded by default.** Cognition: multi-agent collaboration is "fragile" in 2025; share full traces because actions carry implicit decisions ([Jun 12 2025](https://cognition.ai/blog/dont-build-multi-agents)).
- **Orchestrator–worker where branches are truly independent.** Anthropic's Research system: +90.2% over single-agent on their internal eval, but ~15× chat tokens, and explicitly "most coding tasks involve fewer truly parallelizable tasks" ([Jun 13 2025](https://www.anthropic.com/engineering/multi-agent-research-system)). Their fix for information loss: subagent writes a **file**, passes a reference ([same post, Appendix](https://www.anthropic.com/engineering/multi-agent-research-system)).
- **Generator–evaluator (evaluator-optimizer) as the load-bearing split.** Separating the agent doing work from the agent judging it is "a strong lever"; a self-judging agent praises itself ([Mar 24 2026](https://www.anthropic.com/engineering/harness-design-long-running-apps)).
- **Context engineering** — compaction, just-in-time retrieval, structured note-taking, subagents as compression ([Sep 29 2025](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).
- **Event/session interfaces, not graph topologies.** Managed Agents virtualizes session + harness + sandbox and "makes no assumptions about the number or location of brains" ([Apr 8 2026](https://www.anthropic.com/engineering/managed-agents)).
- **Shared task list + mailbox** ([agent teams docs](https://code.claude.com/docs/en/agent-teams)): start with research/review, "avoid file conflicts", 3–5 teammates.
- LangGraph still exists but now sells itself as a *low-level orchestration runtime* and routes beginners to prebuilt agents ([docs](https://docs.langchain.com/oss/python/langgraph/overview)).

## 2. Is the DAG still right?

It's the right *dispatcher's* representation, not the right *design* frame. The Dec 2024 pattern list (chaining/routing/parallelization/orchestrator-workers/evaluator) is now backgrounded even by Anthropic, who point to Managed Agents instead ([Dec 19 2024](https://www.anthropic.com/engineering/building-effective-agents)). Consensus is your 3.7: sequential first, parallel only where it earns itself.

## 3. Does 3.6 earn its place?

**You're wrong to doubt it — but right to shrink it.** Your own traversal is the strongest evidence: a hand-written plan silently dropped two of three nodes' checks and `validate_plan` said "plan ok" (`references/method.md:357-365`). A topology that cannot drop a check is not a formality. And the graph's five-part node contract (tools/context/contract/evidence/state) is exactly what makes file conflicts and silently-lost checks structurally impossible rather than prompt-hoped — matching the teams docs' "each teammate owns a different set of files."

The **vestigial** part is only the topology *as such* — edges, joins, parallel branches drawn for their own sake.

## 4. Better algorithm

Replace "draw the graph" with a **coverage matrix + declared-parallel set**: (a) criteria→node coverage as the primary artifact (your existing rule); (b) only nodes passing all five 3.7 tests written as an explicit parallel set; (c) a declared-dependency check (the `--design` comparison, already built); (d) fixed evidence file path per node at design time. Then adopt Anthropic's removal discipline: every element must be shown load-bearing by traversal — your `method.md:561` note ("two graphs nobody queried, deferred a third") is that discipline already working, not evidence against graphs.
