# CLAUDE.md — Ancient Games

## The name

**The Ancient Games** — named by EJ, 2026-09-06. Its principles come from two poles: **孫子兵法** (ancient Chinese
strategy) on one side and **game theory** on the other, with **modern military doctrine** and **complexity science**
in between.

## What this folder is for

This folder is EJ's place for designing dynamic workflows for agent work, using the knowledge kept here.

The Ancient Games is one framework for agent work: the workflow-design method (`.claude/skills/workflow-design/`)
is the part that turns an incoming task into a designed workflow, and `ancient_games/` is the part that referees
the work, with the referee's findings feeding back into the method.

The method's skill is linked into both harness roots so it works in every project —
`~/.agents/skills/workflow-design` (the user-global root the DeepSeek Harness and Codex scan) and
`~/.claude/skills/workflow-design` (Claude Code). The knowledge below is what that skill uses.

Designing a workflow means deciding, for a given task: which kinds of agents to use, what runs in sequence and what
runs in parallel, what repeats (with its limit and stop condition), who decides who works next, how agents pass
information and where they must not, and how each result is verified. Runnable workflows live in
`.claude/workflows/`.

When EJ brings a task or a question about a workflow, the job is to help design that workflow from this knowledge.
Work on the referee code (`ancient_games/`) serves that purpose; it is not the goal by itself.

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
  method takes from the referee code, and the mapping from method section numbers to the skill's steps.
- `docs/EXECUTOR_KINDS.md` — who can run a node (method 3.1 / 3.6): the engines (Claude subagent, Codex, Antigravity `agy`, Qwen, opencode), what each is assigned, how it is called, its read-only form and structured output, and its
  default model and effort. A node's engine choice reads this. n=0; *reported* versus *verified* marked throughout.
- `.claude/skills/workflow-design/` — the method packaged as a skill. `SKILL.md` is the packaging and the trigger:
  its frontmatter `description` is what makes an agent decide to use it, and its body is the method as eight steps.
  Its method and templates are links into `docs/`, so there is one copy of each. It is the source of truth;
  `~/.claude/skills/workflow-design` is a link to it, which makes it available in every project.
- `20260919-state.md` — what Ancient Games can and cannot decide today about graph, loop, swarm, sequential,
  parallel and communication patterns, and the proposed direction. Start here for workflow design.
- `ancient_games/` — the referee: the part of the framework that referees agent work. Fixed rules, no LLM calls, a
  journal of every decision. Five stages: Gate (how many agents), Guard (which actions need approval), Corroborate (how many independent
  sources a claim needs), Filter (which candidates survive), Prove (is the plan cleared).
- `PROJECT_OVERVIEW.md` — map of the code, how a run works, open findings F1–F11.
- `SPEC.md`, `DECISIONS.md` — the referee's contract. Only EJ changes these.
- `docs/` — design documents and ablations: what was tried, what held, what is marked n=1 and not to be built on.
- `.claude/workflows/enhance-ancient-games.js` — a worked example of a designed workflow: dependencies between
  segments, bounded verify/repair loops, independent verifiers.

## Working with EJ here

- Answer the question that was asked, in plain language, before offering options or plans.
- Discuss first. Do not plan or run anything large until EJ says so.
- Tests: `env -u NO_COLOR python3 -m pytest -q`

### When EJ states a rule, a requirement or an algorithm

Asked for by EJ, 2026-10-05: *"each time when I told you something, you will eval my statement or algo, and ask me
what I missing, and we complete it."*

**Evaluate it, do not just apply it.** Run the statement through the **`requirement-check` skill** — load it
(`skill requirement-check`) or read `~/skills/requirement-check/SKILL.md` — and say which of the eight it passes and
fails. Then **ask EJ the failing ones** and write the completed version together.

The eight, by name: **source · one thing · unit · can it fail · weak words · level · basis · links.** Their
definitions live in the skill — one copy, not four.

**Two rules for me, learned the hard way on 2026-10-05:**

- **Never fill a gap with my own value.** If the unit, threshold or test is missing, it goes to EJ as an open
  question — inventing it is how rules become weird later. Recorded in the register as 11.1/11.2.
- **Never add structure that was not given.** No "halves", no numbered reasons, no ordered pairs unless the person
  said so. Quote them, state the operative sentence, stop.

- **Ask only what changes the shape.** A question the template already answers, or that has an obvious default, is a
  question I should not ask — it is "never add structure" done to *questions* instead of facts. Three of four
  questions I asked EJ on 2026-10-06 (a large-batch cap, "may the worker refuse", the list's destination) were
  invented problems; only one changed the template. State the sensible default and move on.

### Who is this for — and who fills it in?

EJ, 2026-10-05: *"have to remember we doing things for who."* **Every artifact has one maker.** A return template is
the worker's output, so every field in it is written by the worker; a verdict is the human's decision, and it does not
share the worker's form. Before adding a field, a step or a rule, name **who fills it** — if the answer is "someone
else, later", it is a different artifact, not a field on this one.

This is the "one thing" question applied to *people* instead of *facts*: a form that two different people fill at two
different times is two forms.

### Evidence lives in the project, not `/tmp`

EJ, 2026-10-06. The pass-back `evidence:` path points into `runs/<run-id>/` — **SHOULD**, not MUST: a worker may
leave evidence elsewhere with a written reason, but the default is the run's folder. **Basis: n=1** — the
code-graph-tool run's optimize node wrote its "old-vs-new" proof to `/tmp`, it was deleted, and the fix became
unverifiable. When evidence needs a persistent home, **suggest `runs/<run-id>/` and get the user's agreement** — do
not pick a path silently. Scratch in `/tmp` is fine; it is the *refer-back* artifact that must not stay there.
