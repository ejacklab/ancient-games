# CLAUDE.md — Ancient Games

## What this folder is for

This folder is EJ's place for designing dynamic workflows for agent work, using the knowledge kept here.

The main product is `.claude/skills/workflow-design/`: a skill that designs workflows, symlinked to
`~/.claude/skills/workflow-design` so it works in every project. The knowledge below is what that skill uses.

Designing a workflow means deciding, for a given task: which kinds of agents to use, what runs in sequence and what
runs in parallel, what repeats (with its limit and stop condition), who decides who works next, how agents pass
information and where they must not, and how each result is verified. Runnable workflows live in
`.claude/workflows/`.

When EJ brings a task or a question about a workflow, the job is to help design that workflow from this knowledge.
Work on the Ancient Games code serves that purpose; it is not the goal by itself.

## The knowledge here

- `docs/WORKFLOW_DESIGN_METHOD.md` — the method for turning a challenge into a prompt file or a workflow design:
  understand the challenge (objective, scope, six whys, category), readiness (with a check of the product's
  blueprint), algorithm first, list the unclear spots, clear pieces as loops, then the graph; sequential first;
  state-file driven. Templates in `docs/workflow-templates/`. Runnable form:
  `.claude/workflows/intake.js` (args `{challenge, runId}`); each run writes to `runs/<runId>/`.
- `docs/TASK_TYPES.md` — the default execution pattern, engine, check and sabotage per task category, seeded
  combination pipelines, and the 20% challenger rule with `docs/TASK_TYPES_LEDGER.md`. The skill's
  `scripts/design_gate.py` parses it — this file is the table's only copy (n=0 until the ledger fills).
- `docs/WORKFLOW_DESIGN_DIAGRAM.md` — the same algorithm as diagrams: the whole flow, the blueprint check, what the
  method takes from the Ancient Games code, and the mapping from method section numbers to the skill's steps.
- `docs/EXECUTOR_KINDS.md` — who can run a node (method 3.1 / 3.6): the three engines (Claude subagent, Codex,
  Antigravity `agy`), what each is assigned, how it is called, its read-only form and structured output, and its
  default model and effort. A node's engine choice reads this. n=0; *reported* versus *verified* marked throughout.
- `.claude/skills/workflow-design/` — the method packaged as a skill. `SKILL.md` is the packaging and the trigger:
  its frontmatter `description` is what makes an agent decide to use it, and its body is the method as eight steps.
  Its method and templates are links into `docs/`, so there is one copy of each. It is the source of truth;
  `~/.claude/skills/workflow-design` is a link to it, which makes it available in every project.
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
