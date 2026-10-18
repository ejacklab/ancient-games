# Dave — approve or change the COO's wording in the memory requirements

## Answer
CHANGE. Six records change. K5.2's `who_decides`, Rd1.1 and W1.2b stay as written.

1. **K5.1**
   - Text. Current: "appended to and never edited." New: "appended to; a line once written is never changed or removed."
   - `fails_if`. Current: "a journal file is edited after it is written, or raw notes are kept elsewhere, with no written reason." New: "a commit changes or removes a line already written in a journal file, or raw notes are kept elsewhere, with no written reason."
   - `check`. Current: "git". New: "git; reviewer". Git can see changed lines. Only a person reading can see notes kept somewhere else.
   - Cost: fixing a typo in a journal now needs a written reason.
2. **W1.2a** `fails_if`. Current: "a header is not between two `---` lines." New: "the file's first line is not exactly `---`, or no later line is exactly `---`." Cost: a file with a blank line or a BOM before the header now fails the tool. The record's text already says it should.
3. **W5.2** `fails_if`. Current: "a task ends with what it learned unwritten, with no written reason." New: "a task ends with no lessons, observations or hypotheses written from it and no reason in its `state.md`; a written 'nothing new' is a reason." Cost: this checks that the step was done, not how good it was. A lazy "nothing new" will pass.
4. **W6.1a** text. Current: "Agents never append to one shared file." New: "Agents never add an entry to a file that already exists." Cost: the sentence may also have been meant to stop agents appending to any shared file, to avoid merge conflicts. If so, the new words drop that, and it needs its own record.
5. **Rd5.2** `check`. Current: "reviewer". New: "reviewer, on audit of the session's journal; test: a planted entry that contradicts a standing instruction is shown to be read, and is not followed". Cost: the test needs a fixture and one run per engine, and each run is n=1. Until the test exists, this MUST is audited, not gated, and the record now says so.
6. **K1.1** `who_decides`. Current: "the project's workflow: when work goes the other way". New: "the project owner, through the project's workflow: when work goes the other way". Cost: none. If the workflow already names a role that decides, name that role instead.

## Why
- K5.1 and W1.2a: each `fails_if` must trip on the fault and only on it. K5.1's trips on every correct append, because git shows an append as a change to the file. W1.2a's lets through a header that does not start on line 1. One git diff and one test file settle both, which is cheaper than arguing (my #2).
- W5.2 and Rd5.2: a check has to be something its checker can see. Only the agent knows what it learned, so I rewrote W5.2 to ask for something written or a reason, and a null result counts as a result (my #9). For Rd5.2 I said what a reviewer's audit does not show (my #5). The test needs a control: first show that the planted entry was actually read (my #4).
- W6.1a: the MUST's text is wider than its `fails_if`. A reviewer could fail work that the gate itself does not test (my reading).
- K1.1: a document cannot decide; a person decides through it (my reading).
- How sure I am: the K5.1, W5.2, Rd5.2 and K1.1 points repeat my 2026-10-15 answer. That is the same rules applied twice, not independent confirmation. Each point is n=1, and no record has been tried on a real journal or entry (my #10).

## What I need to know
- Do agents write `INDEX.md`, adding a line for each entry, or does a tool generate it? If a tool generates it, W6.1a's current sentence is true as written and change 4 becomes optional. If agents write it, the current sentence breaks Rd1.1's own layout.
- Does the YAML's `check` field allow values other than reviewer, git and tool? If not, Rd5.2's `check` becomes "reviewer", the "on audit" note goes beside it, and the test drops out.
- Does an extra folder under `project-memory/` count as "laid out otherwise" in Rd1.1? I approved it reading "otherwise" as "a listed path is missing or moved". If extra folders should fail too, the `fails_if` has to say so.
- Does K5.2 already log every journal read? If it does, W5.2's check could point at that log line instead of the reviewer.

## How I decided
- `runs/20261016-four-experts-what-counts-as-change/insight.md#F-8243a18f`: a criterion copied from habit that could never be met as written. K5.1's `fails_if` has the same flaw (every correct append trips it), so I changed it rather than leave it to a written reason.
- `…#F-336edcb0`: a criterion must be something its checker can mark within the task. This made me rewrite W5.2 into something visible and label Rd5.2 as audit plus test.
- `…#F-0f2fa841`: a plant has to be shown to work before the result is trusted. That is why the Rd5.2 test first proves the planted entry was read.
- `…#F-d8221199`: a check that reads a different thing than it means to. W6.1a's text against its `fails_if`, and K5.1's git check covering only half its `fails_if`, are the same gap.
- No category was named. I chose `check`, which fit. The `instruction` and `tool` insights are about engines and shells and do not apply.
