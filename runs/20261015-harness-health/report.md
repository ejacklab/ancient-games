# Report — harness health in the readiness step

Run `20261015-harness-health`, 2026-10-15. Built on branch `feat/harness-health` in the worktree
`../ancient-games-harness-health` (commits `cb808f1`, `d7a1390`, `d743b10`). **Not merged**: the live skill is unchanged
until EJ says merge.

## What was built

- `readiness.py` now probes `dsh` and `opencode` (both `verified` on this machine).
- New `scripts/harness_health.py`: ten requirement rows, then one line per finding (`present / absent / measured /
  covered / unknown`, with readiness's four statuses), then **Help** — file, what it changes, how to apply, and a
  snippet where the fix is a setting. It reads only, spends no quota, prints no config value except recognised
  mode/event names and counts, and says at the top: *configured is not enforced*.
- Probed in depth: Claude Code (deny rules, sandbox, permission mode, bypass-mode prompt, hooks) and Codex
  (`sandbox_mode`, `approval_policy`). agy, qwen, dsh, opencode: `unknown` — their config formats are not verified.
- One sentence each in method 3.1 and the skill's step 1; `skills/` bundle regenerated.

## On this machine (evidence/harness-health-this-machine.md)

| Requirement | Finding |
|---|---|
| R6 | Claude: no deny rule, sandbox not enabled · Codex: `sandbox_mode` not set · agy/qwen/dsh/opencode unknown |
| R8 | Claude: bypass-mode prompt skipped (`skipDangerousModePermissionPrompt` true, user) · Codex: `approval_policy` not set |
| R10 | Claude hooks present (UserPromptSubmit) |
| R1, R4, R9 | measured (instruction files, memory, session logs) · R2, R3, R5, R7 covered by the method's scripts |

## Checks (who wrote each, and what it does not establish)

| Check | Result | Written by | Does not establish |
|---|---|---|---|
| Full suite | 994 → 1029 passed | repo + main agent (35 new) | that harnesses enforce what is configured |
| Mutation of the first tests | 4 / 4 caught (evidence/mutation-check.txt) | main agent | — |
| New tests vs reviewed versions | round-1 fixes: 12 tests fail on `cb808f1`; round-2 fixes: 5 fail on `d7a1390` | main agent | — |
| Key names | Codex: verified on 0.160.0 (rejects a bad value); Claude: *reported* from 2.1.299 binary strings | main agent | Claude key names are not harness-validated |
| Independent review | Codex gpt-6.1-sol, read-only, 2 rounds (review-round1.md, review-round2.md) | Codex | it could not run the tests (read-only sandbox) |
| Backtest | 0 of 7 recorded traps flagged, as predicted (backtest.md) | main agent, on paper | — |

Review dispositions: round 1 — 9 defects, all fixed. Round 2 — 6 defects: 5 fixed in `d743b10` (not re-reviewed by
Codex; each has a test that fails on the round-2 script); 1 kept as stated: `covered` proves the gate script exists,
not that it works (docstring says so). Deny-rule semantics beyond the `mcp__…(` case are not modelled.

## Deviations from the method, stated

- Built by the main agent, not split through `workload.py` with opencode priority — one module; reviewer of a
  different kind (Codex) instead.
- Status on a version change downgrades to `reported`, where 孫子 and 老子 asked for `unknown`.
- The "Found → effect on the design" table is proposed in `workflow-design.md` (n=0), not written into method 3.1 (Dave's defer).

## Questions for EJ (from the experts, merged — experts/compare.md)

1. Block or inform: should a finding stop dispatch? (built: inform only)
2. An opt-in `--canary` that spends a little quota — the only way to see the five behaviour traps at readiness.
3. Is "no deny rule" a finding at all? Requirement 6 says "hard policies", not a deny list. (built: yes)
4. A trap catalogue (Dave): each recorded harness trap with its fix as the help — the backtest says this is where the
   failures this project has actually had would be caught.
5. Drift against the previous health output — wanted, and where kept?
6. Merge `feat/harness-health` into master and push?
