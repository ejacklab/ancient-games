# Item 9, prefixes (agy)

Labels: **[EJ]** his words; **[design]** already in `SOURCE_OF_TRUTH.md`, the vision, or `REQUIREMENTS.md`; **[proposed]** mine. Line numbers refer to files as read on 2026-10-13.

## Recommendation

[proposed] Confirm `O-` for observation and `H-` for hypothesis, giving each of the five settled kinds a unique single-letter initial prefix (`D-`, `F-`, `H-`, `L-`, `O-`) that matches its `kind` field exactly.

[proposed] This completes the 1:1 mapping between file prefix and entry kind across all settled kinds without adding multi-letter prefixes, new folder levels, or special-cased validation rules.

## Three reasons

1. **The kinds are already settled in the vision, and separating their prefixes preserves distinct epistemic weight.**
   - [EJ] *"lessons, observations and hypotheses"* (`source-of-truth-memory-vision-statements.md` l.23, citing EJ 2026-10-12; `SOURCE_OF_TRUTH.md` l.66).
   - [EJ] *"ok the vision is confirm"* (`source-of-truth-memory-vision-statements.md` l.3).
   - [design] W2.2 assigns distinct definitions to all three: *"A lesson comes from a failure or a human correction. An observation records what was seen. A hypothesis is a guess, labelled as one."*
   - [design] W2 Fails if: *"Fails if kind holds any other value, or a guess is recorded under any kind but hypothesis."*
   - [proposed] A hypothesis is an unverified guess; a lesson is a verified correction from failure; an observation records what was seen. Collapsing them under a shared prefix (such as `L-`) would blur an unverified guess with a verified lesson before the file body is read, violating the vision's explicit separation of what was learned. Giving `H-` and `O-` their own prefixes makes the epistemic status obvious at a glance in `git diff`, directory listings, and `INDEX.md`.

2. **The `INDEX.md` generator draft is already built for `O-` and `H-` and relies on prefixes for deterministic sorting.**
   - [design] `REQUIREMENTS.md` B1.1: *"Only files directly in `project-memory/entries/` whose name matches `^[DFLOH]-[^/]+\.md$`. No subfolders, no dotfiles, not `INDEX.md`. The `O-` and `H-` prefixes are proposed in the design (W1.1); the script accepts them."*
   - [design] `REQUIREMENTS.md` B2.4: *"An active entry must also have: a kind from the five (decision, fact, lesson, observation, hypothesis); a file prefix that matches its kind; a `**Why:**` line; and a non-empty claim."*
   - [design] `REQUIREMENTS.md` B3.1: *"One line per active entry, sorted by file name in code-point order: `- [<id>](entries/<percent-encoded file name>) <kind>: <claim>`."*
   - [proposed] As noted in `runs/20261012-index-md-algorithm/proposals/claude.md` (l.38–39), sorting by filename in code-point order automatically groups `INDEX.md` lines by kind (`D`, `F`, `H`, `L`, `O`). Confirming `O-` and `H-` makes the draft generator in `REQUIREMENTS.md` valid as written, without changing the regex in B1.1 or the 1:1 prefix/kind check in B2.4. Dropping prefixes entirely would destroy this grouping unless a complex multi-field sort key was invented.

3. **Single-letter initials are the simplest mechanism: zero collision, zero added structure, and uniform across all five kinds.**
   - [design] W1.1 established single-letter prefixes: *"`D-` decision, `F-` fact and `L-` lesson"*.
   - [design] W1.1 explicitly proposed: *"plus `O-` observation and `H-` hypothesis (proposed; the design leaves these two open)"*.
   - [design] `SOURCE_OF_TRUTH.md` layout line (l.143): *"File prefixes for observations and hypotheses: `O-` and `H-`, proposed in W1.1."*
   - [proposed] The initial letters of all five kinds—**D**ecision, **F**act, **H**ypothesis, **L**esson, **O**bservation—are mutually distinct ASCII characters. There is no letter clash. Confirming `O-` and `H-` requires no two-letter disambiguation, no new metadata tags, and no exceptions in tooling. It cleanly closes the only open note in W1.1 under the owner's rule of keeping memory simple.

## Text changes

### Design (`SOURCE_OF_TRUTH.md`)

**Header**: add a revision note after the item-8 block. [proposed]
> **Revised 2026-10-13, prefixes (item 9):** the prefixes `O-` for observation and `H-` for hypothesis are confirmed (W1.1). Every kind has a unique single-letter initial prefix matching its kind. Four-reader round: `runs/20261013-sot-item9-prefixes/`.

**Where it is put**: change the layout block, one line, and drop the note below it.
- Old [design]: `entries/           one file per entry: D- decision, F- fact, L- lesson`
- New [proposed]: `entries/           one file per entry: D- decision, F- fact, H- hypothesis, L- lesson, O- observation`
- Old [design] (l.143): `File prefixes for observations and hypotheses: O- and H-, proposed in W1.1.`
- New [proposed]: delete this sentence; all five prefixes are now settled and listed directly in the layout line and W1.1.

**W1.1**
- Old [design]: *"The prefixes are `D-` decision, `F-` fact and `L-` lesson, plus `O-` observation and `H-` hypothesis (*proposed*; the design leaves these two open). There is no runbook prefix (W3.6)."*
- New [proposed]: *"The prefixes are `D-` decision, `F-` fact, `H-` hypothesis, `L-` lesson and `O-` observation, each matching the entry's `kind` (W2). There is no runbook prefix (W3.6)."*
- Old [design] Fails if: *"a lint over `entries/` finds a missing field or section, or a reviewer finds two claims in one entry."*
- New [proposed]: *"a lint over `entries/` finds a missing field or section, a reviewer finds two claims in one entry, or an entry file has a prefix outside the five or mismatched with its `kind`."*

### Generator requirements (`docs/index-md/REQUIREMENTS.md`)

**B1.1**
- Old [design]: *"Only files directly in `project-memory/entries/` whose name matches `^[DFLOH]-[^/]+\.md$`. No subfolders, no dotfiles, not `INDEX.md`. The `O-` and `H-` prefixes are *proposed* in the design (W1.1); the script accepts them."*
- New [proposed]: *"Only files directly in `project-memory/entries/` whose name matches `^[DFLOH]-[^/]+\.md$`. No subfolders, no dotfiles, not `INDEX.md`. The prefixes match the five settled kinds in W1.1."*
- **Fails if** [design, unchanged]: *"an untracked entry gets a line, a file outside B1.1 gets a line, or a path with a space or a non-ASCII character is read wrongly in either mode."*

**Other places checked** [proposed]:
- `source-of-truth-memory-vision-statements.md` names kinds, not prefixes, so it needs no change.
- `SOURCE_OF_TRUTH.md` W2.2 and W5.2 already list lessons, observations, and hypotheses; no text changes needed.
- `REQUIREMENTS.md` B2.4 already checks the five kinds and prefix/kind matching; no text changes needed.

## Id form (optional)

[proposed] My recommendation does not depend on the id form.
[proposed] The single-letter prefix and hyphen delimiter (`^[DFLOH]-`) cleanly isolate the kind whether `<id>` is a timestamp, hash, or random nonce (G4.1). Sorting by filename in code-point order (B3.1) partitions entries by prefix letter first, so the internal structure of `<id>` does not affect kind grouping or prefix validation.

## What could go wrong

[proposed] **Case: unretired, speculative hypotheses accumulate and exhaust the `INDEX.md` size cap.**

1. An agent concludes a task and follows W5.2: it converts speculative debugging notes from its journal into an active entry: `H-0041-possible-sqlite-lock.md` (`kind: hypothesis`).
2. Later tasks solve the problem via another path or prove the guess irrelevant, but never touch `H-0041`.
3. Because age alone never expires an entry (K4.2) and no automated drift subagent exists (removed 2026-10-12), `H-0041` remains `status: active` indefinitely.
4. Under K6.1 and B3.1, every active entry must receive a line in `INDEX.md`. As speculative `H-` and `O-` entries accumulate across tasks, `INDEX.md` grows towards `MAX_LINES` (200 lines, B4.1).
5. When `INDEX.md` exceeds the cap, pre-commit checks fail (G2.1, C1.2), blocking all memory commits until EJ manually intervenes to retire the stale hypotheses.

[proposed] *Mitigation:* standing instructions in `AGENTS.md` should clarify that raw, transient guesses belong in the task journal (`work/<task-id>/journal/`, K5.1), and only hypotheses that govern pending multi-task investigations should be elevated to `H-` entry files.

## Questions for EJ

1. **Should post-code findings have distinct single-letter prefixes (`O-` and `H-`, my recommendation), or should all post-code findings share `L-` with the distinction kept in frontmatter `kind:` only?**
   - If they share `L-`, W1.1 retains only three prefixes (`D-`, `F-`, `L-`), the layout line does not add `O-`/`H-`, and B2.4 relaxes strict prefix-to-kind exact matching.
2. **Should active hypotheses (`H-`) be listed in `INDEX.md` (the current B3.1 default), or excluded from `INDEX.md` until confirmed as facts or lessons to conserve index headroom (Rd3.1)?**
   - If excluded, B3.1 adds a filter condition (`kind != 'hypothesis'`), and `REQUIREMENTS.md` B3.1 and C2 tests change.
