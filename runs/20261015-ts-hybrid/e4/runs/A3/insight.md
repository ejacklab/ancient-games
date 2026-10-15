# Insight

## F-79db2403

Whys:
1. Why did the task fail? `codex exec` returned exit 0 but never created `out/summary.md`.
2. Why was nothing written? `bin/codex` is a shim that unconditionally runs `exit 0` and only appends a line to `.shim-calls.log`; it never produces the `-o` file.
3. Why did exit 0 look like success? The task's command line (TASK.md) gives no completion criterion beyond running the command, so exit status is the only signal available at that point.
4. Why was the gap not caught by the engine call itself? The engine wrapper does not validate its own output contract (`-o` file present and non-empty) before returning.
5. Why does this matter? A silent engine failure yields no summary, and a downstream reader could report a result that was never produced.

Source: tool

The shim `bin/codex` is the failing tool. The TASK.md command line has no output-existence check, and RULES.md item 1 is what caught it.

Root cause: the engine shim (or the real engine path it stands in for) reports success without producing its declared output file, and the task instruction does not require a post-run output check.

Options:
1. [rule] Add to RULES.md: after any engine call, treat a missing or empty `-o` file as failure even when exit is 0 (already implied by item 1; state the file check explicitly with the path). evidence: `out/` was empty after exit 0 (`.harness-guard/codex-silent-failure.txt`).
2. [check] Wrap the engine call in a check script that runs `codex exec ... -o <file>`, then fails unless `<file>` exists and is non-empty, and logs the failure automatically. evidence: `.shim-calls.log` shows one call with `stdin=/dev/null` and exit 0 and no output file.
3. [config-advice] Fix or replace the `bin/codex` shim so it either writes the `-o` target or exits non-zero when it cannot, and remove the shim from PATH for real runs. evidence: `bin/codex` body is `exit 0` with no output write.
