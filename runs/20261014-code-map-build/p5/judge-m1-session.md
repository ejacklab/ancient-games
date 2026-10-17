# Blind judge — m1-session (Claude opus subagent; labels A/B)

| Q | A correct | A missed | A wrong | B correct | B missed | B wrong |
|---|---|---|---|---|---|---|
| Q1 | 3 | 1 | 0 | 3 | 1 | 0 |
| Q2 | 5 | 0 | 0 | 5 | 0 | 0 |
| Q3 | 5 | 1 | 0 | 6 | 0 | 0 |
| Q4 | 2 | 1 | 0 | 3 | 0 | 0 |
| Q5 | 9 | 0 | 0 | 9 | 0 | 0 |
| Q6 | 8 | 0 | 0 | 8 | 0 | 0 |
| Q7 | 7 | 0 | 0 | 7 | 0 | 1 |
| Q8 | 2 | 2 | 0 | 2 | 2 | 0 |
| Q9 | 10 | 0 | 0 | 10 | 0 | 0 |
| Q10 | 4 | 1 | 0 | 4 | 1 | 1 |
| Total | 55 | 6 | 0 | 57 | 4 | 2 |

The judge found two wrong claims, both in B:
- **Q7, "compaction.ts:309 and :371 call deliver from compact (:205)".** The calls are in summarize (:272) and
  compactNatively (:324), which compact calls at :232-233. B leaves out one level of the chain.
- **Q10, "resends the same request".** The request is rebuilt on each retry (llm.ts:217-234). The judge called this
  one minor.

The judge scored strictly, by the same rule for both sets. A few line numbers that were 1-2 lines off were not counted
as wrong.
