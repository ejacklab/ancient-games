---
name: workflow-design
description: "Designing a workflow for an incoming task or challenge — or deciding that none is needed — before any agents are dispatched: understand the challenge (objective, scope, six whys, category and its default pattern), check readiness (including the product blueprint: vision, requirements with acceptance criteria, domain, architecture, data, UI, non-functional), write the algorithm first, list every unclear spot, size the pieces, run clear pieces as loops with objective checks, then wire the rest as a graph whose nodes each carry tools, context, a contract, evidence and state; sequential and state-file driven first, parallel decided last. Use whenever someone asks to design, plan, create, improve or review a workflow, an agent pipeline, an orchestration or a multi-agent / subagent setup; asks how many agents a task needs, whether to parallelise or loop, or how agents should pass information; brings a task too big for one prompt; or when you are about to write a Workflow script or dispatch several subagents without a written design. NOT for: a task of one to three obvious steps (just do it), the Workflow script API, or running an already designed workflow."
---

# Workflow design

This is the method half of the **Ancient Games** framework (see `CLAUDE.md`): the method designs a workflow, the
referee (`ancient_games/`) clears the plan, the knowledge (`docs/`) is shared.

The job: turn a challenge into **a prompt file** (small task) or **a workflow design** (bigger task). You are
designing, not executing. The full method with its reasons is `references/method.md`; the templates are in
`assets/templates/`. Read the method once before your first design in a session.

Why this exists: agents left alone pick a pattern first ("let's fan out five subagents") and discover later that
they lacked information, that a loop had no way to close, or that two parallel workers collided. This method makes
the cheap discoveries first.

## First: understand the challenge (method 3.0)

**Ask the time first.** With the task's details, ask the person how much time you have to try to find a
solution (a time, or a number of rounds), unless they gave it; the answer makes the run time-boxed (method 3.8 item 14).
Record a time with `guard/src/cli.ts deadline start --minutes N --run runs/<run>` (rounds: the last round in the state
file) — you cannot feel time pass; the guard
tells you after every tool call. Briefs ask for small pieces and timestamped progress lines; work with more than one
node runs as a workflow when possible (method 3.8 item 14).

From the challenge text alone — no tools, no agents — state the **objective**, what is **in scope** and what is
**out of scope**, answer the **six whys** (stop when an answer no longer changes the design), and end with a
**provisional category** from `references/task-types.md`. The table of whys, what each feeds, and what an
unanswerable one becomes: method 3.0.

## Then: is it tiny?

If it is tiny, do not design a workflow: do the task, or fill in `assets/templates/prompt-file.md`. The test reads the
restatement, not the raw text — method §2. A process that costs more than the task is a failure of the method, not a
success. (Trial 1, n=1: a one-line README fix went through the full process and cost about 309k tokens, partly
because checks and handover were counted as steps. Count only the steps the challenge itself needs.)

## The steps

Work through these in order. Each step's output is a file, because files are the one memory every tool and every
agent can read; a subagent starts with nothing but its prompt. Each step is a summary; the rule itself is in the
method section named beside it.

1. **Readiness** (method 3.1). Prove each tool by running it (`scripts/readiness.py` runs the standard inventory and
   marks each line verified/reported/unknown; `scripts/harness_health.py` adds how each harness is set up, with help
   for what is absent; `guard/src/cli.ts doctor` says whether the guard's hooks are installed — installing them is the
   owner's, `install --print <harness>`), list the skills that already cover part of the work, and check the
   information. Anything missing becomes a preparation piece at the front. Template: `readiness.md`. A node run by
   Codex or `agy`: `references/executor-kinds.md` first — the canary, read-only versus write, the bundled-runtime
   trap, CLI first and provider second, and the COO's contract. Every node names its role, engine, exact model and
   effort (never a default).
   **Blueprint check** (method 3.1): if the task changes a product, the kind of task decides which sections of
   `docs/blueprint/` it needs, and each needed section's status (settled, draft, incomplete, missing) decides the
   flow. A piece that builds waits for settled sections — blueprint questions are not answered by silence (method
   3.1). Why: without a fixed target every review finds more to do, and the run never ends.
2. **Write the algorithm** (method 3.2). First the use cases and the criteria the result will be scored on
   (R13 in the `requirement-check` skill; `references/harness-requirements.md` R12.7): the person's basic use cases plus the agent's suggestions the
   person accepts, each with its purpose, fails-if and minimum acceptance; requirements only where a use case leaves
   a detail unclear or qualities pull against each other, each naming the use case it serves; a conflict goes to the
   person, and the use case wins. Then steps that each name their check; a step you cannot write clearly, or
   whose check you cannot name, is an **unclear spot**. Then **label the pieces** by category from
   `references/task-types.md`. **A label is not a node**: a subagent hand-off must buy an objective check, a
   different kind, or context room.
3. **List every unclear spot before resolving any** (method 3.3): its kind (information · decision · unknown), what
   it blocks, what it depends on. Questions go to the person as one batch, each with a provisional assumption —
   unless the person gave a time or a number of rounds: then they go to the experts and you decide provisionally,
   and only a question three failed trials or the time given could not settle goes to the person (method 3.8 item
   14).
   In a workflow design, **ask the experts once the list is written**: the `four-experts` skill with
   `--only linus,sun-tzu,lao-tzu,dave` and its `unclear-spots` question. Their answers are advice: a raised spot is
   added and marked, a "drop it" goes to EJ as a question, never silently.
4. **Size** (method 3.4). Up to 3 steps with nothing unclear except decisions that have a default → a prompt file;
   otherwise a workflow design, **default-first** from `references/task-types.md`. Never hand an engine one huge
   prompt: hours-long work splits into six or more logical pieces. Judge risk separately from size.
5. **Clear pieces run as loops** (method 3.5) while the unclear spots are being resolved — only when loop-ready: the
   five conditions are in method 3.5. A loop closes only on an objective check; escalation is a fresh node on a
   stronger tier, never a switch inside the session. Before a piece runs as a loop, **ask the experts about its
   check**: `four-experts` with `--only linus,fan-li,sun-tzu,dave` and its `loop-check` question; a failure the
   check would miss strengthens the check or sends the piece back to the unclear list.
6. **The rest is a knowledge graph** (method 3.6). Nodes, edges, a result verified before anything that depends on
   it starts, joins where contradictions are a stop. The design's edges schedule; role agents do not decide who
   works next. The design and the plan are compared by `scripts/dispatch.py validate PLAN --design DESIGN`.
7. **The workflow is a checked sequence** (method 3.7): sequential, state-file-driven steps; parallel only where the
   five conditions of method 3.7 hold, and never without naming the unit. Running a node — executors are tools, two
   timers, no polling, pass-back, the brief's template, example and standard, the researcher and explorer roles — is
   method 3.8; `scripts/dispatch.py run PLAN` enforces it in code (`--dry-run` first; `docs/DISPATCHER_DESIGN.md`).
   With the guard installed (`guard/`, method 3.8 item 13), every engine call made through a shell is linted before it
   runs and its result checked after; without it, call `guard/src/cli.ts lint` and `result` yourself and log a failure
   with `fail` (a reason and evidence are required).
8. **The run ends at the acceptance criteria** (method 3.6). A piece that builds names the blueprint sections it
   depends on and the criteria it covers; its stop is the three-part stop of method 3.6. Anything else found goes to
   `docs/blueprint/backlog.md`, never into the current run. How nodes use project memory and its caches: method §4.
   A run with logged failures ends with an insight named in the final report (`guard/src/cli.ts insight` lists what is
   open); a use-case register is checked with `guard/src/cli.ts register <file>` (method 3.8 item 13). A run that
   succeeded records its path (`guard/src/cli.ts path new`); a similar task starts from a recorded path
   (`path parents <category>`), changes something and tries to beat it (method 3.8 item 13, R12.7); the run is scored
   on criteria written before the work (`guard/src/cli.ts criteria new`, then `criteria score`).

## Every node carries five things

| | What to write |
|---|---|
| **Tools** | what the agent uses, each proved working; a memory cache only for search, and only where it is built (method §4) |
| **Context** | exactly what it is given, and what is withheld (a verifier never sees the worker's reasoning); the memory entries it needs, as text in the brief or by an import; a sentence asking for them only as the stated fallback (method §4) |
| **Contract** | the intent, the observable stop condition (for a piece that builds: its acceptance criteria pass, the baseline still passes, "must not change" holds), what it returns and in what shape, what it may and must not change; the memory entries it reads before editing and checks before acting on (method §4) |
| **Evidence** | the proof that comes back with the result (a command and its output, or file:line) and the file it is saved in |
| **State** | what it reads from the state file before starting and what it writes back, and the memory entries it writes, and when (method §4) |

An edge is then concrete: the earlier node's returns and evidence become the later node's context.

## State file

The state lives in a file (`assets/templates/state.md`): each agent reads it, does one step, writes the new state
back. One writer at a time. It holds progress and results, never reasoning — notes go in the worker's own output
file. This is what lets another agent, another tool, or tomorrow's session continue the run.

## Before calling a design finished

Check it shows all three — **predictability**, **debuggability**, **quality control** — and say so in the design.
What each needs, and the step that defines it: method §5.


**One more thing, and it is not a quality: the engine split.**
For build work, run `scripts/workload.py --plan <plan> --write` before the run starts. It gives **opencode priority** (EJ, 2026-10-04) by **module**, crossing each module's code and tests so the tests are written by the engine that did not write the code. The default is the *smallest* lead that counts as priority — which at five modules is exactly 60/40, costing one module its independent tests; demanding 60% on a larger plan costs far more, so `--share` is there when the bigger lead is wanted. Never split dev and tests independently: that gives half the modules their code *and* their tests from one engine. `check()` refuses a plan where opencode does not lead, that self-tests more than its lead costs, or whose verifier shares its node's engine. `docs/EXECUTOR_KINDS.md` has the rule and the arithmetic.

## Writing a rule down

Before adding or changing any rule in these documents, run it through the **`requirement-check` skill**
(source, one thing, unit, can it fail, weak words, level, basis, links). One copy of the checklist, in that skill.
**Never fill a missing unit or threshold with your own value; leave it open and ask.**

## Output

- Small task → `assets/templates/prompt-file.md`, filled in.
- Bigger task → `assets/templates/workflow-design.md`, filled in, with `state.md` and `readiness.md` beside it.
- A blueprint piece writes into the product's `docs/blueprint/`, following `assets/templates/blueprint.md`.
- Put a run's files in one folder (in the Ancient Games repo: `runs/<YYYYMMDD-slug>/`).
- Give the person the questions batch and the cost estimate before anything is run. Designing is cheap; running
  agents is not, so a run needs their go-ahead. A time or a number of rounds the person gives **is** that go-ahead:
  the run then asks the experts instead of the person, decides provisionally, asks the person only about a question
  three failed trials or the time given could not settle, and stops at the limit with a report (method 3.8 item 14); the
  safety bounds still wait for the person.

## Running the method as a script

`~/dev/ancient-games/.claude/workflows/intake.js` walks a challenge through steps 1–4 with one agent per step and
fixed yes/no checks in script code (args `{challenge, runId}`). It is a multi-agent run — about 300k tokens in its
one trial — so use it only when the person asks for it. Its offline test: `node tests/workflows/intake_harness.mjs`.

## Related skills

`challenge-mediation` types a challenge and rates the cost of being wrong — useful input to the risk judgment in
step 4. `task-decomposition-strategies` helps with splitting; where it leans parallel, this method's sequential-first
rule wins. `agent-loop` enforces a test loop for step 5. `chronos-ledger` tracks state across sessions.
`requirement-check` evaluates a rule before you write it; `meaningful-names` checks a name does one job.

Everything here comes from one working session and one trial (n=1); most rules have had no run at all (n=0, dates
in `docs/METHOD_CHANGELOG.md`). Treat the numbers — the 3-step rule, the cost figures — as working values to be
tested, and tell the person when a real task contradicts them.
