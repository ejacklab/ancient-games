I'll start by reading the project conventions and exploring what's already there.
I improved it rather than confirming it. Sources read: `CLAUDE.md`, `docs/TASK_TYPES.md:89`, `docs/FEEDBACK_TEMPLATES.md`, `docs/workflow-templates/result-file.md`, `node-brief.md`, `validate_result.py`, one real reviewer return (`runs/20261005-code-graph-tool/nodes/n5-review-1.result.md`), and the `code review` row of the task-type ledger. I did not open the other engines' answers.

## Verdict

**Keep `Basis` (it is the load-bearing field), fold `Why` into `Method` as its tail, keep `Findings` but give it a count, delete `Report`, add one field — `Unclear`.**

```
## Summary
- Basis:    <what it was judged against — spec file:line / requirement ids / diff range>
- Method:   <checklist item -> pass | fail | skipped, one line each; anything it added or dropped
 over the default, and why — only when it deviated>
- Findings: <N total; each with file:line + one line. If truncated: N total, M above, rest at evidence>
- Unclear:  <what it could not decide, and what would decide it — or none>
```

First line: one sentence, per `result-file.md:18`.

## Why `Basis` is the one field that must never be empty

1. Why does it exist? A finding is a finding *against* something. "matches the spec" and "is wrong" are both defensible sentences; which is right depends entirely on what the reviewer held as correct. **Fact, n=1:** the real reviewer wrote `I took design attempt 4 as the spec (see UNCLEAR below)` — and could not settle it from the run.
2. Why not leave it to the brief? The brief says what it *offered*; the reviewer says what it *used*. In that run the two diverged and only the reviewer could see it.
3. Why not the draft's "the spec / requirements / diff"? Those are three bases giving three finding sets, and the placeholder lets a worker satisfy it by naming any one. Only a version that names *which file, which lines, which ids* can be re-derived.
4. Why does it matter more here than for other types? Because this row's check is a **fixed checklist**, and unlike a building node (method 3.6 supplies its checklist's three parts from the method itself), **nothing fixes a code review's checklist** — it is derived from the basis. *Stops at a fact:* `TASK_TYPES.md:89` names "fixed checklist" and names no source for its items.
5. So an unnamed basis ⇒ an unreproducible checklist ⇒ any reviewer who picks their own items passes. That is why the author said "review based on what" twice.

## Why `Method` + `Why` is one field

1. Why does `Method` exist at all? Most of it is already fixed by the default — blind session, risk-tiered engine, fixed checklist. "I walked the checklist" restates the brief.
2. What survives? What the brief cannot know: which items were answered, which skipped, what was added. 3-of-8 answered reads exactly like 8-of-8 passed. Precedent in the same file: `Look` carries "which states it does NOT show", `Coverage` ends "required but not covered: none".
3. What about "why that way"? It hides two cases. (a) *Why the design chose* a blind, risk-tiered method — not the worker's; it is in the brief and the state file. (b) *The worker deviated* — only it knows, and it is a fact about its own run. **Value judgement:** default-first (`FEEDBACK_TEMPLATES.md:4`) makes (b) a real case, since the LLM may propose a better shape "with a written reason".
4. So: one field, with the why attached to a deviation. A standalone `Why` invites the worker to re-argue the design's choice — i.e. invites a second writer, the exact failure the one-writer rule exists to prevent.
5. **Open for you, not decided by me:** if a worker *proposing* a method (not executing one) must justify it, that line goes at the tail of `Method` or in the state file where a proposal is actually made. Which one is a framework call.

## Why `Findings` keeps the field but earns the count

1. It *is* the check — `TASK_TYPES.md:89` names "findings with file:line" and the sabotage is the planted defect.
2. Why a locator per line? A defect claim without one cannot be re-opened, so it cannot be refuted either. `n5-review-1` is the working shape: each finding names `code_graph.py:730` and what the spec says instead.
3. What is missing from the draft? **How many exist.** The COO reads a capped number of lines (`result-file.md:3`, `validate_result.py --summary`); a truncated list is indistinguishable from a whole one. "31 found, 4 blocking above, 27 at evidence" is a fact about the run that nothing else carries — same move as `Labeled: N of T`.
4. Why does that not bring `Report` back? Because the *count* is what truncation needs; the *path* is already in the header. Two different things, only one was missing.
5. **Severity: left out.** The check doesn't ask for it and a 4-finding review doesn't need it. If 296-finding runs become the norm rather than the exception (`TASK_TYPES_LEDGER.md:17`), ordering becomes load-bearing — that is the run's call.

## Why `Report` goes

1. Why does it exist? "where the full report lives."
2. Why isn't `evidence:` enough? For most nodes evidence is a command's output; for a review **the proof *is* the report**. `validate_result.py:67` already checks the path exists.
3. Is it redundant, then? Yes whenever the summary is the whole report — which is what the real reviewer did: `evidence: none` and the entire review in the body.
4. Why is that not merely harmless? Two paths in one artifact is one too many: if `Report` names one file and the header names another (or `none`), the reader has no rule for which is authoritative. Its only non-redundant content is "what is *not* here", which belongs on `Findings` with the count.
5. **Left for you:** whether a review ever gets a body cap that makes a separate report mandatory. No result-body cap exists today (only digests, `validate_result.py:72`). If you add one, the count form survives and `Report` would come back for the overflow — I won't add it on a hypothetical.

## Why `Unclear` is added

1. Why add? The real reviewer used a heading the draft has no home for: `UNCLEAR: four design results exist, and the run log does not say which is "the spec" … Best guess: attempt 4`. *n=1*, and it was the review's most useful line — it names a fact about the **run**, not about the code.
2. Why is the worker its writer? Only it saw the ambiguity, and it is the one node positioned to notice it — the maker has the context that hides it.
3. Why may it not resolve the spot? Resolution is a second writer (the COO's, from the state file). So the field is written unresolved, naming what would decide it.
4. Why does it matter? A spot resolved in place is invisible to the design; a reported one is a hole in a record. Silent, it becomes the reader's assumption — the same shape as the missing checklist layer in `docs/research/20261004-sunzi/gate-review-minimax-m3.1-flash.md:249`, declared in a docstring and staffed in zero of 300 designs.
5. Name it `Unclear`, not `Questions`: a "Questions" field invites answers in the same field.

## Untouched

`Effort` stays absent — single node (`TASK_TYPES.md:89`). Whether a maker-repair round makes this a loop is minimax's open question for `test data gen`; it applies unchanged here, so I don't re-argue it.

## The brief's rules, evaluated (CLAUDE.md:62)

- **"every field has a writer, and the writer is the worker"** — passes source/one-thing/unit. Fails *can it fail*: a field the worker fills honestly that encodes a judgement only you may make (`Findings: nothing blocking`). It catches **who writes**, not **what the worker may claim** — which is why I added no verdict or severity field.
- **"Effort is loop types only"** — unit is fine; the rule is silent on repair rounds. Fails *level*: no MUST/SHOULD attached.
- **The check cell "fixed checklist; findings with file:line"** — fails *can it fail*: it doesn't say **who fixes the checklist**. A reviewer who writes their own checklist passes it vacuously. That belongs in the row, not the template, and it is the strongest thing I would send back to the table.

---

Plan mode is on, so I wrote nothing. Say the word and I'll write this to `runs/20261005-feedback-template/minimax-m3.1-flash-code-review.md` — and, with the blind period over, read the other engines' answers and report where we disagree.
