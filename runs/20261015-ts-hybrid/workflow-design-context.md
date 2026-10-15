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
