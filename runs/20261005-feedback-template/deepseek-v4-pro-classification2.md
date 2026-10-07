# Classification template — verdict (deepseek-v4-pro)

**Agree** with the shape as drafted. It covers all three required outputs
(labels, labeled count, unlabeled count) and keeps every field worker-written.

## The argued point: who writes "Unlabeled: M of T"

**The worker.** M is a field on the worker's return, so by the one rule its
writer is the worker. It is not the verifier's field.

1. Only the worker attempted the whole batch, so only the worker knows which
   items could not be labeled and why. The verifier's check draws its sample
   from the labeled items and never touches the unlabeled ones — the verifier
   has no data from which to write M.
2. The one rule — every field has a writer, and the writer is the worker —
   makes a field's writer follow the artifact, not the check. A count the
   verifier produces would be a different field on a different artifact (the
   verdict), not a line on the worker's summary.
3. N, M and T are all known to the worker at labeling time (N + M = T, and T
   is the batch size the worker was handed). "Verifier recomputes M = T − N"
   adds no information and would put a second writer on one form.

## Flag (no change made)

"Which items, and why" is worker-reported and is not covered by the unchanged
check (agreement on a labeled sample). That is consistent with the rule, but it
means an unlabeled claim is reported, not verified. If unlabeled claims need
checking, that is a change to the check — the human's call, not mine.
