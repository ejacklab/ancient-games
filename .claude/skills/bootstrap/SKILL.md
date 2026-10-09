---
name: bootstrap
description: Bootstrap a new project's agent orchestration from the Ancient Games — generate its AGENTS.md (instructions) and orchestration.mdc (workflow-design + orchestration rules) from its blueprint, and adopt the Ancient Games style. Use when a project wants to work the Ancient Games way.
---

# Bootstrap a project's orchestration

Turn the Ancient Games knowledge into a new project's **standing** orchestration files. Run once when a project
adopts the style; after that the project's AIs read its own `AGENTS.md` + `orchestration.mdc`, not the Ancient Games.

Both files are read on **every** session in that project, so both stay short — they point at the rest, they do not
paste it (method §4, Appendix B). Write them for a first-time AI in that project: it has never heard of the Ancient
Games, and neither has whoever reads these files in six months.

## What you produce

1. **`AGENTS.md`** — the project's instructions: what the folder is for, where its blueprint is, its working rules,
   and the commands that test it. This is the **portable** instruction entry point. Consult
   `references/executor-kinds.md`, "Reads which instruction file", including its uncertain/reported labels;
   a harness's own file (`CLAUDE.md`, `GEMINI.md`, `QWEN.md`) points to the canonical instructions rather than a second
   copy. Where a project keeps its
   real instructions in one of those other names, that file is the one to write and `AGENTS.md` is its pointer.
2. **`orchestration.mdc`** — the project's orchestration rules: engines, checks, loops, the five referee stages and
   the feedback templates, instantiated for this project. Keep it at the project root as readable markdown;
   `.mdc` is a rules-file convention, not a guarantee that a harness loads it. Put this explicit instruction in
   `AGENTS.md` (or its canonical target): **Read `orchestration.mdc` before starting work in every session.**
   Preserve an existing harness registration if there is one; do not rely on it for other harnesses.

## Read the sources, then adapt

Locate the installed `workflow-design` folder beside this skill. Read its `SKILL.md`, then these files before
drafting; references below are relative to that folder, not to the adopting project:

| source | use it for |
|---|---|
| `references/method.md` §§3.0–3.8, §4 | design order, readiness, verified handoffs, node contracts, state and project memory |
| `references/task-types.md` | matching category, execution pattern, engine suggestion, check and sabotage |
| `references/executor-kinds.md` | role versus engine, exact model/effort, readiness probe and instruction-file support |
| `references/feedback-templates.md` | worker return fields and their meanings; retain any proposed/unsettled status |
| `assets/templates/blueprint.md` | blueprint sections, acceptance criteria and the map to existing project documents |
| `assets/templates/workflow-design.md`, `assets/templates/state.md`, `assets/templates/readiness.md` | per-run design, progress and readiness artifacts |

Also read the installed `requirement-check` and `meaningful-names` skills. If a required source is absent, report
the missing file and hold the part that depends on it; do not reconstruct its rules from memory.

## Before you write anything

1. **Look before overwriting.** Read existing instruction files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `QWEN.md`),
   their linked instructions and any existing orchestration rules before changing them;
   keep everything in them that is specific to this project, show the person what you would change and why, and wait
   for the answer unless the person already authorized those changes. The project's own file outranks the Ancient
   Games' defaults. Keep one canonical instruction file and avoid circular pointers. If `AGENTS.md` is only a
   pointer, its canonical target carries the instruction content and standing rules described below.
2. **Find the blueprint** — `docs/blueprint/`, one file per section, with a `README.md` map saying where each
   section lives (layout: `assets/templates/blueprint.md`). Use the map to select and read the relevant section
   contents, including linked specifications; the map alone is not the blueprint. Existing specs may stay in their
   own locations — map them instead of copying them. When the map is absent, identify the existing documents first.
3. **Judge each section this project needs** (method 3.1) — `settled` (the person accepted it, with a date) ·
   `draft` (proposed, not accepted) · `incomplete` (it exists but does not cover the needed work) · `missing` (absent).
   A missing or incomplete section is
   an unclear spot: an agent drafts it, the person accepts it, and a piece that builds never starts on a draft. If
   the project has no blueprint at all, say so and ask — an agent may write down the vision its owner has stated, and
   never invent one. The sections are vision, requirements, domain model, business logic, architecture, data model,
   UI/UX (user interface and experience), and non-functional requirements (performance, security and operating
   limits). Mark a section not applicable with a reason rather than inventing content for it.
4. **Collect the project facts.** Find its test/build commands in its own documentation and manifests, its actual
   task types, available engines, protected paths and approval owners. Distinguish observed facts from suggestions.
   Send unresolved choices as one questions batch, naming what each blocks. A provisional assumption is a proposal,
   not acceptance; missing units, thresholds and tests stay open. Draft known parts while waiting, but label the
   files as drafts and affected task types as blocked until their needed answers are accepted.

## How

1. **Write `AGENTS.md`** from the blueprint: the project's name, what it is for, where the blueprint is, the working
   rules and actual test/build commands with their working directory. Include the session-read instruction above
   and the installed skill locations. State each rule through `requirement-check` (source, one thing, unit, can it
   fail, weak words, level, basis, links); name things through `meaningful-names` (one word, one job). A missing unit or threshold goes to the person
   as an open question — never your own value.
2. **Write `orchestration.mdc`** by mapping **this project's** task types onto the Ancient Games defaults. The types
   come from the blueprint (a fix · a feature · a new product · research or a question), not from the Ancient Games'
   sixteen-row table: carry over the row that matches, and write a row of your own where the project has work the
   table does not name. A product-level type such as "feature" may map to several pieces, such as code generation
   and code review; it need not match one category. Record the source row/section for each mapping. Each mapped
   type gets a pattern, engine with exact model/effort, check with its expected result and owner, sabotage, loop
   limit counted in attempts, limit-hit exit and worker return-template reference. Use a limit only where the
   applicable source or the person supplies it; otherwise leave it open. A non-loop type says "no loop" and why.
   A custom row is a proposal until its unresolved choices are accepted, not an invented default.
3. **Fill in the five referee stages** — instantiate the decisions below for this project; only count-based
   stages need numbers. The referee *code* (`ancient_games/`) does not travel with this skill, so a project that
   adopts the bundle gets these five as written rules. Executable-referee adoption is separate; it requires the
   code, dependencies and contract documents, and verification in that project.
4. **Make the workflow usable.** In `orchestration.mdc`, state that the main session or workflow script follows
   the declared dependencies; workers do not choose the next worker. For each run, name the design and state
   paths under `runs/<run-id>/` (a project-local folder for one run). A node reads state, does its work, saves its
   result and evidence, and has that result verified before any dependent node starts. On failure, feed back the
   check's actual output and follow the bounded repair/exit rule; on success, pass the verified returns and evidence
   as the next node's input. Keep one state writer at a time, progress/results in state, and reasoning in worker
   notes withheld from verifiers. Joins compare branch results; a contradiction stops dependent work.
   Define each node's tools, given/withheld context, contract (intent, observable stop, returns, may/must-not-change),
   evidence path and state reads/writes. Its brief gives the return template, a filled example and the standard
   it will be checked against (method §3.8). A building node stops when its acceptance criteria pass, its recorded
   baseline still passes and its protected scope holds. Other discoveries go to the project's backlog.
   Keep execution sequential by default; refer to method §3.7 for all five conditions before permitting parallel
   work. Declaring knowledge dependencies does not require a graph database or a diagram.
5. **One copy per rule.** Point at the installed skills with resolved locations; do not paste their bodies into the
   project. The four standing rules below are the explicit exception: reproduce them verbatim in both files.

## `orchestration.mdc` — the shape

```markdown
# Orchestration rules — <project>
## Engines      — per task type: what runs it, on which model, at which effort (from executor-kinds.md)
## Checks       — per task type: the check that can fail, and the sabotage — the wrong answer it must catch
## Loops        — per task type: attempt limit · a check the worker cannot edit · the exit when the limit is hit ·
                  the feedback it gets (the script's real output, not "failed")
## Referee      — the five stages below, with this project's decisions and applicable counts
## Feedback     — the return shape per task type (from feedback-templates.md); every field is the worker's
## Workflow     — design/state paths, node declarations, verification before handoff, failure exit, joins and stop
## Rules        — who fills it · evidence in project · checked sequence · declared knowledge graph
```

This is an outline, not finished content: fill each section with the project's mappings or a resolved reference.
Do not leave unfilled project/model/command placeholders in a finished file; a documented path pattern such as
`runs/<run-id>/` remains a pattern, including in the standing rules. Put long mappings in a project-local companion file
if needed and link it; the session-read instructions and standing rules remain in the two standing files.

## The five referee stages

What each decides, and the default to write into the project:

| stage | decides | default |
|---|---|---|
| **Gate** | how many agents a task gets | ask the cheap means first — if a read answers it, nobody is dispatched; then one agent per independent angle the main session lacks; more than three and the task splits into groups of three |
| **Guard** | which actions need a person | per path or command: low stakes run, medium stakes stop at a checkpoint first, high stakes are approved by the person before the run |
| **Corroborate** | how many independent sources a load-bearing claim needs | required count is the action's stakes level (1 low, 2 medium, 3 high; from the referee's SPEC §4 B), including any higher owner-gated decision stakes; at most three corroborating agent dispatches for one plan, not a concurrency cap or a cap on cited documents/checks; record sources and unresolved disagreement; a claim with no source stays unproven and nothing builds on it |
| **Filter** | which candidates survive | drop a candidate dominated on cost, expected value, risk and confidence; concentrate on the branch that decides the objective; merge duplicates and record follow-ons; a person-gated candidate stops at that gate until the named person's approval is recorded |
| **Prove** | is the plan cleared | every claim shows the command that backs it, every action has a check that can fail, every metric names its unit; one finding sends the plan back to the planner, not into a run |

These are the Ancient Games' working values (n=0 — none of them has been measured outside the Ancient Games). A
project that changes one says which of its own evidence or owner decision says so — that is question 1, *source*, of
`requirement-check`.

For Guard, name the project's affected paths/commands, their stakes, checkpoint and approval owner from its
existing policy or the person's answer. Do not invent the policy. Gate's groups of three are task partitions, not
permission to run three workers concurrently. For Corroborate, independent means distinct evidence/checking
mechanisms or independently framed assessments, not copies of one source or repeated identical prompts. If the
required count cannot be met under the dispatch cap, disclose the shortfall and route to the named checkpoint or
owner gate; do not mark the claim proven. Record the five stage results in the run's state/evidence even when no
executable referee is installed. A Prove pass clears the plan's checks; it does not grant a pending human approval.

## Vocabulary for the receiving AI

Use these meanings in the generated files, inline at first use or through a short glossary; gloss any additional
project terms too. The skill names above also describe their jobs, rather than assuming the reader knows them.

| term | meaning |
|---|---|
| standing files / harness | instructions reused each session / the app or CLI that runs the AI |
| blueprint / acceptance criterion | the product's agreed target documents / an observable test of a requirement |
| baseline | the project's recorded test results before the run changes it |
| piece / node / edge | a bounded unit of work / that piece in the design / a declared dependency on another piece's result |
| building node / backlog | work changing product code, tests, schema, UI or configuration / the project's list of discoveries outside this run's scope |
| knowledge graph / DAG | declared needs, outputs and information boundaries / directed acyclic graph, a dependency topology that alone does not verify results |
| code graph | a tool's map of source-code relationships, distinct from the workflow's declared knowledge dependencies |
| role / engine / model / effort | the job / executor tool / exact model identifier / explicit reasoning setting, or documented lack of one |
| check / sabotage | a test or fixed judging checklist with a pass condition / a deliberately wrong example the check must reject, tried in an isolated fixture |
| loop / attempt / exit | attempt-check-repair repetition / one worker try evaluated by the check / where work goes when its attempt limit is reached |
| return / verdict | worker-filled result / a separately written verifier judgment or human decision; identify each writer |
| evidence / state | saved proof such as a command with output or file:line / the run's progress and results |
| join | a step comparing separate results before downstream work uses them |
| referee / stakes / checkpoint | five plan-review decisions / the action's project-defined risk level / a named pause and review before proceeding |
| load-bearing claim / dominated candidate | an assertion an action depends on / an option no better on any comparison axis and worse on at least one |
| follow-on / person-gated / terminal | newly discovered work needing its own review / waiting for the named person's approval / no automatic continuation past that gate |
| n=0 / SHOULD / MUST / guidance | unmeasured working value / default with a reasoned exception / work-stopping gate / advice; preserve each source's level |

## The rules every generated file must carry

- **Every field has one writer** — a return template is the worker's; a verdict is the human's. Name who fills it.
- **Evidence lives in the project** (`runs/<run-id>/` by default, SHOULD — a written reason may override); scratch in `/tmp` is fine, the refer-back artifact must not stay there.
- **A workflow is a checked sequence** — each step's result is verified, then becomes the next step's input. Not a
  DAG for its own sake.
- **The knowledge graph is declared** — each piece's needs and outputs, and what each must not see.

Both files also point at the installed skills by name — `workflow-design` designs the workflow, `requirement-check`
evaluates the rule, `meaningful-names` names the thing — and name the project, not the Ancient Games.

## Before you call it done

- Each of the four rules above is copied verbatim into **each** generated file (the canonical target if `AGENTS.md`
  is a pointer). The one-copy guidance does not remove these required repetitions. Glosses go outside the rules.
- Follow the instruction pointers as a fresh session would: they reach both standing files without a cycle, and
  each named skill and reference resolves. If a harness cannot discover a skill, give its readable `SKILL.md` path.
- Every project path either file names exists **in that project**, or is marked as still to be created, with who
  creates it and when. Installed-skill paths resolve under the actual skill root. This is the
  portability check: `docs/WORKFLOW_DESIGN_METHOD.md`, `ancient_games/`, `code_graph/` and the rest of this
  repository's paths do not belong in another project's files.
- Every mapped task type has all the fields listed in How step 2, and each non-loop has a reason. Check commands
  come from this project; a claimed verified check has recorded output. Demonstrate sabotage in a fixture, not by
  damaging the project's working files. Keep missing checks or limits open and the affected type blocked.
- If a selected template expects a code graph or other tool, resolve the actual project tool and its source
  artifacts, or record that dependency as missing; a template reference does not install the tool.
- Every engine marked verified has actually passed a readiness probe in this project with its stated model/effort
  and required read/write capability. Record the command and evidence path; presence in a catalog is insufficient.
  A proposed or unavailable engine stays `unknown`, blocks dispatch, and has no silent substitute.
- Trace one representative project task on paper: find its mapping, inputs, worker output, protected check,
  verifier, evidence path, state writer, success handoff and limit-hit exit. This is a completeness review, not a
  request to execute the task. Missing links mean draft, not finished.
- Then report: the files written, the questions the blueprint could not answer, and every number carried over from a
  default.

Source references in this skill are relative to the installed sibling `workflow-design/` folder; project paths
such as `runs/<run-id>/` are relative to the adopting project. The referee's SPEC is provenance for the table,
not a required installed file. n=0: the bootstrap has never been run on a project outside this repository; when
it produces something wrong, fix the skill here too.
