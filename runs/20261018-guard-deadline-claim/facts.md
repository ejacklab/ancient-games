# Facts (checked 2026-10-18 ~09:20 by the main agent)

## The deadline files (`.harness-guard/deadlines/*.json`, id · start · minutes · run · session · ended)
```
D-593045da  2026-10-17T18:18:18.023Z  360  runs/20261014-code-map-build       1159cce6-66c2-47bb-8a08-d44519140778  -
D-26f68ad7  2026-10-17T18:18:32.775Z  360  runs/20261018-sot-finish           7d643882-c1cb-4372-ae3c-68a4a559448b  -
D-17979aae  2026-10-17T18:18:45.732Z  360  runs/20261018-finish-everything    1159cce6-66c2-47bb-8a08-d44519140778  2026-10-18T00:34:56.359Z
D-e215bad1  2026-10-18T00:34:52.374Z  296  runs/20261014-code-map-build       16098663-21b0-4aad-9346-c02eeddbc506  -
```
D-593045da belongs to the code-map run but carries session 1159cce6 (this session, run finish-everything).

## How D-593045da was started
Session 16098663's transcript (`~/.claude/projects/-home-smoke01-dev-ancient-games/16098663-….jsonl`) holds the start
command `cd /home/smoke01/dev/ancient-games && G=.claude/skills/workflow-design/guard/src/cli.ts; ls $G
.claude/workflows/ ; bun $G deadline start --minutes 360 --run runs/20261014-code-map-build 2>…` and its output
`D-593045da: 360 min, deadline 08:18; …`.

## The claim
- `src/hooks.ts:851-857` (`withTime`): a PostToolUse of Bash claims when a segment's command word is `bun` and its
  text matches `/\/src\/cli\.ts\s+deadline\s+start\b/`; then `claimDeadlines(root, session)`.
- `src/deadline.ts:64-73` (`claimDeadlines`): every deadline with `session === null` gets this session.
- SPEC T1 (`SPEC.md:545`): "claims every unclaimed deadline file for its session".

## The pattern on three command forms (`bun -e`, regex from hooks.ts)
```
false  bun src/cli.ts deadline start --minutes 360
true   bun .claude/skills/workflow-design/guard/src/cli.ts deadline start --minutes 360
false  cd guard && bun src/cli.ts deadline start
```
`bun $G deadline start` holds no `/src/cli.ts` before `deadline`, so it is missed too.

## What it caused (run 20261018-finish-everything, report.md)
After that run's own deadline was ended, every call of the session and of its workflow agents got "harness-guard time
is up (N min over)"; one workflow's two steps stopped at their first call and were rerun.
