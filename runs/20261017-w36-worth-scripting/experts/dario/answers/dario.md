# Answer — May a scriptable procedure stay a page because it runs rarely?

## Answer
Yes, but only on a comparison, not on rarity alone. The agent writing the procedure decides when it writes the page and records a reason, and the owner decides if that is contested. Add this to W3.6: *"A procedure that could be a script may stay a page when the agent writing it records a reason that building and keeping the script would cost more than it saves over the runs it can expect, counting the effort of each run and the harm of a skipped or wrong step; 'it runs rarely' by itself is not that reason. The agent makes this comparison when it writes the page and again each time it follows the page; the owner decides if it is contested."*

## How I decided
1. **The gap is narrow.** W3.6 is a SHOULD, and the levels let a SHOULD be skipped with a written reason. `fails_if` already treats a written reason as the way out. The only open point is what counts as a reason for "could be a script, but not worth it."
2. **The sources say it is a comparison.** The research shows every source weighs scripting as the cost of building and keeping against what it saves per run (SRE workbook A1–A2, xkcd A5). It found no measured break-even frequency (A9). The owner's rule (a trigger is "measure X against Y", never an invented number) therefore points to a comparison.
3. **Rarity cuts both ways (my reading of B10–B11, C16, C18–C19).**
   - A rarely-run procedure saves less per year.
   - A rarely-run script is the kind that rots, so its keep cost rises.
   - A rarely-run page drifts, and whoever follows it is out of practice, so the harm of a wrong step rises.
   - Rarity therefore belongs inside the comparison and cannot be the reason by itself.
4. **What an agent can compare when it writes the page:**
   - the build cost, for example whether the steps are already commands;
   - the keep cost, meaning how often the things the script touches change and whether anything will run it on a schedule;
   - the effort per run;
   - the harm of a skipped or wrong step, and whether it can be undone.
   - The number of future runs is only a guess at that point.
5. **Why the agent decides.** It has the facts and, by W3.6, has already tried the script first. The owner keeps the contested cases, and 孫子 also puts the value judgment on the owner. The agent pays the build cost now and does not pay the keep cost later. That favours "not worth it", so the written reason and the owner's right to contest are the check.
6. **The two moments.**
   - When the page is written, because that is when the script is tried first.
   - Each time the page is followed again, because that is the first real evidence of how often it runs (Limoncelli, A7: you learn what to automate by doing it repeatedly).
7. **I wrote the W3.6 text to match.** It adds only the test and the moment. The existing "agent decides, owner if contested" sentence stays as it is.

## What I need to know
- **Who follows these pages: agents, EJ, or both?** Bainbridge's skill-erosion point (C18) is about people. If agents follow most pages, the harm of a rarely-run page is mostly drift and misreading, and the answer tilts further toward "page may stay." If EJ follows them, it tilts toward a script.
- **Where does the written reason live?** The levels say a skipped SHOULD gets its reason in the task's `state.md`. A procedure page outlives the task, so the next reader never sees that file. I left the place out of the sentence. I would put one line on the page, but that conflicts with the levels text, so EJ should say.
- **Does the project run scripts on a schedule or in CI?** If it does not, a rarely-run script has a higher keep cost, because it needs its own exercise to stay alive (B10, B15). That tilts toward a page.
- **Should irreversible or destructive procedures be treated differently?** I assumed the harm of a wrong step counts like any other cost. If EJ wants those to default to scripts, that would be a separate rule.

## Costs and risks
- **The comparison is easy to write down badly.** Build cost is certain and now, while keep cost is uncertain and later. "Not worth it" will be over-chosen. The only brakes are the written reason, the reviewer check (which can fail a reason that says only "rare") and the owner's contest.
- **A page that could be a script is a standing copy of the procedure.** That is the drift `procedure-to-skill` warns about ("summaries drift"), and W3.6's first sentence is against copies. The clause accepts this risk and does not remove it.
- **The expected number of runs is a guess.** It can be wrong in either direction. Re-asking each time the page is followed costs a little each time, and an agent may skip it. I am least sure of that second sentence.
- **Choosing "script" is no cure for rarity.** A script that nothing exercises fails when it is finally needed (SRE failover, B10). The clause does not require a scheduled run. Middle forms exist (a page with exact commands, a do-nothing script, partial automation, A3 and A7–A8), and the clause does not name them.
- **Limits of the evidence.** There is no measured break-even frequency. The runbook-drift claims are vendor or reported sources (C16–C17, not measured). The Bainbridge point comes from secondary notes. The research was mostly SRE and vendor writing, not studies of repos like this one.

## How we would know I was right
- **Reviewer test, observable now.** Read each page kept under this clause. A reason that names a cost on both sides (building and keeping against the saving) passes. A reason that says only "rarely run" fails. If reviewers cannot tell the two apart, the sentence is too vague.
- **Later comparison, not yet measured.** For pages kept under the clause, compare how often a run found the page stale or a step skipped with the same count for scripts that run about as often. If pages are clearly worse, the clause lets too much through. EJ reads the comparison, with no number set in advance.
- **Owner contests.** If EJ overturns most of the written reasons, the test is too loose. If EJ never contests any, either it works or no one is looking, and the first check above tells which.
