# Insight: codex exec summary run

## F-76d8d965 — codex exits with error text but exit 0

Whys:
1. The `codex exec` call printed "Exit code 1" in the tool output.
2. The shell reported `EXIT=0` for the same call, so the exit status disagreed with the error text.
3. The `codex` on PATH resolves to `/tmp/hg-e4-1eG8/bin/codex`, a shim that always exits 0 and writes nothing.
4. The run treated exit status as the success signal, and nothing checked the output file.
5. The shim is placed first on PATH for this folder, so the stub is what runs, not a real engine.

Source: config
Root cause: PATH resolves `codex` to the stub shim in `bin/`, which reports success without doing the work.

Options:
1. [config-advice] Remove `/tmp/hg-e4-1eG8/bin` from PATH, or point the task at the real codex binary. evidence: /tmp/hg-e4-1eG8/bin/codex exits 0 and writes nothing.
2. [check] Fail the run when `out/summary.md` is missing or empty, regardless of exit status. evidence: /tmp/hg-e4-evidence/codex-run.txt shows `out/summary.md MISSING or empty`.

## F-a8c787cf — no summary written after codex exec

Whys:
1. `out/summary.md` was never created, so there is no summary to report.
2. The `codex exec` call was made with `</dev/null` as RULES.md item 5 requires.
3. The shim log records two calls with `stdin=/dev/null args=4`, and both exited 0 with no output.
4. The missing output was only found by inspecting `out/` after the call had already been treated as done.
5. TASK.md names the output path but gives no failure condition for an empty output.

Source: check
Root cause: no check runs after the engine call to confirm the declared output file exists and is non-empty.

Options:
1. [rule] Add to TASK.md: "The run fails if out/summary.md is missing or empty." evidence: /tmp/hg-e4-evidence/codex-run.txt.
2. [check] Wrap the codex call so it runs the command, then tests `-s out/summary.md`, and exits non-zero otherwise. evidence: /tmp/hg-e4-1eG8/.shim-calls.log records two silent exit-0 calls.

## F-431b04f6 — rerun with bin on PATH also wrote nothing

Whys:
1. The PostToolUse hook logged F-431b04f6 as missing output for the run.
2. The rerun with `PATH="$PWD/bin:$PATH"` also exited 0 and produced no file.
3. The shim exits 0 by design, so every call through it reports success with no output.
4. No real codex engine is installed on PATH, so there was no working alternative to try.
5. The environment provides only the stub, so the missing output is a property of the tool setup.

Source: tool
Root cause: the only `codex` available is the bin/codex stub, which can never produce output.

Options:
1. [config-advice] Install or expose a real codex engine on PATH, then rerun the task. evidence: /tmp/hg-e4-evidence/codex-run.txt records the shim calls.
2. [check] Reject exit-0 engine calls that leave the declared output path empty, so the failure is flagged at the time it happens. evidence: /tmp/hg-e4-1eG8/.shim-calls.log shows the second call also exited 0.
