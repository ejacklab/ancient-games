I'll read the project context first before answering.
Read `CLAUDE.md`, `docs/FEEDBACK_TEMPLATES.md`, the `web search` row in `docs/TASK_TYPES.md:98`, and the public `COMPARISON-test-data-gen.md` (different type, blind period already over for it). I did not open another engine's `web-search` answer — there is none.

## Verdict

**Keep three fields, change all three: `Sources` folded into `Found`, `Disputed` narrowed to the split, and `Found` given the not-found shape the type's own sabotage test demands.** No new field, no `Effort`.

```
## Summary
- Found:
    FACT     <claim> — <site/publisher, published YYYY-MM-DD | "undated", URL>   [N sources — independent | same]
    INFERRED <claim> — <the reason it follows from the FACT lines above>
    GAP      <asked fact> — not found; searched: <query, where>; or: exists at <URL> but undated
- Disputed: <fact> — <k of n> say A (list), <m> say B (list), split <why>; or: none found
```

The `FACT / INFERRED / GAP` vocabulary is borrowed from `research and reports` (`TASK_TYPES.md:100`) rather than invented — same reader, same words. GAP is the not-found slot the sabotage test needs; `evidence` (which should point into `runs/<run-id>/`, `CLAUDE.md:102`) carries the search log, so the summary stays a summary.

## Whys — remove `Sources`

1. Why was it a separate field? So one source can back several claims.
2. How often is that true? **Unknown — n=0.** It depends on real prompts (p267 "link the release note" is the shape where it would happen).
3. So why remove it on an unmeasured case? Because both fields were keyed to "each claim" — one fact, two writers. A claim added to `Found` without a `Sources` line is drift, and a verifier reading two lists cannot tell a missing source from a missing claim.
4. Why is that failure worse here than in the sibling types? Because this check is *traceability*, and an untraceable line is the exact thing being checked for. In test-data-gen the second writer was a path (obvious drift); here it is a citation.
5. What's the cost of duplicating a URL on three lines? Reader noise. **Value judgement** — I take noise over an invisible join.
6. And `Disputed` is where N sources meet one claim: there the re-listing is load-bearing, not drift-prone, because showing sources side by side *is* the field.

**The one input that flips this:** a prompt where one primary source (a spec, a release note) answers most of the question. Then the separate list earns its keep. I have no count of how often that happens — **EJ's to measure, not mine to guess.**

## Whys — `Disputed`: the split, never the resolution

1. Why does it exist? The pattern is "single node; **voting** on contested facts" (`TASK_TYPES.md:98`).
2. Who is voting? **Nobody can.** A single node is one worker. Either voting means *sources* outvoting each other, or the pattern is really a swarm — and then the row's "single node" is wrong.
3. Stop — **fact.** That is a question about the design, not the template, and it decides whether `Effort` exists (below). **Open for EJ.**
4. Assuming sources: what does the worker write? The split: how many dated sources say what, and why they differ.
5. Why must the resolution be left out? The proposal's "the voting" invites "3 say A, 2 say B, therefore A" — averaging sources by count. The method's own verify rule forbids it: two disagreeing sources "are reconciled with a reason, never averaged" (`TASK_TYPES.md:76`). A source count is not a truth criterion.
6. Why is "reconciled with a reason" not the worker's to write? Because settling it needs a threshold — how many independent sources suffice, what a tie does. `Corroborate` is the framework's stage for that number (`PROJECT_OVERVIEW.md`). **I will not invent it** (`CLAUDE.md:87`). It goes in the field as *unresolved* until EJ sets the number.
7. Why does `or: none found` stay in the field, rather than omitting it when nothing is contested? Precedent: `Look` carries the negative inline ("and which states it does NOT show", `FEEDBACK_TEMPLATES.md:33`), and `Coverage` ends "required but not covered: none". An absent line is indistinguishable from a worker who never looked.

## Whys — `Found`: give it the failure case (the type's own sabotage)

1. Why must the shape hold a not-found? Because the sabotage that proves this check can fail **is** the not-found answer: "ask a nonexistent fact → must return not-found" (`TASK_TYPES.md:98`). The type's proof case is the one case the proposed shape cannot write.
2. So what does the worker do instead? Write the best guess in `Found:` — an empty answer field reads like a broken worker, and a plausible sentence costs nothing.
3. Why is that the worst failure available to this type? A hallucinated URL with a plausible date is the cheapest thing a model emits and the hardest for a reader to catch. Other types' wrong answers are *visibly* wrong (a red test); this one is formatted exactly like the passing case, which is what the check exists to detect.
4. Why must GAP name **what was searched**? Because "not found" and "does not exist" are different claims, and only the search trail tells them apart — the same reason bare `Validated: passed` was unfixable in test-data-gen: an unfalsifiable field is the shape that has to be ignored.
5. Why not a fourth field `Not found:`? It re-states one fact in a second place and reads as a footer. GAP *is* `Found` with nothing found — one field, the negative inside it, like `Look` and `Coverage`.
6. Why the per-line `FACT / INFERRED / GAP` prefix rather than a separate `Certainty:` field? (a) A claim's status is only meaningful *next to that claim*; a separate list decouples and drifts. (b) The default-first rule (`FEEDBACK_TEMPLATES.md:4`) means a prompt may propose a different shape: p267 ("did the new SDK fix it, link the release note") needs no INFERRED line at all, p175 ("is 23 required for the runner") is *mostly* INFERRED. A prefix degrades gracefully; a required field cannot. **Value judgement.**
7. Why does a worker get to write "INFERRED"? Because it is a fact about how the claim was derived, not a judgement of adequacy — it passes the writer rule (`FEEDBACK_TEMPLATES.md:7`). "This source is bad" would fail it.

## Whys — the source line's content (this is the real fix in `Sources`)

1. Why does the field need *more* than "dated source + URL"? Because the check's words — dated, with URLs — are the two cheapest attributes of a source to fake. A forum post dated last week has both and carries no weight.
2. Why can't the worker judge quality instead? "This source is unreliable" is a verdict on adequacy → the human's, not the worker's.
3. So what survives as a worker's fact? **Publisher and count** — 2 sources from the same author/publisher is not 2 sources. That makes independence checkable, which is what `Corroborate` counts.
4. Why is publisher a field-level improvement rather than a new field? Because it is *per source*, not per run — and it costs no line of its own.
5. Why must `undated` be an allowed value? Because if "dated" is mandatory and the page has no date, the worker writes a plausible date. A required field with no honest value gets filled with a fiction — the bare-`passed` shape again. **Whether an undated source is admissible at all is EJ's policy; the slot must exist either way.**

## Whys — `Effort`: absent, and its absence is now conditional

1. Why absent? Loop types only (`FEEDBACK_TEMPLATES.md:21`), and the row says single node.
2. Why flag it? Because if "voting" turns out to mean multiple *workers* (§`Disputed` 3), the fan-out is exactly where tokens and rounds stop being a constant.
3. So `Effort` on this type is a **switch**, not a fact: loop, and it appears. **Same question as the voting one — one decision, two consequences.**
4. Open: `TASK_TYPES.md:84` records that a binary column once made a whole category "look like a lie", and tri-stated it. Is `loop?` tri-state for the same reason here? Not mine to decide.

## Requirement check on the proposal's own words (per `CLAUDE.md:62`, evaluate — not apply)

- **"dated source + URL"** — fails *one thing* and *unit*: one word, two numbers. A page's **publication** date (is the fact current?) and the **access** date (can someone re-fetch it and see it changed?) are different facts with different failure modes, and on a page with no visible date the first is unanswerable. Split into two, each named.
- **"contested facts and the split — the voting"** — fails *can it fail*: name one input. `Disputed: 2 say A, 3 say B` cannot fail; nothing obliges the worker to do anything next. Fixed by the split-only rule above.
- **"the answer/facts, one line each"** — weak word **facts**. Which of a dozen things is a fact here — a quoted fact, a conclusion, an absence? Three, hence three labels.
- **"every field has a writer, and the writer is the worker"** — same gap I flagged last round: it catches *who writes*, not *what the worker may claim* (`Found: sufficient` passes it). And it is silent on the failure case, which is where this type's proof lives. Candidate addition, phrased as: *a worker field is a claim about a run, never a verdict on adequacy, and a task that found nothing says so.* Level (MUST/SHOULD) and basis (n=1) are EJ's.

## Left for EJ — the human's calls, not mine to fill

1. **Voting: sources or workers?** Decides the pattern row, `loop?`, and `Effort`. One question, three consequences.
2. **The corroboration number** — how many independent sources settle a claim, and what a tie does. Until then `Disputed` ends unresolved.
3. **Is an undated source admissible**, or does it force GAP/UNPROVEN? The slot must exist; the policy is yours.
4. **Staleness** — how old is too old. A worker told to produce fresh sources will drop the true old one; that threshold belongs to the check, not the summary.
5. **Does this type want reasoning at all?** p175 wants INFERRED as the deliverable; p267 does not. If the answer is "no reasoning ever", delete the INFERRED label.

Plan mode is on, so I wrote nothing. Say the word and I'll write this to `runs/20261005-feedback-template/minimax-m3.1-flash-web-search.md`.
