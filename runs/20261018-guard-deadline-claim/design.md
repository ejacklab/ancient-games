# Workflow design — the guard claims another run's deadline (research, fix, test, evaluate)

Status: designed, not run. It runs on the owner's go, with a time box the owner gives.

## 1. The challenge (method 3.0)
- **Objective.** A session's clock shows only deadlines that session started: no session ever claims, or is told
  "time is up" by, a deadline another session started.
- **In scope.** The claim (`claimDeadlines`, `src/deadline.ts:65`), the claim call (`withTime`, `src/hooks.ts:851`),
  SPEC T1, their tests, and what to do with deadlines already claimed wrongly.
- **Out of scope.** The rest of the clock (T2–T5, Round 20's DL rules), other guard rounds.
- **Category.** debugging + test cases gen + code review (fix a defect, default-first, `docs/TASK_TYPES.md`).
- **Six whys** (each checked; file and line, or command and output, in `facts.md`):
  1. Why was this session told "time is up" after its own deadline ended? It owns D-593045da, the code-map run's
     360-min deadline (`.harness-guard/deadlines/D-593045da.json`: run `runs/20261014-code-map-build`, session
     `1159cce6…`).
  2. Why does it own another run's deadline? Its `deadline start` (D-17979aae, 18:18:45Z) claimed every unclaimed
     deadline file, and D-593045da (18:18:18Z) was still unclaimed (SPEC T1: "claims every unclaimed deadline file for
     its session").
  3. Why was D-593045da unclaimed 27 s after its start? Its own session (16098663…) started it with
     `G=.claude/skills/workflow-design/guard/src/cli.ts; … bun $G deadline start …` (that session's transcript). The
     claim runs only when the command text matches `/\/src\/cli\.ts\s+deadline\s+start\b/` (`src/hooks.ts:855`), and
     `bun $G deadline start` does not. Neither does `bun src/cli.ts deadline start`, the form run from the guard folder
     (checked: the regex returns false for both).
  4. Why is the call recognised by its text? Round 10 review finding 2 made only "a call that ran this guard's
     `deadline start` and succeeded" claim; the command text was the signal chosen.
  5. Why can one session's claim take another's file? "Every unclaimed" assumes the only unclaimed file is the one just
     started, which holds only when every start is claimed at once.
  6. The source to change: the claim's rule (SPEC T1 and its code), not the agents' command style.

## 2. Readiness (method 3.1)
- Tools (run before the workflow starts): `bun test` and `tsgo` in the guard (1560 pass after `d608608`); opencode,
  Codex (`codex --search exec`), Claude subagents; the six experts (`six-experts` skill). Engine availability is
  checked at the start of each step. Another session uses opencode often: one opencode at a time; Codex is the
  fallback for code.
- The memory notes and lessons for the guard, fed to each brief by `lessons for --agent <engine> --kinds code-edit,test`.
- Blueprint: the guard's contract is `SPEC.md`; a Round 21 section is written before any code.
- **The clock for this run.** It must not hit its own defect. The run's deadline is started with the plain
  `bun .claude/skills/workflow-design/guard/src/cli.ts deadline start …` form, and every step reads its clock with
  `deadline status --run runs/20261018-guard-deadline-claim` (Round 20 DL2), never the session's choice.

## 3. The algorithm (method 3.2), each step with its check
1. **Research the claim, inside the repo** (explorer, Claude). Every path that writes `session` into a deadline file;
   every `deadline start` call in this machine's Claude Code transcripts with its session, its command form and
   whether its own session claimed it. Check: a table with one row per start; the count of starts claimed by the
   wrong session or by none (the defect's rate, measured, not guessed).
2. **Research the harness** (researcher, Claude; web and docs). What a PostToolUse payload for Bash carries
   (`tool_response` stdout? the session id?), whether Bash's environment holds the session id, and how subagents' and
   workflow agents' hooks report their session. Check: each answer cites a doc page or is shown by a probe hook
   payload saved in the run folder; an answer with neither is *not established*.
3. **The fix options, to the experts** (`experts-decide`, all six). The options, from research:
   - (a) **Claim by the id the call printed.** PostToolUse reads the start call's output for `D-xxxxxxxx: N min` and
     claims that one id only, whatever the command's text.
   - (b) **The session is written at start.** The CLI writes `session` itself, from an id the harness gives the
     command (only if step 2 finds one).
   - (c) **Claim only a deadline started during the call.** Its `start` lies between the call's start and end.
   Check: the compare's majority and dissent are written; the main agent picks (provisional, R12.3) and says why.
4. **SPEC Round 21** (main agent): the chosen rule, its Fails-if, and what happens to deadlines already claimed
   wrongly (§5, U3). Check: `requirement-check`'s eight pass, or each failure is named.
5. **Tests, red first** (Claude): the incident replayed as a fixture (the two real deadline files and the three real
   start commands: `bun $G deadline start`, `bun src/cli.ts deadline start`, the full path form); two sessions starting
   deadlines 27 s apart; a start whose claim was missed; a workflow agent's call. Check: `expect-fail` records each red
   run; every other guard test passes.
6. **Code** (opencode; Codex if opencode is busy past 30 min). Check: the result file, and the diff touches only the
   files the brief names.
7. **Verify** (Sonnet, a separate step): guard `bun test`, `tsgo`, the test files' hashes unchanged. Check: all hold.
8. **Review** (Codex, read-only) and **judge** (Claude reproduces each finding). Check: each finding reproduced or
   dropped with a reason.
9. **Repair loop**: reproduced findings → tests → code → verify, until a review round reproduces none or the round
   limit is reached (the owner's number; 2 proposed). Check: the loop's stop is the judge's empty list, never a
   worker's report.
10. **Evaluate** (Claude, a step that wrote none of the code), three measures against the old code:
    - **Replay:** the real deadline files and start commands from step 1, run through the old and the new claim in a
      scratch copy of `.harness-guard/`: old — session 1159cce6 claims D-593045da; new — it does not, and
      16098663 claims its own.
    - **Rate:** step 1's table re-scored with the new rule: starts claimed by the wrong session or by none, before
      against after.
    - **Planted repeat** (R12.3): the old claim line planted back into the new code; at least one test fails on it.
    Check: the three results, each with its command and output in `evaluate/`.
11. **Report** (main agent): the path (steps, engines, checks, measures) and the provisional decisions.

**Runnable form.** `workflow.js` in this folder runs in two phases, because step 4 is the main agent's:
`{phase: 1}` (default) runs steps 1–3 and stops; the main agent writes SPEC Round 21, `briefs/r21-code.md` and
`briefs/review.md`; `{phase: 2, rounds: N}` runs steps 5–10. Before phase 1: `deadline start --minutes <yours> --run
runs/20261018-guard-deadline-claim` with the full path (no deadline file is unclaimed now, checked 09:22, so the
start claims only its own).

## 4. Unclear spots (method 3.3)
| # | Kind | What | Blocks | Provisional |
|---|---|---|---|---|
| U1 | decision | Which fix: (a), (b) or (c) | 4–10 | the experts advise in step 3; my lean before research is (a): it needs nothing from the harness |
| U2 | information | Does the harness give a Bash command its session id, and does PostToolUse carry stdout? | option (b), and (a)'s reading | step 2 answers it |
| U3 | decision | The deadline files already claimed by the wrong session (D-593045da today) | 4 | leave past files as they are; the fix acts on new claims only. Rewriting another session's deadline file waits for your yes |
| U4 | decision | "Evaluate" means step 10's three measures, not the requirements evaluator: the guard's contract is `SPEC.md`, which the evaluator's parser does not read | 10 | as written |
| U5 | decision | The time box and the repair rounds | the run | yours to give; proposed: 2 hours, 2 repair rounds |

## 5. The graph (method 3.6–3.7)
Sequential, state-file driven (`state.md`): 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → (9 ↺ ≤ rounds) → 10 → 11.
Steps 1 and 2 are the one parallel pair: they read different sources, write different files, and neither needs the
other's result. Edges: 1–2's `facts.md` is 3's question; 3's compare is 4's input; 4's SPEC section is the brief of 5
and 6; 5's test hashes are 7's check; 8's judged findings are 9's input; 1's table is 10's rate.

## 6. Every node's five things
| Node | Engine (model, effort) | Context given / withheld | Returns | Evidence |
|---|---|---|---|---|
| 1 research-repo | Claude Opus, high | the defect, file paths / no fix idea | table of starts, claim paths | `research/starts.md` |
| 2 research-harness | Claude researcher (Opus), high | the three questions / — | answers with sources | `research/harness.md`, `research/probe-payload.json` |
| 3 experts | six experts (skill defaults) | facts.md, options a–c / each other's answers | compare.md | `fix-q/compare.md` |
| 4 spec | main agent | compare.md | SPEC Round 21 | SPEC.md diff |
| 5 tests | Claude Opus, high | SPEC Round 21, existing round10/round20 tests / the code to come | test files, red runs | `nodes/r21-*.red.txt` |
| 6 code | opencode MiniMax-M3.1-Flash-Preview, high (Codex gpt-6.1-sol fallback) | brief + SPEC / the tests' reasoning | result file | `nodes/r21-code.result.md` |
| 7 verify | Claude Sonnet 5.5 | commands only / the worker's report | pass, failing | `nodes/verify-*.txt` |
| 8 review + judge | Codex gpt-6.1-sol high, read-only; Claude judge | diff + SPEC / the tests | findings, verdicts | `nodes/review-*.md` |
| 10 evaluate | Claude Opus, high | old and new code, step 1's data / the worker's reasoning | three measures | `evaluate/` |
Each brief carries a `## Lessons` section and asks for its result file first as `status: partial`. Every prompt
starts with `cd "$(git rev-parse --show-toplevel)"` and reads the clock by `--run`.

## 7. Parent path (R12.7)
Parent: guard Round 20 in run 20261018-finish-everything (Claude tests red first → opencode code → Sonnet verify →
Sonnet review → fix → Codex review → fix). Changed: research and the experts come before the spec, and an evaluation
step measures the fix on the real incident. Measure: reproduced review findings after the first fix — the parent's
value was 4 (Sonnet) + 2 (Codex) in its guard parts.

## 8. Predictability, debuggability, quality control (method §5)
- Predictable: fixed order, one round limit, each step's stop is a check (§3).
- Debuggable: one progress file per step, every red run and result file kept in the run folder, `state.md` after each
  step.
- Quality: tests from an engine that writes no code; verify and evaluate by steps that wrote none of it; a planted
  repeat must fail the tests.

## 9. Cost (estimate, not measured)
About 1.0–1.5M tokens: research 0.15M, experts 0.6M, tests and code 0.2M, verify 0.05M, review and judge 0.15M per
round, evaluate 0.1M. About 1.5–2.5 hours, most of it waiting on opencode and the experts.
