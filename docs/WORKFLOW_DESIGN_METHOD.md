# Workflow design method

Agreed between EJ and Claude on 2026-09-20. This is the method this folder uses to turn an incoming challenge into
either a prompt file or a workflow design. It has been tried on nothing yet: every number and every piece of
"evidence" below comes from one session (n=1) and is not to be built on as a rule until it has been used on real
challenges. Most sections were added later and have had no run at all (n=0); when each rule was added, and every
rule that was removed or changed, is in `docs/METHOD_CHANGELOG.md`.

Runnable form: `.claude/workflows/intake.js`. Templates: `docs/workflow-templates/`. Runs: `runs/<run id>/`.

**One word, one job:** `check`, `validate`, `verify`, `probe`, `compare`, `checklist` and `accepted` each mean one
thing here — the table is Appendix A.

## 1. The ideas behind it

- Real tasks are rarely one pattern. Except when a task is tiny, it needs a hybrid. The mix comes from choosing a
  pattern **per piece**, not one pattern for the whole task.
- A piece that is too big fits no single pattern. A piece that is too small costs more than it is worth: every agent
  has a fixed cost, every split loses context, more pieces mean more connections, and a very small piece has
  nothing that can be verified on its own.
- A tiny task needs no workflow, only a prompt file. A workflow is prompts plus the wiring between them.
- Do not assume the model knows what it needs. Every agent starts with only its prompt.

## 2. When not to use this method

Understand the challenge first (3.0); the test reads the restatement, not the raw text. If you can state the
restated problem, the fix and the check in one sentence each, and being wrong would show itself at once: write the
prompt file by hand from `docs/workflow-templates/prompt-file.md`, or just do the task. Running the intake
workflow on such a task costs more than the task. A big-sounding challenge with a narrow objective stays small; a
vague one ("improve performance") cannot slip through as tiny.

## 3. The steps

### 3.0 Understand the challenge — before anything

From the challenge text alone — no tools, no agents, no repository browsing except opening the vision and
requirement files the last step names — state three things:

- the **objective**: what is true when the task is done;
- **in scope**: what the task touches;
- **out of scope**: what it must not touch.

Then answer the **six whys**, each feeding one design field. Stop early on any why whose answer no longer
changes the design — six is the ceiling, never a target:

| # | Why | Feeds | Unanswerable ⇒ |
|---|---|---|---|
| 1 | Why does EJ want this — what problem is behind the ask? | the objective (the XY-problem guard) | unclear spot, decision |
| 2 | Why now — what triggered it? | priority; whether a cheaper fix exists | noted; rarely blocking |
| 3 | Why this shape of solution — why the requested approach over alternatives? | the provisional category and its default pattern (`docs/TASK_TYPES.md`) | decision spot, batched |
| 4 | Why would it fail — what breaks if we get it wrong? | the risk tier → review depth and independent checks | assume the higher tier |
| 5 | Why does it stop where it stops? | in scope / out of scope | decision spot |
| 6 | Why would we believe it is done? | the stop condition and check kind (script, checklist, EJ) | the piece is not loop-ready (3.5) |

End with a **provisional category** (multi-label, marked *inferred*) from `docs/TASK_TYPES.md`. It is a guess
from the text alone: it feeds the tiny test (§2) and a first default lookup, and 3.2 relabels it from the
algorithm.

A part that cannot be written, or a challenge that allows two readings, is the first **unclear spot** (kind:
decision, 3.3): a question for EJ with the restatement as the provisional assumption. No new blocking rule is
added: a prompt file's restatement stands on its provisional assumption like any decision, and a design's
question batch reaches EJ before anything runs.

#### Then: the vision and requirements the task serves (every task except a tiny one)

A task that is not tiny (§2) names the vision and requirements it serves before any research, design or build
starts. This includes research, design and documentation tasks: they have a target too, even when they change no
product.

- **Vision**: what the result is for and who uses it. It is EJ's: cite the file, or quote EJ's own words from the
  conversation. An agent never writes the vision. If there is none, that is a question for EJ.
- **Requirements**: what the result must do, each with an acceptance criterion that some input can fail. If they
  exist, cite them. If they are missing or incomplete, the agent drafts them from the vision and from what EJ has
  said, marks them *draft*, and puts them to EJ with the restatement.

**Work does not start until EJ confirms the requirements.** This question is not answered by silence (as in the
blueprint check, 3.1).

Then read the restatement against them. Where the objective, the scope or a why disagrees with the vision or a
requirement, rewrite it and say what changed.

*Basis:* EJ, 2026-10-12, n=1. In run `20261012-memory-caches` the first caches design was framed without a vision,
and EJ had to correct its scope. The runs after the vision and R1–R8 existed (`20261012-caches-routing`,
`20261012-caches-merge`) had a fixed target for every check.

The restatement, the why-answers and the provisional category go at the top of the output, beside the verbatim challenge in
the state file, so EJ sees and can correct what the run understood before tokens are spent.

Cost guard (trial 1, 3.4): this step is one paragraph and six short answers in the same session, never an
agent, never a tool call, apart from opening the vision and requirement files. On a tiny task it is the prompt file's first lines, so the cheap path stays cheap.

### 3.1 Readiness — always first

**`git` is not a requirement.** A run must work in a plain directory; readiness checks the `git` binary only because
the tooling uses it when it is there, and in a repository the run keeps a pre-run `git status --short` to tell what
*it* changed. The **baseline** is the product's test command and its output (`baseline.command`, gate rule G10),
written to the state file before the first node that builds starts; everything it records as passing must still
pass (3.6). A `git status` snapshot never stands in for it.

For the task, and later for each piece, list:

- **Tools**: the commands, scripts and connections needed, each with the command that proved it works. Run it; do
  not assume. The skill's inventory script (`.claude/skills/workflow-design/scripts/readiness.py`) proves the
  standard set in one pass and marks every line verified / reported / unknown; what it cannot prove stays unknown.
  Beside it, `harness_health.py` reads how each installed harness is set up against ten harness requirements
  (guardrails, approval, hooks, logs, instruction files) and, for what is absent, names the file and what to change,
  with a snippet where the fix is a setting; it reads configuration, it does not prove enforcement, and it changes
  nothing (n=0).
  `guard/src/cli.ts doctor` reports, per harness, whether the guard's hooks are installed and whether the guard answers
  a planted trap; it reads settings key names only and changes nothing.
  `memory_check` (`bun memory_check/src/cli.ts --project <repo root> --out runs/<run>/memory-check.md`) checks the
  project's memory against `docs/memory-system/SOURCE_OF_TRUTH.md` and `CACHES.md`; it reads only. It runs once,
  here, not per node; the report is saved in the run folder and its counts line goes into readiness. A failing MUST
  does not stop the run: it is an unclear spot (3.3), and only the pieces that read that memory wait. "Needs a
  reviewer" is a note, never a gate; "could not run" is recorded as unknown; pass or "not applicable" carries on, and
  an absent `project-memory/` is no reason to create one.
  For a node run by Codex or `agy`, the proof is the canary piece in `docs/EXECUTOR_KINDS.md`, which
  also says which kind a node is assigned to and how its failure shows.
- **Skills** that already cover part of the work.
- **Information**: is the knowledge there; what structure is it in (a state file, a root map, a hierarchy of md
  files, a memory folder, a journal or index, a graph, only the web); and which agents and tools can actually use
  that structure.

What the information check finds changes the flow:

| Found | Effect |
|---|---|
| Well-structured files with a map | Fast path: each agent's brief points at exact files |
| There, but unstructured | Add a piece at the front that extracts and organises it |
| Readable by one tool only | Route that piece to that tool, or export what is needed to a plain file |
| There, but not verified | Add a small piece that checks it against the source |
| Missing | Research becomes a piece of the flow; only the pieces that need it wait for it |

Anything missing becomes a preparation piece at the front. Each task should leave the knowledge better structured
than it found it, so the next task gets the fast path.

#### Blueprint check — part of readiness

A stop condition means something only against a fixed target. For a task that changes a product, that target is the
product's **blueprint**: what the product is for and what it must do, written down and accepted by EJ. The tools and
information checks above do not ask for it, so this check does.

The blueprint lives in the product's repository, in `docs/blueprint/`, one file per section, with a map
(`docs/blueprint/README.md`) that says where each section is. Where a project already keeps a section elsewhere, the
map points there and that project's rules on who may change it still hold. Layout and headings:
`docs/workflow-templates/blueprint.md`.

| # | Section | Whose decision |
|---|---|---|
| 1 | Product vision | EJ's. An agent may only write down what EJ has said |
| 2 | Core requirements, each with checkable acceptance criteria (R1, R1.1, …) | EJ's. An agent may draft from the vision |
| 3 | Domain model | drafted by an agent from sections 1–2, accepted by EJ |
| 4 | Business logic | drafted by an agent from sections 2–3, accepted by EJ |
| 5 | System architecture | drafted by an agent from sections 2–4 and 8, accepted by EJ |
| 6 | Data model, schema design and its decisions | drafted by an agent from sections 3–5, accepted by EJ |
| 7 | UI / UX design | drafted by an agent from sections 2–4, accepted by EJ |
| 8 | Non-functional requirements (performance, security, cost, limits) | EJ's. An agent may draft from the vision |

Each section traces to the sections it is drawn from: a line that serves nothing above it is a finding, not a
feature.

**Which sections a task needs** depends on what kind of task it is:

| Kind of task | Sections needed |
|---|---|
| Not a product change (research, a question, an analysis, an edit to documentation only) | none of the blueprint sections; its vision and requirements were settled in 3.0 |
| Fix: restores behaviour the requirements already describe (if they do not describe it, it is a feature) | the requirement it restores, and the sections the fix touches |
| Feature: adds or changes behaviour | vision, requirements, and every section the feature changes |
| New product | all eight present; four settled before anything builds — vision, the first slice's requirements, the hard-to-reverse architecture choices as short decision records, the non-functional targets with runnable checks; the other four settled for the slice only, unknowns marked |

The kind of task is itself checked against the challenge: a task that changes the product's code, schema, UI or
configuration is never "not a product change". A wrong kind switches the whole check off, so it is a stop, not
something a later step can repair.

**Status of each needed section, judged for this task** (not the status line in the file, which only says whether
EJ accepted it):

- **settled** — EJ has accepted it (the file says so, with a date) and it covers what this task needs;
- **draft** — it covers what this task needs, but EJ has not accepted it;
- **incomplete** — it exists, accepted or not, but does not cover this task (for example the feature has no
  requirement yet, or the change needs a table the data model does not have);
- **missing** — there is no such section.

**What each status does to the flow:**

| Status | Effect |
|---|---|
| settled | nothing; the fast path |
| draft | an unclear spot of kind **decision**: a question for EJ ("accept this section as written?"), the draft being the provisional assumption |
| incomplete | an unclear spot of kind **information**: a blueprint piece at the front drafts the missing part into the section (for requirements: the new R-blocks with their acceptance criteria), and EJ accepts it (the piece's check is EJ's) |
| missing | an unclear spot of kind **information**: a blueprint piece at the front drafts the section from the sections above it, and EJ accepts it (the piece's check is EJ's) |

**Blueprint confirmations are not answered by silence.** In a prompt file other questions stand on their provisional
assumption unless EJ corrects them (3.3); blueprint questions do not. A piece that **builds** — changes the
product's code, schema, UI or configuration — does not start until every section it depends on is settled, so a
blueprint question must be answered, and a blueprint piece accepted, before such a piece runs. Pieces that only
research or design may run on draft sections, without waiting for the answer; their output names the draft sections
they assumed. Any piece that depends on an incomplete or missing section needs the blueprint piece that drafts it,
because until then there is nothing to read. Each unsettled section has exactly one blueprint spot.

This check is per task. Per piece, the design records which sections the piece depends on (3.6).

### 3.2 Write the algorithm

Try to write the steps that would solve the task. A **step** is one action with a result that can be checked.

- Steps can be written clearly, each with its check → a strictly defined problem. The number of steps is the size,
  and the steps show what must be in order and what repeats.
- A step cannot be written clearly → the problem is ambiguous there. It is an **unclear spot**.
- A step with no check you can name counts as unclear, however tidy it looks. This guards against a confident
  algorithm for a problem that is not understood.

**Label the pieces.** Once the steps are written, group them into
**pieces** — consecutive steps that end in one deliverable — and give each piece a category from
`docs/TASK_TYPES.md`, with its default pattern, engine and check beside it. The labels come from the algorithm, not
from the prompt text: a prompt that reads as one category often holds several (fix a test, then document it).

- Label deliverables, not raw steps. File IO, shell execution and workflow execution stay inside the piece they
  serve (TASK_TYPES.md, "Step-level, not categories"); its labelling rules 1–9 apply per piece.
- A piece with no matching row is `others` and gets the full method from first principles. Steps that cannot be
  grouped into one deliverable are an unclear spot.
- The piece labels replace the provisional category from 3.0. Where they differ, the pieces win and the
  difference is a Log line.
- Facts check, per piece: a piece that changes product code, schema, UI or configuration is never labelled
  read-only, and a label that contradicts what the piece writes is a **stop and replan**, not a repair (the
  blueprint kind-guard's shape).
- **A label is not a node.** Labelling says what kind of work a piece is; it does not say it needs its own agent.
  Pieces that share an engine and have no independent check between them merge into one node run by the main
  agent in one session — the default. A hand-off to a subagent must pay for itself: it has its own objective
  check, or needs a different kind (a blind reviewer, another engine), or its context would not fit. EJ's
  experience (2026-10-02, unmeasured here): a prompt finished by the main agent is faster than the same work split
  over three subagents going back and forth, from the waiting and from context lost at every hand-off. Same
  warning as 3.4: fixed cost per agent, context lost at every split, more joins.
- Output: one row per piece in the state file — steps · deliverable · category · default pattern, engine and check
  from the table · and the node it merges into. The node contract still names the exact model and effort.

### 3.3 List all the unclear spots before resolving any

For each spot record:

| | |
|---|---|
| Kind | missing **information** → a research piece · a **decision** → ask EJ (in a time-boxed run, the experts: 3.8 item 14) · **unknown** → a bounded explore loop |
| Blocks | which steps cannot start until it is resolved; everything else can start |
| Depends on | another spot whose answer might remove or change this one |

Questions for EJ go out as one batch, each with a provisional assumption so it can be answered in a few words — except
in a time-boxed run, where they go to the experts and the main agent decides provisionally (3.8 item 14).
In a prompt file a provisional assumption stands unless EJ corrects it; a workflow design's questions are answered
before the designed workflow runs. Blueprint questions are the exception in both: they are not answered by silence,
and they hold back only the pieces that build on them (3.1). Where spots are resolved separately, one
joining step compares the answers. A contradiction is a stop: pick one and say why, never average.

**Ask the experts once the list is written** (EJ, 2026-10-13; SHOULD; n=0). In a workflow design — not a prompt
file — after every spot is listed and before the questions go to EJ, the COO runs the `six-experts` skill with
`--only linus,sun-tzu,lao-tzu,dave` on the algorithm and the spot list (question template
`.claude/skills/six-experts/assets/questions/unclear-spots.md`; run it as `.claude/workflows/experts-decide.js`,
3.8 item 14). Each answers its own question:

- **Linus** (Codex): which choices depend on missing technical facts, and what would make a mistaken choice reversible?
- **孫子** (dsh): for each piece, do we know that our engines and tools can do it, that the task as posed can be done,
  and that the ground (files, blueprint, information) permits it — and which is only half known?
- **老子** (opencode): which spots can be answered by giving up a step rather than by resolving it?
- **Dave** (Claude): for each *unknown*, what is the smallest reversible experiment, what is predicted before it
  runs, and when does it stop?

Their answers are advice. A spot an expert raises goes into the table with *raised by* that expert. A spot an
expert says can be dropped goes to EJ as a question — never dropped silently: 老子 named the risk himself, his rules
reward subtraction where the method needs coverage. A proposed experiment becomes a bounded explore loop only when
the COO or EJ accepts it. Experts who disagree are shown side by side, under the contradiction rule above. The state
file records the expert run's folder, or *not asked* with the reason. Basis: four of the five experts named 3.3 as
where their rules help most (`runs/20261013-four-experts-where-in-ej-s-workflow/compare.md`) — their own reading,
not measured. Look again after the first three designs that use it: count the spots the experts added, dropped or
changed, and whether the run still reached its stop.

### 3.4 Size

- Up to 3 steps and nothing unclear except decisions that have a provisional assumption → one piece → a prompt
  file, with those decisions listed at the top as questions for EJ. A spot of kind information or unknown always
  means a workflow design. Blueprint spots follow the same rule: a missing or incomplete section
  always means a workflow design; a draft section alone does not.
- More than 3 steps → consider a new piece. Split only if each part keeps its own check **and** splitting changes
  how the work is done ("Split iff it changes the route", `challenge-mediation` skill).
- **Health is a reason to split.** A long single attempt hides its failure and cannot be
  watched; a run whose work is cut into segments ends each one and can be looked at.
- **Size from an estimate, and never hand an engine one huge prompt** (a design guideline). A model can estimate a
  piece's workload **before** it runs — use that, rather than discovering the size from a timeout. **A piece whose work is hours long is not a piece: split it into six or more logical pieces**, each with
  its own deliverable and its own check. The anti-pattern is concrete — one ten-hour prompt to Codex.

  It does not remove 3.2's warning that every hand-off has a fixed cost and loses context at the split.
- Risk is judged separately from size: how late a mistake would be noticed, whether it can be undone, how many
  things it touches. Tiny but risky → the prompt file gets one independent check.

**Default-first design.** When the size decision says workflow design, the design starts from a lookup, not a
blank page: each piece's category row (labelled in 3.2) or combination pipeline in `docs/TASK_TYPES.md` supplies the default pattern,
engine, check and sabotage; `others` gets the full method from first principles. A bespoke (challenger) design
replaces a default only on a written claim of ≥20% lower projected run cost **at equal coverage** (same
criteria ids, same checks, same blindness — coverage is a gate, never an axis). The decision is reviewed by the
script gate (`design_gate.py`) plus one blind fixed-checklist pass (Sonnet 5.5; a different kind when the
design builds or EJ flagged high risk), and every run reconciles its claim in `docs/TASK_TYPES_LEDGER.md` —
that ledger is how the defaults earn their n.

Anchors for the number 3 **in a piece's step count** (not a cap on roles or concurrency — there is none, 3.7): Gate
splits capability lists over three (`ancient_games/stages.py:109`) and the plan-wide cap of 3 dispatched
corroborating sources (`ancient_games/registry.py:24`, used at `stages.py:309`; it caps dispatches per plan, not
agents running at once).

### 3.5 Clear pieces run as loops

While the unclear spots are being resolved, the pieces that are already clear and not blocked run as loops: a
defined output, the agent attempts, the check runs, pass → close the loop, fail → the feedback goes back to the agent.

A piece is loop-ready only if it has all five:

1. A check. Best is a script; next a fixed checklist judged by a separate agent; last EJ's own judgment.
2. A limit on the **number** of attempts — a count, not a time limit (time is 3.8's business).
3. Specific feedback: the script's real output, not just "failed".
4. An exit for when the limit is hit. If the attempts ran on a cheap tier, the exit is a fresh node on a stronger
   tier with a short handoff note (the piece, its check, the last feedback) and its own limit — never a tier switch
   inside the running session: a switch voids the prompt cache, so the stronger tier re-reads the whole context at
   its fresh input rate, and a session in which the cheap tier flailed is mostly wrong turns that would anchor the
   stronger tier towards the same dead ends. When that limit is hit too, or there is no stronger tier, the piece
   goes back to the unclear list or to EJ. It was not as clear as it looked.
5. A check the worker cannot edit, and that is known to be able to fail (the house sabotage check).

A loop only closes when its check is objective. (n=1: a planner/critic loop whose check was "try to reject it" ran
three rounds, 6 → 5 → 4 problems, and never closed. See `20260919-plan-critic-issues.md`.)

**Ask the experts before calling a piece loop-ready** (EJ, 2026-10-13; SHOULD; n=0). In a workflow design, before
a piece runs as a loop, the COO runs the `six-experts` skill with `--only linus,fan-li,sun-tzu,dave` on the piece,
its check (conditions 1 and 5) and its attempt limit (condition 2); several pieces may go in one call (question
template `.claude/skills/six-experts/assets/questions/loop-check.md`; run it as `.claude/workflows/experts-decide.js`,
3.8 item 14). Each answers its own question:

- **Linus** (Codex): could this check pass while the requested result is wrong or an existing user workflow breaks?
- **孫子** (dsh): what is left to the worker's good character rather than to a check it cannot edit?
- **范蠡** (agy): what bounds the attempts before the loop must exit, and how promptly must it close when the check
  passes?
- **Dave** (Claude): what result would show this check can fail, and what is its control?

A concrete failure the check would miss means the check is strengthened before the loop runs, or the piece is not
loop-ready and goes back to the unclear list. 老子 is left out: he named 3.5 as a place where his rules are not
reliable. The state file records the expert run's folder per piece, or *not asked* with the reason. Same basis and
the same review as the 3.3 paragraph: count the checks the experts changed, and whether a later failure was one
they had named.

Attempts start on the cheapest tier that could plausibly do the piece; a stronger tier, which costs many times more
per token, is bought only for what the cheap one could not finish; escalation is item 4's exit.

### 3.6 The rest is a knowledge graph

When the spots are resolved and the clear loops have closed, the algorithm is fully defined. The rest is declared
as a **knowledge graph** — what each piece knows, needs and produces — not drawn as an execution DAG:

- a node = a right-sized piece, with what it needs as input and what it produces as output (a node may hold its own loop);
- an edge = "this piece needs that piece's result" — the knowledge that flows from one to the next;
- what each piece must not see is written down (the information boundaries);
- a result is verified before anything that depends on it starts;
- a joining node where branches meet; contradictions there are a stop.

Every node carries five things, so that it can be run, checked and resumed without asking anyone:

| | What it says | Borrowed from Ancient Games |
|---|---|---|
| **Tools** | what the agent uses, each proved working | — |
| **Context** | exactly what the agent is given, and what is withheld | `KNOWN_FACTS`, `READ_SCOPE.deny` |
| **Contract** | the intent, the stop condition, what comes back and in what shape (given to the worker as a template, an example and a standard, 3.8), what may and must not change | `INTENT`, `STOP`, `OUTPUT`, `SCOPE` (`ancient_games/schema.py`) |
| **Evidence** | the proof that comes back with the result and the file it is saved in; a verifier reads the evidence, never the reasoning | `CLAIMS`, `VERIFY_OUTPUT`, `NOT_ESTABLISHED` (the return contract) |
| **State** | what the node reads from the state file and what it writes back | the journal, read before every step |

An edge is then more than "needs": it is the earlier node's *returns* and *evidence* becoming the later node's context.

A node that **builds** also names the blueprint sections it depends on and the acceptance criteria it covers
(R1.1, …, and non-functional N1.1, …; ids in exactly that form). Every criterion in scope is covered by at least one
node that builds; a node that does not build carries no criteria, except a blueprint piece, which names the criteria
it is expected to propose. The stop condition of a node that builds has three parts, all objective:

1. the acceptance criteria it covers pass;
2. the baseline recorded in 3.1 still passes;
3. its contract's "must not change" holds.

A failure of any of the three is a failed attempt, not a backlog item. If its check is judged, it is a fixed
checklist of those three parts, never an open-ended review. The node `needs` the blueprint piece for any of its
sections that was missing or incomplete, and for any criterion that piece is to propose; it does not start while any
of its sections is unsettled (3.1, blueprint check). Criteria a blueprint piece proposes are fixed when EJ accepts
the piece, before any node that builds starts; if EJ accepts different criteria than the design expected, the nodes
that cover them are planned again, as when a node hits its attempt limit.

Anything else a worker, a verifier or the final "what is missing" pass finds — a new wish, an improvement, a
problem that neither the criteria in scope nor the baseline covers — is written to the product's
`docs/blueprint/backlog.md` with the date and the run id (a suspected break of something the baseline does not cover
is marked as such, for EJ); it does not become a new piece or a new attempt in this run. This is what lets a run end.

**The evaluator at a milestone.** The requirements evaluator (`docs/evaluator/`, code on branch `build/evaluator`)
judges a product against its vision, use cases and requirements. It runs on a milestone build, or a build the owner
names — never per task or per node: one evaluation costs about a million tokens and twenty minutes. Its `verdict.json`
reaches the guard through `guard/src/cli.ts evaluation ingest <verdict.json> --run runs/<run> --baseline <the
product's last accepted verdict.json>`: each requirement group that fails with a FAIL case the accepted verdict did
not fail becomes one failure found by the evaluator (R12.2); a group whose FAIL cases were all in the accepted verdict
is a note in `evaluator-notes.md` ("FAIL in the baseline too"), since the owner accepted it with that build; an UNKNOWN
is a note too; an evaluation that crashed, timed out or was blocked is a note, never a failure, because a crash is no
judgment. When the owner accepts the build, its verdict becomes the accepted verdict for the next evaluation. (This
"accepted verdict" is not the test baseline of 3.1.)

With everything known, the design's edges decide who works next: a Workflow script, or the COO (the main Claude
session) following the knowledge graph. A node's role subagents do not choose the next node. Each node names its role, engine,
model and effort; the COO's contract, and when she does a small node herself, are in `docs/EXECUTOR_KINDS.md`. If a node hits its attempt limit
and its tier exit is spent, it returns to the unclear list and only that part of the knowledge graph is planned again.

**The design and the runnable plan are two artifacts, and the COO writes both.** The design carries the plan of
work — categories, checks, edges, loops — and the gate validates it; the plan (`plan.json`) carries what a run needs
— each node's engine as a bare name, its model, its timers, its brief path. `dispatch.py validate PLAN --design
DESIGN` compares them, and `run` refuses a plan that loses the design. The comparison is asymmetric: **the design's
promises must survive; the plan may add and may not lose.** Without `--design` the command says so on stderr.

Whole picture: knowledge graph on the outside, loops inside the nodes, exploration only inside the unknown-spot nodes. This is
what `20260919-state.md` calls combined execution.

### 3.7 The workflow is a checked sequence

The workflow is a sequence, and the check at each handoff is the machine — not the topology. A step's result is
verified, then becomes the next step's input. A plain prompt chain lacks exactly this: it stacks errors silently — a
wrong output at step 2 becomes step 3's trusted input — while a checked sequence catches the error at the seam.

This is also why sequential holds *for research*: a handoff compresses (one agent's distilled result is the next
agent's input), where fan-out duplicates (each branch re-reads and re-discovers). Design the whole flow as
sequential, state-based steps — read the state file → do one step → write the state back — and look for parallel
only when the design is complete, and only where it really earns it. All five must hold:

1. neither needs the other's result;
2. no shared files or resources;
3. doing one would not change how the other is done;
4. each has its own check;
5. the time saved is worth the extra joining step.

Parallel buys only clock time, and it costs predictability, debuggability and extra joins. Independence of
verifiers is about what they see, not when they run: two verifiers can run one after another and stay independent.

There is no cap on roles or on how many run at once (the deleted caps rule: `docs/METHOD_CHANGELOG.md`); the budget
keeps `max_rounds` and `max_calls`, which limit *attempts* (3.5). **If a run needs many roles, that is a design
question, not a cap.** **Never write "running in parallel" without naming the unit** — resident sessions, engine
processes alive, or candidate approaches (Appendix C).

### 3.8 Running a node: executors are tools, timers, pass-back, no polling

Every number here is a provisional working value (n=0) that the ledger replaces with measured ones.
`scripts/dispatch.py` enforces the timers, the ceiling, the brief's three parts, the pass-back check and the
executor-failure rule in code (`docs/DISPATCHER_DESIGN.md`); the engines' own facts are in `docs/EXECUTOR_KINDS.md`.

The COO (the main Claude session) is the leader and holds the thinking. Codex, `agy`, `qwen` and role subagents are
**tools** she calls: agents are not yet stable (a call may stop half-way, return nothing, or return something
malformed), and every exchange with them costs the COO a turn that re-reads her whole context. Before any call, know
which binary will make it and record its version (`docs/EXECUTOR_KINDS.md`, "The bundled-runtime trap"). So:

1. **One small task per call** — one deliverable, one command line, an expected finish inside its timeout; a loop
   runs outside the call, each attempt a fresh small call (3.5), and a piece too big for one call is split only where
   3.2's "a label is not a node" allows.
2. **Two timers per call, both named in the node** — the tool's inner timer (`qwen --max-wall-time`,
   `agy --print-timeout`; `codex exec` has none verified) and an outer `timeout` a little longer; provisional sizes,
   listed with the design's cost estimate: classification or lookup 60–90 s, one-file change, one-file test set or
   diff review about 5 min, research about 10 min; **no call runs past the 8-hour ceiling** — hitting it is an
   executor failure (item 5), and `validate_plan` refuses an `outer_timeout_s` past it.
3. **No polling** — the COO waits by one blocking call under the outer timer, a background run that notifies her on
   exit, or a script that prints one line `done|fail|timeout <result path>`; a progress file is read only after a
   timeout; the design states the COO turns it expects per node (provisional: two, dispatch and accept) and in total.
4. **Pass-back contract** — one result file per call at `runs/<id>/nodes/<node>-<attempt>.result.*`, written to a
   temp name and renamed, with the fixed header of `docs/workflow-templates/result-file.md`; the script
   `.claude/skills/workflow-design/scripts/validate_result.py` checks it, and the COO reads only the capped summary
   (provisional: the header and the first 40 lines) and the path, never the raw output.
5. **An unstable return is a failure of the executor, not of the work** — no file, empty file, unparseable header,
   wrong model, a timeout, or a clean exit with no result (instances: `docs/EXECUTOR_KINDS.md`); it does not count
   against the attempt limit, the node is **blocked** and goes to EJ, and there is no fallback — one engine per node;
   `partial` is the COO's call: retry only the remainder as a new small call.
6. **A half-finished node must not leave a mess** — a node that builds writes only inside its "may change" paths,
   from a clean commit or a worktree, so a failed call is discarded whole; the COO never reverts by hand to "tidy
   up": a revert of anything but a discarded worktree is a Rule 6 confirmation.
7. **Keep the COO's reading small** — results by path, one-line Log entries, only the state rows the next step
   needs; raw tool output never enters her context.
8. **The stronger model gives the worker a template, an example and a standard** — every brief
   (`docs/workflow-templates/node-brief.md`) carries the template the result must follow, one small real worked
   example, and the standard it is judged by (the check as the worker can run it, what failing looks like, the
   sabotage it catches); a brief missing any of the three is not dispatched, and a part the COO cannot write is an
   unclear spot (3.3).
9. **Research is written to files** — the *researcher* reads docs, papers and the web, writes full findings (each
   with an id, a source and a label) to `docs/research/<date>-<topic>/FINDINGS.md` and returns a digest of about 15
   lines, no more than 20, plus the path (`docs/workflow-templates/research-file.md`); a doubt is settled by reading
   one finding by id or by a small verify node; a design decided from research becomes a decision entry in `project-memory/entries/` (§4).
10. **Exploring existing code is its own role** — the *explorer* reads code, tests, configs and git history, never
   the web, read-only under a stated budget and never a repo-wide overview (TASK_TYPES, case C); every claim carries
   file:line and a verbatim quote that `scripts/quote_check.py` confirms (a failing quote is a failed finding;
   `docs/workflow-templates/explorer-file.md`); every behaviour claim is marked `read` (inferred) or `ran`
   (confirmed by running it), and a `read` claim a build depends on is an unclear spot until it is run; it returns a
   digest and the path; the COO explores herself when the affected area fits her context (`docs/EXECUTOR_KINDS.md`,
   roles).
11. **Every run leaves a feedback record** (`docs/research/20261002-workflow-feedback`) — `scripts/runlog.py exec`
   wraps each Codex, `qwen` or `agy` call (raw output to the gitignored `runs/<id>/raw/`) and `runlog.py verdict`
   logs each node check; afterwards `scripts/harvest_run.py` writes `runs/<id>/feedback.jsonl` from the engines' own
   records, never guessed, and prints a digest whose last line is the ledger's Actual cost; tokens are kept in parts
   (new input, cache read, output), only ids, numbers, paths and status are written (the repo is public), and every
   parser fails loudly when an engine changes its format.
12. **Design decisions cite their evidence** — every design decision cites the finding ids it rests on (items 9,
   10); one with no source is marked *model knowledge*, treated like a `read` claim, and may not drive a node that
   builds until checked against a source or by running code; the researcher and explorer gather, the COO designs; the
   codebase comes first for a feature in an existing system (case C), current docs first for a new stack (case D).
13. **Code holds what needs no judgment** — the rules it serves are `docs/HARNESS_REQUIREMENTS.md` (R11 results can
   be judged, R12 failures and great successes improve the harness; R13, use cases and requirements, is kept in
   the `requirement-check` skill); the skill's `guard/` package (bun, TypeScript, no dependencies) runs at
   fixed points, so an agent cannot skip it once it is installed: before an engine call it lints the command against a
   trap catalogue (`guard/data/traps.yaml`; only `approved` entries act); after the call it treats a missing or empty
   output, a known silent-failure text or a failing exit as a failure (exit 0 is not success) and logs it to
   `.harness-guard/journal.jsonl` with its evidence. **What the guard sees is evidence, not a failure (R12.2):** a
   failing test run, an errored call, a non-zero exit, criteria written late. A failure is what the evaluator judges
   wrong against the product's vision, use cases and requirements, or a correction from the owner (`fail --found-by
   evaluator|owner`); only those block the stop until an insight answers each (whys to a changeable source, the root
   cause, 2–3 fix options with evidence) and the final message names it. The agent applies the option it ranks first
   and reports it; the owner may overrule (R12.3); each fix is recorded in `insight-decisions.md` beside the insight,
   and its lesson filed in the agent-lessons store (`.claude/skills/agent-lessons/`) when it holds for an agent type or
   every agent.
   It also learns from success (R12.7): every checked result that passed is one `success` line, so `guard/src/cli.ts
   rates` reads failures against how often a check ran; a session with successes is asked once for its **path**
   (`path new`, then `path check`); a great success gets a `## great:` insight section; and a similar task borrows a
   recorded path as its parent (`path parents <category>`), changes at least one thing and tries to be 2% better —
   reported, never a gate. A result is scored as the share of its criteria met: before the work the agent writes the
   criteria (`guard/src/cli.ts criteria new`, from a use-case register with `--from-register`), marks each met or not
   met with evidence at the end, and every criterion not met becomes a failure (`criteria score` prints the score).
   Judgment stays with the agent: the whys, the options, use cases and their fails-if. Installing the hooks is
   the owner's (`guard/src/cli.ts install --print <harness>`); the agent changes a harness config only after the
   owner's yes to that diff (R12.3). Measured once
   (`runs/20261015-ts-hybrid/effectiveness/`, n = 3 per arm on one short task): with the rules in the working folder,
   agents followed them without the hooks; the hooks caught a format slip the rules let through and, after one round of
   fixes, cost no extra time. Not measured: a long session where the rules are out of reach.
14. **A time-boxed run asks the experts, not the owner** (SHOULD; n=0). **The time is asked at the start:** when a task
   starts, the agent asks the owner, with the task's details, how much time it has to try to find a solution — a time,
   or a number of rounds — unless the owner already gave it. When the project owner gives a task a limit —
   a time, or a number of rounds (a round is one pass from the criteria to the score and the path, R12.7; each round
   after the first borrows the previous round's path; given both, the run ends at whichever comes first) — the run
   settles its own questions before the limit, and asks
   the owner only about one it could not settle:
   - Every question that would go to the owner — an unclear spot of kind *decision* (3.3), a suggested use case or
     requirement to accept (R13.1, R13.5), a blueprint question, a choice between options — goes to the experts
     (the `six-experts` skill: the experts 3.3 or 3.5 names for that step, or all five where no step names them),
     run as the saved workflow `.claude/workflows/experts-decide.js`. The main agent decides from their advice and
     writes the decision into the state file as **provisional**: the
     question, the choice, the reason, and the experts' run folder.
   - **Vision and use cases first.** Every question to the experts carries the vision and the use cases the work
     serves (the question templates have the slots; `time-boxed-decision.md` for a decision no step names). With no
     vision yet, the first provisional decision is one, written from the request and its research.
   - **Research and data, not recall.** Before a question goes to the experts, the run researches it (the researcher
     role, or Codex with `--search`) or measures it, and saves the findings, labelled verified / reported / measured,
     in the run folder; the experts get that file and cite its finding ids. A provisional decision cites at least one
     finding or measurement; a point that rests only on an engine's training data is labelled *recall* and does not
     decide alone.
   - A provisional decision binds for the rest of the run. When the run ends, the owner accepts or declines each one;
     work resting on a declined one is marked to redo, never deleted.
   - **Asking the owner: after three trials, within the time given.** A trial is one provisional choice tried and
     checked; one that fails its check is a failed trial (logged, R12.2), and the next trial takes the experts' next
     option. A question goes to the owner, for a discussion, only after three failed trials on it, or once the time the
     owner gave is used up, whichever comes first — with the trials, their checks and the experts' folders. While it waits, the run goes on
     with every piece that does not rest on it.
   - The limit is the owner's go-ahead for the engine calls the run needs inside it, the experts' included.
   - At the start the agent writes the deadline (start time plus the limit, or the last round) into the state file,
     checks it before every step, and works until the time is up or the run times out; then it stops trying and
     writes the report: what was built, every provisional decision, every failure and insight, and what is left open.
   - **The agent is told the time; it does not keep it.** It cannot feel time pass, so the guard keeps a time limit:
     `guard/src/cli.ts deadline start --minutes N --run runs/<run>` at the start (a limit in rounds has no clock: the
     state file holds the last round and the agent checks it before each round); after that the hooks add a one-line
     clock after every Bash or file-write call (the calls the guard watches), and after the deadline the time-up line
     on every such call. There is no fuller block at set points — those marks were removed (EJ: "not able to well
     predict, specific when exploring solutions"). The workers' progress is read with `deadline status`, not shown in
     the hook's context. `deadline status` is the check the agent can run; `deadline wait`, run in the background, is
     a timer that returns at the deadline; `deadline end` stops the clock when the task finishes early.
   - **Workers report while they work.** Every brief tells the worker to divide its task into small pieces, list them
     first, and append a timestamped line as each starts and ends (`docs/workflow-templates/node-brief.md`, "Pieces and
     progress"); the six-experts runner writes the same lines per expert (`--progress`). The main agent sees progress
     and duration during the run, not only the end.
   - **Workflows when possible.** Work with more than one node runs as a workflow — a script that orchestrates the
     agents in phases with visible progress (`.claude/workflows/`, the harness's Workflow tool where it has one) —
     rather than as hand-dispatched calls or one long prompt. Three are saved for a time-boxed run; each script's
     `whenToUse` gives its args (the one copy): `experts-decide.js` asks the experts one question, reruns an expert
     with no usable answer once, checks each answer and writes the comparison; the main agent still decides.
     `crossed-build-check.js` has tests written on another engine than the code's, shows each new test failing on the
     base commit, runs them on the head and has the work reviewed. `review-enhance.js` reviews a built tool on two
     read-only engines, judges each finding against the tool's vision, use cases and requirements, reproduces the
     accepted ones as failing tests, has the code engine fix them, loops until a review finds nothing new, then builds
     the experts' top enhancement the same way. They replace running those rounds by hand. Every brief they give an
     engine carries a Lessons section, the text of `guard/src/cli.ts lessons for --agent <engine>`.
   - Safety bounds still wait for the owner (MUST), limit or not: a push, a message sent, a deletion outside the run's
     branch and folder, a harness's config, `SPEC.md` or `DECISIONS.md`, spend beyond the limit. The run works around
     it (a branch, a draft) and lists it in the report.

   Fails if: a task starts with its trial time neither given nor asked; a time-boxed run asks the owner about a
   question before three failed trials on it or before the time given is used up; a question stays on trials past
   three failures or past the time given without going to the owner; the run stops waiting
   when pieces that do not rest on the question remain; a provisional decision has no reason or no
   experts' run folder; a question to the experts carries no vision or no use cases; a brief asks for no small
   pieces or no timestamped progress lines; a run limited by time starts no deadline; a provisional decision cites no
   researched finding or measurement, or rests on recall alone; the run goes past its limit; the report leaves out a provisional decision; a safety-bound
   action is taken without the owner.

## 4. State and memory

The state lives in a file (`docs/workflow-templates/state.md`). Each agent reads it, does one step, writes the new
state back; the next agent, or another tool, continues from there, and a broken run resumes from the last written
state. One writer at a time. The state file holds progress and results, never a worker's reasoning; a worker's
detailed notes go in its own output file, so a verifier can be kept blind to them.

Of the kinds of memory an agent has (Appendix B), **files in the repo** are the one every tool and every agent can
read — use them for anything that must last.

Working rules: each agent gets a brief with only what its piece needs (with a template, an example and a standard, 3.8) and writes its full result to a file; research and decided designs are files too (3.8, `docs/research/`, decision entries in `project-memory/entries/`); the
main agent keeps conclusions, not details; stored knowledge carries a date and is rechecked before it is relied on;
knowledge (stable) is kept apart from state (changes every run).

**Memory in a designed workflow.** Agents do not use memory well on their own: their tool loads a fixed set of
files, and anything past that is read only if the model decides to (`runs/20261013-memory-in-workflow-design/report.md`
§1, my reading; E1 and E2 measured invoking a skill or a tool, not reading a file). So the design decides, for every
node, what memory reaches it and what it writes; nothing is left to a reminder the agent may skip. Project memory
follows `docs/memory-system/SOURCE_OF_TRUTH.md` and its caches follow `docs/memory-system/CACHES.md`; the method does
not repeat their rules. It applies them per node, in the fields every node already has (3.6; the skill's "Every node
carries five things"), in the table below.

**Until a product has `project-memory/`.** A product that already keeps `docs/blueprint/decisions.md`, `changelog.md`
and `lessons.md` keeps writing them under the rules this section had before 2026-10-13 (`docs/METHOD_CHANGELOG.md`),
until that product's owner moves it to `project-memory/`. The table below still applies, read
against those files. Nothing in this change moves or deletes them. A new product starts with `project-memory/`; the
first node that writes an entry creates the folder.

| Field | Memory in it |
|---|---|
| **Context** — memory in | The entries the node needs, named by id or by the paths they cover (SoT Rd4.1), and how they reach it: their text inside the brief, or by an import where the engine has one, so the node does not have to choose to read them. A brief that carries an entry's text is an on-demand read for the node's task (SoT Rd4), not a session-start load (EJ, 2026-10-13: *"apply all"*, on the COO's recommendation). A start hook carries only the four session-start reads (SoT Rd2.1); entry bodies are never loaded by a hook (SoT Rd2.2). A sentence asking the node to read an entry is the fallback, used only where neither the brief nor an import can carry it, and the design says so (SoT Rd2.1). What it must not receive: a verifier gets no worker's reasoning, and no entry or journal that carries it. |
| **Contract** — before acting | Before editing a file, the node reads the entries whose `covers` include it (SoT Rd4.1). Before acting on a decision or fact, it checks it against the code, test or commit it points to; a mismatch is reported in the state file and to EJ, not settled (SoT Rd5.1, Rd5.3). Two cases are not mismatches: a decision with no `done:` yet whose code is still being built, and the node whose own task is that change (SoT Rd5.4). |
| **State** — memory out | What the node writes, and when: a decision or fact before the code it governs, and a human correction at once (W5.1); `done:` on a decision to build something when its work is complete (W5.3); raw notes to the task's `journal/` (K5.1), read at the end of the task and before a handoff, turned into lessons, observations and hypotheses, with that read logged in `state.md` (W5.2, K5.2); `INDEX.md` regenerated in the same commit as any entry (K6.2). The node's return lists the entries it wrote, and its check fails if a required one is missing (this method's rule, not the design's; n=0). |
| **Tools** — the caches | A cache is never loaded at start (CACHES Rd1). Each is used only once it exists, after its own trigger fired: full-text search for a free-text "what do we know about X" question (B1.1), and the vector index when the question's wording may differ from the entry's (B1.2; built after the full-text index, a *proposed* policy). Otherwise `INDEX.md`, grep, then read the entry. Exact strings, "every entry covering X", "have we never…", header fields and "why" questions go to the files, never to a cache (CACHES § When to use which store). A cache answer names its entry (CACHES Rd2.1), and the node reads that entry before acting on it (SoT Rd5.1). |

An engine's own built-in memory (Claude Code auto memory, a subagent's `memory` field, Codex memories) is not part of
the design: a rule a node must follow lives in the repo files that reach it, never only in one engine's memory (report
M14, T6; no run has broken such a rule, so the harm is not measured).

A release note is for users, not for agents: it says what shipped, not why, so it is an output of the run and not
memory. A product on `project-memory/` keeps one, in the blueprint's `changelog.md` (EJ, 2026-10-14: *"yes want a
release note"*, to 老子's proposal in the review of 2026-10-13). The node whose work ships adds its entry when the work
ships, written from the decisions' `done:` lines (SoT W5.3) and the commits.

Caution on graphs: this repo built two graphs nobody queried and then deferred a third. Its rule — "no node or edge
type without a listed query" — applies here too (`docs/KNOWLEDGE_GRAPH_DESIGN.md` §1, `docs/STORE_DESIGN_DECISION.md`).

## 5. Three qualities every design must show

- **Predictability** — the edges schedule and stop conditions are written before the run (3.6), attempts are
  bounded (3.5), and a cost estimate comes before the run (3.4, 3.8 item 2).
- **Debuggability** — each node labelled and its input, output and state in files (3.6, §4), small enough to rerun
  alone (3.4), with feedback kept per attempt (3.5, 3.8 item 11).
- **Quality control** — a check per piece that can fail (3.5), a blind verifier and a contradiction check at joins
  (3.6), the three-part stop for the final "what is missing" pass (3.6); skipped or unrun checks reported.

## Appendix

Reference detail, moved out of the main flow on 2026-10-08 (`docs/METHOD_CHANGELOG.md`).

### A. One word, one job

| word | one job |
|---|---|
| `check` | a node's success test — the field in a design and a plan |
| `validate` | is a document well-formed (`validate_plan`) |
| `verify` | run a node's success test (`verify_node_result`) |
| `probe` | inspect the environment (`probe_binary`, `probe_blueprint`, …) |
| `compare` | plan against design (`compare_plan_to_design`) |
| `checklist` | the judged fixed list |
| `accepted` | the run's own gate passed: every claim traces to a sourced row and the result is internally consistent. It does **not** mean the claims are true — no source is re-read independently, so a wrong paper, a bad number, or a conclusion the source does not support all pass. Whoever reports one names the check's author and what it does not establish (`CLAUDE.md`, "Quotes, labels, and who wrote the check") |

### B. Kinds of memory (§4)

Kinds of memory when running in Claude Code or Codex with subagents:

| Memory | Limit |
|---|---|
| Context window | Temporary; a subagent starts with only its prompt; long sessions get summarised |
| `CLAUDE.md` / `AGENTS.md` | Loaded every session, so keep them short and let them point to the rest |
| Claude Code auto-memory | Only Claude Code reads it |
| **Files in the repo** | The one memory every tool and every agent can read — use it for anything that must last |
| Skills | How to do things, not facts about a task |
| Run records (workflow `journal.jsonl`, the Ancient Games journal) | Nobody reads them unless asked |
| A subagent's final report | All that comes back; the rest is lost unless written to a file |

### C. Concurrency: name the unit (3.7)

Different things get called "parallel":

| phrase | what it counts | does an idle one count? |
|---|---|---|
| **resident sessions** — the harness's `@deepseek-ai/dsh-subagent` `maxActiveSubagents`, default **8**, `maxDepth` **1** | child sessions that exist and can be continued | **yes** — a continuable subagent waiting for its parent still holds a slot |
| **engine processes alive** — the dispatcher's pool (`MAX_ENGINE_PROCESSES` in `scripts/dispatch.py`) | `Popen` calls that have not exited | no |
| **candidate approaches** — the spike rule in `TASK_TYPES.md` | approaches tried for one question | n/a |

**8 resident sessions can be one working. 8 processes are 8 working.** They are not the same quantity. Read the
harness's ceiling from the harness when you need *sessions*; pick the pool size on its own merits when you need
*processes*, and mark it unmeasured until someone measures it. **Never write "running in parallel" without saying
which of the three you mean.**
