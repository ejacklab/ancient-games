# Evaluator step E3 — classify each failure case

## Task (one deliverable)

Give every failure case in `{RUN}/requirements.json` exactly one kind, with a reason. Write `{RUN}/classify.json`.
You do not check anything yourself, and you do not write tests.

## Context (only what this step needs)

Read only these:
- `{RUN}/requirements.json`: the groups, their requirement sentences (in the spec), and their failure cases.
- `{RUN}/workspace/spec/REQUIREMENTS.md` and `VISION.md`: the sentences behind each case.
- `{RUN}/workspace/product/`: **only a file listing**, to see what kind of thing the product is (a CLI, a library,
  docs, config). Do not read source code to decide whether a case holds.

## The four kinds (EV-C1.1)

| kind | when | example |
|---|---|---|
| `executable` | a test can run the product and observe the failure | "MEETS is given with an UNKNOWN": run the verdict script on a run folder holding one UNKNOWN case and read `meets` |
| `static` | inspecting files or config, without running behaviour, can tell | "the probe writer and the mutant writer are the same kind": read the engine names in the workflow's plan |
| `judged` | only reading the code against the sentence can tell | "a model's text is the verdict": only reading the workflow shows whether any model output is copied into the verdict |
| `human` | only EJ can tell, or you are unsure which of the other three applies | a requirement whose only check is EJ's acceptance |

## Template

```json
{"cases": [{"case": "<case id>", "kind": "executable|static|judged|human", "reason": "<one sentence: how it would be checked, or why only EJ can tell>"}]}
```

## Example (real cases from the evaluator's own requirements, `docs/evaluator/REQUIREMENTS.md`)

```json
{"cases": [
 {"case": "EV-P1-F2", "kind": "executable", "reason": "run verdict.py on a run folder with one UNKNOWN case; meets must be false"},
 {"case": "EV-C3-F2", "kind": "static", "reason": "read the engines the workflow names for the probe and mutant steps; they must differ in kind"},
 {"case": "EV-P1-F3", "kind": "judged", "reason": "only reading the workflow shows whether a model's text reaches verdict.json"}
]}
```

## Standard

- Every case id in `requirements.json` appears exactly once, and no other id appears.
- Every `reason` is a non-empty sentence. An empty reason turns the case into `human` (EV-C1.2), so a missing reason
  costs a verdict.
- If you hesitate between two kinds, choose `human` and say why. A forced label is the failure this step is judged on.

## Write the result to

Write every file with the Write tool, not with shell redirection such as `cat > file`. Then list the file once to confirm it exists: a step whose file is missing has failed, and the run stops there.

`{RUN}/classify.json`, written to a temp name and renamed. Return one line: the counts per kind.
