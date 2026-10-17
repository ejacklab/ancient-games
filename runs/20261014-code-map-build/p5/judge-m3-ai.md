# Blind judge — m3-ai (Claude opus subagent; labels A/B, mapping kept by the COO until all three are in)

| Q | A correct | A missed | A wrong | B correct | B missed | B wrong |
|---|---|---|---|---|---|---|
| Q1 | 3 | 2 | 0 | 4 | 1 | 0 |
| Q2 | 4 | 1 | 0 | 5 | 0 | 0 |
| Q3 | 9 | 0 | 0 | 9 | 0 | 0 |
| Q4 | 4 | 1 | 0 | 5 | 0 | 0 |
| Q5 | 6 | 0 | 1 | 6 | 0 | 0 |
| Q6 | 7 | 1 | 0 | 8 | 0 | 0 |
| Q7 | 4 | 1 | 0 | 4 | 1 | 0 |
| Q8 | 4 | 1 | 0 | 3 | 2 | 0 |
| Q9 | 8 | 0 | 0 | 8 | 0 | 0 |
| Q10 | 6 | 1 | 0 | 6 | 1 | 0 |
| Total | 55 | 8 | 1 | 58 | 5 | 0 |

The one wrong claim is in A, Q5: "`new HttpOptions` (`:571`, defined outside the repo)". It is defined in the repo at
packages/ai/src/schema/options.ts:68.

Some misses come only from the line rule: the claim is stated, but its file:line is more than 3 lines from the
key's, or missing. These are A Q2 M3.2e, A and B Q7 M3.7a, A and B Q8 M3.8e, B Q8 M3.8d, and A and B Q10 M3.10g.
The content misses are A Q1 M3.1d and M3.1e, B Q1 M3.1e, A Q4 M3.4a, and A Q6 M3.6e.
