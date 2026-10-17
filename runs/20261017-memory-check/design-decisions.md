# Design decisions after the experts' research (research-q/compare.md)

The main agent's pick for each question, applied to `memory_check/REQUIREMENTS.md` (R12.3: applied and reported; the
owner may overrule). Each line: the question, the pick, why.

1. Snapshot — the staged state for files (memory_index.py --check's view), named in the report's first line (C5). Five
   experts: --check reads staging, not the working tree.
2. Required locations — AGENTS.md required; absent project-memory/ is not applicable, report only (F1, C4). So this
   repo is not warned every session.
3. memory_index.py — unchanged; parsed, output pinned by tests; the tool adds only the clauses it misses (C3).
4. Results — pass, fail, needs a reviewer, not applicable, could not run; exit 1 when a MUST fails or could not run
   (C2, R3).
5. Mixed tool+reviewer records — a tool-found break fails, else needs a reviewer (C2).
6. git labels git cannot back (W2.1b, W5.1, K1.1; W6.1b, W6.2) — needs a reviewer, reported to the owner; the YAML is
   not edited (C1; one design, one document).
7. Caches v1 — B2.2 and Rd1 only (C6).
8. Session hook — locations, index, index size; never opens .cache; ids, not entry text (R2).
9. History — since the first commit touching project-memory/, --since, range printed; shallow clone could not run (C5).
10. Guidelines copy — the tool's own, version printed (C1).
11. --project — a git root, else a usage error (F2).
12. Ids — prefixed SoT: and CACHES: (C1).
13. Expected INDEX.md — literal bytes by hand (T1; the known-answers lesson).
14. Expected answers — by an engine that did not write the code (T1; crossed-build-check).
15. A real project to calibrate on — none known; fixtures only, said in the report. (The owner may name one.)
16. The method change (a question trials cannot answer goes to the owner at once) — the owner's; not applied.
