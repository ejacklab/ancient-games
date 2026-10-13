I'll read the brief and my stage-1 review first.
# INDEX.md — proposal (opencode)

## The algorithm

One script, `scripts/index.py` — Python 3, standard library only, no install step, no configuration, run from the repo
root. Two modes: run it, it writes; `--check`, it only reports. Everything below is inside that one file.

**1. What it reads.** Every file under `project-memory/entries/` whose name matches `<prefix>-<id>-<slug>.md`. Nothing
else — not `docs/`, not `AGENTS.md`, not `.cache/`, not git history, not file mtimes. One entry file in, one index line
out (X2, C8).

**2. Header parse.** First line `---`; the block to the next `---` is `key: value` lines. Required: `id`, `kind`,
`status`, `author`, `recorded`, `covers`, `changed:`. A missing or malformed one is a validation error (exit 2) and the
file is **not** indexed — a line with a hole in it is worse than a missing line, because the index is what makes the
entry discoverable (W1.2, O43, X11, X35). No third-party frontmatter linter is added; the fields are four lines of code.

**3. Filter.** Keep only `status: active`. A `superseded` or `retired` entry produces no line at all — the index does not
list it as available, because an entry that is only reachable by a link must not look active (K4.1, C36).

**4. One line per entry**, in K6.1's own field order:

```
- [D-0001](entries/D-0001-use-plain-markdown.md) decision: memory is plain markdown files kept in git
```

The link path is relative to `INDEX.md`, so it resolves from the file the agent already read (C1: a resolving long link
beats a short dead one). `covers` is **not** in the line: it stays in the header and is what Rd4.1 reads before an edit.
If entries ever go missing in practice, `covers` is the first thing to add, because it is already parsed (O35).

**5. The one-line claim.** Take the body after the header: the text up to the first `**Why:**` line or the first blank
line, whichever comes first; join to one line; drop emphasis markers; cap the **whole rendered line** at 150 charactersby cutting the claim at a word boundary and appending `…`. The id, kind and link are never truncated (C1, C46, X30).

**6. Order.** Sort by entry filename in byte/codepoint order — never `localeCompare`, never a bare `sort` with no
`LC_ALL` (C2, X2, C9, O6, C14). With zero-padded ids this is also id order, so a new decision lands at the bottom and
touches no line any other branch is editing (C2, C34).

**7. Nothing volatile in the output.** No generation date, no time, no hostname, no file count, no locale-dependent
ordering, no mtime (O7, C15, X8, O6). Two runs over the same `entries/` produce byte-identical files on any machine
(O5). This is what makes step 11's check mean anything.

**8. Fixed head.** Title line, a "generated — do not edit by hand" line, and the two commands, then the lines. Fixed
text, no date. It counts against the budget like every other line.

**9. Write.** Render to bytes, compare with the file on disk. **Identical → do not write** (no mtime churn, no no-op
commits, no ping-pong between collaborators) (C3). Different → write, then `git add project-memory/INDEX.md`. The script
stages that one path and nothing else; it never commits, never amends, never pushes, never runs `git commit` (C26, C34).

**10. When it is too big.** The generator never truncates, samples, drops or reorders an entry to fit — that would make
the check in step 11 pass on a file that lies. Over budget it writes the complete index, exits **2**, and prints one
line: the size, and the two accepted fixes — shorten the claim (an authored change to the entry) or split a `kind` into
its own second index. Refusing to write a partial result is the tested prior art (C52, C46); the only difference is that
this script still writes the full file, because the entries are the truth and the index must not be stale (X19).

**11. Check mode.** `python3 scripts/index.py --check` writes nothing and exits `0` clean, `1` out of date (with the
line to run to fix it in the message, and a diff with `--diff`), `2` a validation or size failure (X31, X32, C55, O39,
O40). One command both makes and checks the file; there is no second implementation to keep in sync. Anyone can also
check by hand: regenerate, then `git diff --exit-code project-memory/INDEX.md`.

**12. When it runs and what runs it** — four triggers, because no single one covers everyone (O13, C17):

- **After any agent writes an entry**: a `PostToolUse` hook, `matcher: "Edit|Write"`, filtered to
  `project-memory/entries/**`, runs the script (O17, X9). This is the K6.2 trigger, and it is the only one that can
  claim "right after".
- **Before every commit that touches `project-memory/`**: a repo hook, defined in a version-controlled config file and
  armed by one install command a clone runs once (O14, X11, C26). It runs `--check` and refuses the commit if the index
  is out of date (O12). `pre-commit`-style stashing is fine here; the check is about the staged snapshot.
- **On pull requests in CI**: `worktree add HEAD` in a temp dir, regenerate there, fail if `git status --porcelain` is
  non-empty — so the check never touches a dirty tree, and every PR is checked against the base (C54, O38, X15).
- **In `AGENTS.md`, as the first instruction**: if the index is stale, run the script before reading it — a hook is
  deterministic where an instruction is advisory (O19, O18).

Nothing runs on `post-merge`, `post-checkout` or `post-rewrite`. `post-merge` never fires on the conflicted mergesthat leave a shared generated file stale (O15, X14), and re-running after a conflict is not a repair — a conflict is
resolved by merging the entries, not by replaying a step.

**13. What happens in git.** The index is committed, because Rd1.2 says a fresh clone reads it with no cache and no
service (O25, C25, C39). Two lines in `.gitattributes`, the only per-path in-repo mechanism git offers (O29):

```
project-memory/INDEX.md linguist-generated=true
project-memory/INDEX.md merge=binary
```

`linguist-generated` collapses it in diffs so review stays about the entries (O22, C41). `merge=binary` takes one side
and leaves the path unresolved (O23) — the right behaviour, because the correct result of a merge of two branches is
not a text merge of two old outputs; it is whatever the merged entries generate. **No merge driver.** `union` re-adds
lines one branch deleted, so a superseded entry comes back as active — the exact failure K6 names — and does so
silently (O24, C35, C36, X21); a custom driver lives in `.git/config`, so a fresh clone has it inert while the
attribute implies it works (C37, X22, O37).

The conflict procedure, written into `AGENTS.md` and the merge-request template:

1. Merge normally. `INDEX.md` may come out conflicted or be left unresolved; do not hand-edit it.
2. Resolve the **entry files**.
3. `python3 scripts/index.py`.
4. `git add project-memory/INDEX.md`, commit, push.

This is FKF's policy verbatim in shape — resolve the topic files, rerun the generator, take its output wholesale
(X19) — and mdsmith's (C38), minus the driver that cannot survive a clone.

**14. How anyone checks it is in step.** `--check`, in CI, and by hand in step 11. Plus one rule that catches whatbyte-comparison cannot: a change to an entry and a change to `INDEX.md` belong in the same commit, so `git show --stat`
on any commit touching `entries/` shows both. That is `K1.1`'s shape applied to the index, and it is what makes drift
visible in review rather than at the next session.

## Three supporting reasons

1. **The index has to be committed, and committing it is the whole problem the other reviews' tools avoid.**
   Rd1.2 forces the commit (O25, C25, C39). GitLab's changelog and CPython's `Misc/NEWS` both broke under parallel
   branches and both "fixed" it by not committing the combined file — an answer Rd1.2 closes off (C31, C32, C33). The
   only prior art that fits is regenerate-never-hand-merge (X19, C38), and the trap sitting next to it is `union`, which
   reinstates deleted lines silently (O24, C36, X21). The design's `W6.1` already removed the input-side conflict; step
   13 removes the output side the same way. (findings: X19, C38, C31, C32, O24, C36, X22)
2. **K6.2's trigger is a write-side trigger, and deferring generation — the common prior art — cannot satisfy it.**
   Towncrier, Changesets and blurb all generate at release, so working branches never touch the shared file (C23, X12,
   X18); Understorm and Qwen regenerate on write (X9, C22), which is the shape K6.2 describes. But hooks are not
   shipped in a clone (O13, C26) and `post-merge` skips conflicted merges (O15, X14), so the write-side hook alone
   leaves people and stale clones uncovered — hence four triggers in step 12 with commit and CI as backstops.
   (findings: X9, C22, O13, O15, O26)
3. **Byte-stability is what turns "regenerating changes it" into a check instead of an alarm.** K6's *fails if* is only
   meaningful if regenerating the same `entries/` gives the same bytes; Qwen Code found this the hard way — locale
   ordering made collaborators rewrite the file back and forth and wedged their sync — and pinned code-unit ordering and
   a byte-identical skip (C2, C3). Reproducible Builds names the volatile inputs: `LC_COLLATE`/`LC_ALL`, `LC_TIME`,
   `LC_CTYPE`, `TZ`, and timestamps (O6, O7, C15, X8). A check that fires on locale noise is a check people learn to
   ignore, which is worse than no check. (findings: C2, C3, O6, O7, C15, X8)

## Six must-not-dos

1. **Do not give `INDEX.md` `merge=union` or `merge=ours`.** `union` "tends to leave the added lines in random order"
   and silently re-adds a removed line — the case K6 requires to fail; `ours` is inert without per-clone config while
   the attribute claims otherwise. (findings: O24, C35, C36, X21, C37, X22)
2. **Do not resolve the conflict with a merge driver.** A driver is defined in `.git/config`, which a fresh clone does
   not have; the committed attribute would imply the conflicts are auto-resolved when they are not. Merge the entries,
   run the script, take its output. (findings: C37, X22, C38, X19)
3. **Do not put a timestamp, a date, a count or a locale-dependent ordering in the file, and do not sort with
   `localeCompare` or a bare `sort`.** Same `entries/` must give the same bytes on every machine, or the K6 check
   becomes a false alarm. (findings: O6, O7, C2, C9, C15, X2, X4, X8)
4. **Do not write when the bytes are unchanged, and do not let the generator stage or commit anything but
   `INDEX.md`.** No-op rewrites churn mtimes and produce ping-pong commits; a hook that commits turns a stale file into
   an unrequested commit. (findings: C3, C26, C34)
5. **Do not truncate, sample, rank-and-fit or dedupe entries to meet the size budget, and do not generate a summary the
   author did not write.** Dropping a line makes an active decision unfindable at session start, which is worse than a
   long index; a merge of two entries deletes the evidence that two exist. Over budget is a message to shorten a claim,
   not a silent edit. (findings: C46, C52, X7, C26, X26)
6. **Do not treat any single hook as the enforcement.** Client-side hooks are not copied by `git clone`, `post-merge`
   never runs on a conflicted merge, and `post-checkout` fires but repairs nothing. The write-side hook plus a   commit-time check plus CI plus the `AGENTS.md` instruction is the minimum that survives a clone. (findings: O13, O15,
   O16, O17, X14, C24)

## Design changes

- **W1.3** — the body's claim becomes "**on a single line**", then **Why:**, then **How to apply:**. Without this, "one
  or two sentences" leaves the generator's extraction rule a judgement call, and no source in any review defines how to
  take a body claim and make it one physical line (codex's gap #3). This is the only reason `K6.1` needs no second
  `claim:` field in the header, which is deliberate: one claim, one place, nothing to drift.
- **K6.1** — "showing its id, kind and one-line claim" becomes "showing its id, its file as a link, its kind and its
  one-line claim". The link is what makes the index a map rather than a table of contents: it is what llms.txt, Qwen's
  index and mdsmith's catalog all do, and Rd4.1/Rd4.2 already assume the agent moves from the index to the entry.
- **Rd3.1** — name the two numbers the generator enforces: **190 lines and 24 KB**, total file, with the head counted.
  These are the design's own example figures. Stated plainly because the reviews show the ceiling depends on *how* the
  file is loaded: Claude Code's 200-line/25 KB limit is documented for its **native** `MEMORY.md`, not for a repo file
  an agent opens (C45, X26), and Codex's 32 KiB applies only to files it concatenates itself (C48, C29). No source
  establishes a byte ceiling for our actual load path, so the design's own example stands until measurement replaces  it — which is what the requirement already says.
- **K6.2** — "regenerated right after any decision or fact is written, so the next session sees it" becomes
  "**regenerated and staged before the task's last commit; a session that writes an entry and does not regenerate says
  so in its `state.md`**". Reason: W6.2 puts each agent on its own branch, so a write and the next session's read are
  on different sides of a merge — there is no moment where "right after" is shared. K6's *fails if* still fires at the
  commit hook and in CI, so the requirement is not weakened, only made achievable.
- **W6 "Open: who resolves a merge conflict"** — half-closed by this proposal: the *procedure* is regenerate (step 13),
  and the person merging runs it. What stays open is whether a conflict may also be resolved by the machine without a
  person; I would say no, and that is EJ's call.

## Where I disagree with the other reviews

- **Line vs link.** I emit a markdown link per line. claude's Qwen/mdsmith and codex's OKF evidence both point that
  way (C1, C5, C12, X5); neither claude nor codex proposes it, and K6.1's wording as written would produce a bare id.
  I side with the link and record the wording change above.
- **Where the claim comes from.** Every nearest tool reads an authored `description` field (X3, X27, X33, C5); the
  accepted design puts the claim in the body. I take it from the body and change W1.3, because a second copy of the
  claim is a second thing that can go stale and be believed.
- **Order.** claude notes Repomix and Aider rank by importance to fit a budget (C19, C53) and my own review notes the
  same (O35). Ranking plus truncation breaks K6.1's "one line per active entry" and cannot be byte-stable across
  clones. Path order; over budget is a message.
- **Triggers.** claude's mdsmith evidence leans on `pre-merge-commit` (C24) and codex excluded a Phoenix issue about a
  failed post-merge update. Merge-time hooks are not shipped in a clone (O13) and skip exactly the conflicted merges that
  leave a generated file stale (O15, X14). K6.2 needs the write-side trigger first.
- **The size number.** claude correctly finds the 200-line figure applies to Claude Code's native `MEMORY.md`, not to a
  repo file (C45, X26). I do not treat that as a reason to abandon Rd3.1's example; I treat it as the reason the
  generator must print the measurement instead of silently picking a number. claude's "committed *and* not committed,
  per branch" answer is not available to us: Rd1.2 forces the commit.
- **Two checks, one script.** codex separates source validation from output freshness (X33, X35) and I agree, but I
  fold both into one script with two exit codes rather than two commands, so there is one thing to document and one
  thing to install.
- **CI: fail, do not self-heal.** terraform-docs pushes the regeneration onto the PR branch (O20); the design's K6 says
  "Fails if", so CI fails and names the command. Pushing to someone's branch makes review show a commit the author did
  not make.
