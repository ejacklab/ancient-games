# Answer — deliver a lesson with the edit's result, or hold the first edit?

## Answer
Use context and never hold. Return `additionalContext` for a matching Write/Edit/MultiEdit and also for the Read that comes before it, so the lesson normally arrives before the first edit without a denied call. Keep "hold once" as a per-lesson fallback, used only if the planted-repeat test shows a lesson still fails to stop its mistake.

## How I decided
1. **Option A cannot deliver before the first edit.** The hooks reference says `additionalContext` is added "alongside the tool result", and "before the tool runs" is "not found in docs". My reasoning, not a documented fact: the model is not called again between the hook and the tool, so context can reach it only with the result.
   - Under A the first match of a lesson therefore arrives after the edit it was meant to guide.
   - Section 3 of the plan says "before the edit runs". That is wrong for context-only delivery and should be reworded.
2. **Once per session makes the first match the one that matters.** If the lesson arrives late on that match, it never arrives early in that session.
3. **Option B is the only way to get a lesson in before a Write/Edit.** Deny with a reason is a mechanism already in use: `guard/src/hooks.ts:106-128` denies Bash calls and the agent reads the reason and retries.
   - B's cost is certain. Every first match burns a turn and re-sends the Write or Edit, including when the agent was already doing it right.
   - Those blocked-but-correct calls are noise, which is the opposite of the owner's aim.
   - B also changes the plan's piece 4, which says "no deny, context only".
4. **Option C: deliver one step earlier, by context.**
   - An edit to an existing file normally follows a Read of it (*recall*: Claude Code refuses an Edit on a file not yet read).
   - A Read of a matching path, or of a neighbouring test file, is a call whose result carries the lesson. The lesson is then in context before the edit and costs no denied call.
   - It adds `Read` to the matcher and to the tool-name set. Today `handlePreToolUse` returns quiet for anything that is not Bash (`hooks.ts:106`), so Write/Edit are new code either way.
   - The edit-time context stays as a backstop. It covers a Write to a new file, and it repairs late if the lesson was missed.
5. **Nothing can be tested live now** (R12.3), so I picked the option that costs least if wrong. C builds on the plan's context-only piece, is a small extension of it, and can be switched to B per lesson by adding a hold flag.

## What I need to know
- Does a PreToolUse `additionalContext` on Write/Edit/Read reach the model at all, and in which turn? This is plan piece 1, still unverified. If it does not reach the model, A and C fall back to B.
- Does the Claude Code version in use really require a Read before an Edit or an overwriting Write (*recall*)? If not, Read-time delivery misses some edits.
- Do a subagent's tool calls fire this hook under the same `session_id` (*recall*)? If so, a subagent could use up the "once per session" flag before the main agent sees the lesson.
- Is any lesson about a mistake that cannot be cheaply undone, such as a Write over an uncommitted file? Those few should be held (B); the others should not.

## Costs and risks
- **Late arrival is still possible.** A Write to a new file with no preceding Read gets the lesson only after the edit. The agent may read it as information and leave the edit in place. The lesson text should name the edit just made and what to check.
- **More shown-but-not-applied lessons.** Reads are far more frequent than edits, so a Read matcher shows some lessons on files that are never edited. Each lesson still appears once per session, so the extra noise is bounded. It is also one more hook run per Read, which adds latency.
- **The owner must change a setting.** The matcher moves from `Write|Edit|MultiEdit` to include `Read`, and R12.3 makes that the owner's decision. Until they do, nothing is live.
- **No delivery record exists yet.** Neither option leaves a journal record of a lesson shown, and the denied path records nothing at all. The noise comparison needs a "lesson shown (id, session)" record in any case.
- **Compaction.** A lesson shown once and then compacted away is not shown again. This applies to every option.

## How we would know I was right
1. **Timing check.** After the owner installs the matcher, plant a lesson with a unique token on a throwaway path. Do a Read, then an Edit. In the session transcript, check where the token appears relative to the Read's result and the Edit's call. Delivery before the Edit proves C works. Delivery only after the Edit proves the Read-time part failed.
2. **Planted repeat (plan §5).** Replay a call that failed before, once with the lesson filed and once as a control with none.
   - C was wrong if the first edit repeats the mistake as often as the control does.
   - Then switch those lessons to B and run the same replay. If B stops the repeat, hold those lessons.
3. **Cost and noise, reported without a threshold.** Per session, count B's retries and re-sent tokens against A's repair edits. Count lessons shown against lessons the transcript shows were applied. Reads that show a lesson and are never followed by an edit of that kind count against C.

**Choice:** Option C: context only, never a hold, delivered at the Read before an edit and again at the edit itself, with hold-once as a per-lesson fallback if the planted-repeat shows context did not prevent the mistake.
