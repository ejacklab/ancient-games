# Answers to the review (`nodes/review.result.md`, Codex gpt-6.1-sol, effort high, read-only)

| # | Finding | Answer | Where |
|---|---|---|---|
| 1 | malformed doctor `guard` ([] or {}) crashes gather | fixed: the whole Round 7 shape is checked before any line is built, so a non-string guard is "unexpected output" | `harness_health.py` `GUARD_SHAPE`; HH-29 (`guard=[]`, `guard={…}`) |
| 2 | incomplete payloads accepted | fixed: every field of each command's shape, present and typed (`answers`, `health`, `check`, `engine`, `invalid`, `unreadable`, null elements) | HH-29, 11 planted shapes; mutants M10–M12 killed |
| 3 | JSON lost through a bun consumer's pipe | not changed, with reason: not reproduced outside the Codex sandbox — 0 of 80 child runs lost output (5 B to 300 KB, `process.stdout.write` then `process.exit`), the guard suite passes 1187/1187 here while the reviewer's sandbox failed 41 tests including old CLI tests. Same cause as F-76013d09 (sandbox). Recorded as F-0a1f3ca1 | `insight.md` |
| 4 | R13 reference not in the exported skill | fixed: `tools/export_skills.py` copies a single-file skill's `references/`; a test checks every named reference resolves in the bundle (shown failing on the old export for requirement-check) | `tests/test_skills_export.py` |
| 5 | "each requirement binds only once accepted" widens R13.5 | fixed: "a suggested one binds only after the user accepts it, and an edited one needs a new acceptance" | `requirement-check/SKILL.md` |
| 6 | "Check, in this order" adds an order | fixed: "Check each of these against the rule" | same |
| 7 | Limits uses a reported source (F4) | fixed: the older-summary sentence removed; Limits keeps only F1 (verified) and the 403s | same |
