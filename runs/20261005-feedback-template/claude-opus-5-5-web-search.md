I improved the template rather than just confirming it. The full answer is in `runs/20261005-feedback-template/claude-opus-5-5-web-search.md`. The only other things I read were the brief and the web search row of `docs/TASK_TYPES.md` (line 98). I listed the run folder, so I saw the other engines' file names, but I didn't open any of their answers.

```
## Summary
- Found:     <claim> [S1][S2]                — one line per claim; every line cites ≥1 source id
- Not found: <the question asked> — searched: <queries tried>
- Disputed:  <claim> — for [S1][S3] / against [S2] — <worker's reading, or "unresolved">
- Sources:   [S1] <title> — <published: YYYY-MM-DD | undated> — <URL> — accessed YYYY-MM-DD
```

The worker writes every field. There's no `Effort` field because web search is a single node, not a loop. I added one field, tightened three, and removed none.

**The changes and where each chain of whys ends:**
1. **Add `Not found`.** The row's sabotage test is "ask a nonexistent fact → must return not-found", and the current template has nowhere to put that answer. An empty `Found` line looks the same as a worker who forgot, and a verifier can't check silence. With the new field, every question asked must appear under `Found` or `Not found`, so the check becomes mechanical. *Ends at a fact: the test is already in the table and needed a visible result.*
2. **`Found` cites source ids.** "Claims traceable" means each claim, not the report as a whole. A list of URLs at the bottom proves the sources exist, not that a given claim came from a given source. Two lists kept in matching order break silently if one line is dropped. *Ends at general knowledge that a real URL is often attached to a claim it doesn't support; I haven't measured this here (n=0).*
3. **`Sources` names two dates.** "Dated sources" doesn't say which date. The published date shows how old the fact is; the accessed date shows when the worker saw the page. Writing `undated` instead of leaving it blank means a blank fails the check while an honestly undated source still passes.
4. **`Disputed` lists the sides by source id.** "The split" doesn't say how it was counted. A count like "2–1" can't be checked, but ids can be opened. Also, three sites copying one press release are one source, not three. *Ends at an open question: who judges which sources are independent.*

**Left for you to decide:**
- **Who votes?** The row says "single node; voting on contested facts". If the voting is between sources inside one worker, `Disputed` fits. If it's between several runs, whoever compares the runs writes the tally, not the worker. Under the one-writer rule that makes it a separate artifact, not a field here.
- Are undated sources allowed at all?
- Can the worker pick a side on a dispute, or must it write `unresolved`?
- Should `searched:` stay? It's the weakest part of the proposal. It tells "doesn't exist" apart from "didn't look", but it's only worth having if the verifier actually re-runs the queries.
