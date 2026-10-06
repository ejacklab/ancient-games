I'd keep the same three fields and change what goes in each. The data doesn't need a separate `Location` line, but the reason isn't that the result file already carries the path. Fixture paths should go inside `Created` instead.

I saved the full whys to `runs/20261005-feedback-template/claude-opus-5-5-test-data.md` (the one new file; nothing else edited). I worked blind and didn't open any other engine's file in that folder.

```
## Summary
- Created:   <path> — <what it holds, rows/records> — one line per file; "none (validation-only run)" if nothing was written
- Validated: <schema path> (given | written by me) · <exact command> → <N pass / M fail> · corrupted row: rejected | accepted
- Coverage:  <edge case> → <file:row/id>, one per case; Not covered: <case> — <reason>, or "none"
```

**Changes and their main whys:**

- **`Validated`:** the proposed `<schema validation passed>` can only ever say "passed", so the field can't fail. It now names:
  - the exact command, so a gate can rerun it;
  - where the schema came from, because if the worker wrote both the data and the schema, the data grades itself (a `{}` schema passes everything);
  - the corrupted-row result, which is this type's built-in proof that the validator actually rejects bad rows.
- **`Coverage`:** each edge case points to a row, and a `Not covered` part is required. Without those, coverage can't be checked and always looks complete.
- **`Created`:** each line starts with the file path. This task type also has a validation-only form that writes nothing, so the field says "none (validation-only run)" rather than staying blank.

**On `Location`:** the result file's header holds one `evidence` path, which by default is the result file itself (`design_gate.py:427`), not the fixtures. So that isn't why `Location` is unneeded. It's unneeded because the paths are already in `Created`, and a second list would drift from the first.

That clashes with `test cases gen`, which has a separate `Location`. The two types should follow one rule; I'd fold paths into `Created` for both.

**No `Effort`:** this type is a single step, not a loop.

**Left for you to decide:**
1. **Who runs the corrupted-row check, the worker or a script?** The pattern has no reviewer, and I couldn't tell which is intended. If a script runs it, drop that part from `Validated`, because the script's output doesn't belong in the worker's summary.
2. **Who supplies the edge-case list?** If the worker makes up its own list, the cases it missed are invisible to everyone. That belongs to the design, not this template.
3. **`Location`:** fold it into `Created` for both types, or keep it separate in both.
4. **Should there be a `Source: synthetic | derived from real data` field?** Fixtures built from real data can carry personal data into a public repo. I left it out because I have no real case of this happening.
