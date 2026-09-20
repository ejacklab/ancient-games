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
Where spots are resolved separately, one joining step compares the answers. A contradiction is a stop: pick one and
say why, never average.

### 3.4 Size

- Up to 3 steps and nothing unclear except decisions that have a provisional assumption → one piece → a prompt
  file, with those decisions listed at the top as questions for EJ. A spot of kind information or unknown always
  means a workflow design. (Changed 2026-09-20 after trial 1, where three decisions with obvious defaults helped
  push a one-line fix out of "small"; n=1.)
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
| **Predictability** | The script schedules; fixed bounds on attempts, pieces and concurrency; structured outputs; stop conditions and success criteria written before the run; a cost estimate before the run |
| **Debuggability** | Every agent labelled; each step's input and output saved to a file; pieces small enough to rerun alone; resume from the failed point; feedback kept per attempt; state in one place |
| **Quality control** | A check per piece; a verifier that does not see the worker's reasoning; proof the check can fail; a contradiction check at joins; a final "what is missing" pass; skipped or unrun checks reported |
