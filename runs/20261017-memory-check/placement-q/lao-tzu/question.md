# Question — where does memory-check belong in the workflow-design method?

The owner (EJ) asks: the tool is built — which part of the workflow-design algorithm should use it? The owner decides.

Rules for this question:
- Rest each point on a fact below (each with its source) or one you check in this repository; a point from memory
  only is labelled *recall* and does not decide alone.
- Keep the owner's aim in view: fewer, better steps, not more. A placement that adds a step must show what it catches
  that nothing in the method catches now.

## Facts
- The method: `docs/WORKFLOW_DESIGN_METHOD.md`, steps 3.0 (understand) · 3.1 (readiness) · 3.2 (algorithm) · 3.3
  (unclear spots) · 3.4 (size) · 3.5 (loops) · 3.6 (graph, acceptance) · 3.7 (sequence) · 3.8 (running a node) ·
  §4 (state and memory) · §5 (three qualities). Source: its headings (lines 34–625). The skill's eight steps:
  `.claude/skills/workflow-design/SKILL.md`.
- 3.1 Readiness already names read-only checks run before work: `readiness.py` (tools), `harness_health.py` (how each
  harness is set up), the guard's `doctor` (hooks installed). Source: `docs/WORKFLOW_DESIGN_METHOD.md` lines 92–110.
- §4 says project memory follows `docs/memory-system/SOURCE_OF_TRUTH.md` and its caches `CACHES.md`, applied per
  node in the five fields every node carries (Tools, Context, Contract, Evidence, State). Source: the same file,
  lines 578–600.
- The tool: `memory_check/` — finds a project's memory, checks it against those two guidelines, prints a report and a
  short warning (`--warn`: failing MUSTs and a missing `AGENTS.md`); read only; 70 tests pass. Source:
  `memory_check/VISION.md`, `memory_check/REQUIREMENTS.md`, `cd memory_check && bun test`.
- A session-start hook running `--warn` is proposed and waits for the owner's yes. Source:
  `runs/20261017-memory-check/settings-diff.md`.
- This repository has no `project-memory/` yet, so on it the tool reports almost everything "not applicable". Source:
  `runs/20261017-memory-check/nodes/smoke-report.md`.

## The decision
1. Which step (or steps) of the method should run memory-check, and at what moment (before a run, per node, at the
   end of a run, at session start only)? Name the step by its number.
2. What does that step do with the result — stop, ask the owner, carry on with a note? Tie it to the result states
   (pass, fail, needs a reviewer, not applicable, could not run).
3. Is anything in the method now redundant once the tool exists, or anything it must not do?

End with your recommendation in four lines or fewer.
