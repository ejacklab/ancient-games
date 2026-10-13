# INDEX.md changes to the design (agy)

Labels: **[EJ]** his words; **[design]** already in `SOURCE_OF_TRUTH.md`, the vision, or `REQUIREMENTS.md`; **[proposed]** mine. Line numbers refer to files as read on 2026-10-13.

## 1. K6.2 and When to write

### Recommendation
[proposed] Make it as proposed: regenerate `INDEX.md` using `tools/memory_index.py` whenever any entry of any kind is created or changed (including status changes), and commit `INDEX.md` in the same commit as the entry.

### Reason
- [design] `REQUIREMENTS.md` G1.1: *"Whoever creates or changes any entry file runs the script, of every kind and for every status change, and commits `INDEX.md` in the same commit as the entry."*
- [design] `REQUIREMENTS.md` C1.2: *"It passes (exit 0) only when the entries are valid, the bytes are equal, and the size is within the limits."*
- [proposed] *My reading:* `INDEX.md` lists every active entry across all five kinds (D, F, L, O, H); restricting regeneration to decisions and facts leaves `INDEX.md` stale whenever an agent adds a lesson, an observation, a hypothesis, or retires an entry at the end of a task, immediately failing the byte-for-byte check in C1 and the pre-commit hook in G2.

### Exact text (`SOURCE_OF_TRUTH.md`)

**When to write table (l.103–108):**
- Old [design]:
  `| Immediately | Decisions and facts, before the code — and INDEX.md is regenerated right after, so the next session sees them. A human correction. The state of unfinished work before a handoff, an interruption or a context reduction. |`
- New [proposed]:
  `| Immediately | Decisions and facts, before the code. A human correction. The state of unfinished work before a handoff, an interruption or a context reduction. |`

**Text immediately following the "When to write" table:**
- [proposed] Add: `Whenever any entry is created or changed (every kind, every status change), INDEX.md is regenerated using tools/memory_index.py and committed in the same commit as the entry.`

**"Still open" line under "When to write" (l.117):**
- Old [design]:
  `**Still open:** which tool generates INDEX.md and what runs it (K6); who resolves a git merge conflict (W6). Whether a changed decision is edited in place or superseded is proposed in K4.3.`
- New [proposed]:
  `**Still open:** who resolves a git merge conflict on an entry file (W6). Whether a changed decision is edited in place or superseded is proposed in K4.3.`

**Requirement K6.2 (l.296–297):**
- Old [design]:
  `- K6.2 It is regenerated right after any decision or fact is written, so the next session sees them.`
  `- Open: which tool generates it and what runs it (a build detail).`
- New [proposed]:
  `- K6.2 Whoever creates or changes any entry file runs tools/memory_index.py (for every kind, and for every status change), and commits INDEX.md in the same commit as the entry.`
  *(Delete the "Open: which tool generates it and what runs it" line; `tools/memory_index.py` and the entry author settle it.)*
- Old [design] Fails if (l.298–299):
  `- Fails if regenerating INDEX.md changes it, meaning it was out of step, or it lists a superseded entry as active.`
- New [proposed] Fails if:
  `- Fails if a commit creates or changes an entry file without including the matching regenerated INDEX.md, regenerating INDEX.md produces a diff against the committed file, or INDEX.md lists a superseded or retired entry as active.`

---

## 2. K6.3, never hand-merge

### Recommendation
[proposed] Make it as proposed: add K6.3 barring manual edits or hand-merging of `INDEX.md`, requiring conflicting entry files to be resolved first and `INDEX.md` regenerated via `tools/memory_index.py`, and update W6 to clarify who resolves entry conflicts.

### Reason
- [design] `DESIGN.md` § Must not 1: *"Edit or hand-merge `INDEX.md`, or give it `merge=union`. `union` silently re-adds a superseded entry's line (C36)."*
- [design] `REQUIREMENTS.md` G3.2: *"When `INDEX.md` conflicts, nobody edits it. Resolve the entry files first, then run the script, stage `INDEX.md` and commit."*
- [proposed] *My reading:* `INDEX.md` is a purely derived artifact whose code-point order and claim formatting must match byte for byte; resolving merge conflicts by hand invites syntax mistakes, misordering, or accidental restoration of superseded entries, whereas regenerating `INDEX.md` after resolving individual entry files guarantees an exact, reproducible index.

### Exact text (`SOURCE_OF_TRUTH.md`)

**Add new requirement K6.3 under K6:**
- New [proposed]:
  `- K6.3 INDEX.md is never edited or merged by hand. When a git merge or rebase causes a conflict in INDEX.md, the person or agent doing the merge resolves any entry file conflicts first, runs tools/memory_index.py to regenerate INDEX.md, stages INDEX.md, and commits.`
- New [proposed] Fails if:
  `- Fails if a merge commit contains an INDEX.md that differs from what tools/memory_index.py generates from the merged entries, or git history shows conflict markers in INDEX.md resolved by hand.`

**Requirement W6 (l.259–261):**
- Old [design]:
  `- Open: who resolves a merge conflict.`
- New [proposed]:
  `- W6.3 When two branches conflict on an entry file, the person or agent merging the branch resolves the conflict in that file. A conflict in INDEX.md is never resolved by hand; it is resolved by regenerating it (K6.3).`
- Old [design] Fails if (l.260):
  `- Fails if an edit to an entry is lost without a conflict.`
- New [proposed] Fails if:
  `- Fails if an edit to an entry is lost without a conflict, or a merge conflict in INDEX.md is resolved by hand editing.`

---

## 3. Rd3.1, who checks the size

### Recommendation
[proposed] Make it as proposed: replace "the build checks it" in Rd3.1 and line 180 with "the script checks it (`tools/memory_index.py --check`), and the repo tests run the check".

### Reason
- [design] `REQUIREMENTS.md` C2 header: *"replaces "the build checks it" in Rd3.1"*
- [design] `CLAUDE.md` l.62: *"Tests: `env -u NO_COLOR python3 -m pytest -q`"*
- [proposed] *My reading:* The repository contains no build system or compilation step; the size check is performed by `tools/memory_index.py --check` and tested by pytest via `tests/test_memory_index.py` (`--check HEAD`), so citing a non-existent build step creates an unverifiable requirement.

### Exact text (`SOURCE_OF_TRUTH.md`)

**Summary line before Core requirements (l.180):**
- Old [design]:
  `INDEX.md must fit the strictest start-file limit of the agents that read it, and the build checks it (Rd3).`
- New [proposed]:
  `INDEX.md must fit the strictest start-file limit of the agents that read it; the script checks it (tools/memory_index.py --check), and the repo tests run the check (Rd3).`

**Requirement Rd3.1 (l.332–335):**
- Old [design]:
  `- Rd3.1 INDEX.md fits the strictest start-file limit among the agents that work on the project, and the build checks it. Example, from CACHES.md: about 24 KB and 200 lines when Claude Code, Qwen and agy share a project.`
- New [proposed]:
  `- Rd3.1 INDEX.md fits the strictest start-file limit among the agents that work on the project. The script checks it (tools/memory_index.py --check), and the repo tests run the check. Example, from CACHES.md: about 24 KB and 200 lines when Claude Code, Qwen and agy share a project.`
- Old [design] Fails if (l.334):
  `- Fails if INDEX.md exceeds that strictest limit.`
- New [proposed] Fails if:
  `- Fails if INDEX.md exceeds that strictest limit, tools/memory_index.py --check passes an index exceeding MAX_LINES or MAX_BYTES, or the repo test suite (pytest) does not run the check on HEAD.`

---

## 4. W1.1, the id

### Recommendation
[proposed] Make it as proposed: add to W1.1 that an entry's `id` must be unique without coordination between git branches and never sequential ("the next free number"), leaving the exact form open for EJ.

### Reason
- [design] `REQUIREMENTS.md` G4.1: *"An entry's `id` must be unique without coordination between branches. It is never "the next free number"."*
- [design] `SOURCE_OF_TRUTH.md` W6.2: *"Each agent works on its own branch or worktree, so two edits to the same lines meet as a merge conflict, not a silent overwrite."*
- [proposed] *My reading:* Independent agents working on separate git worktrees or branches without central coordination will inevitably choose the same sequential number (e.g. both allocating `0014`), causing ID collisions that remain hidden until merge time.

### Exact text (`SOURCE_OF_TRUTH.md`)

**Requirement W1.1 (l.194–198):**
- Old [design]:
  `- W1.1 Each entry is one file: project-memory/entries/<prefix>-<id>-<slug>.md. The prefix is one letter per kind (W2): D- decision, F- fact, L- lesson, O- observation and H- hypothesis. It matches the entry's kind. There is no runbook prefix (W3.6). An entry's kind, and so its prefix, never changes. A changed kind (a hypothesis confirmed, an observation that turns out to be a fact) is a new entry that supersedes the old one (K4.1; EJ, 2026-10-13).`
- New [proposed]:
  `- W1.1 Each entry is one file: project-memory/entries/<prefix>-<id>-<slug>.md. The prefix is one letter per kind (W2): D- decision, F- fact, L- lesson, O- observation and H- hypothesis. It matches the entry's kind. An entry's id is unique without coordination between git branches, and is never sequential ("the next free number"); the exact form (such as a date, a hash or a nonce) is open. There is no runbook prefix (W3.6). An entry's kind, and so its prefix, never changes. A changed kind (a hypothesis confirmed, an observation that turns out to be a fact) is a new entry that supersedes the old one (K4.1; EJ, 2026-10-13).`
- Old [design] Fails if (l.204–207):
  `- Fails if a lint over entries/ finds a missing field or section, or a file whose prefix is not one of the five or does not match its kind. It also fails if a reviewer finds two claims in one entry, or git shows an entry file renamed to a different prefix.`
- New [proposed] Fails if:
  `- Fails if two entries share an id, an entry uses a sequential number allocated from existing entries, a file's prefix is not one of the five or does not match its kind, or a lint over entries/ finds a missing field or section.`

---

## 5. W1.2 and W1.3, the format

### Recommendation
[proposed] Make it as proposed: specify in W1.2 that the header is frontmatter between two `---` lines starting on line 1 with `key: value` fields, and in W1.3 that the claim is the body between the closing `---` and the exact line prefix `**Why:**`.

### Reason
- [design] `REQUIREMENTS.md` B2.1: *"The header starts on line 1 with `---` and ends at the next line that is exactly `---`. Inside it, read only top-level `id:`, `kind:` and `status:` as `key: value`, stripping whitespace and surrounding quotes."*
- [design] `REQUIREMENTS.md` B2.2: *"The claim is the body after the header, up to the first line that starts with `**Why:**`."*
- [proposed] *My reading:* The parser in `tools/memory_index.py` expects strict `---` delimiters and the exact prefix `**Why:**`; without specifying these exact syntactic tokens in the design, agents format headers with non-standard YAML boundaries or markdown headings (`## Why`), causing parser crashes, validator rejections, or claims bloating `INDEX.md`.

### Exact text (`SOURCE_OF_TRUTH.md`)

**"What will be put in" (l.87–91):**
- Old [design]:
  `An entry is one markdown file. Its header holds: id, kind, status, author, the date it was recorded, covers (the code paths it is about), its source or evidence, links (depends_on, supersedes, superseded_by), a changed: log, and, on a decision to build something once its work is complete, done: (the time, the result, and the test results or a pointer to them; W5.3). Its body is the claim in one or two sentences, then **Why:**, then **How to apply:**.`
- New [proposed]:
  `An entry is one markdown file. Its header is frontmatter starting on line 1 with --- and ending at the next line of ---, holding top-level key: value fields: id, kind, status, author, the date it was recorded, covers (the code paths it is about), its source or evidence, links (depends_on, supersedes, superseded_by), a changed: log, and, on a decision to build something once its work is complete, done: (the time, the result, and the test results or a pointer to them; W5.3). Its body begins after the closing ---: the claim in one or two sentences up to the first line starting with **Why:**, then **Why:**, then **How to apply:**.`

**Requirement W1.2 (l.199–201):**
- Old [design]:
  `- W1.2 The header holds id, kind, status, author, the date recorded, covers (the code paths it is about), its source or evidence, depends_on, supersedes, superseded_by, and changed:. A decision to build something, once its work is complete, also holds done: (W5.3).`
- New [proposed]:
  `- W1.2 The header is frontmatter starting on line 1 with --- and ending at the next line that is exactly ---. It holds top-level key: value fields: id, kind, status, author, the date recorded, covers (the code paths it is about), its source or evidence, depends_on, supersedes, superseded_by, and changed:. A decision to build something, once its work is complete, also holds done: (W5.3).`

**Requirement W1.3 (l.202–203):**
- Old [design]:
  `- W1.3 The body is the claim in one or two sentences, then **Why:**, then **How to apply:**. There is one claim per entry.`
- New [proposed]:
  `- W1.3 The body begins after the header's closing ---. The claim is the text after the header up to the first line starting with **Why:** (one or two sentences, one claim per entry). Following the claim is **Why:**, then **How to apply:**.`

**Fails if (for W1, l.204–207):**
- Old [design]:
  `- Fails if a lint over entries/ finds a missing field or section, or a file whose prefix is not one of the five or does not match its kind. It also fails if a reviewer finds two claims in one entry, or git shows an entry file renamed to a different prefix.`
- New [proposed]:
  `- Fails if an entry does not start with --- on line 1, its header is not closed by a second --- line, it lacks an exact line starting with **Why:**, its claim is empty, a required field is missing, or a reviewer finds two claims in one entry.`

---

## What could go wrong

[proposed] **Concrete case: Hand-editing conflict markers in `INDEX.md` during a branch merge on a fresh clone with hooks unconfigured.**

1. [proposed] Branch `task-1` creates active decision `D-20261013-alpha.md` and commits the regenerated `INDEX.md`.
2. [proposed] Branch `task-2` concurrently creates active decision `D-20261013-beta.md` and commits the regenerated `INDEX.md`.
3. [proposed] Because both file names begin with `D-20261013-`, their lines in `INDEX.md` fall adjacent in code-point sort order (B3.1). When merging `task-1` into `task-2`, git flags a merge conflict in `INDEX.md`.
4. [proposed] A developer or agent unaware of K6.3 opens `INDEX.md` and manually resolves the `<<<<<<<` and `>>>>>>>` conflict markers, but reverses alphabetical order or adds extraneous spacing.
5. [proposed] Because git hooks do not activate automatically on a fresh clone without `git config core.hooksPath .githooks` (G2.2), the `.githooks/pre-commit` hook does not run, and the hand-edited `INDEX.md` is committed and pushed to `main`.
6. [proposed] Subsequent test runs in CI fail on `pytest tests/test_memory_index.py` (`--check HEAD`), blocking other tasks until someone regenerates `INDEX.md` cleanly.

---

## Questions for EJ

1. [proposed] **For W1.1 (the entry id): what specific format should the decentralized id take (for example, date prefix `YYYYMMDD-<slug>`, a 6-character content hash, or a date plus random nonce), or should it remain open until multi-branch work requires a fixed format?**
   - [proposed] If EJ picks a specific format, W1.1 defines that exact format; if left open, W1.1 keeps "the exact form is open".
2. [proposed] **For K6.2 (When to write): when an existing entry is updated in a way that leaves `INDEX.md` byte-identical (such as logging a timestamp in `changed:` or recording `done:` on a finished decision), should K6.2 require committing `INDEX.md` only when `INDEX.md` has actual diffs?**
   - [proposed] If yes, K6.2 clarifies "commits `INDEX.md` in the same commit whenever `INDEX.md` changes", avoiding confusion when running the generator produces no git diff.
