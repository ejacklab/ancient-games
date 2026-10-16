# Harness requirements — release notes

## 2026-10-16 — R12.2: a check fails only on a written meaning, and warns where it guesses

An automatic check records a failure only where what it saw has a written meaning; where it can only guess it records a
warning, which the agent settles (logged as a failure, or dismissed with a kept one-line reason the owner may
overrule); a check drops what it saw only on a written "not a failure" meaning. Agreed with the project owner after two
false alarms in run `runs/20261016-integrate-r11-r13/` (F-3e11ce16, F-8392b4ce); the wording and the split between
"written meaning" and "guess" were the main agent's proposal, accepted as proposed. Guard rounds 8 and 9.

## 2026-10-16 — R13 moved to the requirement-check skill

R11 and R12 are harness validation and stay here; R13 (use cases and requirements) is a check of what the work is
built and judged against, so its one copy moved, unchanged and with its ids, to
`.claude/skills/requirement-check/references/use-cases-and-requirements.md`, and the skill's description and body now
cover it. `harness_health.py` reports R11 and R12 (R10 is replaced by R12). Run `runs/20261016-integrate-r11-r13/`.

## 2026-10-16 — R11–R13 accepted

Accepted by the project owner as a whole ("accept all the proposed requirements we discuss here"). Drafted and
discussed in `runs/20261015-harness-health/` (`requirements-draft.md`, `state.md`, the experts' `experts-*/compare.md`),
`runs/20261015-ts-hybrid/`, `runs/20261015-long-session/`, `runs/20261015-learn-success/`,
`runs/20261015-ga-learn-from-success/` and `runs/20261015-score/`. The three R12.7 defaults (where paths are kept, one
change per run, R12.7 extends the 20% challenger rule) were the main agent's proposals, accepted with the rest. Two
choices stay with the owner (R12.5 schedule, R12.6 reach).
