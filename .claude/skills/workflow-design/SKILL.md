---
name: workflow-design
description: "Designing a workflow for an incoming task or challenge — or deciding that none is needed — before any agents are dispatched: understand the challenge (objective, scope, six whys, category and its default pattern), check readiness (including the product blueprint: vision, requirements with acceptance criteria, domain, architecture, data, UI, non-functional), write the algorithm first, list every unclear spot, size the pieces, run clear pieces as loops with objective checks, then wire the rest as a graph whose nodes each carry tools, context, a contract, evidence and state; sequential and state-file driven first, parallel decided last. Use whenever someone asks to design, plan, create, improve or review a workflow, an agent pipeline, an orchestration or a multi-agent / subagent setup; asks how many agents a task needs, whether to parallelise or loop, or how agents should pass information; brings a task too big for one prompt; or when you are about to write a Workflow script or dispatch several subagents without a written design. NOT for: a task of one to three obvious steps (just do it), the Workflow script API (use workflow-authoring), or running an already designed workflow."
---

# Workflow design

The job: turn a challenge into **a prompt file** (small task) or **a workflow design** (bigger task). You are
designing, not executing. The full method with its reasons is `references/method.md`; the five templates are in
`assets/templates/`. Read the method once before your first design in a session.

Why this exists: agents left alone pick a pattern first ("let's fan out five subagents") and discover later that
they lacked information, that a loop had no way to close, or that two parallel workers collided. This method makes
the cheap discoveries first.

## First: understand the challenge (method 3.0)

From the challenge text alone — no tools, no agents. State the **objective** (what is true when the task is
done), what is **in scope**, what is **out of scope**. Then the **six whys**, each feeding one design field:
why does the person want this (objective) · why now (priority) · why this shape of solution (category + default
pattern) · why would it fail (risk tier → review depth) · why does it stop where it stops (scope) · why would
we believe it is done (check kind). Stop early when an answer no longer changes the design — six is a ceiling,
never a target. End with a **provisional category** (multi-label, marked inferred) from `references/task-types.md`: a guess
that feeds the tiny test and a first default lookup; step 2 relabels it from the algorithm. A part that cannot be written, or a challenge that allows two readings, is the first unclear
spot (kind: decision) — a question for the person with the restatement as the provisional assumption. The
restatement goes at the top of the output, beside the verbatim challenge in the state file. One paragraph in
the same session, never an agent, never a tool call. (Added 2026-10-01 at EJ's request; six whys and
categorization the same day; n=0.)

## Then: is it tiny?

The test reads the restatement, not the raw text. If the restated problem, the fix and the check are one sentence
each, and a mistake would show itself at once, do not design a workflow. Do the task, or fill in
`assets/templates/prompt-file.md`. A process that costs more than the task is a failure of the method, not a
success. (Trial 1, n=1: a one-line README fix went through the full process and cost about 309k tokens, partly
because checks and handover were counted as steps. Count only the steps the challenge itself needs.)

## The steps

Work through these in order. Each step's output is a file, because files are the one memory every tool and every
agent can read; a subagent starts with nothing but its prompt.

1. **Readiness.** List the tools (run a command to prove each works — do not assume), the skills that already cover
   part of the work, and the information: is it there, what structure is it in, is it verified against its source,
   and which agents and tools can read it. The bundled `scripts/readiness.py` runs the standard inventory in one
   pass — binaries, model caches, skill/workflow/memory locations, MCP config, machine — each line marked
   verified/reported/unknown; what it cannot prove stays unknown and needs the canary. Anything missing becomes a
   preparation piece at the front of the flow.
   Template: `readiness.md`. A node run by Codex or `agy` (not a Claude subagent): read `references/executor-kinds.md`
   first — the canary that proves the tool, read-only versus write. (The fallback rule was removed 2026-10-05:
   a failed engine blocks the node and reports.)
   **Prove the binary that will make the call, and record its version** — not the version on `PATH`. A provider can
   bundle an older copy of an engine and the two do not accept the same model names; the error names the model or
   the account, never the version. `references/executor-kinds.md`, "The bundled-runtime trap".
   **Call the CLI first and the provider tool second** (EJ, 2026-10-04): the binary on `PATH` is the one that
   updates, while a provider pins an older bundled copy and will not use `PATH` even if asked. Reach for the
   provider when the CLI is unavailable, or when a role must be read-only or blind and needs the harness-enforced
   `toolFilter` — a CLI call has no such mask.
   Every node names its role, engine, exact model and effort (never a default; the Codex plugin's example models are
   stale). The COO is the main Claude session: she distributes by the graph, monitors the state file, reviews
   verdicts, and may do a small node herself under four conditions and a tool-call cap — same file.
   **Blueprint check** (part of readiness). If the task changes a product, check the product's blueprint in
   `docs/blueprint/` (layout: `blueprint.md`): vision, core requirements with acceptance criteria, domain model,
   business logic, architecture, data model and schema decisions, UI/UX, non-functional requirements. The kind of task
   decides which sections are needed (a fix: the requirement it restores and what it touches; a feature: vision,
   requirements and what it changes; a new product: all eight present, four settled first (vision, first slice's requirements,
   hard-to-reverse architecture, non-functional targets), the rest per slice; not a product change: none, and no acceptance
   criteria). A task that changes code, schema, UI or configuration is never "not a product change"; a wrong kind
   switches the check off, so it is a stop. Each needed section is
   settled (EJ accepted it and it covers the task), draft (covers the task, not accepted), incomplete (does not cover
   the task, e.g. no requirement for the feature yet) or missing. Draft → a question for the person; incomplete or
   missing → a blueprint piece at the front that drafts the missing part for the person to accept. A piece that
   builds does not start until every section it depends on is settled — blueprint questions are not answered by
   silence. Research and design pieces may run on drafts and name the drafts they assumed; any piece that depends on
   an incomplete or missing section needs the piece that drafts it. Why: without a fixed
   target every review finds more to do, and the run never ends.
2. **Write the algorithm.** Try to write the steps that would solve the task. A step is one action with a result
   that can be checked, and each step names its check. The attempt is the evaluation: steps that write clearly mean
   a defined problem; a step you cannot write clearly, or whose check you cannot name, is an **unclear spot**.
   Then **label the pieces**: group the steps into pieces that each end in one deliverable and give each a category
   from `references/task-types.md` (file IO, shell and workflow execution stay inside their piece; no matching row =
   `others`, full method). The piece labels replace the provisional category and the difference is a Log line.
   A piece that changes product code, schema, UI or configuration is never read-only: a contradicting label is a
   stop and replan. One state-file row per piece: steps · deliverable · category · default pattern, engine, check · node it merges
   into. **A label is not a node**: pieces with the same engine and no independent check between them merge into
   one main-agent session, the default; a subagent hand-off must buy an objective check, a different kind, or
   context room (EJ's experience: splitting one prompt over three subagents is slower — waiting and lost context).
3. **List every unclear spot before resolving any.** For each: its kind (missing *information* → a research piece ·
   a *decision* → a question for the person · *unknown* → a bounded explore loop), which steps it blocks, and whether
   it depends on another spot. Listing first matters because one answer often removes another spot. Questions go to
   the person as one batch, each with a provisional assumption so it can be answered in a few words. A draft
   blueprint section is a decision spot; an incomplete or missing one is an information spot, so the task is a
   workflow design.
4. **Size.** Up to 3 steps with nothing unclear except decisions that have a default → a prompt file, questions at
   the top. More than 3 steps → consider a new piece, but split only if each part keeps its own check and the split
   changes how the work is done. A workflow design starts **default-first**: each piece's category row (labelled in step 2) or combination
   pipeline in `references/task-types.md` supplies the default pattern, engine, check and sabotage; a challenger
   design replaces a default only on a written ≥20%-lower-projected-cost claim at equal coverage, reviewed by
   `scripts/design_gate.py` plus one blind fixed-checklist pass (a different kind when it builds), and reconciled
   in the ledger (n=0). Too-small pieces cost more than they give: fixed cost per agent, context lost at
   every split, more joins. Judge risk separately from size (noticed late? cannot be undone? touches many things?);
   tiny but risky gets one independent check.
   **Size from an estimate — never hand an engine one huge prompt (EJ, 2026-10-05).** A model can estimate a
   piece's workload before it runs; use that. Hours-long work is not one piece: split it into **six or more logical
   pieces**, each with its own deliverable and check, rather than one ten-hour prompt to Codex. Health is a reason
   to split: a long attempt hides its failure and cannot be watched. Method 3.8 sets a ceiling of 8 hours on one
   call, and `check_plan` refuses a plan past it.
5. **Clear pieces run as loops** while the unclear spots are being resolved. A piece is loop-ready only with: a check
   (a script is best; next a fixed checklist judged by a separate agent; last the person's judgment), an attempt
   limit, specific feedback (the check's real output), an exit for when the limit is hit, and a check the worker
   cannot edit and that is known to be able to fail. A loop closes only on an objective check — an open-ended
   "find problems" reviewer always finds one more, so that loop never ends. Attempts start on the cheapest tier that
   could plausibly do the piece. When its limit is hit, the exit is a fresh node on a stronger tier with a short
   handoff note (the piece, its check, the last feedback) and its own limit, never a tier switch inside the running
   session: a switch voids the prompt cache, so the stronger tier re-reads the whole context at its fresh input rate,
   and the cheap tier's wrong turns would anchor it towards the same dead ends. When that limit is hit too, or there
   is no stronger tier, the piece goes back to the unclear list or to the person. (Added 2026-09-22 at EJ's request;
   n=0.)
6. **The rest is a graph.** Nodes are right-sized pieces, edges are "needs the result of", a result is verified before
   anything that depends on it starts, and branches meet at a joining step where contradictions are a stop, never
   averaged. The design's edges schedule (a script, or the COO following the graph); role agents do not decide who works next. A node that hits its limit with its tier
   exit spent goes back to the unclear list and only that part is planned again.
7. **Sequential first; parallel is the last decision.** Design everything as sequential, state-file-driven steps.
   Only when the design is complete, look for really independent pieces — all five must hold: neither needs the
   other's result; no shared files or resources; doing one would not change how the other is done; each has its own
   check; the time saved is worth the extra join. Parallel buys only clock time and costs predictability and
   debuggability. Independent verifiers need to be blind to each other, not simultaneous. When running, executors are
   tools (method 3.8): one small bounded task per call, an inner and an outer timer named in the node, no polling
   (every status check is a turn), one atomically written result file with a fixed header that a script validates,
   and any missing, empty, malformed, wrong-model or timed-out return is a failure of the executor, not of the work.
   The stronger model's work is the brief: every one carries a template, a worked example and the standard the result
   is judged by (`references/method.md` 3.8; `docs/workflow-templates/node-brief.md`). Research goes to files
   (`docs/research/<date>-<topic>/`) and only a digest of about 15 lines returns to the COO. To run a designed
   workflow, `scripts/dispatch.py run PLAN` enforces timers, the brief's three parts, the pass-back and model
   checks, the repair rounds and the call budget in code (`--dry-run` first; `docs/DISPATCHER_DESIGN.md`). There is
   **no caps rule** — deleted 2026-10-05 — and **no fallback**: a failed engine blocks the node and reports. Two reading roles: the
   *researcher* reads docs, papers and the web; the *explorer* reads existing code read-only, cites file:line with a
   quote, and marks each behaviour claim `read` or `ran` — only `ran` claims feed a build (method 3.8 item 10).
8. **The run ends at the acceptance criteria.** A piece that builds names the blueprint sections it depends on and the
   acceptance criteria it covers (ids like R1.1 or N1.1); every criterion in scope is covered by a piece that builds.
   Its stop: those criteria pass, everything the baseline recorded as passing still passes (the test command and its
   output, written to the state file before the first piece that builds), and its "must not change" holds; a failure
   of any of these is a failed attempt. A judged check is a fixed checklist of those three, never an open-ended
   review. Criteria a blueprint piece proposes are fixed when the person accepts it; if they differ from what the
   design expected, the pieces covering them are planned again. Anything else found — a new wish, an improvement, a
   problem neither the criteria nor the baseline covers — by a worker, a verifier or the final "what is missing" pass
   goes to `docs/blueprint/backlog.md` with the date and run id, never into the current run.
   A product also keeps three append-only memory files beside it: `decisions.md` (why, what was rejected),
   `changelog.md` (one entry per run that builds; release notes come from it) and `lessons.md` (dated traps with a
   recheck); each answers one listed query and is found by id or path, never read whole (method §4).

## Every node carries five things

| | What to write |
|---|---|
| **Tools** | what the agent uses, each proved working |
| **Context** | exactly what it is given, and what is withheld (a verifier never sees the worker's reasoning) |
| **Contract** | the intent, the observable stop condition (for a piece that builds: its acceptance criteria pass, the baseline still passes, "must not change" holds), what it returns and in what shape, what it may and must not change |
| **Evidence** | the proof that comes back with the result (a command and its output, or file:line) and the file it is saved in |
| **State** | what it reads from the state file before starting and what it writes back |

An edge is then concrete: the earlier node's returns and evidence become the later node's context.

## State file

The state lives in a file (`assets/templates/state.md`): each agent reads it, does one step, writes the new state
back. One writer at a time. It holds progress and results, never reasoning — notes go in the worker's own output
file. This is what lets another agent, another tool, or tomorrow's session continue the run.

## Before calling a design finished

Check it shows all three, and say so in the design:

- **Predictability** — the design's edges schedule (script or COO); limits on attempts, pieces and concurrency; structured outputs; success
  criteria written before the run (for a product change: the acceptance criteria in scope); an agent count and a
  cost estimate with its basis.
- **Debuggability** — labelled agents; every step's input and output in a file; pieces small enough to rerun alone;
  a resume point after a failure.
- **Quality control** — a check per piece; blind verifiers; proof each script check can fail; a contradiction check
  at joins; a final "what is missing" pass measured against the three-part stop of step 8 (a failure there is a
  failed attempt; anything else goes to the backlog); skipped or unrun checks reported as such.


**One more thing, and it is not a quality: the engine split.**
For build work, run `scripts/workload.py --plan <plan> --write` before the run starts. It gives **opencode priority** (EJ, 2026-10-04) by **module**, crossing each module's code and tests so the tests are written by the engine that did not write the code. The default is the *smallest* lead that counts as priority — which at five modules is exactly 60/40, costing one module its independent tests; demanding 60% on a larger plan costs far more, so `--share` is there when the bigger lead is wanted. Never split dev and tests independently: that gives half the modules their code *and* their tests from one engine. `check()` refuses a plan where opencode does not lead, that self-tests more than its lead costs, or whose verifier shares its node's engine. `docs/EXECUTOR_KINDS.md` has the rule and the arithmetic.

## Writing a rule down

Before adding or changing any rule in these documents, run it through the checklist in
`docs/research/20261005-requirement-statements/FINDINGS.md` (§2): source, one thing, unit, can it fail, weak words,
level, basis, links. It was written on 2026-10-05 after four rules in this repository read as arbitrary — and run
against three of this project's own rules, it caught four failures in one and three in another. **Never fill a
missing unit or threshold with your own value; leave it open and ask.**

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

Everything here comes from one working session and one trial (n=1); the restate step and the tier rule in step 5
have had none (n=0). Treat the numbers — the 3-step rule, the cost figures — as working values to be tested, and
tell the person when a real task contradicts them.
