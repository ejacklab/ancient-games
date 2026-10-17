# State — 20261017-sot-item11

Rules: one writer at a time. Read this file before your step; update it after. Progress and results only — never
reasoning. Never delete a log line.

## Challenge (verbatim)

EJ, 2026-10-17: *"design a workflow to use the 6 experts to research and fix item 11"* — item 11 of the TODO in
`runs/20261014-sot-yaml-review/state.md`.

## Steps

| # | Step | Status | Output |
|---|---|---|---|
| D | Design | done | workflow-design.md, question.md |
| P1 | Research and six experts (`experts-decide`) | done | research/experts.md, experts/compare.md |
| P2 | Apply the majority, check, commit and push | done | nodes/p2.result.md |

## Log (append only)

- 2026-10-17 D done: design and question written; every file the question cites is inside the repo. Reuses `.claude/workflows/experts-decide.js`, as run `20261017-w36-worth-scripting` did.
- 2026-10-17 23:47 EJ: *"go go go , let's do it on 2026-10-17 11:47pm"* — the defaults stand: Q1 60 minutes (`deadline start --minutes 60`), Q2 apply the majority directly and show after, Q3 a tool build is its own later run. P1 started.
- 2026-10-18 P1 done (`experts-decide`, 14 agents, 744k tokens, about 16 minutes): research verified the documented limits for six engines; six experts usable; 老子's check failed only on 為/爲 (a script variant); `experts/compare.md`.
- 2026-10-18 P2 done: majorities on A–E applied (W6.3a, the kit, Rd3.1a/b, prose, release notes); points with no majority listed in `nodes/p2.result.md` and the TODO; the three checks pass. Committed and pushed with this file.
