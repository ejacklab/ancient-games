# Insight: codex exec produced no output

## F-5c0f9976

Whys:
1. Why was there no summary? `out/summary.md` was never created.
2. Why was it not created? The first `codex exec ... -o out/summary.md` run exited with code 1.
3. Why did the engine call exit with code 1? The cause is not in the captured output, because the first run's stderr was not saved.
4. Why was no cause captured? The call was run directly, with no log file for stdout and stderr.
5. Why was that not caught? Nothing in the task checks engine output before the run is reported.

Source: tool

Root cause: the codex engine call failed without leaving a usable reason. The cause is not confirmed.

Options:
1. [config-advice] Before the real run, check the codex setup with `codex --version` and a trivial call such as `codex exec "reply OK" </dev/null`, and confirm the call returns text. evidence: both runs in this session failed without output (/tmp/hg-e4-evidence/codex-exit.txt, /tmp/hg-e4-evidence/codex-stderr.txt).
2. [tool] Redirect stdout and stderr of every engine call to a file in `out/` (for example `> out/codex.log 2>&1`), so a failure always has evidence. evidence: the second run's stdout and stderr were both empty, so no reason was recorded (/tmp/hg-e4-evidence/evidence.txt).

## F-9b0f927a

Whys:
1. Why was the result unusable? The `-o` output file did not exist after the call.
2. Why did the file not exist? `codex exec` wrote nothing to `out/summary.md`.
3. Why did codex write nothing? The engine call did no usable work, and nothing was printed.
4. Why was this not visible? The exit status was the only signal, and it does not show whether output was produced.
5. Why was the exit status trusted? The task went from the call's exit status to the report without checking the output file.

Source: check

Root cause: the call's success was not verified against its output. The reason codex produced no output is not confirmed.

Options:
1. [check] After every engine call, fail when the `-o` target is missing or empty, whatever the exit code. evidence: the second run exited 0 and `out/summary.md` was absent (`ls -la out/` showed an empty directory).
2. [rule] Add to RULES.md that an engine call counts as successful only when its output file exists and is non-empty. evidence: F-d9b6b41b was logged with the same output-missing check, after an exit code of 0.

## F-d9b6b41b

Whys:
1. Why was the result unusable? `out/summary.md` was missing after the second `codex exec` run.
2. Why was it missing? The second run also printed nothing to stdout or stderr.
3. Why did it print nothing? The engine call did no usable work, and gave no reason.
4. Why was no reason recorded? The output was not redirected to a file.
5. Why did the second run repeat the first run's failure? The first failure was not investigated before the retry.

Source: tool

Root cause: the engine call produced no output on retry, and the first failure was not diagnosed before it was retried.

Options:
1. [rule] Require a diagnosis step before any retry of an engine call: capture stdout, stderr, and exit code to a file, and state the reason in the failure log. evidence: `/tmp/hg-e4-evidence/codex-stdout.txt` and `codex-stderr.txt` were both empty on the retry.
2. [config-advice] Confirm that `codex` is authenticated and configured for this machine before running tasks that depend on it. evidence: both runs ended without output, which is consistent with a setup problem, though this is not confirmed.

## F-8f525eb4

Whys:
1. Why does the failure exist? The check `output-file-exists` found that `out/summary.md` was missing.
2. Why was the file missing? `codex exec` wrote nothing to it.
3. Why did codex write nothing? Its stdout and stderr were also empty, so it gave no reason.
4. Why was it still reported as done? The exit code was 0, and the task did not compare the output with the expected file.
5. Why were the expected output and exit code not compared? Rule 1 is not enforced by any tool or check.

Source: check

Root cause: exit code 0 was treated as success, although no output was produced. The reason codex produced no output is not confirmed.

Options:
1. [check] Add a harness check that runs after every `codex exec` call and fails when `-o` produces no non-empty file. evidence: this failure was logged with exit 0, `out/summary.md` absent, and empty stdout and stderr (`/tmp/hg-e4-evidence/evidence.txt`).
2. [tool] Wrap engine calls in a small script that runs the call, checks the output file, and prints a clear error if it is missing. evidence: the same run was reported without any such check (`ls -la out/` shows an empty directory).
