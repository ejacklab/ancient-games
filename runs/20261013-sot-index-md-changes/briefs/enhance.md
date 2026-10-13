# Brief — one part of a memory design: the changes the INDEX.md work implies

You are one of four independent readers. You do not see the others' work. Your job is to **enhance**: think it
through and propose one complete, simple answer for each change, for the owner, EJ, to decide.

## Read first

- `/home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md`, the design, accepted by EJ. Read it whole.
- `/home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/source-of-truth-memory-vision-statements.md`,
  the settled vision.
- `/home/smoke01/dev/ancient-games/docs/index-md/REQUIREMENTS.md` and `DESIGN.md` in the same folder: the requirements
  and design for the script that builds `project-memory/INDEX.md` from the entry files. Its last section, "Open, for
  EJ", item 4, lists the changes below.
- Optional, as evidence of what already exists: `tools/memory_index.py`, `.githooks/`, `tests/test_memory_index.py`
  and `docs/index-md/BACKLOG.md`. The script is built and merged. The design describes what memory needs; it is not
  rewritten to match the script's details.

## The problem

The `INDEX.md` work settled things that the design still leaves vague or open. Five changes are proposed, none made:

1. **K6.2 and the "When to write" table.** Today: *"It is regenerated right after any decision or fact is written"*.
   Proposed: after **any** entry is created or changed (every kind, every status change), and `INDEX.md` is
   committed **in the same commit** as the entry. K6's "Open: which tool generates it and what runs it" and the
   "Still open" line under "When to write" may now be answerable.
2. **A new K6.3:** `INDEX.md` is never hand-merged. On a conflict, resolve the entry files, then regenerate. This
   touches W6's "Open: who resolves a merge conflict".
3. **Rd3.1** (and the matching line before "Core requirements"): *"the build checks it"* becomes "the script checks
   it, and the tests run the check". This repo has no build step.
4. **W1.1, the id.** An entry's `id` must be unique without coordination between git branches, never "the next free
   number". The form (a date, a hash, a random suffix) is open.
5. **W1.2 and W1.3, the format.** The script reads a header between two `---` lines with `key: value` fields, and
   takes the claim as the body up to the first line starting with `**Why:**`. The design names the fields and the
   sections but not this format or this spelling.

## Your task

For **each** of the five:

1. **Recommend** in one sentence: make it as proposed, make it differently, or don't make it. A simpler idea is
   welcome.
2. **One reason**, grounded in the design, the vision or the `INDEX.md` documents. Quote the line you rely on.
3. **The exact text**, by section or requirement id. Each requirement you change keeps a **Fails if** check.

Then, once for the whole set:

4. **What could go wrong:** one concrete case.
5. **Questions for EJ:** at most two, and only ones whose answer changes your text.

Rules:
- Keep it simple. The owner's rule is that memory is simple, and a mechanism that is not needed is removed.
- Label each line *EJ's* (his words), *design* (already in the document) or *proposed* (yours).
- Do not invent numbers or limits. Where a value is not known, say it is open.
- Read only; do not change any file.

## Output — one markdown report

```
# INDEX.md changes to the design (<your engine name>)

## 1. K6.2 and When to write
## 2. K6.3, never hand-merge
## 3. Rd3.1, who checks the size
## 4. W1.1, the id
## 5. W1.2 and W1.3, the format
## What could go wrong
## Questions for EJ
```

The launcher tells you your engine name and where the report goes.
