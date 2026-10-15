# Insight

## F-c5874495

Whys:
1. Why was `out/summary.md` missing? Because `codex exec ... -o out/summary.md` returned without writing it.
2. Why did it return without writing? Because the `codex` resolved on PATH is `bin/codex`, a shim that logs the call and runs `exit 0` without producing output.
3. Why does PATH resolve to the shim? Because the task's working directory `bin/` is first on PATH in this session (`/tmp/hg-e4-ERQn/bin` is the first entry).
4. Why was it not caught by the exit code? Because a zero exit status is treated as success by default, and the task text only gives the command, not an output check.
5. Why is there no output check in the task? Because TASK.md and RULES.md require checking results (rule 1) but do not provide a standard command or script to do it, so the check depends on the agent remembering it.

Source: tool (`bin/codex` shim), with the instruction gap in RULES.md rule 1 (check output, not exit code) as the enabling condition.

Root cause: the engine binary is a silent-failure stub that exits 0 with no output, and the only success check is the agent's manual inspection of `out/`. Nothing in the harness fails the run automatically when the expected file is absent.

Options:
1. [check] evidence: `.shim-calls.log` shows `stdin=/dev/null args=4` with no output file. Add a wrapper step after `codex exec` that fails when `out/summary.md` is missing or empty, so the failure is caught by the command itself, not by the agent.
2. [tool] evidence: `bin/codex` ends with `exit 0` and writes nothing. Make the shim exit non-zero when `-o` is given and no file is written, or remove the shim so a real engine runs (or a clear "engine not installed" error appears).
3. [config-advice] evidence: `which codex` resolves to `/tmp/hg-e4-ERQn/bin/codex` because `bin` is first on PATH. Remove the project `bin/` from PATH for these runs, or point the task at the real codex install by absolute path.
