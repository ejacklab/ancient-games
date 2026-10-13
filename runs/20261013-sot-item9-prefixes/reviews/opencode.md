I'll read the brief first.
Now let me check where else prefixes are referenced in the repo docs.
Verified the code paths by running them; nothing in the repo was changed. Here is the report.

# Item 9, prefixes (opencode)

## Recommendation

Keep one prefix per kind, and confirm the last two: the five kinds are `D-` decision, `F-` fact, `L-` lesson, `O-` observation, `H-` hypothesis, and no other prefix exists. *(proposed)*

Not recommended, and considered: dropping the prefix altogether and reading the kind only from the header field `kind:`. It is one mechanism less, but the design then has nothing to say about a file's kind before it is opened, and every other choice — a shared prefix for observation and hypothesis, or a second, heavier id — is more change than confirming two letters. EJ's own rule applies: *"memory is very simple"* *(EJ, vision l.57)*. Confirming two letters is the whole of it.

## Three reasons

**1. The prefix is the only thing that shows which half of memory an entry is, before it is opened.** The vision splits memory in two: *"the **decisions and facts** the code must follow, written **before** the code; — what was **learned** after: lessons, observations and hypotheses"* *(design, vision l.22–23)*. A name starting `D-` or `F-` says "requirement the code must follow" in a folder listing and in `git log -- project-memory/entries/`; `L-`, `O-`, `H-` say "written after". Without a prefix that line exists only inside the file, in `kind:`, once someone has opened it.

**2. `H-` is the one label the design itself makes load-bearing.** *"Guesses not labelled as a hypothesis"* are excluded from memory *(design, l.119)*, and W2's check is *"**Fails if** `kind` holds any other value, or a guess is recorded under any kind but hypothesis"* *(design, W2, l.205)*. A guess is the entry most likely to be mistaken for a fact, and `H-` puts the label where it is read first — in the listing, in the commit line — not only in the header. *This argument is strong for `H-`, weak for `O-`:* an observation carries no label the reader must not miss, because "records what was seen" is not a claim anyone is tempted to act on as a requirement. `O-` is cheap, not important; that is the honest weight of the weaker half of this answer.

**3. Confirming them costs nothing; every document downstream already assumes them.** The INDEX draft reads file names by prefix: *"whose name matches `^[DFLOH]-[^/]+\.md$`"* and requires *"a `kind` from the five (decision, fact, lesson, observation, hypothesis); a file prefix that matches its `kind`"* *(design, `docs/index-md/REQUIREMENTS.md` B1.1, B2.4)*, and `tools/memory_index.py` already maps `O` and `H`. Any other answer is the change; `O-`/`H-` is only the deletion of a hedge sentence. *(proposed)*

## Text changes

Read-only run: no file was changed. The edits below are what EJ would apply.

**1. `docs/memory-system/SOURCE_OF_TRUTH.md`, header — a new revision line** *(proposed)*, after the item 8 block at l.25–28:

```
> **Revised 2026-10-13, item 9 (the last two prefixes):** the `O-` observation and `H-` hypothesis prefixes are
> confirmed, so each of the five kinds has one prefix and W1.1 no longer marks the last two *proposed*. The INDEX
> draft already reads all five (`^[DFLOH]-`); `tools/memory_index.py` still accepts the `R-` runbook prefix removed on
> 2026-10-13, and is brought back into step.
```

**2. W1.1** *(design, l.189–191 — replaces three lines)*:

```
- **W1.1** Each entry is one file: `project-memory/entries/<prefix>-<id>-<slug>.md`, with one prefix per kind: `D-`
  decision, `F-` fact, `L-` lesson, `O-` observation, `H-` hypothesis. The prefix must match the entry's `kind`.
  There is no runbook prefix (W3.6).
```

The last sentence is unchanged. `(*proposed*; the design leaves these two open)` is deleted. The clause *"The prefix must match the entry's `kind`"* is added because the design never stated the rule while `REQUIREMENTS.md` B2.4 already enforces it — stating it once, in W1.1, removes a mismatch between the two documents rather than adding a mechanism. *(proposed)*

**3. W1's Fails if** *(design, l.197 — extended, not replaced)*:

```
- **Fails if** a lint over `entries/` finds a missing field or section, a file whose prefix does not match its `kind`,
  or a reviewer finds two claims in one entry.
```

**4. "Where it is put", the layout** *(design, l.135)*:

```
  entries/           one file per entry: D- decision, F- fact, L- lesson, O- observation, H- hypothesis
```

**5. "Where it is put", the closing sentence** *(design, l.142–143)* — delete *"File prefixes for observations and hypotheses: `O-` and `H-`, proposed in W1.1."*, and end the paragraph as:

```
The project's existing documents (requirements, architecture) stay in `docs/`; memory links to them instead of copying
them. Every kind has one prefix; they are listed in W1.1.
```

**6. `docs/index-md/REQUIREMENTS.md` B1.1** *(draft, l.22–23)* — keep the regex, delete the hedge:

```
- **B1.1** Only files directly in `project-memory/entries/` whose name matches `^[DFLOH]-[^/]+\.md$`, one prefix per
  kind (W1.1). No subfolders, no dotfiles, not `INDEX.md`.
```

**7. B1's Fails if** *(draft, l.28–29 — extended)*: add *"an `R-` file gets a line"* after *"a file outside B1.1 gets a line"*. B1.1's own check is kept.

**8. `tools/memory_index.py`** — the enforcement must agree with the design, or the design is not the truth *(proposed)*:
- l.42 `ENTRY_NAME = re.compile(r"[DFLROH]-[^/]+\.md")` → `"[DFLOH]-[^/]+\.md"`.
- l.47 delete `"R": "runbook",` from `PREFIX_KIND`.

This is not housekeeping. `KINDS = tuple(PREFIX_KIND.values())` (l.51) means the script's list of kinds *is* the prefix map, so the removed runbook kind is still one of its six kinds today. I checked this on a throwaway repo: a file `R-20261013-0001-deploy.md` with `kind: runbook` builds an `INDEX.md` line and `python3 tools/memory_index.py --check HEAD` exits **0**, against a design that removed the runbook kind on 2026-10-13 (W3.6). Add a case to `tests/test_memory_index.py` (C2.2): an `R-` file is refused, an error, not a line.

**9. No change** — the vision statement (it names kinds, never prefixes), `docs/index-md/DESIGN.md` (l.31 and l.48 already match the confirmed set), and the "Open, for EJ" list in `REQUIREMENTS.md` (the prefixes were never in it).

## Id form (optional)

My answer does not depend on the id: the prefix is a separate leading field, and G4.1 already settles only that it is *"unique without coordination between branches"*. One consequence to note: B3.1 sorts `INDEX.md` *"by file name in code-point order"*, so with a date id the index is grouped by kind, not newest-first — a fact to accept, not a reason to move the prefix. And `docs/memory-system/CACHES.md` l.185 uses `D-0012` as an example id, which is the numeric form G4.1 forbids; that example needs changing whenever the form is settled.

## What could go wrong

A kind changes and the file has to be renamed, and renames meet merges badly. Concrete case: `O-20261013-postgres-autovacuum.md`, an observation, turns out to be something the code must respect, so it becomes a fact and the file becomes `F-…md`. Two agents are on their own branches (W6.2). One runs `git mv`; the other adds a `changed:` line to the same entry, because W4.2 requires it. If the body also changed, git's rename detection can fail and the merge becomes a modify/delete conflict — on the one file whose conflict owner W6 leaves open: *"**Open:** who resolves a merge conflict."* *(design, l.250)* The fix already exists inside the design and costs nothing: do not rename. Write the new entry and mark the observation `superseded`, which is exactly what K4.1 provides — *"An entry is never deleted. It is marked `superseded` or `retired`, links to what replaced it (`superseded_by`), and keeps its old body."* *(design, l.266)* Whether the design should say so is question 2 below.

## Questions for EJ

1. **Must the file prefix match the entry's `kind`?** If yes, my added clause in W1.1 stands and `REQUIREMENTS.md` B2.4 cites it. If the prefix is free text, B2.4's *"a file prefix that matches its `kind`"* must be dropped from the INDEX draft instead — otherwise the build enforces a rule the design never made.
2. **When an entry's kind changes, is the file renamed, or does a new entry supersede the old one?** This decides whether W1.1 gets one sentence (*an entry keeps its file and prefix; a change of kind is a new entry that supersedes it*) and whether W6's open merge-conflict question has to mention renames. My recommendation is the second, for the reason above.
