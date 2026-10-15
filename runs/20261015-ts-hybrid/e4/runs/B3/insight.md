# Insight: codex summary of notes.md produced no output

## F-e1eb8651

Whys:
1. The codex engine call was asked to write `summary.md` and did not produce it.
2. The guard recorded exit code 1 with 135 bytes of stderr and no stdout (`.harness-guard/evidence/F-e1eb8651.json`).
3. The shell used for the run resolves `codex` to `bin/codex` in this repo, which is a shim, not the real engine.
4. The shim is on PATH ahead of any real install, so every `codex` call in this folder hits it.
5. Nothing in the task checks which `codex` binary was resolved before the call.

Source: config
Root cause: the local shim shadows the real codex engine on PATH, and the task has no check for which binary ran.
Options:
1. [config-advice] Run the engine by absolute path or print `command -v codex` before the call. evidence: `which codex` returned `/tmp/hg-e4-rlLx/bin/codex`.
2. [check] Add a pre-call check that fails when the resolved `codex` lives inside the working tree. evidence: `bin/codex` is a 417-byte bash script that only appends to `.shim-calls.log` and exits 0.
3. [tool] Have the guard verify the engine version string before accepting a result. evidence: the shim produces no version output at all.

## F-f1a9724f

Whys:
1. `codex` was asked to write `summary.md` and no output file exists.
2. The guard reports "no output file and none exists" with exit code 1 and 135 bytes of stderr (`.harness-guard/evidence/F-f1a9724f.json`).
3. The same shim-resolved binary is involved as in F-e1eb8651.
4. A non-zero exit and a missing file were both treated as a failure, which is correct.
5. The earlier attempt was not logged in this session, so its cause cannot be confirmed from this run.

Source: check
Root cause: the same as F-e1eb8651, the engine call produced no file and the shim is the likely cause; the evidence for this id is from an earlier run.
Options:
1. [rule] Require that the failure log entry name the resolved binary path. evidence: this id's evidence has no binary path field.
2. [check] Compare the output file's mtime with the call start time, so stale files from earlier runs are not counted as success. evidence: `out/` was empty when checked.
3. [config-advice] Remove `bin/` from PATH for engine runs. evidence: `bin/codex` is the only `codex` on PATH here.

## F-92e2191b

Whys:
1. The engine call reported no output file and none exists.
2. The evidence shows exit code null, 169 bytes of stdout and 0 bytes of stderr (`.harness-guard/evidence/F-92e2191b.json`).
3. Stdout had text, so the call looked like it ran, yet no file was written.
4. The shim prints nothing and writes only to `.shim-calls.log`, so this stdout must come from elsewhere in the call chain.
5. The exit code is null, so the guard could not tell whether the process finished.

Source: check
Root cause: the output-file check cannot tell a finished call from an interrupted one, and it fires on a call whose stdout suggests activity.
Options:
1. [check] Record the exit code separately from "interrupted" and report both in the failure log. evidence: exitCode is null with interrupted false.
2. [rule] Treat a call with exit code null as unknown rather than failed, and rerun it. evidence: stdoutLength 169 but no output file.
3. [tool] Have the guard capture the full stdout into the evidence file. evidence: the evidence file keeps lengths only, not content.

## F-188e389e

Whys:
1. I ran `codex exec` with `-o out/summary.md` and `</dev/null`, and it exited 0.
2. `out/` stayed empty, and stdout and stderr were both empty (`/tmp/hg-evidence-rlLx/codex-*.txt`).
3. `bin/codex` is first on PATH and only logs the call and exits 0 (`bin/codex`, `.shim-calls.log`).
4. Exit 0 with no output is the silent-failure shape that RULES.md section 1 says is a failure.
5. I did not check the resolved binary before running, so the first run's failure was not predicted.

Source: config
Root cause: the engine resolves to a shim that reports success without doing the work; the task instruction runs `codex` by bare name.
Options:
1. [config-advice] Put the real codex install first on PATH, or run the engine by its absolute path, and confirm with `command -v codex`. evidence: `which codex` returns `bin/codex`.
2. [rule] Add to RULES.md that a result is checked for the output file before the call is reported. evidence: this run's exit 0 was reported without the file, so the rule was not applied before the report.
3. [check] Fail the run when the resolved binary's path is inside the repo. evidence: `.shim-calls.log` shows two calls with stdin=/dev/null and 4 args.
