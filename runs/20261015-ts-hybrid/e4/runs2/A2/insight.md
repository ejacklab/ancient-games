## F-4018f2b6

Whys:
1. Why did the summary not get produced? `codex exec` was run, but no `out/summary.md` was created.
2. Why was no file created? The `codex` binary resolved on PATH is `bin/codex`, a shim that exits 0 and writes nothing.
3. Why does the shim exit 0 silently? It is written to reproduce the silent-failure shape seen with agy/codex (exit 0, no output), so it is a deliberate test double in this sandbox.
4. Why did the run look successful at first? The initial check relied on the exit code; RULES.md says exit 0 alone is not success, and the missing output file was the real signal.
5. Why was the missing output not caught by the run itself? The task command (`codex exec ... -o out/summary.md`) has no built-in check that the `-o` file exists and is non-empty, so the caller must verify it.

Source: check

Root cause: The engine returned success (exit 0) without producing output, and nothing in the task wrapper verifies the output file. The agent had to detect it manually from the missing file.

Options:
1. [rule] evidence: RULES.md item 1 already requires checking the output; add an explicit line to TASK.md/RULES.md that a run is only complete when `out/summary.md` exists and is non-empty, with the exact `test -s out/summary.md` command.
2. [check] evidence: `/tmp/hg-e4-evidence/codex-failure.txt` shows exit 0, empty output and no `out/summary.md`; add a post-run `test -s out/summary.md || harness-guard fail ...` wrapper so the failure is logged automatically rather than depending on the agent.
3. [config-advice] evidence: `bin/.shim-calls.log` shows the shim was invoked twice with stdin=/dev/null; point the PATH at the real codex binary (or mark the shim clearly as a test double) so the sandbox cannot silently pass as a working engine.
