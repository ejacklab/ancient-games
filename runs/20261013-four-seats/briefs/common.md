# Common brief — all four seats

You are one of four reviewers of `runs/20261013-four-seats/design.md` (repo: /home/smoke01/dev/ancient-games).
Read it in full first. You may also read the repo's CLAUDE.md and docs/ for context. Read-only, except your one
output file.

Rules:
- Answer **only your seat's question**. Do not review from the other seats' angles.
- **Do not imitate the person's voice or temper.** Plain English. The person is a source of principles, not a costume.
- Every point must cite (a) the line or section of design.md it is about, and (b) the principle you are applying,
  quoted. A point you cannot tie to both, drop.
- Label each conclusion: *quoted* (with source), *my reading*, or *not measured*.
- Do not invent thresholds, numbers or requirements for EJ. If one is missing, list it as an open question.
- Max 400 words. No preamble.

Output: write to `runs/20261013-four-seats/reviews/<seat>.md` with this shape:

```
# <seat> — review of design.md
Question: <your seat's question>
## Findings
1. <design.md line/section> — <finding> — principle: <quote> — label: <quoted|my reading|not measured>
## Verdict
<one or two sentences: does the design hold up from this seat's question?>
## Open questions for EJ
- ...
```
Then return the same text as your final answer.
