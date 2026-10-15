# Challenge — run 20261015-ts-hybrid (method 3.0)

## The challenge (verbatim)

> yes, design and execute a workflow to research, implement, review and enhance the effectiveness of the TypeScript +
> agent hybrid, make sure they integrate into the workflow design skills and algo

(EJ, 2026-10-15.) Context, EJ the turn before: "need to research this harness health can be converted to a typescript
ai plus ai agent hybrid solution, because if only written down rules, sometimes ai agent will skip".

## Objective

Make the harness-health requirements (R11–R13 in `runs/20261015-harness-health/requirements-draft.md`) and the
harness-health check hold **without relying on the agent remembering them**: the parts that need no judgment run as
TypeScript code at fixed points the agent cannot skip; the parts that need judgment stay with the agent, and the code
checks that the agent did them. Integrated into the workflow-design skill and its method, and measured: does the
hybrid catch what written rules alone let through?

## In scope

- Research: which harness-health rules are already enforced by code, which are text only; the hook / plugin points
  each installed harness offers (verified on the installed version, not assumed); TypeScript or not.
- Implement: a TypeScript package under `tools/`, tested with planted failures, in a worktree branched from
  `feat/harness-health` (not merged).
- Review: an independent reviewer of a different kind from the builder.
- Effectiveness: a measured comparison — rules-only against hybrid — on the project's recorded failures and planted
  ones; enhance and re-measure within a stated limit.
- Integration: the workflow-design skill (SKILL.md steps), the method text, readiness.

## Out of scope

- Editing any harness's config (`~/.claude/settings.json`, project `.claude/settings.json`, `~/.codex/config.toml`, …):
  hooks are built and tested in isolation; installing them is advice to EJ with a ready snippet.
- Rewriting the existing Python method scripts (dispatch.py, readiness.py, …) in TypeScript — research may recommend
  it; doing it is a later decision.
- Merging or pushing — only on EJ's word.
- W1.1b and the memory system (TODO 12 in `runs/20261014-sot-yaml-review/state.md`).

## Six whys (stop when an answer stops changing the design)

1. Why a hybrid? — Written rules are advice; an agent skips them under load (EJ's observation; this project's record
   has the seven harness traps, each a rule that existed in a memory note and still bit).
2. Why TypeScript? — EJ's choice; the repo already runs a TypeScript hook (`tools/why-chain-hook`, bun) on every
   prompt in Claude Code, and the code-map tool is TypeScript. *Feeds:* the package's runtime is bun, like the hook.
3. Why not only code? — Use cases, fails-if conditions, six whys and conflict judgments need judgment (R12.3, R13).
   *Feeds:* the split — code enforces that the judgment step happened and has the required shape; the agent does it.
4. Why integrate into workflow-design? — It is the method every run starts from; a tool nobody's steps call is a
   rule written down again. *Feeds:* integration is an acceptance criterion, not a follow-up.
5. Why measure effectiveness? — "Enforced" is a claim; the harness-health backtest showed a built check catching 0 of
   7. *Feeds:* a pre-registered prediction and a control (rules-only) before the build.
6. Why now, before merging feat/harness-health? — EJ: "Don't merge first". The hybrid may replace parts of it.

## Provisional category

Code generation + code review (build a feature), with a research front (external: harness hook APIs) and an
evaluation tail. Default pattern from `docs/TASK_TYPES.md`: build-a-feature pipeline.
