# State — 20261012-caches-requirements-review

EJ, 2026-10-12: *"use your subagents, codex and opencode to review them"* — the Build / Keep / Read requirements in
`docs/memory-system/CACHES.md` and today's vision edits. Read-only reviews; nothing is merged from here without EJ.

- Inputs snapshotted in `inputs/` (CACHES.md, vision, diff against HEAD). Brief: `briefs/review.md`.
- Reviewers: codex (`gpt-6.1-sol`, high, read-only), opencode (`MiniMax-M3.1-Flash-Preview`, plan agent), Claude
  subagent (fresh context). Launched by `run.sh` and from the session.

## Log
- 2026-10-12T14:54:53Z launched codex + opencode (run.sh), Claude subagent
- 2026-10-12T14:58:39Z codex+opencode done: [exited with code 0]
- 2026-10-12T14:58:49Z read codex (REPAIR, 12 findings) and opencode (REPAIR, 5 high + 15 medium/low); waiting on Claude
- 2026-10-12T15:01:25Z Claude review done (REPAIR). Synthesis written: reviews/synthesis.md. Two questions for EJ; no docs changed from the reviews.
- 2026-10-12T15:02:57Z EJ: full-text trigger = B1.1 comparison; K3 cost part dropped. Applied to CACHES.md (rule, routing row, FTS why 4, 5W1H When, K3.1, K3 rebuild-cost table, SEZA K3 line) and the vision's 'Too many entries' line.
- 2026-10-12T15:24:46Z EJ: apply wording and citation fixes. Applied to CACHES.md requirements (B1.1 scoring/citation/rerun, B1.2 miss def + hybrid wording, B2, B3, B4 reference set, K1/K2 citations, K3.1, Rd1 CP6, Rd3.3, Rd4.1, rules heading). New requirements (decision record, concurrency, replayable record) not applied.
- 2026-10-12T15:36:54Z EJ: 'yes, write them in'. Added B1.0 decision record, K2.2/K2.3, Rd4.4-Rd4.6 (proposed); questions/ in SOURCE_OF_TRUTH.md (layout, Rd1.1, Rd2.2).
- 2026-10-12T15:40:35Z EJ: no splitting; removed code-graph section from CACHES.md (synced current version to docs/code-graph/CODE_GRAPH.md first), title, two Part 1 rows, rule/cost lines.
- 2026-10-12T15:45:27Z EJ: 'others can accept and apply'. CACHES.md requirements accepted except Rd4.3 (questions/); vision re-accepted with who-decides, grep figure, G-F5 label, stale never-line; Part 2 moved out; B4 status dropped. questions/ explained, pending EJ.
- 2026-10-12T15:52:26Z EJ: 'yes , made that change' — full question log dropped. Rd4 = misses noted in journal + question set built per comparison; questions/ removed from SOURCE_OF_TRUTH.md; vision test wording updated.
