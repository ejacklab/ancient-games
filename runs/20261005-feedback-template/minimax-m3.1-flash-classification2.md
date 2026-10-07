**Verdict: agree with the shape.** Three edits, one of which is the thing that's been argued twice.

## The argued point: `Unlabeled` count is the worker's field

Whys:

1. Only the worker has seen the batch. The verifier never sees the items — it sees a label on a sampled subset. So the verifier could not author the count even if we gave it the job.
2. A sample cannot produce M. It produces a rate with an interval. M is a property of the whole batch, not of the sample, so "the verifier computes it" is not a design — it's a different quantity with the same name.
3. If the worker reports only items and the verifier tallies, the count and its reasons become two records with two provenances, and the summary stops being what the worker claimed.
4. That's worst exactly where it matters: the silent-drop case — worker gives up on the hard items and doesn't mention them. A derived count hides that; a claimed count exposes it, because M is a number the worker is caught out on.
5. In every other template a gap is an accident. Here the gap is the finding. A gap the worker cannot report cannot be measured, and this template's whole purpose is to surface the unlabelable.
6. So the verifier gets a different verb: **falsify, not author.** It checks `Labeled + Unlabeled = T`, checks every unlabeled item carries a reason, and files a finding if the sample contradicts a label. Owner and checker stay two roles. Adding a verifier-written count would collapse them for no gain.

## Three edits

```
## Summary
T = <batch size handed to the worker; do not re-derive>
- Labels:       <item → label, one line each>
- Labeled:      <N of T>
- Unlabelable:  <M of T>
- Why:          <item → reason, one line per unlabelable item>
```

1. **Split the count from the reasons.** One prose "why" for M items is exactly where count and reasons drift apart; per-item reasons make M checkable by counting lines, which is the check the verifier can actually run.
2. **`Unlabeled` → `Unlabelable`.** "Unlabeled" reads as work-in-progress — will be done — not terminal, cannot be done. The reason field proves it's terminal, but the name shouldn't contradict it, and the invariant reads naturally: N + M = T, both now unambiguous.
3. **T is a contract, not a value.** If the worker restates the denominator it can restate it wrong. State it once, above the block; the three lines carry only the two counts.

Keeping both counts written out, redundantly, is deliberate — the redundancy is what makes them falsifiable. Don't derive one from the other.

## Three calls I left to you

- **Is the label set given to the worker, or proposed by them?** This decides whether "schema-valid label" is the worker's check or the template's.
- **Can T exceed a format's per-item line budget?** Needs a cap and a fallback that still leaves item→label addressable for sampling.
- **Does "could not be labelable" need a closed reason vocabulary?** Without one, M isn't comparable across batches — it becomes M-some-unknown-thing.
