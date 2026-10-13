# Evaluator step E9 — judge the cases only reading can decide

## Task (one deliverable)

For each case you are given (the `judged` cases), decide whether the product **holds**: whether the case's failure
does **not** happen. Quote file:line evidence for each. Do not fix anything.

## Context (only what this step needs)

You are given **one** of two call shapes (R1-F2: call 1 is never told the run folder).

- **Call 1** (`CALL=1 JUDGE_DIR=<folder>`). Read only `{JUDGE_DIR}/judge-input.json` (the case ids, their failure
  texts and their groups' requirement sentences) and `{JUDGE_DIR}/product/`, the product's code. This copy **may
  contain one planted defect** that makes one of your cases fail. You are not told which case; finding it is part of
  how this judging is checked. Write `{JUDGE_DIR}/judge-1.json`. `<file>` paths are relative to
  `{JUDGE_DIR}/product/`.
- **Call 2** (`CALL=2 RUN=<run> PRODUCT_COPY=<folder> CASE=<id>`). Judge **only** case `{CASE}`, using
  `{RUN}/judge-input.json` for its text and `{PRODUCT_COPY}/` for the code. Write `{RUN}/judge-2.json`.

Judge every case on what the code actually does, not on what its comments or names say. You see nothing else: no
tests, no probes, no other run files.

## Template

`<file>` is the path **relative to the product folder you were given** (`{JUDGE_DIR}/product/` in call 1, `{PRODUCT_COPY}` in call 2), for example `tools/x.py`.

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

Write every file with the Write tool, not with shell redirection such as `cat > file`. Then list the file once to confirm it exists: a step whose file is missing has failed, and the run stops there.

`{JUDGE_DIR}/judge-1.json` in call 1, `{RUN}/judge-2.json` in call 2. Reply in one line: the counts of holds and does not hold.
