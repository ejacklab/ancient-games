# State — 20261002-prompt-corpus-campaign

Rules: one writer at a time. Read this file before your step; update it after. Progress and results only —
never reasoning. Never delete a log line.

## Challenge (verbatim)

> yes, take it as testing material, create 300 testing prompts, test 100 on first round, then collect all the
> bugs and lession learns, enhance at the ending, then retest with the second 100 testing prompts, then collect
> all the bugs and lession learn is there are, and enhance again, lastly run the 3rd 100 set of prompts
> testing. see the generated design, collect all the issues and lesson learns for enhancement again, do them at
> the ending, then gerate a report of what have been fix and enhanced, any principle changes or not. may
> directly use agy and codex in the testing

## Restatement (method 3.0)

Objective: `tests/operator-prompt-list.md` becomes testing material: a 300-prompt corpus exists; three rounds
of 100 prompts each run through the §3.0-understand + TASK_TYPES default-first pipeline; every round's bugs and
lessons are collected and the system enhanced at the round's end; round 3 also reviews the generated designs; a
final report states what was fixed/enhanced and whether any principle changed. All repo checks green at the end.
In scope: corpus + harness under tests/, enhancements to TASK_TYPES.md / design_gate.py / method-skill copies
where lessons demand, executor samples via codex + agy (quota approved by EJ this turn), run artifacts here,
campaign reports in docs/research/20261002-prompt-corpus-campaign/. Out of scope: ancient_games/ framework
code, intake.js encoding (TODO.md), committing or pushing (EJ says when), changing SPEC/DECISIONS.
Six whys: (1) the taxonomy + gate were built from a synthetic 16-prompt corpus — untested against EJ's real
prompting distribution; (2) now, because the real 90-prompt file just arrived; (3) this shape (rounds with
enhancement) because bugs found early must not pollute later rounds — each round tests the enhanced system;
(4) failure = a taxonomy that misroutes real work, or false confidence from a circular test; (5) stops when
3 rounds are green + report written + repo checks pass; (6) done = corpus_check exit 0 per round, executor
agreement measured, report file exists, pytest/harness/gate green. Categories (inferred): multi step planning,
test cases gen, test script gen, research and reports, run grading — combination not in TASK_TYPES pipelines →
full method (others), sequential rounds, script gates.

## Baseline

`git status --short`: 7 modified + 9 untracked paths (the 2026-10-01 task-types system, uncommitted, plus
tests/operator-prompt-list.md and .qwen/, runs/). pytest: **395 passed**. intake harness: all passed.
design_gate --self-test: PASS. readiness --self-test: PASS.

## Steps

| # | Step | Status | Output |
|---|---|---|---|
| 1 | Canaries: codex + agy (+1 sabotage) | done | canary/ |
| 2 | Corpus round 1 (100 prompts) | done | tests/fixtures/operator_prompts_r1.jsonl |
| 3 | Harness corpus_check.py | done | tests/workflows/corpus_check.py |
| 4 | Round 1: classify, gate, executor samples, bugs, enhance | done | results_r1*.jsonl, round1.md |
| 5 | Round 2: same on prompts 101–200 | done | results_r2*.jsonl, round2.md |
| 6 | Round 3: prompts 201–300 + generated designs review | done | results_r3*.jsonl, designs_r3/, round3.md |
| 7 | Final report + full regression | done | REPORT.md |

## Canary log

- canary codex 0.159.3 pass: fixed-answer exact; sabotage task reported "CANARY FAIL cannot read" (can-fail proven)
- canary agy 1.2.14 fail→pass: attempt 1 exit 2 (`--print-timeout 120` rejected — needs duration suffix `120s`);
  attempt 2 exit 0 with EMPTY stdout + approval-denied notice on stderr (the documented soft-denial trap; house
  rule "exit code alone is never the check" caught it); attempt 3 with "Do not use any tools." prefix: pass,
  exact content, clean stderr.
- Lesson L0: every agy headless call needs the no-tools prefix + `Ns` duration suffix; wrapper prompts must
  carry both. Candidate for EXECUTOR_KINDS.

## Log (append only)

- 2026-10-02 step 0 done: run folder created, baseline taken (395 passed), restatement written.
- 2026-10-02 step 1 done: canaries pass (codex first try + sabotage; agy third try, two failure modes logged).
- 2026-10-02 steps 2–4 done: corpus r1 (100), harness corpus_check.py, classification, 35 script bugs
  (GAP/G2/G6 false positives) fixed by two new rows + tri-state product column; executor samples codex 12%/32%,
  agy 24%/72% strict/lenient; labelling rules written into TASK_TYPES.md; checker exit 0; tests 15/15.
  Report: docs/research/20261002-prompt-corpus-campaign/round1.md. No principle changes.
- 2026-10-02 step 5 done: round 2 (p101–p200). Checker 0 bugs on first pass. Executor agreement with rules
  embedded: codex strict 12%→84%, agy 24%→72%. Five disagreement classes (C1–C5) fixed by labelling rules 1/3/5/6
  amended + rule 7 added. Key lesson L5: flash tier collapses vague→tiny (fail-unsafe); the tiny call needs
  script gate + COO verdict review. Report: round2.md. No principle changes.
- 2026-10-02 step 6 done: round 3 (p201–p300). Gate caught the corpus author's own p269 label (rule 5
  refined); executor agreement codex 96%, agy 76%/88%; rules 8–9 added. 100 designs emitted and gated;
  blind codex review 2 ACCEPT / 3 REJECT (G6 dilution, missing regrade node, unmaterialized doc review);
  repairs verified ACCEPT (p279 needed a builder fix after hitting its attempt limit — documented).
- 2026-10-02 step 7 done: full regression green (397 pytest, intake harness, gate + readiness self-tests,
  three checkers exit 0). Final report: docs/research/20261002-prompt-corpus-campaign/REPORT.md.
  Principle changes: none. Campaign stop condition met.
- 2026-10-02 post-report regression: the round-3 builder enhancement broke round-1 p073 (a building document
  design got a same-kind embedded review node) — G6 caught it on the re-run. Builder fixed (doc review node
  takes a different kind when the doc piece builds), regression test added. All three rounds exit 0 again.
- 2026-10-02 addendum: re-running all three rounds after each enhancement caught two regressions (p073
  embedded doc-review kind; p195/p273 multi-kind build groups). Fixed: G6 reviewer→worker pairing via the
  reviews field, per-kind review splits, builder updates, regression test. Final: rounds 1/2/3 exit 0,
  398 pytest passed, self-tests PASS, harness passed. Campaign closed; nothing committed (EJ's call).
