# State — 20261015-ts-hybrid

Rules: one writer at a time. Read this file before your step; update it after. It holds progress and results only —
never reasoning; put notes in your own output file. Never delete a log line.

## Challenge (verbatim)

> yes, design and execute a workflow to research, implement, review and enhance the effectiveness of the TypeScript +
> agent hybrid, make sure they integrate into the workflow design skills and algo

(EJ, 2026-10-15.) Restatement: `challenge.md`. Requirements the hybrid serves: R11–R13 in
`runs/20261015-harness-health/requirements-draft.md`.

## Baseline

- `git status --short` before the run: `pre-run-git-status.txt`.
- `readiness.py` (feat/harness-health version) exit 0, 22 verified: `readiness.md`. `harness_health.py`:
  `harness-health-before.md`.
- `tools/` TypeScript suite (why-chain-hook, bun 1.4.3): 64 pass, 0 fail.
- Python suite on `feat/harness-health` (`d743b10`): 1029 passed (run 20261015-harness-health).
- `Bun.YAML.parse` exists in bun 1.4.3 (checked).

## Steps

| # | Step | Status | Output file |
|---|---|---|---|
| 1 | Research: hook points per harness; code-vs-text inventory | done | research/hook-points.md, research/code-vs-text.md |
| 2 | Design: algorithm, unclear spots, experts, size, plan | done | workflow-design.md |
| 3 | Prediction and effectiveness protocol, written before the build | done | prediction.md |
| 4 | Build in a worktree: modules, tests crossed between engines, gates | done | nodes/, evidence/ |
| 5 | Independent review | done | review-*.md |
| 6 | Effectiveness: measure, enhance, re-measure | done | effectiveness.md |
| 7 | Integration into workflow-design (skill, method, readiness) | done | evidence/ |
| 8 | Report to EJ; merge only on EJ's word | doing | report.md |

## Unclear spots

| Id | What is unclear | Kind | Blocks | Depends on | Provisional assumption |
|---|---|---|---|---|---|
| U1 | Which session or run a failure and its insight belong to, so the Stop hook knows what to check | decision | M2, M3, M5 | — | a journal per harness session (`session_id`) under a gitignored `.harness-guard/`; the insight file lives in the run folder and is registered against the session |
| U2 | Loop guard on Stop: block until the insight exists, or block once | decision | M5 | U1 | block once; on `stop_hook_active` allow the stop and write an `insight_skipped` record that `doctor` reports |
| U3 | How PostToolUse recognises an engine call and finds its output | unknown | M1, M5 | — | a pattern list per engine (codex exec, opencode run, agy, dsh headless, qwen, claude -p, four_experts.py, dispatch.py) and the output from `-o FILE` or `> FILE`; otherwise stdout |
| U4 | Port `harness_health.py` (460 lines, 35 tests) to TypeScript, or keep it and add `doctor` beside it | decision | M6 | — | keep the Python check; `doctor` adds guard-installed status and calls it — one copy of each probe |
| U5 | Installing a hook is editing harness config, which the agent never does | decision | M5, step 6 | — | `install --print` only; the effectiveness test loads hooks with `claude -p --settings <run file>` in a sandbox, which edits no config |
| U6 | The register's format | decision | M4 | — | YAML (`Bun.YAML.parse`, checked present in bun 1.4.3) |
| U7 | Where the trap catalogue lives and who adds to it | decision | M1 | — | a data file in the package, generic (no project paths); an insight's trap-type fix adds an entry |
| U8 | Fix the dispatcher hole now or report it | decision | — | — | report; fix only if one line plus a test, as its own commit |
| U9 | Effectiveness arms, model and n | decision | step 3, 6 | U5 | arm A: written rules only; arm B: rules + hooks; same model; small n per arm; plus a quota-free replay of the 7 recorded traps and planted R11–R13 violations |
| U10 | Which harness adapters now | decision | M5 | — | the Claude-protocol handler (Claude Code, Codex, Qwen, dsh bridge) and the opencode plugin; agy later (exit-code meaning unknown) |

## Log

- 2026-10-15 step 1 started: two read-only research subagents (hook points per harness; code-vs-text inventory).
- 2026-10-15 step 1 done: research/hook-points.md (all six harnesses have a blocking point a bun command can serve; verified from installed versions, nothing fired); research/code-vs-text.md (no R11–R13 rule runs on every task; dispatcher used by 10/97 runs, none since 2026-10-10; dispatch.py marks a no-check node with `status: fail` done).
- 2026-10-15 step 2: workflow-design.md written; U1–U10 listed; experts (linus, sun-tzu, lao-tzu, dave) asked on the unclear spots.
- 2026-10-15 N1 (Dave) verified: claude -p --settings <file> --setting-sources project loads and fires PreToolUse, PostToolUse and Stop hooks from the file; no config edited (env -u ANTHROPIC_API_KEY for the subscription login; claude-haiku-5-5; evidence/n1/: field names and value types only). Bash PostToolUse tool_response has stdout, stderr, interrupted, isImage, noOutputExpected — no exit code.
- 2026-10-15 m1-tests attempt 1 started: codex gpt-6.1-sol high, workspace-write, in ../ancient-games-ts-hybrid (brief runs/20261015-ts-hybrid/briefs/m1-tests-1.md on feat/ts-hybrid).
- 2026-10-15 step 2 done: experts-spots/compare.md (decisions per spot, the COO's, provisional). U2 changed from the provisional "block once" to "block every time while open" — EJ made R12.3 MUST.
- 2026-10-15 step 3 done: prediction.md, committed `5d0117d` on feat/ts-hybrid before any guard code. E2 corpus counted: 65 sessions, 3,677 Bash calls, 284 engine-like (raw commands in local scratch only).
- 2026-10-15 step 4 started: worktree ../ancient-games-ts-hybrid, branch feat/ts-hybrid from feat/harness-health d743b10. COO wrote SPEC.md, src/types.ts, data/*.yaml (`04a8ef9`). Engine split by workload.py (build-plan.json): m1 code opencode/tests codex · m2 same · m3 opencode/opencode (self-tested) · m4 code codex/tests opencode · m5 code codex/tests opencode. Order per module: tests first, then code.
- 2026-10-15 m1-tests attempt 1 did not run: runlog.py usage error (--runs-root must precede exec); the wrapper's last command hid exit 2 — the COO's own R12.1 slip, now caught by run_node.sh (checks the result file). Re-run as attempt 1.
- 2026-10-15 U8: dispatcher hole fixed, `27c25e3` — reproducer test (fail and partial, no check) failed 2/2 before the fix; test_dispatch*.py 45 passed after.
- 2026-10-15 m1-tests done (codex gpt-6.1-sol, 4 min, exit 0): test/traps.test.ts 54 tests, loads and fails only on the missing module; 3 CONTRADICTS resolved in SPEC by the COO (node:os; background from the command; wrapper outputFile is its folder, status file is the check). Tests frozen at `f4bee07`. m1-code attempt 1 started (opencode).
- 2026-10-15 m2-tests attempt 1 started (codex) beside m1-code (opencode): independent files (test/journal.test.ts vs src/traps.ts), different engines, neither commits — the parallel conditions of method 3.7 hold.
- 2026-10-15 m1-code done (opencode, 2 min, exit 0): src/traps.ts; COO re-ran: 112 pass, tsgo clean, tests unchanged (sha256 73fb47a9…), only src/traps.ts touched; committed `786b4b3`. COO mutants (evidence/m1-mutants.txt): 3 of 5 killed; survivors: M1e proposed *result* traps acting (a real test gap — repair to the test writer), M1c a weak mutant (exact-match set, no meaning).
- 2026-10-15 m3-tests attempt 1 started (opencode) beside m2-tests (codex): disjoint files.
- 2026-10-15 E2 round 0 (effectiveness/e2-round0.md): 37 denies over 3,677 past commands, 31 false (6 real codex-stdin); 12 crude misses (2 real dispatch.py runs, not in scope). M1 round 2: SPEC Segments + anchored catalogue, `a880eb9`; m1-tests attempt 2 (codex) started.
- 2026-10-15 m2-tests done (codex, exit 0): test/journal.test.ts loads, fails only on the missing module; CONTRADICTS (raw content in agent-written records) resolved in SPEC; frozen `87cff91`. m2-code waits for m3-tests: two opencode runs at once is a catalogued trap.
- 2026-10-15 m3-tests done (opencode, exit 0): 72 tests; 4 CONTRADICTS — 3 resolved in SPEC (runs/** depth, unknown option kind fails, root trusted), 1 was the COO's brief wrongly saying M2 was built (it ran in parallel). Note: opencode wrote a throwaway reference implementation in /tmp to mutate its own tests (7 mutants, 6 caught) — outside the repository, against the brief's limit; nothing kept. Frozen `266dc6c`. m2-code attempt 1 started (opencode).
- 2026-10-15 m1-tests attempt 2 done (codex): +320 lines of segment tests; one changed test would deny 'printf task | codex exec -' (a false deny) — SPEC gains Segment.piped and unless_piped (`ef22d4d`); m1-tests attempt 3 (codex) started for that one test.
- 2026-10-15 m1-tests attempt 3 done (codex): piped test inverted, piped/unless_piped tests added; M1 tests frozen `f1b6227`. m1-code attempt 2 queued behind m2-code (opencode, one at a time).
- 2026-10-15 m2-code attempt 1 done (opencode): journal.ts, 89/90 journal tests; the 1 failure is a test bug the COO reproduced (an empty-array test.each element makes bun treat the parameter as a done callback; not a bun bug) — m2-tests attempt 2 (codex) to fix it; SPEC: evidence/appendRecord drop raw keys. m1-code attempt 2 (opencode, segments) started in parallel.
- 2026-10-15 M2 done: m2-tests attempt 2 (codex) wrapped the table — 90/90; COO mutants 4/4 killed (evidence/m2-mutants.txt); committed `a4d8ef0`. Next on opencode after m1-code-2: m3-code, then m4-tests, m5-tests.
- 2026-10-15 engine swap: m4/m5 tests now codex, code opencode (opencode was the bottleneck, codex idle). workload.check() on the swapped plan: no problems (opencode 6/10, 4/5 modules independently tested — unchanged). m4-tests and m5-tests (codex) started, one after the other.
- 2026-10-15 m4/m5-tests did not start: the COO generated their briefs from the wrong folder; run_node.sh refused ('no brief') — moved and re-started.
- 2026-10-15 M1 round 2 done: traps.ts on segments, 189/189; committed `71082d1`. E2 round 1 (effectiveness/e2-round1.md): 14 denies, 14 real, 0 false; 3 real recognition misses (a segment starting with the shell keyword 'do') carried to the enhance round.
- 2026-10-15 m3-code attempt 1 started (opencode).
- 2026-10-15 m3-code done (opencode): insight.ts 72/72; its CONTRADICTS misread a Fails-if line (no change). COO mutants (evidence/m3-mutants.txt): 3 of 5 killed; survivors: an unknown option kind such as [policy] accepted (real gap — SPEC says it fails), an extra source word accepted (weak). Committed `17c9435`. The M3 test gap goes to codex — a different engine from M3's writer — after m4/m5 tests.
- 2026-10-15 m4-tests done (codex, no CONTRADICTS), frozen `c226a83`; m4-code attempt 1 started (opencode).
- 2026-10-15 M4 done: register.ts 92/92, COO mutants 5/5 killed (evidence/m4-mutants.txt), `363fc68`. m5-tests attempt 1 done (codex): hooks + CLI tests; 2 CONTRADICTS (doctor options, plugin signature) resolved in SPEC, `3b0e72d`. Started in parallel: m5-tests attempt 2 (codex: doctor + plugin tests) and m5-code attempt 1 (opencode).
- 2026-10-15 decision (COO, provisional, for EJ at the report): at integration the package moves from tools/harness-guard/ into .claude/skills/workflow-design/guard/ — the skill is linked into other projects and exported as a bundle, so the guard must travel with it; done after M5 and the review, not while nodes write.
- 2026-10-15 m5-tests attempt 2 done (codex): doctor + plugin tests, no CONTRADICTS; committed `f5696f2`. m3-gap (codex) started: tests for the two surviving M3 mutants.
- 2026-10-15 m3-gap done (codex): +13 tests, 85/85; the two surviving M3 mutants now killed (evidence/m3-mutants.txt); `3564c5a`.
- 2026-10-15 m5-code attempt 1 (opencode, 8.5 min, exit 0): wrote hooks, install, plugin, doctor, cli — then stopped with **no result file** (stdout ends 'Now the CLI:'); not caught by run_node.sh because the COO edited that script while it ran (bash error after the call). Full suite 633/634, tsgo 0 — the 1 fail is a test bug (test.each empty array). Logged with the guard's own CLI: F-cf7d58f7, F-08cf4cc3, F-f44538b2 (one record was refused for lacking evidence — R12.2 working). m5-tests attempt 3 (codex) for the test bug.
- 2026-10-15 m5-tests attempt 3 (codex): wrapped the hooks table, then **hit its usage limit** (until 7:24 PM local) — exit 1, no result file; runner reported result=MISSING (caught this time). Logged F-3b8bdcec. Full suite 634/634, tsgo 0; M5 committed `59a81ff` (m5-code accepted by the COO without a result file, on the suite). Codex unavailable → the review goes to a Claude subagent (a different kind from both builders: opencode/MiniMax wrote the code, Codex the tests).
- 2026-10-15 step 6 started. E1 round 1: 4 of 7 (predicted 5; trap 3 missed — a path inside a quoted prompt). E3 round 1: 12 of 12 (as predicted; circular). E4 (6 live runs, claude-haiku-5-5, A1–A3 rules only, B1–B3 rules + hooks via --settings) started in parallel.
- 2026-10-15 E4 round 1 (effectiveness/e4-round1.md): A 3/3 trap avoided, 3/3 logged, 2/3 valid insight, 3/3 raised; B 3/3 on all four, 0 denies, 2–4 Stop blocks per run, 2.4× slower; prediction for A was wrong (agents followed written rules on a short task). Duplicate records in B (hook + agent). Setup fault: RULES.md named a location the guard does not read.
- 2026-10-15 step 5 done: review by a Claude subagent (claude-opus-5-5; Codex at its usage limit) — 1 high, 7 medium, 12 low, 1 suspected, each with an input it ran (nodes/review-1.result.md). Round 3 spec (C1–C23) from the review + E1/E2/E4, data regexes fixed, `2a215a9`. Note: E4 round 2 was running while data/traps.yaml changed (only the codex-stdin unless and agy-502 regexes; neither is exercised by that task).
- 2026-10-15 E4 round 2 (effectiveness/e4-round2.md): arm A again followed the rules (found RULES.md by listing the folder) — prediction wrong; arm B 3/3 but slow (203/72/839 s vs 59/39/41); B3 killed at 900 s after two 120 s stalls, cause not reproduced. Round-3 tests (Claude subagent): test/round3.test.ts 162 tests + 4 changed existing rows; 685/796 pass before the code change, 111 fail as expected.
- 2026-10-15 round-3 tests committed `73f3ec5`; SPEC C24 added. r3-code attempt 1 (opencode) started.
- 2026-10-15 r3-code attempt 1 done (opencode, status partial only because its own process tripped the C17 tests' precondition): COO re-run 796/796, tsgo 0; mutants 5/6 killed + 1 equivalent (evidence/r3-mutants.txt); committed `2c1af3d`.
- 2026-10-15 re-measure after round 3: E1 5/7 (prediction held; round 1 was 4), E2 14 real denies / 0 false, recognition misses 3 → 0 real, E3 12/12.
- 2026-10-15 E4 round 3 (arm B after round-3 code): 3/3 on all four, blocks 1/0/1, records 1/2/2, 35/50/49 s (round 2 B: 203/72/839) — prediction held; the hooks no longer cost time on this task. Enhance loop stops here (round 2 of 2 would change no count measured).
- 2026-10-15 step 7 done: package moved to .claude/skills/workflow-design/guard/; SKILL.md steps 1/7/8, method 3.1 and 3.8 item 13; export skips node_modules; skills/ re-exported. Suites: Python 1031 passed (1029 + 2 dispatch tests), guard 796/796, tools/ 64/64. COO insight (runs/20261015-ts-hybrid/insight.md on the branch) answers its 4 logged failures — the guard's gate says no open failures. Build record committed on feat/ts-hybrid. Step 8: report.md.
- 2026-10-15 step 8: report.md written; waiting on EJ — merge, install, provisional choices, the long-session test, insight options.
