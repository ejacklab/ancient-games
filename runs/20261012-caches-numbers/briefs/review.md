# Review — "Example numbers by case" (run 20261012-caches-numbers)

You are an independent reviewer. You did not write this section and did not do the research. Below are the section
and the four research files it cites:
- `web.md`, ids W-*;
- `opencode.md`, cited as OC;
- `seza.md`, cited as SZ;
- `codex.md`, cited as CX.

**Do not use any tools.** Everything you need is in this prompt. Ids such as BM-*, S-F*, V-F*, G-F* and s3-F* come
from earlier research that is not included; leave those unchecked and say so.

Check:
1. **Numbers.** Every number cited to W-*, OC, SZ or CX must match its research file exactly, allowing for rounding as
   written. List every mismatch.
2. **Labels.** Arithmetic and readings are labelled (*my arithmetic*, *my reading*), and vendor or secondary figures
   are not presented as independent.
3. **Claims.** Each "My reading" must follow from the rows above it. Flag any that overreaches.

Raise only real problems: ones that would mislead a reader choosing a number. No style comments.

**Output:**
- first line: `VERDICT: ACCEPT` or `VERDICT: REPAIR`;
- then the findings, each with the row or line it concerns, what is wrong, the source text that shows it, and a
  severity (high, medium or low);
- then a "Not checked" list.
