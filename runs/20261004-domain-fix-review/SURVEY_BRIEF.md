# Survey brief — the algorithm's open issues, area by area

You are a **孫子兵法 and game-strategy expert**. Three of you work independently and blind; a chair merges you after.
Your job is not to find new defects — 45 are already catalogued. It is to say, **area by area, what can be fixed
directly and what cannot, and why.**

## Read these

- `runs/20261004-defect-register.md` — the 45 issues, in 8 numbered areas. **This is your scope: all 8 areas.**
- `runs/20261004-open-defects.md` — which of them are already fixed, partial, or open. Do not re-recommend a fix
  that is already in place; say so and move on.
- The three research notes, and their chair's merge, in `docs/research/20261004-sunzi/`:
  `claude-opus-5-5.md`, `minimax-m3.1-flash.md`, `deepseek-v4-pro.md`, `CANONICAL.md`.

**Your permitted classical source is those notes and nothing else.** Cite a line only if it appears there, and carry
its **Basis** label (VERIFIED / RECALLED). A 孫子兵法 quotation from your own memory is forbidden — that is the
failure mode the notes exist to prevent. Game-theoretic reasoning outside the notes is allowed if labelled
`(not from a note)`.

## What to write

One file: **`runs/20261004-domain-fix-review/surveys/areas-ENGINE.md`** (ENGINE is given below). Create nothing else.

For **each of the 8 areas**, in order:

```
## Area <n>. <its title from the register>

| issue | verdict | what would fix it, or what blocks it |
|---|---|---|
| 1.1 | SCHEMA | one sentence. Name the field, the file, or the person who must decide. |
| 1.2 | DIRECT | ... |
```

Use **exactly** these verdicts and no others — a script parses this column:

- **DIRECT** — fixable now by editing a named file, and the fix is checkable. Name the file and the check.
- **SCHEMA** — the design format must carry a field that does not exist yet. Name the field.
- **DECISION** — only EJ can settle it. Name the choice.
- **DOC** — prose that disagrees with other prose. Name both files.
- **LATER** — real, but not worth doing now, or not verifiable with what exists. Say which.

After the eight areas:

```
## What I would fix first
Three items, ordered, each with the check that would prove it. If your list is not the same as the other two
surveys, that is expected — the chair's job is to reconcile them, not yours to guess theirs.
```

```
## Where 孫子兵法 does not help
Two or three issues on this list that a strategy text has nothing useful to say about. Say so rather than
manufacturing a principle.
```

## Rules

- Only `DIRECT` needs a check named. A `DIRECT` without a named, runnable check is not a `DIRECT` — use `LATER`.
- Do not restate what the register already says. Assume the reader has it. Spend your words on the verdict and the
  reason.
- Every one of the 45 issues must appear exactly once, under its own area. A missing row fails the check and the
  file comes back to you.
