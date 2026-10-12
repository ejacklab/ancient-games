# State — 20261011-source-of-truth-design

## Challenge (verbatim)

> ok , let's get opencode to design this source of truth, why we need this memory, it is for who, for what , what
> will be put in , what will not, put where, when will be use, when will not be use

## Restatement (method 3.0)

**Objective.** opencode designs the source-of-truth memory: the eight questions answered, each grounded in the
verified recommendation from run `20261011-project-memory-engines`.
**In scope.** The eight questions, in EJ's order, as the whole document.
**Out of scope.** Building it; any ninth section; any value the source does not give (those stay `OPEN`).
**Provisional category.** `document and explain` (prose design for a human), verified by `code review`.

## Steps

| # | Node | Status | Output file |
|---|---|---|---|
| 1 | opencode 1.14.41, `minimax-coding-plan/MiniMax-M2.5` — design the source of truth | done (exit 0, 5.9 KB, read the source) | docs/memory-system/SOURCE_OF_TRUTH.md |
| 2 | blind verify (claude 2.1.296, `claude-sonnet-5-5`) — grounding, no invented values, one planted defect | done (items 1,2 PASS; item 3 FAIL on the plant; plant located exactly at line 35) | runs/20261011-source-of-truth-design/nodes/verify.stdout.md |

## Log (append only)

- 2026-10-11 brief written; opencode dispatched (job `bash-1115`), exit 0, and its stderr shows it read
  `RECOMMENDATION.md` — unlike its answer in the earlier research run, where it read nothing.
- 2026-10-11 planted an invented index cap ("500 entries") at line 35 of `verify/DESIGN-planted.md`; blind verify
  on claude found it and named the line. `VERDICT: REPAIR` for the planted copy; the unplanted design (now
  `docs/memory-system/SOURCE_OF_TRUTH.md`) passes all four items.
- 2026-10-11 **run accepted.** Deliverable moved on EJ's instruction to `docs/memory-system/SOURCE_OF_TRUTH.md`,
  with a provenance block; the run folder keeps the brief, the raw engine output, the verify verdict and the report.
  The folder name was chosen as `memory-system` so it does not squat on CP3 (codex's option is a memory tree *under
  `docs/`*) — the folder holds design documents about the memory system, not the memory tree.
- 2026-10-11 node 3, codex review (`gpt-6.1-sol`, medium effort, 27,972 tokens): **REPAIR**. Its planted control
  was caught at the right line and row (M16 vs M13), so the review can fail. Coverage PASS, no-invented-values
  PASS; OWNERSHIP FAIL (who may revise entries and maintain the artifacts is unnamed), CONSISTENCY FAIL (the
  `memory/` paths contradict the OPEN placement; "every entry carries" vs the source's "use applicable fields";
  M18's "auto-" dropped), GROUNDING FAIL (three beyond the control). Three findings re-verified by the COO.
- 2026-10-11 the design at `docs/memory-system/SOURCE_OF_TRUTH.md` is **open again**, not accepted: the repair
  (feedback to opencode, the designer) has not been run.
- 2026-10-11 node 4, Claude Code reviewing both tools (9.8 KB): **REPAIR**, HEADLINE: AGREE. It rejected the
  planted false codex finding (from the files alone) — but its two hypotheses about how that finding arose are both
  wrong: the COO planted it. It confirmed codex's M16/M13 finding, though it read `state.md`, so that catch is not
  blind. New findings codex missed: contested rows (M23, M24, M17, M6) cited as settled; no `model knowledge` label
  anywhere; staleness dropped in favour of an age threshold; missing layout places; `OPEN:` without "by whom". It
  corrected codex twice (the provenance block was charged to the design; the "every field" conflict is inside the
  source, M11 vs R:140) and admitted its own earlier grounding PASS was lenient and self-authored.
- 2026-10-11 three engines have now spoken: opencode wrote the design; codex and claude both say REPAIR. The design
  at `docs/memory-system/SOURCE_OF_TRUTH.md` is **not accepted**; the repair has not been run.
