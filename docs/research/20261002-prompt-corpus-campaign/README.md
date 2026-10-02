# Prompt-corpus campaign — 2026-10-02

Three rounds of 100 prompts each, testing the §3.0 understand-step + TASK_TYPES default-first pipeline against
300 prompts derived from `tests/operator-prompt-list.md` (EJ's real operator library) plus synthetic prompts in
the same voice. Enhancement at each round's end; blind design review in round 3; canaries and executor samples
via codex and agy (quota approved by EJ).

| File | Content |
|---|---|
| `round1.md` | p001–p100: 35 script bugs (2 missing categories, tri-state product defect), executor baseline 12%/24%, labelling rules v1 |
| `round2.md` | p101–p200: rules effect measured (codex 84%, agy 72%), five disagreement classes, rules v2 |
| `round3.md` | p201–p300: gate caught the corpus author's own label; 100 designs generated; blind review rejected 3/5 with real defects; repairs verified ACCEPT |
| `REPORT.md` | the final report: what was fixed/enhanced, agreement trajectory, principle changes (none), known limits |

Raw evidence (untracked): `runs/20261002-prompt-corpus-campaign/` — state file, canary logs, batch prompts,
executor raw outputs, per-round results and bug lists, the 100 emitted designs.

Status legend as elsewhere: verified (command run, dated) / reported (source claims) / n-markers. The
campaign measured *routing* (300 classifications, 300 gated designs); it did not execute any real workflow —
`docs/TASK_TYPES_LEDGER.md` is still empty, so all defaults remain n=0 for execution.
