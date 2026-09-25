# Workflow design method

Agreed between EJ and Claude on 2026-09-20. This is the method this folder uses to turn an incoming challenge into
either a prompt file or a workflow design. It has been tried on nothing yet: every number and every piece of
"evidence" below comes from one session (n=1) and is not to be built on as a rule until it has been used on real
challenges.

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

If you can state the problem, the fix and the check in one sentence each, and being wrong would show itself at
once: write the prompt file by hand from `docs/workflow-templates/prompt-file.md`, or just do the task. Running the
intake workflow on such a task costs more than the task.

## 3. The steps

### 3.1 Readiness — always first

For the task, and later for each piece, list:

- **Tools**: the commands, scripts and connections needed, each with the command that proved it works. Run it; do
  not assume.
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
| New product | all eight |

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
- Risk is judged separately from size: how late a mistake would be noticed, whether it can be undone, how many
  things it touches. Tiny but risky → the prompt file gets one independent check.

Anchors for the number 3: Gate splits capability lists over three (`ancient_games/stages.py:109`) and the
concurrency cap is 3 (`ancient_games/registry.py:24`).

### 3.5 Clear pieces run as loops

While the unclear spots are being resolved, the pieces that are already clear and not blocked run as loops: a
defined output, the agent attempts, the check runs, pass → close the loop, fail → the feedback goes back to the agent.

A piece is loop-ready only if it has all five:

1. A check. Best is a script; next a fixed checklist judged by a separate agent; last EJ's own judgment.
2. A limit on attempts.
3. Specific feedback: the script's real output, not just "failed".
4. An exit for when the limit is hit: the piece goes back to the unclear list or to EJ. It was not as clear as it
   looked.
5. A check the worker cannot edit, and that is known to be able to fail (the house sabotage check).

A loop only closes when its check is objective. (n=1: a planner/critic loop whose check was "try to reject it" ran
three rounds, 6 → 5 → 4 problems, and never closed. See `20260919-plan-critic-issues.md`.)

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
| **Contract** | the intent, the stop condition, what comes back and in what shape, what may and must not change | `INTENT`, `STOP`, `OUTPUT`, `SCOPE` (`ancient_games/schema.py`) |
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

With everything known, the script schedules; agents do not decide who works next. If a node hits its attempt limit
it returns to the unclear list and only that part of the graph is planned again.

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

Working rules: each agent gets a brief with only what its piece needs and writes its full result to a file; the
main agent keeps conclusions, not details; stored knowledge carries a date and is rechecked before it is relied on;
knowledge (stable) is kept apart from state (changes every run).

Caution on graphs: this repo built two graphs nobody queried and then deferred a third. Its rule — "no node or edge
type without a listed query" — applies here too (`docs/KNOWLEDGE_GRAPH_DESIGN.md` §1, `docs/STORE_DESIGN_DECISION.md`).
Not verified: Codex's memory and subagent features beyond `AGENTS.md`.

## 5. Three qualities every design must show

| Quality | What must be there |
|---|---|
| **Predictability** | The script schedules; fixed bounds on attempts, pieces and concurrency; structured outputs; stop conditions and success criteria written before the run — for a product change, the acceptance criteria in scope; a cost estimate before the run |
| **Debuggability** | Every agent labelled; each step's input and output saved to a file; pieces small enough to rerun alone; resume from the failed point; feedback kept per attempt; state in one place |
| **Quality control** | A check per piece; a verifier that does not see the worker's reasoning; proof the check can fail; a contradiction check at joins; a final "what is missing" pass, measured against the three-part stop of 3.6 (a failure there is a failed attempt; anything else it finds goes to the backlog); skipped or unrun checks reported |
