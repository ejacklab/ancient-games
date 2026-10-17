# Answer — Approve or change the COO-written requirement wording

## Answer
CHANGE. Six changes. The other records and the K5.2 `who_decides` value stand. I was not shown W1.2b's text, so I cannot judge it.

1. **K5.1 text.**
   - Current: *"Both hold raw notes, one file per agent session, appended to and never edited."*
   - New: *"Both hold raw notes, one file per agent session, appended to; a line already written is never changed or removed."*
2. **K5.1 `fails_if`.**
   - Current: *"a journal file is edited after it is written, or raw notes are kept elsewhere, with no written reason."*
   - New: *"a line already written in a journal file is changed or removed, or raw notes are kept elsewhere, with no written reason."*
3. **K1.1 `who_decides`.**
   - Current: *"the project's workflow: when work goes the other way"*
   - New: *"the project owner, through the project's workflow: when work goes the other way"*
4. **W5.2 `fails_if`.**
   - Current: *"a task ends with what it learned unwritten, with no written reason."*
   - New: *"a task ends with no lesson, observation or hypothesis written, and no written reason for none."*
5. **W6.1a text.**
   - Current: *"Agents never append to one shared file."*
   - New: *"Agents never append an entry to a file that already holds one."*
6. **W1.2a `fails_if`.**
   - Current: *"a header is not between two `---` lines."*
   - New: *"the file's first line is not exactly `---`, or no later line is exactly `---`."*

## Why
- K5.1 says "appended to" and "edited" for the same act. A `check: git` can only test whether a line already written was changed or removed.
- A workflow is a document and cannot decide, so K1.1 must name a person.
- W5.2's old `fails_if` can be judged only by someone who knows what the agent learned. The new words test what a reviewer can see: something was written, or a reason was.
- W6.1a is a MUST whose text is broader than its `fails_if`. A hand-appended `INDEX.md` or a shared `state.md` would break it literally.
- W1.2a's old `fails_if` passes a header that starts on line 3, which the text forbids, and the tool will implement the `fails_if`.

## What I need to know
- Do agents append to `INDEX.md` or to a shared `state.md` by hand? If `INDEX.md` is generated and no two agents write the same `state.md`, change 5 is not needed.
- What is the "other" in W5.2's "other lessons"? If it points at an earlier W5 record, the W5.2 text stands.
- Rd5.2: I approve it as written. Dave suggested labelling its check "only on audit". Does the `check` vocabulary have such a value? If it does, apply it. Also, which texts count as "standing instructions"? I was not told (`AGENTS.md`, the task brief, or both).
- Rd1.1 puts `AGENTS.md` at the repo root but does not say where `project-memory/` lives. Is it at the root too? If not, Rd1.1 needs the path.
