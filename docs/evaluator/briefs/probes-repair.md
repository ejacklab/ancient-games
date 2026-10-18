# Evaluator step E8-repair — rewrite the probes the confirm step judged unfaithful (one round only)

## Task (one deliverable)

The confirm step judged some probes **not faithful** to their requirement: each asserts something its requirement
sentence does not say. Rewrite **only those probes**, so each tests exactly what its sentence says. This happens
once per run (EV-C4.2); there is no second round.

## Context (only what this step needs)

Read only these:
- `{RUN}/confirm.json`: the entries with `faithful: false` that have **no** `note`. Entries with a `note` were voided
  by the script (no failure output, a quote not found, or a file the blind workspace removed); leave those alone.
- `{RUN}/confirm-input.json`: for those probes, the requirement sentences (`group_text`), the probe's source and its
  failure output.
- `{RUN}/workspace/spec/REQUIREMENTS.md`: the sentences in full.
- `{RUN}/probes/`: the probe files to edit.

You never see the product's tests or the mutants.

## Template

- Edit the probe function in place, in its own file, keeping its **name** and the case id at the start of its
  docstring.
- Assert only what the requirement sentence says. If the sentence cannot be tested without the extra assumption that
  made the probe unfaithful, **delete that probe function**. Its case then becomes UNKNOWN "no probe", which is
  honest.
- `EVAL_PRODUCT` and `tmp_path` work as before. Never write inside `EVAL_PRODUCT`.

## Example (real, from calibration K1c)

- **The requirement**, B2.3: *"No two entries share an `id`."*
- **The unfaithful probe** asserted that the error message names **both** files. B2.3 does not say that.
- **The rewrite** keeps the parts the sentence supports: the run exits 1, and the output names at least one of the
  two files. It drops "names both".

## Standard

- `python3 -m pytest --collect-only -q -c /dev/null {RUN}/probes` still collects.
- Only the listed probes changed. The matrix and the confirm step run again afterwards, and they judge the result.

## Write the result to

Write every file with the Write or Edit tool, not with shell redirection. Reply in one line: which probes you
rewrote, and which you deleted.
