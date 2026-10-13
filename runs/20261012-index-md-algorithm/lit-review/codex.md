# INDEX.md generation — literature review (codex)

## Sources

Research date: 2026-10-12. This review inspected primary documentation and source code; it did not execute generators, benchmark alternatives, or change repository files. GitHub branch links identify the inspected implementation, but are not immutable commit snapshots.

| id | source (name + URL) | what it is | date or version, if shown |
|---|---|---|---|
| S0 | [Source-of-Truth Memory Design](/home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md) | Accepted local design; no public URL supplied | Accepted and revised 2026-10-12 |
| S1 | [Towncrier introduction](https://towncrier.readthedocs.io/en/stable/index.html) | Open-source tool combining separate news fragments | Documentation 26.9.0 |
| S2 | [Towncrier tutorial](https://towncrier.readthedocs.io/en/stable/tutorial.html) | Fragment format, rendering and Git workflow | Documentation 26.9.0 |
| S3 | [Towncrier command reference](https://towncrier.readthedocs.io/en/stable/cli.html) | Build, reproducibility and checking commands | Documentation 26.9.0 |
| S4 | [Towncrier pre-commit integration](https://towncrier.readthedocs.io/en/stable/pre-commit.html) | Commit and CI hooks | Documentation 26.9.0 |
| S5 | [miku-indexgen README](https://github.com/igapyon/miku-indexgen) | Open-source directory index generator expressly intended for AI agents | Living README; release example 1.6.2 |
| S6 | [mkdocstrings recipes](https://mkdocstrings.github.io/recipes/) | Generates reference pages and a Markdown navigation index | No version shown |
| S7 | [Open Knowledge Format specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) | Markdown knowledge bundles with YAML frontmatter and directory indexes | Version 0.2 |
| S8 | [Understory indexer source](https://github.com/thecodacus/understory/blob/main/packages/core/src/okf/indexer.ts) | Concrete Markdown memory-index generation algorithm | `main`; emits OKF 0.1 |
| S9 | [Understory mutation source](https://github.com/thecodacus/understory/blob/main/packages/core/src/okf/knowledge-base.ts) | Write-time regeneration, mutation queue and optional Git commits | `main` |
| S10 | [Understory README](https://github.com/thecodacus/understory/blob/main/README.md) | Agent memory implementation and session-start overview | References OKF 0.1 |
| S11 | [Understory validator source](https://github.com/thecodacus/understory/blob/main/packages/core/src/okf/validate.ts) | Frontmatter and link validation | `main` |
| S12 | [Fab Knowledge Format](https://shll.ai/fab-kit/fkf/) | Generated Markdown memory indexes and explicit merge policy | FKF 0.1 |
| S13 | [Fab command reference](https://shll.ai/fab-kit/commands/) | Generation and read-only checking CLI | Fab 2.24.9; captured 2026-09-10 |
| S14 | [Claude Code memory documentation](https://code.claude.com/docs/en/memory) | Agent-loaded memory index and overflow behavior; vendor documentation | Living documentation |
| S15 | [llms.txt proposal](https://llmstxt.org/) | Markdown discovery index for agents | Version 2; modified 2026-08-10 |
| S16 | [Changesets CLI documentation](https://changesets.dev/guide/cli) | YAML-frontmatter Markdown fragments combined into changelogs | Living documentation |
| S17 | [Changesets automation documentation](https://changesets.dev/guide/automating) | GitHub Actions generation and release PR workflow | Examples use action v2 |
| S18 | [pre-commit documentation](https://pre-commit.com/) | Staged-content checks and CI execution | Living documentation |
| S19 | [Git hook reference](https://git-scm.com/docs/githooks) | Commit and merge hook lifecycle | Manual last updated in Git 2.54.0 |
| S20 | [Git attributes reference](https://git-scm.com/docs/gitattributes) | Built-in and custom merge drivers | Living manual |
| S21 | [Cog command documentation](https://cog.readthedocs.io/en/latest/running.html) | Generated-text freshness checking | Documentation 3.6.0 |

## Findings

### 1. Building the lines

**X1 — my reading, S5.** miku-indexgen scans local files, parses Markdown YAML frontmatter, copies a documented whitelist of metadata, and extracts a summary from the first heading or leading body text while excluding frontmatter. It supports `status`, but its README does not document filtering entries to `status: active`. [Source](https://github.com/igapyon/miku-indexgen)

**X2 — quoted, S5.** miku-indexgen specifies: “`files[]` entries are sorted by normalized relative path using UTF-16 code unit order.” It also excludes the current run’s generated index files from the input listing, avoiding self-inclusion. [Source](https://github.com/igapyon/miku-indexgen)

**X3 — my reading, S12.** FKF derives index tables from folder contents and each file’s required `description` frontmatter, with dates excluded from domain indexes. This establishes prior art for deterministic rendering from an authored summary field rather than generating a new summary during each rebuild. [Source](https://shll.ai/fab-kit/fkf/)

**X4 — my reading, S8.** Understory sorts immediate directory entries with `localeCompare`, skips hidden entries and reserved filenames, reads `title` and `description` from frontmatter, and emits linked Markdown bullets before a separate subdirectory section. It falls back to filenames on parsing errors, does not filter by lifecycle status, and does not enforce single-line descriptions; its locale-dependent comparison also leaves cross-environment ordering unestablished. [Source](https://github.com/thecodacus/understory/blob/main/packages/core/src/okf/indexer.ts)

**X5 — quoted, S7.** OKF says: “Entries SHOULD include the description from the linked concept’s frontmatter.” Its index structure groups links and descriptions under headings and can include links to subdirectories. [Source](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)

**X6 — my reading, S6.** The mkdocstrings recipe explicitly sorts discovered source paths, converts them to relative Markdown paths, accumulates navigation entries, and writes `SUMMARY.md` from that navigation object. This is executable prior art for discovery → explicit ordering → relative links → generated Markdown navigation, although its inputs are source modules rather than memory entries. [Source](https://mkdocstrings.github.io/recipes/#generate-a-literate-navigation-file)

**X7 — my reading, S2.** Towncrier reads a fragment’s identifier and type from its filename and uses its body as the displayed content; the tutorial demonstrates grouping by type and combining identical descriptions associated with different issue IDs. That deduplication differs from K6.1’s requirement for one line per active entry. [Source](https://towncrier.readthedocs.io/en/stable/tutorial.html)

**X8 — my reading, S3.** Towncrier’s generated date comes from an explicit `--date`, then `SOURCE_DATE_EPOCH`, then the system clock. Its reproducibility controls show why identical fragment files alone do not guarantee identical output when generation also consumes changing environmental inputs. [Source](https://towncrier.readthedocs.io/en/stable/cli.html#reproducible-builds)

### 2. When it runs and what runs it

**X9 — my reading, S9.** Understory’s write and patch methods await an `afterMutation` step that regenerates the changed directory’s index and its ancestors, appends a log entry, and optionally commits. Regeneration is part of the write operation, providing a closer timing analogue to K6.2 than release-time generation. [Source](https://github.com/thecodacus/understory/blob/main/packages/core/src/okf/knowledge-base.ts)

**X10 — my reading, S3.** Towncrier exposes an on-demand `build` command, a draft mode that renders without writing files, and `--keep` to retain processed fragments. These are documented execution modes, not evidence that Towncrier automatically runs after each source-file edit. [Source](https://towncrier.readthedocs.io/en/stable/cli.html)

**X11 — my reading, S4.** Towncrier documents both checking and updating hooks for commit-time or CI execution, including an update example that retains fragments. The generator and its trigger are therefore separate configurable parts of the workflow. [Source](https://towncrier.readthedocs.io/en/stable/pre-commit.html)

**X12 — my reading, S16.** Changesets separates adding a Markdown fragment with YAML frontmatter from running `changeset version`, which consumes accumulated changesets to update versions and changelogs. Contributors can record source fragments before the combined output is generated. [Source](https://changesets.dev/guide/cli)

**X13 — my reading, S10.** Understory regenerates its compact seed overview for every new session and refreshes the tool description after its own memory mutations; its README says out-of-band edits are picked up on the next session. This is session-start generation of an agent overview, distinct from rebuilding a committed Markdown index. [Source](https://github.com/thecodacus/understory/blob/main/README.md#seed-memory)

**X14 — my reading, S19.** Git’s `pre-merge-commit` runs after a successful merge and before creating the merge commit, and can be bypassed; `post-merge` cannot change the merge outcome and does not run when merging fails with conflicts. Neither hook alone supplies a procedure for resolving a generated-file conflict that has already stopped the merge. [Source](https://git-scm.com/docs/githooks)

**X15 — quoted, S18.** pre-commit explains that it “only runs on the staged contents of files by temporarily stashing the unstaged changes while running hooks.” It also documents `pre-commit run --all-files` for CI, distinguishing commit-snapshot checks from checks over the working tree. [Source](https://pre-commit.com/)

**X16 — my reading, S17.** Changesets’ documented automation runs on pushes to `main`, creates a versioning PR, and groups concurrent workflow runs by branch. This is prior art for generating combined artifacts after contributor branches land, but does not provide immediate regeneration inside each contributor’s worktree. [Source](https://changesets.dev/guide/automating)

### 3. Git: committed or not, and parallel branches

**X17 — quoted, S1.** Towncrier contrasts fragments with “one single file which developers all write to and produce merge conflicts.” Its conflict-avoidance mechanism is separate contributor input files rather than simultaneous authoring of the combined changelog. [Source](https://towncrier.readthedocs.io/en/stable/index.html)

**X18 — my reading, S2.** Towncrier’s production command stages the generated news file and removes processed fragments with `git rm`, leaving the commit to the user. This makes the combined output a tracked release artifact; deleting consumed inputs would conflict with this project’s retained-entry requirement. [Source](https://towncrier.readthedocs.io/en/stable/tutorial.html#producing-news-files-in-production)

**X19 — quoted, S12.** FKF’s merge procedure starts with “Resolve the conflicts in the topic files only” and ends with “Take its output wholesale as the resolution.” Between those steps it reruns the generator, providing explicit prior art for resolving authoritative inputs first and replacing the conflicted generated index. [Source](https://shll.ai/fab-kit/fkf/#merge-policy-regenerate-never-hand-merge-normative)

**X20 — my reading, S6.** mkdocs-gen-files creates navigation and reference files during documentation builds without writing them into the source documentation directory or requiring them to be versioned. This avoids contributor conflicts on those outputs, but does not itself provide an already-present, clone-readable `INDEX.md`. [Source](https://mkdocstrings.github.io/recipes/#generate-pages-on-the-fly)

**X21 — quoted, S20.** Git warns that the `union` merge driver can leave added lines “in random order” and says the user should verify the result. Combining both branches’ text therefore does not establish canonical ordering or agreement with the authoritative entries. [Source](https://git-scm.com/docs/gitattributes#_built_in_merge_drivers)

**X22 — my reading, S20.** A custom Git merge driver is configured in Git configuration, while `.gitattributes` selects it for paths; the driver receives temporary ancestor/current/other files and writes its result into the current-file argument. A committed attributes file alone does not carry the driver’s executable configuration into a fresh clone. [Source](https://git-scm.com/docs/gitattributes#_defining_a_custom_merge_driver)

**X23 — my reading, S9.** Understory serializes mutations through a promise queue belonging to one `KnowledgeBase` instance. That code supports ordered writes within that instance, but does not establish coordination across separate processes, branches or worktrees. [Source](https://github.com/thecodacus/understory/blob/main/packages/core/src/okf/knowledge-base.ts)

**X24 — my reading, S14.** Claude Code’s native auto memory is machine-local, and worktrees of one repository share its memory directory. It is useful index-format prior art, but its default storage does not satisfy this design’s fresh-clone portability requirement. [Source](https://code.claude.com/docs/en/memory#storage-location)

### 4. Size: when the index outgrows the start-file limit

**X25 — quoted, S14.** Claude Code loads “The first 200 lines of `MEMORY.md`, or the first 25KB, whichever comes first.” An oversized write still succeeds, but returns an error requesting a rewrite, and content beyond the loading limit is omitted next time. [Source](https://code.claude.com/docs/en/memory#how-it-works)

**X26 — my reading, S14.** The documentation explicitly confines that limit to native `MEMORY.md`; it is not documented there as a general limit on every Markdown file an agent opens. Moving detail into topic files reduces index size, but does not eliminate the growth of an index that retains one line for every entry. [Source](https://code.claude.com/docs/en/memory#how-it-works)

**X27 — my reading, S12.** FKF uses a domains-only root index and per-domain file indexes, and applies description limits of 500 characters as guidance and more than 1,000 as a blocking condition. These are that project’s hierarchy and thresholds, not a supported replacement for Rd3’s strictest-agent limit. [Source](https://shll.ai/fab-kit/fkf/)

**X28 — my reading, S8.** Understory summarizes each subdirectory using its recursive concept count, distinct types and up to three example titles, while linking to the directory for detail. This gives a concrete deterministic progressive-disclosure algorithm, but does not enforce an overall byte or line budget. [Source](https://github.com/thecodacus/understory/blob/main/packages/core/src/okf/indexer.ts)

**X29 — quoted, S15.** llms.txt describes its `Optional` section as “links an agent can skip when a shorter context is needed.” The proposal also supports indexes at subpaths and fetching linked detail on demand, establishing selective and hierarchical discovery rather than guaranteed enumeration of every item in one startup file. [Source](https://llmstxt.org/#format)

**X30 — my reading, S5.** miku-indexgen shortens long frontmatter descriptions to 256 UTF-16 code units, including the trailing ellipsis. That bounds one metadata value; its README does not document a total-index budget or an overflow policy preserving all entries. [Source](https://github.com/igapyon/miku-indexgen)

### 5. Checking: whether the index is in step with the entries

**X31 — quoted, S21.** Cog’s maintainers document `--check` as “Check that the files would not change if run again,” with `--diff` to show a failing comparison. This is direct prior art for K6’s regenerate-and-compare freshness check; equality does not independently establish that the extraction algorithm is correct. [Source](https://cog.readthedocs.io/en/latest/running.html#continuous-integration)

**X32 — my reading, S13.** Fab documents a read-only `docs-index --check` returning 0 for clean output, 1 for benign drift or blocking findings, and 2 for destructive loss, with optional JSON diagnostics. Its current command reference identifies `memory-index` as a deprecated alias for `docs-index docs/memory`. [Source](https://shll.ai/fab-kit/commands/#fab-docs-index)

**X33 — my reading, S12.** FKF separately validates malformed frontmatter and offending descriptions because a bad source description can reproduce byte-identically in the generated index. Its maintainers explicitly distinguish source-content validation from generated-output freshness. [Source](https://shll.ai/fab-kit/fkf/#32-description-required-curated)

**X34 — my reading, S3.** Towncrier’s `check` checks whether a feature branch adds a news fragment, and skips that check when the main news file changes. This check was written for fragment-presence policy; it does not establish that the combined file equals current generator output. [Source](https://towncrier.readthedocs.io/en/stable/cli.html#towncrier-check)

**X35 — my reading, S11.** Understory’s validator checks parseable frontmatter and a non-empty type, and warns about missing title/description and certain broken links. The inspected validator does not regenerate indexes or compare their bytes, so its conformance result does not establish index freshness. [Source](https://github.com/thecodacus/understory/blob/main/packages/core/src/okf/validate.ts)

## What I looked for and did not find

- I searched the web and GitHub for generated agent-memory indexes, Markdown frontmatter indexing, fragment aggregation, generated-file merge handling, and freshness checks. I found close components and an explicit memory-index merge policy, but no inspected project implementing this exact combination of `id`, `kind`, body claim, active-only filtering, immediate regeneration and a flat startup index.
- I did not find a comparative benchmark establishing a **best** algorithm under these requirements. Conflict frequency, regeneration latency and agent recall quality were **not measured** in this review.
- I did not find a source-backed rule for extracting this design’s one- or two-sentence body claim while excluding **Why:** and **How to apply:**, preserving its meaning, and rendering one physical line. The closest sources use frontmatter descriptions or generic leading-text extraction.
- I did not find a demonstrated overflow algorithm that retains one line per active entry in a single bounded startup file for an indefinitely growing corpus. Hierarchical indexes and selective loading exist, but change that flat enumeration contract.
- I did not establish the current strictest loading limit across all agents intended to read this project’s `INDEX.md`. Claude’s native memory limit is documented, but X26 limits its applicability.
- I did not find an inspected implementation proving cross-worktree atomicity or consistent snapshots while entries are being changed. Understory’s queue establishes only the narrower scope in X23.
- Some miku-indexgen raw-source requests failed; its findings here rely on its accessible README. A search also surfaced Phoenix issue #1718 about a failed post-merge index update, but the full issue could not be opened, so it is excluded from the findings.

## Gaps and disagreements between sources

- **My reading — no established winner.** The sources support different parts of the problem: miku-indexgen supplies explicit path ordering, Understory supplies write-time regeneration, FKF supplies generated-memory merge handling, and Cog supplies regeneration equality checks. These observations do not constitute comparative proof or a stage-2 proposal.
- **My reading — summary location remains unsettled.** FKF and OKF consume authored frontmatter descriptions; miku-indexgen can derive leading-text summaries. The [accepted design](/home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md) places the claim in the body, so these are different input contracts, not interchangeable extraction rules.
- **My reading — timing changes the conflict surface.** Towncrier and Changesets defer combined-output generation; Understory regenerates on writes. Deferral avoids frequent contributor edits to the combined artifact, while K6.2 requires regeneration immediately after decisions and facts.
- **My reading — tracking is a material tradeoff.** Build-time virtual indexes avoid tracked-output conflicts, while tracked indexes can be read directly from a clone. The former does not by itself satisfy Rd1.2’s already-readable memory index.
- **My reading — deterministic generation does not prevent textual conflicts.** FKF supplies a regeneration-based resolution procedure. Git’s union merge combines text without establishing the canonical result, and a clean textual merge does not prove freshness.
- **My reading — overflow is still a design question.** Claude truncates oversized native memory, llms.txt permits selective loading, and Understory uses hierarchy. None establishes unchanged compliance with both K6.1’s complete flat listing and Rd3’s bounded startup file.
- **My reading — validation policies differ.** Understory tolerates malformed files during indexing, whereas FKF blocks specified malformed inputs. Neither policy is automatically the missing-field and active-status policy required here.
- **My reading — version distinctions matter.** The inspected OKF specification is 0.2, while Understory identifies and emits 0.1; FKF’s specification uses `memory-index`, while its newer command reference calls it a deprecated alias. Those versions and command names should remain explicit when carrying findings into stage 2.
- **Not measured — verification limits.** External maintainers wrote the checks described above; I inspected their documentation or implementation and did not run them. Freshness equality, schema validity, merge correctness and the truth of an entry’s claim are separate properties, and no inspected check establishes all of them.
