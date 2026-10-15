# Insight: codex summary failures

## F-7a2574b7

Whys:
1. Why was there no `out/summary.md`? The `codex` that ran was `bin/codex`, not the real CLI.
2. Why did `bin/codex` run? `bin/` is first on PATH, so it shadows `~/.npm-global/bin/codex`.
3. Why does the shim exit 0 with no output? It is written to simulate a silent failure (its own comment says so).
4. Why did exit 0 look like success? The task's command only checks the exit code, not the output file.
5. Why is the check missing from the task? Nothing in TASK.md requires an output check; RULES.md item 1 does, but it is not wired into the run.

Source: config
Root cause: PATH resolves `codex` to the repo shim, which exits 0 and writes nothing. Evidence: `.harness-guard/evidence/F-7a2574b7.json` (exitCode null, stdoutLength 241, outputName summary.md), `.shim-calls.log`, `bin/codex`.
Options:
1. [config-advice] Remove `bin/` from PATH for this task, or invoke codex by absolute path. evidence: `~/.npm-global/bin/codex` exists and ran (exit 1 from usage limit, not silent).
2. [check] After each engine call, fail unless `out/summary.md` exists and is non-empty. evidence: `out/evidence-codex-summary.txt` shows the missing file while exit was 0.
3. [tool] Make `bin/codex` exit non-zero when it writes no output, so the silent shape is loud. evidence: `bin/codex` line 5 `exit 0`.

## F-acd8b58b

Whys:
1. Why did the guard flag exit code 1? The codex call exited 1.
2. Why did it exit 1? The real binary hit its usage limit and reported an error.
3. Why was no summary produced? The engine stopped before writing `-o out/summary.md`.
4. Why was this not caught earlier? The first run used the shim, so the real account limit was never reached.
5. Why does that matter? A quota error and a shim-silence look different, but both leave the task unfinished.

Source: tool
Root cause: the codex account is out of usage until 7:24 PM. Evidence: `.harness-guard/evidence/F-acd8b58b.json` (exitCode in guard output is 1), `out/evidence-codex-usage-limit.txt`.
Options:
1. [check] Treat a non-zero codex exit as a failure with the error text captured in the evidence file. evidence: `out/evidence-codex-usage-limit.txt`.
2. [tool] Retry after the reset time or use another configured engine, only if the user approves. evidence: the usage-limit message gives "try again at 7:24 PM".
3. [config-advice] Check remaining codex quota before the run. evidence: the failure appeared only after the call, not before.

## F-0b99fc48

Whys:
1. Why was the output missing again? A second guard entry was written at the same time as F-acd8b58b.
2. Why two entries for one run? The guard logged both the missing-output and exit checks for the same call.
3. Why were they not merged? The guard keys each check separately, with no grouping by call.
4. Why does that matter? One bad call inflates the failure count.
5. Why was this not seen before? The journal is append-only and has no per-call id.

Source: check
Root cause: the guard reports one failure per rule for each engine call. Evidence: `.harness-guard/evidence/F-0b99fc48.json` (exitCode null, stdoutLength 241), `.harness-guard/journal.jsonl`.
Options:
1. [check] Group guard failures by call id so one call yields one failure. evidence: F-acd8b58b and F-0b99fc48 share the same timestamp and input.
2. [rule] Add a note to RULES.md that a missing output and a non-zero exit from one call count as one failure. evidence: both entries have `input: "codex summary.md"`.
3. [config-advice] Leave the rule as is and read the counts with that overlap in mind. evidence: the guard output lists four open ids for one task.

## F-99ea442b

Whys:
1. Why did this failure get logged? The real codex call exited 1 with no output file.
2. Why was it logged by hand? The guard did not catch the real-binary run, so I logged it with `harness-guard fail`.
3. Why was the guard silent on it? The run used the absolute path, outside the guard's hook.
4. Why does that matter? Failures can go unlogged when the engine is called by another path.
5. Why is the path different? PATH points at a shim, and the real binary has its own absolute path.

Source: tool
Root cause: the guard hook covers `codex` on PATH, not the absolute path to the real binary. Evidence: `out/evidence-codex-usage-limit.txt`, `.harness-guard/journal.jsonl` (F-99ea442b).
Options:
1. [check] Log every engine call through the same guard, whatever path it was run by. evidence: F-99ea442b was logged by hand, not by the hook.
2. [config-advice] Put the real codex first on PATH, so the guard hook sees it. evidence: `~/.npm-global/bin/codex` is found only when `bin/` is removed from PATH.
3. [rule] Require the agent to log each failure at the moment it happens, as RULES.md item 2 already says. evidence: F-99ea442b was logged after the run, not during it.
