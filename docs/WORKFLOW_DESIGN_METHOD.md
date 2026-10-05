# Workflow design method

Agreed between EJ and Claude on 2026-09-20. This is the method this folder uses to turn an incoming challenge into
either a prompt file or a workflow design. It has been tried on nothing yet: every number and every piece of
"evidence" below comes from one session (n=1) and is not to be built on as a rule until it has been used on real
challenges. The tier rule in 3.5 was added on 2026-09-22, and the restatement step 3.0 on 2026-10-01; neither has
had a run at all (n=0).

Runnable form: `.claude/workflows/intake.js`. Templates: `docs/workflow-templates/`. Runs: `runs/<run id>/`.

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
workflow on such a task costs more than the task.

## 3. The steps

### 3.0 Understand the challenge — before anything

(Added 2026-10-01 at EJ's request; extended the same day with the six whys and categorization; not tried on a
real challenge, n=0. Not yet encoded in `intake.js`; see `TODO.md`.)

From the challenge text alone — no tools, no agents, no repository browsing — state three things:

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
algorithm (since 2026-10-02; before, the category was fixed here and only checked against the facts).

A part that cannot be written, or a challenge that allows two readings, is the first **unclear spot** (kind:
decision, 3.3): a question for EJ with the restatement as the provisional assumption. No new blocking rule is
added: a prompt file's restatement stands on its provisional assumption like any decision, and a design's
question batch reaches EJ before anything runs.

The tiny test (§2) reads the restatement, not the raw text: tiny means the *restated* problem, fix and check are
one sentence each. A big-sounding challenge with a narrow objective stays small; a vague one ("improve
performance") cannot slip through as tiny.

The restatement, the why-answers and the provisional category go at the top of the output, beside the verbatim challenge in
the state file, so EJ sees and can correct what the run understood before tokens are spent.

Cost guard (trial 1, 3.4): this step is one paragraph and six short answers in the same session, never an
agent, never a tool call. On a tiny task it is the prompt file's first lines, so the cheap path stays cheap.

### 3.1 Readiness — always first

**`git` is not a requirement (EJ, 2026-10-05).** A run must work in a plain directory: where the product is a git
repository the run keeps a pre-run `git status --short` so it can tell what *it* changed, and where it is not, that
record is simply absent. Readiness checks the `git` **binary** because the tooling uses it when it is there — not
because a repository is required. The **baseline** never depended on git: it is the product's test command and its
output (`baseline.command`, gate rule G10), which is also why a `git status` snapshot can never stand in for it.
Before 2026-10-05 the runnable form ran `git status --short` unconditionally and a plain directory died at the first
step of every run (register 9.2).

For the task, and later for each piece, list:

- **Tools**: the commands, scripts and connections needed, each with the command that proved it works. Run it; do
  not assume. The skill's inventory script (`.claude/skills/workflow-design/scripts/readiness.py`) proves the
  standard set in one pass and marks every line verified / reported / unknown; what it cannot prove stays unknown.
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

(Added 2026-09-25 after EJ found that several projects never ended: their workflows built without a fixed target,
so every verify or review step could find more to do. Not yet tried on a real challenge; n=0.)

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
| Not a product change (research, a question, an analysis, an edit to documentation only) | none; record why, and the check ends here. It carries no acceptance criteria |
| Fix: restores behaviour the requirements already describe (if they do not describe it, it is a feature) | the requirement it restores, and the sections the fix touches |
| Feature: adds or changes behaviour | vision, requirements, and every section the feature changes |
| New product | all eight present; four settled before anything builds — vision, the first slice's requirements, the hard-to-reverse architecture choices as short decision records, the non-functional targets with runnable checks; the other four settled for the slice only, unknowns marked (EJ, 2026-10-03; was "all eight settled"; n=0) |

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

**Label the pieces (added 2026-10-02 at EJ's request; n=0).** Once the steps are written, group them into
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
| Kind | missing **information** → a research piece · a **decision** → ask EJ · **unknown** → a bounded explore loop |
| Blocks | which steps cannot start until it is resolved; everything else can start |
| Depends on | another spot whose answer might remove or change this one |

Questions for EJ go out as one batch, each with a provisional assumption so it can be answered in a few words.
In a prompt file a provisional assumption stands unless EJ corrects it; a workflow design's questions are answered
before the designed workflow runs, except blueprint questions, which hold back only the pieces that build on them.
Blueprint questions are the exception in a prompt file too: they need an explicit
answer before any step that builds on them runs (3.1, blueprint check). Where spots are resolved separately, one
joining step compares the answers. A contradiction is a stop: pick one and say why, never average.

### 3.4 Size

- Up to 3 steps and nothing unclear except decisions that have a provisional assumption → one piece → a prompt
  file, with those decisions listed at the top as questions for EJ. A spot of kind information or unknown always
  means a workflow design. (Changed 2026-09-20 after trial 1, where three decisions with obvious defaults helped
  push a one-line fix out of "small"; n=1.) Blueprint spots follow the same rule: a missing or incomplete section
  always means a workflow design; a draft section alone does not.
- More than 3 steps → consider a new piece. Split only if each part keeps its own check **and** splitting changes
  how the work is done ("Split iff it changes the route", `challenge-mediation` skill).
- **Health is a reason to split (EJ, 2026-10-05; n=0).** A long single attempt hides its failure and cannot be
  watched; a run whose work is cut into segments ends each one and can be looked at.
- **Size from an estimate, and never hand an engine one huge prompt (EJ, 2026-10-05; n=0).** A design guideline:

  > *"When we design the workflow, we don't ask a subagent to give a HUGE prompt that runs like 10 hours to Codex.
  > Since an LLM can already estimate the workload, better to divide into like 6 or more pieces of prompts that are
  > logical."*

  A model can estimate a piece's workload **before** it runs — use that, rather than discovering the size from a
  timeout. **A piece whose work is hours long is not a piece: split it into six or more logical pieces**, each with
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
that ledger is how the defaults earn their n. (Added 2026-10-01 at EJ's request; n=0.)

Anchors for the number 3 **in a piece's step count** (not a cap on roles or concurrency — that rule was deleted
2026-10-05, see 3.7): Gate splits capability lists over three (`ancient_games/stages.py:109`) and the
the plan-wide cap of 3 dispatched corroborating sources (`ancient_games/registry.py:24`, used at `stages.py:309`; it caps dispatches per plan, not agents running at once — corrected 2026-10-03).

### 3.5 Clear pieces run as loops

While the unclear spots are being resolved, the pieces that are already clear and not blocked run as loops: a
defined output, the agent attempts, the check runs, pass → close the loop, fail → the feedback goes back to the agent.

A piece is loop-ready only if it has all five:

1. A check. Best is a script; next a fixed checklist judged by a separate agent; last EJ's own judgment.
2. A limit on the **number** of attempts — a count, not a time limit. (Renamed 2026-10-05: it read *"a limit on
   attempts"*, and EJ read it as a time bound, which is 3.8's business. Two different rules were wearing the same
   three words.)
3. Specific feedback: the script's real output, not just "failed".
4. An exit for when the limit is hit. If the attempts ran on a cheap tier, the exit is a fresh node on a stronger
   tier with a short handoff note (the piece, its check, the last feedback) and its own limit. When that limit is
   hit too, or there is no stronger tier, the piece goes back to the unclear list or to EJ. It was not as clear as
   it looked. (Tier exit added 2026-09-22 at EJ's request; n=0.)
5. A check the worker cannot edit, and that is known to be able to fail (the house sabotage check).

A loop only closes when its check is objective. (n=1: a planner/critic loop whose check was "try to reject it" ran
three rounds, 6 → 5 → 4 problems, and never closed. See `20260919-plan-critic-issues.md`.)

Attempts start on the cheapest tier that could plausibly do the piece; a stronger tier, which costs many times more
per token, is bought only for what the cheap one could not finish. Escalation is a fresh node, never a tier switch
inside the running session: a switch voids the prompt cache, so the stronger tier re-reads the whole context at its
fresh input rate, and a session in which the cheap tier flailed is mostly wrong turns that would anchor the stronger
tier towards the same dead ends. (Added 2026-09-22 at EJ's request; n=0.)

### 3.6 The rest is a graph

When the spots are resolved and the clear loops have closed, the algorithm is fully defined:

- nodes = right-sized pieces (a node may hold its own loop);
- edges = "this piece needs that piece's result";
- gates = a result is verified before anything that depends on it starts;
- a joining node where branches meet.

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
2. what passed before still passes — everything recorded as passing in the **baseline**: the product's test command
   and its output, written to the state file before the first node that builds starts;
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

With everything known, the design's edges decide who works next: a Workflow script, or the COO (the main Claude
session) following the graph. A node's role subagents do not choose the next node. Each node names its role, engine,
model and effort; the COO's contract, and when she does a small node herself, are in `docs/EXECUTOR_KINDS.md`. If a node hits its attempt limit
and its tier exit is spent, it returns to the unclear list and only that part of the graph is planned again.

**The design and the runnable plan are two artifacts, and the COO writes both (EJ, 2026-10-05).** The design carries
the plan of work — categories, checks, edges, loops — and the gate validates it. The plan (`plan.json`) carries what
a run needs to execute — each node's engine as a bare name, its model, its timers, its brief path — and the
dispatcher validates *its* internal consistency. **They are compared, since 2026-10-05.** This was decided as *C — leave it* earlier the same day, on the reasoning
that one author writes both and can see both, so a checker would guard against someone standing right there.

**C was revisited the same day, because a traversal measured the cost.** One real challenge was run end to end:
`intake` → design → gate → plan → dispatch. The hand-written plan **silently dropped two of three nodes' checks**,
plus `touched_paths`, the baseline, the categories and the estimate — and `check_plan` said *"plan ok"*. Every
validator agreed while two checks had vanished, and a node with no check reports **done**.

So `dispatch.py check PLAN --design DESIGN` now compares the two, and `run` refuses a plan that loses the design.
The comparison is **asymmetric on purpose**: a plan carries what a design does not (a bare engine name, an exact
model, timers, a brief path, a role), so equality is wrong. **The design's promises must survive; the plan may add
and may not lose.** Without `--design` the command **says so** on stderr rather than passing silently.

*The first measurement of a decision's cost changed the decision. That is the argument for traversing a chain once
rather than reasoning about it.*

Whole picture: graph on the outside, loops inside the nodes, exploration only inside the unknown-spot nodes. This is
what `20260919-state.md` calls combined execution.

### 3.7 Sequential first; parallel is the last decision

Design the whole flow as sequential, state-based steps: read the state file → do one step → write the state back.
Only when the design is complete, look for tasks that are **really independent** — all five must hold:

1. neither needs the other's result;
2. no shared files or resources;
3. doing one would not change how the other is done;
4. each has its own check;
5. the time saved is worth the extra joining step.

Parallel buys only clock time, and it costs predictability, debuggability and extra joins. Independence of
verifiers is about what they see, not when they run: two verifiers can run one after another and stay independent.

**Caps — deleted 2026-10-05 (EJ: "not logic at all").** A rule here read *"at most 5 subagent roles per run and at
most 3 running at once"*. It was removed once its numbers were traced: they are the **spike rule's** in
`docs/TASK_TYPES.md` — *"run at most 3 in parallel"*, *"up to 5 in a round"*, both about candidate **approaches** for
one question — re-labelled as a rule about **roles** and **concurrency**.

The two halves were never the same kind of thing, which is why the sentence would not parse:

* **5 roles** counted distinct `role` values over a run's nodes — a property of a *design*.
* **3 running** counted engine processes alive at one instant — a property of the *machine* (the dispatcher's worker
  pool, now the constant `MAX_ENGINE_PROCESSES` in `scripts/dispatch.py`).

The pair survives where it belongs, in the spike rule, still about approaches. `check_plan` no longer refuses a plan
for having many roles or a wide parallel group; the budget keeps `max_rounds` and `max_calls`, which are limits on
*attempts* and are required by 3.5. **If a run needs many roles, that is a design question, not a cap.**

**Concurrency: name the unit, because four different things get called "parallel".** (EJ, 2026-10-05: *"how many
running in parallel is even more weird"* — right, and this is the whole reason.)

| phrase | what it counts | does an idle one count? |
|---|---|---|
| **resident sessions** — the harness's `@deepseek-ai/dsh-subagent` `maxActiveSubagents`, default **8**, `maxDepth` **1** | child sessions that exist and can be continued | **yes** — a continuable subagent waiting for its parent still holds a slot |
| **engine processes alive** — the dispatcher's pool | `Popen` calls that have not exited | no |
| **candidate approaches** — the spike rule in `TASK_TYPES.md` | approaches tried for one question | n/a |

**8 resident sessions can be one working. 8 processes are 8 working.** They are not the same quantity, and using one
number for the other is the mis-transcription that produced the deleted "5 roles and 3 at once" rule. So: read the
harness's ceiling from the harness when you need *sessions*; pick the pool size on its own merits when you need
*processes*, and mark it unmeasured until someone measures it. **Never write "running in parallel" without saying
which of the three you mean.**

### 3.8 Running a node: executors are tools, timers, pass-back, no polling

(Added 2026-10-02 at EJ's request. n=0: every number below is a provisional working value that the ledger replaces
with measured ones. Not yet encoded in `design_gate.py` or `intake.js`.)

The COO (the main Claude session) is the leader and holds the thinking. Codex, `agy`, `qwen` and role subagents are
**tools** she calls: agents are not yet stable (a call may stop half-way, return nothing, or return something
malformed), and every exchange with them costs the COO a turn that re-reads her whole context. So:

**Before any of it: know which binary will make the call, and what version it is.** A provider can bundle its own
copy of an engine, older than the copy on `PATH`, and the two do not accept the same model names — the error blames
the model or the account, never the version. Check the catalog of the binary that will actually run, and record that
version in the canary. `docs/EXECUTOR_KINDS.md`, "The bundled-runtime trap", has the three instances that cost this
project three diagnoses in two days.

1. **One small task per call.** A call has one deliverable, one command line and an expected finish inside its
   timeout. A loop is not inside the call: if a piece loops, the COO or the script runs the loop and each attempt is
   a fresh small call (3.5). A piece too big for one bounded call is not handed over whole; the COO splits it only
   where 3.2's "a label is not a node" allows (own check, different kind, or context room).
2. **Two timers per call, both named in the node.** The *inner* timer is the tool's own (`qwen --max-wall-time`,
   `agy --print-timeout`; `codex exec` has none verified, so it relies on the outer one). The *outer* timer is a
   `timeout` around the whole command, a little longer than the inner. Timeout values scale with the task; the
   provisional sizes are: classification or lookup 60–90 s (the canary's figure), one-file change or one-file test
   set about 5 min, diff review about 5 min, research about 10 min. The design lists them with its cost estimate,
   and the ledger records actual wall time so the numbers get replaced.

   **But no single call runs longer than the ceiling: 8 hours (EJ, 2026-10-05; n=0).** The per-task timers scale;
   the ceiling does not. Past it the run is not healthy and cannot be monitored — a call that has been going for
   hours has hidden its failure, cannot be watched, and leaves nothing to resume from. A call that hits the ceiling
   is an **executor failure**, so it blocks the node and reports (there is no fallback). **`check_plan` refuses a
   node whose `outer_timeout_s` is past the ceiling**, so this is enforced before the run, not remembered.

 **This is the reason long
   work is cut into segments**: not only cost — a segmented run is healthier and easier to monitor, because every
   segment ends and can be looked at.
3. **No polling.** The COO never repeats "is it done?" and never sleeps in a loop; each check is a turn. She waits
   in one of three ways: a blocking call under the outer timeout; a background run that notifies her when it
   exits; or a small script that waits and prints one line `done|fail|timeout <result path>`. A progress file the
   tool writes is read only after a timeout, to see how far it got. The design states the COO turns it expects per
   node (provisional: two, dispatch and accept) and the total.
4. **Pass-back contract.** Every call writes one result file in the node's own path
   (`runs/<id>/nodes/<node>-<attempt>.result.*`), written to a temp name and renamed, with a fixed header: node,
   attempt, engine, model as the tool reports it, `status: ok|fail|partial`, start and end time, evidence path;
   then the body (`docs/workflow-templates/result-file.md`). A **script** (no model,
   `.claude/skills/workflow-design/scripts/validate_result.py`) validates it: the file exists and is not empty, the
   header parses, the status is present, the reported model, node and attempt equal the contract's, the evidence
   path exists. The COO reads the capped summary (provisional: the
   header and the first 40 lines) and the path, never the raw output.
5. **An unstable return is a failure of the executor, not of the work.** All of these count: no file, empty file,
   unparseable header, wrong model, a timeout, and a clean exit with no result (`qwen` headless exits 0 with no file
   when its write tools are withheld; a wrong `-m` exits 0 and silently runs another model — both seen
   2026-10-02, `docs/EXECUTOR_KINDS.md`). `partial` is a status the COO decides on: retry only the remainder as a
   new small call. Executor failures follow the existing rule: they do not count against the attempt limit, the
   node is **blocked** and goes to EJ. There is no fallback (removed 2026-10-05): one engine per node, and a
   failure reports rather than hopping to an engine nobody chose.
6. **A half-finished node must not leave a mess.** A node that builds writes only inside its contract's "may
   change" paths, and runs from a clean commit or a worktree, so a failed call is discarded whole. The COO never
   reverts files by hand to "tidy up": a revert of anything but a discarded worktree is a Rule 6 confirmation.
7. **Keep the COO's reading small.** Results by path, one-line Log entries, only the state rows the next step
   needs. Raw tool output never enters her context.
8. **The stronger model gives the worker a template, an example and a standard** (EJ, 2026-10-02: this is the
   COO's real work). The COO is the smarter model and the worker is a tool, often a cheaper one; so every brief
   carries (a) the **template** the result must follow, (b) one worked **example** of a good result, small and
   real, and (c) the **standard** it will be judged by: the check as the worker can run it, what failing looks
   like, and the sabotage the check is known to catch. The COO writes these once, in the brief
   (`docs/workflow-templates/node-brief.md`), instead of correcting the result afterwards: it cuts unstable
   returns, retries and her own review reading. A brief with no template, no example or no standard is not
   dispatched; a part she cannot write is an unclear spot (3.3).
9. **Research is written to files.** The *researcher* reads docs, papers and the web (WebSearch, WebFetch). A
   research node writes the full findings to
   `docs/research/<date>-<topic>/FINDINGS.md` (each finding with an id, a source and a label) and returns only a
   digest of about 15 lines, no more than 20, plus the path (`docs/workflow-templates/research-file.md`). The COO
   reads the digest; to settle a doubt she reads one finding by id, or sends a small verify node. A design decided
   from the research goes to `decisions.md` (4).
10. **Exploring existing code is its own role** (EJ, 2026-10-03; n=0). The *explorer* reads the existing system —
   code, tests, configs, git history — never the web. The two roles differ in source, tools, evidence and how a
   claim is checked (`docs/EXECUTOR_KINDS.md`, roles). Its contract:
   - **Read-only**, under a stated budget (tool calls or tokens), favouring recall inside the affected area and
     never a repo-wide overview (TASK_TYPES, case C).
   - **Every claim carries file:line and a short verbatim quote**, and `scripts/quote_check.py` confirms each quote
     is at its line (`docs/workflow-templates/explorer-file.md`); a quote that fails is a failed finding, not a typo.
   - **Every behaviour claim is marked `read` or `ran`.** `read` = inferred from the code; `ran` = confirmed by
     running it (a test, a differential run, `~/skills/verify-extraction`). Only `ran` claims may feed a node that
     builds; a `read` claim a build depends on is an unclear spot until it is run.
   - It returns a digest and the path, like research: the impact map (case C), the old system's behaviours and
     golden outputs (case B), or the findings for use cases #1 and #2.
   - The COO explores herself when the affected area is small and fits her context (whale rule); an explorer node
     is for a large or unfamiliar codebase.
11. **Every run leaves a feedback record** (added 2026-10-02; n=0; `docs/research/20261002-workflow-feedback`).
   During the run, `scripts/runlog.py exec` wraps each Codex, `qwen` or `agy` call (start, end, exit, duration;
   raw output to the gitignored `runs/<id>/raw/`) and `runlog.py verdict` writes one line per node check. After
   it, `scripts/harvest_run.py` reads what the engines already recorded (Workflow run JSON and agent transcripts,
   Codex rollouts joined by time window and cwd, never guessed) into `runs/<id>/feedback.jsonl` and prints a
   digest whose last line is the ledger's Actual cost. Tokens are kept in parts (new input, cache read, output):
   cache reads are often ten times the new input. Only ids, numbers, paths and status are written; the repo is
   public. Every parser fails loudly when an engine changes its format.
12. **Design decisions cite their evidence** (EJ, 2026-10-03; n=0). Model memory goes stale, so every design
   decision cites the finding ids it rests on — research (item 9) or exploration (item 10). A decision with no
   source is marked *model knowledge* and treated like a `read` claim: it may not drive a node that builds until it
   is checked against a source or by running code. The researcher and explorer gather; the COO designs, so their
   picks do not become the design without a second look. Which source comes first depends on the case: the
   codebase for a feature in an existing system (TASK_TYPES case C), current docs for a new stack (case D).

## 4. State and memory

The state lives in a file (`docs/workflow-templates/state.md`). Each agent reads it, does one step, writes the new
state back; the next agent, or another tool, continues from there, and a broken run resumes from the last written
state. One writer at a time. The state file holds progress and results, never a worker's reasoning; a worker's
detailed notes go in its own output file, so a verifier can be kept blind to them.

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

Working rules: each agent gets a brief with only what its piece needs (with a template, an example and a standard, 3.8) and writes its full result to a file; research and decided designs are files too (3.8, `docs/research/`, `decisions.md`); the
main agent keeps conclusions, not details; stored knowledge carries a date and is rechecked before it is relied on;
knowledge (stable) is kept apart from state (changes every run).

**Project memory for software work (added 2026-10-02 at EJ's request; n=0).** A release note is written for users
after the fact; it tells an agent what shipped, not why or what to avoid, so it is an output here, not the
memory. A product keeps three small append-only files beside its blueprint, each existing to answer one listed
query (the rule above: no store without a query):

| File (`docs/blueprint/`) | Answers | Entry (kept to about 5 lines) | Written by, when |
|---|---|---|---|
| `decisions.md` | "Why did we choose X? What did we reject?" | date · decision · why · alternatives rejected · the R/N ids it serves · source (finding ids, or *model knowledge*, 3.8 item 12) | the COO, when a decision spot is answered (3.3) or a design choice is made; EJ's answers are the decisions |
| `changelog.md` | "What did run N change, and did it pass?" | date · run id · what changed · criteria covered (R1.1…) · commits · baseline result · optional `release note:` line for users | the COO, once at the end of each run that builds, from the state file |
| `lessons.md` | "What goes wrong around module Y?" | date · where (path or module) · the trap · how it was found · recheck by (a date or a trigger) | any node proposes, the COO appends; an entry past its recheck is marked stale, never silently trusted |

Working rules: append only, never rewritten (a reversal is a new entry that points at the old one); every entry
carries a date and, where it applies, a requirement id or a path, so an agent finds it by `grep`, not by reading the
file; readiness (3.1, information) and the design read only the entries for the sections, ids and paths the task
touches; the blueprint's `README.md` map lists the files so an agent knows they exist. A release note, when one is
needed, is generated from the `release note:` lines of the changelog, not written separately. The qwen findings of
2026-10-02 (silent model substitution, exit 0 with no file) are examples of lessons.

Caution on graphs: this repo built two graphs nobody queried and then deferred a third. Its rule — "no node or edge
type without a listed query" — applies here too (`docs/KNOWLEDGE_GRAPH_DESIGN.md` §1, `docs/STORE_DESIGN_DECISION.md`).
Not verified: Codex's memory and subagent features beyond `AGENTS.md`.

## 5. Three qualities every design must show

| Quality | What must be there |
|---|---|
| **Predictability** | The design's edges schedule (script or COO); fixed bounds on attempts, pieces and concurrency; structured outputs; stop conditions and success criteria written before the run — for a product change, the acceptance criteria in scope; a cost estimate before the run |
| **Debuggability** | Every agent labelled; each step's input and output saved to a file; pieces small enough to rerun alone; resume from the failed point; feedback kept per attempt; state in one place |
| **Quality control** | A check per piece; a verifier that does not see the worker's reasoning; proof the check can fail; a contradiction check at joins; a final "what is missing" pass, measured against the three-part stop of 3.6 (a failure there is a failed attempt; anything else it finds goes to the backlog); skipped or unrun checks reported |
