# Three experts on `test data gen` — 2026-10-05

Blind, six-whys, on the proposal `Created / Validated / Coverage` (+ the open `Location` question).

## Convergence (all three)

1. **`Validated: <passed>` is broken.** It can only ever say "passed", so on a failed run the worker lies or leaves
   it empty. All three fixed it: the field must name the schema/validator + command and report the **real outcome**
   (N pass / M fail), not a stamp.
2. **Drop `Location`.** The fixture path is already the harness-written evidence path; a worker-copied path is *one
   fact, two writers* (the "who fills it" rule, applied). The harness path cannot go stale; the worker's can.
3. **No `Effort`.** Single node, not a loop; Effort would be a constant.

## Where they differ

- **The field name.** deepseek: `Schema` — because `Validated: failed` is self-contradictory. claude + minimax kept
  `Validated` but changed its content. (I side with `Schema` for the same reason.)
- **`Coverage`'s key.** minimax: re-key it to **acceptance criteria ids** (R1.1 / N1.1), matching `test cases gen`,
  because the worker inventing its own edge-case list makes coverage self-graded and uncheckable. deepseek kept
  "edge cases". The *real* point all three share: **the covered set comes from the requirements, not the worker.**
- **A `Source` field.** claude alone: `synthetic | derived-from-real`, because real-derived fixtures can carry
  personal data into a public repo.

## Merged template

```
## Summary
- Created:  <path> — <what it holds, rows> — one line per file
- Schema:   <schema path> · <exact command> → <N pass / M fail> · corrupted row: rejected
- Coverage: <criteria id / edge case> → <file:row> · Not covered: <case> — <reason>, or none
```

## Open — EJ's, not the experts'

1. **Name** — `Schema` or `Validated`?
2. **The covered set's source** — requirements (criteria ids), or the worker's edge-case list? (All three say
   requirements; it decides whether `Coverage` is keyed to `R1.1` ids or to edge cases.)
3. **Add `Source: synthetic | derived-from-real`?** (claude's privacy flag.)
4. **`Location` consistency** — `test cases gen` keeps a separate `Location`; `test data gen` folds the path into
   `Created`. Both claude and minimax say the two types should follow one rule.
