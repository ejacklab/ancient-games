# Workflow design — 20261012-caches-merge

## Challenge (verbatim)

> create and design a workflow to delegates 3 subagents, use agy , dsh cli , codex and opencode , to review both
> version , and discuss and come out with the best version that have the strenght of both version

## Restatement (method 3.0)

**Objective.** A single version of the caches design that keeps the strengths of both drafts. It comes from three
independent reviews, one round of discussion between the reviewers, and a merge.

**The two versions.** Both are copied into `inputs/` under neutral names, with sha256 recorded:
- **Version A** (`runs/20261012-caches-enhance/CACHES.md`): reasoned from earlier research. A 21-row decision table
  for memory entries, the cost GAPs, and six disagreements (D1–D6) left unresolved.
- **Version B** (`runs/20261012-caches-routing/CACHES.enhanced.md`): measured on this repo's code and docs. Tables
  BM-1 to BM-9, a routing table for development and testing, and runtime coverage for test selection.

**Who does what.** My reading of the request:
- the **three subagents** are the three reviewers: **agy, codex and opencode**;
- **dsh** writes the merge.

dsh is the only engine that did not write either version, review it, or build its evidence. codex and opencode
each contributed to both runs, which is a stake noted under "Independence" below. agy contributed to neither.

**In scope.** Reviewing both versions, the discussion round, the merged draft, and a check of the merge.

**Out of scope.**
- Editing any shared file: `docs/memory-system/*` stays as it is, per the rule both sessions adopted.
- Building or measuring anything new.
- Changing the vision: the vision proposals stay EJ's call.

**Category.** code review (three independent reviewers) → join (merge) → document and explain, with a check.

## Readiness (verified 2026-10-12)

| Engine | Canary | Model, effort | Read-only form |
|---|---|---|---|
| agy 1.3.3 | `AGY-OK`, exit 0 | `gemini-3.1-pro-high` (from `agy models`) | `--mode plan` |
| codex-cli 0.160.0 | `CANARY-OK`, exit 0 (earlier today) | `gpt-6.1-sol`, effort high | `--sandbox read-only` |
| opencode 1.18.34 | ran twice today | `minimax-coding-plan/MiniMax-M3.1-Flash-Preview` | `--agent plan` |
| dsh (headless profile) | `DSH-OK`, exit 0 | `deepseek-flash`, the profile's model (read from `~/.dsh/profiles`, reported; dsh takes no `--model`) | prints to stdout; the task is given on stdin |

## Nodes (state file `state.md`; the driver is `run.sh`)

| # | Node | Engine | Input | Output |
|---|---|---|---|---|
| R1 | Round 1: independent review of A and B against a fixed rubric | agy, codex, opencode, run in parallel | both versions, their evidence, the vision | `reviews/r1-<engine>.md` |
| R2 | Round 2: discussion. Each reviewer reads the other two reviews and, for each point of disagreement, holds or changes its position with a reason. No new topics | agy, codex, opencode, run in parallel | own R1 and the other two R1s | `reviews/r2-<engine>.md` |
| M | Merge: the best version, with every section traced to A, B or a review. Points still disputed after R2 become explicit rows, never averaged | dsh | both versions and all six reviews, inline on stdin | `merge/CACHES.merged.md`, `merge/merge-notes.md` |
| V | Check: every id and number in the merge traced to A or B (script); the never-rules kept; no shared file touched; then a read by the COO | COO (script, then reading) | the merge and both inputs | `verify/check.md` |

**Parallel only where it holds.** R1 and R2 are each three independent, read-only engines writing separate files.
R2 needs all three R1s, so R1 → R2 is a barrier. M needs all of R2. V needs M.

**Bounds.**
- One call per engine per round.
- `timeout 1500` per call.
- One discussion round.
- No retries: a failed engine is reported, and the merge proceeds with the reviews that exist.

## Independence

- **codex** wrote B's question set and reviewed B's section, and it answered A's vector question.
- **opencode** built B's harness, and it answered A's SQLite question.
- **agy** touched neither.
- The reviewers are told the versions only as A and B. The content still names its runs, so the blinding is partial.
- The merge is done by dsh, which touched neither version.

## Stop conditions

- **Done:** `merge/CACHES.merged.md` exists; every id and number in it traces to A or B, or is flagged; every
  disputed point is an explicit row; and `git status` outside this folder matches the baseline.
- **Failure:** fewer than two R1 reviews. The run stops and reports.

## Predictability, debuggability, quality control

- **Predictability:** fixed nodes, a one-round discussion, no retries, and a fixed rubric.
- **Debuggability:** every engine's prompt is in `briefs/`, its command line in `run.sh`, and its raw stdout and stderr
  in `reviews/` or `merge/`.
- **Quality control:** three independent kinds review; the merger is a fourth kind with no stake; the trace check is a
  script, written by the COO, and `verify/check.md` says what that script does not establish.
