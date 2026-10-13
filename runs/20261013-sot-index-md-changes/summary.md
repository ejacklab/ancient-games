# Summary — readers on the INDEX.md-implied design changes

COO (Claude `claude-opus-5-5`), 2026-10-13. Four reports: `reviews/claude.md`, `reviews/codex.md`,
`reviews/opencode.md`, `reviews/agy.md`. **agy ran on `gemini-3.8-flash-high`**, not the usual `gemini-3.1-pro-high`,
which agy no longer offers (first attempt failed: `reviews/` stderr kept in state.md log).

## Where all four agree

1. **K6.2: any entry, same commit.** All four: make it. Three of four (claude, opencode, agy) also move the INDEX.md
   clause out of the "Immediately" row into one line under the table, because lessons and observations are written at
   task end and change the index too. K6's "Open: which tool" and the "Still open … (K6)" line go.
   - The check widens to every commit: *"a commit's `INDEX.md` differs from what the tool builds from that commit's
     entries"* (claude; opencode and agy say the same). This also covers the case agy and codex raise: an edit that
     leaves the index byte-identical needs no index diff.
2. **K6.3: never hand-merge.** All four: make it. Resolve the entries, then regenerate.
   - claude adds *"with no conflict markers left in the entries"*, from a verified run: the tool indexed a claim still
     holding `<<<<<<< … >>>>>>>` and both modes exited 0.
3. **Rd3.1: "the build" goes.** All four: this repo has no build step. They split on wording (see below).
4. **W1.1: id unique without coordination, never "the next free number".** All four: make it, form open for EJ.
   - opencode adds: the id never changes when the entry is edited (it is in the file name, and K4.3 proposes editing
     in place).
5. **W1.2 / W1.3: header between two `---` lines, `key: value` fields, sections spelled `**Why:**` and
   `**How to apply:**`.** All four: make it. Reason (claude): W1's check is a lint, which needs a fixed format.
   - claude proposes names for the two keys the design never spelled: `recorded:` and `source:`, and multi-value
     fields on indented lines. opencode prefers fixing the format only as far as the generator reads it.

## Where they split

- **Rd3.1, naming the tool.** codex, opencode, agy name `tools/memory_index.py` and the tests in Rd3.1. claude names
  the tool once, in K6, and Rd3.1 says *"the check that keeps it in step (K6) also fails when it does not fit"*.
  opencode asks the root question: may the design name repo scripts at all, given W3.6 (*"AGENTS.md names the
  project's scripts"*)?
- **W6's open question.** codex and agy answer it: whoever does the merge resolves entry conflicts. claude and
  opencode only narrow it: an `INDEX.md` conflict is settled by regenerating; who resolves an entry conflict stays
  open.

## Outside the design (the build session's files; not the COO's to edit)

- **The tool still accepts runbooks** (`[DFLROH]`, `"R": "runbook"`). claude verified in a scratch repo; opencode
  found the test that asserts it (`tests/test_memory_index.py:405`).
- **The tool passes conflict markers** (claude, verified).
- **Nothing runs the check automatically here** (claude): `core.hooksPath` unset, no CI, the repo test checks nothing
  until `project-memory/` exists (BACKLOG 3).
- **Size unit** (opencode): agy's limit may be 12,000 characters; the script counts bytes. Already open as B4.
