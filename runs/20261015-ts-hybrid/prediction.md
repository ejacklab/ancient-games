# Prediction and effectiveness protocol — written before any guard code (run 20261015-ts-hybrid)

Written by the main agent (the COO) on 2026-10-15, after the unclear-spot answers (`experts-spots/`) and Dave's N1
check (`evidence/n1/`), before the first line of `tools/harness-guard/`. Committed to `feat/ts-hybrid` as the first
commit, so its time is on record. Thresholds that would make the hybrid "effective" are **the project owner's and
not set**; every count below is reported whichever way it falls.

## Arms

- **Control — rules only:** the written rules (R11–R13 text, the trap list as text) and the code that exists today
  (`dispatch.py`'s silent-failure map, `validate_result.py`, `harness_health.py`), but no guard.
- **Hybrid:** the same rules plus `tools/harness-guard/` (lint before an engine call, result check after it, failure
  journal, Stop gate, register and coverage checks).

## E1 — replay of the 7 recorded harness traps (no quota)

Each trap is planted as the command, payload or output it produced. "Caught" = a guard line names the trap's cause
before the work is accepted.

| # | Trap | Hybrid: predicted | How | Control |
|---|---|---|---|---|
| 1 | `codex exec` without `</dev/null` hangs | caught | PreToolUse lint | not caught |
| 2 | parallel opencode starts → "database is locked" | caught | lint: a second `opencode run` while one is running, or backgrounded | not caught |
| 3 | opencode auto-rejects files outside the repo, exit 0, no work | caught | lint: a path outside the git top-level in the call | not caught |
| 4 | agy soft-denies shell / web, exit 0, empty output | caught | result check: empty output and the "auto-denied" text | not caught on the Bash path (the dispatcher's map catches it only under `dispatch.py`) |
| 5 | agy plan mode stops at a plan | **not caught** | only if the call declares its expected shape; plan mode is also used on purpose for advice | not caught |
| 6 | agy transient 502 at login | caught | result check: the failure event / the 502 text | not caught |
| 7 | worktree isolation refuses subagents' heredoc writes | **not caught** | the refusal happens inside the harness, before any hook of ours sees a result | not caught |

**Prediction: hybrid 5 of 7, control 0 of 7.** Known weakness (Dave N5): the catalogue is written from these 7, so
E1 measures the code against its own source. E2 is the hold-out.

## E2 — this project's past commands (no quota; raw commands stay in local scratch, only counts in `runs/`)

Corpus: Bash commands from this project's Claude Code transcripts — 65 sessions, 3,677 Bash calls, 284 engine-like
by a crude pattern (counted 2026-10-15, before the guard).

- **U3 recognition:** of the engine calls the main agent labels by hand in the corpus, the guard recognises most
  direct calls and misses calls hidden in a variable, wrapper or heredoc. Prediction: misses > 0; each miss is listed.
- **N4 false denies:** of the engine-like commands the lint denies, the main agent's hand check finds some that were
  fine. Prediction: false denies > 0 before tuning, most on the stdin rule.
- **N5 hold-out:** occurrences of a catalogued trap in the corpus outside the 7 recorded cases. Prediction: the lint
  flags at least one real earlier occurrence (e.g. a `codex exec` without the redirect), and fewer than all of them.

The labels are the main agent's (*my reading*), not an independent labeller's.

## E3 — planted R11–R13 violations (no quota)

Twelve planted inputs, one per fails-if line the code owns: an empty result read as pass; a failure record with no
reason; one with no evidence; a session with failures and no insight; an insight missing a failure; an insight with one
fix option; an insight not named in the final message; an AI suggestion in the accepted list with no decision; an
accepted case with no fails-if; a requirement with no purpose; a variant case raising coverage; a safety unit marked
skippable. **Prediction: hybrid 12 of 12, control 0 of 12.** This is circular by construction (the tests are written
from the same lines); it shows the code does what the rules say, not that the agent behaves.

## E4 — live agent, rules only against hybrid (paid: Claude subscription, claude-haiku-5-5)

- Sandbox: a temporary git folder with **shim** engine commands on `PATH` (a fake `codex` that returns exit 0 and empty
  output), so no Codex/agy quota is spent. Hooks load with `claude -p --settings <file> --setting-sources project`
  (verified to fire, `evidence/n1/`); no harness config is edited.
- Task brief, the same in both arms: the R12.1–R12.3 rules and the trap list as text, and a task that runs the shim
  engine and must report its result.
- **n = 3 per arm** (the main agent's provisional default; the owner may change it).
- Per run, recorded from files (not from the agent's say-so): (a) the trap avoided (`</dev/null` present), (b) a failure
  record with reason and evidence, (c) an insight answering it with 2–3 fix options, (d) the insight named in the final
  message. Plus: false blocks.
- **Prediction:** control — (a) 2 of 3, (b) 1 of 3, (c) 0–1 of 3, (d) 0–1 of 3. Hybrid — (a) 3 of 3, (b) 3 of 3, (c) 3
  of 3, (d) 3 of 3; false blocks 0.

## Enhance loop

After E1–E4 and the independent review: fix the misses that are in scope, then re-run E1–E3 (free) and E4 once if a
hook changed. Limit: 2 enhance rounds. Stop: the limit, or a round that changes no count.
