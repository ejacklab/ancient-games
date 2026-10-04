You are a domain expert, and your task is a **research note with evidence discipline**. Read this whole brief first.

## Domain

**孫子兵法** — the ancient Chinese war-strategy corpus (Sun Tzu's *Art of War* and its immediate tradition).

## Purpose

A project called **The Ancient Games** designs workflows for teams of AI agents. Its principles come from two poles:
孫子兵法 and game theory, with modern military doctrine and complexity science in between. Your note contributes the
孫子兵法 pole. The consumers are workflow designers, so every principle must be **usable as a design rule**, not a
piece of appreciation.

## The one thing that matters

**Separate what you can cite from what you remember.** You may not have the text in front of you — most of what you
know is from training. That is fine, but it must be labelled, because a fabricated classical quotation is worse than
no quotation:

- `VERIFIED` — you fetched or read a source and the line is copied from it. Name the source you actually read.
- `RECALLED` — you are quoting from memory. Say so plainly. Do not dress recall up as citation.

A note that is honest about its recall is worth more than one that looks scholarly and cannot be checked.

## What to produce

**8 to 14 candidate principles.** For each one:

```
### <n>. <the principle in one line>
- **Text**: the Chinese line, then an English rendering. Chapter name where you can.
- **Basis**: VERIFIED (source: …) | RECALLED (from training)
- **Reading**: what the line actually says, in two or three sentences. Where the classical text is ambiguous,
  say it is ambiguous and give both readings rather than picking one.
- **Design rule**: the rule a workflow designer would apply, stated so it can be obeyed or violated. One or two
  sentences. If the mapping from 4th-century-BC warfare to agent orchestration is loose, say it is loose.
- **Violated by**: the concrete design mistake that breaks this rule. One sentence.
```

Then, at the end:

```
## What I would not claim
Two or three things people commonly assert about 孫子兵法 that the text does not actually support, or that you
cannot check.
```

## Rules

- **Write your note to the one file you are told to write**, and create no other file. Do not modify anything else.
- English, plain. Chinese only for the quoted lines.
- No filler, no introduction, no conclusion beyond the two required sections. The note starts with `# 孫子兵法 — <your engine name>`.
- Do not pad to reach 14. Eight real principles beat fourteen thin ones.
- If two principles are the same idea in different clothes, merge them and say you merged them.

---

## Your file, and your name

Your engine name is **AGENT_NAME**. Write your note to exactly this path, relative to the repository root
`/home/smoke01/dev/ancient-games`:

    docs/research/20261004-sunzi/AGENT_FILE

Create no other file and change nothing else in the repository. When you are done, reply with only the path you
wrote and the number of principles you recorded.
