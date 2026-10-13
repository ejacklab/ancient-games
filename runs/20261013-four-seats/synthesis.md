# Four seats — synthesis of the first review

Written by Claude (main session), 2026-10-13, from `reviews/*.md`. Run: four seats, parallel and blind, one Claude
model each, reviewing `design.md`. n=1.

## Found by all four (blind)

- **范蠡 as the sizer is broken.** "Only Linus" still costs a 范蠡 pass, and nothing checks how 范蠡 judges small vs
  big. — 老子 #1, 范蠡 #2, Linus #4, 孫子 #2.
- **No evidence or baseline.** No measure of success, no comparison (worker checks itself, or one plain reviewer), no
  test that a seat can fail. — 老子 #5, 范蠡 #1 #4, Linus #1 #6, 孫子 #4 #5.

## Found by two or three

- **The diagnosis is untested.** The two failure modes are my reading; no real case is cited. — Linus #1, 孫子 #1.
- **Sequential order is a risk.** Later seats anchor on earlier ones, and 老子 may undo 孫子's safeguards with no route
  to EJ. — 孫子 #3 #7, 老子 #6.
- **No stop condition** for a review or for a seat. — 范蠡 #5, 老子 #7.

## Found by one seat only

- Linus: evidence-checking should be a rule for every seat, not a seat (#3); "this project's common sense" has no
  owner (#2); the referee's Gate and Guard already cover agent count and irreversibility (#4, grep only).
- 孫子: no planted flaw to prove the seats can fail (#5); the AI can't see its own defaults, so the first big mistake
  is the one the list misses (#6).
- 老子: four came from "or maybe we can have 4", not from the problem (#3).

## Style or judgment?

No review imitated a voice. Every finding cites a design.md line and a quoted principle. 老子 and Linus each argued
against their own seat. Each seat also had findings no other seat had.

**What this does not establish:** I wrote the design, the briefs and this synthesis, and all four seats are the same
model. So the agreement between them is not independent evidence, and "they followed the brief" is a check I wrote.

## Open for EJ

1. Two or three real AI suggestions that had no logic, to test the diagnosis (Linus).
2. "maybe 范蠡 better": instead of 孫子, or in addition (老子)?
