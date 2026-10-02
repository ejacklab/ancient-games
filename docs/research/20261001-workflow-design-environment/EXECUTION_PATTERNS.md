# Execution patterns for agent work — 2026-10-01

The well-known ways to execute a prompt/agent workload, organised by three dimensions. EJ's original ladder
(main only → main+1 subagent → main+N subagents seq/graph/tree) covers one dimension only: **agent count and
shape**. `20260919-state.md` already identified the second — **routing authority** (who decides who works
next). The 2026 industry material adds the third — **trigger/carrier**.

Status: pattern names are stable across sources (Azure docs + two 2026 blogs + local state.md citations of
Google ADK, Strands, AutoGen). The "hierarchical wins" conclusion is **reported consensus, not measurement**.

## Dimension 1 — topology (shape)

| # | Pattern | What it is | In this folder |
|---|---|---|---|
| 1 | Single-agent loop | one agent + tools, ReAct-style, step by step | EJ's (1); COO small-node rule |
| 2 | Prompt chaining / pipeline | fixed stages, gates between | method's sequential-first default |
| 3 | Routing / triage | classifier picks one branch per input | `classification` category (agy); intake.js size decision |
| 4 | Orchestrator–worker (supervisor) | hub decomposes, fans out to workers that never talk to each other, aggregates | EJ's (3) static form; the COO design |
| 5 | Parallelization — sectioning | split work into independent parts run at once | method step 7, all-five-tests gate |
| 6 | Parallelization — voting | same task N times independently; aggregate/judge | blind independent verifiers; corroboration n≥2 |
| 7 | Evaluator–optimizer (maker–checker, critic loop) | generator + checker until objective pass or limit | method step-5 loop (scar: the n=1 critic loop that never closed → objective checks only) |
| 8 | Debate / adversarial | opposing agents argue, judge decides | `/codex:adversarial-review`; EXECUTOR_KINDS rule 6 keeps the stop-time gate off |
| 9 | Swarm / handoffs (decentralized) | peers transfer control; blackboard/group-chat variants | researched in state.md; effectively rejected — `READ_SCOPE.deny` protects source independence |
| 10 | Hierarchical tree | managers of managers; context-window management | EJ's "tree"; Gate's split-over-3 |

## Dimension 2 — routing authority (who decides next)

| # | Pattern | What it is | In this folder |
|---|---|---|---|
| 11 | Workflow-as-code | deterministic script holds the edges; models fill nodes | intake.js; "the design's edges schedule, role agents do not decide" |
| 12 | Model-driven orchestration | main agent decomposes/delegates live | EJ's (1)/(3) without a written graph; Claude Code natively |
| 13 | Blackboard / shared state file | coordination through artifacts, not messages | state-file-driven rule; Ancient Games journal |
| 14 | Agent-as-tool | agent wrapped as a function call; caller keeps control and the return | ADK's third communication mode; the Claude wrapper calling `codex exec` / `agy -p` |

## Dimension 3 — trigger / carrier

| # | Pattern | What it is | In this folder |
|---|---|---|---|
| 15 | Event-driven / scheduled | hooks, monitors, cron, loop-wakeups start runs | Claude Code hooks (incl. `agent` type), routines, cron tools |
| 16 | Fork / context-clone | workers inherit parent context + prompt cache | `/subtask`, `/fork`; tier-exit alternative |
| 17 | Batch / async API | many independent one-shot transforms, fire-and-forget | `/batch`, `/batch-api` (half price), Claude Code /batch → 5–30 worktree subagents |
| 18 | Human-in-the-loop gates | approvals as structural nodes | Ancient Games D stage; blueprint questions |

## Naming crosswalk (reported, Azure Architecture Center)

| Common name | Azure name | Aliases |
|---|---|---|
| Orchestrator–worker | Sequential orchestration | pipeline, prompt chaining, linear delegation |
| Parallelization | Concurrent orchestration | fan-out/fan-in, scatter-gather, map-reduce |
| Handoffs | Handoff orchestration | routing, triage, transfer, dispatch |
| Evaluator–optimizer | Maker-checker loop | generator-verifier, critic, reflection loops |

## The one industry conclusion worth keeping

"Hierarchical wins over swarm in production almost every time" (digitalapplied.com, reported); swarm is
reserved for exploratory research. This independently confirms the folder's existing shape: COO hub-and-spoke,
sequential-first, parallel decided last, loops inside nodes. state.md's proposed two-axis planning decision
(task structure × routing authority) is a better design vocabulary than an agent-count ladder, because it
separates *what shape* from *who decides*.

## Sources

- https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- https://www.digitalapplied.com/blog/agent-architecture-patterns-taxonomy-2026
- https://gurusup.com/blog/agent-orchestration-patterns
- local: `20260919-state.md` (with its citations of Google ADK, Strands, AutoGen)
