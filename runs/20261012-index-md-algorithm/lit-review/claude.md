# INDEX.md generation — literature review (claude)

Researched 2026-10-12 with WebSearch, WebFetch and `gh api` (GitHub contents API) for primary files. Where WebFetch
summarised a page through its small model, the quotes below are the strings it returned as quotes; where I read the
file itself through `gh api`, the quote is copied from the file. Each source row says which.

## Sources

| id | source (name + URL) | what it is | date or version, if shown |
|---|---|---|---|
| S1 | Claude Code docs, "How Claude remembers your project" — https://code.claude.com/docs/en/memory | vendor doc: CLAUDE.md, AGENTS.md, auto memory `MEMORY.md` index | page mentions Claude Code v2.1.214–v2.1.285; fetched 2026-10-12 |
| S2 | Claude Code docs, Hooks reference — https://code.claude.com/docs/en/hooks | vendor doc: SessionStart hook, context size cap | fetched 2026-10-12 (first 100k chars of the page read) |
| S3 | OpenAI Codex, AGENTS.md guide — https://learn.chatgpt.com/docs/agent-configuration/agents-md (redirect from developers.openai.com/codex/guides/agents-md) | vendor doc: `project_doc_max_bytes` | no date or version shown |
| S4 | Gemini CLI, GEMINI.md — https://geminicli.com/docs/cli/gemini-md/ | vendor doc: context files | no date shown |
| S5 | AGENTS.md — https://agents.md/ | open format page | no date shown |
| S6 | llms.txt proposal — https://llmstxt.org/ and its source `nbs/index.qmd` in https://github.com/AnswerDotAI/llms-txt | spec of an index file written for LLMs | published 2024-09-03, modified 2026-08-10 (per page) |
| S7 | Karpathy, "LLM Wiki" gist — https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f | write-up: LLM-maintained `index.md` + `log.md` | page shows "Created April 4, 2026" |
| S8 | mdsmith docs — https://github.com/jeduden/mdsmith (`docs/features/self-maintaining-sections.md`, `git-native.md`, `progressive-disclosure.md`, `size-and-readability.md`, `docs/guides/directives/generating-content.md`, `docs/reference/cli/merge-driver.md`), read via `gh api` | Markdown linter that generates a catalog/index from front matter, with a merge driver | repo pushed 2026-10-11; 21 stars |
| S9 | adr-tools — https://github.com/npryce/adr-tools (`src/adr-generate-toc`, `src/adr-list`, `src/_adr_title`), read via `gh api` | shell tool: ADR table of contents | last commit 2020-03-30 |
| S10 | adr-log README — https://github.com/adr/adr-log | Node tool: ADR log/index from ADR files | repo pushed 2023-01-05 |
| S11 | log4brains README — https://github.com/thomvaill/log4brains | ADR knowledge base published as a static site | repo pushed 2024-12-17 |
| S12 | towncrier docs — https://towncrier.readthedocs.io/en/stable/tutorial.html and /cli.html | changelog from one-file-per-change "news fragments" | "stable" docs, fetched 2026-10-12 |
| S13 | blurb README — https://github.com/python/blurb, read via `gh api`; plus a listing of https://github.com/python/cpython/tree/main/Misc | CPython's NEWS-fragment tool | listing taken 2026-10-12 |
| S14 | GitLab blog, "How we solved GitLab's CHANGELOG conflict crisis" — https://about.gitlab.com/blog/solving-gitlabs-changelog-conflict-crisis/ | write-up of the move to one file per entry | 2018-07-03 |
| S15 | GitLab docs, Changelog entries — https://docs.gitlab.com/development/changelog/ | current GitLab practice (commit trailers) | fetched 2026-10-12 |
| S16 | reno docs — https://docs.openstack.org/reno/latest/user/design.html and /usage.html | OpenStack release-notes tool, notes read from git history | "latest" docs |
| S17 | reno 2.9.0 release announcement — https://lists.openstack.org/pipermail/release-announce/2018-April/004980.html | release note for the reno cache file | 2018-04 |
| S18 | Changesets — https://github.com/changesets/changesets/blob/main/docs/intro-to-using-changesets.md (self-marked outdated) and https://changesets.dev/guide/cli | npm monorepo change files | fetched 2026-10-12 |
| S19 | git, gitattributes(5) — https://git-scm.com/docs/gitattributes | git manual: `merge` attribute, `union`, custom drivers | current online manual |
| S20 | Wikimedia Phabricator T201514 — https://phabricator.wikimedia.org/T201514 | bug report on `merge=union` | 2018-08-08 |
| S21 | github/gh-aw PR #50639 — https://github.com/github/gh-aw/pull/50639, read via `gh pr view` | PR removing an inert `merge=ours` from a generated file's attributes | merged 2026-08-05 |
| S22 | npm docs — https://docs.npmjs.com/cli/v6/configuring-npm/package-locks and https://docs.npmjs.com/cli/v10/configuring-npm/package-lock-json | lockfile conflict resolution by regeneration | npm v6 and v10 docs |
| S23 | Kubernetes `hack/lib/verify-generated.sh` — https://github.com/kubernetes/kubernetes/blob/master/hack/lib/verify-generated.sh, read via `gh api` | CI helper that checks generated files are current | fetched 2026-10-12 |
| S24 | Cog, "Running cog" — https://cog.readthedocs.io/en/latest/running.html | tool that writes generated text into files; `--check` | "latest" docs; no version shown |
| S25 | pre-commit — https://pre-commit.com/ | git-hook framework | fetched 2026-10-12 |
| S26 | Go command docs, `go generate` — https://pkg.go.dev/cmd/go#hdr-Generate_Go_files_by_processing_source | generated-file convention | fetched 2026-10-12 |
| S27 | GitHub docs, "Customizing how changed files appear on GitHub" — https://docs.github.com/en/repositories/working-with-files/managing-files/customizing-how-changed-files-appear-on-github | `linguist-generated` | fetched 2026-10-12 |
| S28 | GitHub docs, "Managing a merge queue" — https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue | merge queue | fetched 2026-10-12 |
| S29 | Reproducible Builds, "Stable order for inputs" — https://reproducible-builds.org/docs/stable-inputs/ | guidance on deterministic output | fetched 2026-10-12 |
| S30 | Reproducible Builds, "Timestamps" — https://reproducible-builds.org/docs/timestamps/ | guidance on timestamps in output | fetched 2026-10-12 |
| S31 | Aider, "Repository map" — https://aider.chat/docs/repomap.html | token-budgeted repo map for an agent | fetched 2026-10-12 |
| S32 | Repomix README — https://github.com/yamadashy/repomix | packs many files into one file for an LLM | fetched 2026-10-12 |
| S33 | Beads README — https://github.com/steveyegge/beads (commit b630f96f5bd2) | issue tracker / memory for coding agents | pushed 2026-10-12 |
| S34 | ai-memory README — https://github.com/akitaonrails/ai-memory (reached via MD-Generalist/ai-memory) | git-backed markdown memory for agent CLIs | pushed 2026-10-11 |
| S35 | Qwen Code docs, Memory — https://github.com/QwenLM/qwen-code/blob/main/docs/users/features/memory.md, read via `gh api` | vendor doc: generated `MEMORY.md` index, team memory in git | last commit 864850816e92, 2026-10-05 |
| S36 | Qwen Code source — `packages/core/src/memory/indexer.ts`, `index-budget.ts` (commit 864850816e92, 2026-10-05) and `team-memory-sync.ts` (commit 93c0d6d20d68, 2026-09-12) in https://github.com/QwenLM/qwen-code, read via `gh api` | the code that builds, orders, sizes and syncs that index | as stated |
| S37 | dune-common issue #266 — https://gitlab.dune-project.org/core/dune-common/-/issues/266 | project issue on CHANGELOG.md conflicts | no date shown |

## Findings

### 1. Building the lines

- **C1** — Qwen Code builds its team-memory `MEMORY.md` index from the files in a directory, one line per file:
  `- [title](relative path) — description`, where the line is capped and an over-long description is shortened, not
  the link. *Quoted* (S36, `indexer.ts`): `` const link = `- [${title}](${encodeIndexPathTarget(doc.relativePath)})`; ``
  and the comment *"a resolving long link beats a short dead one"*. The cap is `MAX_INDEX_LINE_CHARS = 150`
  (`index-budget.ts`).
- **C2** — Qwen Code sorts that committed index by path with a code-unit comparison and says why: locale-dependent
  order made collaborators rewrite the file back and forth. *Quoted* (S36, `indexer.ts`): *"Code-unit comparison, NOT
  localeCompare: the index is committed and pushed, so its ordering must be byte-identical across machines/locales —
  otherwise two collaborators churn MEMORY.md back and forth and the ff-only sync wedges."* It also orders by path, not
  by modification time: *"docs are ordered by path (not mtime) so the committed file is deterministic across machines
  and does not churn after a git checkout."*
- **C3** — Qwen Code skips the write when the new index is byte-identical to the old one. *Quoted* (S36,
  `indexer.ts`): *"Skip a byte-identical rewrite: regenerating MEMORY.md every run would churn its mtime and produce
  no-op commits that ping-pong between collaborators."*
- **C4** — Qwen Code's team index merges entries whose descriptions are the same after normalising, into one line with
  an "(also: …)" list; the topic files are kept. *Quoted* (S36, `indexer.ts`): *"When two people save the same shared
  fact, collapsing them into one index line — listing the other files via "(also: …)" — keeps the index readable. The
  topic files themselves are never removed"*, and the match is *"Conservative (normalized-exact, not fuzzy) so two
  genuinely different facts are never silently merged."*
- **C5** — mdsmith generates an index from the front matter of files matching a glob, one row per file, with a row
  template, a `where` filter and a sort key; the default is one link per file sorted by path. *Quoted* (S8,
  generating-content.md): *"outputs `- [<basename>](<path>)` per file, sorted by path"*; `row: "| {id} |
  [{title}]({filename}) |"`; *"The filter runs after globbing and front matter parsing, but before sort and render."*
- **C6** — mdsmith's sort rule handles numeric ids and missing fields explicitly. *Quoted* (S8): *"Format:
  `[-][numeric:]KEY`. … Missing values sort as empty string."*; the `numeric:` prefix exists because ids
  *"would otherwise collate lexicographically (`100` before `52`)"*. If any value is not an integer it *"falls back to
  string compare for all entries — no error is raised"*. Gitignored files are excluded by default (*"files matched by
  `.gitignore` rules are excluded from catalog results"*).
- **C7** — mdsmith presents the same catalog as an index for coding agents, one summary line per document. *Quoted*
  (S8, progressive-disclosure.md): *"A `<?catalog?>` in the agent file keeps one `summary` line per tracked doc. The
  agent skims the index, then opens only the files a task touches."*
- **C8** — adr-tools builds its table of contents by listing files whose names start with a number, sorting the list
  with `sort`, taking each title from the file's first line, and writing one bullet per file. *Quoted* (S9, code):
  `find $adr_dir | grep -E "^$adr_dir/[0-9]+-[^/]*\\.md" | sort`; `head -1 … | cut -c 3-`;
  `echo "* [$title]($link)"`.
- **C9** — *My reading* (S9 with S29): adr-tools calls `sort` with no `LC_ALL=C`, so its order can change with the
  machine's locale — the failure S29 warns about and that C2 reports Qwen Code hitting.
- **C10** — adr-log writes one line per ADR, either to stdout, to a new `index.md`, or between markers in an existing
  file. *Quoted* (S10): `* [ADR-0000](0000-example-1.md) - Example 1`; *"Edit the <input> file directly, injecting the
  log at <!-- adrlog -->."*
- **C11** — Claude Code's auto memory keeps an index file with one line per memory file, but Claude writes it; it is
  not generated by a program. *Quoted* (S1): *"`MEMORY.md` # Index, one line per memory, loaded into every session"*;
  *"Claude keeps `MEMORY.md` concise by moving detailed notes into separate topic files."*
- **C12** — llms.txt, an index file written for LLMs, fixes a line format of one Markdown link with optional notes.
  *Quoted* (S6): *"Each "file list" is a markdown list, containing a required markdown hyperlink `[name](url)`, then
  optionally a `:` and notes about the file."*
- **C13** — Karpathy's LLM Wiki keeps an `index.md` of one-line summaries that the LLM updates, not a script.
  *Quoted* (S7): *"each page listed with a link, a one-line summary"*, optional metadata *"like date or source
  count"*, and *"The LLM updates it on every ingest."*
- **C14** — Directory listing order is not stable and sort order depends on locale; the fix is an explicit
  locale-free sort. *Quoted* (S29): *"Most filesystems do not guarantee that listing files in a directory always
  results in the same order"*; *"Different locales have different orders of e.g. uppercase characters relative to
  lowercase characters"*; its example pipes through `LC_ALL=C sort -z`.
- **C15** — A build time written into output breaks reproducibility; a date, if needed, should come from version
  control. *Quoted* (S30): *"Timestamps make the biggest source of reproducibility issues"*; *"it's best to extract
  such a date from the revision control system or from a changelog."*
- **C16** — blurb names each fragment so that sorting file names sorts entries by time and names do not collide.
  *Quoted* (S13): `Misc/NEWS.d/next/<section>/<datetime>.gh-issue-<issue_number>.<nonce>.rst`; the nonce is the first
  6 characters of a base64 MD5 of the text; this means *"All entries in `Misc/NEWS` will be sorted by time"* and a
  filename clash is *"unthinkably unlikely"*.
- **C17** — reno orders notes by a topological walk of git history, which it calls deterministic but not
  predictable. *Quoted* (S16 usage, via WebFetch): *"deterministic, but not necessarily predictable or mutable"*; the
  design page states the goal *"we do want the ordering to be predictable and consistent."*
- **C18** — towncrier names a fragment by an issue id and a type, and groups output by type in a fixed category order;
  the tutorial states no sort rule inside a category. *Quoted* (S12): *"the filename consists of the issue/ticket ID
  (or some other unique identifier) as well as the ‘type’."*
- **C19** — Tools that must fit a budget rank by importance instead of by id: Repomix sorts by git change frequency by
  default, and Aider ranks files on a graph and keeps what fits. *Quoted* (S32): `--no-git-sort-by-changes` *"Don't
  sort files by git change frequency (default: most changed files first)"*; (S31) *"selecting the most important parts
  of the codebase which will fit into the active token budget."*
- **C20** — Go's convention marks a generated file with a header line that tools can match. *Quoted* (S26):
  `^// Code generated .* DO NOT EDIT\.$`, which *"must appear before the first non-comment, non-blank text in the
  file."*
- **C21** — Cog detects hand edits to generated output with a checksum and refuses to overwrite them. *Quoted* (S24):
  *"If the generated code is edited by a misguided developer, the next time cog is run, the checksum won't match, and
  cog will stop to avoid overwriting the edited output."*

### 2. When it runs and what runs it

- **C22** — Qwen Code regenerates the team index when a memory is written and, with sync turned on, at session start
  before pulling and committing. *Quoted* (S35): *"at session start Qwen best-effort syncs the `.qwen/team-memory/`
  directory: it rebuilds the shared `MEMORY.md` index, fast-forward-pulls collaborators' updates **first**, then
  commits your team-memory changes on top, and pushes **only that sync commit**"*. The write path calls
  `rebuildTeamAutoMemoryIndex` when `params.scope === 'team'` (S36, `metadata-migration.ts` line ~620, *quoted*).
  Sync is *"Off by default."*
- **C23** — Generators run at release, at one serial point, rather than on every branch: towncrier, Changesets,
  blurb, and GitLab's old YAML process. *Quoted*: towncrier *"will remove the news files (with `git rm`) and append the
  built news … and then stage the news file changes"* and *"leaves committing the changes up to the user"* (S12);
  `changeset version` *"consumes all changesets"* (S18); blurb's `Misc/NEWS` is *"rendered on demand (e.g. when
  building a release)"* (S13); GitLab *"collect those files, compile them to Markdown, remove them from the stable
  branch"* (S14).
- **C24** — mdsmith regenerates on `mdsmith fix`, reports staleness on `mdsmith check`, and can run the fix in a
  `pre-merge-commit` hook. *Quoted* (S8): *"Both regenerate their body on `mdsmith fix` and flag stale content on
  `mdsmith check`"*; *"`mdsmith pre-merge-commit install` adds a hook that runs `mdsmith fix` after a merge and
  re-stages the `.md` files."*
- **C25** — Go never runs its generators as part of a build; generation is explicit and the result is committed.
  *Quoted* (S26): *"Go generate is never run automatically by go build, go test, and so on. It must be run
  explicitly."* (That the output is committed is *my reading* of this sentence: a `go build` from a clone must work
  without running the generator.)
- **C26** — pre-commit fails a hook that changes files, which makes a generator in a pre-commit hook force the
  regenerated file into the commit; it also offers `post-merge` and `post-checkout` stages and a CI run over all files.
  *Quoted* (S25): *"The hook must exit nonzero on failure or modify files"*; output *"Files were modified by this
  hook"*; post-merge/post-checkout hooks *"must be set as `always_run: true` or they will always be skipped"*;
  *"adding `pre-commit run --all-files` as a CI step will ensure everything stays in tip-top shape."*
- **C27** — Claude Code's SessionStart hook adds a script's stdout to the context, on startup, resume, clear, compact
  and fork. *Quoted* (S2): *"Claude Code adds a SessionStart hook's plain-text stdout to Claude's context."* *My
  reading:* generating the index at session start from a hook would never put a generated file in git, but see C44
  for the hook's size cap.
- **C28** — Claude Code loads imported files at launch: an `@path` import in `CLAUDE.md` is a way to put a file in
  the start context. *Quoted* (S1): *"Imports … don't reduce its context cost, because imported files also load at
  launch."*
- **C29** — Codex and Gemini CLI load fixed instruction files by concatenation; neither page documents loading some
  other file such as an index on its own. *Quoted*: Codex *"concatenates files from the root down, joining them with
  blank lines"* (S3); Gemini CLI *"concatenates the contents of all found files, and sends them to the model with every
  prompt"* (S4). *My reading:* for those agents, `INDEX.md` reaches session start only through an instruction, an
  import, or a hook.
- **C30** — log4brains builds its ADR site in CI and publishes it, taking some metadata from git. *Quoted* (S11):
  *"publish them automatically as a static website"*; *"ADR metadata automatically guessed from its raw text and git
  logs"*.

### 3. Git: committed or not, and parallel branches

- **C31** — The shared generated file in the open-source world first broke on parallel branches, and the fix was one
  file per entry. *Quoted* (S14): *"we'd constantly see merge conflicts in the changelog when multiple merge requests
  attempted to add an entry to the list"*; placeholder lines left *"The problem was lessened, but not solved"*; the fix
  was *"Each changelog entry would be its own YAML file in a `CHANGELOG/unreleased` folder."* blurb exists to *"rid
  CPython core development of the scourge of `Misc/NEWS` conflicts"* (S13).
- **C32** — CPython stopped committing the combined file. *Quoted* (S13): *"`Misc/NEWS` could be deleted from the
  CPython repo and thereafter rendered on demand"*. *My reading* of the directory listing (S13, 2026-10-12):
  `python/cpython` `Misc/` holds `NEWS.d` and no `NEWS`.
- **C33** — GitLab later dropped entry files altogether and generates the changelog from a commit trailer; the docs
  give no reason for the change. *Quoted* (S15): *"Each list item, or **entry**, in our CHANGELOG.md file is generated
  from the subject line of a Git commit."*
- **C34** — Qwen Code commits its generated team index, and avoids merges by only fast-forwarding: a branch that has
  diverged is left alone. *Quoted* (S36, `team-memory-sync.ts`): *"`--ff-only` never creates a merge commit or a
  conflict; a diverged branch is left untouched and surfaced as `pull-failed`."* (S35): *"A diverged branch is left
  untouched … sync simply does nothing that session; resolve the divergence (`git pull`) and it resumes."* Neither
  source says what happens to `MEMORY.md` when a person merges two diverged branches by hand.
- **C35** — git's built-in `union` driver keeps lines from both sides without conflict markers, and git warns about
  it. *Quoted* (S19): *"take lines from both versions, instead of leaving conflict markers. This tends to leave the
  added lines in the resulting file in random order and the user should verify the result. Do not use this if you do
  not understand the implications."*
- **C36** — `union` silently brings back removed lines. *Quoted* (S20): *"if one side removes a line and the other adds
  in the same place, it will re-add the removed line"*; *"This will happen silently without warning, without any merge
  conflict being reported."* *My reading:* for `INDEX.md` a line disappears when an entry is superseded, so `union`
  could put a superseded entry back as active — the case K6 says must fail.
- **C37** — A custom merge driver is defined in git config, not in `.gitattributes`, so a fresh clone does not have it
  until something installs it. *Quoted* (S19): *"The definition of a merge driver is done in the `.git/config` file,
  not in the `gitattributes` file"*; the driver *"is expected to leave the result of the merge in the file named with
  `%A` … and exit with zero status if it managed to merge them cleanly"*. mdsmith says the same of its own install:
  *"Both are git-internal and untracked"* (S8). gh-aw removed a `merge=ours` line because without config it did
  nothing: *"`merge=ours` is not a built-in git merge driver — without `merge.ours.driver` configured it is inert,
  falsely implying generated-file conflicts are auto-resolved."* (S21).
- **C38** — mdsmith's merge driver resolves a conflict in a generated block by regenerating it. *Quoted* (S8): *"On a
  conflict it re-runs the directive and keeps the regenerated body, so the conflict never reaches you"*; it *"strips
  conflict markers in those blocks and runs `mdsmith fix` to regenerate them. It exits non-zero if any unresolved
  conflict markers remain."* In CI and merge queues it uses `ci-install`, which checks the committed `.gitattributes`
  and *"never writes the tracked file"*.
- **C39** — npm resolves a lockfile conflict by regenerating the lockfile, and commits the lockfile. *Quoted* (S22
  v10): *"This file is intended to be committed into source repositories"*. (S22 v6, *my summary* — the fetch tool
  would not return the section verbatim): since npm 5.7.0, fix `package.json` conflicts by hand and run `npm install`
  again, and npm writes a merged lockfile; `npm-merge-driver` automates this in git; one short quote: *"you will have
  to resolve that by hand and run `npm install` manually, even with the merge driver."*
- **C40** — Random or hash ids in file names keep parallel branches from creating the same file name. *Quoted*:
  reno identifies each note by *"the unique identifier (a 16-character hexadecimal SHA) embedded in its filename"*
  (S16); blurb's nonce (C16); Beads: *"Hash-based IDs (`bd-a1b2`) prevent merge collisions in
  multi-agent/multi-branch workflows."* (S33); log4brains: *"No required file numbering schema (i.e., `adr-0001.md`,
  `adr-0002.md`...): avoids git merge issues"* (S11).
- **C41** — GitHub can mark a committed generated file so its diff is collapsed. *Quoted* (S27): matching paths are
  *"ignored for the repository's language statistics and hidden by default in diffs."* gh-aw writes
  `.github/workflows/*.lock.yml linguist-generated=true` for its committed generated files (S21, *quoted*).
- **C42** — A merge queue checks each pull request against the base branch plus the pull requests ahead of it, so a
  check runs on the result that will actually land. *Quoted* (S28): changes are *"grouped into a `merge_group` with
  the latest version of the `base_branch`"* and *"changes from pull requests ahead of it in the queue"*, for
  *"ensuring the branch is never broken by incompatible changes."* *My reading:* this is where a "regenerate and
  compare" check would catch two branches that each merged cleanly but left `INDEX.md` out of step.
- **C43** — Two tools that started from files in git moved state elsewhere, keeping files as an export or a rebuildable
  index. *Quoted*: Beads' `.beads/issues.jsonl` *"is an export for viewers and interchange, not the source of truth or
  a backup"*, with Dolt's *"cell-level merge"* now underneath (S33); ai-memory: *"The database is a derived index that
  can always be rebuilt from the files."* (S34). reno added a cache file for copies without git history: *"a reno
  cache file that can be used to build release notes documents without the full Git history present"* (S17).

### 4. Size

- **C44** — Claude Code's SessionStart hook output is capped at 10,000 characters, with no setting to raise it; past
  that, only a 2,000-character preview reaches the context. *Quoted* (S2): *"capped at 10,000 characters"*; *"Claude
  Code saves the output to a file in the session directory and replaces it with the file path and a preview of up to
  the first 2,000 characters"*; *"Claude Code doesn't ask Claude to read the file, so keep anything Claude must always
  see within the cap"*; *"this cap has no setting or environment variable to raise it."*
- **C45** — Claude Code loads the first 200 lines or 25 KB of `MEMORY.md`, warns when the file is near the limit, and
  errors when it is over; that limit is for `MEMORY.md` only. *Quoted* (S1): *"The first 200 lines of `MEMORY.md`, or
  the first 25KB, whichever comes first, are loaded"*; near a limit it reminds Claude to *"keep one line per entry,
  move detail into topic files, and merge or drop stale entries"*; over it, *"everything past the limit is dropped on
  the next load"*; *"This limit applies only to `MEMORY.md`. Claude Code loads a CLAUDE.md file of up to 4 MiB in full
  and skips a larger file."* Guidance for CLAUDE.md: *"target under 200 lines per CLAUDE.md file."*
- **C46** — Qwen Code caps its generated index at 200 lines and 25,000 UTF-16 code units; under pressure it keeps
  short entries first, keeps the original order, drops whole lines, and appends a warning. *Quoted* (S35): *"Its
  generated body and the portion loaded into prompts share a limit of 200 lines and 25,000 UTF-16 code units"*;
  *"complete ordinary entries (up to 150 code units) get space before longer entries, and retained entries keep their
  original order. An entry that cannot fit is skipped whole, so its Markdown link is never cut in the middle."* (S36,
  `index-budget.ts`): the warning text is *"> WARNING: MEMORY.md is too large; only part of it was written. Keep index
  entries concise and move detail into topic files."*
- **C47** — Qwen Code also offers a structured mode that replaces the flat index with a tree and loads only the
  relevant subtree. *Quoted* (S35): *"The structured protocol replaces that with a hierarchical memory tree, injects
  only the subtree relevant to your current request, and gives Qwen a `search_memory` tool to pull full entries on
  demand"*.
- **C48** — Codex stops adding instruction files at 32 KiB by default; the limit is configurable. *Quoted* (S3):
  *"(32 KiB by default)"*; Codex *"stops adding files once the combined size reaches the limit defined by
  `project_doc_max_bytes`."* The page does not say whether a file that partly fits is cut.
- **C49** — Gemini CLI and the AGENTS.md page state no size limit for context files. *Found nothing* (S4, S5).
- **C50** — llms.txt keeps the file small by pushing detail behind links, and marks a section agents may drop.
  *Quoted* (S6): *"The file itself stays small enough to fit in context. The detail lives behind the links"*; the
  "Optional" section holds *"links an agent can skip when a shorter context is needed."* No byte or token limit is
  given.
- **C51** — Karpathy reports the single index working only at moderate scale. *Quoted* (S7): it *"works surprisingly
  well at moderate scale (~100 sources, ~hundreds of pages)"*.
- **C52** — mdsmith caps the number of files a catalog reads and, over the cap, leaves the old output instead of
  writing a partial one; it also checks file length and token budget. *Quoted* (S8): *"A `<?catalog?>` directive
  matches at most 10,000 files. When the glob resolves more than that limit, mdsmith emits a diagnostic and leaves the
  generated section unchanged"*; default rules `max-file-length` *"`max: 300` lines"* and `token-budget` *"`max:
  8000`, `mode: heuristic`"*.
- **C53** — When a combined file is too big, Repomix splits it into numbered parts on directory boundaries, and Aider
  keeps the top-ranked parts within a token budget. *Quoted* (S32): *"Split output into multiple numbered files"*;
  *"A single file or directory will never be split across multiple output files."* (S31): `--map-tokens` *"defaults to
  1k tokens"*, and the map *"will usually stay within that setting's value"*.

### 5. Checking that the index is in step

- **C54** — Kubernetes checks generated files by regenerating them in a clean git worktree of HEAD and failing if
  `git status` shows any change. *Quoted* (S23, code): `git worktree add -f -q "${_tmpdir}" HEAD`; `"$@"`;
  `diffs=$(git status --porcelain | wc -l)`; `if [[ ${diffs} -gt 0 ]]; then … git diff >&2 … return 1`. The comment:
  *"This function verifies whether generated files are up-to-date."*
- **C55** — Cog has a check mode that reports whether a run would change any file, and a diff option. *Quoted* (S24):
  *"use the `--check` option to run cog just to check that the files would not change if run again"*; *"The `--diff`
  option will show a unified diff of the change that caused `--check` to fail."* The page states no exit status.
- **C56** — mdsmith's `check` reports a stale generated block, and its `ci-install` fails when the committed
  `.gitattributes` has drifted. *Quoted* (S8): *"`mdsmith check` flags the index when it drifts; `mdsmith fix`
  rebuilds it"*; `ci-install` *"exits non-zero when `.gitattributes` is missing, has no managed block, or has
  drifted."*
- **C57** — Changesets and towncrier check that a branch added a fragment, not that a combined file is current.
  *Quoted*: `changeset status` exits `1` when *"there are changes to packages but no changesets are present"* (S18);
  towncrier check *"compares the current branch against `origin/main`"* (S12). *My reading:* this is a different
  check from K6's "regenerating changes nothing".
- **C58** — Claude Code checks the index's size at every write. *Quoted* (S1): *"After Claude writes to `MEMORY.md`,
  Claude Code measures the file against the 200-line and 25KB read limits."*

## What I looked for and did not find

- **A source saying what git does when `.gitattributes` names a merge driver that the clone's config does not
  define.** The gitattributes manual (S19) does not say; the gh-aw PR (S21) says `merge=ours` was *"inert"* in that
  case, which is one project's claim, not git's documentation.
- **What Qwen Code does with a committed `MEMORY.md` when a person merges two diverged branches.** S35 and S36 cover
  only the fast-forward path. I did not find the rebuild call inside `team-memory-sync.ts` itself; the docs (S35) say
  sync rebuilds the index, and the code search found the call in `metadata-migration.ts` (write path) only. GitHub
  code search may be incomplete.
- **A tie-break rule in mdsmith's sort** for two files with the same key value. Not stated in S8.
- **towncrier's order inside a category, and its `check` exit code.** Not stated on the pages read (S12).
- **Why GitLab moved from YAML entry files to commit trailers.** S15 does not say; S14 predates it.
- **Antigravity (agy) start-file size limit from a primary page.** A search summary reported a 12,000-character limit
  per rules file "from the official docs", but the official URL returned only a redirect notice to
  `/docs/rules?tab=ide`, which I did not fetch. Not verified — not used as a finding.
- **Any size limit for Gemini CLI context files or AGENTS.md** (C49).
- **A tool that writes an agent index into a committed file and regenerates it inside a git merge driver**, other
  than mdsmith (S8, 21 stars, adoption not measured). Qwen Code (S35/S36) commits a generated index but avoids merges
  rather than resolving them.
- **trinayhari/agents PR #1**, which a search result described as a `scripts/mem index` command that regenerates an
  `INDEX.md`: `gh` could not resolve the repository, so it is not used.
- **dune-common #266 on `merge=union`**: a search summary said the issue described `merge=union` breaking; the page
  itself (S37) does not mention `merge=union`. It only proposes per-entry `.yml` files or adding the entry just before
  merging. Not used beyond that.
- **Claude Code's `Read` tool line limit** when an agent reads `INDEX.md` with a tool rather than having it loaded:
  I did not search for it.

## Gaps and disagreements between sources

- **Commit the combined file, or not.** Qwen Code (C34), npm (C39), Go (C25) and gh-aw (C41) commit generated output;
  CPython (C32), log4brains (C30) and GitLab today (C33) do not, and build it on demand or at release. Towncrier and
  Changesets (C23) commit it, but only at release, so working branches never touch it.
- **What to do when two branches meet.** Three answers, each from a different source: avoid the merge
  (Qwen Code, fast-forward only, C34); regenerate inside the merge (mdsmith, C38; npm, C39); or take both sides
  (`union`, C35), which the git manual and a bug report warn against (C35, C36). The merge-driver answer depends on
  per-clone config that a fresh clone lacks (C37).
- **Order.** Qwen Code and mdsmith sort by path with a locale-free or explicit comparison (C2, C5); adr-tools uses
  locale-dependent `sort` (C8, C9); blurb sorts by a time stamp in the file name (C16); reno by git topology (C17);
  Repomix and Aider by importance (C19). Sorting by importance and truncating fits a budget; sorting by path keeps the
  file byte-stable. No source does both.
- **Size limits differ by agent and by how the file is loaded.** Claude Code: 200 lines / 25 KB for `MEMORY.md`, but
  4 MiB for a CLAUDE.md and its imports, and 10,000 characters for SessionStart hook output (C44, C45). Qwen Code:
  200 lines / 25,000 UTF-16 code units (C46). Codex: 32 KiB across all instruction files (C48). Gemini CLI and
  AGENTS.md: none stated (C49). *My reading:* the "strictest limit" of Rd3 depends on which load path is chosen, not
  only on which agents read the file.
- **What to do when the index is too big.** Qwen Code drops whole lines, short ones first, and warns (C46); Claude
  Code errors and asks for a rewrite (C45); mdsmith refuses to write a partial result (C52); Codex stops adding files
  (C48); Repomix splits (C53); llms.txt and Qwen's structured mode move detail behind links or a tree (C47, C50).
- **Who writes the index.** Claude Code's `MEMORY.md` (C11) and Karpathy's `index.md` (C13) are written by the model;
  Qwen Code's (C1) and mdsmith's (C5) are generated by code. Only the generated ones can be checked by regenerating
  (C54–C56).
- **Source quality.** mdsmith (21 stars) and ai-memory are small projects; Qwen Code's team memory is off by default
  (C22) and n is unknown for how often it is used. The vendor limits (S1, S2, S3, S35) are documented behaviour, not
  measured by me.
