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

## Product baseline (a product change only)

The product's test command and its output, taken by the run that builds, before its first step or piece that builds
(intake designs only, so it leaves this empty). "What passed before" means this. Leave out for a task that is not a
product change.

```
<command and output>
```

## Steps

Status is one of: todo · doing · done · blocked.

| # | Step | Status | Output file |
|---|---|---|---|
| 1 | Intake, readiness and blueprint check | todo | readiness.md |
| 2 | Algorithm and unclear spots | todo | algorithm.md |
| 3 | Size decision | todo | (recorded below) |
| 4 | Prompt file or workflow design | todo | prompt.md or workflow-design.md |
| 5 | Checks | todo | check.md |

## Blueprint

Kind of task: <not a product change | fix | feature | new product>. Map: <path, or none>.
Needed sections not settled: <section: draft | incomplete | missing, …, or none>.

## Size decision

<small | design> — steps: <n>, unclear spots: <n>, risk: <low | high>

## Unclear spots

| Id | What is unclear | Kind (information / decision / unknown) | Blueprint section (or none) | Blocks steps | Depends on spot |
|---|---|---|---|---|---|

## Questions for EJ (one batch)

| # | Question | Provisional assumption if unanswered | Must be answered before building (blueprint questions: yes) |
|---|---|---|---|

## Log (append only)

- <date> step <n> <status>: <one line>
