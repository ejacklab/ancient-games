# Report — run 20261016-time-monitor (time-boxed: 60 min, 10:22 → 11:22 +0800)

**Done in about 19 minutes; nothing asked of the owner during the run.** Criteria 7/7 (`criteria.yaml`).

## What was built
- **The three time monitors** (guard Round 10, method 3.8 item 14):
  1. *A check:* `guard/src/cli.ts deadline status` — used/left, the deadline, and each worker's progress.
  2. *A timer:* `deadline wait [--mark P]`, run in the background, returns at the deadline (or a mark).
  3. *The guard tells you:* after every tool call a one-line `harness-guard clock: 9/57 min (16%), 48 left`; at 50%,
     80% and 100% a fuller block with the workers' progress; after the deadline, time-up on every call. `deadline
     start --minutes N --run runs/<run>` begins it (claimed by the call that ran it); `deadline end` stops it early.
     The first prompt of a session asks for the time if none is set.
- **Workers report while they work:** every brief (`docs/workflow-templates/node-brief.md`) asks for small pieces
  listed first and a timestamped line as each starts and ends; `deadline status` and the 50/80/100% blocks show them.
  The four-experts runner writes the same lines (`--progress`) and records each expert's start and finish.
- **The experts know the pattern:** their brief has "How we work — the pattern you adapt and improve" (time set at
  the start, small timestamped pieces, vision and use cases first, research not recall, workflows when possible).
- **"Workflows when possible"** is in method 3.8 item 14 and in my memory as a standing preference.

## How it was checked
- Tests: 42 by Codex from the spec alone (its progress file showed 7 pieces, 10:23–10:26), plus 8 by me; 6 of mine
  failed on the code before the review fixes. Guard 1264/1264, tsgo clean, Python 1083.
- 12 planted mutants, all killed (`mutants.txt`, `mutants-after-optimise.txt`). I planted them.
- An independent review (Codex, high effort, wrote none of the code): 10 findings, all fixed or answered
  (`review-answers.md`). Its sandbox could not capture bun's output, so its 47 suite failures are that, not the code.
- Live in this session: the clock appeared after every Bash and Write call from 10:25 on.

## Optimisation (measured)
The guard's added cost per tool call, in-process, 300 calls × 3: **+0.17 ms before → about 0 after** (the workers'
files are read only for a mark block, the journal only after the first mark). Past the first mark: not measured.

## Provisional decisions — yours to accept or decline (state.md)
- **D1** the clock after every tool call, not only at 50/80/100% — research F1–F8 (`research/reminders.md`: every
  tested design shows the budget at every step; a budget given once fails) and 5/5 experts (`experts/`).
- **D2** the guard runs after every tool, not only Bash and writes — the review showed Read/Grep/web calls would never
  see the clock; one hook run is 0.02 s.

## Waiting for you (safety bounds)
- **Your installed hooks still use the old matchers**, so the clock reaches only Bash, Write and Edit calls. To get it
  on every tool, update `~/.claude/settings.json` from `bun .claude/skills/workflow-design/guard/src/cli.ts install
  --print claude-code` (the PostToolUse and PostToolUseFailure entries lose their `matcher`). I did not edit it.
- **Push:** committed on master, not pushed.

## Failures and insights (`insight.md`)
F-173e0190 (four-experts runner swallowed Dave's prompt — fixed), F-84636a96 (a quote with a variant character 為/爲),
F-a03fa5b3 (I typed a deadline time from memory, a year off — the guard refused it). Each has 2–3 fix options for you.
