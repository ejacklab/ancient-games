# Brief — review-lessons (read-only)

Review the change "agent lessons, delivered by the guard" in this repository (the current folder is its root). Do not
change any file; your final message is the review.

The change: `git diff 00a81fc..402adb7` (`.claude/skills/agent-lessons/`, `.claude/skills/workflow-design/guard/`
code, tests, `SPEC.md` section "Round 18", `tools/export_skills.py`). The owner's decision: a lesson is filed for one
agent type or all agents and travels to every project; project facts stay in a `LESSONS.md` beside the code; the
guard gives the main agent the matching ones before a Write/Edit/MultiEdit (by path) or a Bash call (by command
word), each once per session, by holding the call once (L6).

## Lessons (from `lessons for --agent codex --kinds code-edit,test`)
- When a change sends new cases into an existing code path, list that path's early returns and exemptions first, and
  add one test per exemption fed one of the new cases.

Find defects: a call that should get a lesson and does not, or gets one it should not; a hold that repeats (the retry
held again, a loop), including when the session id is missing or the shown file is unreadable; a hold on a call the
guard would also deny for another reason; matching (`isTestFile`, the globs relative to the git root, a path outside
the root, Windows separators); front-matter parsing (`Bun.YAML`, quotes, an empty list, CRLF); the facts' `LESSONS.md`
line format; the CLI's usage errors; the export of the skill; a test that passes against wrong code; SPEC text that
says what the code does not do. Return `status: done`, then a heading `Findings` with one numbered finding per defect —
severity, file:line, what is wrong, the input that shows it, the fix — and "Checked and found nothing" for each area
that is clean.
