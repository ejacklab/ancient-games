# Review of proposals/claude.md (codex)

## Verdict

**ACCEPT WITH FIXES.** My reading: the deterministic generator is a sound core, but Git coverage, input parsing, filename handling and the size policy need fixes before the proposal satisfies the accepted design.

## Problems

The failure cases below are my analysis of the proposed steps. No generator exists to test; I inspected the local Git 2.43 manuals and ran only an in-memory probe of the filename regex and whitespace transformation.

| # | where | what | failure case | severity | fix (one line, if obvious) |
|---|---|---|---|---|---|
| 1 | Steps 11, 13; design change 4 | The two hooks do not check every operation that combines branches. A clean rebase can produce a snapshot that fails Rd3 without invoking either proposed check. | Let the line limit be N and the base index contain N−1 lines. One branch adds a decision and another adds a runbook at sufficiently separated locations; each branch has N lines and passes. A clean rebase combines them into N+1 lines without the proposed gate checking the result. | breaks | Specify verification of the resulting snapshot after rebases and other operations outside these hooks. |
| 2 | Step 11 | The acknowledged bypass is not repaired by the next ordinary hooked commit: the early exit can return success while inherited memory remains stale. This limits the enforcement claim. | Commit an active entry without its index update using `--no-verify`, then make a code-only commit with hooks enabled. The hook exits 0 because the staged memory diff is empty, and the new commit still contains the wrong index. An explicit `--check HEAD` would fail. | breaks | State the guarantee narrowly, or check the complete snapshot at the acceptance point that requires current memory. |
| 3 | Steps 7, 11 | Changes to the generator or its limits can invalidate the index without touching `project-memory/`, so the hook skips them. | Correct the renderer’s link escaping, or lower `MAX_BYTES` below the existing index size, and commit only `tools/memory_index.py`. The hook returns 0 although regeneration or the size check now fails. | breaks | Include the generator and its policy inputs in the hook’s triggering paths. |
| 4 | Step 3; assumptions; “no changes to W1.2” | W1 specifies header fields but does not settle frontmatter delimiters or scalar syntax. The proposal imposes a new input contract, and stripping surrounding quotes does not implement YAML scalar parsing. | An otherwise conforming entry with an undelimited header is rejected. If YAML frontmatter is intended, `status: active # current` is rejected as an unknown status, while `id: "D-\u0061"` is copied as an escape sequence rather than decoded to `D-a`. | gap | Have EJ settle the header grammar and record that decision; parse or explicitly reject the supported scalar forms. |
| 5 | Step 4; must-not 4 | Required-field “presence” does not specify whether an empty value fails. Non-empty claims are checked explicitly, but non-empty ids are not. | An entry has `id: ""`, valid kind and status, and a non-empty claim. A presence-only implementation accepts it and renders an empty link label, contradicting “do not emit a line with a hole in it.” | gap | Explicitly reject an empty id after parsing. |
| 6 | Steps 1, 6 | Filenames are inserted into Markdown destinations without encoding. The admitted filename set also includes newlines, which can defeat one physical line per active entry. | `D-a-cache#ttl.md` passes the regex but its link points to a fragment of `D-a-cache`; `D-a-fix timeout.md` produces an invalid ordinary link destination. A filename containing a newline produces multiple physical lines. Regeneration equality can pass all three outputs. | breaks | Encode link destinations and define handling of control characters in filenames. |
| 7 | Step 1, check mode | The specified Git listings quote unusual paths unless NUL-delimited output is requested. The proposal does not specify decoding that representation. | With default `core.quotePath`, `D-a-決策.md` appears quoted with escapes in `git ls-files -s` and `git ls-tree`. Treating that output as the actual pathname makes `git show` fail or makes discovery omit the entry, although write mode reads it successfully. | gap | Use NUL-delimited Git listings and parse paths separately from metadata. |
| 8 | Step 3 | Collapsing every whitespace run can alter the claim’s literal content, rather than merely putting it on one line. | The claim `Use two spaces (` followed by an inline code span containing two spaces, then `) between records.` becomes a code span containing one space. The generated index changes the recorded separator while its freshness check passes. | breaks | Preserve whitespace inside literal content; collapse only layout whitespace. |
| 9 | Step 9, suggested fix | The repair command rebuilds from the working tree, although the failing check examines staged entries. It therefore does not reliably repair a partially staged commit. | Stage claim A, then leave claim B unstaged in the same entry. Following the printed command stages an index for B alongside the staged entry containing A; the check fails again. | gap | Explain that entries and index must represent the same snapshot, and account for partial staging in the repair instructions. |
| 10 | Step 7; reason 3; design change 4 | The strictest applicable limit remains unsettled beyond choosing an exact byte number. The agent set, loading paths, aggregate budgets and the status of the line limit must also be established. | If only Claude Code loads the index through a `CLAUDE.md` import, adopting the native `MEMORY.md` 200-line cap would reject 201 short lines despite the different import limit reported in C45. Other loading paths may instead impose an aggregate budget. | gap | Settle the readers, loading paths and applicable exact limits before closing Rd3. |
| 11 | Steps 8, 14; design change 4 | Writing an oversized index and rejecting its commit does not cover the next session reading that working tree. The proposal preserves enumeration but leaves the Rd2/Rd3 startup behavior unresolved after failure. | An entry makes the index exceed the applicable limit. Write mode replaces `INDEX.md` and exits 1; a new session in that worktree then follows Rd2.1 and reads the oversized file before any commit occurs. | gap | Leave post-overflow session behavior explicitly open for EJ alongside the overflow policy. |
| 12 | Step 14; design change 4 | “Until EJ decides” introduces an approval condition that is not reconciled with W4’s permission for anyone to change entries. The check also cannot establish that EJ decided. | A contributor shortens a claim or retires an entry, bringing the index under the limit. The check passes before EJ has decided, although the stated policy says memory commits stop until that decision. | gap | Clarify whether EJ decides only policy changes or also approves ordinary size-reducing edits, and reconcile that with W4. |
| 13 | Reason 3, third bullet | O31 does not establish that an entire long file is ignored “without notice.” It describes instructions getting lost in a bloated `CLAUDE.md`, which differs from the documented native-memory truncation in C45. | An oversized imported instruction file suffers reduced instruction adherence without being omitted. The proposal presents this as silent file omission, overstating the evidence for that loading path. | minor | Describe O31 as instruction loss; confine documented truncation to the paths the cited findings cover. |

## Citations checked

These comparisons check the local finding texts supplied to this review, not the underlying external sources anew.

| finding id | what the proposal says it shows | does it? (yes / partly / no) |
|---|---|---|
| C2, C14, O6 | Explicit ordering avoids filesystem and locale variation. | **yes** — Python code-point ordering is a different comparator from Qwen’s code-unit ordering, but is explicitly deterministic. |
| C2, reason 1 | Sorting puts parallel additions on different lines and supports usually clean merges. | **partly** — C2 supports stable ordering; it does not measure merge frequency. The proposal labels the merge claim as its reading. |
| C3 | Avoid byte-identical rewrites. | **yes** |
| C15, O7, X8 | Time-dependent output can defeat reproducibility. | **yes** |
| C20, O2, O39 | Mark generated output and identify how to rebuild it. | **partly** — C20 supports a generated marker, O2 a rerun instruction, and O39 a repair command in diagnostics rather than an in-file marker. |
| X33, O43 | Source validation and freshness checking are separate checks. | **yes** — neither establishes that this proposed parser is correct. |
| C54, O38 | Regenerate and compare in an isolated Git snapshot. | **partly** — Kubernetes checks a complete clean worktree, including its generator; the proposal reads entry and index objects while executing the working-tree script. |
| C55, X31 | Regeneration equality and a diff are established freshness checks. | **yes** |
| O40 | One generator can expose a non-writing check mode with a failing exit code. | **yes** |
| X15 | Check staged content without incorporating unstaged edits. | **yes** — the proposal uses a different mechanism to obtain that isolation. |
| X19, C38, C39 | Resolve authoritative inputs, then regenerate the derived conflict resolution. | **yes** |
| C31, X17 | Separate contributor input files avoid shared-file authoring conflicts. | **yes** — they do not prove that committing the combined output eliminates conflicts. |
| O25, C25, C34 | Committed generated artifacts have prior art and support clone readability. | **partly** — C34 directly covers a committed index; O25 concerns Cargo’s lockfile; C25 explicitly labels commitment as an inference. |
| C32, O21, X20 | Some projects generate combined output at release, build or read time. | **yes** |
| O5 | Bitwise reproducibility supports an exact freshness comparison. | **yes** — “pure function of entries” is the finding’s stated interpretation, not the quoted general definition. |
| C9 | An unpinned shell sort can depend on locale. | **yes** |
| C46 | Qwen’s native index drops whole entries under budget pressure. | **yes** — the finding reports UTF-16 code units, not UTF-8 bytes. |
| C45, X25 | Oversized native `MEMORY.md` content is omitted on subsequent loading. | **yes** — this does not establish the same behavior for `INDEX.md` loaded through another path. |
| C52 | mdsmith refuses a partial result when its catalog input count exceeds its cap. | **partly** — this is an input-file-count cap, not a rendered startup-index size cap. |
| C53 | Repomix splits output and Aider selects within a budget. | **yes** |
| O35, O36, X27, C47 | Ranking and hierarchical discovery are existing alternatives. | **yes** — none proves unchanged compliance with this design’s flat startup listing. |
| X26 | Claude’s native memory cap is not a general limit on every Markdown file. | **yes** — it does not establish an impossibility theorem for every way of reducing index size. |
| O31 | A long file is ignored without notice. | **no** — the finding describes instruction loss in bloated context. |
| C51 | Karpathy reports moderate-scale operation at approximately 100 sources. | **yes** — source count does not establish index row count or headroom for this design. |
| C36, C35, O24, X21 | Union merging can resurrect removed content or disrupt ordering. | **yes** |
| X4 | Understory falls back on malformed input and lacks relevant validation guarantees. | **yes** |
| C40, C16 | Nonces and hashes reduce filename collisions across branches. | **yes** — this is collision avoidance, not an absolute uniqueness proof. |
| C44 | SessionStart stdout has a cap and substitutes a preview and file reference beyond it. | **yes** |
| C28 | Claude supports startup imports from `CLAUDE.md`. | **yes** |
| O17, O41 | Claude tool hooks and commit hooks are different trigger mechanisms with coverage limits. | **yes** — the findings acknowledge the bypasses. |
| O16 | `post-checkout` fires on branch movement, clone and worktree creation. | **partly** — its timing is supported; the finding does not prove regeneration dirties every checkout. |
| O23, O26 | Binary merge behavior and rerere exist. | **yes** — whether they are needed here remains a design judgment. |
| O20, O42 | CI can regenerate and push, or fail; choosing between them is policy. | **yes** |
| O30, O33 | Opencode identifies a 200-line figure as the strictest it found. | **partly** — O30 quotes guidance for `CLAUDE.md`; it is not simply an application of the native `MEMORY.md` hard cap. |
| O1, O35, O37 | Delimited-region injection, ranking and optional tails are existing patterns. | **yes** |
| X3, X5 | FKF and OKF derive descriptions from frontmatter. | **yes** |
| C4, C34, C47 | Deduplication, fast-forward-only synchronization and hierarchical loading differ from this proposal’s contract. | **yes** |

## What holds up

- One shared renderer, deterministic ordering, fixed encoding and regeneration equality provide a clear freshness check.
- Active-only selection directly serves K6.1. A claim without `**Why:**` is explicitly rejected; I found no problem with that case.
- Checking staged objects avoids leaking unstaged entry edits into the proposed commit.
- Regenerating a conflicted index after resolving its entries follows the cited merge policy.
- Keeping full W1 lint separate is explicitly stated; this index check should not be described as proving full entry conformance.
- I found no additional unnecessary mechanism to remove. Deferring caches, hierarchy, custom merge drivers and agent-specific generation hooks fits the simplicity rule.
- For the single byte-equality freshness rule, the requirement-check criteria **source, one thing, unit, can it fail, weak words, level, basis and links** pass. Its bounded claim is that the selected snapshot equals this renderer’s output.
- **Not measured:** generator behavior, Git-history counterexamples, merge frequency, startup recall and usable headroom. Codex wrote the small regex/whitespace probe; it confirms those transformations only and is not independent evidence of implementation correctness.
