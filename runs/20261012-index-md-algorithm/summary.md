# INDEX.md algorithm — summary for EJ

Run `20261012-index-md-algorithm`, 2026-10-12. Written by the COO (Claude `claude-opus-5-5`) after reading the three
literature reviews (`lit-review/`) and the three proposals (`proposals/`). agy was dropped by EJ (headless mode could
not read web pages). Labels: *quoted* (with the source), *my reading*, *not measured*.

## The answer in one paragraph

All three proposals, written independently, land on the same algorithm (*my reading* of the three reports). One small
Python script with no dependencies reads `project-memory/entries/`. It keeps the active entries, sorts them by file
name, and writes one line per entry, `- [id](entries/<file>) kind: claim`, into a **committed** `INDEX.md`. It writes
no date. The same script with `--check` regenerates the file and compares the bytes. Whoever writes an entry runs the
script and commits the index in the same commit. When `INDEX.md` conflicts in a merge, nobody edits it: resolve the
entries, rerun the script, take its output. When it is too big, nothing is cut; the check fails and EJ decides.

## Where all three agree

| # | Point | Why (finding ids from the reviews) |
|---|---|---|
| 1 | Commit `INDEX.md` | Rd1.2: a fresh clone must read it with nothing run (O25, C25, C34) |
| 2 | One script, two modes: write, and `--check` (byte compare, diff, exit code) | Kubernetes and Cog check generated files exactly this way (C54, C55, X31) |
| 3 | Read only `entries/`; header `id`, `kind`, `status`; active only; the claim is the body up to `**Why:**` | Superseded entries must not appear (K6); no second copy of the claim in the header |
| 4 | Sort by file name, by code point; no locale, no directory-listing order, no timestamp; don't rewrite an identical file | Qwen Code hit locale order making collaborators rewrite the file back and forth (C2, quoted); Reproducible Builds (C14, C15) |
| 5 | Each line is a link to its entry | llms.txt, Qwen Code and mdsmith all do this (C1, C5, C12) |
| 6 | Never hand-merge; never `merge=union`; no custom merge driver | `union` silently re-adds a deleted line, so a superseded entry comes back as active (C36, quoted); a driver lives in `.git/config`, which a clone doesn't have (C37, X22) |
| 7 | Over the size limit: never truncate, drop or rank; fail loudly | A cut index hides active entries without a sign (C45, C46) |
| 8 | Run after **every** entry change, not only decisions and facts, and commit the entry and index together | A lesson or a supersede also changes the index |

## Where they differ

| | claude | codex | opencode |
|---|---|---|---|
| What runs it | the writer, plus committed git hooks (`pre-commit`, `pre-merge-commit`, switched on with `core.hooksPath`) | the writer, plus a staged check, CI, and a check at session start | four triggers: Claude `PostToolUse` hook, pre-commit, CI, `AGENTS.md` |
| Merge setting | normal text merge; sorted lines usually merge cleanly | normal | `merge=binary`, so every merge that touches it stops as a conflict |
| Over the limit | write the full file, fail | keep the old file, fail | write the full file, fail |
| Size limit | two constants in the script | a new `index-limits.json` per agent and load route | fixed 190 lines / 24 KB, plus a 150-character line cap that cuts the claim |

## My review (*my reading*)

**Take claude's proposal.** It has the fewest parts: one script, one hook file, and two lines in `AGENTS.md`. It covers
every agent and every person, it drops what this repo doesn't have (CI), and its hook choice is right. git's manual
(local, git 2.43) says of a conflicted merge that `pre-merge-commit` *"will not be executed, but the pre-commit hook
will"*. Checking both hooks therefore catches clean merges and conflicted ones alike. Verified by me.

**Don't take these:**
- **opencode's 150-character cut.** It shortens the author's claim, against its own must-not ("do not generate a summary
  the author did not write"). Its fixed 190 lines / 24 KB also sets a number up front, which the design avoids.
- **opencode's `merge=binary`.** Verified in git's manual: it *"leave[s] the path in the conflicted state"*. That turns
  merges that would be clean into manual work.
- **opencode's `PostToolUse` hook.** It covers Claude only.
- **codex's `index-limits.json`.** It's one more file and mechanism. A constant in the script does the job.

**One real new finding: entry ids can collide across branches** (claude must-not 5; C40). If ids are "the next free
number" (`D-0001`, `D-0002`…), two branches will both take the same one. blurb, reno and Beads use a datetime, a nonce
or a hash for this reason. W1.1 doesn't say how an id is made, so this is a gap in the design.

**I withdraw my earlier suggestion** to leave `INDEX.md` uncommitted and generate it at session start. None of the three
adopted it. Rd1.2 asks for a readable file in the clone, and sorting by file name makes most merges clean, so the
conflict I worried about is smaller than I thought (*my reading*, not measured). Separately, Claude Code caps a
SessionStart hook's output at 10,000 characters with no setting to raise it (verified on the hooks page), so that route
could not carry the index anyway.

## The six must-nots (consensus across the three)

1. Don't edit or hand-merge `INDEX.md`, and don't use `merge=union`.
2. Don't let the output depend on the machine: no locale sort, no directory-listing order, no date or timestamp.
3. Don't truncate, drop, rank or dedupe lines to fit the size.
4. Don't skip a malformed entry silently, and don't write a line with a hole in it. Fail and name the file.
5. Don't rely on one trigger alone. Hooks aren't copied by `git clone` and can be bypassed with `--no-verify`.
6. Don't let the script stage, commit or push anything beyond `INDEX.md`, and don't let it delete entries (unlike
   changelog tools, which consume their fragments).

## Design changes the proposals ask for (none made; EJ decides)

- **K6 Open:** close it with the script, the writer, and the hooks.
- **K6.2:** "right after any decision or fact is written" becomes *right after any entry is created or changed, in the
  same commit*.
- **New K6.3:** `INDEX.md` is never merged by hand. Resolve the entries, then regenerate.
- **Rd3.1:** "the build checks it" becomes *the script checks it at every commit that touches `project-memory/`*. Over
  the limit, nothing is cut.
- **W1.1:** an id is unique without coordination between branches; never the next free number.

## What I checked, and what I did not

- **Checked myself:** git's hook manual on `pre-merge-commit` and `pre-commit`; the `merge=binary` text; the Claude Code
  SessionStart 10,000-character cap; and the `CACHES.md` line giving about 107–150 lines for 25 KB.
- **Not checked:** the other citations in the reviews. Whether sorted lines really merge cleanly in practice is
  *not measured*. No script exists; nothing was built.
