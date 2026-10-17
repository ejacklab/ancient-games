# Brief — tests-lessons

You work in the repository root. Do not change any file outside the ones named under Limits. Do not commit.

## Task
Write acceptance tests in `.claude/skills/workflow-design/guard/test/round18-crossed.test.ts` for the guard's agent
lessons as `.claude/skills/workflow-design/guard/SPEC.md` section "Round 18" states them (L1–L6 and its Fails-if
line). Import from `src/lessons.ts` (`parseLesson`, `readLessons`, `checkLessons`, `factsFor`, `isTestFile`,
`matches`, `lessonsFor`, `takeUnshown`) and `src/hooks.ts` (`handleHook`, `LESSON_HOLD`). Feed the hook `PreToolUse`
payloads for Write, Edit, MultiEdit and Bash with an env whose `lessons` field names a temporary store folder you
write lesson files into. Run the CLI (`src/cli.ts lessons for|check ... --dir <store>`) with `spawnSync`. Read
`test/round4.test.ts` only for how a temporary git root and a payload are set up; do not open
`test/round18-lessons.test.ts`.

## Lessons (from `lessons for --agent opencode --kinds test,brief`)
- Each fact in a question or brief for another agent carries its own label and the file:line or command that checked
  it; a fact with neither is marked recall. One "verified" label over a block of facts hides a recalled one.
- When a change sends new cases into an existing code path, list that path's early returns and exemptions first, and
  add one test per exemption fed one of the new cases. (Here: `handlePreToolUse` sends Write/Edit/MultiEdit calls,
  which it used to return quiet for, into the lessons path; and Bash calls that pass every lint now reach it. Its
  early returns are: a tool other than Bash/Write/Edit/MultiEdit; no `lessons` in the env; a Write with no
  `file_path`; a Bash call the lint, the read-missing hold or the inline-script hold denies — source:
  `src/hooks.ts`, `lessonLines` and `handlePreToolUse`.)

## Pieces and progress (first)
Divide the work into small pieces. Before starting, append one `planned` line per piece to
`runs/20261017-agent-lessons/nodes/tests-lessons.progress.md`, then a line as each starts and ends:
`- <ISO time from date -Iseconds> · <piece-id> · <planned|start|done|fail> · <short note>` (the piece id is one word).

## Standard
- Cover each L item and each Fails-if clause at least once, and each early return above with one case.
- Assert exact outputs where the SPEC gives them (the `lessons for` line forms, the hold's first line, exit codes).
- `cd .claude/skills/workflow-design/guard && bun test test/round18-crossed.test.ts` — report the counts.

## Limits
May change: that test file, the progress file, and `runs/20261017-agent-lessons/nodes/tests-lessons.result.md` only.
No other AI engine. Foreground commands only.

## Result
`runs/20261017-agent-lessons/nodes/tests-lessons.result.md`: `status: done|partial|fail`, one sentence; the test file;
the command and its last lines; CONTRADICTS (with the SPEC line) or none.
