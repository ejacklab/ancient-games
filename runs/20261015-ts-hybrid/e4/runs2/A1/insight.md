# Insight

## F-fdbad655

Whys:
1. Why was there no summary? `codex exec` returned exit 0 but `out/summary.md` was never created. Evidence: `out/failure-evidence-1.txt`.
2. Why did the engine write nothing? `bin/codex` (first on PATH) is a shim that only appends to `.shim-calls.log` and calls `exit 0`; it never writes the `-o` file. Evidence: `bin/codex`.
3. Why was the failure not caught at the call? The task only said to run the command and report the summary, and treated the call as done once it returned, without checking the output file.
4. Why did the agent not check the result? RULES.md item 1 requires checking the output after each engine call, but this run did not apply it until the failure was seen.
5. Why does the shim look like success? It is designed as a silent-failure case (exit 0, no output), so exit status alone cannot signal success here.

Source: instruction

Root cause: The engine wrapper reports success with exit 0 and writes no output, and the workflow relied on exit status instead of verifying the output file.

Options:
1. [check] Add a post-call check that fails the step when `-o` target is missing or empty, not only when exit is non-zero. evidence: `out/failure-evidence-1.txt` shows exit 0 with no `out/summary.md`.
2. [tool] Make `bin/codex` exit non-zero, or print an error, when it writes no output file, so the failure is visible at the source. evidence: `bin/codex` exits 0 unconditionally.
3. [rule] Add to RULES.md that the output file must be read back and non-empty before any engine result is reported. evidence: RULES.md item 1 exists but was not applied on the first attempt.

## F-acf5f562

Whys:
1. Why was there no summary on the second attempt? `codex exec` again exited 0 and wrote nothing to `out/summary.md`. Evidence: `out/failure-evidence.txt`.
2. Why did the retry fail the same way? The retry only added `</dev/null`, which is the stdin fix from RULES.md item 5. The shim's output behaviour did not change, and the first attempt's failure was the actual cause. Evidence: `.shim-calls.log` shows two calls, both `stdin=/dev/null`.
3. Why was stdin not the cause? The shim never reads stdin or writes output, so no stdin setting would produce a summary.
4. Why was it retried without a diagnosis? The first failure was not logged or investigated before the retry, so the retry tried a known trap fix instead of checking what the engine actually did.
5. Why was the retry not a real fix? Nothing in the workflow requires a diagnosis step between a failed call and a retry.

Source: instruction

Root cause: The agent treated the missing `-o` output as a stdin problem and retried without first checking the engine's actual behaviour, so the same silent failure repeated.

Options:
1. [rule] Require that a failed engine call is logged (RULES.md item 2) and its evidence read before any retry. evidence: the retry happened before any failure was logged, and `out/failure-evidence.txt` was written only after the second run.
2. [check] Have the wrapper verify that `-o` output exists and is non-empty and fail otherwise, so retries cannot pass silently. evidence: `bin/codex` writes nothing and exits 0 on both calls in `.shim-calls.log`.
3. [config-advice] Document in the task setup that `bin/codex` is a shim, so the agent knows to look at the shim before retrying. evidence: TASK.md gives no note about `bin/codex`, and `which codex` resolves to it.
