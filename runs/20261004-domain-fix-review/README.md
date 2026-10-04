# The domain fix review — a designed workflow, gated and executed

EJ, 2026-10-05: after the mutation matrix, record what is *not* fixed, then design and run a workflow that uses the
孫子兵法 research as domain knowledge for three expert agents, goes through the algorithm's issues **area by area**,
and sorts them into what can be fixed directly and what cannot.

## The design

Designed with the project's own method, and then **run through the project's own gate** — the tool reviewing the
workflow that reviews the tool:

```
$ python3 .claude/skills/workflow-design/scripts/design_gate.py runs/20261004-domain-fix-review/design.json
PASS
```

| node | engine | role | check |
|---|---|---|---|
| n1-claude | claude-opus-5-5 | survey, blind | `areas-survey.py` — all 8 areas, 45 ids, verdict from a fixed vocabulary |
| n2-minimax | minimax-m3.1-flash | survey, blind | same |
| n3-deepseek | deepseek-v4-pro | survey, blind | same |
| n4-chair | deepseek-v4-pro | join the three into `FIX_PLAN.md` | every register id carries a verdict; every DIRECT names a check |
| n5-verifier | claude-opus-5-5 | blind re-read of the surveys against the register | every DIRECT traceable to a test that can fail |

Readiness (method 3.1): the engines are the three proven today — claude 79–356 s, minimax 170–560 s, deepseek in
seconds as a subagent. **`agy` cannot take part**: headless it auto-denies the `command` permission it needs to read
a file, and the escape it suggests is the flag EXECUTOR_KINDS rule 3 forbids. Rule 2 routes research to agy, so the
routing and the tool disagree; that is a finding, not a reason to skip the review.

Sequential first (method 3.7): the three surveys are genuinely parallel — they do not read each other, and the whole
point is three independent readings. The chair is a barrier: it needs all three. The verifier needs the chair.

### The acceptance criteria

1. Every one of the 45 issues appears in each survey exactly once, with a verdict from
   `DIRECT | SCHEMA | DECISION | DOC | LATER`. Nothing silently dropped.
2. Every `DIRECT` names a runnable check. **A DIRECT without a check is a LATER** — a fix nobody can verify is not a
   direct fix.
3. `FIX_PLAN.md` reconciles the three, and says where they disagreed.
4. The verifier is a different session from the chair, and blind to the surveys until it reads them.

### The check, and its own proof

`areas-survey.py` parses the register for the expected areas and ids, then holds each survey to them. Its
`--self-check` feeds it a survey missing an area, carrying a nonsense verdict, and marking a DIRECT with no check —
and requires all three to be caught. It is not trusted until it has been shown to fail.

**One defect it had itself, found while writing it:** with no survey files present it exited 0. That is register 3.2
(absent directories report `verified`) reproduced in the checker that polices the surveys. It now fails on absence.

## Files

- `design.json` — the workflow, gate-checked
- `SURVEY_BRIEF.md`, `brief-*.txt` — the contract for n1..n3, identical but for the output path
- `areas-survey.py` — the check, with `--self-check`
- `surveys/areas-*.md` — the three blind surveys
- `FIX_PLAN.md` — the chair's join
- `VERIFICATION.md` — n5's blind re-read
- `run.sh` — what was executed, in order
