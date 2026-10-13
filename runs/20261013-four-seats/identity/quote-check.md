# Quote check — identity research

Checked by Claude (main session), 2026-10-13, with a script I wrote (scratchpad `zh_quote_check.py` plus inline
checks). It fetches the source text and tests whether each quoted clause appears in it. It normalises variant characters
(彊/強, 爲/為, 塡/填, 胜/勝, 无/無) and strips Wikisource's inline commentary.

**What it establishes:** the quoted words exist in the named source. **What it does not establish:** that the source
is the right attribution, that the English gloss is right, or that the rule drawn from the quote is a fair reading.
I wrote the check and ran it, so it is not independent evidence.

| Seat | Source texts fetched | Result | Notes |
|---|---|---|---|
| 范蠡 | Wikisource 國語/卷21, 史記/卷041, 史記/卷129 | all quotes found | Rule 4 drops 「淫佚之事，上帝之禁也」 from the middle of the quote without marking the cut. |
| 老子 | Wikisource 道德經 (王弼本), 史記/卷063, 老子 (帛書校勘版) | 89/89 clauses found | The two first misses were my checker's (胜/勝; a 河上公 note stripped as commentary). |
| Linus | docs.kernel.org process/{management-style, submitting-patches, coding-style} | 26/29 pieces exact, 3 reworded | Small rewordings inside quote marks: "it's version N" for "this is version N"; "There is one thing" for "There's one thing"; "they will" for "they'll". Meaning unchanged. |
| 孫子 | Wikisource 孫子兵法, 史記/卷065 | 104/105 clauses found | The miss is one character: 「恃吾有以待也」 for the source's 「恃吾有以待之」 (九變). First attempt failed with opencode "database is locked" when four runs started at once; the rerun alone succeeded. |

Also checked: the design's own 范蠡 quote 時不至，不可強生；事不究，不可強成 is in 國語/卷21 (as 彊), where design.md
says it is.

## Round 2 — top 12 (`top12/*.md`)

Same check, same limits.

| Seat | Result | The misses |
|---|---|---|
| 范蠡 | 154/155 clauses | 飢/饑 variant |
| 孫子 | 250/251 clauses | an added 故 before 無恃其不來 |
| 老子 | 92/93 clauses | 萬物作而不辭 for the source's 萬物作焉而不辭 (焉 dropped) |
| Linus | every real quote found (2.Process added as a source) | "and that there will be" for "and there will be"; list numbers (1)/(2) added to a rendered list; the other misses were my regex pairing quote marks across lines |

**A wrong claim in a review, caught here.** `top12/fan-li.md` Gaps says design.md's 「時不至，不可強生；事不究，不可強成」 is 韋昭's
commentary, "and 范蠡 does not speak them". The line is in 國語/卷21 **twice**: once in 韋昭's note on 節事者與地 (quoting
ahead), and once in the main text as 范蠡's answer to 「節事奈何？」 — 對曰：「節事者與地。…時不至，不可彊生；事不究，不可彊成。」
The reviewer saw only the first. Its own item 2 quotes the same line as 范蠡's words. design.md's attribution stands.
