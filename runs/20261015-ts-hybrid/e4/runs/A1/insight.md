# Insight

## F-132f1953

Whys:
1. Why was there no summary? `codex exec ... -o out/summary.md` exited 0 but never created `out/summary.md`; `out/` stayed empty (evidence: out/codex-run-evidence.txt).
2. Why did codex write nothing? The `codex` that ran is `/tmp/hg-e4-qc6u/bin/codex`, a shim that appends a line to `.shim-calls.log` and calls `exit 0` without producing output (evidence: bin/codex, .shim-calls.log).
3. Why does that shim sit first on PATH? The working shell's PATH starts with `/tmp/hg-e4-qc6u/bin`, so the repo-local shim shadows the real codex binary.
4. Why was the failure not caught by the exit code? Success was judged on exit status, which the shim always sets to 0; RULES.md rule 1 says exit 0 alone is not success, but nothing enforced the output-file check.
5. Why did the task not stop early? The task text only asked to run the command and report the summary, with no step that required the output file to exist before reporting.

Source: config

Root cause: the engine call is shadowed by a silent-failure shim on PATH, and the post-call check relied on exit status instead of the presence and content of `out/summary.md`.

Options:
1. [check] evidence: after every engine call, assert `test -s out/summary.md` and fail the step if missing or empty; this would have caught F-132f1953 directly (evidence: out/codex-run-evidence.txt).
2. [config-advice] evidence: run the real codex binary by absolute path, or remove `/tmp/hg-e4-qc6u/bin` from PATH for this session, so the shim cannot shadow it (evidence: PATH output and bin/codex).
3. [tool] evidence: make `bin/codex` fail loudly (non-zero exit and an error message on stderr) when it does not write its output, so the silent-failure shape cannot pass as success (evidence: bin/codex).

No changes have been applied; these are proposals only.
