# State — 20261012-index-md-build

Rules: one writer at a time. Read this file before your step; update it after. It holds progress and results only —
never reasoning; put notes in your own output file. Never delete a log line.

## Challenge (verbatim)

EJ, 2026-10-12: *"our objective here is to build the tool to gen index , doc are at docs/index-md/*"*, then *"you
active the workflow design and ancient game skills"*, then *"design a workflow to complete teh whole SDLC of this index
dev and test"*.

## Restatement (method 3.0)

Build `tools/memory_index.py`, `tests/test_memory_index.py`, `.githooks/pre-commit` and `.githooks/pre-merge-commit`
on a branch. Every in-scope Fails if in `docs/index-md/REQUIREMENTS.md` gets a test that is proved able to fail, and
the suite still passes. Out of scope: DESIGN's do-not list, G1.2, G4.1 and the B4 open line. Category (*inferred*):
code generation + test cases gen + code review. Full text: `workflow-design.md`.

## Baseline

`git status --short`, main tree, 2026-10-12, before this run folder was created:

```
 M docs/TASK_TYPES_LEDGER.md
 M docs/memory-system/CACHES.md
 M docs/memory-system/SOURCE_OF_TRUTH.md
 M docs/memory-system/vision-statements/caches-memory-vision-statements.md
 M docs/memory-system/vision-statements/source-of-truth-memory-vision-statements.md
?? .claude/workflows/research-agent-memory.js
?? docs/code-graph/
?? docs/index-md/
?? docs/research/20261011-agent-memory-graph-r2/
?? docs/research/20261011-agent-memory-graph/
?? runs/20261011-agent-memory-graph-r2/
?? runs/20261011-agent-memory-graph/
?? runs/20261011-project-memory-engines/
?? runs/20261012-caches-enhance/
?? runs/20261012-caches-requirements-review/
?? runs/20261012-caches-routing/cov/.coverage
?? runs/20261012-index-md-algorithm/
```

Spec hashes at design time (N0 re-records them before the run):

```
e5d6778e6d6fe23a6716e7e4b5490dc9674bc6b6106e58852a414a91dc3d58d8  docs/index-md/DESIGN.md
f8fb52b40a7a7dc8f0af78c309bfb28ceef97c2fe6572dd80173c17bfdc8028d  docs/index-md/REQUIREMENTS.md
e14a3fceb174a21b6c08838a3ac1cf5779c3a3e199c4c9970a5cdfe74c60c208  docs/index-md/VISION.md
```

## Product baseline

At design time, in the main tree: `env -u NO_COLOR python3 -m pytest -q` → `529 passed in 31.61s`. N0 records the
per-test version in the worktree (`baseline.json`).

## Steps

| # | Step | Status | Output file |
|---|---|---|---|
| D | Design | done | workflow-design.md, readiness.md, design.json |
| N0 | Prep: pin, worktree, baseline, canaries | done | nodes/n0-1.result.md, baseline.json, plan.json |
| N1 | Acceptance tests, blind (Codex) | done | nodes/n1-<a>.result.md |
| N2 | Script, hooks and unit tests, loop (opencode) | done | nodes/n2-<a>.result.md, gate-<a>.txt |
| N3 | Sabotage: mutants | done | nodes/n3-1.result.md |
| N4 | Blind review, planted defect (Claude Sonnet 5.5) | done | nodes/n4-<a>.result.md |
| N5 | Close: traceability, must-not, ledger, report | done | traceability.md, report.md |

## Blueprint

Kind of task: feature. Map: none (spec in `docs/index-md/`). Needed sections not settled: vision: draft, requirements:
draft, architecture (`DESIGN.md`): draft → Q1.

## Size decision

design — steps: 6, unclear spots: 3 (all decisions with provisional assumptions), risk: medium.

## Unclear spots

| Id | What is unclear | Kind | Blueprint section | Blocks steps | Depends on spot |
|---|---|---|---|---|---|
| U1 | Build against the draft spec? | decision | vision, requirements, architecture | N1–N5 | — |
| U2 | Override `workload.py` so all tests are Codex's | decision | none | N1, N2 | — |
| U3 | Backlog location | decision | none | N4, N5 (writing only) | — |
| U4 | opencode effort flag for MiniMax-M3.1-Flash-Preview | unknown | none | N2 dispatch | — (N0 canary) |

## Questions for EJ (one batch)

| # | Question | Provisional assumption if unanswered | Must be answered before building |
|---|---|---|---|
| Q1 | Build against the current drafts? | EJ: *"as you suggest"* → yes, pinned by hash | answered |
| Q2 | Override `workload.py` (opencode code, Codex tests)? | EJ: *"we can have another diff test"* → read as: no override; opencode writes code + unit tests, Codex writes a separate blind acceptance file | answered (reading stated to EJ) |
| Q3 | Backlog at `docs/index-md/BACKLOG.md`? | EJ: *"follow what you suggest"* → yes | answered |

## Log (append only)

- 2026-10-12 D done: design written; readiness ran (tools verified, canaries not run); baseline 529 passed; workload.py
  tried on 1- and 2-module plans (script self-tested in both) → Q2.
- 2026-10-12 D gate: `design_gate.py design.json` → PASS, after a first run gave 6 findings (G3 ×3: no brief, G9 ×2: no sabotage, G10: no baseline). The gate checks structure only. The blind checklist review of the design (Codex, because it builds) has **not** run.
- 2026-10-12 Q1–Q3 answered by EJ (see the table). Q2 changed the design: N2 also writes `tests/test_memory_index_unit.py`, and N3's mutants must be killed by the acceptance file. Waiting for EJ's go to start N0.
- 2026-10-12 EJ: "go , complete the whole cycle".
- 2026-10-12 N0 done: hashes unchanged; worktree /home/smoke01/dev/ancient-games-index-md @96caa07 (build/index-md); baseline 529/529 ×2; canaries ok after </dev/null (codex hung on stdin: "Reading additional input from stdin..."); opencode --variant high accepted. Interface fact given to both workers: the script works on the git repo of its cwd.
- 2026-10-12 N1 attempt 1 dispatched: codex gpt-6.1-sol high, workspace-write, -C worktree, outer 1200 s.
- 2026-10-12 N1 done (attempt 1, 495 s, codex gpt-6.1-sol high per stderr header; its result header says "exact model identifier not exposed"): 35 test functions / 130 cases; COO check: collect ok, trace_check 29/29, 129 failed all with "tools/memory_index.py is not built yet" + 1 [static] pass. Frozen as c93d8fe on build/index-md (N2's gate base-ref).
- 2026-10-12 N2 attempt 1 dispatched: opencode MiniMax-M3.1-Flash-Preview --variant high --agent build, outer 1500 s.
- 2026-10-12T15:47:56Z COO session restarted mid-N2; the N2 call survived (pid alive, 4 files written). The old scratchpad with the N3 runner was lost; runner rewritten at checks/mutate.py (generic, no mutants in it). Mutants will be kept outside worker-read files until N5.
- 2026-10-12 N2 attempt 1: opencode 586 s, exit 0; COO gate PASS (tests/baseline/scope/must-not/tamper, 673 tests). COO join on its "Choices not in the spec": (1) untracked inactive entry -> warning, done to satisfy test_inactive_content_problems_warn_without_blocking[write], whose write-mode case never stages D-old.md — the test contradicts B1.2 ("An untracked entry file is an error"), spec wins; (9) `--check <bad rev>` -> exit 0 "nothing to check" breaks C1.2 (pass only when valid/equal/in limits; C1.3 exempts only unborn HEAD). Verdict: failed attempt. Outside criteria for backlog: (5) deleted-but-tracked entry keeps its line in write mode. Citation: CACHES.md agy row is line 446 at HEAD, 519 in the main tree's uncommitted copy -> cite the row, not a line.
- 2026-10-12 N1 attempt 2 (repair, last) dispatched: fix the write-mode staging defect, add untracked-retired (B1.2) and bad-rev (C1.2) tests. N2's code stashed out of the worktree (git stash "n2-1 code, hidden from n1 repair") so the test writer stays blind.
- 2026-10-12T15:52:59Z N1 attempt 2 done: COO check collect 133, trace 29/29, 132 red + 1 static; frozen as f6af152 (new gate base-ref). N2 code restored from stash. N2 attempt 2 dispatched (feedback: briefs/n2-2-feedback.md).
- 2026-10-12T15:58:15Z N2 attempt 2 done: opencode 268 s exit 0; COO gate PASS (678 = 529 + 133 + 16), base f6af152; committed on build/index-md. Backlog for EJ: (a) tracked entry deleted from the working tree -> warning, no line; (b) B4.2 'every run prints the size' vs DESIGN step 5 exiting before step 7 — no size line on invalid entries.
- 2026-10-13 N3 round 1: 32 mutants (one or more per in-scope Fails if; mutants kept outside worker-read files until N5), 30 killed. Survivors: one is **equivalent** (C1.2 bad rev still exits 1 through the git error path; verified by hand); one is a **B2.4 test gap** (no test fails only because a staged active entry is malformed). One N3 repair round dispatched to codex in a code-free worktree at f6af152 (/home/smoke01/dev/ancient-games-index-md-tests), brief briefs/n1-3.md.
- 2026-10-12T16:06:55Z N3 done: after the repair round (codex added test_staged_malformed_active_entries_fail_without_writing, frozen 9979add; it passes on the code unchanged), gate PASS 682, mutants 31/32 killed, the survivor equivalent. N4 dispatched: Claude subagent sonnet, effort high, read-only packet outside the repo with one plant.
- 2026-10-13 N4 done: Claude subagent sonnet-5.5 (high), 128 s, 97k tokens. **The plant was found** (its F1: write_atomically writing INDEX.md directly; the plant was in the review copy only — the real code uses temp file + os.replace). In criteria, fixed by the COO (each one sentence, under the 8-call cap): F2 an unreadable/deleted tracked entry is now an error (Must not 4), F3 the over-limit warning also prints when INDEX.md is already up to date (B4.3), F5 OSError is reported as `<file>: <problem>` (B2.6). Each has a unit test; reverting each fix turns its test red (nodes/n4-fixes-sabotage.md). Gate PASS 685 (base 9979add), mutants 31/32 (the survivor is the equivalent one). Outside criteria → docs/index-md/BACKLOG.md: F4, F6, O1–O5, plus N2's choice that write mode skips the size line on invalid entries.
- 2026-10-13 N5 done: spec hashes unchanged; branch adds only the planned files; hooksPath unset; no project-memory/; master moved to baf9643 (another session, no shared path). Plant and mutants copied into sabotage/ after the verdicts. traceability.md 29/29 rows. BACKLOG.md written (Q3 location). harvest_run.py matched no rollouts (0 tokens); token counts taken from engine stderr instead. Ledger row added. Test worktree removed. report.md written. Run ends at EJ's acceptance; merge/push not done.
- 2026-10-12T16:18:02Z EJ: "merge it to master". Merged build/index-md into master as 17c73f1 (no-ff, no conflicts); full suite on master 685 passed; `--check HEAD` → nothing to check (no project-memory/ yet). Not pushed.
