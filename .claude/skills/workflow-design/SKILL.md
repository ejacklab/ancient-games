---
name: workflow-design
description: "Designing a workflow for an incoming task or challenge — or deciding that none is needed — before any agents are dispatched: check readiness (including the product blueprint: vision, requirements with acceptance criteria, domain, architecture, data, UI, non-functional), write the algorithm first, list every unclear spot, size the pieces, run clear pieces as loops with objective checks, then wire the rest as a graph whose nodes each carry tools, context, a contract, evidence and state; sequential and state-file driven first, parallel decided last. Use whenever someone asks to design, plan, create, improve or review a workflow, an agent pipeline, an orchestration or a multi-agent / subagent setup; asks how many agents a task needs, whether to parallelise or loop, or how agents should pass information; brings a task too big for one prompt; or when you are about to write a Workflow script or dispatch several subagents without a written design. NOT for: a task of one to three obvious steps (just do it), the Workflow script API (use workflow-authoring), or running an already designed workflow."
---

# Workflow design

The job: turn a challenge into **a prompt file** (small task) or **a workflow design** (bigger task). You are
designing, not executing. The full method with its reasons is `references/method.md`; the four templates are in
`assets/templates/`. Read the method once before your first design in a session.

Why this exists: agents left alone pick a pattern first ("let's fan out five subagents") and discover later that
they lacked information, that a loop had no way to close, or that two parallel workers collided. This method makes
the cheap discoveries first.

## Before anything: is it tiny?

If you can state the problem, the fix and the check in one sentence each, and a mistake would show itself at once,
do not design a workflow. Do the task, or fill in `assets/templates/prompt-file.md`. A process that costs more than
the task is a failure of the method, not a success. (Trial 1, n=1: a one-line README fix went through the full
process and cost about 309k tokens, partly because checks and handover were counted as steps. Count only the steps
the challenge itself needs.)

## The steps

Work through these in order. Each step's output is a file, because files are the one memory every tool and every
agent can read; a subagent starts with nothing but its prompt.

1. **Readiness.** List the tools (run a command to prove each works — do not assume), the skills that already cover
   part of the work, and the information: is it there, what structure is it in, is it verified against its source,
   and which agents and tools can read it. Anything missing becomes a preparation piece at the front of the flow.
   Template: `readiness.md`.
   **Blueprint check** (part of readiness). If the task changes a product, check the product's blueprint in
   `docs/blueprint/` (layout: `blueprint.md`): vision, core requirements with acceptance criteria, domain model,
   business logic, architecture, data model and schema decisions, UI/UX, non-functional requirements. The kind of task
   decides which sections are needed (a fix: the requirement it restores and what it touches; a feature: vision,
   requirements and what it changes; a new product: all eight; not a product change: none). Each needed section is
   settled (EJ accepted it and it covers the task), draft, or missing. Draft → a question for the person; missing →
   a blueprint piece at the front that drafts it for the person to accept. A piece that builds does not start until
   every section it depends on is settled — blueprint questions are not answered by silence. Why: without a fixed
   target every review finds more to do, and the run never ends.
2. **Write the algorithm.** Try to write the steps that would solve the task. A step is one action with a result
   that can be checked, and each step names its check. The attempt is the evaluation: steps that write clearly mean
   a defined problem; a step you cannot write clearly, or whose check you cannot name, is an **unclear spot**.
3. **List every unclear spot before resolving any.** For each: its kind (missing *information* → a research piece ·
   a *decision* → a question for the person · *unknown* → a bounded explore loop), which steps it blocks, and whether
   it depends on another spot. Listing first matters because one answer often removes another spot. Questions go to
   the person as one batch, each with a provisional assumption so it can be answered in a few words. A draft
   blueprint section is a decision spot; a missing one is an information spot.
4. **Size.** Up to 3 steps with nothing unclear except decisions that have a default → a prompt file, questions at
   the top. More than 3 steps → consider a new piece, but split only if each part keeps its own check and the split
   changes how the work is done. Too-small pieces cost more than they give: fixed cost per agent, context lost at
   every split, more joins. Judge risk separately from size (noticed late? cannot be undone? touches many things?);
   tiny but risky gets one independent check.
5. **Clear pieces run as loops** while the unclear spots are being resolved. A piece is loop-ready only with: a check
   (a script is best; next a fixed checklist judged by a separate agent; last the person's judgment), an attempt
   limit, specific feedback (the check's real output), an exit for when the limit is hit, and a check the worker
   cannot edit and that is known to be able to fail. A loop closes only on an objective check — an open-ended
   "find problems" reviewer always finds one more, so that loop never ends.
6. **The rest is a graph.** Nodes are right-sized pieces, edges are "needs the result of", a result is verified before
   anything that depends on it starts, and branches meet at a joining step where contradictions are a stop, never
   averaged. The script schedules; agents do not decide who works next. A node that hits its limit goes back to the
   unclear list and only that part is planned again.
7. **Sequential first; parallel is the last decision.** Design everything as sequential, state-file-driven steps.
   Only when the design is complete, look for really independent pieces — all five must hold: neither needs the
   other's result; no shared files or resources; doing one would not change how the other is done; each has its own
   check; the time saved is worth the extra join. Parallel buys only clock time and costs predictability and
   debuggability. Independent verifiers need to be blind to each other, not simultaneous.
8. **The run ends at the acceptance criteria.** A piece that builds names the blueprint sections it depends on and the
   acceptance criteria it covers; its stop is those criteria passing. Anything found outside them — by a worker, a
   verifier or the final "what is missing" pass — goes to `docs/blueprint/backlog.md`, never into the current run.

## Every node carries five things

| | What to write |
|---|---|
| **Tools** | what the agent uses, each proved working |
| **Context** | exactly what it is given, and what is withheld (a verifier never sees the worker's reasoning) |
| **Contract** | the intent, the observable stop condition (for a piece that builds: the acceptance criteria it covers), what it returns and in what shape, what it may and must not change |
| **Evidence** | the proof that comes back with the result (a command and its output, or file:line) and the file it is saved in |
| **State** | what it reads from the state file before starting and what it writes back |

An edge is then concrete: the earlier node's returns and evidence become the later node's context.

## State file

The state lives in a file (`assets/templates/state.md`): each agent reads it, does one step, writes the new state
back. One writer at a time. It holds progress and results, never reasoning — notes go in the worker's own output
file. This is what lets another agent, another tool, or tomorrow's session continue the run.

## Before calling a design finished

Check it shows all three, and say so in the design:

- **Predictability** — the script schedules; limits on attempts, pieces and concurrency; structured outputs; success
  criteria written before the run (for a product change: the acceptance criteria in scope); an agent count and a
  cost estimate with its basis.
- **Debuggability** — labelled agents; every step's input and output in a file; pieces small enough to rerun alone;
  a resume point after a failure.
- **Quality control** — a check per piece; blind verifiers; proof each script check can fail; a contradiction check
  at joins; a final "what is missing" pass measured against the acceptance criteria in scope (anything else goes to
  the backlog); skipped or unrun checks reported as such.

## Output

- Small task → `assets/templates/prompt-file.md`, filled in.
- Bigger task → `assets/templates/workflow-design.md`, filled in, with `state.md` and `readiness.md` beside it.
- A blueprint piece writes into the product's `docs/blueprint/`, following `assets/templates/blueprint.md`.
- Put a run's files in one folder (in the Ancient Games repo: `runs/<YYYYMMDD-slug>/`).
- Give the person the questions batch and the cost estimate before anything is run. Designing is cheap; running
  agents is not, so a run needs their go-ahead.

## Running the method as a script

`~/dev/ancient-games/.claude/workflows/intake.js` walks a challenge through steps 1–4 with one agent per step and
fixed yes/no checks in script code (args `{challenge, runId}`). It is a multi-agent run — about 300k tokens in its
one trial — so use it only when the person asks for it. Its offline test: `node tests/workflows/intake_harness.mjs`.

## Related skills

`challenge-mediation` types a challenge and rates the cost of being wrong — useful input to the risk judgment in
step 4. `task-decomposition-strategies` helps with splitting; where it leans parallel, this method's sequential-first
rule wins. `agent-loop` enforces a test loop for step 5. `chronos-ledger` tracks state across sessions.
`workflow-authoring` is the script API for turning a finished design into a Workflow script.

Everything here comes from one working session and one trial (n=1). Treat the numbers — the 3-step rule, the cost
figures — as working values to be tested, and tell the person when a real task contradicts them.
