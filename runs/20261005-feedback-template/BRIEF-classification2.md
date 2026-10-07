# Classification, corrected — do you agree with this shape?

We are designing the **`classification`** feedback template (the summary a worker reports back). The author just
corrected what the type means, so re-read it:

> Classification is **sorting / managing / labeling data**. Example: *"identify which business rule belongs to
> which type of call file."* The worker labels a batch of items, and the return should show: **the labels, how many
> were labeled, and how many could NOT be labeled.**

A first draft to agree with or improve:

```
## Summary
- Labels:    <item → label, one line each>
- Labeled:   <N of T>
- Unlabeled: <M of T> — <which items, and why they could not be labeled>
```

The check is unchanged: *schema-valid label + agreement on a labeled sample*. The one rule over all templates: every
field has a writer, and the writer is the worker.

**Answer the author's question directly: agree or not — and if you change it, say what and why (3–6 whys).** Note in
particular whether the *count of unlabeled* is the worker's field or the verifier's, because that is the one thing
that has been argued twice already.

Rules: blind, concise, no file edits (reply or write to
`runs/20261005-feedback-template/<your-engine>-classification2.md`), leave the human's calls to the human.
