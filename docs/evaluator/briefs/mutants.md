# Evaluator step E5 — write one broken copy per case

## Task (two deliverables)

1. `{RUN}/mutants.json`: for each `executable` or `static` case in `{RUN}/classify.json`, **one** mutant, the
   smallest edit to the product that makes that case's failure happen.
2. `{RUN}/plants.json`: the same, for each `judged` case.

You never see the probes (EV-C3.1). You are a different engine kind from the probe writer, so your mutants do not
share its blind spots.

## Context (only what this step needs)

Read only these:
- `{RUN}/workspace/spec/REQUIREMENTS.md`: the failure sentences.
- `{RUN}/requirements.json` and `{RUN}/classify.json`.
- `{RUN}/workspace/product/`: the source you will edit (on paper; the script applies the edits).

## Template (DATA.md, E5)

```json
[{"case": "<case id>", "file": "<path relative to the product>", "old": "<exact text, occurring once in that file>", "new": "<replacement>"}]
```

- `old` must occur **exactly once** in `file`, or the mutant is invalid and its case cannot be PASS. Include enough
  surrounding lines to make it unique.
- **One case per mutant.** The edit must cause that case's failure and, as far as you can tell, no other. A mutant
  that breaks everything (a syntax error, deleting `main`) proves nothing about the case.
- If no single edit can produce a case's failure, leave that case out and name it in your reply with the reason.

## Example (real: the evaluator's own case EV-P1-F2, "MEETS is given with an UNKNOWN", against `tools/evaluator/verdict.py`)

```json
[{"case": "EV-P1-F2",
  "file": "tools/evaluator/verdict.py",
  "old": "return {\"meets\": all(row[\"verdict\"] == \"PASS\" for row in requirement_rows),",
  "new": "return {\"meets\": not any(row[\"verdict\"] == \"FAIL\" for row in requirement_rows),"}]
```

This edit makes an UNKNOWN count as passing, which is exactly the EV-P1-F2 failure, and nothing else. *(Run
2026-10-13: the probe in `probes.md`'s example passes on the real `verdict.py`, and fails with this mutant
applied.)*

## Standard

- Every entry's `old` occurs exactly once in its `file`. The script checks this, and an invalid mutant leaves its case
  unproven.
- Every `executable` and `static` case has a mutant, or is named in your reply with a reason.
- Each edit is one minimal change.

## Write the result to

Write every file with the Write tool, not with shell redirection such as `cat > file`. Then list the file once to confirm it exists: a step whose file is missing has failed, and the run stops there.

The two JSON files, each written to a temp name and renamed. Reply in one line: the counts, and the cases left out.
