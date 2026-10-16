# State — run 20261016-six-experts (plan B, time-boxed: 4 hours or 6 rounds, whichever first)

Plan: `~/.claude/plans/six-experts-dave-insights.md`. Branch `feat/six-experts`, worktree `../ancient-games-six`.
Start 2026-10-16 14:19 +0800 · **deadline 18:19 +0800** · 6 rounds.

## Rounds
| # | Round | State |
|---|---|---|
| 1 | research + experts decide Q1, Q2 | done: research/context-windows.md (R1–R16), experts-q1q2(-opencode)/, D1, D2 |
| 2 | insight index + categories | done in the tree: guard Round 11 (insight index/show), 6 categories, Category: override |
| 3 | Dave loads insights; Dario | done (08ac07c) |
| 4 | rename to six-experts | moved first (renaming after editing would do the work twice): done in the tree, not committed |
| 5 | tests, mutants, review | done: 15+25 tests, 7/7 mutants, dsh review 8 findings fixed (ff83d32, cac39ff) |
| 6 | trial, all six, n=1 | done: trial/compare.md (Dave 216 s vs Dario 70 s; not judged) |

## Provisional decisions (item 14; the owner accepts or declines at the end)
- **D1 the 6 categories and the pick.** config · tool · test · guard-check · spec · own-work — the Source kinds, with
  `check` split into test / guard-check and `instruction` into spec / own-work (范蠡's and 孫子's structure, plain
  names). Placed by rules in `guard/data/insight-categories.yaml` (Source, then title words); a section's own
  `Category:` line wins. Picking: (c) both — the main agent names categories in the question, Dave reads the one-line
  index, may add sections, cites every id, and says in one line if a named category was wrong (all four; 老子's line).
  Dissent kept: Linus — "six is EJ's number … not something today's corpus supports"; 老子 — sort by the moment the
  fix belongs. Measured: the title rules misplaced at least 5 of my own instruction sections (spec items read as
  own-work); fixed with `Category: spec` lines in my files; other sessions' sections are placed by the rules alone.
- **D2 Dave's engine:** Claude Sonnet 5.5 for Dave and Dario alike (Linus, 孫子, 老子; 范蠡 said Opus), the insights
  as a stable prefix; ≈$0.03–0.05 per question at today's ≈25k tokens (research R1–R4). Revisit when one question's
  load passes 100k tokens (孫子) — today ≈25k for all of it.
- **D3 No Workflow script for rounds 5–6.** Every node is an outside CLI (opencode, dsh, agy) that must run one at a
  time (opencode) or is already orchestrated by the six-experts runner; a workflow would wrap each call in a Claude
  agent that only runs the command. EJ's "always use workflows when possible" is kept for multi-agent Claude work.
- P0 "whichever first" for 4 hours vs 6 rounds — main agent's reading of "4 hours , 6 rounds".

## Conflicts named (Rule 7)
- **Dario vs the 2026-10-13 removal of the plain control.** Memory `four-experts-skill.md`: EJ removed the plain
  no-persona control ("don't want the control with no persona"). Today EJ: "let's create a plain-Claude control called
  Dario". The newer instruction wins; the memory is updated when the skill changes. Flagged by the plan A session.

## Log
- 14:19 start; worktree from 740c842; plan A's session (ancient-games-32) told about the insight index and the rename.
- 14:2x plan A's session: not building `insight index` (go ahead); its commits 7306ddd, 740c842 are in this branch; the rename must update tests/test_four_experts_codex_quota.py.
- 14:2x round 4 done early: git mv four-experts → six-experts, four_experts.py → six_experts.py, the quota test → test_six_experts_codex_quota.py (8/8); live references moved (run-folder names kept); engines.yaml accepts both script names; SIX_EXPERTS_SEATS falls back to FOUR_EXPERTS_SEATS.
- 14:2x Dario added (plain seat, brief-plain.md, check reads sections only); the runner now waits for a running opencode expert before starting another (the 'database is locked' trap; Linus is on opencode while Codex has 0%).
- 14:3x round 1 done (4 experts; Linus and 老子 rerun after F-7f938bdf); round 2 done in the tree.
- 14:5x plan A's session asked to wait before merging: uncommitted mcode fallback for Linus in four_experts.py and its tests; merge waits for its commit message, then carries the change into six_experts.py.
- 15:1x round 6 trial: all six answered, check PASS; compare.md written; open: the index includes nested experiment insight files.
