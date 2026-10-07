# classification — feedback template (claude-opus-5-5)

Worked blind: read only `BRIEF-classification.md` and the `classification` row of `docs/TASK_TYPES.md`.

## Template

```
## Summary
- Item:  <id or path of the input, as given — not a paraphrase>
- Label: <one value from the allowed list, or `unknown`>
```

Two fields. One field changed, one widened, one removed. No `Effort` (not a loop type).

## Whys

### `Agreed` — removed (the worker cannot honestly write it)

1. Why remove it? Because to write "N of M matched", the worker must compare its labels to the human's labels.
2. Why is that a problem? To compare, the worker has to see the human's labels.
3. Why does that matter? A worker that sees the answer key can copy it, so "Agreed" would measure copying rather than judgment.
4. Why do we need judgment measured? The real item has no answer key. Agreement on the samples is the only evidence
   that the real label is right.
5. So who writes it? Whoever holds the key: the verifier. It is a different artifact (the brief's rule: every field
   has one writer, and the writer is the worker). **Fact:** the worker cannot both not see the key and count matches.

What the worker contributes to calibration is simply its **labels** on the sample items, in the same two-field form.
The verifier compares them to the key.

### `Item` — changed to an id, not a paraphrase

1. Why keep it? A label alone does not say which input it belongs to. Downstream routing needs that pairing.
2. Why an id or path instead of "the thing, one line"? A one-line paraphrase is the worker's reading of the input,
   and that reading may have drifted from the input.
3. Why does drift matter? The verifier (and the agreement check) must re-read the **actual** input. If the input
   was misread, the paraphrase hides the misreading.
4. Why not include both? The paraphrase adds nothing the verifier can check that the id does not already point to.
   **Value judgement:** a checkable pointer beats a readable summary on a one-line type.

### `Label` — widened with `unknown`

1. Why add `unknown`? TASK_TYPES' sabotage check for this row is *"an ambiguous sample → unknown/escalate, not a forced
   label."* A template that only lists the buckets forces a label.
2. Why is a forced label bad here? This is a routing node, so the label decides which branch the item goes down.
3. Why does that matter more than elsewhere? The next node trusts the label; a wrong route is silent. No one sees
   the item that was never sent to the right place.
4. Why prefer `unknown`? A visible "I don't know" costs one human look. A silent misroute costs whatever the wrong
   branch does. **Value judgement:** the visible failure is the cheaper one.

### Not added (each rejected by a short chain)

- **Confidence** → an LLM's self-reported confidence is not calibrated → the samples are the calibration → it would
  be a second, weaker version of the same check. *Fact (the check already exists).*
- **Reason / rationale** → it is free text, and free text is what a template exists to replace → the check is
  agreement, not reading a reason → a stated reason is not necessarily the actual cause of the label.
  *Fact: the check does not read it.*

## Open for EJ — not filled in by me

1. **Are the calibration samples mixed in blind** (the worker cannot tell sample from real item), or run as a
   separate pass? Blind is stronger, but it is a design decision, not mine to make. Either way, the worker's form
   above does not change.
2. **`unknown/escalate`** in TASK_TYPES has a slash, which fails the "one thing" test. Is `unknown` the label and
   `escalate` what the graph does with it? Or are they two distinct outcomes?
3. **M and the pass mark** (how many samples, how many must match) belong to the verifier's check, not to this
   template. They are still unset.
4. **Many items in one run:** one block per item, or a two-column table? It is a format choice; the fields are the
   same.
