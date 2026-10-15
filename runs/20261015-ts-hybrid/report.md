# Report — TypeScript + agent hybrid for harness health (run 20261015-ts-hybrid)

Branch `feat/ts-hybrid` in worktree `../ancient-games-ts-hybrid`, 27 commits on top of `feat/harness-health`
(`d743b10`). **Not merged, hooks not installed** — both are EJ's.

## What was built

`.claude/skills/workflow-design/guard/` — bun, TypeScript, no npm dependencies; it travels with the skill and the
`skills/` bundle. **Code does what needs no judgment; the agent does the rest; the code checks the agent did it.**

| Module | Does | Requirement |
|---|---|---|
| traps (M1) | lints a command before an engine call against `data/traps.yaml` (7 recorded traps; only `approved` act), reads the shell as the shell does (segments, heredocs, quotes, wrappers like `timeout`/`env`/`runlog.py --`, `--help`); after the call: missing/empty output, silent-failure text, failing exit → fail | R12.1 |
| journal (M2) | `.harness-guard/journal.jsonl`; a failure needs a reason and evidence that exists, whoever logs it | R12.2 |
| insight (M3) | an insight answers each failure: whys 3–6, a changeable source, root cause, 2–3 fix options with evidence | R12.3 |
| register (M4) | use cases (user list + AI suggestions with a decision), fails-if, minimum acceptance; requirements with a purpose; conflicts shown; coverage over frozen units, 80% target reported, safety never skipped | R11.1, R13 |
| hooks / plugin / install / doctor / CLI (M5) | one handler for the Claude Code hook protocol (Codex, Qwen and the dsh bridge use the same field names — *reported*): PreToolUse denies a trap; PostToolUse logs a failed engine call; Stop blocks while a failure has no insight or the final message does not name it; SessionStart raises other sessions' open failures; an opencode plugin (lint only); `install --print` prints settings, never writes; `doctor` reports where it is installed | R12.1–R12.3 |

Also: a hole in `dispatch.py` fixed (a result whose own header says `status: fail` or `partial` was marked done when
the node had no check) — reproducer test failed first.

Integration: `SKILL.md` steps 1, 7 and 8; method 3.1 (one sentence) and 3.8 **item 13** (new, appended); `skills/`
re-exported. Suites: Python **1031 passed** (1029 + 2), guard **796/796**, `tools/` 64/64, typecheck clean.

## How it was built (method, and where it deviated)

Research (two read-only subagents) → design + 10 unclear spots → four experts on the spots → prediction committed
before code → five modules, tests first, code and tests from different engines by `workload.py` (opencode MiniMax
wrote all code; Codex wrote most tests; M3's first tests were opencode's, so Codex added the gaps) → COO mutants per
module → independent review → measure, enhance, re-measure → integrate. **Deviations, stated:** the engine split was
swapped for M4/M5 mid-run to unblock opencode (workload's own check passed: still 4 of 5 modules independently
tested); Codex hit its usage limit, so the review (and round-3 tests) went to Claude subagents — a different kind from
both builders; `m5-code` stopped without a result file and was accepted by the COO on the suite.

## Did it work? (each against a prediction written before the run)

| Measure | Rules only (control) | Hybrid, first build | Hybrid, after one enhance round | Prediction |
|---|---|---|---|---|
| E1 — the 7 recorded traps | 0 / 7 | 4 / 7 | **5 / 7** (trap 3 — a path inside a quoted prompt — fixed) | 5 / 7 — **held** after the round; traps 5 (plan mode) and 7 (inside the harness) out of reach |
| E2 — 3,677 past commands | — | 37 denies, **31 false** | **14 real denies, 0 false**; 3 missed calls (`do` loops) now recognised | false denies > 0 before tuning — held |
| E3 — 12 planted rule violations | 0 / 12 | 12 / 12 | 12 / 12 | 12 / 12 — held (circular by design) |
| E4 — live haiku, rules in the brief (n=3/arm) | trap 3/3, logged 3/3, valid insight 2/3, raised 3/3 | 3/3 all four, 2.4× slower | — | control ≤ 1/3 — **wrong** |
| E4 — rules in the folder, not named | 3/3 all four (agents found RULES.md themselves) | 3/3, but 203 / 72 / **839** s | **3/3, 35 / 50 / 49 s**, ≤ 1 block, no `find /` | control 0/3 — **wrong**; round-3 speed — held |

**My reading:** the guard catches what the record shows (5 of 7 recorded traps, 6 earlier real `codex exec` stdin traps
and 8 parallel `opencode` starts in the project's own history, with no false blocks), and the review's 21 findings are
fixed. **The live test did not show agents skipping the rules**: with the rules anywhere in the working folder, haiku
found and followed them on a short task. The hooks' measured value there is catching a format slip (one in six runs)
— at no extra time after the fixes. The case EJ described — rules out of reach in a long session — is **not
measured**.

## Dogfooding

The COO logged its own four failures with the guard's `fail` command (one was refused for lacking evidence — R12.2
working), and wrote the insight `runs/20261015-ts-hybrid/insight.md` (on the branch); the guard's gate reports no open
failures. Its fix options are proposals for EJ: a result-file check for hand-run nodes; never edit a running script;
briefs write `status: partial` first; a quota check per engine at readiness.

## Decisions for EJ

1. **Merge** `feat/ts-hybrid` (it carries `feat/harness-health` too) into master and push? Note: this run's main-repo
   folder `runs/20261015-ts-hybrid/` is untracked and shares some file names with the branch's copy
   (`prediction.md`); I'd fold the main folder into the branch before merging.
2. **Install the hooks** for Claude Code? `bun .claude/skills/workflow-design/guard/src/cli.ts install --print claude-code`
   prints the settings; it is your config, so you add it (or tell me to print it for Codex / Qwen / opencode).
3. **Provisional choices I made**, each in `experts-spots/compare.md` / `state.md`: journal keyed by session; Stop
   blocks every time while open (the harness's cap is the loop guard); the package lives in the skill; `Source:` passes
   on its first word.
4. **The long-session test** — the one that would show whether hooks beat written rules where it matters. Worth a run?
   (A paid Claude call per session; a design for it is the next step if you want it.)
5. **The insight's fix options** for the COO's four failures — choose any to apply.
