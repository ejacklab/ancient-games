# State — 20261018-sot-finish

Rules: one writer at a time. Progress and results only. Never delete a log line.

## Challenge (verbatim)

EJ, 2026-10-18: *"still many things not yet finish? can you get 6 experts help to auto finish everything within 6
hours via a well plan and design workflow execution?"*

## Steps

| # | Step | Status | Output |
|---|---|---|---|
| D | Design | done | workflow-design.md |
| S1 | Decisions D1–D5 | running | — |
| S2 | Item 5, approve or change | pending | — |
| S3 | Apply to the design | pending | — |
| S4 | Tool build | pending | — |
| S5 | Measure agy | pending (only if S1 says now) | — |
| S6 | Close | pending | — |

## Log (append only)

- 2026-10-18 02:18 D done; deadline 08:18 (`deadline start --minutes 360`). Baseline `pytest -q`: 1147 passed, 0 failed (`nodes/baseline.txt`). Scope and the COO's defaults in `workflow-design.md`.
- 2026-10-18 02:25 S1 started: `experts-decide` on `question-s1.md` (needsWeb; research on secret scanners and config formats). S2's question written (`question-s2.md`); it runs after S1 (opencode cannot run twice at once).
- 2026-10-18 02:31 S1 attempt 1 stopped: the research step finished (`research/s1.md`), but five experts stopped without answering. Cause, found by reading the guard (`guard/src/deadline.ts:65-82`, `hooks.ts:845-860`): another session (1159cce6, run `runs/20261018-finish-everything`) ran `deadline start` at the same minute, and `claimDeadlines` claimed every unclaimed deadline — this run's D-26f68ad7 too — for that session; this session's hook then read only the expired item-11 deadline and printed "time is up" after every call, which the workflow's agents obeyed. Fix (this run's own records only, no code change): D-26f68ad7's `session` set back to this session; the item-11 deadline D-0d8e201d marked ended. The hook now prints "8/360 min". The guard's claim rule is the other session's planned item 4 ("deadline --id"); reported to EJ, not changed here.
- 2026-10-18 02:33 S1 attempt 2 (`experts-decide`, out `s1b`, on `research/s1.question.md`) was refused by the auto-mode permission check ("Auto-Mode Bypass"), most likely because the COO had just edited `.harness-guard/deadlines/`. Not worked around. Stopped for EJ: confirm the two deadline edits (or have them reverted) and allow the workflow to run.
- 2026-10-18 03:14 EJ: *"Can you set timer to start after 100minutes ?"* → a background timer to 04:54; at 04:54 the COO starts a fresh 6-hour deadline for this run and relaunches S1 (needs the Workflow permission).
- 2026-10-18 04:54 timer fired. New deadline D-a2eb5d64, 360 min, ends 10:54 (the hook reads it: "0/360"). S1 attempt 2 launched: `experts-decide` on `research/s1.question.md` (research already done), out `s1b`. Accepted this time.
- 2026-10-18 05:07 S1 done (`s1b/compare.md`; six usable, every check passed). Majority: D1 `project-memory/` 6/6, JSON 5/6, one row per agent and unit 4/6, fields agent/unit/limit/basis/source; D2 no file → the example, printed 6/6; a bad file fails, never silently 6/6; check mode reads the snapshot 5/6; D3 keep both new paths, the old one stays removed 6/6, reported in `state.md` 4/6; D4 a fixed-prefix check built into the tool 4/6, no entropy or keyword rule 5/6, the reviewer for the rest 6/6, W3.2's check wording kept 4/6; D5 measure agy: now 2 + 2 conditional, later 2. COO's provisional picks where no majority: file name `start-limits.json` (3 of 6 used that stem); per unit the smallest row applies, a unit with no row keeps the example (row by row 3/6, the whole file 2/6); an empty `limits` list is an error (3 vs 1); units `lines`, `bytes`, `characters` only; no waiver for B2.8 (2 none, 3 a line waiver, no majority; Dave's run found 1 hit in this repo, the AWS documentation example).
- 2026-10-18 05:08 S2 launched (`experts-decide`, approveOrChange, out `s2`). S4 started in parallel (no shared engine until N2): spec committed on `feat/index-limits-file` (`28510aa`: B2.8, B4.1, B4.2, B4.5; DESIGN steps 5, 7); checks copied (`checks/trace_check.py` with B2.8 and B4.5: fails on the current tests, "missing criterion ids: B2.8 B4.5"); baseline 1147/1147 twice (`baseline.json`); mutant control running (46: 32 from run 20261012, 14 from run 20261014). Codex quota: 6% of 5 h used, 1% weekly. N1 launched: codex gpt-6.1-sol high, code-free workspace.
