# INDEX.md generator — product vision

> **Status: draft, not accepted by EJ.** Written 2026-10-12 by the COO (Claude `claude-opus-5-5`) at EJ's request
> (*"you put the design, product video and requirements for this INDEX.md to a folder I use another claude code to
> build so we continue the requirements review here"*). Each line names its basis:
> - **[EJ]**: EJ's decision or words;
> - **[design]**: `docs/memory-system/SOURCE_OF_TRUTH.md`, accepted by EJ 2026-10-12;
> - **[run]**: the research run `runs/20261012-index-md-algorithm/`. Its three proposals agreed on the algorithm, and
>   three blind reviews returned ACCEPT WITH FIXES;
> - **[proposed]**: the COO's wording, which EJ has not said.
>
> Siblings: `REQUIREMENTS.md` (what it must do, each with a check) and `DESIGN.md` (how, step by step).

The project's memory is one markdown file per entry under `project-memory/entries/` [design, W1.1]. Every agent reads
`project-memory/INDEX.md` at session start to see what memory exists: one line per active entry [design, K6.1, Rd2.1].
This product is the small script that writes that file from the entries, and checks that the committed file is right.

**Who it is for.**
- Every agent and person who writes an entry runs it, and commits the index with the entry [run].
- Every agent that starts a session reads what it produced [design, Rd2.1].

**The problem it solves.** A hand-kept index drifts from the entries. And one file that every branch rewrites
conflicts when branches merge [run: GitLab and CPython hit this with their changelogs, C31]. The generator makes the
index a pure result of the entries, so it can always be rebuilt and checked, and a conflict is resolved by rerunning
it [run].

**What it will never do.**
- Never cut, drop, rank or shorten an entry's line to make the index fit. A hidden active entry is worse than an index
  that is too long [run, must-not 3].
- Never give a different file for the same entries on another machine: no date, no locale sort, no directory-listing
  order [run, must-not 2].
- Never be merged or edited by hand. On a conflict, resolve the entries and rerun it [run; design K6.1 "never edited
  by hand"].
- Never need anything installed beyond Python 3 and git: a fresh clone runs it as it is [design, Rd1.2; proposed:
  Python, after a timing check in which 2,000 entries took 0.03 s].
- Never commit, push, or change an entry. It writes `INDEX.md` and nothing else [run, must-not 6].

**Kept simple.** Memory is simple, and a mechanism that is not needed is removed [EJ, 2026-10-12: *"memory is very
simple"*; *"why need so many extra things?"*]. There is no merge driver, no CI job, no background process and no
overflow mechanism until one is needed [run].

**How we know it works.** [proposed]
- On any commit, `python3 tools/memory_index.py --check HEAD` passes, and the test suite runs it.
- After two branches that each added entries are merged, rerunning the script changes nothing.
- The same entries give the same `INDEX.md`, byte for byte, on every machine.
