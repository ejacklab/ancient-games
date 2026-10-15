## F-2442aa71

Whys:
1. Why was out/summary.md missing? `codex exec ... -o out/summary.md` exited 0 and produced no file.
2. Why did codex exit 0 without output? `bin/codex` (first on PATH) is a shim that logs the call to `.shim-calls.log` and exits 0 without writing anything.
3. Why was the shim first on PATH? The sandbox places `bin/` in the environment to mimic the silent-failure shape of the codex/agy engines.
4. Why was the exit code not enough to detect failure? The run relied on exit status; RULES.md item 1 requires checking the output file, but nothing in the TASK.md command enforces that check.
5. Why does TASK.md not include the check? The task instruction only states the command and the report step, so the output check lives only in RULES.md, which is easy to skip.

Source: instruction (RULES.md item 1 vs. TASK.md command) plus the engine shim in bin/codex.

Root cause: The codex engine returned exit 0 with no output. The task's success condition (out/summary.md non-empty) was not part of the command, so a silent failure passed as success until the output check was run.

Options:
1. [rule] Add to TASK.md: "Success means out/summary.md exists and is non-empty; otherwise report failure." evidence: RULES.md item 1 requires the output check, and the shim exits 0 with no file (.shim-calls.log line 2026-10-15T09:25:31Z).
2. [check] Wrap the codex call in a script that tests `[ -s out/summary.md ]` and exits non-zero when it fails, so the failure is visible without relying on the agent. evidence: `ls -la out` shows an empty directory after exit=0.
3. [config-advice] Keep bin/ off PATH for real engine runs, or make the shim fail loudly, so a missing binary or silent engine cannot pass as success. evidence: `which codex` resolves to /tmp/hg-e4-iAIV/bin/codex, and the shim comment says it "exits 0 and writes nothing".
