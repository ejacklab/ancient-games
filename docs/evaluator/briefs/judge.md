# Evaluator step E9 — judge the cases only reading can decide

## Task (one deliverable)

For each case listed in `{RUN}/judge-input.json` (the `judged` cases), decide whether the product **holds**: whether
the case's failure does **not** happen. Quote file:line evidence for each. Write `{RUN}/judge-{CALL}.json`. Do not fix
anything.

## Context (only what this step needs)

Read only these:
- `{RUN}/judge-input.json`: the case ids, their failure texts, and their groups' requirement sentences.
- `{PRODUCT_COPY}/`: the product's code. This copy **may contain one planted defect** that makes one of your cases
  fail. Judge every case on what the code actually does, not on what its comments or names say.

You see nothing else: no tests, no probes, no other run files.

## Template

```json
{"cases": [{"case": "<id>", "holds": true|false,
            "evidence": "<file>:<line> \"<the quoted code>\" — <one sentence why this holds or fails>"}]}
```

## Example (real, from a blind review in run `20261012-index-md-build`)

> **Case:** "the index is replaced by writing a temporary file and renaming it".
>
> ```json
> {"case": "X2-F1", "holds": false,
>  "evidence": "tools/x.py:453 \"with open(path, \"wb\") as stream: stream.write(rendered)\" — the target is opened and truncated directly; no temp file, no rename, though the docstring promises both"}
> ```

A reviewer found exactly that planted defect: the docstring described the right behaviour, and the code did not do
it. **Read the code, not the comments.**

## Standard

- One entry per listed case. `evidence` quotes code that exists at that file:line. A script checks the quote, and a
  quote that is not found voids that entry.
- `holds: false` needs the quoted line that breaks the sentence. `holds: true` needs the quoted line that satisfies
  it.
- Whether you find the planted defect is how this judging itself is checked. If you miss it, every answer here is
  void (EV-C5.2).

## Write the result to

`{RUN}/judge-{CALL}.json`. Reply in one line: the counts of holds and does not hold.
