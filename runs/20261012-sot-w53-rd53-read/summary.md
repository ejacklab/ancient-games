# Summary — four readers on W5.3 and Rd5.3

COO (Claude `claude-opus-5-5`), 2026-10-12. Sources: `reviews/claude.md`, `reviews/codex.md`, `reviews/opencode.md`,
`reviews/agy.md`, each read blind. "All four" means each report raised the point on its own. Fixes marked *proposed*
are the COO's; EJ has not decided them.

## W5.3 — started when written, `done:` when complete

| # | Finding | Raised by | Proposed fix |
|---|---|---|---|
| 1 | **A standing rule is never "complete".** Example: "all timestamps are UTC" governs forever, so a reviewer would fail a task for a `done:` that can never be due. | all four | `done:` applies to a decision to **build something** (EJ's words: *"we decided to build something"*). A standing rule never gets `done:`. |
| 2 | **"The agent or person who did the work"** conflicts with W4.1 and with handoffs: the worker is often gone, or another session finishes the job. | all four | Whoever finishes the work adds `done:`, with a `changed:` line as for any change. |
| 3 | **The check passes `done: TBD`.** It looks only for the line. | all four | The judged check looks at the contents: a time, a result, and test results (or "no tests" said plainly). |
| 4 | **W3.1 conflict.** Copying test output or commit details repeats what git and the tests already hold. | all four | `done:` gives the result in a sentence and points to the evidence (`runs/<id>/` or the commit). It does not copy output. |
| 5 | **Result differs from the decision.** A `done:` saying "shipped with grep instead of SQLite" quietly settles a mismatch. | claude | That is a Rd5.3 mismatch: report it, and don't settle it in `done:`. |

## Rd5.3 — the reader reports a mismatch and does not change the entry

| # | Finding | Raised by | Proposed fix |
|---|---|---|---|
| 6 | **Clash with K1.1, the sharpest one.** K1.1 writes the decision first, so the code *should* differ until the work is done. The agent building it, or one whose task is to change the decision, is blocked or breaks a check whichever way it goes. | all four (opencode: "no branch of this case satisfies both") | Rd5.3 applies only to a decision that has `done:`. Before `done:`, a mismatch is just work in progress. A task whose job is to change a decision follows K1.1, because that is an intended change, not a found one. *This is where W5.3 and Rd5.3 fit together: `done:` is what separates "being built" from "drifted".* |
| 7 | **An unstated exception to W4.1** ("anyone may change any entry, no approval gate"). Does it bind EJ? | all four | W4.1 says "except as Rd5.3 says". Rd5.3 binds readers, not EJ, and EJ deciding and fixing is one act. |
| 8 | **No place for the report,** so it's lost when the session ends and the next reader reports it again. The old open item "how the report reaches EJ" was dropped when the subagent was removed. | claude, opencode, agy | **Open, for EJ:** where the report lives. |
| 9 | **The check misses a reader who finds a mismatch and never reports it.** A note in its own journal also counts as "saying so". | all four | The check fails a found mismatch without a report that holds the three items. |
| 10 | **Wait or carry on?** It isn't said what the reader does until EJ decides. | all four | Don't act on the contradicted part; carry on with everything else. |
| 11 | **Rd6.1 clash.** A fresh session that reports a mismatch "asks EJ" about something a decision answers, so Rd6 fails. | claude, agy | Rd6's check excludes a Rd5.3 report. |
| 12 | A **fact about the outside world** (a vendor's limit) can be wrong while the code still matches it, so checking against the code can't catch it. | claude | Note only; this is a limit of Rd5, not a fix. |

## For the whole section, not just these two

None of the requirements says MUST, SHOULD or guidance (all four). The house rule is that a method earns SHOULD, not
MUST. This is a separate pass over the whole section, not part of item 2.
