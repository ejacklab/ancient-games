# CLAUDE.md — Ancient Games

## What this folder is for

This folder is EJ's place for designing dynamic workflows for agent work, using the knowledge kept here.

Designing a workflow means deciding, for a given task: which kinds of agents to use, what runs in sequence and what
runs in parallel, what repeats (with its limit and stop condition), who decides who works next, how agents pass
information and where they must not, and how each result is verified. Runnable workflows live in
`.claude/workflows/`.

When EJ brings a task or a question about a workflow, the job is to help design that workflow from this knowledge.
Work on the Ancient Games code serves that purpose; it is not the goal by itself.

## The knowledge here

- `docs/WORKFLOW_DESIGN_METHOD.md` — the method for turning a challenge into a prompt file or a workflow design:
  readiness (with a check of the product's blueprint), algorithm first, list the unclear spots, clear pieces as
  loops, then the graph; sequential first; state-file driven. Templates in `docs/workflow-templates/`. Runnable form:
  `.claude/workflows/intake.js` (args `{challenge, runId}`); each run writes to `runs/<runId>/`.
- `.claude/skills/workflow-design/` — the same method as a skill, so an agent is told when to use it. It is the
  source of truth; `~/.claude/skills/workflow-design` is a link to it, which makes it available in every project.
  Its method and templates are links into `docs/`, so there is one copy of each.
- `20260919-state.md` — what Ancient Games can and cannot decide today about graph, loop, swarm, sequential,
  parallel and communication patterns, and the proposed direction. Start here for workflow design.
- `ancient_games/` — the framework: a referee for agent work. Fixed rules, no LLM calls, a journal of every decision.
  Five stages: Gate (how many agents), Guard (which actions need approval), Corroborate (how many independent
  sources a claim needs), Filter (which candidates survive), Prove (is the plan cleared).
- `PROJECT_OVERVIEW.md` — map of the code, how a run works, open findings F1–F11.
- `SPEC.md`, `DECISIONS.md` — the framework's contract. Only EJ changes these.
- `docs/` — design documents and ablations: what was tried, what held, what is marked n=1 and not to be built on.
- `.claude/workflows/enhance-ancient-games.js` — a worked example of a designed workflow: dependencies between
  segments, bounded verify/repair loops, independent verifiers.

## Working with EJ here

- Answer the question that was asked, in plain language, before offering options or plans.
- Discuss first. Do not plan or run anything large until EJ says so.
- Tests: `env -u NO_COLOR python3 -m pytest -q`
