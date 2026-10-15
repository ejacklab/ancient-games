# Brief — r4-tests, attempt 1

You are working in a git worktree; the current folder is the repository root. Work only inside it.

## Task

Write the acceptance tests for **Round 4** of the bun TypeScript package `.claude/skills/workflow-design/guard/` —
read the section "Round 4 — the agent's own failures" at the end of `.claude/skills/workflow-design/guard/SPEC.md`
(items D1–D5 and its Fails-if). Put them in a new file `.claude/skills/workflow-design/guard/test/round4.test.ts`.
The implementation does not have Round 4 yet; a different engine changes it afterwards to pass your tests. You may
read `src/` only to learn function names and signatures (`handleHook`, `HookEnv`), never to shape expectations.

## Standard

- Every D item and every Round 4 Fails-if line is pinned by a test with a planted payload, driven through
  `handleHook(payload, env)` with a temporary git repo as `env.cwd` (`fs.mkdtempSync(path.join(os.tmpdir(), "hg-"))`,
  `git init`), and checked through the journal (`readJournal` from `src/journal.ts`) and the hook's output.
- Payload shapes to use (verified on Claude Code 2.1.300): PostToolUseFailure `{hook_event_name, session_id, cwd,
  tool_name: "Bash", tool_input: {command}, error: "Exit code 1\n<output>", is_interrupt: false}`; PostToolUse
  `{…, tool_response: {stdout, stderr, interrupted: false}}`.
- Plant `SECRET-PLANT-7f3a9c` in test output text and assert it never reaches the journal, evidence or hook output.
- bun pitfall: in `test.each` tables wrap each element in its own array (`[[x]]`), or bun takes the callback's
  parameter as a `done` callback and times out.
- Run `cd .claude/skills/workflow-design/guard && bun test test/round4.test.ts` and
  `./node_modules/.bin/tsgo --noEmit -p .`; many new tests should fail now — report which.
- Change no other file. Do not commit. Do not start any other AI engine.

## Write the result to

`runs/20261015-long-session/nodes/r4-tests-1.result.md` (write `.tmp` first, then rename), header:
`---` node: r4-tests · attempt: 1 · engine: codex · model · status · started · ended · evidence:
runs/20261015-long-session/nodes/r4-tests-1.evidence.txt `---`, then: one sentence; files written; the check
commands and counts; tests failing now; CONTRADICTS (each, or none).
