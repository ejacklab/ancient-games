# State — 20261017-w36-worth-scripting

Rules: one writer at a time. Read this file before your step; update it after. Progress and results only — never
reasoning. Never delete a log line.

## Challenge (verbatim)

EJ, 2026-10-17: *"design a workflow to use the 6 experts to research and fix item 13"* — item 13 of the TODO in
`runs/20261014-sot-yaml-review/state.md`: *"'Can' versus 'worth it': may a scriptable procedure stay a page because
it runs rarely, and who decides that?"*

## Steps

| # | Step | Status | Output |
|---|---|---|---|
| D | Design | done | workflow-design.md, question.md |
| P1 | Research and six experts (`experts-decide`) | done | research/experts.md, experts/compare.md |
| P2 | Proposal from the majority (EJ: apply it directly, then show) | done | nodes/p3.result.md |
| P3 | Apply, check, commit and push | done | nodes/p3.result.md |

## Log (append only)

- 2026-10-17 D done: design and question written. Reuses the saved workflow `.claude/workflows/experts-decide.js` (research + six experts + check + rerun + compare). Experts on the design's unclear spots: not asked, with the reason in the design.
- 2026-10-17 EJ: *"go , q1 : an hour , q2 : directly use what the mejority sasys and shows me"*. Q1: the run has 60 minutes (`deadline start --minutes 60`). Q2: the COO applies the experts' majority wording directly, commits and pushes, then shows EJ; EJ may overrule after. P1 started.
- 2026-10-17 P1 done (`experts-decide`, 16 agents, 810k tokens, about 14 minutes): research 22 findings (17 verified, 4 reported, 1 not found: no measured break-even for scripts against pages); all six experts usable, every check passed, 老子 rerun once; `experts/compare.md`.
- 2026-10-17 P2/P3 done: majority applied to W3.6 (text, `fails_if`, `who_decides`), the prose sentence and the release notes; the three checks pass (`nodes/p3.result.md`). Committed and pushed with this file.
