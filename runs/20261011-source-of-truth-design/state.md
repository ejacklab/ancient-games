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
- 2026-10-12 commit `2940b32` ("Simplify the source-of-truth memory design and record EJ's decisions"): Claude
  revised the design together with EJ. Opencode did not, so the repair loop above was not run as such. The annotated
  version, with a provenance block listing what changed, is
  `runs/20261011-source-of-truth-design/DESIGN-detailed-2026-10-12.md`. Lines 8–11 of `SOURCE_OF_TRUTH.md` summarise
  EJ's decisions (EJ, 2026-10-12): no owners and no human approval gate; decisions and facts come before the code; a
  fact is a constraint the code must respect; the drift check covers decisions and facts only; a background subagent
  keeps memory current. The split of what is written immediately and what later is in
  `runs/20261012-memory-update-timing/notes.md`, where it is labelled "My reading — not in the sources".
- 2026-10-12 commit `df09e06` ("Memory design: drop proposed/active, journal is read at milestones"), pushed to
  origin/master. It removes the open question "who moves an entry from `proposed` to `active`". The commit's reason:
  that step existed only for the approval gate EJ removed, so it was a leftover, not a real open question.
  EJ, 2026-10-12: an agent reads `journal/` at each milestone and writes what is worth keeping as entries; `journal/`
  is still never loaded at session start.
- 2026-10-12 discussion only, the design did not change. EJ, 2026-10-12: task and project memory need a journal; user
  and agent memory do not. The main session checked this against `docs/research/20261011-agent-memory-graph-r2/`
  (s1-F19 EverMemOS, s1-F27 Agent Zero Memory, s1-F2). Its reading, not verified: the claim holds, but not because
  user and agent memory have no episodes — the research says they keep an episodic layer. It holds because their raw
  record already exists as private Claude Code transcripts that only one owner reads, while task and project memory
  need a shared raw record in the repo, and reading another agent's transcripts is excluded
  (`runs/20261011-project-memory-engines/RECOMMENDATION.md:187`). The design already matches the split: project
  memory has `journal/`, task memory has `work/<task-id>/events/`.
- 2026-10-12 four questions remain in the design's "Not decided yet (EJ decides)" list (line 78): which tool generates
  `INDEX.md` and what runs it; how the script tells that the entry changed earlier than the code; who resolves a git
  merge conflict; whether a changed decision is edited in place or superseded. The main session's reading: they are
  build details or have obvious defaults. The `INDEX.md` size number (line 126, "EJ sets the number") is the
  exception: it has no basis until an index exists. EJ has not ruled on any of them.
- 2026-10-12 the design is still a **draft, not accepted** (its header says so). The codex and Claude reviews
  (REPAIR, 2026-10-11) have not been re-run on the revised text, so whether the revision fixes their findings is not
  checked.
- 2026-10-12 commit `7757f21` ("Memory caches: research and design for SQLite FTS, vector and code graph"), pushed to
  origin/master, adds `docs/memory-system/CACHES.md`. It is the design for the `.cache/` that `SOURCE_OF_TRUTH.md`
  allows (line 104), and it is a separate run: `runs/20261012-memory-caches/`. The commit does not touch
  `SOURCE_OF_TRUTH.md`.
- 2026-10-12 `CACHES.md`'s conclusion, quoted from "The answer first": "None of the three caches is needed today."
  The three are SQLite full-text, vector and code graph. Each has a trigger, and every trigger number is left to EJ
  (`CACHES.md`, "Not known").
- 2026-10-12 `CACHES.md` proposes an answer to one of the open questions at line 78, "how the script tells that the
  entry changed earlier than the code". Quoted from its "What this changes elsewhere (proposed, not done)": "The
  research suggests an answer for EJ to decide: compare `git log` times of the entry file and its `covers:` paths."
  The proposal is for EJ to decide; `SOURCE_OF_TRUTH.md` has not been changed.
- 2026-10-12 `CACHES.md` also depends on the `INDEX.md` size limit, still open here (line 126, "EJ sets the number"):
  it is the full-text index's trigger. Quoted from its SQLite When row: "Built when the trigger fires: `INDEX.md` can
  no longer list every active entry."
- 2026-10-12 EJ accepted the design ("yes I accept the source of truth design"), with its vision and its Write / Keep / Read requirements. The status line in docs/memory-system/SOURCE_OF_TRUTH.md says so.
