# 孫子兵法 — the first domain of the principle base

EJ, 2026-10-05: expert agents that research one of the project's own founding domains and write what they find to
files. "Ancient Games" names two poles — 孫子兵法 and game theory — with modern military doctrine and complexity
science in between; this is the first pole, done properly.

## What was asked of the engines

Three engines, **blind to each other**, an identical brief with one substitution — the file to write:

- `claude-opus-5-5.md` — Claude Opus 5.5, via the CLI
- `minimax-m3.1-flash.md` — MiniMax-M3.1-Flash-Preview, via opencode
- `deepseek-v4-pro.md` — DeepSeek-V4-Pro, as a DSH subagent

The brief (`BRIEF.md`) asked for 8-14 principles, each with: the classical line (Chinese + English), a **Basis**
label, a reading, a design rule a workflow designer could obey or violate, and the mistake that breaks it. Plus a
"What I would not claim" section.

**The one hard requirement** was the Basis label:

> `VERIFIED` — you fetched or read a source and the line is copied from it. Name the source you actually read.
> `RECALLED` — you are quoting from memory. Say so plainly. Do not dress recall up as citation.

A fabricated classical quotation is worse than none, so honesty about recall was worth more than scholarly
appearance.

## What came back

| engine | time | principles | basis | source |
|---|---|---|---|---|
| minimax-m3.1-flash | 538 s | 13 | 14 VERIFIED, 1 RECALLED | Chinese Wikisource, fetched |
| deepseek-v4-pro | — | 13 | 14 VERIFIED | Chinese Wikisource, fetched |
| claude-opus-5-5 | 172 s | 14 | **0 VERIFIED, 15 RECALLED** | none — it fetched nothing |

All three produced the required shape: **40 principles, zero missing fields.** Each carried its caveats section.

**The cheapest engine did the most evidence work.** MiniMax fetched the received text and then machine-checked every
Chinese fragment in its own note against it — 128 distinct runs — reporting two defects it had introduced and fixed:
a fabricated `之` in `兵之形象水`, and several places where it had replaced the source's punctuation inside a quoted
span. `deepseek-v4-pro` also fetched and verified.

**The strongest model produced the least verifiable note** — and was honest about it. Opus labelled all fifteen
lines RECALLED and named no source, which is exactly what the brief asked for when nothing was fetched. It is not a
worse contribution for that; it is a different kind of contribution, and the label is what makes the difference
usable.

## Verified here, not taken on trust

The notes claim their Chinese matches Wikisource, so the claim was checked independently: I fetched the same page
and compared.

| line | marked | Wikisource |
|---|---|---|
| 兵者，國之大事，死生之地，存亡之道，不可不察也。 | VERIFIED (始計) | exact |
| 故上兵伐謀，其次伐交，其次伐兵，其下攻城。 | VERIFIED (謀攻) | exact |
| 故兵貴勝，不貴久。 | VERIFIED (作戰) | exact |
| 夫兵形象水 | MiniMax's *self-corrected* reading | exact |

MiniMax's caveat that `上畧伐智，中畧伐義，下畧伐勢` are **not** Sun Tzu's words is confirmed by Wikisource's own
editorial note on that appendix — `此亦不似孫武語，蓋後世兵多祖孫武` (this too does not look like Sun Wu's
language; later military writers mostly traced themselves to him). A model that volunteers "this famous line is not
actually his" is doing the job.

## The chair

`CANONICAL.md` is written by a **separate, persistent DeepSeek-V4-Pro session** — the domain chair. It is kept
alive, and EJ can ask it follow-up questions in the same session.

Two things make the chair a real adjudicator rather than a formatter:

- **It is not the same session as the deepseek-v4-pro researcher**, so it does not quietly bless its own note.
- `CHAIR_BRIEF.md` tells it the asymmetry plainly: two notes verified against the *same* witness are two readings
  of one source, not two independent witnesses; the recall-only note must not be cited as if checked; and it must
  hold its own engine's note to the same standard — *"a chair that quietly favours its own note has produced
  nothing."*

It is also told to drop principles that are modern management ideas in classical costume **even when all three
notes carry them**, because popularity is not evidence about what a text says.

## Keeping an expert alive — what actually works

Asked whether these agents can be kept alive, the answer differs by executor, and it was checked rather than
assumed:

| executor | mechanism | survives a harness restart |
|---|---|---|
| DeepSeek-V4-Pro (the chair) | DSH `backgroundMode: continuable` — a live session EJ can message between turns | no: it dies with the `dsh web` process |
| Claude Opus 5.5 | **not through the provider** — `dsh-subagent-claude-code` sets `persistSession: false` and exposes no resume. Use the CLI: `claude -p --resume <session-id>` | yes: the session is a file on disk |
| opencode MiniMax | `opencode run -s <session-id>` (or `-c` for the last, `--fork` to branch) | yes |

All four CLIs support it — `claude --resume`, `opencode -s`, `agy --conversation`, `codex exec resume` — so the
**CLI experts are the more durable ones**, which is the opposite of what "keep them alive" suggests.

The consequence for design: **the files are the memory, not the session.** A long-lived expert's context grows
every turn and each follow-up re-reads it — the wrapper cost method 3.8 names. If a session dies, nothing is lost
as long as the canonical file is on disk. The live session is a convenience for the next question.

`agy` took no part: headless it auto-denies the `command` permission it needs to read or browse, and the escape it
suggests is the flag EXECUTOR_KINDS rule 3 forbids. Rule 2 routes research to agy, so this is a live conflict
between the routing and the tool's actual behaviour — recorded, not worked around.

## Files

- `BRIEF.md`, `brief-*.txt` — the identical brief, one per engine with its own output path
- `CHAIR_BRIEF.md` — the adjudication brief, including the evidence asymmetry and the self-favour warning
- `claude-opus-5-5.md`, `minimax-m3.1-flash.md`, `deepseek-v4-pro.md` — the three notes, unedited
- `CANONICAL.md` — the chair's merge

## Next domains

The protocol is domain-agnostic: swap the domain paragraph in `BRIEF.md` and run the same three engines. The
remaining poles are **game theory**, **modern military doctrine** and **complexity science**. On this evidence the
one change worth making first is to tell every engine to fetch a source — or to run the cheapest engines, which
actually did it.
