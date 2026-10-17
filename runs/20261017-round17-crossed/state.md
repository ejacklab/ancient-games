# State — run 20261017-round17-crossed

Times are from the files' and commits' timestamps (`ls -l nodes/`, `git log`), written after the fact.

Request: "run the crossed check on round 17". Criteria: `criteria.yaml` (4/4). Report: `report.md`.

## Log
- 11:20 crossed-build-check started (wf_a9e82ef9-09e): base 5ffe562, head 0cb4657; tests by opencode, review by codex.
- 11:24 done: 15 tests (6 red on base, 15 pass on head); review 7 findings.
- 11:25 findings reproduced (`probe.ts`, `nodes/probe.base.txt`, `nodes/probe.head.txt`): 1 a regression, 2/3/4/5/7 existed before, 6 SPEC wording; 1 and 6 fixed (T5 red first); commit b6f361f at 11:27.
- 11:32 EJ: "go with your pick, option 1, and push" — findings 2, 4, 5 fixed (T6–T8, two opencode pipe tests changed, all red first); 3 and 7 kept as known limits in SPEC Round 17; insight option 1 as a working rule; 1376/1376; commit 49fe260, pushed.
- 11:39 insight decisions moved to `insight-decisions.md` (EJ: a separate file for the owner's choices).
