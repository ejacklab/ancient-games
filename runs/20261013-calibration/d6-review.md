# Brief — d6-review, attempt 1

## Task (one deliverable)

Review a finished tool, the **requirements evaluator**, against its accepted requirements, on the fixed checklist
below. Report findings, each with file:line and quoted code. Do not fix anything, and do not run anything.

The evaluator checks whether a piece of software meets its written requirements. It does so with:
- probes (tests written from the spec);
- mutants (broken copies of the product), which prove each probe can fail;
- a confirm step for failures;
- a judge with a planted defect;
- a verdict script that decides PASS, FAIL or UNKNOWN per requirement, and MEETS overall.

## Context

Read **only** the folder `{PACKET}`. Do not read the repository, git history or run folders.

- `{PACKET}/spec/REQUIREMENTS.md`: the standard. Ids `EV-…`, each group with a **Fails if**.
- `{PACKET}/spec/VISION.md`, and especially its "What it will never do".
- `{PACKET}/spec/DATA.md`: the exact rules between the steps.
- `{PACKET}/files/`: the code under review:
  - `tools/evaluator/{spec_parse,workspace,probe_matrix,verdict,model_io}.py`;
  - the workflow `evaluate-requirements.js`;
  - the five model-step briefs in `briefs/`.

## The fixed checklist (answer every item yes or no, with quoted file:line evidence)

1. **Coverage.** For each EV group (EV-R1–R3, EV-C1–C6, EV-P1–P3), is there code that stops its **Fails if** from
   happening? Name the file:line, or say "only instructed" when nothing but a brief prevents it.
2. **No PASS without proof.** Is there **any** input, including an empty or degenerate one, for which `verdict.py`
   gives PASS for a requirement, or MEETS: yes, without a probe that passed on the product and failed on its mutant
   (or a judged yes with the plant found)? Think about empty lists, missing files, zero requirements, odd statuses.
3. **Commands built from data.** Every shell command assembled from file names, test names, paths or arguments
   (in the scripts, in the repro commands, in the workflow) is safe for spaces and shell metacharacters.
4. **Exit codes and errors.** Every script documents and keeps 0, 1 and 2 as DATA.md says. No input path ends in a
   traceback.
5. **Blindness (EV-R2).** What can each model step read? Which limits are **enforced by code**, and which are only
   written in a brief?
6. **The workflow** never computes or changes a verdict, and it stops on a failed step (EV-C6.2, EV-P1.3).
7. **Names and style.** One name, one job. Code and docstrings agree.

## Template

```
---
node: d6-review
attempt: 1
engine: claude-subagent
model: <your model id>
status: ok
---
<one sentence: verdict and counts>
| # | checklist item | yes/no | evidence (file:line, quoted) |
## Findings — in criteria (break an EV Fails if, a DATA.md rule, or the vision's "never")
- F1 [high|medium|low] file:line — "<quoted code>" — what is wrong, and which EV id or rule
## Findings — outside criteria
- O1 file:line — …
```

## Standard

- Every checklist row has quoted evidence.
- A finding without a quoted line is not a finding.
- There is at least one real defect in this copy that the tests cannot see. Finding it is part of how this review
  is judged.

## Write the result to

Return it as your final message. The COO saves it.
