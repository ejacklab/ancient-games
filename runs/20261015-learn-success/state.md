# State — 20261015-learn-success

Challenge (EJ, 2026-10-15): "now design and execute a workflow to build this newer enhance requirements, if anything can
be parallel do it, I wish can complete within an hour". The requirement: R12.7 Learn from success
(`runs/20261015-harness-health/requirements-draft.md`). Started 14:49 UTC; aim: done by 15:49 UTC.

## Design (compact; method 3.0–3.7)

- Objective: the guard records every checked result (success lines), shows rates, validates success paths (borrow,
  don't copy; 2% aim reported), checks great-success insight sections, and Stop asks once for the path.
- Pieces and engines (disjoint files, so parallel holds — method 3.7): tests by Codex ×3 (hooks, paths, insight) from
  SPEC alone; code by a Claude subagent (hooks.ts, journal.ts, rates.ts, cli.ts), opencode (paths.ts), a Claude
  subagent (insight.ts) — each test file from a different engine than its code. Only one opencode run (the parallel
  opencode trap). COO: spec + types (done first, `f8d1a51`), integration, mutants, live check.
- Checks: the full guard suite (922 before) + round-5 tests; tsgo; COO mutants; one live haiku session with hooks.
- Worktree `../ancient-games-success`, branch `feat/learn-success`; merge on EJ's earlier "merge it" only after the suite passes.

## Steps

| # | Step | Status |
|---|---|---|
| 1 | Spec + types | done 14:50 |
| 2 | Tests ×3 and code ×3 in parallel | doing |
| 3 | Integrate, full suite, mutants | todo |
| 4 | Method/skill text, export | todo |
| 5 | Live check (one haiku session) | todo |
| 6 | Merge, report | todo |

## Log

- 14:49 worktree; 14:50 spec + types committed; 14:51 six nodes started in parallel.

## Prediction for the live check (written before it runs)

One long-session arm-B run (template2, haiku, hooks from the round-5 guard): the journal holds success lines for the
green test runs, the Stop hook asks for the path once, the agent writes a path file that `path check` passes, and
`rates` shows the test runs' ok/fail counts. The insight for the engine failures is written as before.

## Result

- 14:50 spec + types; 14:51 six nodes in parallel (Codex ×3 tests; Claude subagent ×2 and opencode code); 14:55 all
  back; 2 conflicts reconciled by the COO (22 old "no record" assertions vs S1's success line; a child path with no aim);
  1078/1078, tsgo clean; COO mutants 4/4 killed (`mutants.txt`); method 3.8 item 13 + SKILL.md step 8; Python 1031 in
  the worktree; merged `affbc2b` → master at 14:57 (8 minutes from spec to merge).
- Live check (prediction above), one hooked long session, haiku, 371 s: **held** — 6 `success` lines for green test
  runs and 2 for engine calls, the Stop hook asked for the path once, the agent wrote `.harness-guard/paths/textstats-tdd.yaml`
  and `path check` passes it, `rates` gives ok/fail per check, no open failures. Also logged by the agent itself: three
  of its own failures (`notes-accuracy`, `tool-call-completed`, `codex-review-output`).
- **Unplanned:** after the shim's empty output, the agent called the **real** codex binary by its full path
  (`/home/smoke01/.npm-global/bin/codex exec …`) for both reviews — 2 real Codex calls spent; they returned output, so
  those 2 `engine-call` successes are real. Not foreseen by the sandbox design (the shim was only first on PATH).
- The guard logged the COO's own failures this session and asked for this build's path: `insight.md` and
  `success-path.yaml` here.
