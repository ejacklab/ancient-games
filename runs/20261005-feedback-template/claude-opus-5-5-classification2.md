**I agree with the shape, with one change.** The unlabeled count belongs to the worker.

```
## Summary
- Labels:    <item → label, one line each>
- Labeled:   <N of T>
- Unlabeled: <M of T> — <which items, and why they could not be labeled>
```

**The change: T should come from the brief.** The worker copies the item count from the brief instead of counting the items itself. If a worker silently drops two items, it can report "48 of 48" and nobody notices. When T comes from the brief, the same mistake shows up as 48 + 0 ≠ 50. So N + M = T becomes a check that doesn't depend on trusting the worker.

**Why the unlabeled count is the worker's field:**
1. **Why report it?** So the reader knows how much of the batch is actually done.
2. **Why the worker?** Only the worker tried every item, so only the worker knows which ones it gave up on.
3. **Why not the verifier?** The verifier checks a sample. To count unlabeled items across the whole batch, it would have to redo the work.
4. **So what has the argument been about?** I think the two earlier rounds mixed up two different numbers:
   - **"could not label"**: the worker knows this, so it goes in the summary.
   - **"labeled wrong"**: the worker can't know this, or it would have fixed it. The verifier finds it from the sample, and it goes in the verdict, which is a separate artifact.
5. **Why list the items and a reason, not just M?** So the human can act on it: add a missing label to the set, fix the input, or settle a tie.

**The check fails when:**
- N + M ≠ T, or T doesn't match the brief.
- A label isn't in the label set from the brief.
- An unlabeled item's reason is empty, `TBD` or `—`.
- The Labels list doesn't have exactly N lines.

**Your calls (I haven't filled these in):**
1. **One label or several?** Can one business rule belong to more than one call-file type? If yes, "item → label" becomes "item → labels", and "labeled" needs a definition.
2. **Large batches.** One line per item works for 20 items, not for 2,000. Is there a size above which the list goes to an evidence file in `runs/<run-id>/` and the summary only gives the path? If so, what size?
3. **Can the worker leave an item unlabeled?** If the brief doesn't allow it, M will always be 0 and the field tells you nothing. That rule belongs in the brief, not in this template.

I didn't add confidence scores, per-label counts or reason categories, because nobody asked for them. A per-label count would make lopsided results easy to spot. If you want it, the worker would write it.

I didn't read the other engines' answers. My answer is saved in `runs/20261005-feedback-template/claude-opus-5-5-classification2.md`.

Separately: several connectors (Gmail, Calendar, Drive, and some plugin servers) need authorizing in claude.ai or via `/mcp` before they'll work, and `plugin:data:definite` failed to connect. None of them were needed for this.
