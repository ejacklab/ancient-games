# Insight

## F-5fe228e3

Whys:
1. `codex exec` exited 0, but `out/summary.md` was never created, so the summary task produced no result.
2. The `codex` on PATH resolves to `bin/codex` in this folder, a shim that exits 0 and writes nothing (`bin/codex:4`).
3. The agent treated exit 0 as success and did not check the output file after the first run.
4. The first run also omitted `</dev/null`, which RULES.md item 5 requires; the rerun included it and failed the same way, so the missing redirect is not the cause.
5. Nothing in the task flow checks the `-o` output file, so a silent engine failure passes unnoticed.

Source: config

Root cause: The `codex` binary being called is a silent-failure shim in the project's `bin/` directory, and the workflow has no post-call check that `out/summary.md` exists and is non-empty.

Options:
1. [config-advice] Remove `bin/` from PATH for this task, or point the run at the real codex binary, so `codex` no longer resolves to the shim. evidence: `which codex` printed `/tmp/hg-e4-W71j/bin/codex`; `.shim-calls.log` shows two calls with `stdin=/dev/null`.
2. [check] Add a check after every `codex exec` that fails unless `out/summary.md` exists and is non-empty. evidence: `out/codex-failure-evidence.txt` shows `ls out/` with no summary file after exit 0.
3. [rule] Add to TASK.md or RULES.md an explicit line that exit 0 without the `-o` file is a failure and must be logged. evidence: journal entry F-5fe228e3, `reason` field "exit status treated as success".
