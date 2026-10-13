# INDEX.md changes to the design (claude)

Reader: Claude `claude-opus-5-5`, 2026-10-13. Read: `SOURCE_OF_TRUTH.md` (whole), its vision, `docs/index-md/`
(REQUIREMENTS, DESIGN, VISION, BACKLOG), `tools/memory_index.py`, `.githooks/`, the test names. I did not read the
other readers' reviews. Two claims below rest on runs I made in a scratch repo outside the project (commands in
"What could go wrong" and in section 5). I changed no project file.

Labels: *EJ's* = his words; *design* = already in `SOURCE_OF_TRUTH.md`; *proposed* = mine.

## 1. K6.2 and When to write

**Recommend** *(proposed)*: make it as proposed. Also take the `INDEX.md` clause out of the "Immediately" row and
put it in one line under the table, because lessons and observations are written at the end of a task, not
immediately, and they change `INDEX.md` too.

**Reason** *(design)*: Rd1.2, *"With no network, no cache and no private agent store, a fresh clone can read
`INDEX.md` and every entry."* A clone gets only commits. So an entry committed without its `INDEX.md` line is missing
from what Rd2.1 loads at session start, whatever its kind. K6.2's own reason, *"so the next session sees it"*, holds
for every kind, not only decisions and facts.

**Text:**
- "When to write" table, row **Immediately**: "Decisions and facts, before the code. A human correction. The state of
  unfinished work before a handoff, an interruption or a context reduction." *(design, with the `INDEX.md` clause
  removed: proposed)*
- New line under the table: "Whenever an entry is created or changed, at any of these times (any kind, any status
  change), `INDEX.md` is regenerated and committed in the same commit as the entry (K6.2)." *(proposed)*
- **K6.2**: "Whenever an entry is created or changed (any kind, any status change), `INDEX.md` is regenerated and
  committed in the same commit as the entry, so the next session, on any clone, sees it." *(proposed; "so the next
  session sees it" is design)*
- K6 **Open** is replaced by: "**Tool:** `tools/memory_index.py` builds it. Its `--check [<rev>]` compares the
  `INDEX.md` in the staging area, or in a commit, with what it builds from the entries there. Whoever changes the
  entry runs it (K6.2). Requirements and design: `docs/index-md/`." *(proposed)*
- **K6 Fails if**: "**Fails if** a commit's `INDEX.md` differs from what the tool builds from that commit's entries
  (`--check <commit>` fails), or it lists a superseded or retired entry as active." *(design, widened from
  "regenerating changes it" to every commit: proposed)*. Every commit includes the entry commits (K6.2), hand edits
  (K6.1) and merges (K6.3).
- **"Still open"** line: "**Still open:** who resolves a git merge conflict in an entry file (W6). Whether a changed
  decision is edited in place or superseded is proposed in K4.3." *(proposed; the K4.3 sentence is design)*

## 2. K6.3, never hand-merge

**Recommend** *(proposed)*: make it as proposed, and add "with no conflict markers left in the entries". The tool
does not catch markers: I ran it and it indexed one (see "What could go wrong").

**Reason** *(design)*: K6.1, *"It is never edited by hand."* Resolving a conflict in `INDEX.md` by hand is a hand
edit. The INDEX.md vision says the same: *"a conflict is resolved by rerunning it"* (`docs/index-md/VISION.md`).

**Text:**
- **K6.3** (new): "`INDEX.md` is never merged by hand. When a merge conflicts, resolve the entry files first, with no
  conflict markers left in them, then regenerate `INDEX.md` and commit it with them." *(proposed)*
- **K6 Fails if** (section 1's text) gets this addition: "…, or an entry or `INDEX.md` holds a git conflict-marker line
  (`<<<<<<<` or `>>>>>>>`)." *(proposed)*. Today this half is judged by a reader, because the tool does not check
  for markers.
- **W6 Open**: "**Open:** who resolves a merge conflict in an entry file. A conflict in `INDEX.md` is not resolved by
  hand (K6.3)." *(proposed: K6.3 narrows the open question. It does not answer who resolves a conflict in an entry.)*
- W6 **Fails if** stays as it is *(design)*.

## 3. Rd3.1, who checks the size

**Recommend** *(proposed)*: make it differently. Say which check covers the size (the K6 check), and not which
program runs it, so that the design names the tool once, in K6.

**Reason** *(design of the tool)*: C1.2 says the check *"passes (exit 0) only when the entries are valid, the bytes
are equal, and the size is within the limits"*. The size is already part of the one check K6 relies on. If Rd3.1
also says "the script" and "the tests", the design names the tool in two places.

A fact, not a reason for the choice: in this repo nothing runs that check on its own. `git config --get
core.hooksPath` printed nothing (I ran it), so the hook is off, and there is no CI. BACKLOG item 3 also notes that
the real-repo test *"checks nothing yet"* until `project-memory/` exists. "The tests run the check" is true only when
someone runs `pytest`.

**Text:**
- **Rd3.1**: "`INDEX.md` fits the strictest start-file limit among the agents that work on the project. The check
  that keeps it in step with its entries (K6) also fails when it does not fit. *Example*, from `CACHES.md`: about
  24 KB and 200 lines when Claude Code, Qwen and agy share a project." *(first and last sentences design; middle
  sentence proposed)*
- **Rd3 Fails if**: "**Fails if** `INDEX.md` exceeds that strictest limit, or the K6 check passes an `INDEX.md` that
  exceeds it." *(design, extended: proposed)*
- The line before "Core requirements": "`INDEX.md` must fit the strictest start-file limit of the agents that read it,
  and the check that keeps it in step fails when it does not (Rd3, K6)." *(proposed)*

## 4. W1.1, the id

**Recommend** *(proposed)*: make it as proposed and leave the form open until EJ picks it (Question 1).

**Reason** *(design)*: W6.2, *"Each agent works on its own branch or worktree"*. Branches create entries without
seeing each other, so two branches would hand out the same "next free number". The tool rejects duplicate ids
(REQUIREMENTS B2.3). The clash would then block the merge commit, and fixing it means renaming an id that
`depends_on` or `supersedes` links may already cite.

**Text:**
- **W1.1**, add after the first sentence: "The `id` is unique without coordination between branches: two branches that
  each create an entry never produce the same id. It is never 'the next free number'. Its form is open (EJ)."
  *(proposed; the form is EJ's to choose)*
- **W1 Fails if**, add: "It also fails if two entries share an `id`, or the id's form lets two branches, working
  apart, create the same one (judged)." *(proposed)*

## 5. W1.2 and W1.3, the format

**Recommend** *(proposed)*: make it. Give the header format once in W1.2 and the section spellings in W1.3. Present
it as the format every writer produces and the lint reads, not as the script's detail.

**Reason** *(design)*: the W1 check is *"a lint over `entries/` finds a missing field or section"*. A lint can find a
missing field or section only if the format and the spellings are fixed. The tool already reads this format
(REQUIREMENTS B2.1, B2.2), so the design and the tool would agree.

**Text:**
- **W1.2**: "The header starts on the file's first line, which is exactly `---`, and ends at the next line that is
  exactly `---`. Each field is one `key: value` line. The keys are `id`, `kind`, `status`, `author`, `recorded` (the
  date recorded), `covers` (the code paths it is about), `source` (its source or evidence), `depends_on`,
  `supersedes`, `superseded_by` and `changed`. A field with several values (`changed`, `covers` and the links) holds
  them on indented lines below its key. A decision to build something, once its work is complete, also holds `done`
  (W5.3)." *(the field list is design; the delimiters, the `key: value` form, the indented lines and the two key
  names `recorded` and `source` are proposed. See Question 2.)*
- **W1.3**: "The body follows the header: the claim in one or two sentences, then a line starting with `**Why:**`,
  then a line starting with `**How to apply:**`. There is one claim per entry." *(design, with the exact spellings
  fixed: proposed)*
- **W1 Fails if**: "**Fails if** a lint over `entries/` finds a header that is not between two `---` lines, a missing
  field or section, a section not spelled as in W1.3, or a file whose prefix is not one of the five or does not match
  its `kind`. It also fails if a reviewer finds two claims in one entry, or git shows an entry file renamed to a
  different prefix." *(design, with the format clause added: proposed)*. Add section 4's id sentence to this.

**A mismatch found while reading** (reported under Rd5.3 and not settled here): the merged tool still accepts the
runbook kind, which item 8 removed. `tools/memory_index.py` has `ENTRY_NAME = re.compile(r"[DFLROH]-[^/]+\.md")` and
`"R": "runbook"` in `PREFIX_KIND`. In a scratch repo, an `R-x1-deploy.md` entry with `kind: runbook` was indexed and
the tool exited 0. The design's W1.1 (*"There is no runbook prefix"*) and REQUIREMENTS B1.1 (`^[DFLOH]`) both
exclude it. EJ decides whether the tool is fixed. Either way, the tool is not yet a complete lint for W1.

## What could go wrong

**Verified in a scratch repo:** someone regenerates while an entry still has conflict markers, and both modes pass.

- Two branches each change the claim of `D-20261013-a-utc.md` and run the tool. The merge conflicts in the entry and
  in `INDEX.md`.
- Running `python3 tools/memory_index.py` before resolving the entry exits 0.
- After `git add -A`, `--check` also exits 0 (*"up to date"*).
- `INDEX.md` now reads:
  `- [20261013-a](entries/D-20261013-a-utc.md) decision: <<<<<<< HEAD Use UTC in logs. ======= Use UTC everywhere. >>>>>>> b1`

Every later session loads that line at start (Rd2.1), and no check catches it. K6.3's "no conflict markers left" and
its Fails-if clause (section 2) cover this in the design. Whether the tool should also reject markers is a separate
build decision for EJ.

## Questions for EJ

1. **The form of an entry id** (W1.1, section 4): a date, a hash, a random suffix, or something else? Your answer
   replaces "Its form is open (EJ)" with the form itself.
2. **The two header keys the design does not spell** (W1.2, section 5): may the date recorded be `recorded:` and the
   source or evidence be `source:`? If not, W1.2 uses your names.
