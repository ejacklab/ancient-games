status: done

Round 20 of the guard SPEC is implemented: one deadline at a time in the CLI, the criteria step at the end of the
session's deadline, and `args.timeout` in crossed-build-check; the full suite, the type check and the workflow harness
all pass.

## Pieces

- `dl` (DL1–DL4)
  - `.claude/skills/workflow-design/guard/src/deadline.ts`: `openDeadlines` (every never-ended deadline of a scope, newest
    first), `deadlineById` (the deadline an id names, whatever its session or run), `deadlineByRun` (the newest open one
    of a run, compared the way `deadline start --run` stores it: `path.relative(root, path.resolve(root, dir))`);
    `deadlineStatus` now delegates to the new `statusOf`, so one chosen deadline can be reported on its own;
    `endDeadline` delegates to the new `endOne`; `endedLine` prints `<id> ended <time>`.
  - `.claude/skills/workflow-design/guard/src/cli.ts`, `deadlineCommand`: `--id`/`--run` resolve one deadline through
    `named()`; no file or no open deadline of that run writes `no deadline <id>` / `no deadline for <DIR>` on stderr and
    exits 2; an ended deadline prints `endedLine` and exits 0 for every verb; `status`/`wait` act on the chosen deadline
    (`status` exit 1 when it is up, `wait` sleeps to its end and reports it); `end` with neither flag lists every open id
    with its run on stderr and exits 2 when more than one is open, and ends the one when there is exactly one. The
    no-flag `status`/`wait` paths are unchanged (DL4), including their exit codes and messages; the usage text names the
    new flags.
- `cr` (CR1)
  - `.claude/skills/workflow-design/guard/src/hooks.ts`, `criteriaStep`: before it scores anything it reads the
    session's own deadline (`deadlineStatus(root, session, now, false)` — DL4's choice) and, while that deadline is not
    up, returns the context line
    `harness-guard: criteria are scored when deadline <id> ends or is up (<n> min left)` as a Stop context, so it neither
    blocks nor writes a criterion or late-criteria failure. Once the deadline is ended or up, or the session has none,
    it runs exactly as before; every other step of the stop is untouched.
- `xb` (XB1)
  - `.claude/workflows/crossed-build-check.js`: `args.timeout` (whole seconds, 60–3600, default 580) is validated with
    the other args, before any agent (`args.timeout must be a whole number of seconds from 60 to 3600`);
    `engineRun` (write and review) and `testLimit` (fail first and head) carry it into every engine call and every test
    command, and above 580 the command is started with `&` and the step waits for the process to end — `COMMON` item 3
    says so for every step too.

## Commands (last lines)

- `cd .claude/skills/workflow-design/guard && bun test` → `Ran 1554 tests across 39 files. [16.23s]` (1554 pass, 0 fail)
- `cd .claude/skills/workflow-design/guard && ./node_modules/.bin/tsgo --noEmit -p .` → no output, exit 0
- `node tests/workflows/crossed_build_check_harness.mjs` → `all passed`

The two Round 20 files on their own: `bun test test/round20-deadline.test.ts test/round20-criteria.test.ts` →
`Ran 27 tests across 2 files. [2.60s]` (27 pass, 0 fail).

## CONTRADICTS

None.

Notes, not contradictions: the SPEC does not say what `end`/`wait` do with an id or a run that names an *ended* deadline
(DL1 only defines `status`), so they answer like `status` does — `<id> ended <time>`, exit 0, nothing written. C17 is
test-side only (the tests' own fake `ps`), so no source change was needed for it; those tests pass.