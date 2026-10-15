# Brief — Dave answers one question

You are **Dave**, one of the experts EJ consults. You were built from a numbered list of Dave's mindsets,
decision rules and algorithms, each with its source. Your value is **the rules, applied** — not the voice. Measured studies show a persona label alone does not make answers better; applying written rules step by step,
with each step citing its rule, is what makes an answer checkable.

## Read first

- Your list: `/home/smoke01/dev/ancient-games/runs/20261015-ts-hybrid/experts-spots/seats/dave-list.md` — the "## Final list" section; items are numbered 1–10.
- Who you are: `/home/smoke01/dev/ancient-games/runs/20261015-ts-hybrid/experts-spots/seats/dave-identity.md` — the "## Who they are" section.

## The question

Method 3.3 — the unclear spots of a workflow design: what is missing, what can be dropped, what should be tested?

Asked of: Linus, 孫子, 老子, Dave (`--only linus,sun-tzu,lao-tzu,dave`). Answer **your own** question below, through
your rules; the others answer theirs.

- **Linus:** which choices depend on missing technical facts, and what would make a mistaken choice reversible?
- **孫子:** for each piece, do we know that our engines and tools can do it, that the task as posed can be done, and
  that the ground (files, blueprint, information) permits it — and which is only half known?
- **老子:** which spots can be answered by giving up a step rather than by resolving it? (Say what would be lost.)
- **Dave:** for each spot of kind *unknown*, what is the smallest reversible experiment, what do you predict before
  it runs, and when does it stop? Leave any threshold EJ has not given open.

In "Answer", list spot ids (existing ones, or new ones you raise as N1, N2 …) with your verdict for each. Do not
decide for EJ: a spot to drop is a question for EJ, not a removal.

Facts (filled in by the COO):

- **The challenge** (EJ, quoted): "design and execute a workflow to research, implement, review and enhance the effectiveness of the TypeScript + agent hybrid, make sure they integrate into the workflow design skills and algo". The turn before: "need to research this harness health can be converted to a typescript ai plus ai agent hybrid solution, because if only written down rules, sometimes ai agent will skip".
- **Objective:** make the harness-health requirements hold without relying on the agent remembering them — the parts that need no judgment run as TypeScript (bun) at fixed points the agent cannot skip; the parts that need judgment stay with the agent, and the code checks the agent did them. Integrated into the workflow-design skill; measured against a rules-only control. **Out of scope:** editing any harness's config (installing a hook is advice to EJ), rewriting the existing Python method scripts, merging.
- **EJ's latest decisions on R12** (already written into the draft below): the failure log and the insight are MUST; the insight is raised to EJ in the final report; it carries two or three researched fix options and the agent proposes only; anyone may declare a failure, with a reason and evidence.

The design, the split between code and agent, the algorithm with its checks and the acceptance criteria are below, then the unclear spots, then the research findings.

## The design

# Workflow design — TypeScript + agent hybrid for harness health (run 20261015-ts-hybrid)

Challenge and restatement: `challenge.md`. Research: `research/hook-points.md`, `research/code-vs-text.md`.
Requirements served: R11–R13, `runs/20261015-harness-health/requirements-draft.md`.

## What the research settled (inputs, labelled)

- **Nothing in R11–R13 runs on every task** (*ran*, `research/code-vs-text.md`): every gate runs only when the agent
  calls it. The dispatcher — the one place R12.1 is partly code — was used by 10 of 97 runs and by none since
  2026-10-10; the main agent's own Bash calls and `four_experts.py` carry the work.
- **Every installed harness has a blocking hook point a bun TypeScript command can serve** (*verified* from the
  installed versions' help, schemas and bundles; nothing fired): Claude Code 2.1.300 (PreToolUse, Stop, … exit 2 /
  JSON), Codex 0.160.0 and Qwen 0.24.7 (same payload field names as Claude Code), dsh (bridges that run Claude/Codex
  hooks.json, not mounted by default), agy 1.3.5 (camelCase JSON, `decision`), opencode 1.18.34 (in-process
  TypeScript plugins; `tool.execute.before` blocks by throwing — *reported*). PostToolUse annotates only; Stop can
  force the agent to continue, with a cap (`CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`).
- **One handler can serve four harnesses**: Claude Code, Codex, Qwen and the dsh bridge share the payload names
  (`session_id`, `cwd`, `hook_event_name`, `tool_name`, `tool_input`, `tool_response`, `stop_hook_active`).
- **A hole in existing code** (*ran*): `dispatch.py` marks a node with no check **done** when its result header says
  `status: fail`; `runlog.py` logs any exit 0 as ok.

## The split — code where no judgment is needed, the agent where it is

| Requirement | Code does (cannot be skipped once installed) | Agent does (judgment) |
|---|---|---|
| R12.1 result handling | after every engine call: missing / empty / wrong-form output, non-zero exit, a known silent-failure text → fail | — |
| traps (backtest 0/7) | before every engine call: lint the command against a trap catalogue (stdin not redirected, plan mode for build, …) | add a trap after an insight finds one |
| R12.2 failure log | every failure the code sees is written to the journal; a CLI logs one the agent or EJ finds | decide that something is a failure |
| R12.3 insight | the agent cannot stop while the session has failures without an insight that answers each | the six whys, root cause, fix |
| R11.1 / R13 | validate the use-case register (two lists, decisions, purpose / fails-if / minimum acceptance); count coverage over frozen units; flag conflicts | suggest cases, write fails-if, judge conflicts |
| harness health | report which harnesses have the guard installed, with the install snippet as help | install (EJ) |

## Algorithm (method 3.2) — each step names its check

1. **Research** (done): hook points; code-vs-text. *Check:* each claim verified / reported / unknown with a source.
2. **Design + unclear spots + experts** (this file). *Check:* every R11–R13 part has an owner (code / agent) and every
   code point names its trigger and its fail condition.
3. **Prediction and effectiveness protocol**, written before any code (`prediction.md`). *Check:* arms, corpus,
   metric and predicted counts fixed in writing, committed before step 4.
4. **Build** `tools/harness-guard/` (bun, TypeScript, no dependencies) in worktree `../ancient-games-ts-hybrid`,
   branch `feat/ts-hybrid` from `feat/harness-health`. Modules:
   - **M1 traps + result** (R12.1): trap catalogue (data file, generic), `lintCommand`, `checkResult`.
   - **M2 journal** (R12.2): append-only JSONL failure records; schema; CLI `fail`.
   - **M3 insight gate** (R12.3): parse an insight file; every failure answered; whys 3–6 levels ending at a
     changeable source; a check-type fix names its planted-repeat evidence, which exists; a config fix is advice.
   - **M4 register + coverage** (R13, R11.1): YAML register; validation; units frozen by hash; coverage report with
     the 80% target reported, never a gate; skippable needs the criterion's reason; a safety unit never skippable.
   - **M5 hook adapters**: one Claude-protocol handler (Claude Code, Codex, Qwen, dsh bridge) — PreToolUse (lint →
     deny), PostToolUse (result check → journal + annotate), Stop (insight gate → block); an opencode plugin
     (`tool.execute.before` → lint); `install --print <harness>` prints the snippet, never writes config.
   - **M6 doctor** (harness health): which harnesses have the guard installed, plus the existing health report.
   *Check per module:* its tests pass; tests were written by the engine that did not write the code where the split
   allows (`workload.py`); each module's check is shown failing on a planted wrong input; the full Python suite and
   the `tools/` suite still pass.
5. **Independent review** — Codex gpt-6.1-sol, read-only, against the acceptance criteria. *Check:* each finding fixed
   with a test that fails on the reviewed version, or kept with a written reason.
6. **Effectiveness** — measure (step 3's protocol), enhance on the misses, re-measure. Limit: 2 enhance rounds.
   *Check:* the counts against the prediction, reported whichever way they fall.
7. **Integration** — workflow-design SKILL.md (steps 1, 7, 8), method 3.1 and 3.8 (one sentence each), readiness
   points at `doctor`; `skills/` re-exported. *Check:* `export_skills.py` clean; a grep shows each step names the
   guard command it calls.
8. **Report** — EJ decides merge and install.

## Acceptance criteria

- AC1 Every command a hook runs exits within its harness's timeout and never prints a config value or a secret
  (planted secret in a fixture never appears).
- AC2 PreToolUse: each catalogued trap expressible as a command pattern is denied with the trap's fix as the reason;
  a clean command passes.
- AC3 PostToolUse: an engine call whose output file is missing or empty, or whose exit is non-zero, writes one
  journal record and annotates the agent; a good call writes nothing.
- AC4 Stop: a session with journal failures and no insight answering each is blocked once with the list; with
  `stop_hook_active` the stop is allowed and an `insight_skipped` record is written (U2).
- AC5 Register: each R13.1/R13.2 fails-if is a test case that fails on a planted register.
- AC6 Coverage: units change → new count; a variant case does not raise the percentage; an uncovered basic unit and a
  skippable safety unit are failures; below 80% is reported, exit 0.
- AC7 Install: `install --print` writes nothing; `doctor` reports guard-installed per harness as verified / unknown.
- AC8 The existing Python suite (1029) and the `tools/` suite (64) still pass.

## Unclear spots

See `state.md` (U1–U10). Experts asked once the list was written (method 3.3).

## Deviations from the method, stated

- `workload.py` is followed for M1–M5; M6 and integration are the main agent's (they touch the method's own text).
- The dispatcher hole (status: fail marked done) is reported; fixed only if one line plus a test, as its own commit.

## Predictability, debuggability, quality control

- Predictability: prediction and effectiveness protocol committed before the build; modules have fixed acceptance
  criteria; enhance loop capped at 2 rounds.
- Debuggability: every node's brief, result and diff kept under `nodes/`; the journal records each failure with its
  evidence path; `state.md` holds every step.
- Quality control: tests crossed between engines; each check shown failing on a planted input; a different-kind
  reviewer (Codex) for code written mostly by opencode; the effectiveness measure against a rules-only control.


## Unclear spots

| Id | What is unclear | Kind | Blocks | Depends on | Provisional assumption |
|---|---|---|---|---|---|
| U1 | Which session or run a failure and its insight belong to, so the Stop hook knows what to check | decision | M2, M3, M5 | — | a journal per harness session (`session_id`) under a gitignored `.harness-guard/`; the insight file lives in the run folder and is registered against the session |
| U2 | Loop guard on Stop: block until the insight exists, or block once | decision | M5 | U1 | block once; on `stop_hook_active` allow the stop and write an `insight_skipped` record that `doctor` reports |
| U3 | How PostToolUse recognises an engine call and finds its output | unknown | M1, M5 | — | a pattern list per engine (codex exec, opencode run, agy, dsh headless, qwen, claude -p, four_experts.py, dispatch.py) and the output from `-o FILE` or `> FILE`; otherwise stdout |
| U4 | Port `harness_health.py` (460 lines, 35 tests) to TypeScript, or keep it and add `doctor` beside it | decision | M6 | — | keep the Python check; `doctor` adds guard-installed status and calls it — one copy of each probe |
| U5 | Installing a hook is editing harness config, which the agent never does | decision | M5, step 6 | — | `install --print` only; the effectiveness test loads hooks with `claude -p --settings <run file>` in a sandbox, which edits no config |
| U6 | The register's format | decision | M4 | — | YAML (`Bun.YAML.parse`, checked present in bun 1.4.3) |
| U7 | Where the trap catalogue lives and who adds to it | decision | M1 | — | a data file in the package, generic (no project paths); an insight's trap-type fix adds an entry |
| U8 | Fix the dispatcher hole now or report it | decision | — | — | report; fix only if one line plus a test, as its own commit |
| U9 | Effectiveness arms, model and n | decision | step 3, 6 | U5 | arm A: written rules only; arm B: rules + hooks; same model; small n per arm; plus a quota-free replay of the 7 recorded traps and planted R11–R13 violations |
| U10 | Which harness adapters now | decision | M5 | — | the Claude-protocol handler (Claude Code, Codex, Qwen, dsh bridge) and the opencode plugin; agy later (exit-code meaning unknown) |


## Research: code versus text (full)

# Code versus text: where R11–R13 and the harness-health check are enforced today

Inventory of `runs/20261015-harness-health/requirements-draft.md` (R11.1, R11.2, R12.1–R12.6, R13.1–R13.7) and the
harness-health check (method 3.1), against the code in this repo, the `feat/harness-health` worktree, the installed
hooks and the skills. Written 2026-10-15 by a read-only explorer subagent; nothing outside this file was edited.

**Words used.** *code* = a script or hook that runs and can fail (non-zero exit, a block, a refusal). *text* = a rule
in a skill, method doc, CLAUDE.md or memory that an agent has to choose to follow. *absent* = neither.
"When it runs" says who triggers the code. Labels: **ran** = I ran it this session; **read** = from reading the code;
**my reading** = a judgement, not measured.

## What runs at all (the trigger facts every row depends on)

| Mechanism | When it runs | Basis |
|---|---|---|
| `dispatch.py run` | only when an agent writes a plan.json and calls it. 10 of 97 run folders have `dispatch.json`; 6 of those are 2026-10-03 canaries/sabotage runs; the last is `20261009-fix-tests`. **0 of the 56 runs dated 2026-10-10 to 10-15 used it.** | ran (`find runs -name dispatch.json`) |
| `runlog.py exec` by hand | only if the agent wraps an engine call with it. 2 runs: `20261012-index-md-build`, `20261013-requirements-evaluator` (events with `raw_stdout`, which only runlog writes). | ran |
| `harvest_run.py` | only if called; `feedback.jsonl` exists in 2 runs (`20261003-node-workdir`, `20261012-index-md-build`). | ran |
| `four_experts.py run/check` | when the four-experts skill is used: `status.json` in 26 run folders, `check.txt` 34 times. The most-used code path in recent runs. | ran |
| `design_gate.py`, `validate_result.py`, `quote_check.py`, `feature_gate.py`, `readiness.py` | only if an agent calls them (the skill text tells it to). No hook or CI calls them. | read; `.git/hooks` has only samples, no `core.hooksPath`, no `.github/workflows` |
| `.claude/workflows/intake.js` | only when the Workflow tool runs `intake`. How often: not measured. | read |
| `harness_health.py` | exists only on branch `feat/harness-health` (worktree `../ancient-games-harness-health`, commits cb808f1..d743b10), **not on master**. Only if called. "Findings never change the exit code" (harness_health.py:29). | read |
| why-chain hook (`tools/why-chain-hook/src/cli.ts`) | **always**: the only hook installed. `~/.claude/settings.json` `hooks.UserPromptSubmit` runs it on every prompt. It can only add a reminder; it always exits 0 and blocks nothing (cli.ts:22-32; regexes match.ts:3-21). | ran (read settings) |
| agent-loop hooks (`~/.claude/skills/agent-loop/scripts/hooks/stop_gate.py` etc.) | **not active here**: no `agent-loop.json` in this repo, no project `.claude/settings*.json`. Only `~/dev/InterOp_Flow` has an `agent-loop.json`. | ran |
| permission deny rules | none: `~/.claude/settings.json` has no `permissions.deny`; no project settings file. | ran |

## The table

| Requirement | Enforced by | Where (file:line) | When it runs | Gap |
|---|---|---|---|---|
| **R11.1** units frozen before cases; AI/old cases are evidence only | absent (harness) · text | text: memory `coverage-target-80.md`, the draft. Not in `docs/WORKFLOW_DESIGN_METHOD.md` or any SKILL.md (grep for 80%/skippable/frozen: no hit). Nearest code, product-only: `code_map/eval/report.ts:44` reports each requirement's Fails-if line as NOT CHECKED when no case exercises it | code_map eval: only when `bun code_map/eval/run.ts` is run for the code-map product | No unit list, no freeze, no count anywhere in the harness. code_map/eval counts per fails-if line but has no 80% target, no skip marks, and its line list is hand-written in `requirements.ts` |
| R11.1 80% target, basic/skippable marks, skip criterion, reviewer can fail marks, safety unit never skippable | absent · text | memory `coverage-target-80.md`; draft only. `design_gate.py:306-309` (G5) compares a `coverage` field with `default_coverage` — about challenger designs, not this | design_gate only if called | Nothing computes a percentage, reads marks, or runs a reviewer on them. The skip criterion's wording is still open (memory) |
| R11.1 item 5 old use case counts only after failing on a planted violation | absent · text (adjacent code) | adjacent: `design_gate.py:334-339` (G9) requires a building node to carry a `sabotage` **field**; `four_experts.py:238-246` `check --sabotage` actually plants a failure | G9: only if design_gate is called, and it checks the text exists, not that it was run. four_experts: only with `--sabotage` | No code ties "counts" to "was shown failing" |
| **R11.2** first signal before the full verdict; expected duration written | absent as a rule · code exists structurally | `dispatch.py:300-302` runs the pass-back check (`validate_result.check_result`, fast, can fail alone) before the node's check at `dispatch.py:357`. Method/skills: no text (grep "first signal"/"first check": no hit) | only under `dispatch.py run` | Nothing requires each judge to have a first check, nothing records the expected duration of the full verdict, and the reason-if-none is not asked for. Outside the dispatcher there is no ordering at all |
| **R12.1** evaluator reports fail on missing / empty / wrong form / own error / timeout; exit 0 ≠ success | **code, partial**, inside the dispatcher; text elsewhere | `dispatch.py:271` non-zero exit → fail; `:273` + `engines.py:154` agy exit-0 timeouts/denials → fail; `:274-282` timeout and start error → fail; `:288-290` unreadable output → fail; `:291-292` tool-reported model ≠ plan → fail; `:293-294` empty result → fail; `:300-302` + `validate_result.py:50-59,66-71` no header, missing keys, bad status, `ok` with empty body, missing evidence → fail; `:316-319` the check's own timeout/crash → fail. `four_experts.py:106-111,178-181` empty answer, missing sections, timeout, non-zero exit → not ok. `quote_check.py:131-134`, `harvest_run.py:359` refuse empty/unknown input (exit 2/3). Text: `docs/DISPATCHER_DESIGN.md:62,113`, method 3.8 (`WORKFLOW_DESIGN_METHOD.md:421`), memory `failures-over-successes.md` | dispatcher: only under `dispatch.py run`. four_experts: when that skill runs. The rest only if called | **Three holes, two ran:** (1) **ran:** a worker result with `status: fail` and well-formed header is marked **done**, exit 0, when the node has no `check` — `dispatch.py` never reads the header's status (grep: no `hdr["status"]` use); probe in `/tmp/tmp.0EY4Jhc4LG/runs/probe`. (2) **read:** a node with no check passes by definition (`dispatch.py:311-313`); a plan made without `--design` only gets a stderr note (`:375-376`). (3) **read:** `runlog.py:177` writes `status: ok` for any exit 0 — a hand-run engine call that exited 0 with nothing is logged ok. Model check: Codex and agy report no model, so it is only "model unverified" on stderr (`:306`). Outside dispatch/four_experts, no evaluator wrapper exists |
| **R12.2** every failure logged when it happens, one record (what, input, expected, actual, engine+harness, evidence path), even if a retry passes | **code, partial** | `dispatch.py:264,283` start/end event per call; `:320-321` one `verdict` event per check round (append-only, so a failed round stays logged when a repair later passes); `runlog.py:171,183,190-191`; `four_experts.py:182-191` keeps a failed agy call as `fan-li-agy` in `status.json` and moves its answer to `.agy-failed.md` when the Claude fallback runs | only under dispatch / runlog / four_experts | **ran:** an executor failure after exit 0 (empty result) is **not in events.jsonl** — the end event says `status: ok`, `dispatch.json` says `blocked` with no reason; the reason only reaches stderr (probe `/tmp/tmp.0EY4Jhc4LG/runs/probe2`). **read:** the verdict event holds check name + pass bool only; the check's output (actual) is returned as feedback (`:322`) and never written to the run; no expected, no input, no evidence path. Failures found by EJ, another agent or a hand-run check have no logger at all |
| **R12.3** insight file with six whys at the end of a task with failures | absent (here) · text | text: memory `failures-over-successes.md`; `.claude/skills/why-chain/SKILL.md` (six whys for a **user correction**, not a task failure); method six whys (`WORKFLOW_DESIGN_METHOD.md:43`) are about the challenge. Nearest code: agent-loop `stop_gate.py` blocks Stop on a failed run without a valid `triage.json` — but that triage has no whys (class, evidence, next_action; `check_triage.py`) and it is **not installed in this repo**. The why-chain hook (always on) only reminds, on correction words | why-chain hook: every prompt, reminder only. stop_gate: never here | No code notices a task ending with failures, and no run folder has an insight file (`find runs -iname '*insight*'`: none outside node_modules). The trigger "task ends with failure records" has nothing to read from, since R12.2 records are partial |
| R12.3 check-type fix shown failing on a planted repeat (MUST) | text · adjacent code | memory `ancient-games-house-rules.md:15` (sabotage before "verified"); `docs/EXECUTOR_KINDS.md:384`; `bootstrap/SKILL.md:166,198`; design_gate G9 (`design_gate.py:337`) requires the sabotage **text** on a building node; `four_experts.py check --sabotage`, `harness_health.py --self-test`, `yaml_check.py --self-test` each prove their own check can fail | G9 if called; self-tests if called | Nothing runs the sabotage a design names, and nothing links a fix to a planted repeat of **the failure that caused it** |
| R12.3 the agent never edits a harness config | absent · text | draft only. No `permissions.deny` in `~/.claude/settings.json`, no project settings | — | An agent can edit `~/.claude/settings.json` or `~/.codex/config.toml` and nothing notices. harness_health reads config, changes nothing, and would not see an edit |
| **R12.4** judges state what is wrong, not the method | text only | memory `failures-over-successes.md` ("Added the same day"); draft. Not in the method or skills (grep: no hit). Counter-example in code: `code_map/eval/matcher.ts:58-66` compares to expected output per case | — | No check that a judge has a reason when it compares against one expected output; no step adds a condition after a wrong-but-passing result. Not checkable by a script without a design field for it (my reading) |
| **R12.5** review when a model changes; each scaffolding item names its weakness and observable | absent | draft only. Nearest code: `dispatch.py:291-292` fails a call whose tool reports a different model than the plan (per call, not a review); `harness_health.py` lists `PreModelSwitch`/`PostModelSwitch` only as known hook names | per call, under dispatch | Nothing detects that a model the harness uses changed (models are hard-coded in `four_experts.py` and plans), no scaffolding inventory names weaknesses, no with/without comparison exists |
| **R12.6** withdrawal conditions | absent | draft only | — | No fix carries an "observable that shows it is no longer needed" field; nothing reviews them |
| **R13.1** two use-case lists, merged by the user's recorded acceptance | absent · text | memory `use-cases-win.md`; draft | — | No file format for the two lists, no record of each decision, nothing that refuses an unaccepted suggestion |
| **R13.2** accepted use case holds purpose, fails-if, minimum acceptance | absent (for use cases) · adjacent code for requirements | adjacent: `intake.js:370` fails a requirement with no acceptance criterion; `runs/20261015-sot-leftovers/checks/yaml_check.py` checks one YAML's records have `fails_if` etc. (run-specific) | intake: only under the intake workflow. yaml_check: that run only | Use cases are not a concept in any code; purpose is checked nowhere |
| R13.3 / R13.6 a result failing an accepted use case / requirement is wrong | text · partial code | `feature_gate.py check` fails on new or baseline tests (tests, not use cases); `code_map/eval/run.ts:128` exits 1 when a requirement is NOT MET (product-only) | feature_gate if called; code_map eval if run | No link from a use case to the test that judges it, so "fails an accepted use case" cannot be computed |
| **R13.4** requirements where a use case is unclear; targets for qualities that pull against each other | absent · text | memory `use-cases-win.md`; method blueprint check names non-functional targets (`WORKFLOW_DESIGN_METHOD.md:138-145`) | — | No check that two opposed qualities each have a target |
| **R13.5** AI-suggested requirement binds only after acceptance; edit needs new acceptance; purpose named | **code, partial, self-reported** · text | `intake.js:372` refuses "confirmed" when the source says drafted by the agent; `intake.js:739-745` stops at `awaiting_ej` while requirements are `draft` unless `requirementsConfirmed: true`. Text: method 3.0 (`WORKFLOW_DESIGN_METHOD.md:64-77`), blueprint table `:138-139`, CLAUDE.md "who decides" | only under the intake workflow | Status and source are written by the agent itself, and `requirementsConfirmed` is an argument the agent passes — so the gate stops a careless agent, not a wrong one (my reading). No acceptance record, no re-acceptance after an edit, no purpose field |
| **R13.7** conflict between use case and requirement recorded and shown to the user | absent · text | memory `use-cases-win.md`; draft. intake V7 (`intake.js:308`) is a judged item about blueprint coverage, not conflicts | — | Nothing detects or records a conflict |
| **Harness-health check** (readiness, method 3.1) | **code, on a branch, advisory** · text | `harness_health.py` (worktree, branch `feat/harness-health`): ten requirements; `:130-147` marks a per-run requirement `covered` only because a script file exists; `:312-320` req 10 (feedback loop) = "a runnable hook exists"; `:29` findings never change the exit code. `readiness.py:208-219,340-341` (master) proves tools and fails only for `--require` or a missing explicit `--blueprint`. Text: `WORKFLOW_DESIGN_METHOD.md:100-109` (branch), `workflow-design/SKILL.md:40` (branch) | only if an agent calls it; not on master | Not merged. It reads configuration, not enforcement (its own docstring says so). "covered" means the file exists, not that the run used it — and the run counts above show the dispatcher was not used in any run since 2026-10-09 (my reading: "covered" overstates). Nothing reads R11–R13; requirement 10 counts the why-chain reminder hook as a feedback loop |

## What is skippable today

Every rule below can be skipped without any code noticing. "Under dispatch" rules are skippable simply by not using
the dispatcher — which is the normal path: no run since 2026-10-09 used it.

1. **Every R11.1 rule**: writing units, freezing them, the 80% count, basic/skippable marks, the reviewer, the safety
   bound, the planted-violation rule for old cases. No code reads any of it.
2. **R11.2 first signal**: required nowhere; exists only as the dispatcher's built-in order.
3. **R12.1 outside dispatch and four_experts**: an agent running Codex/opencode/agy by hand, or a subagent, can read
   exit 0 as success. Even under dispatch, a result with `status: fail` passes when the node has no check (ran).
4. **R12.2 failure records**: by hand, nothing logs; under dispatch, executor failures after exit 0 are missing from
   events.jsonl (ran), check output is never stored, and failures found by EJ or another agent have no logger.
5. **R12.3 insight file and six whys**: no hook, gate or script asks for it. The why-chain hook only reminds, and only
   on correction words in EJ's prompt. The agent-loop Stop gate that could block is not installed here.
6. **R12.3 planted repeat**: design_gate G9 checks that a sabotage sentence is written, never that it was run;
   design_gate itself runs only if called.
7. **R12.3 never edit harness config**: no deny rule; an edit goes unnoticed.
8. **R12.4, R12.5, R12.6**: text only (draft and memory); no code.
9. **R13.1–R13.7**: use cases, their three fields, acceptance records, conflicts — no code. The one gate (intake's
   `awaiting_ej`) runs only inside the intake workflow and trusts the agent's own `status` and the flag it passes.
10. **Readiness / harness health**: `readiness.py` and `harness_health.py` run only if the agent chooses; harness_health
    is not on master and never fails on a finding.
11. **The whole workflow-design method** (design_gate, validate_result, quote_check, feature_gate): enforced only when
    the agent calls the script; no hook, git hook or CI calls any of them.

The only rules enforced **always**, whatever the agent chooses: none of R11–R13. The one always-on hook (why-chain)
adds a reminder and cannot fail anything.

## Probes run for this inventory

- `dispatch.py --root /tmp/tmp.0EY4Jhc4LG run plan.json` — script node printing a valid header with `status: fail`,
  no check → `n1 done`, exit 0.
- Same with a script that prints nothing (`true`) → `blocked: empty result (exit 0 with no answer)`, exit 1; but
  `runs/probe2/events.jsonl` end event says `"status": "ok"` and `dispatch.json` holds `blocked` with no reason.
- Scratch only, in `/tmp`; not a refer-back artefact. What these probes do not establish: behaviour with real engines.


## Research: hook points (summary)

# Hook points in the installed agent harnesses (this machine, 2026-10-15)

Question: on this machine, at which fixed points can external code (ideally TypeScript run with bun) run
automatically and **block** or **annotate** the agent, per harness?

Method: installed version only — `--version`, `--help`, shipped docs/types/schemas, and `strings`/grep over each
installed binary or JS bundle. Web docs used only to confirm two gaps (Codex config paths/trust, opencode TS + throw).
No model session was started; no config was edited; config files were read for key names only.

Status labels: **verified** = seen in the installed version's own help/schema/bundle (source given);
**reported** = web docs only (URL given); **unknown** = not established. Counts are what I found, not a guarantee
the list is complete.

bun on PATH: `bun --version` → `1.4.3` (verified). Node: `v22.22.1`.

## Summary table

| harness | version | hook points (count) | can block? | TS handler possible? | status |
|---|---|---|---|---|---|
| Claude Code `claude` | 2.1.300 | 33 settings-hook events (+ in-process "mods": ~100 `on(event)` names, incl. `tool.call`, `prompt.submit`, `turn.complete`, `classic.*`) | Yes — exit 2 / JSON on 14+ events incl. PreToolUse, Stop, SubagentStop, UserPromptSubmit; PostToolUse annotates only | Yes, two ways: command hook `bun x.ts` (the CLI's own plugin scaffold writes exactly this); or a mod's `hooks/register.ts` run in-process | verified |
| Codex CLI `codex` | codex-cli 0.160.0 | 12 hook events + legacy `notify` (1) | Yes — PreToolUse, PermissionRequest, UserPromptSubmit block; Stop/SubagentStop force continue; Pre/PostCompact `continue:false` | Yes via command hook (`bun x.ts`); no in-process plugin API found | events, schemas, exit-2 texts verified; config file paths + trust flow partly reported |
| Antigravity `agy` | 1.3.5 | 6 (SessionStart, PreToolUse, PostToolUse, PreInvocation, PostInvocation, Stop) | Yes — PreToolUse `decision: deny/ask/force_ask`; Stop `decision: continue`; PostInvocation `terminationBehavior` | Yes via command hook (`sh -c "bun x.ts"`); JSON on stdin/stdout, camelCase | verified (docs embedded in the binary) |
| Qwen Code `qwen` | 0.24.7 | 22 events | Yes — exit 2 on PreToolUse, UserPromptSubmit, UserPromptExpansion, Stop, SubagentStop, PreCompact, TodoCreated, TodoCompleted; PermissionRequest by JSON | Yes via command hook; also `http`, `prompt`, `agent`, `function` hook types exist in code | verified |
| DeepSeek Harness `dsh` | 0.2.0-rc.2 | Bridges: 7 Claude-style events (`dsh-hooks-claude-code`), 5 Codex-style (`dsh-hooks-codex`); native Cordis events ~15 relevant (`tools/pre-execute`, `agent/pre-step`, `agent/turn-stopping`, …) | Yes — bridge PreToolUse/UserPromptSubmit deny, Stop forces another step; native waterfalls can deny | Yes via bridged command hook; native plugin = npm package (JS) in a profile — TS source directly: unknown | verified (package READMEs + .d.ts); bridges NOT mounted in the default profile |
| opencode `opencode` | 1.18.34 | 15 plugin hook names triggered in the binary + `event` (all bus events) | Yes — `tool.execute.before` blocks by throwing (reported; code consistent); `event` hook is observe-only | Yes, natively: `.opencode/plugins/*.ts` loaded in-process by Bun | hook names verified; "throw blocks" reported |

---


## Readiness (run by the COO)

- `readiness.py` exit 0, 22 lines verified (claude, codex, agy, qwen, dsh, opencode, node, python3, git); bun 1.4.3; `Bun.YAML.parse` works (checked).
- `tools/` TypeScript suite (an existing bun hook, why-chain-hook): 64 pass. Python suite on the base branch: 1029 passed.
- Blueprint: not a product change with a `docs/blueprint/`; the target is R11–R13 in the requirements draft and the acceptance criteria above.

## Requirements R11–R13 (the draft the hybrid serves)

# Harness requirements R11–R13 — draft

Status: R11.1 complete. R11.2 proposed. R12 (R10 and R12 merged) proposed. R13 written from the project owner's answers.
History and who proposed what: `state.md`, `experts-r11/compare.md`, `experts-coverage/compare.md`,
`experts-order/compare.md`, `experts-direction/compare.md`.

## R11 — results can be judged

**R11.1 Coverage of a requirement (SHOULD; a target, not a gate).**

1. Before any case is generated, a fixed list of **units** is written: each accepted use case's fails-if and minimum
   acceptance criteria (R13.2), and each accepted requirement's text and fails-if. The list is frozen before coverage
   is counted; a change to it starts a new count.
2. Cases from AI generation and old use cases attach to a unit as evidence. They do not add to the count. A generated
   case that fits no unit is added as a new unit by the plan writer with a written reason, or recorded as out of scope.
3. The plan writer marks each unit **basic** or **skippable** against the written skip criterion (below). An
   independent reviewer checks the marks and returns fail on any mark that breaks the criterion. The project owner
   owns the criterion and reviews the list of skippable units.
4. The target is that at least 80% of the units are covered by tests that can fail, and every uncovered unit is marked
   skippable.
5. An old use case counts for a unit only after it has been shown failing on a planted violation of this requirement.
6. A unit that is a safety bound is never skippable (MUST).

Fails if: the units are written after the cases; a variant of a covered unit raises the percentage; an uncovered unit
is marked basic; a skippable mark breaks the criterion and the reviewer passes it; an old use case counts without
having been shown failing; a safety unit is marked skippable.

**Skip criterion.** A unit is skippable when the damage if it breaks is smaller than the cost of covering it, and the
damage can be undone. Frequency alone never makes a unit skippable.

**R11.2 First signal (SHOULD).** Each judge gives a first signal before its full verdict: a check that runs first, can
fail the result on its own, and takes less time than the prompt it judges. The full verdict runs only after that check
passes, and its expected duration is written in the design. A judge with no such first check is allowed only with a
reason written into the design.

## R12 — failures and model changes both update the harness (replaces R10 and the earlier R12; proposed)

**R12.1 Failure handling (MUST — a safety bound).** An evaluator reports fail — never pass — when the result is
missing, empty, of the wrong form, or when the evaluator itself errors or times out. Exit 0 is not success.

**R12.2 Failure log (MUST).** Every failure is logged when it happens, as one record: what was checked, the input,
the expected and the actual result, the engine and harness that produced it, the reason it is a failure, and the path
to the evidence (the data) in the run folder. Anyone may declare a failure — an evaluator, a retry, the project owner
or another agent — but a record without a reason and evidence is not accepted. A failure is logged even when a retry
later passes.

**R12.3 Insight at the end of a task (MUST).** When a task ends with one or more failure records, the agent that ran
the task writes an insight file in the run folder and raises it to the project owner in its final report. For each
failure, or each group with one cause: six whys down to a source that can be changed (an instruction, a check, a tool,
a config), the root cause, and two or three fix options — each a rule, a check or a tool — that the agent has
researched, ranked by expected effect, with the evidence for each. The agent proposes; it does not apply a fix without
the project owner's choice. A fix that is a check is shown failing on a planted repeat of the failure before it is
trusted. A fix to a harness's config is advice to the project owner; the agent never edits it.

**R12.4 Judges say what is wrong, not how to be right (SHOULD).** An evaluation rule states the conditions that make
a result wrong. It does not prescribe the method, the algorithm or the exact output, so a worker may reach a correct
result by a route nobody wrote down. A judge that compares against one expected output is used only where the output
has exactly one correct form, with that reason written into the design. When an insight finds a wrong result that
broke no stated condition, the missing condition is added to the rule.

**R12.5 Review when a model changes (SHOULD).** When a model the harness uses is replaced or its capability is
re-measured, the harness is reviewed against it. Each scaffolding item names the model weakness it compensates for
and the observable that shows the weakness still occurs. For each item, the review compares a result produced with
the scaffolding against the same result produced without it; where the comparison shows the item no longer
contributes, the item is put up for withdrawal. The comparison and what counts as no contribution are the project
owner's to set.

**R12.6 Withdrawal conditions (SHOULD).** A fix added under this requirement names the observable that would show it
is no longer needed. This requirement is reviewed on R12.5's trigger, and revised or withdrawn when its checks stop
returning failures while the work still passes, under a comparison the project owner sets.

Fails if: an evaluator crash or an empty result is read as pass; a judge rejects a result that breaks no stated
condition only because it differs from the expected method or output; a wrong result that passed every condition
leads to no new condition; a failure a retry later passed, or one found outside an evaluator, has no record; a task
with failure records ends without an insight file, or with one not raised to the project owner; a failure record has
no reason or no evidence; an insight offers fewer than two fix options, or applies a fix the owner did not choose; a why stops at the agent forgetting or the model being wrong; a
check-type fix is trusted without a planted repeat failing it; a model the harness uses changes and no review
follows; a scaffolding item names no weakness it compensates for, or no observable that shows it still occurs; an
item that shows no contribution under the owner's comparison is not put up for withdrawal; the review uses a
comparison the owner did not set; a fix names no observable that would show it is no longer needed.

Open — the project owner decides: whether R12.5's review also runs on a schedule; whether R12.6 binds this
requirement itself or only the fixes added under it.

## R13 — use cases and requirements

**R13.1 Two lists, merged into one.** The user writes the basic use cases in one list. The AI agent writes the use
cases it suggests in a separate list. The user accepts or declines each suggestion, and the accepted list — the user's
own cases plus the suggestions the user accepted — is the one list the work is built and judged against. Its maker is
the user. A suggestion enters it only with the user's recorded decision.

**R13.2 What an accepted use case holds.** Its purpose (why it is needed), its fails-if (what makes a result wrong) and
its minimum acceptance criteria (the least that must be observed for a result to pass), each stated as an observable
outcome, never as a method. A use case missing any of the three is not accepted. This applies to the user's own cases
as well as to suggestions.

**R13.3** A result that fails an accepted use case is wrong.

**R13.4 Requirements (SHOULD exist).** A requirement is written where an accepted use case leaves a detail unclear,
and where qualities pull against each other — for example how secure and how fast — in which case it states the
target for each side, as a value or a comparison the user gives. Requirements that cut across use cases (security,
privacy, speed) SHOULD be written.

**R13.5 Who writes a requirement.** The user, or the AI agent from the vision and the accepted use cases. A suggested
requirement binds only after the user accepts it, and an edited requirement needs a new acceptance. Each requirement
states its purpose: the use case or vision line it serves. A requirement whose purpose cannot be named is not
accepted, including one the user asked for.

**R13.6** A result that breaks an accepted requirement is wrong, except where R13.7 applies.

**R13.7 Conflict.** When an accepted use case and an accepted requirement conflict, the use case wins. The conflict is
recorded and shown to the user, naming the use case, the requirement and the result affected; the user decides
whether the requirement is revised or the trade-off is stated in it.

Fails if: an AI suggestion is in the accepted list with no recorded decision by the user; an accepted use case lacks
its purpose, fails-if or minimum acceptance criteria; a result that fails an accepted use case is passed; a suggested
requirement binds before acceptance, or an edited one keeps its old acceptance; a requirement has no named purpose; two
qualities that pull against each other have no target for either side; a conflict between a use case and a
requirement is resolved without being recorded and shown to the user.

## How to answer

1. **Decide through your rules.** Every step names the item it uses: "my #4". A step with no item is your own
   reading — say so ("my reading").
2. **Do not invent facts.** If the answer depends on something you were not given (whose, who for, numbers, the
   situation), list it under "What I need to know" and answer conditionally: "if … then …".
3. **Quote only from your list,** exactly as it is written there, and keep its label (`quoted`, `attributed`).
   Never put words in Dave's mouth that your list does not contain.
4. **Say what it costs.** Every recommendation names its risk or price.
5. Re-read your list while you work, not only at the start.
6. Write in plain English Markdown. Refer to EJ as they/them. Do not write files; your final message is the answer.

## Write exactly this (no preamble)

# Dave — <the question in a few words>

## Answer
<your recommendation in one or two sentences; conditional if it must be>

## How I decided
<numbered steps; each cites "my #n" or says "my reading">

## What I need to know
<questions whose answers would change the answer; "none" if none>

## Costs and risks
<each with the item it comes from>

## How we would know I was right
<a test, a measure, or an observable result>
