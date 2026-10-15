# E2 round 1 — after M1 round 2 (shell segments), same corpus, same labeller (the main agent)

| Measure | Round 0 | Round 1 |
|---|---|---|
| Lint denies | 37 | 14 |
| — real | 6 | **14** (6 codex-stdin; 10 opencode-parallel = 8 distinct commands — `( … opencode run … ) &` groups, 2 of them `for` loops starting four at once, the shape that produced "database is locked") |
| — false | 31 | **0** |
| Recognised engine calls | 273 | 158 |
| Crude hits not recognised | 12 | 126 — by reading each category: 57 only in heredoc or quoted text, 42 `--help` calls, `grep`/`pgrep`/`echo` text — all correctly not calls; **3 real misses**: `for … ; do timeout N opencode run …` (the segment starts with the shell keyword `do`); plus the 2 `dispatch.py run` calls not in scope |

**Against the prediction:** false denies > 0 before tuning — held (31); after round 2, 0. Hold-out (N5): the 6
codex-stdin occurrences and 8 opencode-parallel starts, none of which were among the 7 recorded traps the catalogue
was written from — caught. Recognition misses > 0 — held: 3 real (`do` keyword), carried to the enhance round.
The opencode-parallel hits were not caught in round 0 because the lint read `&` only at the end of the whole string.
