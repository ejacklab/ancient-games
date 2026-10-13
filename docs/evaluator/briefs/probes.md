# Evaluator step E4 — write probes from the spec

## Task (one deliverable)

For every case that `{RUN}/classify.json` marks `executable` or `static`, write at least one probe: a pytest test
that **fails if the case's failure happens**. Write them to `{RUN}/probes/test_<group>.py`. Do not run them against
anything but a dry collect.

## Context (only what this step needs)

Read only these:
- `{RUN}/workspace/spec/REQUIREMENTS.md` and `VISION.md`: the requirement sentences. **These are the standard. Test
  what they say, not what the code happens to do.**
- `{RUN}/requirements.json` and `{RUN}/classify.json`: the cases and their kinds.
- `{RUN}/workspace/product/`: the product, to learn its interface (command line, functions, file layout). Never copy
  its behaviour into an expectation. The expectation comes from the sentence.

You never see the product's own tests, and you never see the mutants (EV-C2.1, EV-C3.1).

## Template

- A module-level `test_*` function per behaviour. Its docstring **starts with** the case id(s), then one sentence
  saying which failure it catches: `"""B1-F1 — an untracked entry must not get a line."""`
- The product's path is the environment variable `EVAL_PRODUCT`. **Never write inside it.** Copy what a test needs into
  `tmp_path`.
- Isolate the machine: when a test runs git, set `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1` and author
  and committer variables. No network.
- Assert exact text only where the sentence gives exact text. Otherwise assert exit codes, file contents and names.
- Standard library and pytest only.

## Example (real: the evaluator's own case EV-P1-F2, "MEETS is given with an UNKNOWN")

```python
import json, os, subprocess, sys
from pathlib import Path

def test_one_unknown_means_not_meets(tmp_path):
    """EV-P1-F2 — a run with one UNKNOWN case must not answer MEETS."""
    product = Path(os.environ["EVAL_PRODUCT"])
    (tmp_path / "requirements.json").write_text(json.dumps({
        "spec": {"requirements": None, "vision": None},
        "groups": [{"group": "X1", "title": "t", "ids": ["X1.1"], "status": "in_scope", "fails_if": "a",
                    "cases": [{"case": "X1-F1", "text": "a"}], "open_ids": []}],
        "vision": [], "manifest": ["X1.1"]}))
    (tmp_path / "classify.json").write_text(json.dumps({"cases": [{"case": "X1-F1", "kind": "human", "reason": "r"}]}))
    r = subprocess.run([sys.executable, str(product / "tools/evaluator/verdict.py"), "--run", str(tmp_path)],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert json.loads((tmp_path / "verdict.json").read_text())["meets"] is False
```

Copy the shape: one case per test, the docstring first, `EVAL_PRODUCT`, `tmp_path`. The content is only an
illustration.

## Standard (how this step is judged)

1. `python3 -m pytest --collect-only -q -c /dev/null {RUN}/probes` collects with no error.
2. Every `executable` and `static` case id appears at the start of a probe docstring. A case you could not probe gets
   no probe, and you name it in your reply with the reason. It becomes UNKNOWN; it is never skipped silently.
3. **Later, out of your sight,** each probe must stay green on the real product if the requirement holds, and turn
   red on a copy broken for its case. A probe that checks only "exit 0" will not survive that.

## Write the result to

Write every file with the Write tool, not with shell redirection such as `cat > file`. Then list the file once to confirm it exists: a step whose file is missing has failed, and the run stops there.

The probe files, then one reply line: the number of probes, and any case ids without a probe, each with its reason.
