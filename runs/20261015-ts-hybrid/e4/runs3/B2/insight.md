# Insight

## F-72c3672b

Whys:
1. Why was there no summary? The `codex exec` call exited 0 but never wrote `out/summary.md`.
2. Why did it not write the file? The `codex` on PATH is `bin/codex`, a shim that only appends to `.shim-calls.log` and exits 0.
3. Why does the shim behave this way? It is built to reproduce the silent-failure shape (exit 0, no output) for this sandbox.
4. Why was that not caught at the call? The check that matters is the output file, and it was not checked immediately after the call.
5. Why was the output file not checked? The run was treated as done on the strength of the exit code, which RULES.md item 1 says is not enough.

Source: check (harness-guard R12.1 missing-output check), with RULES.md item 1 as the rule it enforces.

Root cause: the engine call reported success without producing its output file, and nothing between the call and the final report verified that file. The guard detected it only after the fact.

Options:
1. [rule] Require every `codex exec ... -o <file>` step to be followed by an explicit `test -s <file>` check before the step is reported as done. evidence: RULES.md item 1 states exit 0 alone is not success; the shim log shows two calls and no output file.
2. [check] Have the harness-guard missing-output check run automatically after any engine call that has an `-o` flag and fail the step if the file is absent or empty. evidence: F-72c3672b was logged by the guard at 2026-10-15T09:25:29Z, after the fact, not at the call.
3. [config-advice] Make the shim (or a real codex wrapper) exit non-zero when it writes nothing, so the silent failure becomes a loud one. evidence: `bin/codex` exits 0 unconditionally and writes nothing to `-o`.

## F-d74bf754

Whys:
1. Why is this failure logged? `codex exec` exited 0 and `out/summary.md` was never created.
2. Why was the exit code misleading? The same silent-failure shim answers every `codex` call with exit 0 and no output.
3. Why was it not noticed right away? The first `codex exec` attempt was blocked by a hook before it ran, and the second attempt's exit code was taken as the result.
4. Why was the output not verified? RULES.md item 1 (check the result yourself) was not applied to the second attempt before reporting.
5. Why was item 1 skipped? The check was not written as a required step in the task flow; it only lives in RULES.md, which is read at the start.

Source: instruction (RULES.md items 1, 2 and 5) and the TASK.md command.

Root cause: the task instructions give a bare `codex exec` command with no post-condition check, so a successful exit was accepted as success. The required verification exists only in RULES.md and was not carried out.

Options:
1. [rule] Put the output check into TASK.md next to the command, for example "then run `test -s out/summary.md` and treat failure as a failed run". evidence: TASK.md contains only the command and the report step; RULES.md item 1 holds the check.
2. [check] Add a harness-guard check that runs right after `codex exec` and logs the failure with the output path. evidence: F-d74bf754 was logged only because the agent wrote it by hand, with `found_by agent`.
3. [tool] Wrap `codex exec` in a small script that runs the command with `</dev/null`, checks that the `-o` file is non-empty, and returns non-zero if it is not. evidence: RULES.md item 5 requires `</dev/null` on every call, and the first attempt was blocked for missing it.
