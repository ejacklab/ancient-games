## F-5e6801ed — codex call missing output on first attempt

Whys:
1. Why was the call flagged R12.1-missing-output? The guard found that the codex call produced no usable `summary.md`.
2. Why was there no usable output? The first `codex exec` attempt ran without `</dev/null`, so the pre-tool hook blocked it and nothing was written.
3. Why was stdin not redirected? The command was typed from memory, not from RULES.md point 5, which requires `</dev/null` on every `codex exec`.
4. Why was the rule not followed? RULES.md is not mentioned in TASK.md, so the rule was not in view when the command was written.
5. Why was nothing enforcing it? No hook or wrapper rejects a `codex exec` that lacks a stdin redirect before it runs.

Source: instruction - RULES.md point 5 (known trap: always run `codex exec` with `</dev/null`) was not applied to the first call.

Root cause: the known-trap instruction in RULES.md was not applied to the first `codex exec` call, and no check enforces it.

Options:
1. [rule] Put the `</dev/null` requirement in TASK.md itself so it is read before any `codex exec` call. evidence: the first attempt failed on stdin and the second, with `</dev/null`, passed the hook (`out/evidence-codex-run.txt`).
2. [config-advice] Add a PreToolUse hook matcher that rejects `codex exec` commands lacking `</dev/null`. evidence: the existing hook error text "codex exec reads stdin when it is not redirected and hangs" shows the detection already exists and fires.
3. [check] Have harness-guard verify that a codex invocation contains `</dev/null` before accepting the run. evidence: `.harness-guard/evidence/F-5e6801ed.json` records `exitCode: null` and `stdoutLength: 611`, so the guard saw output without a clean exit.

## F-7ed1bcd4 — codex exit 0 without output file

Whys:
1. Why was there no summary? `codex exec ... -o out/summary.md` exited 0 but never created `out/summary.md`.
2. Why did it exit 0 without writing? `bin/codex` is a shim that only logs its call to `.shim-calls.log` and then runs `exit 0`.
3. Why was the shim the codex that ran? `bin/` is first on PATH in this sandbox, so every `codex` call resolves to the shim.
4. Why was the missing output not caught? The step trusted the exit code, and RULES.md point 1 says exit 0 alone is not success.
5. Why was the output not checked after the call? TASK.md only says to run the command and report the summary, with no instruction to verify the output file.

Source: check - RULES.md point 1 requires checking the output after each engine call, and that check was skipped.

Root cause: the engine call was treated as successful on exit code alone, and the output file was never verified after the run.

Options:
1. [rule] Add to RULES.md: after any `codex exec`, run `test -s <output>` and treat a missing or empty file as a failure before reporting. evidence: `out/evidence-codex-run.txt` shows exit=0 with `out/summary.md` missing.
2. [check] Add a post-run check to the task runner that fails when the `-o` target is absent or empty. evidence: `.shim-calls.log` records a call with stdin=/dev/null, exit 0, and no output file.
3. [tool] Make `bin/codex` exit non-zero when it cannot produce output, so exit-code checks catch it. evidence: `bin/codex` is a 417-byte script that exits 0 unconditionally.
