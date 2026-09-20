# State — <run id>

Rules: one writer at a time. Read this file before your step; update it after. It holds progress and results only —
never reasoning; put notes in your own output file. Never delete a log line.

## Challenge (verbatim)

<the challenge exactly as it was given>

## Baseline

Output of `git status --short`, taken before the run folder was created. The run may add files only under its own
folder; the final check compares against this.

```
<output>
```

## Steps

Status is one of: todo · doing · done · blocked.

| # | Step | Status | Output file |
|---|---|---|---|
| 1 | Intake and readiness | todo | readiness.md |
| 2 | Algorithm and unclear spots | todo | algorithm.md |
| 3 | Size decision | todo | (recorded below) |
| 4 | Prompt file or workflow design | todo | prompt.md or workflow-design.md |
| 5 | Checks | todo | check.md |

## Size decision

<small | design> — steps: <n>, unclear spots: <n>, risk: <low | high>

## Unclear spots

| Id | What is unclear | Kind (information / decision / unknown) | Blocks steps | Depends on spot |
|---|---|---|---|---|

## Questions for EJ (one batch)

| # | Question | Provisional assumption if unanswered |
|---|---|---|

## Log (append only)

- <date> step <n> <status>: <one line>
