status: done

Round 20's four review findings are implemented: a deferred criteria step is no result at all, `deadline wait --mark` fails before anything waits, and above 580 s every command a crossed-build-check step starts runs in the background writing its exit to a `.exit` file, with every test command under `timeout <N>` like an engine call.

## Pieces

- `cr1a` (CR1a)
  - `.claude/skills/workflow-design/guard/src/hooks.ts`, `criteriaStep`: while the session's own deadline is open and not
    up (DL4's choice, unchanged), the step returns `null` — no result at all — instead of `QUIET`, so `handleStop` goes
    on to its next step, `pathAsk`, exactly as when the session touched no criteria file. Nothing is scored, no failure
    and no record is written, and the step still runs as before once the deadline is ended or up. Every other stop step
    is untouched.
- `dl5` (DL5)
  - `.claude/skills/workflow-design/guard/src/cli.ts`, `deadlineCommand`: the `wait --mark` usage error moved up to just
    after the verb check, before `named()` resolves an id or a run and before anything sleeps, so
    `deadline wait --id D-… --mark 50` and `deadline wait --run DIR --mark 50` exit 2 with the same
    `deadline wait: --mark was removed with the percent marks; …` message instead of waiting. The message, the exit code
    and the no-flag path are unchanged.
- `xb` (XB2, XB3)
  - `.claude/workflows/crossed-build-check.js`: `bgCommand(file, command)` and `fgCommand(command)` build every command a
    step starts — above 580 s exactly `( timeout <N> <command>; echo "exit $?" > <file>.exit ) &`, otherwise
    `timeout <N> <command>`. `engineRun` (write, review) and the new `testRun(t, out)` (fail first, head) both go
    through it, so a test command carries the same limit as an engine call (XB3); the old `testLimit()` wording is gone.
    `COMMON(label, file)` now names the step's `.exit` file and says a missing one after `<N>` s is a failed step, never
    a pass (XB2); in the foreground branch it names the Bash tool's own allowance as `(TIMEOUT + 20) * 1000` ms instead of
    the fixed `600000`, so nothing below 580 s is told to use the 600 s cap. `runStep`'s `wait for it to end` prose is
    replaced by the `.exit` rule, and `failFirstStep`/`headStep`/`writeStep`/`runReview` pass their output file to
    `COMMON`.

## Commands (last lines)

- `cd .claude/skills/workflow-design/guard && bun test` → `Ran 1560 tests across 40 files. [14.48s]` (1560 pass, 0 fail)
- `cd .claude/skills/workflow-design/guard && ./node_modules/.bin/tsgo --noEmit -p .` → no output, exit 0
- `node tests/workflows/crossed_build_check_harness.mjs` → `all passed`

The two Round 20b targets on their own: `bun test test/round20b.test.ts` → `Ran 6 tests across 1 file. [104.00ms]`
(6 pass, 0 fail); the harness's XB2 and XB3 checks — `ok XB2 timeout 900: every write, review, fail-first and head prompt
starts its command as ( timeout 900 …; echo "exit $?" > ….exit ) &`, `ok XB2 timeout 900: every prompt says a missing
.exit file is a failed step`, `ok XB3 timeout 120: fail-first and head prompts run "timeout 120 <test_cmd>"`, `ok XB3 the
default: fail-first and head prompts run "timeout 580 <test_cmd>"`, `ok XB3 timeout 120: no prompt holds 600000`.

## CONTRADICTS

None.

Notes, not contradictions: CR1a makes a deferred stop fall through to the path ask, so the Round 20 CR1 test's
"prints nothing" now rests on that session having no success record (its own `pathAsk` is quiet) rather than on the
criteria step returning; it still passes unchanged. In the background form, `fail first`'s exit file is named relative
to the main repository, so the step must pass its absolute path when it runs the command from the worktree — the prose
already told it to use the absolute path for the output file.
