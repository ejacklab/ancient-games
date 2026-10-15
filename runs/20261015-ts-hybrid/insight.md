# Insight — run 20261015-ts-hybrid (the COO's own failures)

Written by the main agent (the COO) for the four failures it logged in `.harness-guard/journal.jsonl` with the
guard's own `fail` command. Proposals only: nothing below is applied without the project owner's choice.

## F-08cf4cc3 — the first Codex call never ran

Whys:
1. Why did m1-tests not run? `runlog.py` stopped with a usage error (exit 2) because `--runs-root` was placed after `exec`.
2. Why was that not seen at once? The wrapper's last command (`ls`) succeeded, so the background task reported exit 0.
3. Why did the wrapper hide the exit? It was a one-off shell line with no check that the node produced a result file.
4. Why was there no such check? The method's runner (`dispatch.py`) was not used for this build, and the hand-run path has no result check of its own — the same gap the code-vs-text inventory found.
Source: check
Root cause: hand-run engine calls had no result-file check; exit 0 of the last command stood in for success.
Options:
1. [tool] Keep `run_node.sh`'s rule — a node ends with "result=present" or fails with exit 3 — as a script in the skill's `scripts/` for hand-run nodes. evidence: it caught m4/m5-tests' missing briefs and m5-tests-3's missing result later in this run (state.md).
2. [check] The guard's PostToolUse result check covers engine calls made through a shell once installed; a `runlog.py … -- <engine>` call is recognised (round 2 wrapper stripping). evidence: E2 round 2, `effectiveness/e2-round2.md`.
3. [rule] Method 3.8 item 4 gains one sentence: a hand-run node is done only when its result file exists and validates. evidence: this failure.

## F-f44538b2 — the runner was edited while it ran

Whys:
1. Why did the m5-code missing result go unseen? `run_node.sh` crashed with a bash syntax error after the engine call.
2. Why did it crash? The COO edited `run_node.sh` (adding the review branch) while a run was still executing it.
3. Why does editing break a running script? bash reads a script as it runs, so the running copy read half of the new text.
4. Why was it edited in place? The COO treated the runner as a config file, not as a program in use.
Source: instruction
Root cause: no rule against editing a script that a running process is executing.
Options:
1. [rule] Never edit a script while a background run uses it; write the new version to a new file and switch over between runs. evidence: tasks/b3jrjz8l0.output ("unexpected EOF").
2. [tool] Runner scripts copy themselves to a temp file and exec the copy, so an edit cannot reach a running instance. evidence: same.

## F-cf7d58f7 — opencode stopped without a result file

Whys:
1. Why was there no m5-code result? opencode's stdout ends after "Now the CLI:" — it wrote the files and stopped before running its checks or writing the result.
2. Why did it stop there? Not established: exit 0, no error text; the brief asked for the result last.
3. Why did nothing block the stop? The brief's result step was the last step, so a stop anywhere before it leaves no result.
Source: instruction
Root cause: the brief put the only progress record at the very end; a partial run left no trace of what it had checked.
Options:
1. [rule] Briefs ask for the result file to be written first as `status: partial` and updated at the end ("write it even if you stop early" was added for r3-code, which did report partial). evidence: `nodes/r3-code-1.result.md`.
2. [check] Treat "files changed but no result" as a failed node in `run_node.sh` and `dispatch.py`. evidence: this failure.

## F-3b8bdcec — Codex hit its usage limit mid-run

Whys:
1. Why did m5-tests attempt 3 end with exit 1 and no result? Codex returned "You've hit your usage limit".
2. Why was the limit reached? Five Codex nodes, a test repair and the experts' runs used the plan's quota in one afternoon.
3. Why was that not foreseen? No step estimated quota per engine before the build (method 3.4's cost estimate was not written for this run).
Source: check
Root cause: no quota estimate or check per engine before a multi-node build.
Options:
1. [check] Readiness records each engine's remaining quota where the CLI can report it, and the plan's node count per engine beside it. evidence: this failure; `readiness.md` has no quota line.
2. [rule] A build plan names a second engine of a different kind for each role, used only when the first is unavailable, and says so in the state file (as this run did by hand with a Claude reviewer). evidence: `nodes/review-1.result.md`.
