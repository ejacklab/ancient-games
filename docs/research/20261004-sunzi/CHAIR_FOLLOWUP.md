# The chair, still alive — follow-up asked after its first task finished

This is the evidence for the question "is it possible to keep them alive". The chair (a DSH
`backgroundMode: continuable` subagent, session `881a0446`) wrote `CANONICAL.md`, finished, and its status went to
*inactive*. It was then sent a follow-up message **in the same session**, with no re-priming:

> You dropped five principles. 1. Which of the five was the **closest call**, and what single piece of evidence
> would have changed your mind and kept it? 2. Of your fifteen canonical principles, which would a careful reviewer
> **challenge** — and what is your answer to them? Pick the one you consider most vulnerable, not the strongest.

It answered from what it already held, without re-reading the files:

**1. Closest call: 上下同欲者勝** — *"Dropping it was hard because the line is real, fetched, and its 'write the
objective once' rule is genuinely useful. What would have changed my mind: a second note that both fetches the line
and derives from it an alignment rule the other notes don't already cover — i.e. 'same desire under load is a
separate, checkable gate', distinct from knowing your own side (#3) and from bounded authority (#5). Without that,
it stays a restatement of principles I keep."*

**2. Most vulnerable: #9 分數形名** — *"A careful reviewer would say: you gave a canonical slot to one engine's
unchecked memory — the very upgrade you were told not to make. My answer: I did not upgrade it. It is labelled
RECALLED, single-source, and flagged as the weakest-evidence principle. It earns the slot on two grounds — the line
is central to 勢篇 and secure in the received tradition, and its rule (define unit structure and message schema
before scaling) answers a need no other principle covers. If that is still too thin, the remedy is to verify the
line against an edition and re-basis it, or drop it — not to cite it as though checked."*

## What this establishes

- **A continuable subagent is genuinely alive between turns.** No context was lost: it recalled which principle
  came from which note, which it dropped, and why — and it named its own weakest link unprompted.
- **It held the line under pressure.** Asked for its most vulnerable principle, it picked the one where it had
  relied on a single engine's recall, conceded the charge was fair, and offered *verify or drop it* rather than
  defending the citation.
- **The limit is the harness process.** This works while `dsh web` lives. A restart ends the session; the file
  (`CANONICAL.md`) is what survives, which is why the files are the memory and the session is a convenience.
- **The CLI experts are the more durable ones** — `claude --resume <id>` and `opencode run -s <id>` persist to disk
  — but they cannot be messaged between turns the way this one was.
