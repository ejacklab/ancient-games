# Item 9, prefixes (claude)

Labels: *EJ's* = his words; *design* = already in `SOURCE_OF_TRUTH.md`, the vision or the `INDEX.md` draft;
*proposed* = mine. *Verified* marks something I read in the code myself.

## Recommendation

*Proposed:* Confirm `O-` observation and `H-` hypothesis, so that every one of the five kinds has one prefix letter,
its initial, and the prefix always matches the entry's `kind`.

*Proposed, considered and not chosen:* dropping prefixes altogether. The prefix repeats the `kind` field, so it is a
duplicate, and the script has to cross-check the two (B2.4). But `D-`, `F-` and `L-` are settled, the script that
checks them is built and accepted, and the prefix does one job the header cannot do (reason 3). Removing it is a
larger change than item 9, so I do not recommend it.

## Three reasons

1. **The same rule for all five kinds, with no exception.**
   - *Design (W2.2):* "A **lesson** comes from a failure or a human correction. An **observation** records what was
     seen. A **hypothesis** is a guess, labelled as one."
   - *EJ's (vision):* "what was **learned** after: lessons, observations and hypotheses."
   - *Design (INDEX.md draft, B2.4):* an active entry must have "a `kind` from the five (decision, fact, lesson,
     observation, hypothesis); a file prefix that matches its `kind`".
   - *Proposed:* the kinds are settled at five, and three of them already have a letter. Leaving two without one would
     need a second naming rule just for those two. One letter per kind, the kind's initial, needs nothing to learn,
     and the five initials D, F, L, O and H do not clash.

2. **Nothing new to build: the text catches up with what is already accepted.**
   - *Design (INDEX.md draft, B1.1):* "Only files directly in `project-memory/entries/` whose name matches
     `^[DFLOH]-[^/]+\.md$` … The `O-` and `H-` prefixes are *proposed* in the design (W1.1); the script accepts
     them."
   - *Verified:* `tools/memory_index.py` lines 42–50 map `O` to `observation` and `H` to `hypothesis` already.
   - *Proposed:* confirming is a text-only change. Dropping prefixes, or giving `O`/`H` some other form, would change
     an accepted script and its tests.

3. **The `H-` prefix keeps a guess labelled wherever its file name appears.**
   - *Design (What will not be put in):* "Guesses not labelled as a hypothesis."
   - *Design (W2, Fails if):* "a guess is recorded under any kind but hypothesis."
   - *Design (Rd5.3):* "When a decision or fact no longer matches the code, the reader does not change the entry."
   - *Proposed:* a file name is shown where the header is not: in `ls entries/`, `grep -l`, `git log --stat`, a link,
     or a merge conflict. With `H-` and `O-`, a reader sees there that an entry is a guess or a sighting and not a
     requirement, so it is not a decision or fact that Rd5.3 checks against the code. With `D-*` and `F-*`, the
     entries Rd5 applies to can be listed without opening any file.

## Text changes

### `docs/memory-system/SOURCE_OF_TRUTH.md`

**Status block, a new paragraph after "Revised 2026-10-13, runbooks (item 8)"** (*proposed*; EJ's quote goes where
the placeholder is, and is not invented):

> **Revised 2026-10-13, prefixes (item 9):** `O-` observation and `H-` hypothesis are confirmed, so each of the five
> kinds has one prefix letter (EJ: *"<EJ's words>"*; readers' round `runs/20261013-sot-item9-prefixes/`).

**Where it is put: the layout.** Current line:

```
  entries/           one file per entry: D- decision, F- fact, L- lesson
```

New lines (*proposed*), wrapped the way the `AGENTS.md` line is:

```
  entries/           one file per entry: D- decision, F- fact, L- lesson, O- observation,
                     H- hypothesis
```

**Where it is put: the paragraph after the layout.** Delete the last sentence, "File prefixes for observations and
hypotheses: `O-` and `H-`, proposed in W1.1." (*proposed*; it only marked the gap). The paragraph then reads:

> The project's existing documents (requirements, architecture) stay in `docs/`; memory links to them instead of
> copying them.

**W1.1.** Current:

> - **W1.1** Each entry is one file: `project-memory/entries/<prefix>-<id>-<slug>.md`. The prefixes are `D-` decision,
>   `F-` fact and `L-` lesson, plus `O-` observation and `H-` hypothesis (*proposed*; the design leaves these two open).
>   There is no runbook prefix (W3.6).

New (*proposed*; the last sentence depends on Question 1):

> - **W1.1** Each entry is one file: `project-memory/entries/<prefix>-<id>-<slug>.md`. The prefix is one letter for
>   each kind (W2): `D-` decision, `F-` fact, `L-` lesson, `O-` observation and `H-` hypothesis. It matches the
>   entry's `kind`. There is no runbook prefix (W3.6). An entry's kind, and so its prefix, never changes: a hypothesis
>   that is confirmed, or an observation that becomes a lesson, gets a new entry that supersedes it (K4.1).

**W1, Fails if.** Current:

> - **Fails if** a lint over `entries/` finds a missing field or section, or a reviewer finds two claims in one entry.

New (*proposed*):

> - **Fails if** a lint over `entries/` finds a missing field or section, or a file whose prefix is not one of the
>   five or does not match its `kind`. It also fails if a reviewer finds two claims in one entry, or git shows an
>   entry file renamed to a different prefix.

*Proposed:* the prefix check is the one `tools/memory_index.py` already runs (B2.4). The rename check holds only if
EJ keeps the last sentence of W1.1 (Question 1).

*No change* to W2 (its Fails if, "`kind` holds any other value", already covers the five), to the vision (it names
kinds, not prefixes), or to Rd1.1 (it names `entries/` without listing prefixes).

### `docs/index-md/REQUIREMENTS.md`

**B1.1.** Current second sentence onward:

> No subfolders, no dotfiles, not `INDEX.md`. The `O-` and `H-` prefixes are *proposed* in the design (W1.1); the
> script accepts them.

New (*proposed*):

> No subfolders, no dotfiles, not `INDEX.md`. The five prefixes are those of W1.1.

B1.1's Fails if does not change.

### `tools/memory_index.py` and `tests/test_memory_index.py`: an item 8 leftover, not item 9 text

- *Verified:* line 42 is `ENTRY_NAME = re.compile(r"[DFLROH]-[^/]+\.md")`, and `PREFIX_KIND` still holds
  `"R": "runbook"`. `tests/test_memory_index.py` lines 31 and 405 still expect an `R-runbook.md` line.
- *Design:* item 8 removed the kind ("There is no runbook prefix (W3.6)"), and B1.1 already reads `^[DFLOH]-`.
- *Proposed:* as the code stands, an `R-` entry with `kind: runbook` gets an index line, which W2's Fails if
  forbids. Removing `R` from both tables and from the test is part of removing runbooks, so the prefix set in the
  code is the same as in W1.1 once this item is settled.

## Id form (optional)

*Proposed:* my answer does not depend on the id form. The prefix is always the first letter and the script reads only
`name[:1]`. One thing to note: B2.3 makes ids unique across all kinds, so the prefix never separates two ids. If the
id form contains `-`, as a date `2026-10-13` does, a person can no longer see where the id ends and the slug starts
in the file name. The script is not affected, because it reads `id:` from the header.

## What could go wrong

*Proposed:* a hypothesis is confirmed. The file is
`H-<id>-index-load-limit-is-in-characters.md`, and a measurement later shows that agy's limit really is in characters.
Under W4.1 an agent may change any entry, so it edits `kind: hypothesis` to `kind: fact`. The script then rejects the
commit, because the prefix and the kind no longer match (B2.4). To get the commit through, the agent renames the file
to `F-…`. Three things follow:
- the `INDEX.md` link and any link written as a path now point at the new name;
- the guess's history now sits under a fact's name;
- a "fact" appears that was found after the code, which W2.1 does not allow ("not something discovered
  afterwards").

The last sentence of the new W1.1 (a change of kind is a new entry that supersedes the old one) closes this case. It
is my rule, though, not EJ's, so it goes to him as Question 1.

## Questions for EJ

1. **When a hypothesis is confirmed or refuted, or an observation turns into a lesson, is that a new entry that
   supersedes the old one, so that an entry's kind and prefix never change? Or is the old entry edited and its file
   renamed?** If it is a new entry, keep the last sentence of W1.1 and the rename check in its Fails if. If it is an
   edit, drop both and add a line saying that a change of kind renames the file in the same commit.
