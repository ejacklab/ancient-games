status: done

Snapshot: HEAD `d483d26` (clock code from `07b67a9`, SPEC and install matchers from `d483d26`). At HEAD: 1325 tests pass, 0 fail; `tsgo` clean. No file was changed. Line numbers below are HEAD.

1. **[medium] The clock after a file write is untested; a build that clocks only Bash passes the whole suite.**  
   `test/round10-deadline.test.ts:32-35` — the `post` helper always sets `tool_name: "Bash"`; `:242-254` varies only the event, never the tool. `test/cli.test.ts:121` checks the installed matcher, not that `withTime` emits for a write.  
   **Wrong code that passes:** insert `if (payload.tool_name !== "Bash") return result;` after `src/hooks.ts:815`. `bun test` → 1325 pass, 0 fail. A `PostToolUse` `Write`/`Edit`/`MultiEdit` then gets no clock, contrary to the owner’s “after every … file-write call.”  
   **Fix:** add cases for `Write`, `Edit` and `MultiEdit` before and after the deadline with `tool_input.file_path`, assert exactly one clock/time-up line, and add a `Read` case expecting no line to pin the matcher scope.

2. **[medium] A valid pre-change deadline file with `marks` is never tested; a build that rejects it passes the whole suite.**  
   `src/deadline.ts:34-42` — `isDeadline` no longer looks at `marks`. The only test files containing `marks` are `test/round10-deadline.test.ts:379-387`, and both are invalid for other reasons (bad id / filename), so they do not exercise compatibility.  
   **Wrong code that passes:** add `&& !("marks" in d)` to `isDeadline`. `bun test` → 1325 pass, 0 fail. Every deadline written before `07b67a9` would silently stop counting and its clock/time-up would disappear.  
   **Fix:** plant a valid old file, e.g. `{"id":"D-00000001","start":"<ISO>","minutes":10,"run":null,"marks":[50,80,100],"session":"s"}`, and assert `deadlineStatus` returns it and a hook at 6/10 min yields `harness-guard clock: 6/10 min (60%), 4 left`. (Current code does handle this — verified — so this is a regression guard, not a live break.)

3. **[low] The clock can say all minutes are used while time is left.**  
   `src/deadline.ts:148` uses `Math.round` for `usedMinutes`; `src/hooks.ts:823` puts it in the every-call clock. With a 10-minute deadline at 9.5 minutes the line is `harness-guard clock: 10/10 min (95%), 1 left`; at 9.99 minutes, `10/10 min (99%), 1 left`. The `deadline status` line (`src/deadline.ts:154`) shows the same contradiction.  
   **Fix:** use `Math.floor` for `usedMinutes` (verified: passes the current suite), or clamp it to `< minutes` while `up` is false; add a test at 9.5/9.9 asserting `used < minutes` while `left > 0`.

4. **[low] The test named “no marks recorded” checks only the 50% id.**  
   `test/round10-deadline.test.ts:268-274` asserts only `deadline:D-00000001:50` is absent. A `raised` record for `:80` or `:100` passes, and the test runs at 60%, so it never reaches 80/100.  
   **Wrong code that passes:** append a `raised` record with id `deadline:<id>:80` at 60%. `bun test` → 1325 pass, 0 fail (the sibling untracked `round10-clock-only.test.ts` does catch it).  
   **Fix:** assert no raised id matching `^deadline:D-[0-9a-f]{8}:` except `deadline-ask`, or no `raised` record for this session containing any `deadline:` mark id, and exercise 50/80/100.

5. **[low] `deadline start --marks` is silently accepted, though SPEC T1 says usage error (2) on anything else.**  
   `src/cli.ts:198-205` ignores unrecognized flags; `SPEC.md:542-545` says the removed shape is `{ id, start, minutes, run, session }` and errors on anything else.  
   **Input:** `bun .claude/skills/workflow-design/guard/src/cli.ts deadline start --minutes 10 --marks 50,80,100` → exit 0, prints `D-…: 10 min, deadline …`, writes a deadline with no `marks` field. A caller using the old interface gets no signal that the flag was dropped.  
   **Fix:** reject `--marks` (and ideally any unknown `--flag`) with `usageError("deadline start: --marks was removed with the percent marks")`, exit 2; add a CLI test. The in-flight `wait --mark` change uses the same pattern.

6. **[low] SPEC says a mention of `deadline start` claims nothing, but a quoted full path does claim.**  
   `src/hooks.ts:809-811` tests `/\/src\/cli\.ts\s+deadline\s+start\b/` over each segment’s text; `SPEC.md:580-582` says “not a mention.”  
   **Input:** a successful `PostToolUse` Bash call with command `echo "bun x/src/cli.ts deadline start --minutes 5"` and an unclaimed `D-00000001` → the file’s `session` becomes `"s"`, and later calls get a clock/time-up for a deadline never started (verified). The test at `test/round10-deadline.test.ts:355-365` uses `echo "deadline start"` without the guard path, so it passes.  
   **Fix:** decide from the segment’s command word and arguments (the guard CLI itself), not a substring regex over the segment text; add a test with the quoted full path and with `false && …`. This is pre-existing, not introduced by `07b67a9`, but the reviewed SPEC still asserts it.

**Checked and found nothing**

- **Code that still produces or records a mark:** no `raised` mark id, no `deadline:<id>:<mark>` record, no `marks` field written by `startDeadline`; `dueMark`, `markId`, `parseMarks` and `DEFAULT_MARKS` are gone. `deadline wait --mark` is a timer the agent starts and writes no record, not a reminder; the working tree’s uncommitted mark-q change removes it, but that is a separate decision, not a defect of this change.
- **A path where the clock is missing before the deadline:** for every `PostToolUse`/`PostToolUseFailure` the installed matcher actually delivers with a live session deadline, `withTime` adds one clock or time-up line; no/ended/other-session deadlines are correctly silent. Caveat, not counted: `src/install.ts:31` watches `PostToolUseFailure` for Bash only, so a failed file write would not be clocked on a harness that emits that event; `SPEC.md:334` records that a failed Edit fired no hook at all in Claude Code, and this is unverified for Codex/Qwen. If such a harness is found, add `Write|Edit|MultiEdit` to that matcher.
- **A deadline file written before the change that now breaks:** none. `isDeadline` ignores the extra `marks` field; a planted old file produced the clock at 6/10 min and `deadline status` read it normally. The missing regression test is finding 2, not a live failure.
- **The rest of the SPEC:** T1’s file shape, T5’s clock/time-up wording, “no raised mark record,” and the installed matchers otherwise agree with the code; the exceptions are findings 5 and 6.
