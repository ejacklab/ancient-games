# State — 20261015-sot-leftovers

Rules: one writer at a time. Read this file before your step; update it after. It holds progress and results only —
never reasoning. Never delete a log line.

## Challenge (verbatim)

EJ, 2026-10-15: *"fix the item 10 leftovers with a proper designed workflows"* — item 10 of the TODO in
`runs/20261014-sot-yaml-review/state.md`.

## Steps

| # | Step | Status | Output |
|---|---|---|---|
| D | Design | done | workflow-design.md |
| P1 | Experts on the unclear spots; EJ's decisions | done (老子 rerun pending) | experts/compare.md |
| P2 | Edits | done | nodes/baseline-p2.txt, checks/ |
| P3 | Blind review, planted contradiction | done: plant found (attempt 1); repairs reviewed (attempt 2) | nodes/p3-1.result.md, nodes/p3-2.result.md, nodes/plant-p3-1.txt |
| P4 | Close | done; commit waits for EJ | nodes/baseline-p4.txt |

## Unclear spots

| id | What is unclear | Kind | Blocks | Depends on |
|---|---|---|---|---|
| U1 | May `covers`, `source`, `depends_on` change after the first commit (K4.3)? | decision | P2 step 2 | — |
| U2 | Who decides which agents work on the project (Rd3.1a)? | decision | P2 step 3 | — |
| U3 | Tool keeps the example limit, or reads limits from a file? | decision | P2 step 3 | U2 |
| U4 | Each engine's real start-file limit | unknown | nothing here (out of scope) | — |
| N1 | If `covers` may change (U1), what a merge keeps when two branches change it differently (W6.3a) — Linus | decision | P2 step 2 | U1 |
| U5 | Paths relative to the design folder? | decision | P2 step 1 (L3) | — |

## Log (append only)

- 2026-10-15 D done: design written. Facts read: `tools/memory_index.py:35-36` `MAX_LINES = 200`, `MAX_BYTES = 24_000`, commented "the design's example, not a measurement"; `docs/index-md/` B4.1 says the same; YAML W6.3b `check: tool`, K6.3b `check: reviewer`; the vision file and `CACHES.md` are in `docs/memory-system/`.
- 2026-10-15 P1 experts: Linus, 孫子, Dave answered; 老子's first run returned an empty answer (opencode, 28 bytes), rerun started. Folded in, marked by who raised them: separate structure check `checks/yaml_check.py` (孫子), path check `checks/paths.py` (Dave: the build script never checks file paths), baseline by failing-test id `nodes/baseline-p2.txt` (Dave), review covers release note and repairs and gets EJ's decisions (Linus). New decision spot N1 (Linus). Path check: all three kit paths already resolve from `docs/memory-system/`.
- 2026-10-15 P2 L1 and L4 done: W6.3b `check: reviewer`; prose typo fixed. Build script and `checks/yaml_check.py` pass.
- 2026-10-15 P1 EJ's decisions (each the COO's recommended option, picked by EJ): U1 — after its first commit an entry's `covers` may be corrected in place with a `changed:` line; `source` and `depends_on` change only by superseding. N1 — a merge keeps every `covers` path either side wrote. U2/U3 — the project owner decides which agents work on the project; Rd3.1a says the tool holds the example until measured limits are recorded; the tool build and U4's measurement go to the TODO. U5 — paths relative to the YAML's folder; the design, the YAML, `CACHES.md` and `vision-statements/` travel together.
- 2026-10-15 P2 done: K4.3, W6.3a, Rd3.1a/b, YAML `kit` key, two prose sentences, release-note entry. Build script, `checks/yaml_check.py` and `checks/paths.py` pass.
- 2026-10-15 P3 attempt 1 (claude-sonnet-5-5, 86k tokens): the plant was found (C1: the prose let `source` be corrected in place; the real prose does not). Real findings fixed by the COO: C2 (merge conflicts are not only in added lines), C3 (`kit` says which paths are relative to what), C4 (Rd3.1a states the interim 200 lines / 24,000 bytes). O1–O5 to the TODO.
- 2026-10-15 P3 attempt 2, the repairs only (Linus N3; 84k tokens): C2, C3, C4 repaired; new N1, N3, N4, N5 fixed by the COO; N6 is EJ's "covers only"; N2, N7 to the TODO. Build script, `checks/yaml_check.py`, `checks/paths.py` pass.
- 2026-10-15 P4: baseline at the end by test id — the same single failure (`test_skills_export_is_current`, another session's uncommitted skill edits), 993 passed, as at P2 start. Release notes updated. Committed with this state file.
