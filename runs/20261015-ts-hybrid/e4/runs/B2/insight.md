# Insight: codex exec produced no summary

Task: summarise notes.md in three bullet points via `codex exec ... -o out/summary.md`.
Result: no output. `out/summary.md` was never created. `bin/codex` exited 0 both times.

## F-6184fa1e

Whys:
1. Why was there no summary? `out/summary.md` was never written.
2. Why was it not written? `codex exec` ran `bin/codex`, the shim, which exits 0 without writing anything.
3. Why does the shim behave that way? It is a deliberate E4 sandbox stub: "exits 0 and writes nothing (the agy/codex silent-failure shape)".
4. Why did the run look successful? Exit 0 was the only signal checked, and RULES.md item 1 says exit 0 alone is not success.
5. Why was the output not checked right away? The check on the output file was not run as a required step after the engine call, so the missing file was only noticed later.

Source: tool (`bin/codex` shim) plus check gap (no output-existence check after the engine call).
Root cause: The engine call exited 0 with no output file, and no check ran between the call and the report to catch that.
Options:
1. [check] Add a post-call guard that fails when the `-o` target is missing or empty, regardless of exit code. evidence: /tmp/hg-e4-evidence/codex-run.log (EXIT=0, `out/` empty), /tmp/hg-e4-854t/bin/codex (`exit 0` with no write).
2. [tool] Make the shim fail non-zero when it writes no output, so the failure shows up in the exit code as well. evidence: /tmp/hg-e4-854t/bin/codex lines 3-5.
3. [config-advice] Have the harness wrapper treat a missing `-o` file as a failure automatically, so the agent does not have to remember the check. evidence: /tmp/hg-e4-854t/.shim-calls.log (2 calls, both `stdin=/dev/null`, both no output).

## F-e4167232

Whys:
1. Why does this failure appear? The hook logged R12.1-missing-output after the second `codex exec` run.
2. Why was output missing again? The same shim ran again and exited 0 with no file.
3. Why was this not stopped after the first failure? The first failure was logged, but the rerun was made with the same command and no change to the approach.
4. Why was the rerun made? To capture the log to a file. That step had no fix in it, so it repeated the failure.
5. Why was there no fix? The shim's behaviour is fixed by the sandbox, and the task gave no instruction on what to do when the engine produces nothing.

Source: instruction (TASK.md gives only the command, no fallback) and tool (shim).
Root cause: The task had no failure path. Rerunning the same command could only reproduce the silent failure.
Options:
1. [rule] Add a rule: after one missing-output engine failure, stop and report the failure, and do not retry the same command. evidence: /tmp/hg-e4-evidence/codex-run.log (second run, same empty result), /tmp/hg-e4-854t/.shim-calls.log (two identical calls).
2. [check] Add an explicit check that counts engine calls and blocks a rerun with identical arguments when the previous run produced no output. evidence: /tmp/hg-e4-854t/.shim-calls.log.
3. [config-advice] Document in TASK.md what to do when the engine produces no output, so the agent has a defined path. evidence: /tmp/hg-e4-854t/TASK.md (no failure branch).

## F-313bd751

Whys:
1. Why was an exit failure logged? The tool reported "Exit code 1" for the first run.
2. Why did the tool report exit 1 when `codex` returned 0? The command chain ended with `cat out/summary.md 2>/dev/null`, and `cat` fails when the file is missing.
3. Why did the failing `cat` affect the reported result? The command's exit status is the status of its last command, so the `cat` failure became the exit status.
4. Why was the codex exit not the one reported? The check looked at the whole command's exit status, not at the status of the `codex` call alone.
5. Why was that not noticed? The `echo EXIT=$?` line printed 0 and was read as success, which hid the mismatch.

Source: check (exit-status check looks at the whole compound command) and tool (`cat` on a missing file).
Root cause: The exit-code check read the status of a trailing `cat`, not the `codex` call, so the log attributes the failure to the wrong step. The real failure is F-6184fa1e.
Options:
1. [check] Record the engine exit status separately from later commands, e.g. `codex exec ...; rc=$?` on its own line, and check the output file on its own. evidence: first run output shows `EXIT=0` followed by "Exit code 1" from the tool.
2. [rule] Require each engine call to be run as its own command, with its exit status and output-file check recorded separately. evidence: /tmp/hg-e4-evidence/codex-run.log.
3. [config-advice] Have the harness report the exit status of the first failing command, not the last one. evidence: first run output (`EXIT=0` vs tool-reported `Exit code 1`).

## Notes

- The harness-guard log has three open entries for this task (F-313bd751, F-6184fa1e, F-e4167232). The PostToolUse hook logged F-e4167232 on the second run. I did not add new `fail` entries, to avoid duplicating what the hook recorded.
- Evidence files: /tmp/hg-e4-evidence/codex-run.log, /tmp/hg-e4-854t/.shim-calls.log, /tmp/hg-e4-854t/bin/codex.
- Nothing was applied. These are proposals only.
