# INDEX.md — proposal (codex)

## The algorithm

**My proposal; not measured.** Use one repo-local script, `scripts/memory_index.py`, to generate a tracked, flat `project-memory/INDEX.md`. Generation runs synchronously as part of writing memory and integrating branches. It has a write mode and a read-only check mode.

Finding prefixes refer to the reviews by [claude](../lit-review/claude.md) (`C`), [codex](../lit-review/codex.md) (`X`), and [opencode](../lit-review/opencode.md) (`O`). This proposal has not been implemented or tested.

1. **Record the actual reading limits.** Keep `project-memory/index-limits.json` in git. Whoever configures an agent’s session-start reading records its agent, loading route, limit value, unit, and supporting documentation or measurement. Each applicable limit is a separate constraint; bytes, lines and character counts are not converted into one guessed number. For a shared loading budget, record the other files charged to it so the check can count their current size too.

   The script supports physical lines, UTF-8 bytes, Unicode characters and UTF-16 code units. An unknown limit, unsupported measurement unit, missing profile or nonpositive ceiling produces an error. The design’s “about 24 KB and 200 lines” remains an example, not the configuration.

2. **Define the commands and their input snapshots.**
   - `python scripts/memory_index.py --write` reads the current worktree and updates its index.
   - `python scripts/memory_index.py --check` reads that worktree and compares without writing.
   - `python scripts/memory_index.py --check --staged` reads paths and blobs from Git’s staging area, including the staged limit configuration and index. It checks the proposed commit, rather than unstaged edits.

   These modes use the same parsing, filtering, ordering and rendering functions. Success returns `0`; any validation, overflow or freshness failure returns `1` with a diagnostic.

3. **Discover the authoritative files.** Enumerate the Markdown entry files directly inside `project-memory/entries/`, including untracked files in worktree mode and newly staged files in staged mode. Reject nested Markdown entry files, symlinks and unreadable inputs rather than silently excluding them. The expected directory must exist; an existing directory containing no entries produces an empty index.

   Inputs are the entries, the limit configuration and any files needed to calculate a shared loading budget. `INDEX.md`, `work/`, `journal/` and `.cache/` are outside entry discovery.

4. **Parse the fields needed for indexing.** Read each entry as UTF-8. Parse its opening `---`-delimited YAML header without executable constructors, rejecting duplicate YAML keys. Require a nonempty string `id`, a recognised `kind`, and a `status` of `active`, `superseded` or `retired`. Reject duplicate ids across entry files.

   A malformed header is an error, including on an inactive entry: otherwise the script cannot reliably determine its membership. This is indexing validation, not a claim that every W1 field or every entry’s meaning has been checked.

5. **Extract each active entry’s existing claim.** For `status: active`, take the body text after the YAML header and before the first section marker `**Why:**` at the beginning of a line. Confirm that a subsequent `**How to apply:**` section exists. A marker may be followed by its section’s text on the same line.

   The claim begins directly after the header; an entry title is not part of this serialization. Require a nonempty claim. Trim its edges and replace each run of Unicode whitespace with one ASCII space. Preserve the remaining text, including both sentences when present. Sentence count and whether the body contains one claim remain reviewer checks.

6. **Filter and render deterministically.** Include exactly the entries with `status: active`. Sort them by the UTF-8 byte sequence of their repo-relative paths, using `/` as the separator.

   Render a fixed generated-file comment, a fixed `# Project memory index` heading, a blank line, then one physical line per entry:

   ```markdown
   - [<id>](entries/<percent-encoded-filename>) — <kind>: <claim>
   ```

   Markdown-escape the id and claim as literal text. Percent-encode the UTF-8 filename for the relative link. Use UTF-8 without a byte-order mark, LF line endings and one final newline. The header identifies the write command and says the file is generated. Include no generation timestamp.

7. **Measure the complete candidate before writing.** Count the rendered header, blank lines, escaped text, links and final newline against every configured constraint. For a shared budget, add the current size of the other files charged to that budget.

   If the candidate exceeds a limit, report the reader and route, measurement unit, measured value and ceiling. Leave the existing index untouched and return failure. A leftover index is explicitly stale after such a failure; memory-dependent work and handoff wait for repair.

   The writer can correct unnecessarily long source wording while preserving its meaning. Duplicate consolidation or lifecycle changes follow the existing entry rules. If the complete active listing still cannot fit, EJ must decide a design change. The generator performs no automatic shortening, selection, retirement or restructuring.

8. **Publish only a successful complete result.** In write mode, compare the candidate bytes with the existing index. If identical, finish without rewriting. Otherwise write a temporary file beside `INDEX.md`, close it, then atomically replace `INDEX.md`.

   Parsing and size failures leave the existing file untouched. The temporary file is removed on failure. Each writer works in its own worktree and completes this synchronous command before its next memory mutation; this proposal adds no cross-process locking service.

9. **Run generation as part of the write operation.** The agent or person who creates or changes an entry runs `--write` immediately after saving its complete contents. For decisions and facts, this happens before the governed code is changed. Applying the same procedure to every entry change also covers lessons, retirement, supersession and completed decisions.

   Put that procedure in `AGENTS.md` and the human contribution instructions. The writer adds the entry’s required `changed:` line; the script changes only the generated index. A failed generation is a failed memory-write procedure, not a successful write awaiting a later repair. No watcher, background subagent or service is introduced.

10. **Commit the source and generated result together.** The writer stages the intended entry changes and corresponding `INDEX.md`, then runs `--check --staged`. The script itself stages, commits and pushes nothing.

    A staged check catches partial-staging mistakes: a correct worktree index can still disagree with the entries actually staged. A configured pre-commit hook may call this command, but the documented procedure and build check remain necessary because hooks can be absent or bypassed.

11. **Regenerate after branch integration.** The agent or person performing a merge, rebase or cherry-pick resolves authoritative entry conflicts first and stages those resolutions. Resolve conflicts in the generator or limit configuration before using them too.

    Then run `--write`, replacing any conflicted index wholesale with the result from the integrated entries. Stage that result and run `--check --staged` before completing the integration. Apply this procedure after clean textual integrations too: a clean merge does not establish index freshness or consistency between claims.

12. **Expose the freshness check wherever it is needed.** In check mode, compare the complete candidate byte-for-byte with the index from the same snapshot. A missing or different index fails with a unified diff and the write command.

    The build and CI run `--check` on the checked-out revision, including the integrated revision when that is what will land. The first session-start instruction runs `--check` before reading `INDEX.md`; failure triggers repair before relying on it. CI reports failure instead of pushing a repair commit.

    **Check authorship and limit:** this check would be written by the implementer of the proposed script; no such check was run for this report. Equality establishes agreement with that implementation. It does not independently establish correct extraction, truthful claims, complete reader-limit measurements or agreement with the code. Rd5 still governs checking memory before acting.

## Three supporting reasons

1. **The output can be reproduced without another summary-writing step.** Parsed metadata, explicit filtering and locale-independent ordering have concrete precedents. Skipping identical rewrites reduces needless file churn. Taking the authored body claim preserves this design’s source of truth; introducing a separate description would create another value to maintain. **My reading; the particular body-extraction rule is my proposal.** (findings: C2, C3, C5, X2, X3)

2. **Write-time generation and source-first merge resolution serve the accepted timing and clone requirements.** Regeneration inside a memory mutation has prior art, and generated artifacts have documented resolution procedures that rebuild from resolved inputs. Keeping the index tracked makes it immediately available in a clone; resolving entries before regenerating avoids treating either branch’s index as authoritative. **My reading.** (findings: X9, C22, X19, C39, O25)

3. **A complete failure is easier to diagnose than a plausible partial index.** Prior art supports refusing partial output and providing read-only regenerate-and-compare checks. Separate source validation matters because malformed content can reproduce perfectly. These mechanisms support a visible overflow error and a useful freshness check without implying semantic verification. **My reading.** (findings: C52, X31, X33, O39, O40)

## Six must-not-dos

1. **Users must not edit `INDEX.md` by hand.** Correct the entry and regenerate; generated-output edits cannot become a second authority. (finding: X19)

2. **The script must not omit an active entry to meet a size budget.** Deduplicating descriptions, ranking entries or dropping whole lines would break K6.1’s complete listing. (findings: C4, C46, X7)

3. **The script must not vary its output with locale, filesystem enumeration order, modification time or the current clock.** Identical authoritative inputs need identical output bytes for the freshness comparison. (findings: C2, C14, C15, X8)

4. **Users must not accept a `union` merge as the final index resolution.** It can reorder lines and silently restore a line removed through supersession. (findings: C35, C36)

5. **The script must not consume or delete entry files after generation.** Changelog tools sometimes remove processed fragments; this design retains entries under K4.1. (findings: X18, C23)

6. **Users must not rely on a Git hook as the sole regeneration trigger.** Hooks need installation, can be bypassed, and post-merge hooks miss conflicted merges. (findings: O13, O15, X14)

## Design changes

These are proposed changes or completions, not changes already accepted by EJ:

- **W1.2 — specify the header serialization:** opening `---`-delimited YAML, with duplicate keys rejected. The design names header fields but does not currently define their machine-readable serialization.
- **W1.3 — specify the extraction boundary:** the claim begins directly after the header and ends at the line beginning `**Why:**`; `**How to apply:**` follows. This makes body extraction explicit without adding a summary field.
- **K6 — complete the open tool and trigger:** name the single script and the writer’s synchronous invocation. Specify that regeneration failure blocks proceeding with the memory-write procedure until repaired. Running after every entry change extends the timing stated in K6.2.
- **Rd3.1 — separate the fit requirement from its build check:** define fit against every applicable, verified loading-route constraint. Record those constraints in the tracked configuration and make overflow an explicit failure.
- **W6 — complete the open merge responsibility:** whoever performs the integration resolves source conflicts and regenerates the index. Use separate worktrees for simultaneous writers so filesystem writes are isolated too.

**Requirement-check of Rd3.1:** source, can it fail, level, basis and links pass. **One thing fails:** fitting and checking are separate requirements. **Unit fails:** “strictest” does not define how different units or shared loading budgets are compared. **Weak words fails:** the example is approximate and the actual ceilings remain open. The revisions above separate the requirements and define the comparison; they do not supply unmeasured ceilings.

**Open question for EJ before implementation:** which agents and loading routes will read this project’s `INDEX.md`, and what verified limits apply to each? Missing limits remain open rather than becoming guessed defaults.

**Not measured:** this proposal’s generation latency, conflict frequency, practical corpus capacity and effect on agent recall. Review those after implementation with real entries and session-start reads.

## Where I disagree with the other reviews

- **Opencode O30/O33:** “aim under 200 lines” is guidance for a particular instruction file, not an established universal loading ceiling. Claude C44–C49 and codex X25–X26 distinguish limits by file and loading route.
- **Opencode O42:** immediate local regeneration and failing CI are compatible. K6.2 does not require CI to push repairs; they operate at different points in the procedure.
- **Opencode’s reported search gaps:** claude C5 and codex X3–X5 identify frontmatter-driven index generators; codex X19 identifies an explicit generated-memory merge policy. Those mechanisms were found across the combined reviews.
- **Overflow approaches in claude C46/C47 and opencode O35–O37:** selection, hierarchy and an optional tail do not preserve both a complete flat listing and a bounded file. For this proposal, overflow is a reported failure requiring repair or an explicit design decision.
