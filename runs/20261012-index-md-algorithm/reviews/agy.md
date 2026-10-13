# Review of proposals/claude.md (agy)

## Verdict
ACCEPT WITH FIXES. The deterministic generator and git-snapshot check are architecturally sound, but the proposal requires fixes for working-tree checkability, hook bypass on fast-forward/rebase, write-mode exit codes, test suite integration, and fragile header/claim parsing.

## Problems
| # | where | what | failure case | severity | fix (one line, if obvious) |
|---|---|---|---|---|---|
| 1 | Step 1 / Step 9 | Check mode with no arguments reads only git objects from the staging area (`git ls-files -s`), preventing verification of the working tree. | An author modifies entries in the working tree without staging them, then runs `python3 tools/memory_index.py --check` before committing; the check inspects the clean staging area against HEAD, exits 0, and falsely indicates the working tree is valid. | breaks | Default `--check` to verify the working tree; use `--staged` / `--cached` for commit-hook execution. |
| 2 | Step 8 | Write mode writes the full oversized `INDEX.md` to disk but exits with status 1, breaking command chaining and scripting. | A writer runs `python3 tools/memory_index.py && git add project-memory/INDEX.md`; when the index exceeds the limit, the file is updated on disk but the script exits 1, causing the shell to abort before staging and leaving an uncommitted dirty working tree. | breaks | Exit 0 after writing the file in write mode (printing a size warning); enforce the exit 1 failure in `--check`. |
| 3 | Step 11 / Design change 4 | `pre-commit` and `pre-merge-commit` do not fire on fast-forward merges, rebases, or cherry-picks, and the hook exits 0 when a commit touches no memory files. | A branch carrying a drifted index committed without hooks is fast-forward merged into `main` (`git merge feature`); no hook runs, and subsequent code-only commits exit 0, leaving an out-of-step `INDEX.md` committed on `main` indefinitely. | breaks | Wire `python3 tools/memory_index.py --check HEAD` into the test suite (`pytest`) so every test run validates index freshness. |
| 4 | Design change 4 | The proposal deletes Rd3.1's requirement that "the build checks it" under the premise that the repo has no build, ignoring the repo's existing test runner. | A contributor runs `pytest` before submitting changes; because the check exists only in bypassable git hooks, test execution passes even if `INDEX.md` violates Rd3.1's limits. | gap | Retain Rd3.1's check by adding a test case in `tests/test_memory_index.py` that invokes `--check HEAD`. |
| 5 | Step 3 / Step 4 | Claim parsing strictly requires a line starting with verbatim `**Why:**` and collapses all preceding lines into the claim, failing on formatted headings. | An entry formats the rationale as `## Why:` or `**Why:** ` (with trailing whitespace); the parser fails to find `**Why:**`, treats the entire body as a claim or flags a missing section, and aborts with exit 1. | breaks | Match `^\s*(#{1,6}\s+)?\*\*Why:\*\*` case-insensitively and strip markdown heading markers (`#`) from the extracted claim. |
| 6 | Step 3 / Step 4 | Naive line-based frontmatter parsing between `---` delimiters breaks if horizontal rules (`---`) appear in the Markdown body. | An entry uses a horizontal rule (`---`) to separate sections in its body; the parser treats the rule as the closing frontmatter delimiter, misclassifying body text as header fields and failing validation. | breaks | Ensure frontmatter begins strictly on line 1 and terminates on the first subsequent line matching `^---$`. |
| 7 | Step 4 / Step 6 | Validation does not check that the filename prefix matches header `kind`, or that the filename contains `id`. | A file named `D-002-constraint.md` specifies `kind: fact`; Step 2 sorts it under the `D-` block by filename, but Step 6 renders `- [D-002](entries/D-002-constraint.md) fact: ...`, corrupting the kind-grouped layout of the index. | breaks | Validate in Step 4 that the filename strictly matches `<kind-prefix>-<id>-*.md`. |
| 8 | Step 6 | Filenames matching `^[DFLROH]-[^/]+\.md$` containing spaces or special characters are rendered into Markdown links without URL encoding. | An entry named `D-001-api auth.md` is rendered as `[D-001](entries/D-001-api auth.md)`, producing an invalid Markdown hyperlink in standard Markdown parsers. | minor | Apply `urllib.parse.quote` to link targets or forbid whitespace in entry filenames in Step 1. |
| 9 | Reason 1 (line 151) | Finding C2 is cited for showing that sorting by file name puts parallel additions on different lines. | A reviewer relies on C2 as evidence that parallel additions merge cleanly without conflict; in fact C2 only demonstrates that code-unit sorting prevents cross-machine locale churn, leaving merge behavior unmeasured. | minor | Remove the C2 citation from line 151, retaining it as an unmeasured reading. |
| 10 | Step 3 / Reason 3 | The proposal refuses to cap individual claim lengths ("Nothing is shortened"), allowing verbose claims to rapidly exhaust the index byte budget. | Multiple authors write detailed two-sentence claims of 350+ characters; 70 entries exceed 25 KB, triggering an early size limit failure and blocking commits. | gap | Cap the rendered claim in `INDEX.md` at a fixed character threshold (e.g. 150–200 characters, following Qwen Code C1). |

## Citations checked
| finding id | what the proposal says it shows | does it? (yes / partly / no) |
|---|---|---|
| C2 | Code-unit sorting prevents cross-machine locale churn (lines 38, 186); sorting by file name puts parallel additions on different lines (line 151) | partly (yes for preventing locale churn across machines; no for parallel branch additions avoiding merge conflicts) |
| C3 | Skip write when generated index is byte-identical to existing file (line 78) | yes |
| C4 | Qwen Code's normalized-exact deduplication with "(also: …)" lists breaks one line per entry (line 247) | yes |
| C9 | `sort` without `LC_ALL=C` causes locale-dependent collation order (line 157) | yes |
| C14 | Directory listing order is unstable and collation depends on locale (lines 38, 157, 186) | yes |
| C15 | Build timestamps in generated output break reproducibility (lines 68, 157, 186) | yes |
| C16 | blurb combines datetime, issue ID, and nonce in filenames to eliminate collisions (line 195) | yes |
| C20 | Marker comment names the command that rebuilds the file (line 69) | partly (C20 documents Go's `// Code generated .* DO NOT EDIT.` convention, but does not specify naming the rebuild command; that comes from O2 and O39) |
| C25 | Go generator output is explicit and committed rather than run during build (line 149) | yes |
| C28 | Claude Code loads `@path` imported files into start-of-session context (line 199) | yes |
| C31 | GitLab and CPython moved from a shared file to one file per entry to end merge conflicts (line 146) | yes |
| C32 | CPython stopped committing the combined NEWS file, rendering it on demand (line 150) | yes |
| C34 | Qwen Code commits team memory index and uses `--ff-only` sync to avoid merges (lines 149, 248) | yes |
| C35 | git `union` merge driver leaves added lines in random order without conflict markers (line 183) | yes |
| C36 | git `union` silently re-adds lines deleted by one side (lines 181, 183) | yes |
| C38 | mdsmith automates conflict resolution by regenerating on conflict (lines 132, 152) | partly (mdsmith automates this via a custom git merge driver, which the proposal explicitly rejects) |
| C39 | npm resolves lockfile conflicts by regenerating the lockfile (lines 132, 152) | yes |
| C40 | Hash-based, nonce, or random IDs prevent branch merge collisions (line 195) | yes |
| C44 | Claude Code SessionStart hook stdout is capped at 10,000 characters with a 2,000-character preview (line 199) | yes |
| C45 | Claude Code caps `MEMORY.md` loading at 200 lines / 25 KB, errors on oversized write, and drops excess on next load (lines 166, 170, 189) | yes |
| C46 | Qwen Code caps index at 200 lines / 25,000 code units and drops whole lines under pressure (lines 166, 189) | yes |
| C47 | Qwen Code structured mode uses a hierarchical tree loaded on demand (lines 167, 249) | yes |
| C51 | Karpathy reports flat single index functioning at moderate scale (~100 sources) (line 173) | yes |
| C52 | mdsmith refuses to write partial index when file count exceeds 10,000 (line 166) | yes |
| C53 | Repomix splits oversized output into numbered files (line 167) | yes |
| C54 | Kubernetes verifies generated files by running generation in a clean worktree of HEAD and asserting zero diff (lines 93, 159, 161) | yes |
| C55 | Cog provides `--check` to detect changes and `--diff` to display drift (lines 93, 159) | yes |
| X4 | Understory falls back silently to filenames on frontmatter parsing errors (line 192) | yes |
| X8 | Towncrier date derives from system clock unless pinned by `--date` or `SOURCE_DATE_EPOCH` (lines 68, 157, 187) | yes |
| X15 | pre-commit stashes unstaged changes so hooks execute only on staged content (line 121) | partly (X15 describes pre-commit stashing; the inference that unstaged entries would leak into committed output is the author's reading) |
| X17 | GitLab and CPython moved to one file per entry (line 146) | partly (X17 describes Towncrier's news fragments vs single changelog file, while C31 covers GitLab and CPython) |
| X19 | FKF normative merge procedure resolves topic files first, then regenerates the index (lines 132, 152) | yes |
| X20 | mkdocs-gen-files generates files on the fly during build without committing them (line 150) | yes |
| X21 | git `union` driver fails to establish canonical ordering or agreement with authoritative inputs (line 183) | yes |
| X25 | Claude Code oversized memory writes succeed but return an error requesting rewrite (line 166) | yes |
| X26 | Claude Code 200-line / 25 KB limit is documented specifically for native `MEMORY.md` (lines 169, 240) | yes |
| X27 | FKF enforces domain-scoped indexes and description character ceilings (line 167) | yes |
| X31 | Cog `--check` verifies files would not change if regenerated (lines 93, 159) | yes |
| X33 | FKF validates source frontmatter separately from output freshness (lines 56, 192) | yes |
| X3, X5 | FKF and OKF extract index descriptions from authored frontmatter description fields (line 244) | yes |
| O1 | Dominant prior art injects generated blocks into handwritten files rather than dedicated standalone files (line 243) | yes |
| O2 | doctoc embeds machine-readable `DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc` pragma (line 69) | yes |
| O5 | Reproducible Builds bit-by-bit stability enables regenerate-and-diff verification (line 156) | yes |
| O6 | Locale collation (`LC_COLLATE`) introduces sorting nondeterminism unless pinned (lines 38, 157, 187) | yes |
| O7 | Timestamps (`LC_TIME`), encoding, and timezones break build determinism (lines 68, 157, 187) | yes |
| O16 | `post-checkout` fires on branch switches, checkouts, and clones (line 232) | yes |
| O17, O41 | Claude Code `PostToolUse` hook fires on `Edit|Write` actions for immediate agent-side regeneration (line 229) | yes |
| O20, O42 | CI can push regenerated files back to PR branches rather than failing the run (line 237) | yes |
| O21 | Read-time generation (mdbook-toc) conflicts with offline fresh-clone readability (line 150) | yes |
| O23, O26 | `merge=binary` declares conflict on non-line-mergeable files, while `git rerere` reuses resolutions (line 234) | yes |
| O24 | `union` merge silently preserves deleted entries as stale lines (line 183) | yes |
| O25 | Machine-maintained files needed on clone without external tooling should be committed (line 149) | yes |
| O30, O33 | Published startup instruction limits are line-based (Claude Code 200 lines, Cursor 500 lines) (line 240) | yes |
| O31 | Oversized context files cause silent instruction ignoring rather than hard failures (lines 171, 189) | yes |
| O35 | aider optimizes repository maps by token budget ranking and selection (lines 167, 243) | yes |
| O36 | Monorepos utilize hierarchical nested instruction files to maintain bounded startup size (line 167) | yes |
| O37 | llms.txt uses `## Optional` sections for secondary links that can be skipped under short context (line 243) | yes |
| O38 | Kubernetes `verify-generated.sh` clones HEAD into a clean worktree and asserts zero diff (lines 93, 159) | yes |
| O39 | Freshness check output includes the exact regeneration command to run (lines 69, 93) | yes |
| O40 | Single CLI tool implements both write mode and non-modifying verification exit codes (lines 93, 160) | yes |
| O43 | Source header schema linting is distinct from index freshness verification (lines 56, 192) | yes |

## What holds up
- **Standard-library single script:** Implementing `tools/memory_index.py` using Python 3's standard library with zero external dependencies satisfies portability and clone-readiness without third-party toolchains.
- **Deterministic pure function:** Omitting volatile timestamps, build dates, and entry counts while sorting strictly by Python unicode code points eliminates collation churn across operating systems and locales (C2, C14, C15, O6, O7, X8).
- **Dual-mode CLI:** Unifying generation and byte-level comparison into one script with `--check` prevents generator and verifier implementations from drifting out of sync (O40, C55, X31).
- **Exclusion of `merge=union`:** Strictly prohibiting `merge=union` avoids silent re-addition of superseded entries and randomized line orders (C35, C36, O24).
- **Rejection of SessionStart hook stdout:** Avoiding delivery of `INDEX.md` through Claude Code SessionStart stdout respects the hard 10,000-character cap and 2,000-character preview truncation (C44).
- **Fail-loud size policy:** Halting memory commits when limits are reached rather than silently dropping or truncating active entries preserves K6.1's requirement for one line per active entry (C45, O31).
- **Decentralized IDs:** Requiring hash, nonce, or timestamp IDs prevents merge clashes between parallel branches without centralized coordination (C16, C40).
