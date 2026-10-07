# classification — feedback template (deepseek-v4-pro)

## Verdict

**Confirm** the three-field shape — `Item` / `Label` / `Agreed` — and add nothing. Three fields is
the right count for a one-line-output routing node; a fourth or fifth would be over-shape even if
defensible. The one thing to make explicit is already implied by the type's check: the allowed list
contains an escape hatch (`unknown`/`escalate`), so an ambiguous item is escalated, never forced into
a bucket — forcing is the exact sabotage this check exists to catch. That is a worker rule on `Label`,
not a new field. `Effort` stays out (loop types only).

## Template

```
## Summary
- Item:   <the thing classified, one line>
- Label:  <the label, from the allowed list>
- Agreed: <N/M> of the labeled samples matched the given answers
```

Worker rules (the field contract):

- `Label` is a value from the allowed list, and the allowed list includes the escape hatch
  (`unknown`/`escalate`). An ambiguous item gets the escape hatch, never a forced routing bucket.
- `Agreed` counts the worker's own labels on the pre-labeled calibration set against the given
  answers; it is a count, not a verdict.

## The six whys

No field added, no field removed — the six whys justify the confirm, field by field.

### 1. Confirmed — `Item`

1. Why does the worker write `Item`? Because a label with no thing attached is unattributed — the
   verifier cannot tell what was classified.
2. Why does that matter? Because the check (schema-valid label + sample agreement) and the downstream
   route both apply to a specific thing: "bug" is meaningful only attached to the ticket it buckets.
3. Why is the label meaningful only attached to the thing? Because classification is a function
   item→bucket; the output is a pair, never a bare label. **Stop — fact** (the shape of the type).
4. Why one line? Because a routing node's input is short text — a message, a ticket, a snippet — so one
   line is the item itself, or its handle. **Stop — value judgement**: if items can be large, one line
   is a handle the verifier must be able to resolve; I flag it rather than add a field.

### 2. Confirmed — `Label`

1. Why does the worker write `Label`? Because the label is the node's entire output.
2. Why is the label the entire output? Because classification is a routing node: its result is a bucket
   choice that downstream branches on.
3. Why does downstream branch on it? Because routing maps each bucket to a different next node — that is
   what the type is. **Stop — fact.**
4. Why "from the allowed list" and not free text? Because only a schema-valid label has a defined next
   node to route to. **Stop — fact** (the schema-validity half of the check).
5. Why does the worker, not the verifier, write it? Because the label is the worker's answer; whether it
   is correct is the human's verdict, which lives elsewhere. **Stop — the one rule.**

### 3. Confirmed — `Agreed`

1. Why does the worker write `Agreed`? Because the check has two parts — schema-valid label *and*
   agreement on a labeled sample — and a summary that shows only the label shows half the task.
2. Why does agreement on labeled samples matter at all? Because for the real item there is no ground
   truth yet; the labeled sample is the only ground truth available.
3. Why is agreement the proxy for "understands the buckets"? Because the human owns the bucket
   definitions, and matching the human's pre-given labels is the only observable test that the worker
   read them the same way. **Stop — fact** (the agreement half of the check).
4. Why one number (N/M) instead of the per-example labels? Because the gate needs only the count; a miss
   is the verifier's cue to open the run log and see which, and listing each would bloat a
   one-line-output shape. **Stop — value judgement** (keep it simple).
5. Why does the worker write the count rather than the verifier computing it? Because the per-example
   labels live in the run log, not the summary — the worker's count is the only trace of the calibration
   in the known shape; the verifier re-checks it against the log. **Stop — fact** (where the data lives).

### 4. Omitted — `Effort`

1. Why no `Effort`? Because the rule puts Effort (tokens + rounds) on loop types only, and classification
   is a single routing node.
2. Why does that rule exclude it here? Because "rounds" is the load-bearing half, and a single node has
   exactly one round — the field would be degenerate.
3. Why is Effort tied to loops? Because its job is the loop's limit and stop condition, and there is no
   loop here to bound.
4. **Stop — fact.** The loop-types-only rule is the author's (2026-10-05/06); I record it, I do not
   extend it.

### 5. Omitted — a "why this label" / confidence field

1. Why no reason or confidence field? Because the check tests schema-validity and sample agreement — it
   does not test reasoning or confidence.
2. Why does an unchecked field get rejected? Because a field the verifier cannot check becomes free text —
   the exact thing the template exists to eliminate.
3. Why does free text defeat the template? Because the template's purpose is "a known shape instead of
   free text", and a known shape is one a check can run against mechanically; unverifiable prose is
   noise. **Stop — fact** (the purpose of the template).
4. Why not add it for the human to read anyway? Because the human's verdict is on the label, not the
   narration; if a reason is wanted, it is a different artifact with a different writer. **Stop — the
   one rule.**

## Left for the human (not mine to decide)

- The allowed list itself — which routing buckets, and the exact name/shape of the escape hatch
  (`unknown` vs `escalate` vs both). The field says "from the allowed list"; the human defines the list.
- The calibration pass threshold — does `Agreed` require N = M, or a minimum? The brief says "agreement"
  but not how much. I report N/M and do not pick the threshold.
- Whether the calibration set contains an ambiguous example whose given answer is the escape hatch. If it
  does not, "agreement" cannot catch the one sabotage the type names (a forced label on an ambiguous
  sample).
