# Stage 3 — summary of the three reviews of `proposals/claude.md`

Written by the COO (Claude `claude-opus-5-5`), 2026-10-12, from `reviews/codex.md`, `reviews/opencode.md` and
`reviews/agy.md`. Each review was blind to the others. Labels: *quoted*, *my reading*, *verified* (by me).

## Verdicts

All three return **ACCEPT WITH FIXES**. None found a reason to change the shape: one deterministic script, a committed
file, a check against a git snapshot, no cutting, regenerate on conflict.

## Problems that two or three reviewers found independently

| # | Problem | Found by | Fix (*my reading*) |
|---|---|---|---|
| 1 | **The hooks miss some ways a wrong index gets committed.** Rebase, cherry-pick and fast-forward run no `pre-commit`. After a `--no-verify` commit, later code-only commits pass because the hook exits early when no memory file is staged. | codex 1–2, opencode 1–2, agy 3 | Add the check to the test suite (`pytest` is already configured, and CLAUDE.md names it as the test command). Reword the design to "checked at commit and at every test run", not "at every commit". *Verified:* the local `git-rebase` manual names only the pre-rebase, post-commit and post-checkout hooks. |
| 2 | **Link targets aren't encoded.** A space, `#`, `?` or a non-ASCII character in a file name gives a dead or wrong link, and the check still passes. | codex 6, opencode 7, agy 8 | Percent-encode the path, as Qwen Code does (C1). |
| 3 | **The file prefix and `kind` aren't tied together.** `D-…md` with `kind: lesson` passes and lands in the D group. | opencode 8, agy 7 | Reject a prefix/kind mismatch in validation. |
| 4 | **`**Why:**` must match exactly.** `**Why**:` or `## Why:` fails the whole build. | opencode 6, agy 5 (codex found no problem) | Fix the exact spelling in W1.3 and keep the strict match. The error names the file, so the failure is loud. |
| 5 | **Write mode and check mode read different sets of files.** An untracked entry is indexed in write mode but missing from the commit; a partially staged entry can't be repaired with the printed command. | opencode 3, codex 9 | Write mode also reads only git-tracked entry files, or refuses while an entry is untracked. |
| 6 | **Size limit not settled.** The units are mixed (bytes against characters) and the readers and load paths are unnamed. "Until EJ decides" conflicts with W4 (anyone may change entries). | codex 10–12, opencode 13 | Leave the limit open, as the proposal does, but drop "until EJ decides": any edit that brings the index back under the limit passes. |
| 7 | **Exit codes.** Write mode exits 1 after writing an oversized file, which breaks `script && git add`. The byte-identical branch has no defined exit code. | agy 2, opencode 16 | Write mode exits 0 and warns; only `--check` fails on size. |
| 8 | **Three citations say less than claimed.** C2 is about locale churn, not clean merges. C20 is Go's "DO NOT EDIT" line and doesn't name a command. O31 is about instructions getting lost, not a file being ignored. | all three on C2; opencode and agy on C20; codex on O31 | Correct the citations; the merge claim stays labelled *not measured*. |

## Found by one reviewer, and worth taking

- **codex 3:** a change to the script itself (or to its size constants) skips the hook. Add `tools/memory_index.py` to
  the paths that trigger the check.
- **codex 7:** `git ls-files` and `git ls-tree` quote unusual paths. Use the NUL-separated form (`-z`).
- **opencode 4:** handle the first run. A missing `INDEX.md` means "write it"; a check before the first commit passes.
- **opencode 5:** one broken retired entry blocks every memory commit, including the commit that would fix it. Validate
  in full only the entries that get a line, and report the others as warnings.
- **opencode 10:** the two hook files can be one: `pre-merge-commit` just calls `pre-commit`.
- **opencode 11:** `AGENTS.md` today only points to `CLAUDE.md` (*verified*), so the two instructions must go into
  `CLAUDE.md` until the planned move.
- **opencode 12:** the script accepts the `O-`/`H-` prefixes, which W1.1 still marks as proposed. List that as a
  design change.
- **opencode 14:** the "When to write" table in `SOURCE_OF_TRUTH.md` needs the same change as K6.2.
- **opencode 15:** add tests: golden bytes, run twice with no diff, and the check rejecting a hand edit. This is the
  same as fix 1.

## Not taken (*my reading*)

- **agy 10:** cap each claim at 150–200 characters. That cuts the author's claim, which the proposal's must-not 3 and
  the earlier consensus forbid.
- **agy 6:** a `---` rule in the body would be read as the end of the header. The proposal takes the header as the first
  `---` line up to the next one, and a rule in the body comes after the closing line. Add "line 1 must be `---`" for
  clarity; there is no defect.
- **codex 8:** whitespace inside code spans gets collapsed. True, but a claim written as one or two plain sentences
  rarely has a code span with two spaces. Minor; note it.
- **agy 1:** `--check` with no argument should read the working tree. That's a choice, not a defect: staged is right
  for the hook. A `--worktree` flag covers the other case.

## What the reviews agree holds up

Reading git objects rather than the working tree (opencode calls it "the strongest single decision"). Byte-level
determinism spelled out. No truncation, and no overflow mechanism until one is needed. K6.2 rewritten to "any entry,
same commit". Must-not 6 (SessionStart output cap) checked and correct. The git-manual quote about `pre-commit` on
conflicted merges checked by opencode and correct.

## Net (*my reading*)

The algorithm stands. Eight fixes, all small, none adding a mechanism except one test file. The test suite replaces
"the hook catches everything", which the reviews showed isn't true.
