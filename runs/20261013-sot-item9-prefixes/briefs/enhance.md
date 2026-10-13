# Brief — one part of a memory design: the file prefixes for observations and hypotheses

You are one of four independent readers. You do not see the others' work. Your job is to **enhance**: think it
through and propose one complete, simple answer for the owner, EJ, to decide.

## Read first

- `/home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md`, the design, accepted by EJ. Read it whole.
- `/home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/source-of-truth-memory-vision-statements.md`,
  the settled vision.
- `/home/smoke01/dev/ancient-games/docs/index-md/REQUIREMENTS.md`, a draft for the script that builds `INDEX.md` from
  the entry files. It reads file names by their prefix letter.

## The problem (review item 9)

Each memory entry is one file, named `project-memory/entries/<prefix>-<id>-<slug>.md` (W1.1). The prefixes `D-`
decision, `F-` fact and `L-` lesson are settled. W1.1 marks `O-` observation and `H-` hypothesis as *proposed*: *"the
design leaves these two open"*. The folder layout lists only `D-`, `F-` and `L-`.

The **kinds** are settled. The vision, from EJ's words, names *"lessons, observations and hypotheses"*, and W2.2
defines all three. Only the two **prefixes** were never confirmed.

Related, also open: the `INDEX.md` draft (G4) notes that an entry's `id` must be unique without coordination between
git branches, never "the next free number". Its form (a date, a hash or a random suffix) is undecided. The prefix and
the id sit side by side in the same file name.

## Your task

1. **Recommend one answer** for the prefixes, in one sentence. Confirming `O-` and `H-` is a starting point, not a
   limit. A simpler idea is welcome, for example whether every kind needs its own prefix at all.
2. **Three reasons**, each grounded in the design, the vision or the `INDEX.md` draft. Quote the line you rely on.
3. **The exact text changes**, by section or requirement id: W1.1, the layout, "Where it is put", and any other place
   your answer touches. Each requirement you change keeps a **Fails if** check.
4. **Optional:** if your answer depends on the id form, say how, in at most three lines. Don't settle the id form
   unless your answer needs it.
5. **What could go wrong** with your answer: one concrete case.
6. **Questions for EJ:** at most two, and only ones whose answer changes your text.

Rules:
- Keep it simple. The owner's rule is that memory is simple, and a mechanism that is not needed is removed.
- Label each line *EJ's* (his words), *design* (already in the document) or *proposed* (yours).
- Read only; do not change any file.

## Output — one markdown report

```
# Item 9, prefixes (<your engine name>)

## Recommendation
## Three reasons
## Text changes
## Id form (optional)
## What could go wrong
## Questions for EJ
```

The launcher tells you your engine name and where the report goes.
