# State — 20261015-harness-health

Rules: one writer at a time. Read this file before your step; update it after. It holds progress and results only —
never reasoning; put notes in your own output file. Never delete a log line.

## Challenge (verbatim)

> design and execute a workflow that enhance the readiness step to also validate a harness health conditions, if not
> good enough can we provide some help, get the 4 experts to plan and design these.

(EJ, 2026-10-15. The ten requirements it refers to: `harness-ten.md`.)

## Restatement (method 3.0)

`challenge.md` — objective, scope, six whys, provisional category (code generation + code review on an existing tool).

## Baseline

`git status --short` before the run folder: `pre-run-git-status.txt`. Readiness before: `readiness-before.json`.

## Product baseline

```
env -u NO_COLOR python3 -m pytest -q tests/test_readiness.py
26 passed in 12.50s
```

## Steps

| # | Step | Status | Output file |
|---|---|---|---|
| 1 | Intake, readiness and blueprint check | done | challenge.md, readiness-before.json |
| 2 | Four experts + Dave: plan and design (with unclear spots U1–U7) | done | experts/, experts/compare.md |
| 3 | Merge into one design; resolve spots; size | done | workflow-design.md |
| 4 | Build in an isolated worktree, tests + sabotage | done | build evidence under this folder |
| 5 | Independent review of the build | done | review.md |
| 6 | Report to EJ; merge only on EJ's word | doing | report.md |

## Blueprint

Kind of task: feature to the method's own tooling. Map: none — the skill scripts have no `docs/blueprint/`; the
target is method 3.1 and the acceptance criteria written in `workflow-design.md`. Assumption (main agent): EJ's
"design and execute" accepts building against those criteria; the build stays on a branch until EJ says merge.

## Unclear spots

| Id | What is unclear | Kind | Blueprint section | Blocks steps | Depends on | Raised by |
|---|---|---|---|---|---|---|
| U1 | Which harnesses are checked | decision | none | 3,4 | — | COO |
| U2 | What "help" is | decision | none | 3,4 | — | COO |
| U3 | "Good enough" with no thresholds | decision | none | 3,4 | — | COO |
| U4 | Extend readiness.py or a new script | decision | none | 4 | — | COO |
| U5 | How the result changes the design | decision | none | 3 | U3 | COO |
| U6 | Harness config formats unverified | unknown | none | 4 | — | COO |
| U7 | Requirements judged per run, not per harness | decision | none | 3 | — | COO |

## Log

- 2026-10-15 step 1 done: readiness.py exit 0; test_readiness 26 passed; run folder created.
- 2026-10-15 step 2 started: `four_experts.py run --question-file expert-question.md --out experts --claude-by-caller`; Dave by a Claude subagent.
- Note: Rule 12 of ~/CLAUDE.md (claim a VTIC ticket) not applied — this repo does not use VTIC (no references outside runs/); the run folder is the claim.
- 2026-10-15 step 2 done: 5 answers; check 2 failures (老子 為/爲 variants), --sabotage 2 failures as required; compare in experts/compare.md.
- 2026-10-15 U6 settled by evidence: codex keys verified on 0.160.0 (evidence/u6-codex-keys.txt); claude keys reported from 2.1.299 binary strings (evidence/u6-claude-keys.txt).
- 2026-10-15 step 3 done: workflow-design.md (decisions, proposed effects n=0, AC1–AC7); prediction.md written before probe code.
- 2026-10-15 step 4 done: worktree ../ancient-games-harness-health, branch feat/harness-health, commit cb808f1. Baseline 994 passed → 1013 passed. Mutation check 4/4 caught (evidence/mutation-check.txt). Machine run: evidence/harness-health-this-machine.md.
- 2026-10-15 step 6 (backtest) done: 0 of 7 flagged, as predicted (backtest.md).
- 2026-10-15 step 5 started: Codex gpt-6.1-sol read-only review, brief briefs/review.md → review.md.
- 2026-10-15 step 5 round 1: Codex — AC2–AC5 did not hold, 9 defects (review-round1.md); fixed in d7a1390, 30 tests, 1024 passed; 12 new/changed tests fail on cb808f1.
- 2026-10-15 step 5 round 2: Codex — 5 round-1 defects fixed, 3 partly, 1 not; 6 defects (review-round2.md); 5 fixed in d743b10 (not re-reviewed; 5 tests fail on d7a1390), 1 kept as stated (covered = script exists). Full suite 1029 passed.
- 2026-10-15 step 6: report.md written; waiting on EJ — questions 1–6, merge.
- 2026-10-15 EJ adds an eleventh requirement: "add 1 more for this check is we must know that are we able to insight the prompt results or not , at least 80% ?" — run through requirement-check; unit, meaning of "insight", level and below-80% action sent back to EJ. Not built.
- 2026-10-15 EJ clarifies R11: "it is more towards the idea, that the idea have rules, checks , tests , eval tool or design standards" — R11 is about whether results can be judged, not about engine logs. Redrafted; unit and place in the method sent back to EJ. Not built.
- 2026-10-15 EJ adds to R11: "and normally the verification should have a fasst feedback method" — proposed as a SHOULD measured by comparison (judge time against the prompt's own run time), no number invented. Not built.
- 2026-10-15 EJ: "yes, should the idea case, because some requirement can be verify within an hour some mnight need half day, or you can imporve this statement?" — R11.2 redrafted: speed bound moves to a first signal; the full verdict's duration is written in the design, not limited. Not built.
- 2026-10-15 EJ: "ok now ask the 4 experts to review the 11 harness requirements" — four_experts.py run --question-file expert-question-r11.md --out experts-r11 --claude-by-caller; Dave by a Claude subagent.
- 2026-10-15 experts-r11 done: 5 answers, no fallback; check 2 failures (老子 為/爲 variants), --sabotage 2 as required; compare in experts-r11/compare.md. Waiting on EJ — 9 questions.
- 2026-10-15 EJ on R11.1: "80% is our target to achieve, how I image is you will gen a plan or a eva for a requirement, then we will looks at the test coverage, why 80% those very basic things and 1 in a million edge cases those doesn't required to test. make sense?" — settles Q1 (unit = cases in a requirement's eval plan) and gate-vs-report (a target). R11.1 redrafted; who marks basic vs rare left open.
- 2026-10-15 EJ: "for me normally I get requirement, I will gen use cases, and also see old use cases cover this requirement or not. and use AI to gen out all possibily, but actually not all require to be covered. so we get the 80% of all the possibility will do. make sense, you you want to ask 4 experts they have better idea or approaches?" — four_experts.py run --question-file expert-question-coverage.md --out experts-coverage --claude-by-caller.
- 2026-10-15 experts-coverage done: 5 answers, no fallback; check 9 failures, all 老子 script/bracket variants of its own list (read, not inventions); --sabotage 2 as required; compare in experts-coverage/compare.md. Waiting on EJ — 6 questions.
- 2026-10-15 EJ answers the coverage questions: "1 yes, 2 consequence, 3 sun tzu, 4 yes, 5 go" — and adds: "each failure is more important the success. the evaluator must handle failure cases, log properly. end of a task create an Insign from the failure and we can check 6why and RCA to improve the harness. make sense?" — decisions written as full rules in requirements-draft.md; trial started in coverage-trial/.
- 2026-10-15 EJ (mid-turn): "the evalution rules must put more efforts on know what is wrong more but not teling what is correct more. so the AI can be more creative find a better algo than human." — R12.4 added to requirements-draft.md.
- 2026-10-15 coverage trial done (coverage-trial/results.md): A 28 cases 46% raw, B 200 cases 20% raw, units 80% both — prediction held (n=1, main agent's mapping). Found: W1.1b fails-if (c) rename has no test and no code.
- 2026-10-15 EJ: "so, 3 things are the must now, visions, requirements and use cases. actually to me use cases should come first. which one come first? 4 experts" — four_experts.py run --question-file expert-question-order.md --out experts-order --claude-by-caller.
- 2026-10-15 experts-order done: 5 answers, no fallback; check PASS 0 failures, --sabotage 2 as required; compare in experts-order/compare.md. Waiting on EJ — 7 questions.
- 2026-10-15 EJ: "use cases, can be from me, I give the most basic one. then ai agent can suggest more, and ask the user me, want to cover or not. to me use cases are must and requirements are SHOULD have. requirements use to cover details that not clear in the use cases. but we know that most important the results are valid for use cases. as requirements are normally details, requirements are must follow. this direction make sense? and also requirements can be suggest by AI agent based on vision and use cases. also of course provide by the user. ask the 4 experts how about this directions?" — four_experts.py run --question-file expert-question-direction.md --out experts-direction --claude-by-caller.
- 2026-10-15 experts-direction done: 5 answers, no fallback; check 1 failure (老子 善故能勇 for 慈故能勇 — a misquote, not a variant); --sabotage 2 as required; compare in experts-direction/compare.md. Waiting on EJ — 6 questions.
- 2026-10-15 EJ on the direction: "i love the idea we have 2 copy and the end merge to one, 1 from me and 1 from AI agent suggestions. yes use cases, yes must define the failes if and the minimum acceptance criterials. use case will win, the requirement should be highlight ... a very secure app but need to be high speed, so we need to know how secure and how fast in the requirements, also this is why we need requirements. 3. should have 4. yes, after accept by human 5. yes. 6. not sure what this means but I got a feeling that, we must always know the purpose of one use case and requirements, not just put just because the use says want some requirements" — written as R13 in requirements-draft.md. Q6 (Dave's blind test) explained, not run. "Highlight" read as: recorded and shown to the user, who decides the revision (main agent's reading, in R13.7).
- 2026-10-15 EJ: "1. Yes accept, 2. Explain the diff between R10 and R12 3. What is W1.1 4. Don't merge first, because need to research this harness health can be converted to a typescript ai plus ai agent hybrid solution, because if only written down rules, sometimes ai agent will skip" — skip criterion accepted as proposed by the main agent (its full text now in requirements-draft.md R11.1). feat/harness-health NOT merged. Research on a TypeScript + agent hybrid proposed, not started.
- 2026-10-15 EJ: "R10 and R12 really seems like saying the same thing, ask sun tzu help me merge them into one" — four_experts.py run --only sun-tzu --question-file expert-question-merge.md --out experts-merge.
- 2026-10-15 EJ (mid-turn): "ok put a todo note for the W1.1 not now, because when this harness solid, we can use this to enhance the whole memory system" — added as item 12 under "TODO next" in runs/20261014-sot-yaml-review/state.md.
- 2026-10-15 experts-merge done: 孫子 on dsh, exit 0; its quotes pass the check (the 4 failures are the four experts not asked). Merged R10+R12 text in experts-merge/answers/sun-tzu.md; not yet written into requirements-draft.md — waiting on EJ.
- 2026-10-15 EJ: "yes, design and execute a workflow to research, implement, review and enhance the effectiveness of the TypeScript + agent hybrid, make sure they integrate into the workflow design skills and algo" — R10+R12 merged into requirements-draft.md as R12.1–R12.6 with 孫子's five questions listed open (main agent read "yes" as covering the merge; the open choices are not filled). New run 20261015-ts-hybrid started.
- 2026-10-15 EJ on 孫子's questions: "q1 Logging level: insight must be both log and raise; q2 Who closes the loop: AGENT research and propose 2 or 3 most effective options; q3 Who can declare a failure: anyone but with reasons and data; q4 Review timing: review for?; q5 Part 6's reach: explain withdrawal more" — R12.2 and R12.3 now MUST (EJ's decision, over the SHOULD default); insight raised in the final report; 2–3 researched fix options, agent proposes only; failure record needs a reason and evidence. q4/q5 explained, still open.
