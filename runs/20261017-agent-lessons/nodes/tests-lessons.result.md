status: done — 40 acceptance tests for Round 18's L1–L6, every Fails-if clause and each early return of `handlePreToolUse` all pass.

## The test file

`.claude/skills/workflow-design/guard/test/round18-crossed.test.ts` — a temporary git root (`guardRoot`) and a temporary
lessons store per test; 7 lesson fixtures (test kind, code-edit kind, a command word, a brief kind, a path glob, another
agent's lesson, one with `enforced_by`), two `LESSONS.md` folders, and PreToolUse payloads for Write, Edit, MultiEdit and
Bash fed to `handleHook` with `env.lessons` pointing at the store. The CLI (`lessons for|check`) is run with `spawnSync`.

Coverage:

| item | cases |
|---|---|
| L1 lesson file | valid parse with every key; `paths`/`commands`/`enforced_by` default empty; 10 broken shapes each reported with its reason; `readLessons` skips an invalid file and `checkLessons` names it; a store that is not there reads empty |
| L2 project fact | only the lines naming that file in that folder; prose lines ignored; the same file name in another folder gets that folder's fact, not this one's |
| L3 which match | `isTestFile` over 11 forms; `all` / the agent / another agent; test file → test lesson, other file → code-edit lesson; path glob matched from the git root (relative and absolute); command word; kind given; `enforced_by` pointer line |
| L4 CLI | `- <text> (<slug>)` and `- <file>: <fact>` exactly, exit 0; the kind, command and path filters; nothing matched prints nothing; unknown agent, `all`, unknown kind and a missing `--agent` all exit 2; `lessons check` exits 0 with `lessons ok: N in <store>` or exits 1 listing `<file>: <reason>` |
| L5 hook | Write, Edit and MultiEdit matched by `file_path` with that file's facts; a test file gets the test lesson only; Bash matched by the command words of its segments; a second call in the session gets only what it has not been given; another session is given them again; `lessons-shown.json` holds `{session: [keys]}`; a hook with no store in its env is quiet for Write, Edit and Bash |
| L6 hold | first line exactly `LESSON_HOLD`, `permissionDecision: "deny"`, exit 0; lessons and facts in one hold; the retry runs quiet; a hold writes no journal record |
| Fails-if (SPEC 848–850) | a non-matching lesson is not given and a matching one is; the retry is not held again; nothing is given twice in one session; no store gives nothing; an invalid lesson file does not break the hook or `lessons check`; a fact never reaches another file's name or folder; `lessons for` with an unknown agent exits 2 |
| early returns of `handlePreToolUse` | Read/Grep/Task/TodoWrite quiet; Write/Edit/MultiEdit with no `file_path` quiet; Bash with no command quiet; a lint deny (`trap:codex-stdin`), a `read-missing` hold and an `inline-script` hold each get that reason alone, and the lessons wait for the next clean call |

Exact outputs are asserted where the SPEC gives them: the two `lessons for` line forms, the `LESSON_HOLD` first line, the
single-line deny reasons of the three other holds, and the exit codes 0 / 1 / 2.

## The command

`cd .claude/skills/workflow-design/guard && bun test test/round18-crossed.test.ts`

```
 40 pass
 0 fail
 196 expect() calls
Ran 40 tests across 1 file. [371.00ms]
```

`bunx tsc --noEmit -p tsconfig.json` is clean. The whole guard suite (`bun test`) gives 1445 pass / 3 fail; the three
failures are C17 in `test/round3.test.ts`, which fail the same way without this file (they read other processes' command
lines on this machine).

## CONTRADICTS

none. Two points where the SPEC is silent and the tests pin the implementation's reading, both consistent with the SPEC's
own words: L3 matches a path given by glob **or** by kind, so a `code-edit` lesson matches any non-test file whether or
not its glob hits (`SPEC.md:826–829`), and `lessons for` prints the lessons of the store sorted by file name before the
project facts (`SPEC.md:831–833`).