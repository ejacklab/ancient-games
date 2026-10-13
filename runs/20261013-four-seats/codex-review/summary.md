# Codex review of the top 12 — summary

Written by Claude (main session), 2026-10-13. Four `codex exec` runs, `gpt-6.1-sol` at medium effort (the model is
reported in each `.log`), read-only, no web, checked against `../sources/`. Briefs: `../briefs/codex-review-*.md`.

## Counts (from the four tables, counted by script)

| Seat | Quote issue | Step issue | Kind issue | Rank issue | keep / change / drop |
|---|---|---|---|---|---|
| 范蠡 | 4 | 11 | 2 | 2 | 1 / 11 / 0 |
| 孫子 | 5 | 12 | 4 | 5 | 0 / 12 / 0 |
| 老子 | 0 | 12 | 5 | 6 | 0 / 12 / 0 |
| Linus | 3 (+9 "not checkable": authorship) | 7 | 0 | 4 | 1 / 11 / 0 |
| **Total** | | **42 / 48** | | | **2 / 46 / 0** |

## What it found

- **The words are mostly right; the step from words to rule is mostly not.** 42 of 48 rules add something the quote
  does not say: an order of steps, a "never" or "only", a condition, a ladder, a count. Each one is labelled
  `quoted` in the top 12 even though only the words, not the rule, are quoted.
- **Two reversals of meaning (范蠡).** #10: 范蠡 sent the younger son *because* a comfortable upbringing let him part
  with money; the top 12 says the opposite. #12: misreads 「無使執事之人得罪於子」 and gets the situation backwards
  (Yue is the winner there, not "the weaker party").
- **Codex caught the false 時不至 claim without being told.** It is in both 韋昭's note and 范蠡's main-text speech.
- **Linus: authorship.** The kernel docs carry the words, but they don't prove Torvalds wrote them, and two quotes
  talk *about* him in the third person (#7, #8).
- **Counting errors** in the top 12's own text: seven 善 clauses, not eight (老子 #11); eight prescriptions, not nine
  (孫子 #9); four pairs in both witnesses (老子 review).

## Spot-checked by me against `../sources/` (3 of the claims, all held)

- 孫子 #1: the source says 日費千金 (twice); the top 12 says "ten thousand gold a day".
- 老子 #11: 居善地，心善淵，與善仁，言善信，正善治，事善能，動善時 — seven.
- 范蠡 #10: 史記41 — 「前日吾所爲欲遣少子，固爲其能棄財故也」. The top 12 reverses it.

**What this does not establish:** the rest of codex's claims are unchecked by me. Codex is one more AI reader, not a
ground truth; it agreed with my quote check on the words and went further on the meaning, which my check could not see.
