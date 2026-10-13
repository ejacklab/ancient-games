# Readiness — 20261013-research-tags-retag

Checked by the COO, 2026-10-13.

## Tools

| Tool | Status | Proof |
|---|---|---|
| python3 3.12.3, node v22.22.1, git 2.43.0, codex-cli 0.160.0 | verified | `readiness.py` inventory |
| `dsh headless` (DeepSeek `deepseek-flash`) | verified today | ran 孫子 in `runs/20261013-four-experts-relay-tags/step-3-sun-tzu/` — `status.json`: engine dsh, ok true |
| research-agent-memory.js offline harness | verified | `node runs/20261011-agent-memory-graph/sabotage-harness.mjs` → "all 14 cases behave as designed" |
| pytest baseline | verified | 684 passed, 1 failed (`test_skills_export_is_current`, skills/ uncommitted) |
| `tools/export_skills.py` | verified | ran 2026-10-13, changed only this session's files |

## Skills

`four-experts` (method 3.3 / 3.5 calls), `requirement-check` (if a definition change comes back to EJ).

## Information

| What | Found | Effect |
|---|---|---|
| The 143 accepted rows | `docs/research/20261011-agent-memory-graph-r2/FINDINGS-s1..s5.md`: 143 rows, labels 94 verified / 44 reported / 3 unproven / 2 unknown; 7 rows carry `|` inside the Source | fast path; R1 joins the extra cells |
| `runs/…-r2/verify/sections/` | s1, s3, s4, s5 identical to docs/research; **s2 differs at F8** — the verifier's planted copy | not used (U2) |
| Old definitions the rows were labelled under | `research-agent-memory.js` lines 64–65 at `HEAD` (four labels) | quoted before piece A edits it (U8) |
| New definitions | `docs/RESEARCH_TAGS.md`, "The tags" | quoted verbatim into R5's brief |
| Label leaks | 13 of 143 Finding texts contain verified / reported / unproven / unknown / primary / secondary | counted in R1 (U5) |
| Bundle path convention | `skills/README.md` "What travels"; 16 `docs/…` paths already in bundled references | B adds a mapping line (U9) |
